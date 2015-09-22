from time import sleep
import jsonrpclib

import wcs
from ui import Menu, ListView
server = jsonrpclib.Server('http://localhost:8080')

class Game():
    def __init__(self, input, output, server):
        self.input = input
        self.output = output
        self.server = server

    def start(self):
        self.server.start_game()
        self.output.display_data("Game started", "")
        sleep(1)

    def stop(self):
        self.server.stop_game()
        self.output.display_data("Game stopped", "")
        sleep(1)

    def show_time(self):
        time_left = self.server.get_time_left()
        #Displaying something something strftime
        self.output.display_data("Time left", time)
        sleep(1)
        
    
class StepManager():
    
    def __init__(self, input, output, server):
        self.input = input
        self.output = output
        self.server = server
        self.steps_listview = ListView([], input, output)

    def list_steps(self):
        steps_list = self.server.get_steps()
        self.steps_listview.contents = [[step['description'], lambda step=step: self.finish_step(step["name"])] for step in steps_list]
        self.steps_listview.activate()

    def finish_step(self, step_name):
        self.server.finish_step(step_name)
        self.output.display_data("Finished step", step_name)
        sleep(2)


class RoomManager():
    
actions = {
"Start game":server.start_game,
"Stop game":server.stop_game,
"Get active steps":server.get_active_steps,
"Get steps":server.get_steps,
"Finish step":server.finish_step,
"Stress test":server.stress_test,

}


