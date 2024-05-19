from configparser import ConfigParser
import g4f
import json
import time
import os
import random
import pickle
import json
from nltk.corpus import stopwords

stop_words = stopwords.words("english")


# устанавливает язык из файла locale.ini
def set_locale():
    config = ConfigParser()
    config.read("./config/locale.ini", encoding='UTF-8')
    language = config.get("LOCALE", "language")  # устанавливаем локаль
    section = language.upper()
    config.read("./config/{}.ini".format(language), encoding='UTF-8')  # читаем файл строковых данных
    return config, section

config, language = set_locale()

# Возвращает ответ нейросети на заданный вопрос
# request - запрос
# action - что именно нужно сделать с текстом (сократить, ответить, пояснить и тд)
def get_response(request, action = ''):
    # model = "gpt-4"
    # model = "gpt-3.5-turbo"
    # provider = g4f.Provider.FreeChatgpt
    # model = "gpt-3.5-turbo"
    # provider = g4f.Provider.Liaobots

    # model = "airoboros-70b"
    # provider = g4f.Provider.DeepInfra
    model = "gpt-3.5-turbo"
    # provider = g4f.Provider.Ecosia
    provider = g4f.Provider.DuckDuckGo
    # provider = g4f.Provider.Aichatos

    time.sleep(random.randint(1,3))
    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": request + ' ' + action}],
        n=1,
        stream=True,
        provider=provider
    )

    return response

# Возвращает данные из json 
def load_data(file):
    f = open(f'./data/{language.lower()}/{file}.json', encoding='UTF-8')
    data = json.load(f)
    f.close()
    return data

# Возвращает список всех переменных черт
def get_traits_keys():
    return ['gender_age', 'personality', 'body', 'health', 'job', 'hobby', 'phobia', 'inventory', 'additional']

# Возвращает текст конкретной черты
def get_traits_text(trait):
    dct = {}
    for trait_key in get_traits_keys():
        dct.update({trait_key : config.get(language, trait_key)})
    return dct[trait]

# Возвращает слово лет/год/года в зависимости от последней цифры возраста
def get_age_text(age):
    last_number = age % 10
    if age < 20: return config.get(language, "age_number0")
    return {
        0 : config.get(language, "age_number0"),
        1 : config.get(language, "age_number1"),
        2 : config.get(language, "age_number2"),
        3 : config.get(language, "age_number2"),
        4 : config.get(language, "age_number2"),
        5 : config.get(language, "age_number0"),
        6 : config.get(language, "age_number0"),
        7 : config.get(language, "age_number0"),
        8 : config.get(language, "age_number0"),
        9 : config.get(language, "age_number0")
    }[last_number]

# Возвращает название возраста
def get_age_name(age):
    if age < 18: return config.get(language, "teenager")
    elif age < 30: return config.get(language, "young")
    elif age < 60: return  config.get(language, "adult")
    else: return config.get(language, "old")

# Создаёт новый файл с логами
def create_log():
    last_num = get_last_log_num()
    next_num = str(int(last_num)+1)
    next_num = next_num.zfill(4)
    f = open("logs/log"+next_num+".txt", "w", encoding="UTF-8")
    f.close()

# Записывает лог в файл
def write_log(player_name, response):
    last_num = get_last_log_num()
    f = open("logs/log"+last_num+".txt", "a", encoding="UTF-8")
    f.write(player_name+"\n"+response+"\n\n")
    f.close()

# Возвращает номер последнего файла с логами
def get_last_log_num():
    directory = "logs"
    files = os.listdir(directory)
    if len(files) > 0:
        last_num = sorted(files)[-1][3:-4]
    else:
        last_num = -1
    return last_num

# Сериализует историю в файл с сохранением
def save_game(story):
    with open('save.pkl', 'wb') as f:
        pickle.dump(story, f)

# Возвращает сохранение истории из файла с сохранением
def load_game():
    with open("save.pkl", "rb") as f:
        story = pickle.load(f)
    return story
