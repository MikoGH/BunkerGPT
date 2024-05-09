from modules import *
from player import Player, get_traits_text, get_traits_keys
from story import Story
from texts import Text
from design.widget_message import Message
import re

config, language = set_locale()

# Выбрать черту для раскрытия
def choose_trait(story, player_name):
    trait_chosen = ''
    if not(story.players[player_name].known['job']): trait_chosen = 'job'
    while trait_chosen == '':
        # выбрать черту
        request = Text.get_request(story, player_name, 'choose trait')
        response = ''.join(get_response(request))
        print(response)

        # проверка, есть ли черта в списке
        for trait in get_traits_keys():
            for word in response.lower().split():
                if word.replace(r'\W', '') in get_traits_text(trait).lower() or get_traits_text(trait).lower() in response.lower() or word.replace(r'\W', '') in story.players[player_name].get_trait_info(trait).lower():
                    trait_chosen = trait
                    break

    # объяснить выбранную черту
    request = Text.get_request(story, player_name, 'explain trait', trait=story.players[player_name].get_trait_info(trait_chosen))
    response = ''.join(get_response(request))
    message = response

    # сократить объяснение черты
    response = ''.join(get_response(response, action=config.get(language, "main_info")))
    story.players[player_name].explanations[trait_chosen] = response
    story.players[player_name].known[trait_chosen] = True

    # записать лог
    write_log(player_name, message)
    return trait_chosen, message


# Голосование за исключение
def choose_player(story, player_name, voting):
    name_chosen = ''
    while name_chosen == '':
        # голосование игрока против кого-то
        request = Text.get_request(story, player_name, 'vote')
        response = ''.join(get_response(request))
        print(response)

        # поиск имени, против кого проголосовал
        for word in response.split(): 
            sub_word = re.sub(r'\W', '', word)
            if sub_word in voting.keys():
                name_chosen = sub_word
                break
    voting[name_chosen] += 1
    
    # записать лог
    write_log(player_name, response)
    return name_chosen, response, voting
