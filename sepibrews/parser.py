#!/usr/bin/env python
from __future__ import print_function, division
import unittest
import command

class Parser():
    def __init__(self, executionEngine):
        self.ee = executionEngine

    def parse(self, commandname):
        return command.Command.create(commandname, self.ee)

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.p = Parser('ee')

    def test_start(self):
        self.assertIsInstance(self.p.parse('start'), command.StartCommand)

if __name__ == '__main__':
    unittest.main()
    
