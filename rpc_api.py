from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import logging

class RPCApi():
    def __init__(self, config, step_manager, room_manager):
        self.config = config
        self.step_manager = step_manager
        self.room_manager = room_manager
        self.server = SimpleJSONRPCServer((self.config['host'], self.config['port']))
        self.server.timeout = self.config['timeout']
        self.register_functions()
        
    def register_functions(self):
        for function_name in self.config['step_manager_functions']:
            function = getattr(self.step_manager, function_name)
            self.server.register_function(function)
        for function_name in self.config['room_manager_functions']:
            function = getattr(self.room_manager, function_name)
            self.server.register_function(function)

    def poll(self):
        self.server.handle_request
