import types
import devices

modbus_class = devices.ModbusDevice

class Devices():
    class Modbus():
        pass

for device_name in dir(devices):
    device = getattr(devices, device_name)
    if isinstance(device, (types.TypeType, types.ClassType)):    
        if issubclass(device, modbus_class) and device.__name__ != 'ModbusDevice':
            print "{} - {}".format(device_name, type(device))
            setattr(Devices.Modbus, device_name, device)

interfaces = devices.interfaces
