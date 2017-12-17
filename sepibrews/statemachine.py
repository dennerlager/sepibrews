#!/usr/bin/env python
from __future__ import print_function, division
from multiprocessing import Queue
from execution_engine import ExecutionEngine

class StateMachine():
    def __init__(self, brewView, tempControllerAddress):
        self.brewView = brewView
        self.qToEe = Queue()
        self.qFromEe = Queue()
        self.ee = ExecutionEngine(tempControllerAddress, self.qToEe, self.qFromEe)
        self.ee.start()

    def start(self):
        print('selected recipe: {}'.format(self.brewView.getRecipe()))
        self.qToEe.put('{} {}'.format('setRecipe', self.brewView.getRecipe()))
        self.qToEe.put('start')

    def stop(self):
        print('stop pressed')
        self.qToEe.put('stop')

    def quit(self):
        print('exit')
        self.qToEe.put('quit')
        self.ee.join()

    def updateViews(self):
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
