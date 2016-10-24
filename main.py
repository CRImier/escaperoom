from __future__ import print_function
import json
from time import sleep

import threading

import signal
import pdb
import os
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

room_manager = RoomManager()
game_manager = GameManager()
step_manager = StepManager()
rpc_api = RPCApi()

room_config = None
game_config = None
scenario = None
rpc_config = None

def read_configs():
    global room_config, scenario, rpc_config, game_config
    scenario = read_config('museum_scenario.json')
    room_config = read_config('museum_config.json')
    rpc_config = read_config('rpc_api.json')
    game_config = read_config('game_config.json')

def prepare_for_game():
    room_manager.init_devices(room_config)
    game_manager.init_game(game_config)
    step_manager.init_steps(scenario, room_manager, game_manager)
    rpc_api.init_api(rpc_config, step_manager=step_manager, room_manager=room_manager, game_manager=game_manager)

def exit(*args):
    #Used for signal handling. As for now, just exits.
    sys.exit(0)

for exit_signal in [signal.SIGTERM]:
    signal.signal(exit_signal, exit)

if __name__ == "__main__":
    logging.info("PID is {}".format(os.getpid()))
    while True: #Endless loop for the script. Guess you could even call it a state machine ;-)
        #TODO: add persistence between script crashes
        read_configs()
        prepare_for_game() #Before every game starts, we need to initialise objects
        game = game_manager.game
        print(room_manager.get_identifiers())
        if not game.running: #At the start, the game usually is not running (might be changed when persistence functions get added). 
            logging.info("Game not running yet")
        rpc_api.start_thread()
        """        for device in room_manager.devices.values():
            #pdb.set_trace()
            if 'reset' in dir(device):
                try:
                    device.reset()
                except Exception as e:
                    logging.warning("Exception while resetting device: {}".format(e))"""
        while not game.running: #Until it is, we just poll the API to receive the game start signal
            print(room_manager.api_stress_test(1))
            #rpc_api.poll()
            logging.debug("Game not running yet")
        logging.info("Game started.")
        step_manager.game_started()
        while game.running: #Now the game is started and we also need to poll steps
            #rpc_api.poll()
            step_manager.poll()
            game.print_time_left()
            sleep(0.1)
