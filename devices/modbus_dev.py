from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import logging
import sys
logging.basicConfig(stream = sys.stdout, level=logging.INFO)

import pdb

client = None

def init_client():
    global client
    if client:
        return
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.1)
    client.connect()

class ModbusDevice():
    comm_retries = 5
    def __init__(self):
        init_client()
        self.client = client

    def test(self):
        response = self.client.read_coils(0, 1, unit=self.modbus_id)
        try:
            response = response.getBit(0)
        except AttributeError:
            response = None
        if response == True or response == False:
            #print "Sensor {} responded".format(self.modbus_id)
            return (True, self.modbus_id)
        else:
            #print "Sensor {} didn't respond".format(self.modbus_id)
            return (False, self.modbus_id)

    def request(self, register):
        counter = 0
        response = None
        while response == None and counter <= self.comm_retries:
            response = self.client.read_holding_registers(register, 1, unit=self.modbus_id)
            if response == None or not hasattr(response, "getRegister"):
                logging.warning("Try {} - didn't get any response from a slave device with ID {}, retrying...".format(counter, self.modbus_id))
                counter += 1
                continue
            response = response.getRegister(0)
            if response == None:
                logging.warning("Try {} - didn't get any response from a slave device with ID {}, retrying...".format(counter, self.modbus_id))
                counter += 1
                continue
        logging.debug("Got the response successfully.")
        return response

    def write(self, register, data):
        return self.client.write_register(register, data, unit=self.modbus_id)


class BinarySensor(ModbusDevice):

    def __init__(self, modbus_id = 1, bits = {1:[0, 1, 2]}):
        ModbusDevice.__init__(self)
        self.modbus_id = modbus_id
        for reg_str in bits.keys(): #Workaround as we need registers to be integers but we get them as strings from JSON
            reg_num = int(reg_str)
            reg_bits = bits[reg_str]
            bits.pop(reg_str) #Removing the key and value
            bits[reg_num] = reg_bits #Restoring the contents
        self.bits = bits
        
    def get_bit_from_value(self, bit_num, value):
        mask = 1 << bit_num
        return mask == mask & value

    def get_all_values(self, bits_dict):
        #Bits are passed as an argument to make this function useful for child classes
        values = []
        for register in sorted(bits_dict.keys()): #In this case it is important to sort keys before they're iterated over because we want them to ne in order
            #Going through every register defined
            register_value = self.request(register)
            for bit_num in bits_dict[register]: 
                #Going through every bit for the given register
                bit_value = self.get_bit_from_value(bit_num, register_value)
                values.append(bit_value)
        return values

    def compare_values(self, *values, **kwargs):
        method_name = kwargs["method_name"] if "method_name" in kwargs.keys() else "all"
        if len(values) != len(actual_values):
            return None #TODO Exception will happen since arrays are compared against each other value by value using indices
        current_values = self.get_all_values(self.bits) 
        try:
            method = eval(method_name) #Allows any(), all() as well as custom functions from child classes. Is vulnerable to attack but is that a valid attack vector?
        except NameError: #Unknown method, what to do? TODO
            return None
        return method([current_value == values[index] for index, current_value in enumerate(current_values)])

    def all_values(self, value=True):
        actual_values = self.get_all_values(self.bits)
        return all([element==value for element in actual_values])

class RegisterSensor(ModbusDevice):

    def __init__(self, modbus_id = 1, registers = [3]):
        ModbusDevice.__init__(self)
        self.modbus_id = modbus_id
        self.registers = registers

    def get_registers_values(self, reg_list):
        #Registers are passed as an argument to make this function useful for child classes
        values = []
        for register in reg_list:
            value = self.request(register)
            values.append(value)
        return values

    def compare_function(self, current_value, expected_value, margin=0):
        if margin == 0:
            return current_value == expected_value
        else:
            return (current_value < expected_value + margin and current_value > expected_value - margin)
        
    def compare_values(self, *values, **kwargs):
        method_name = kwargs["method_name"] if "method_name" in kwargs.keys() else "all"
        margin = kwargs["margin"] if "margin" in kwargs.keys() else 0
        if len(values) != len(self.registers):
            return None #TODO Exception will happen since arrays are compared against each other value by value using indices
        current_values = self.get_registers_values(self.registers)
        try:
            method = eval(method_name) #Allows any(), all() as well as custom functions from child classes.
        except NameError: #Unknown method, what to do? TODO
            raise
        return method([self.compare_function(current_value, values[index], margin) for index, current_value in enumerate(current_values)])
