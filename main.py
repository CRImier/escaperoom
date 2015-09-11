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
from game_manager import GameManager

#A little helper function for all the configs
def read_config(filename):
    f = open(filename, 'r')
    config = json.load(f)
    f.close()
    return config

room_manager = None
step_manager = None
game_manager = None
rpc_api = None
game = None

room_config = {}
scenario = []
rpc_config = {}

def read_configs():
    global room_config, scenario, rpc_config
    room_config = read_config('room_config.json')
    scenario = read_config('scenarios/scenario_small.json')
    rpc_config = read_config('rpc_api.json')

def init_managers():
    global room_manager, step_manager, game_manager, rpc_api, game
    room_manager = RoomManager(room_config)
    room_manager.init_devices()
    step_manager = StepManager(scenario, room_manager)
    rpc_api = RPCApi(rpc_config, step_manager, room_manager)
    game_manager = GameManager()
    game = game_manager.start_game(game_length=60*60)

def init():
    read_configs()
    init_managers()

def test():
    args = (0L, 0L, {})
    try:
        while True:
            args = room_manager.stress_test(*args)
    except KeyboardInterrupt:
        print("Interrupting test - {} failed attempts out of {}".format(args[1], args[0]))
        print(args[2])
        sys.exit(0)

if __name__ == "__main__":
    init()
    test()
    #while game.running:
        #step_manager.stress_test()
        #step_manager.poll()
        #rpc_api.poll()
        #sleep(0.1)
