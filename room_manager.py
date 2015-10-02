from operator import attrgetter

from devices import Devices

import logging


class RoomManager():
    config = {}
    devices = {}
    descriptions = {}

    def __init__(self):
        pass

    def init_devices(self, config):
        self.config = config
        for sensor in self.config['sensors']:
            sensor_name = sensor['name']
            sensor_class = attrgetter(sensor['class'])(Devices)
            args = sensor['args'] if "args" in sensor.keys() else []
            kwargs = sensor['kwargs'] if "kwargs" in sensor.keys() else {}
            sensor_object = sensor_class(*args, **kwargs)
            self.descriptions[sensor_name] = sensor['desc']
            self.devices[sensor_name] = sensor_object
        for actuator in self.config['actuators']:
            actuator_name = actuator['name']
            actuator_class = attrgetter(actuator['class'])(Devices)
            args = actuator['args'] if "args" in actuator.keys() else []
            kwargs = actuator['kwargs'] if "kwargs" in actuator.keys() else {}
            actuator_object = actuator_class(*args, **kwargs)
            self.descriptions[actuator_name] = actuator['desc']
            self.devices[actuator_name] = actuator_object

    def stress_test(self, total_count=0, bad_count=0, error_count={}):
        for device in self.devices.values():
            if device.modbus_id not in error_count.keys():
                error_count[device.modbus_id] = 0
            total_count += 1
            result = device.test()
            if not result[0]:
                bad_count += 1
                error_count[result[1]] += 1
        return total_count, bad_count, error_count

    def api_test_devices(self):
        response = {}
        for device in self.devices.values():
            response[device.name] = device.test()
        return response
            
    def api_stress_test(self, count):
        args = [0L, 0L, {}]
        for iter in range(count):
            args = self.stress_test(*args)
        return args
        
    def get_description(self, device_name):
        return self.descriptions[device_name]
    
    def api_get_device_descriptions(self, *names):
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
