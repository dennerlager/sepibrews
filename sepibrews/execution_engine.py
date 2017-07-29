#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import progressbar
import time
import sys
from multiprocessing import Process, Queue
from serial.serialutil import SerialException
from Queue import Empty
from cn7800 import Cn7800
from cn7800mock import Cn7800Mock
from recipe_builder import RecipeBuilder
from parser import Parser
from totalRemainingTimeEstimator import TotalRemainingTimeEstimator
sys.path.append('./recipes/')

class ExecutionEngine(Process):
    def __init__(self, tempControllerAddress, inq, outq):
        Process.__init__(self)
        self.inq = inq
        self.outq = outq
        self.parser = Parser(self)
        self.isStepTempReached = False
        self.elapsedStepTime = 0
        self.currentStep = 0
        try:
            self.tempController = Cn7800(tempControllerAddress)
        except SerialException:
            print('interface not found, using mock')
            self.tempController = Cn7800Mock(tempControllerAddress)

    def setRecipe(self, recipe):
        self.recipe = RecipeBuilder().parse(recipe)

    def __del__(self):
        self.tempController.stop()

    def run(self):
        while True:
            self.handleCommunication()

    def handleCommunication(self):
        try:
            commandname = self.inq.get(block=True, timeout=0.5)
        except Empty:
            return
        command = self.parser.parse(commandname)
        self.outq.put(command.execute())

    def execute(self):
        self.tempController.start()
        for stepindex, step in enumerate(self.recipe):
            self.currentStep = stepindex
            self.isStepTempReached = False
            self.waitTillTempReached(step.temperatureC)
            self.isStepTempReached = True
            self.holdTemperatureFor(step.durationSec)
        self.stopExecution()

    def stopExecution(self):
        self.tempController.setTemperature(0)
        self.tempController.stop()

    def waitTillTempReached(self, temperatureC):
        print('changing temperature to {:.1f}C'.format(temperatureC))
        self.tempController.setTemperature(temperatureC)
        with progressbar.ProgressBar(
                max_value=progressbar.UnknownLength) as bar:
            i = 0
            while not abs(self.tempController.getTemperature() - temperatureC) < 0.1:
                self.handleCommunication()
                bar.update(i)
                i += 1

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
        return self.recipe.steps[self.currentStep].durationSec - self.elapsedStepTime

if __name__ == '__main__':
    qToEe = Queue()
    qFromEe = Queue()
    from cn7800mock import Cn7800Mock as Cn7800
    ee = ExecutionEngine(1, qToEe, qFromEe)
    ee.setRecipe('./recipes/test.csv')
    ee.execute()
