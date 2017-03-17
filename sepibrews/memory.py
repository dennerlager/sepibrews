#!/usr/bin/env python
from __future__ import print_function, division
import unittest

class Register():
    def __init__(self, address):
        self.address = address

class Memory():
    def __init__(self):
        self.registers = {
            'process_value': Register(0x1000),
            'set_point': Register(0x1001),
            'upper_limit': Register(0x1002),
            'lower_limit': Register(0x1003),
            'input_temp_sens_type': Register(0x1004),
            'control_method': Register(0x1005),
            'heating_cooling_control_selection': Register(0x1006),
            'histeresis_1st_output': Register(0x1010),
            'histeresis_2nd_output': Register(0x1011),
            'output_value_1': Register(0x1012),
            'output_value_2': Register(0x1013),
            'temp_regulation_value': Register(0x1016),
            'led_status': Register(0x102a),
            'push_butten_status': Register(0x102b),
            'lock_status': Register(0x102c),
            'software_version': Register(0x102f),
            'communication_enabled': Register(0x810),
            'at_setting': Register(0x813),
            'control_run_stop': Register(0x814), }

    def getRegisterAddress(self, name):
        return self.registers[name].address

class Memory_test(unittest.TestCase):
    def setUp(self):
        self.mem = Memory()

    def tearDown(self):
        pass

    def test_getRegisterAddress_page0(self):
        address = self.mem.getRegisterAddress('process_value')
        self.assertEqual(address, 0x1000)

    def test_getRegisterAddress_raises(self):
        self.assertRaises(KeyError, self.mem.getRegisterAddress, 'asdf')

if __name__ == '__main__':
    unittest.main()
