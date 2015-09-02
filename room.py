from operator import attrgetter

object_storage = [] #TODO

class RoomManager():
    config = {}
    devices = {}
    descriptions = {}

    def __init__(self, config):
        self.config = config

    def init_devices(self):
        for sensor in config['sensors']
            sensor_name = sensor['name']
            sensor_class = attgetter(sensor['class'])(objects) #TODO
            sensor_object = sensor_class(*sensor['args'], **sensor['kwargs'])
            self.descriptions[sensor_name] = sensor['desc']
            self.devices[sensor_name] = sensor_object

