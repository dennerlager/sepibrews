import sys
import time
import logging
import logging.handlers
import progressbar
from queue import Empty
from cn7800 import Cn7800
from parser import Parser
from cn7800mock import Cn7800Mock
from recipe_builder import RecipeBuilder
from multiprocessing import Process, Queue, Lock
from serial.serialutil import SerialException
from totalRemainingTimeEstimator import TotalRemainingTimeEstimator
sys.path.append('./recipes/')

class ExecutionEngine(Process):
    def __init__(self, tempControllerAddress, inq, outq, interfaceLock):
        Process.__init__(self)
        self.tempControllerAddress = tempControllerAddress
        self.inq = inq
        self.outq = outq
        self.setupLogger()
        self.parser = Parser(self)
        try:
            self.tempController = Cn7800(self.tempControllerAddress, interfaceLock)
        except SerialException:
            self.logger.info('interface not found, using mock')
            self.tempController = Cn7800Mock(self.tempControllerAddress, interfaceLock)
        self.isStopReceived = False
        self.resetRecipe()
        self.recipe = None
        self.isStepTempReached = None
        self.elapsedStepTime = None
        self.currentStep = None

    def setupLogger(self):
        self.logger = logging.getLogger('{}_{}'.format(
            __name__, self.tempControllerAddress))
        self.logger.setLevel(logging.INFO)
        fh = logging.handlers.RotatingFileHandler(
            'ee_{}.log'.format(self.tempControllerAddress),
            maxBytes=20000,
            backupCount=5)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def resetRecipe(self):
        self.recipe = None
        self.isStepTempReached = False
        self.elapsedStepTime = 0
        self.currentStep = 0

    def setRecipe(self, recipe):
        self.logger.info('set recipe: {}'.format(recipe))
        self.recipe = RecipeBuilder().parse(recipe)

    def __del__(self):
        self.tempController.stop()

    def run(self):
        self.logger.info('process started')
        while True:
            self.handleCommunication()

    def handleCommunication(self):
        try:
            commandstring = self.inq.get(block=True, timeout=0.5)
        except Empty:
            return
        self.logger.debug('command received: {}'.format(commandstring))
        command = self.parser.parse(commandstring)
        self.outq.put(command.execute())

    def execute(self):
        self.logger.info('recipe started')
        self.isStopReceived = False
        self.tempController.start()
        for stepindex, step in enumerate(self.recipe):
            self.currentStep = stepindex
            self.isStepTempReached = False
            self.waitTillTempReached(step.temperatureC)
            self.isStepTempReached = True
            self.holdTemperatureFor(step.durationSec)
        self.stopExecution()

    def stopExecution(self):
        self.logger.info('recipe stopped')
        self.tempController.setTemperature(0)
        self.tempController.stop()
        self.isStopReceived = True
        self.resetRecipe()

    def waitTillTempReached(self, temperatureC):
        print('changing temperature to {:.1f}C'.format(temperatureC))
        self.logger.info('set temperature to {}'.format(temperatureC))
        self.tempController.setTemperature(temperatureC)
        if temperatureC == -1:
            return
        with progressbar.ProgressBar(
                max_value=progressbar.UnknownLength) as bar:
            i = 0
            while not abs(self.tempController.getTemperature() - temperatureC) < 0.1:
                self.handleCommunication()
                if self.isStopReceived:
                    break
                bar.update(i)
                i += 1
        self.logger.info('temperature reached')

    def holdTemperatureFor(self, durationSec):
        print('hold temperature for {}seconds'.format(durationSec))
        durationSec = int(durationSec)
        startTime = time.time()
        stopTime = startTime + durationSec
        self.elapsedStepTime = 0
        with progressbar.ProgressBar(max_value=durationSec) as bar:
            while time.time() < stopTime:
                self.elapsedStepTime = time.time() - startTime
                self.handleCommunication()
                if self.isStopReceived:
                    break
                bar.update(min((time.time() - startTime, durationSec)))

    def getSetValue(self):
        return self.tempController.getSetValue()

    def getTemperature(self):
        return self.tempController.getTemperature()

    def getTotalRemainingTime(self):
        return (TotalRemainingTimeEstimator(
            self.recipe,
            self.tempController.temperatureChangeRateCperSec)
                .estimateRemainingSeconds(self.currentStep,
                                          self.getTemperature(),
                                          self.elapsedStepTime,
                                          self.isStepTempReached))

    def getRemainingStepTime(self):
        try:
            rstime = (self.recipe.steps[self.currentStep].durationSec -
                    self.elapsedStepTime)
            return rstime if rstime > 0 else 0
        except (AttributeError, TypeError):
            return 0

if __name__ == '__main__':
    qToEe = Queue()
    qFromEe = Queue()
    ee = ExecutionEngine(1, qToEe, qFromEe, Lock())
    ee.setRecipe('./recipes/test.csv')
    ee.execute()
