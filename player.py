import random
import json

traits_russian = {
            'gender_age' : 'пол и возраст',
            'name' : 'имя',
            'body' : 'телосложение',
            'health' : 'здоровье',
            'job' : 'профессия',
            'hobby' : 'хобби',
            'inventory' : 'инвентарь',
            'additional' : 'доп.информация'
        }

age_russian = {
    0 : 'лет',
    1 : 'год',
    2 : 'года',
    3 : 'года',
    4 : 'года',
    5 : 'лет',
    6 : 'лет',
    7 : 'лет',
    8 : 'лет',
    9 : 'лет'
}

def get_age_name(age, gender):
    if age < 30: age_names = ['молодой', 'молодая']
    elif age < 60: age_names = ['взрослый', 'взрослая']
    else: age_names = ['пожилой', 'пожилая']
    if gender == "Мужчина":
        return age_names[0]
    else:
        return age_names[1]

def load_data():
    f = open('traits_russian.json', encoding='UTF-8')
    data = json.load(f)
    male_names = data['male_names']
    female_names = data['female_names']
    f.close()
    return data, male_names, female_names

data, male_names, female_names = load_data()

class Player():
    # Инициализация нового персонажа
    def __init__(self):
        self.gender = random.choice(data['genders'])                # пол
        self.age = random.randint(14, 90)                           # возраст
        if self.gender == "Мужчина":                                # имя
            self.name = random.choice(male_names)   
            male_names.remove(self.name)
        else: 
            self.name = random.choice(female_names) 
            female_names.remove(self.name)                                       
        self.body = random.choice(data['bodies'])                   # телосложение             
        self.is_healthy = random.choice([True, False])              # здоровый?
        self.disease = random.choice(data['diseases'])              # заболевание
        self.disease_stage = random.choice(data['diseases_stages']) # степень заболевания
        self.job = random.choice(data['jobs'])                      # профессия
        self.job_experience = random.choice(data['experience'])     # опыт работы
        self.hobby = random.choice(data['hobbies'])                 # хобби
        self.hobby_experience = random.choice(data['experience'])   # опыт хобби
        self.inventory = random.choice(data['inventories'])         # инвентарь
        self.inventory_count = random.randint(1,20)                 # инвентарь кол-во
        self.additional = random.choice(data['additional'])         # доп.информация
        self.known = {
            'gender_age' : False,
            'name' : True,
            'body' : False,
            'health' : False,
            'job' : False,
            'hobby' : False,
            'inventory' : False,
            'additional' : False
        }
        self.explanations = {
            'gender_age' : '',
            'name' : '',
            'body' : '',
            'health' : '',
            'job' : '',
            'hobby' : '',
            'inventory' : '',
            'additional' : ''
        }

    @property
    def trait_name(self):
        if not(self.known['name']): return 'Неизвестно'
        return self.name
    @property
    def trait_gender_age(self):
        if not(self.known['gender_age']): return 'Неизвестно'
        return f'{self.gender}, {self.age} {age_russian[self.age % 10]} ({get_age_name(self.age, self.gender)})'
    @property
    def trait_body(self):
        if not(self.known['body']): return 'Неизвестно'
        return f'{self.body}'
    @property
    def trait_health(self):
        if not(self.known['health']): return 'Неизвестно'
        if self.is_healthy:
            return 'Полностью здоров'
        else:
            return f'{self.disease} ({self.disease_stage} степень)'
    @property
    def trait_job(self):
        if not(self.known['job']): return 'Неизвестно'
        return f'{self.job} ({self.job_experience})'
    @property
    def trait_hobby(self):
        if not(self.known['hobby']): return 'Неизвестно'
        return f'{self.hobby} ({self.hobby_experience})'
    @property
    def trait_inventory(self):
        if not(self.known['inventory']): return 'Неизвестно'
        return f'{self.inventory}'
    @property
    def trait_additional(self):
        if not(self.known['additional']): return 'Неизвестно'
        return self.additional

    # Получить краткие сведения о персонаже
    def get_info(self):
        known_traits = [
            f'{f'Пол и возраст: {self.trait_gender_age}. {self.explanations['gender_age']}' if self.known['gender_age'] else ''}',
            f'{f'Телосложение: {self.trait_body}. {self.explanations['body']}' if self.known['body'] else ''}',
            f'{f'Здоровье: {self.trait_health}. {self.explanations['health']}' if self.known['health'] else ''}',
            f'{f'Профессия: {self.trait_job}. {self.explanations['job']}' if self.known['job'] else ''}',
            f'{f'Хобби: {self.trait_hobby}. {self.explanations['hobby']}' if self.known['hobby'] else ''}',
            f'{f'Инвентарь: {self.trait_inventory}. {self.explanations['inventory']}' if self.known['inventory'] else ''}',
            f'{f'Доп.информация: {self.trait_additional}. {self.explanations['additional']}' if self.known['additional'] else ''}'
        ]
        known_traits = [trait for trait in known_traits if trait != '']
        unknown_traits = [traits_russian[trait] for trait in self.known.keys() if not(self.known[trait])]
        return f'{f'Известные сведения о {self.name}:\n{'\n'.join(known_traits)}' if len(known_traits) > 0 else ''}\n{f'Неизвестные сведения о {self.name}:\n{','.join(unknown_traits)}' if len(unknown_traits) > 0 else ''}'
    

class Players():
    def __init__(self, n):
        self.players = []
        for i in range(n):
            new_player = Player()
            self.players.append(new_player)

    def get_info(self):
        return '\n\n'.join([player.get_info() for player in self.players])