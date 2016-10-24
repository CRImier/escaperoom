from operator import attrgetter

from devices import Devices, interfaces

import logging


class RoomManager():
    
    config = {}
    interface_storage = {}
    devices = {}
    descriptions = {}

    def __init__(self):
        pass

    def init_devices(self, config):
        self.config = config
        self.default_interface = config['default_interface']
        for entry in config['interfaces']:
            interface = {}
            interface_name = entry['name']
            interface_class_name = entry['class']
            interface_class = interfaces[interface_class_name]
            args = entry['args'] if 'args' in entry.keys() else []
            kwargs = entry['kwargs'] if 'kwargs' in entry.keys() else {}
            interface_object = interface_class(*args, **kwargs)
            interface_object.interface_name = interface_name
            self.interface_storage[interface_name] = interface_object
        for sensor in self.config['sensors']:
            sensor_name = sensor['name']
            sensor_class = attrgetter(sensor['class'])(Devices)
            args = sensor['args'] if "args" in sensor.keys() else []
            kwargs = sensor['kwargs'] if "kwargs" in sensor.keys() else {}
            if "interfaces" in kwargs: 
                sensor_interfaces = [self.interface_storage[name] for name in kwargs["interfaces"]]
                kwargs['interfaces'] = sensor_interfaces
            else:
                interface_name = kwargs['interface'] if 'interface' in kwargs else self.default_interface
                sensor_interface = self.interface_storage[interface_name]
                kwargs['interface'] = sensor_interface
            sensor_object = sensor_class(*args, **kwargs)
            self.descriptions[sensor_name] = sensor['desc']
            self.devices[sensor_name] = sensor_object
        for actuator in self.config['actuators']:
            actuator_name = actuator['name']
            actuator_class = attrgetter(actuator['class'])(Devices)
            args = actuator['args'] if "args" in actuator.keys() else []
            kwargs = actuator['kwargs'] if "kwargs" in actuator.keys() else {}
            interface_name = kwargs['interface'] if 'interface' in kwargs else self.default_interface
            sensor_interface = self.interface_storage[interface_name]
            kwargs['interface'] = sensor_interface
            actuator_object = actuator_class(*args, **kwargs)
            self.descriptions[actuator_name] = actuator['desc']
            self.devices[actuator_name] = actuator_object

    def stress_test(self, total_count=0, bad_count=0, error_count={}):
        used_ids = []
        for device in self.devices.values():
            identifier = device.get_identifier()
            if identifier not in used_ids:
                if device.modbus_id not in error_count.keys():
                    error_count[device.modbus_id] = 0
                total_count += 1
                result = device.test()
                if not result[0]:
                    bad_count += 1
                    error_count[result[1]] += 1
                used_ids.append(identifier)
        return total_count, bad_count, error_count

    def get_identifiers(self):
        identifiers = {}
        for device_name, device in self.devices.iteritems():
            identifiers[device_name] = device.get_identifier()
        return identifiers

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
    
    def api_get_device_descriptions(self):
        descriptions = []
        for name in self.devices.keys():
            dev_desc = {'name':name, 'description':'', 'id':''}
            dev_desc['description'] = self.get_description(name)
            dev_desc['id'] = self.devices[name].modbus_id #TODO: modify when other types of devices get incorporated
            descriptions.append(dev_desc)
        return descriptions

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

    def reset_device_for_trigger(self, trigger):
        actuator_name = trigger["actuator"]
        actuator = self.devices[actuator_name]
        try:
            actuator.reset()
        except AttributeError:
            logging.warning("Tried to reset device {} with no reset method available".format(actuator_name))
