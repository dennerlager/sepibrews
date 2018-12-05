import minimalmodbus as mmb
mmb.CLOSE_PORT_AFTER_EACH_CALL = True

class Interface():
    def __init__(self, slaveAddress, interfaceLock):
        self.interfaceLock = interfaceLock
        with self.interfaceLock:
            self.dev = mmb.Instrument('/dev/ttyUSB0',
                                      slaveaddress=slaveAddress,
                                      mode='ascii')

    def readBit(self, address):
        with self.interfaceLock:
            return self.dev.read_bit(address)

    def writeBit(self, address, data):
        with self.interfaceLock:
            self.dev.write_bit(address, data)

    def readRegister(self, address):
        with self.interfaceLock:
            return self.dev.read_register(address)

    def writeRegister(self, address, data):
        with self.interfaceLock:
            self.dev.write_register(address, data, functioncode=6)
