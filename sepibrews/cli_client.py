#!/usr/bin/env python
from __future__ import print_function, division
import unittest
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

def automaticTest():
    print('this is the automatic test')

qToEe = Queue()
qFromEe = Queue()
slaveAddress = 1
ee = ExecutionEngine(slaveAddress, qToEe, qFromEe, './recipes/test.csv')
ee.start()
response = raw_input('automatic (a) or manual (m) test?: ')
if response.startswith('m'):
    manualTest()
if response.startswith('a'):
    automaticTest()
qToEe.put('stop')
ee.join()
