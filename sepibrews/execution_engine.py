#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import progressbar
import time
import sys
from multiprocessing import Process, Queue
from Queue import Empty
from cn7800 import Cn7800
from cn7800mock import Cn7800Mock
from recipe_builder import RecipeBuilder
from parser import Parser
sys.path.append('./recipes/')

class ExecutionEngine(Process):
    def __init__(self, slaveAddress, inq, outq):
        Process.__init__(self)        
        self.inq = inq
        self.outq = outq
        self.parser = Parser(self)
        self.tempController = Cn7800(slaveAddress)

    def __del__(self):
        self.tempController.stop()

    def start(self):
        self.handleCommunication()

    def handleCommunication(self):
        try:
            commandstring = self.inq.get(block=True, timeout=0.5)
        except Empty:
            return
        command = self.parser.parse(commandstring)
        self.outq.put(command.execute())

    def setRecipe(self, recipe):
        self.recipe = RecipeBuilder().parse(recipe)        

    def execute(self):
        self.tempController.start()
        for step in self.recipe:
            self.waitTillTempReached(step.temperatureC)
            self.holdTemperatureFor(step.durationMin)
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

    def holdTemperatureFor(self, durationMin):
        print('hold temperature for {}minutes'.format(durationMin))
        durationSec = int(durationMin * 60)
        startTime = time.time()
        stopTime = startTime + durationSec
        with progressbar.ProgressBar(max_value=durationSec) as bar:
            while time.time() < stopTime:
                self.handleCommunication()
                bar.update(min((time.time() - startTime, durationSec)))

if __name__ == '__main__':
    qToEe = Queue()
    qFromEe = Queue()
    ee = ExecutionEngine(1, qToEe, qFromEe)
    ee.setRecipe('./recipes/test.csv')
    ee.tempController = Cn7800Mock(1)
    ee.execute()
