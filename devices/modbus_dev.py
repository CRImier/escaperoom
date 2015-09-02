from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#from settings import settings

class ModbusDevice():
    def __init__(self):
        self.client = client

    def request(self, register):
        return self.client.read_holding_register(register, unit=self.modbus_id)

    def write(register, data):
        return self.client.write_register(register, data, unit=self.modbus_id)
