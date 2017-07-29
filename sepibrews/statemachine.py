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

    def start(self):
        print('selected recipe: {}'.format(self.brewView.getRecipe()))
        self.ee.setRecipe(self.brewView.getRecipe())
        self.qToEe.put('start')

    def stop(self):
        print('stop pressed')
        self.qToEe.put('stop')
