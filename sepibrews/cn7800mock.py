import time

class Cn7800Mock():
    def __init__(self, slaveAddress, interfaceLock):
        self.temperatureChangeRateCperSec = 1
        self.processValue = 25
        self.setValue = 25
        self.atTemperature = True
        self.timeTemperatureSet = time.time()
        self.slaveAddress = slaveAddress
        self.interfaceLock = interfaceLock

    def getTemperature(self):
        if self.atTemperature:
            return self.setValue
        timeElapsed = time.time() - self.timeTemperatureSet
        tempStep = abs(self.processValue - self.setValue)
        timeNeededForChange = tempStep / self.temperatureChangeRateCperSec
        if timeElapsed > timeNeededForChange:
            self.atTemperature = True
            self.processValue = self.setValue
            return self.setValue
        else:
            return self.processValue + timeElapsed * self.temperatureChangeRateCperSec

    def setTemperature(self, temperature):
        self.timeTemperatureSet = time.time()
        self.setValue = temperature
        self.atTemperature = False

    def getSetValue(self):
        return self.setValue

    def start(self):
        pass

    def stop(self):
        pass
