import sys
import unittest

class Command():
    """Use factory method 'create(command_name)' to instantiate"""

    def __init__(self, arguments, executionEngine):
        self.arguments = arguments
        self.executionEngine = executionEngine

    def execute(self):
        raise NotImplementedError()

class StartCommand(Command):
    def execute(self):
        self.executionEngine.execute()

class StopCommand(Command):
    def execute(self):
        self.executionEngine.stopExecution()

class QuitCommand(Command):
    def execute(self):
        self.executionEngine.stopExecution()
        sys.exit()

class GetPvCommand(Command):
    def execute(self):
        return self.executionEngine.getTemperature()

class GetSvCommand(Command):
    def execute(self):
        return self.executionEngine.getSetValue()

class GetRemainingStepTimeCommand(Command):
    def execute(self):
        return self.executionEngine.getRemainingStepTime()

class GetTotalRemainingTimeCommand(Command):
    def execute(self):
        return self.executionEngine.getTotalRemainingTime()

class SetRecipeCommand(Command):
    def execute(self):
        return self.executionEngine.setRecipe(self.arguments[0])

commands = {'start': StartCommand,
            'stop': StopCommand,
            'quit': QuitCommand,
            'getPv': GetPvCommand,
            'getSv': GetSvCommand,
            'getRemainingStepTime': GetRemainingStepTimeCommand,
            'getTotalRemainingTime': GetTotalRemainingTimeCommand,
            'setRecipe': SetRecipeCommand, }

def create(command_name, arguments, executionEngine):
    try:
        return commands[command_name](arguments, executionEngine)
    except KeyError:
        raise ValueError("no such command: {}".format(command_name))

class CommandCreationTest(unittest.TestCase):
    def test_instantiate_raises(self):
        self.assertRaises(ValueError, create, 'asdf', [], 'ee')

    def test_startCommand(self):
        self.assertIsInstance(create('start', [], 'ee'), StartCommand)

    def test_stopCommand(self):
        self.assertIsInstance(create('stop', [], 'ee'), StopCommand)

    def test_quitCommand(self):
        self.assertIsInstance(create('quit', [], 'ee'), QuitCommand)

    def test_getPvCommand(self):
        self.assertIsInstance(create('getPv', [], 'ee'), GetPvCommand)

    def test_getSvCommand(self):
        self.assertIsInstance(create('getSv', [], 'ee'), GetSvCommand)

    def test_getRemainingStepTimeCommand(self):
        self.assertIsInstance(create('getRemainingStepTime', [], 'ee'),
                              GetRemainingStepTimeCommand)

    def test_getTotalRemainingTimeCommand(self):
        self.assertIsInstance(create('getTotalRemainingTime', [], 'ee'),
                              GetTotalRemainingTimeCommand)

    def test_setRecipe(self):
        self.assertIsInstance(create('setRecipe', ['./recipes/test.csv'], 'ee'), SetRecipeCommand)

if __name__ == '__main__':
    unittest.main()
