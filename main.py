from __future__ import print_function
#Imports all the modules

import json

from room import RoomManager
from step_manager import StepManager

room_config = get_json('room_config.json')
scenario = get_json('scenario.json')

room_manager = RoomManager(room_config)
room_manager.init_devices()

step_manager = StepManager(scenario)

step_manager.devices = room_manager.devices

while True:
    step_manager.poll()
