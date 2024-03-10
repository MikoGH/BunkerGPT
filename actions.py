from modules import *
from player import Player, get_traits_text, get_traits_keys
from story import Story
from texts import Text
from design.widget_message import Message

config, language = set_locale()

# Выбрать черту для раскрытия
def choose_trait(story, player_name):
    trait_chosen = ''
    while trait_chosen == '':
        # выбрать черту
        request = Text.get_request(story, player_name, 'choose trait')
        response = ''.join(get_response(request))

        # проверка, есть ли черта в списке
        for trait in get_traits_keys():
            if get_traits_text(trait) in response.lower() or trait in response.lower():
                trait_chosen = trait
                break

    # объяснить выбранную черту
    request = Text.get_request(story, player_name, 'explain trait', trait=story.players[player_name].get_trait_info(trait))
    response = ''.join(get_response(request))
    message = response

    # сократить объяснение черты
    response = ''.join(get_response(response, action=config.get(language, "main_info")))
    story.players[player_name].explanations[trait_chosen] = response
    story.players[player_name].known[trait_chosen] = True
    return trait_chosen, message


# Голосование за исключение
def choose_player(story, player_name, voting):
    # голосование игрока против кого-то
    request = Text.get_request(story, player_name, 'vote')
    response = ''.join(get_response(request))

    # поиск имени, против кого проголосовал
    name_chosen = ''
    for word in response.split(): 
        if word in voting.keys():
            name_chosen = word
            break
    if name_chosen != '':
        voting[name_chosen] += 1
    return name_chosen, response, voting
