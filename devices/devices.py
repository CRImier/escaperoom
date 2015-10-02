from modbus_dev import ModbusDevice, BinarySensor, RegisterSensor
#Incidentally, BinarySensor and RegisterSensor seem to cover most of the sensors that are typically used

import logging
import pdb

class RFIDSensor(ModbusDevice):

    def __init__(self, modbus_id=1, presence_register=3, reader_registers=[4, 5, 6]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.presence_register = presence_register
        self.reader_registers = reader_registers
        
    def get_presence_bits(self):
        presence_data = self.request(presence_register)
        presence_bit_list = [] #:TODO
        #Return a list of booleans with len = reader_count
        raise NotImplementedError
        return presence_bit_list

    def read_id_from_reader(self, number):
        id = self.request(self.reader_registers[number])
        return id

    def compare_ids(self, *ids):
        id_matches = []
        for index, id in enumerate(ids):
            id_matches.append(id == read_id_from_reader(index))
        return all(id_matches)


class DoorRelay(ModbusDevice):

    lock = lambda: None
    unlock = lambda: None

    def __init__(self, modbus_id=1, init_locked=True, lock_invert=False, register=0, bit=0):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.register = register
        self.bit = bit
        if lock_invert:
            self.lock, self.unlock = self.set_false, self.set_true
        else:
            self.lock, self.unlock = self.set_true, self.set_false
        if init_locked:
            self.lock()

    def set_true(self):
        data = self.request(self.register)
        data = data | (1 << self.bit) 
        self.write(self.register, data)
        
    def set_false(self):
        data = self.request(self.register)
        data = data & ~(1 << self.bit) 
        self.write(self.register, data)


