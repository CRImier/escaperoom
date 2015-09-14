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
