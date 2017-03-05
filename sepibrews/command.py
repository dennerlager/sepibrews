#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import sys

class Command():
    """Use factory method 'create(command_name)' to instantiate"""

    @staticmethod
    def create(command_name, executionEngine):
        if command_name == 'start':
            return StartCommand(executionEngine)
        elif command_name == 'stop':
            return StopCommand(executionEngine)
        elif command_name == 'getPv':
            return GetPvCommand(executionEngine)
        elif command_name == 'getSv':
            return GetSvCommand(executionEngine)
        elif command_name == 'getStepTime':
            return GetStepTimeCommand(executionEngine)
        elif command_name == 'getTotalTime':
            return GetTotalTimeCommand(executionEngine)
        else:
            raise ValueError("no such command: {}".format(command_name))

    def __init__(self, executionEngine):
        self.executionEngine = executionEngine

    def execute(self):
        raise NotImplementedError()

class StartCommand(Command):
    def execute(self):
        self.executionEngine.execute()

class StopCommand(Command):
    def execute(self):
        self.executionEngine.stopExecution()
        sys.exit()

class GetPvCommand(Command):
    def execute(self):
        return self.executionEngine.getTemperature()

class GetSvCommand(Command):
    def execute(self):
        return self.executionEngine.getSetValue()

class GetStepTimeCommand(Command):
    pass        

class GetTotalTimeCommand(Command):
    pass        

class CommandCreationTest(unittest.TestCase):
    def test_instantiate_raises(self):
        self.assertRaises(ValueError, Command.create, 'asdf', 'ee')

    def test_startCommand(self):
        self.assertIsInstance(Command.create('start', 'ee'), StartCommand)

    def test_stopCommand(self):
        self.assertIsInstance(Command.create('stop', 'ee'), StopCommand)

    def test_getPvCommand(self):
        self.assertIsInstance(Command.create('getPv', 'ee'), GetPvCommand)

    def test_getSvCommand(self):
        self.assertIsInstance(Command.create('getSv', 'ee'), GetSvCommand)

    def test_getStepTimeCommand(self):
        self.assertIsInstance(Command.create('getStepTime', 'ee'), GetStepTimeCommand)

    def test_getTotalTimeCommand(self):
        self.assertIsInstance(Command.create('getTotalTime', 'ee'), GetTotalTimeCommand)

if __name__ == '__main__':
    unittest.main()
