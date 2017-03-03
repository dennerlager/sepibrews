#!/usr/bin/env python
from __future__ import print_function, division

class Cn7800Mock():
    def __init__(self, slaveAddress):
        pass
    
    def getTemperature(self):
        return self.temperature

    def setTemperature(self, temperature):
        self.temperature = temperature
        
    def start(self):
        pass

    def stop(self):
        pass
        
