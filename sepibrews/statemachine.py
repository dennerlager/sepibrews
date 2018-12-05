import logging
import logging.handlers
from multiprocessing import Queue
from execution_engine import ExecutionEngine

class StateMachine():
    def __init__(self, brewView, tempControllerAddress, interfaceLock):
        self.brewView = brewView
        self.tempControllerAddress = tempControllerAddress
        self.qToEe = Queue()
        self.qFromEe = Queue()
        self.ee = ExecutionEngine(self.tempControllerAddress,
                                  self.qToEe,
                                  self.qFromEe,
                                  interfaceLock)
        self.ee.start()
        self.setupLogger()

    def setupLogger(self):
        self.logger = logging.getLogger('{}_{}'.format(
            __name__, self.tempControllerAddress))
        self.logger.setLevel(logging.INFO)
        fh = logging.handlers.RotatingFileHandler('statemachine.log',
                                                  maxBytes=20000,
                                                  backupCount=5)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def start(self):
        self.logger.info('start')
        self.logger.info('selected recipe: {}'.format(self.brewView.getRecipe()))
        self.qToEe.put('{} {}'.format('setRecipe', self.brewView.getRecipe()))
        self.qToEe.put('start')

    def stop(self):
        self.logger.info('stop')
        self.qToEe.put('stop')

    def quit(self):
        self.logger.info('quit')
        self.qToEe.put('quit')
        self.ee.join()

    def updateViews(self):
        self.logger.debug('update views')
        self.clearQFromEe()
        self.updateSv()
        self.updatePv()
        self.updateRemainingStepTime()
        self.updateTotalRemainingTime()

    def clearQFromEe(self):
        for i in range(self.qFromEe.qsize()):
            self.qFromEe.get()

    def updateSv(self):
        self.qToEe.put('getSv')
        sv = self.qFromEe.get()
        if not sv == None:
            self.brewView.setSetValue(sv)

    def updatePv(self):
        self.qToEe.put('getPv')
        pv = self.qFromEe.get()
        if not pv == None:
            self.brewView.setProcessValue(pv)

    def updateRemainingStepTime(self):
        self.qToEe.put('getRemainingStepTime')
        rst = self.qFromEe.get()
        if not rst == None:
            self.brewView.setStepTimeLeft(rst)

    def updateTotalRemainingTime(self):
        self.qToEe.put('getTotalRemainingTime')
        trt = self.qFromEe.get()
        if not trt == None:
            self.brewView.setTotalTimeLeft(trt)
