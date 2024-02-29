import random
from modules import *

data = load_data('traits')
male_names = data['male_names']
female_names = data['female_names']

class Player():
    # Инициализация нового персонажа
    def __init__(self):
        self.gender = random.choice(data['genders'])                # пол
        self.age = random.randint(14, 90)                           # возраст
        if self.gender.lower() == "мужчина" or self.gender.lower() == "male":  # имя
            self.name = random.choice(male_names)   
            male_names.remove(self.name)
        else: 
            self.name = random.choice(female_names) 
            female_names.remove(self.name)                                       
        self.personality = random.choice(data['personalities'])     # телосложение  
        self.body = random.choice(data['bodies'])                   # телосложение             
        self.is_healthy = random.choice([True, False])              # здоровый?
        self.disease = random.choice(data['diseases'])              # заболевание
        self.disease_stage = random.choice(data['diseases_stages']) # степень заболевания
        self.job = random.choice(data['jobs'])                      # профессия
        self.job_experience = random.choice(data['experience'])     # опыт работы
        self.hobby = random.choice(data['hobbies'])                 # хобби
        self.hobby_experience = random.choice(data['experience'])   # опыт хобби
        self.phobia = random.choice(data['phobias'])                # фобия
        self.inventory = random.choice(data['inventories'])         # инвентарь
        self.inventory_count = random.randint(1,20)                 # инвентарь кол-во
        self.additional = random.choice(data['additional'])         # доп.информация
        self.active = True      # активный персонаж?
        self.known = {          # известные хар-ки
            'gender_age' : False,
            'personality' : False,
            'body' : False,
            'health' : False,
            'job' : False,
            'hobby' : False,
            'phobia' : False,
            'inventory' : False,
            'additional' : False
        }
        self.explanations = {   # объяснения хар-к
            'gender_age' : '',
            'personality' : '',
            'body' : '',
            'health' : '',
            'job' : '',
            'hobby' : '',
            'phobia' : '',
            'inventory' : '',
            'additional' : ''
        }
        
    # Возвращает информацию об указанной характеристике
    def get_trait_info(self, trait):
        return {
            'gender_age' : self.trait_gender_age,
            'personality' : self.trait_personality,
            'body' : self.trait_body,
            'health' : self.trait_health,
            'job' : self.trait_job,
            'hobby' : self.trait_hobby,
            'phobia' : self.trait_phobia,
            'inventory' : self.trait_inventory,
            'additional' : self.trait_additional
        }[trait]
    
    # Возвращает список характеристик персонажа с его объяснениями характеристики. Можно указать только известные или только неизвестные характеристики.
    def get_traits_info_list(self, only="all"):
        lst_traits = []
        for trait_key in get_traits_keys():
            if (only=="all") or (self.known[trait_key] and only=="known") or (not(self.known[trait_key]) and only=="unknown"):
                lst_traits.append(f'{get_traits_text(trait_key).capitalize()} : {self.get_trait_info(trait_key)}. {self.explanations[trait_key]}')
        return lst_traits
    
    @property
    def trait_name(self):
        return self.name
    @property
    def trait_personality(self):
        return self.personality
    @property
    def trait_gender_age(self):
        return f'{self.gender}, {self.age} {get_age_text(self.age)} ({get_age_name(self.age)})'
    @property
    def trait_body(self):
        return f'{self.body}'
    @property
    def trait_health(self):
        if self.is_healthy:
            return config.get(language, "healthy").capitalize()
        else:
            return f'{self.disease} ({self.disease_stage})'
    @property
    def trait_job(self):
        return f'{self.job} ({self.job_experience})'
    @property
    def trait_hobby(self):
        return f'{self.hobby} ({self.hobby_experience})'
    @property
    def trait_phobia(self):
        return self.phobia
    @property
    def trait_inventory(self):
        return f'{self.inventory}'
    @property
    def trait_additional(self):
        return self.additional

    # Получить краткие сведения о персонаже
    def get_info(self, own=False):
        known_traits = self.get_traits_info_list(only="known")
        unknown_traits = [get_traits_text(trait) for trait in get_traits_keys() if not(self.known[trait])]
        info = ''
        if own:
            info += f'{config.get(language, "info_about_own").capitalize()}\n'
            info += f'{'\n'.join(self.get_traits_info_list())}\n'
        else:
            if len(known_traits) > 0:
                info += f'{config.get(language, "known_info_about").capitalize()} {self.name}\n'
                info += f'{'\n'.join(known_traits)}\n' 
            if len(unknown_traits) > 0:
                info += f'{config.get(language, "unknown_info_about").capitalize()} {self.name}\n'
                info += f'{','.join(unknown_traits)}\n'
        return info
