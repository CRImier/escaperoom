from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep

client = None

def init_client():
    global client
    if client:
        return
    client = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=1)
    client.connect()

class ModbusDevice():
    def __init__(self):
        init_client()
        self.client = client

    def request(self, register):
        return self.client.read_holding_registers(register, 1, unit=self.modbus_id).getRegister(0)

    def write(register, data):
        return self.client.write_register(register, data, unit=self.modbus_id)
