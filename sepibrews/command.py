#!/usr/bin/env python
from __future__ import print_function, division
import unittest

class Command():
    """Use factory method 'create(command_name, ...)' to instantiate"""

    @staticmethod
    def create(command_name, address=0x00, data=0x00):
        if command_name == 'nop':
            return NopCommand(address, data)
        elif command_name == 'page_sel':
            return PageSelCommand(address, data)
        elif command_name == 'read':
            return ReadCommand(address, data)
        elif command_name == 'write':
            return WriteCommand(address, data)
        elif command_name == 'quit':
            return QuitCommand(address, data)
        elif command_name == 'reset':
            return ResetCommand(address, data)
        elif command_name == 'row_read':
            return RowReadCommand(address, data)
        elif command_name == 'convert':
            return ConvertCommand(address, data)
        elif command_name == 'exposure':
            return ExposureCommand(address, data)
        else:
            raise ValueError("there's no command {}".format(command_name))

    def __init__(self, address, data):
        if not 0 <= address <= 0x1f:
            raise ValueError('address {} out of range'.format(address))
        self.address = address
        if not 0 <= data <= 255:
            raise ValueError('data {} out of range'.format(data))
        self.data = data    

    def get_bytelist(self):
        return [(self.cid << 5) | self.address, self.data][:]

    def __str__(self):
        return ('command name: {}, address: 0x{:0>2x}, data: 0x{:0>2x}'
                .format(self.name, self.address, self.data))

class NopCommand(Command):
    cid = 0
    name = 'nop'

class PageSelCommand(Command):
    cid = 0
    name = 'page_sel'
    def __init__(self, address, data):
        Command.__init__(self, address, data)
        if not self.address <= 4:
            raise ValueError('page {} out of range'.format(self.address))

    def get_bytelist(self):
        return [(self.cid << 5) | (self.address | 0x10), self.data]

class ReadCommand(Command):
    cid = 1
    name = 'read'

class WriteCommand(Command):
    cid = 2
    name = 'write'

class QuitCommand(Command):
    cid = 3
    name = 'quit'

class ResetCommand(Command):
    cid = 4
    name = 'reset'

class RowReadCommand(Command):
    cid = 5
    name = 'row_read'

class ConvertCommand(Command):
    cid = 6
    name = 'convert'

class ExposureCommand(Command):
    cid = 7
    name = 'exposure'

class Command_test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_instantiate_raises(self):
        self.assertRaises(ValueError, Command.create, 'asdf')

    def test_address_out_of_range(self):
        self.assertRaises(ValueError, Command.create, 'nop', -1)
        self.assertRaises(ValueError, Command.create, 'nop', 0x20)

    def test_data_out_of_range(self):
        self.assertRaises(ValueError, Command.create, 'nop', 0, -1)
        self.assertRaises(ValueError, Command.create, 'nop', 0, 256)

    def test_get_bytelist_nop(self):
        cmd = Command.create('nop')
        self.assertEqual(cmd.get_bytelist(), [0x00, 0x00])

    def test_page_out_of_range(self):
        self.assertRaises(ValueError, Command.create, 'page_sel', -1)
        self.assertRaises(ValueError, Command.create, 'page_sel', 5)

    def test_get_bytelist_page_sel(self):
        cmd = Command.create('page_sel')
        self.assertEqual(cmd.get_bytelist(), [0x10, 0x00])

    def test_get_bytelist_read(self):
        cmd = Command.create('read')
        self.assertEqual(cmd.get_bytelist(), [0x20, 0x00])

    def test_get_bytelist_write(self):
        cmd = Command.create('write')
        self.assertEqual(cmd.get_bytelist(), [0x40, 0x00])

    def test_get_bytelist_quit(self):
        cmd = Command.create('quit')
        self.assertEqual(cmd.get_bytelist(), [0x60, 0x00])

    def test_get_bytelist_reset(self):
        cmd = Command.create('reset')
        self.assertEqual(cmd.get_bytelist(), [0x80, 0x00])

    def test_get_bytelist_row_read(self):
        cmd = Command.create('row_read')
        self.assertEqual(cmd.get_bytelist(), [0xa0, 0x00])

    def test_get_bytelist_convert(self):
        cmd = Command.create('convert')
        self.assertEqual(cmd.get_bytelist(), [0xc0, 0x00])

    def test_get_bytelist_exposure(self):
        cmd = Command.create('exposure')
        self.assertEqual(cmd.get_bytelist(), [0xe0, 0x00])

    def test_string_representation(self):
        command = Command.create('write', 0x05, 0x83)
        str_rep = 'command name: write, address: 0x05, data: 0x83'
        self.assertEqual(str(command), str_rep)

if __name__ == '__main__':
    unittest.main()
