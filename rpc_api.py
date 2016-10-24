from SocketServer import ThreadingMixIn
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import logging

import threading

class SimpleThreadedJSONRPCServer(ThreadingMixIn, SimpleJSONRPCServer):
    pass

class RPCApi():
    server = None

    def __init__(self):
        pass

    def init_api(self, config, **kwargs):
        self.config = config
        self.objects = kwargs #We pass object_name:object pairs with all the objects whose functions have to be registered.
        if not self.server:
            self.server = SimpleThreadedJSONRPCServer((self.config['host'], self.config['port']))
        #Doesn't support changing server's host/port on the fly, but can be easily added if needed
        self.server.timeout = self.config['timeout']
        #TODO: unregister all the functions maybe? Is there even such an action? Would it be necessary?
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
        logging.debug("RPC API: polling...")
        self.server.handle_request() #TODO: remake so that it fullfills all the requests available?

    def run(self):
        while not self.stop_thread:
            self.server.serve_forever()

    def start_thread(self):
        logging.debug("RPC API: running...")
        self.stop_thread = False
        self.thread = threading.Thread(target = self.run, args = ())
        self.thread.daemon = True
        self.thread.start()

    def stop_thread(self):
        self.stop_thread = True
