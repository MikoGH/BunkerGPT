import g4f
from player import Player, Players, traits_russian
from story import Story

# Возвращает ответ нейросети на заданный вопрос
# request - запрос
# action - что именно нужно сделать с текстом (сократить, ответить, пояснить и тд)
def get_response(request, action = ''):
    model = "gpt-4"
    provider = g4f.Provider.You
    # model = "gpt-3.5-turbo"
    # provider = g4f.Provider.FreeChatgpt

    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": request + ' ' + action}],
        n=1,
        stream=True,
        provider=provider
    )
    return response

# request = 'Сгенерируй какой-нибудь текст на 200 слов'
# print(''.join([message for message in get_response(request)]))


# players = Players(6)
# for player in players.players:
#     for trait in player.known.keys():
#         player.known[trait] = True
# print(players.get_info())

# request = players.players[-1].get_info()
# action = 'Расскажи чем этот человек был бы полезен в бункере'
# print(''.join([message for message in get_response(request, action)]))

story = Story(n_players=6)

# Выбрать черту для раскрытия
def choose_trait(player_name):
    request = story.get_request(story.players.players[player_name], 'choose trait')
    response = ''.join(get_response(request))
    print(response)
    trait_chosen = ''
    for trait in traits_russian.keys():
        if traits_russian[trait] in response.lower():
            trait_chosen = trait
            break

    response = ''.join(get_response(request, action='Выдели основную информацию из текста выше.'))
    if trait_chosen != '':
        story.players.players[player_name].explanations[trait_chosen] = response
        story.players.players[player_name].known[trait_chosen] = True


# Голосование за исключение
def choose_player(names=[]):
    voting = {}
    if names == []:
        names = story.players.players.keys()

    for name in names:
        if story.players.players[name].active:
            voting.update({name : 0})

    for player_name in story.players.keys():
        request = story.get_request(story.players.players[player_name], 'vote')
        response = ''.join(get_response(request))
        print(response)

        name_chosen = ''
        for word in response.lower().split(): 
            if word in voting.keys():
                name_chosen = word
                break

        if name_chosen != '':
            voting[name_chosen] += 1

            
    for name in voting.keys():
        print(name, ':', voting[name])

    max_value = 0
    for name in voting.keys():
        if voting[name] > max_value:
            max_value = voting[name]

    count = 0
    for name in voting.keys():
        if voting[name] == max_value:
            count += 1

    if count > 1:
        return choose_player([name for name in names if voting[name] == max_value])



# Круг
for i in range(story.n_players - story.places):
    # Выбрать черту для раскрытия
    for player_name in story.players.players.keys():
        print(story.players.players[player_name].get_info_own())
        for _ in range(3 if i == 0 else 1):
            choose_trait(player_name)
        
    # Голосование за исключение
    choose_player()

