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
        self.places = n_players // 2

    def get_static_info(self, player_name=''):
        return f'{instructions}\nКатаклизм: {self.story_name}.\n{self.story}\nЖелающие попасть в бункер:\n{self.players.get_info(player_name=player_name)}'
    
    def get_person_info(self, player_name):
        return f'Ты отыгрываешь персонажа по имени {player_name}. {self.players.players[player_name].get_info_own()}'
    
    def get_action(self, player, action):
        if action == 'short':
            return 'Выдели основную информацию из текста выше'
        # if action == 'explain trait':
        #     return 'Объясни, почему эта черта может быть полезна в бункере'
        if action == 'vote':
            return 'Напиши имя игрока, которого ты считаешь наименее полезным для бункера'
        if action == 'choose trait':
            return f'Выбери одну черту из списка ниже, которую считаешь наиболее полезной для бункера. Напиши её точно так же, как она написана в списке. Затем поясни, почему эта черта полезна для бункера. \n{'\n'.join([trait for trait in player.known.keys() if not(player.known[trait])])}'

    def get_request(self, player, action):
        return self.get_static_info(player.name) + '\n' + self.get_person_info(player.name) + '\n' + self.get_action(player, action)


