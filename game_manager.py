from __future__ import division
import logging
from subprocess import check_output
from datetime import datetime

class Game():
    running = False
    participant_count = 1
    start_time = 0
    game_length = 0

    def __init__(self):
        pass

    def start(self, p_count=1, game_length=60*60):
        self.participant_count = p_count
        self.set_start_time(datetime.now())
        self.set_game_length(game_length)
        self.running = True

    def stop(self):
        self.running = False

    def update_displayed_time(self):
        pass #Need external trigger support, linking the game manager with devices available

    def print_time_left(self):
        print("Time left - {}:{}".format(*self.get_time_left()))

    def get_time_left(self):
        if not self.running:
            return (0, 0)
        difference = datetime.now() - self.start_time
        seconds_from_start = difference.total_seconds()
        seconds_left = self.game_length - seconds_from_start
        return (int(seconds_left/60), int(seconds_left%60)) #Minutes and seconds till the game ends

    def decrease_time_left(self, amount):
        self.game_length -= amount
        self.update_displayed_time()

    def increase_time_left(self, amount):
        self.game_length += amount
        self.update_displayed_time()

    def set_game_length(self, amount):
        self.game_length = amount
        if self.running:
            self.update_displayed_time()

    def get_game_length(self):
        return self.game_length

    def set_start_time(self, time):
        self.start_time = time

    def get_start_time(self):
        return self.start_time


class GameManager():
    game = None

    def __init__(self):
        pass

    def init_game(self, config):
        self.config = config
        self.game = Game()

    def api_start_game(self, *args, **kwargs):
        self.start_game(*args, **kwargs)

    def api_stop_game(self):
        self.stop_game()

    def api_get_time_left(self):
        if not self.game:
            return (0, 0) #Look, an owl!
        return self.game.get_time_left()

    def api_get_game_state(self):
        return self.game.running

    def start_game(self, *args, **kwargs):
        self.game.start(*args, **kwargs)
       
    def stop_game(self):
        self.game.stop()

    def make_sound(self, sound_filename):
        pass

    def execute_env_trigger(self, trigger):
        action = trigger["action"]
        method = trigger["method"]
        if action == "game":
            if method == "end":
                self.stop_game() 
            elif method == "decrease_time":
                amount = trigger["amount"]
                self.game.decrease_time_left(amount) 
