#!/usr/bin/env python3
import sys
import time
import unittest
from queue import Empty
from command import commands
from multiprocessing import Queue, Lock
from execution_engine import ExecutionEngine

def printAvailableCommands():
    print('possible commands:')
    for command in commands.keys():
        print(command)
    print('q to quit')

def manualTest():
    qToEe = Queue()
    qFromEe = Queue()
    ee = ExecutionEngine(1, qToEe, qFromEe, Lock())
    ee.setRecipe('./recipes/test.csv')
    ee.start()
    printAvailableCommands()
    while True:
        command = input('command: ')
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
        self.ee = ExecutionEngine(1, self.qToEe, self.qFromEe, Lock())
        self.ee.start()
        self.transceive('{} {}'.format('setRecipe', './recipes/test.csv'))

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
        except TypeError:
            pass

if __name__ == '__main__':
    try:
        response = sys.argv[1]
    except IndexError:
        response = None
    while True:
        if response == 'a' or response == 'm':
            break
        response = input('automatic (a) or manual (m) test?: ')

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
