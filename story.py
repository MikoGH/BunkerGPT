import random
from player import Player
from modules import *


config, language = set_locale()

data = load_data('stories')

class Story():
    def __init__(self, n_players):
        self.n_players = n_players
        self.places = (self.n_players+1) // 2
        self.players = {}
        for i in range(n_players):
            new_player = Player()
            self.players.update({new_player.name : new_player})
        # создать лог
        create_log()
        self.story_name = random.choice(list(data.keys()))
        self.story = data[self.story_name]

    @property
    def active_players(self):
        act_players = {}
        for player in self.players.values():
            if player.active:
                act_players.update({player.name : player})
        return act_players
