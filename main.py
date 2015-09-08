from __future__ import print_function
import json
from time import sleep

import pdb
import sys
import logging
sys.excepthook = lambda *args: pdb.pm()
logging.basicConfig(stream = sys.stdout, level=logging.INFO)

logging.info("Importing modules")

from step_manager import StepManager
from room_manager import RoomManager
from rpc_api import RPCApi

#A little helper function for all the configs
def read_config(filename):
    f = open(filename, 'r')
    config = json.load(f)
    f.close()
    return config

room_config = read_config('room_config.json')
scenario = read_config('scenarios/scenario_small.json')
rpc_config = read_config('rpc_api.json')

room_manager = RoomManager(room_config)
room_manager.init_devices()

step_manager = StepManager(scenario, room_manager)

rpc_api = RPCApi(rpc_config, step_manager, room_manager)

while True:
    step_manager.poll()
    rpc_api.poll()
    sleep(0.1)
