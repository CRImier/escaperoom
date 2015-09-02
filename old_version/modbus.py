from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200, timeout=0.3)
client.connect()

class Door():
    def __init__(self, id=0x01, coil = 0):
        self.state = False
        self.id = id
        self.coil = coil
        
    def open(self):
        self.set_state(True)
        
    def close(self):
        self.set_state(False)
        
    def set_state(self, state):
        self.state = state
        client.write_coil(self.coil, state, unit=self.id)
        
    def get_state(self):
        return self.state

class LaserAlarm():
    def __init__(self, id=0x02):
        self.id = id
                
    def get_state(self):
        return client.read_discrete_inputs(0, 2, unit=self.id).bits

    def reset_state(self):
        return client.write_coils(0, (False, False), unit=self.id)



#door = Door()
laser = LaserAlarm()
laser.reset_state()

if __name__ == "__main__":
    while True:
        sleep(0.1)
        print laser.get_state()
        sleep(0.1)

