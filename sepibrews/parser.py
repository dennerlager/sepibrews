#!/usr/bin/env python
from __future__ import print_function, division
import unittest
from execution_engine_mock import ExecutionEngine

class Parser():
    def __init__(self, executionEngine):
        self.ee = executionEngine

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.p = Parser(ExecutionEngine)

    def test_getPv(self):
        

if __name__ == '__main__':
    unittest.main()
    
