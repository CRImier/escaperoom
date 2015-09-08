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
    def __init__(self):
        init_client()
        self.client = client

    def request(self, register):
        counter = 0
        response = None
        while response == None and counter <= 3:
            response = self.client.read_holding_registers(register, 1, unit=self.modbus_id)
            if response == None:
                logging.warning("Try {} - didn't get any response from a slave device, retrying...".format(counter))
                counter += 1
                continue
            print response
            response = response.getRegister(0)
            if response == None:
                logging.warning("Try {} - didn't get any response from a slave device, retrying...".format(counter))
                counter += 1
            print response
        logging.info("Got the response successfully.")
        return response

    def write(self, register, data):
        return self.client.write_register(register, data, unit=self.modbus_id)
