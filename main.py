import g4f
from player import Player, Players

# Возвращает ответ нейросети на заданный вопрос
# request - запрос
# action - что именно нужно сделать с текстом (сократить, ответить, пояснить и тд)
def get_response(request, action = ''):
    # model = "gpt-4"
    # provider = g4f.Provider.You
    model = "gpt-3.5-turbo"
    provider = g4f.Provider.FreeChatgpt

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

players = Players(5)
for player in players.players:
    for trait in player.known.keys():
        player.known[trait] = True
print(players.get_info())

request = players.players[-1].get_info()
action = 'Расскажи чем этот человек был бы полезен в бункере'
print(''.join([message for message in get_response(request, action)]))
