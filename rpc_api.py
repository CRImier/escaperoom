from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import logging

class RPCApi():
    def __init__(self, config, **kwargs):
        self.config = config
        self.objects = kwargs #We pass object_name:object pairs with all the objects whose functions have to be registered.
        self.server = SimpleJSONRPCServer((self.config['host'], self.config['port']))
        self.server.timeout = self.config['timeout']
        self.register_functions()
        
    def register_functions(self):
        for object_name in self.objects.keys():
            object = self.objects[object_name]
            for f_description in self.config[object_name]:
                function_name = f_description["name"]
                function_alias = f_description["alias"] if "alias" in f_description.keys() else function_name
                function = getattr(object, function_name)
                self.server.register_function(function, function_alias)

    def poll(self):
        self.server.handle_request()
