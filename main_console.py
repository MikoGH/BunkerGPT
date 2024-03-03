from modules import *
from player import Player, get_traits_text, get_traits_keys
from story import Story
from texts import Text

config, language = set_locale()


# Выбрать черту для раскрытия
def choose_trait(player_name):
    # выбрать черту
    request = Text.get_request(story, player_name, 'choose trait')
    response = ''.join(get_response(request))
    print(response)

    # проверка, есть ли черта в списке
    trait_chosen = ''
    for trait in get_traits_keys():
        if get_traits_text(trait) in response.lower() or trait in response.lower():
            trait_chosen = trait
            break

    if trait_chosen != '':
        print(story.players[player_name].get_trait_info(trait))
        # объяснить выбранную черту
        request = Text.get_request(story, player_name, 'explain trait', trait=story.players[player_name].get_trait_info(trait))
        response = ''.join(get_response(request))
        print(response)

        # сократить объяснение черты
        response = ''.join(get_response(response, action=config.get(language, "main_info")))
        story.players[player_name].explanations[trait_chosen] = response
        story.players[player_name].known[trait_chosen] = True

    print(*[trait for trait in get_traits_keys() if not(story.players[player_name].known[trait])])


# Голосование за исключение
def choose_player(names=[]):
    # словарь имя : голосов против
    voting = {}

    # из каких имён выбирать
    # при равном голосовании - заново среди тех, за кого больше голосов, иначе среди всех
    if names == []:
        names = story.active_players.keys()
    # голосование только за тех, кто ещё активный
    for name in names:
        voting.update({name : 0})

    # цикл по активным игрокам
    for player_name in story.active_players.keys():
        # голосование игрока против кого-то
        request = Text.get_request(story, player_name, 'vote')
        response = ''.join(get_response(request))
        print(response)

        # поиск имени, против кого проголосовал
        name_chosen = ''
        for word in response.split(): 
            if word in voting.keys():
                name_chosen = word
                break
        if name_chosen != '':
            voting[name_chosen] += 1

    # сколько против кого проголосовали
    for name in voting.keys():
        print(name, ':', voting[name])

    # поиск сколько макс.числа голосов
    max_value = max(voting.values())   
    count = 0
    player_name = ''
    for name in voting.keys():
        if voting[name] == max_value:
            count += 1
            player_name = name

    # если макс.числа голосов несколько, переголосование только среди тех, у кого макс.число голосов. Иначе игрок с макс.числом голосов выбывает
    if count > 1:
        choose_player([name for name in names if voting[name] == max_value])
    else:
        story.players[player_name].active = False



story = Story(n_players=3)

print(story.story_name)
print(story.story)
print(*story.players.keys())

# Круг
for i in range(story.n_players - story.places):
    # # Выбор черты для раскрытия
    for player_name in story.active_players.keys():
        print(story.players[player_name].get_info(own=True))
        for _ in range(3 if i == 0 else 1):
            choose_trait(player_name)
        
    # # Голосование за исключение
    choose_player()

