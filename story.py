import json
import random
from player import Player, Players


def load_data():
    f = open('stories_russian.json', encoding='UTF-8')
    data = json.load(f)
    f.close()
    return data

data = load_data()
instructions = '''Ты играешь в игру "Бункер". Правила игры:
В мире произошёл катаклизм. В бункере ограничено количество мест. Игрокам предстоит выбрать, кого оставить в бункере.
Каждый игрок один раз за раунд раскрывает одну свою черту, которую считает наиболее полезной для бункера, и объясняет, почему она полезна.
Твоя задача - убедить остальных, что ты полезен для выживания в бункере.
'''  # Инструкция к игре


class Story():
    def __init__(self, n_players):
        self.n_players = n_players
        self.players = Players(n_players)
        self.story_name = random.choice(list(data.keys()))
        self.story = data[self.story_name]
        self.places = (n_players+1) // 2

    def get_static_info(self):
        return f'{instructions}\nКатаклизм: {self.story_name}.\n{self.story}'
    
    def get_players_info(self, player_name=''):
        return f'Желающие попасть в бункер:\n{self.players.get_info(player_name=player_name, active=True)}'

    def get_person_info(self, player_name):
        return f'Ты отыгрываешь персонажа по имени {player_name}. {self.players.players[player_name].get_info_own()}'
    
    def get_action(self, player, action, trait=''):
        if action == 'vote':
            return 'Напиши имя игрока без склонений по падежам, которого ты считаешь наименее полезным для бункера. Затем объясни свой выбор.'
        if action == 'explain trait':
            return f'Как {trait} может быть полезно при жизни в бункере? Пиши от лица {player.name}.'
        if action == 'choose trait':
            return f'Выбери одну черту из списка ниже, которую считаешь наиболее полезной для бункера. Напиши её точно так же, как она написана в списке. Только выбери, ничего не объясняй. \n{'\n'.join([trait for trait in player.known.keys() if not(player.known[trait])])}'

    def get_request(self, player, action, trait=''):
        if action == 'choose trait' or action == 'explain trait':
            return self.get_static_info() + '\n' + self.get_action(player, action, trait)
        return self.get_static_info() + '\n' + self.get_players_info(player.name) + '\n' + self.get_person_info(player.name) + '\n' + self.get_action(player, action)
    


