from configparser import ConfigParser
import g4f
import json


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

