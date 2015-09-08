from operator import attrgetter

from devices import Devices

import logging


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
        for actuator in self.config['actuators']:
            actuator_name = actuator['name']
            actuator_class = attrgetter(actuator['class'])(Devices)
            actuator_object = actuator_class(*actuator['args'], **actuator['kwargs'])
            self.descriptions[actuator_name] = actuator['desc']
            self.devices[actuator_name] = actuator_object

    def get_description(self, device_name):
        return self.descriptions[device_name]
    
    def get_descriptions(self, *names):
        return [self.get_description(name) for name in names]

    def execute_hw_trigger(self, trigger):
        actuator_name = trigger["actuator"]
        try:
            actuator = self.devices[actuator_name]
        except:
            logging.warning("Device {} not found in available device list".format(actuator_name))
            return False
        method_name = trigger["method"]
        method = getattr(actuator, method_name)
        args = trigger["args"] if 'args' in trigger.keys() else []
        kwargs = trigger["kwargs"] if 'kwargs' in trigger.keys() else {}
        return method(*args, **kwargs) #I honestly don't know if I need a return statement.

    def execute_env_trigger(self, trigger):
        pass
