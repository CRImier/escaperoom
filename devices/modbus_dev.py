from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import logging
import sys
logging.basicConfig(stream = sys.stdout, level=logging.INFO)

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
            print "Sensor {} responded".format(self.modbus_id)
            return (True, self.modbus_id)
        else:
            print "Sensor {} didn't respond".format(self.modbus_id)
            return (False, self.modbus_id)

    def request(self, register):
        counter = 0
        response = None
        while response == None and counter <= self.comm_retries:
            response = self.client.read_holding_registers(register, 1, unit=self.modbus_id)
            if response == None:
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
