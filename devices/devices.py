from modbus_dev import ModbusDevice, AnalogSensor, DigitalSensor

import logging

import pdb

class KnobPanel(AnalogSensor):

    def __init__(self, modbus_id = 1, knob_count = 1, knob_registers = [3]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.knob_count = knob_count
        self.knob_registers = knob_registers
        self.test()

    def get_knob_values(self):
        values = []
        for knob_index in range(self.knob_count):
            values.append(self.get_register(self.knob_registers[knob_index]))
        return values

    def compare_knobs(self, *args, **kwargs):
        margin = kwargs['margin']
        truth_table = []
        knob_values = self.get_knob_values()
        print("{} - {}".format(str(knob_values), str(args)))
        for index, value in enumerate(args):
            truth_table.append(value < (knob_values[index] + margin) and value > (knob_values[index] - margin))
        return all(truth_table)


class TemperatureSensor(AnalogSensor):

    def __init__(self, modbus_id=1, temperature_register=3, coefficient=1):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.temperature_register = temperature_register
        self.coefficient = coefficient
        self.test()

    def get_temperature(self):
        raw_data = self.get_register(self.temperature_register)
        temperature = raw_data*self.coefficient
        return temperature

    def compare_temperature(self, temperature=0, margin=5):
        current_temperature = self.get_temperature()
        return (current_temperature < (temperature + margin) and current_temperature > (temperature - margin))


class PressureSensor(AnalogSensor):

    def __init__(self, modbus_id=1, pressure_register=3, coefficient=1):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.pressure_register = pressure_register
        self.coefficient = coefficient
        self.test()

    def get_pressure(self):
        raw_data = self.get_register(self.pressure_register)
        temperature = raw_data*self.coefficient
        return temperature

    def compare_pressure(self, pressure=0, margin=5):
        current_pressure = self.get_pressure()
        return (current_pressure < pressure + margin and current_pressure > pressure - margin)


class RFIDSensor(ModbusDevice):

    def __init__(self, modbus_id=1, reader_count=1, presence_register=3, reader_registers=[4, 5, 6]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.reader_count = reader_count
        self.presence_register = presence_register
        self.reader_registers = reader_registers
        self.test()
        #Insert check for len(reader_registers) = reader_count
        
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


class DoorSensor(ModbusDevice):

    def __init__(self, modbus_id=1, door_register=3, bit=0):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.door_register = door_register
        self.bit = bit
        self.test()

    def get_door_register(self):
        raw_data = self.request(self.door_register)
        return raw_data

    def door_opened(self):
        door_data = self.get_door_register()
        mask = 1 << self.bit
        return mask == mask & door_data

        
class FloorSensor(ModbusDevice):

    def __init__(self, modbus_id=1, button_register=3, bit=0):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.button_register = button_register
        self.bit = bit
        self.test()

    def get_button_register(self):
        raw_data = self.request(self.button_register)
        return raw_data

    def was_pressed(self):
        door_data = self.get_door_register()
        mask = 1 << self.bit
        return mask == mask & door_data

        
class ButtonPanel(ModbusDevice):

    def __init__(self, modbus_id=1, button_register=3, bits=[0, 1, 2]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.button_register = button_register
        self.bits = bits
        self.test()

    def get_button_states(self):
        states = []
        register = self.request(self.button_register)
        for button_bit in self.bits:
            states.append(mask == (1<<button_bit) & button_register)
        return states
        
    def compare_state(self, *args):
        return self.get_button_states == args


class ShotSensor(ModbusDevice):

    def __init__(self, modbus_id=1, sensor_register=3, bits=[0, 1, 2]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.sensor_register = sensor_register
        self.bits = bits
        self.test()

    def get_sensor_states(self):
        states = []
        register = self.request(self.sensor_register)
        for button_bit in self.bits:
            states.append(mask == (1<<button_bit) & button_register)
        return states
        
    def compare_state(self, *args):
        return self.get_sensor_states == args


class DoorRelay(ModbusDevice):

    lock = lambda: None
    unlock = lambda: None

    def __init__(self, modbus_id=1, init_locked=True, lock_invert=False, register=0, bit=0):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.register = register
        self.bit = bit
        self.test()
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
