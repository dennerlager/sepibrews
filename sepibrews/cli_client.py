#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import time
import sys
from multiprocessing import Queue
from execution_engine import ExecutionEngine
from Queue import Empty
from command import commands

def printAvailableCommands():
    print('possible commands:')
    for command in commands.keys():
        print(command)
    print('q to quit')

def manualTest():
    qToEe = Queue()
    qFromEe = Queue()
    ee = ExecutionEngine(1, qToEe, qFromEe)
    ee.setRecipe('./recipes/test.csv')
    ee.start()
    printAvailableCommands()
    while True:
        command = raw_input('command: ')
        if command == 'q':
            break
        if not command in commands.keys():
            continue
        qToEe.put(command)
        try:
            print('respone: {}'.format(qFromEe.get(block=True, timeout=1)))
        except Empty:
            print('timed out')
    qToEe.put('quit')
    ee.join()

class AutomaticTest(unittest.TestCase):
    def setUp(self):
        self.qToEe = Queue()
        self.qFromEe = Queue()
        self.ee = ExecutionEngine(1, self.qToEe, self.qFromEe)
        self.ee.setRecipe('./recipes/test.csv')
        self.ee.start()

    def tearDown(self):
        self.transceive('quit')
        self.ee.join()

    def test_flow(self):
        self.assertEqual(self.transceive('start'), 'timed out')
        self.assertAlmostEqual(self.transceive('getPv'), 26, delta=1)
        self.assertEqual(self.transceive('getSv'), 30)
        self.assertAlmostEqual(self.transceive('getTotalRemainingTime'), 32, delta=1)
        time.sleep(6)
        self.assertAlmostEqual(self.transceive('getRemainingStepTime'), 4.5, delta=1)

    def transceive(self, commandname):
        self.qToEe.put(commandname)
        try:
            return float(self.qFromEe.get(block=True, timeout=1))
        except Empty:
            return 'timed out'

if __name__ == '__main__':
    try:
        response = sys.argv[1]
    except IndexError:
        response = None
    while True:
        if response == 'a' or response == 'm':
            break
        response = raw_input('automatic (a) or manual (m) test?: ')

    if response == 'm':
        manualTest()
    if response == 'a':
        try:
            sys.argv[1]
        except IndexError:
            pass
        else:
            sys.argv.pop()
        unittest.main()
