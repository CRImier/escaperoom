from operator import attrgetter

from devices import Devices

class RoomManager():
    config = {}
    devices = {}
    descriptions = {}

    def __init__(self, config):
        self.config = config

    def init_devices(self):
        for sensor in self.config['sensors']:
            sensor_name = sensor['name']
            sensor_class = attrgetter(sensor['class'])(Devices)
            sensor_object = sensor_class(*sensor['args'], **sensor['kwargs'])
            self.descriptions[sensor_name] = sensor['desc']
            self.devices[sensor_name] = sensor_object

