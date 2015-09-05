from modbus_dev import ModbusDevice

import pdb

class KnobPanel(ModbusDevice):

    def __init__(self, modbus_id = 1, knob_count = 1, knob_registers = [3]):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.knob_count = knob_count
        self.knob_registers = knob_registers

    def get_knob_value(self, knob_register):
        raw_data = self.request(knob_register)

    def get_knob_values(self):
        values = []
        for knob_index in range(self.knob_count):
            values.append(self.get_knob_values(self.knob_registers[knob_index]))
        return values

    def compare_knobs(self, *args, **kwargs):
        margin = kwargs['margin']
        truth_table = []
        knob_values = self.get_knob_values()
        for index, value in enumerate(args):
            truth_table.append(value < knob_values[index] + margin and value > knob_values[index] - margin)
        return all(truth_table)


class TemperatureSensor(ModbusDevice):

    def __init__(self, modbus_id=1, temperature_register=3, coefficient=1):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.temperature_register = temperature_register
        self.coefficient = coefficient

    def get_raw_data(self):
        raw_data = self.request(self.temperature_register)
        return raw_data
        
    def get_temperature(self):
        raw_data = self.get_raw_data()
        #pdb.set_trace()
        temperature = raw_data*self.coefficient
        return temperature

    def compare_temperature(self, temperature=0, margin=5):
        current_temperature = self.get_temperature()
        return (current_temperature < temperature + margin and current_temperature > temperature - margin)


class PressureSensor(ModbusDevice):

    def __init__(self, modbus_id=1, pressure_register=3, coefficient=1):
        ModbusDevice.__init__(self) 
        self.modbus_id = modbus_id
        self.pressure_register = pressure_register
        self.coefficient = coefficient

    def get_raw_data(self):
        raw_data = self.request(self.pressure_register)
        return raw_data
        
    def get_pressure(self):
        raw_data = self.get_raw_data()
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

    def get_door_register(self):
        raw_data = self.request(self.door_register)
        return raw_data

    def door_opened(self):
        door_data = self.get_door_register()
        mask = 1 << self.bit
        return mask == mask & door_data
        

class DoorRelay(ModbusDevice):

    def __init__(self, modbus_id=1, register=0, bit=0):
        ModbusDevice.__init__(self) 
        self.modbus_id=modbus_id
        self.register = register
        self.bit = bit

    def open(self):
        data = self.request(self.register)
        data = data | (1 << self.bit) 
        self.write(self.register, data)

    def close(self):
        data = self.request(self.register)
        data = data & ~(1 << self.bit) 
        self.write(self.register, data)
