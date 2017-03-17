#!/usr/bin/env python
from __future__ import print_function, division
import unittest
from memory import Memory
from interface import Interface

class Cn7800():
    def __init__(self, slaveAddress):
        self.memory = Memory()
        self.sif = Interface(slaveAddress)

    def readRegister(self, name):
        return self.sif.readRegister(self.memory.getRegisterAddress(name))

    def writeRegister(self, name, data):
        self.sif.writeRegister(self.memory.getRegisterAddress(name), data)

    def readBit(self, name):
        return self.sif.readBit(self.memory.getRegisterAddress(name))

    def writeBit(self, name, data):
        self.sif.writeBit(self.memory.getRegisterAddress(name), data)

    def getTemperature(self):
        return self.readRegister('process_value') / 10

    def setTemperature(self, temperature):
        temperature = round(temperature, 1) * 10
        self.writeRegister('set_point', temperature)

    def getSetValue(self):
        return self.readRegister('set_point') / 10

    def start(self):
        self.writeBit('control_run_stop', True)

    def stop(self):
        self.writeBit('control_run_stop', False)

class Cn7800test(unittest.TestCase):
    def setUp(self):
        self.tc = Cn7800(1)

    def test_readRegister(self):
        self.assertEqual(self.tc.readRegister('upper_limit'), 6000)

    def test_writeRegister(self):
        before = self.tc.readRegister('set_point')
        after = before + 1
        self.tc.writeRegister('set_point', after)
        self.assertEqual(self.tc.readRegister('set_point'), after)
        self.tc.writeRegister('set_point', before)

    def test_getTemperature(self):
        self.assertTrue(10 < self.tc.getTemperature() < 45)

    def test_setTemperature(self):
        self.tc.setTemperature(12.46)
        self.assertEqual(self.tc.readRegister('set_point'), 125)

    def test_getSetValue(self):
        self.tc.setTemperature(12)
        self.assertEqual(self.tc.getSetValue(), 12)

    def test_readBit(self):
        self.assertEqual(self.tc.readBit('communication_enabled'), True)

    def test_writeBit(self):
        before = self.tc.readBit('control_run_stop')
        self.tc.writeBit('control_run_stop', not before)
        self.assertEqual(self.tc.readBit('control_run_stop'), not before)
        self.tc.writeBit('control_run_stop', before)

if __name__ == '__main__':
    unittest.main()
