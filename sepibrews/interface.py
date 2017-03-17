#!/usr/bin/env python
from __future__ import print_function, division
import minimalmodbus as mmb

class Interface():
    def __init__(self, slaveAddress):
        self.dev = mmb.Instrument('/dev/ttyUSB0',
                                  slaveaddress=slaveAddress,
                                  mode='ascii')

    def readBit(self, address):
        return self.dev.read_bit(address)

    def writeBit(self, address, data):
        self.dev.write_bit(address, data)

    def readRegister(self, address):
        return self.dev.read_register(address)

    def writeRegister(self, address, data):
        self.dev.write_register(address, data, functioncode=6)
