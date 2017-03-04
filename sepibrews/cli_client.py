#!/usr/bin/env python
from __future__ import print_function, division
import unittest
from multiprocessing import Queue
from execution_engine import ExecutionEngine
from Queue import Empty

if __name__ == '__main__':
    qToEe = Queue()
    qFromEe = Queue()
    slaveAddress = 1
    ee = ExecutionEngine(slaveAddress, qToEe, qFromEe, './recipes/test.csv')
    ee.start()
    while True:
        command = raw_input('command: ')
        if command == 'q':
            break
        qToEe.put(command)
        try:
            print('respone: {}'.format(qFromEe.get(block=True, timeout=1)))
        except Empty:
            print('timed out')
    qToEe.put('stop')
    ee.join()
