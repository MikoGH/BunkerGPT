from modules import *


class Text():
    # Инструкция, катаклизм
    def get_static_info(story):
        return f'{config.get(language, "instructions")}\n{config.get(language, "cataclysm").capitalize()}: {story.story_name}.\n{story.story}'
    
    # Информация об игроках (кроме выбранного)
    def get_players_info(story, player_name=''):
        return f'{config.get(language, "applicants").capitalize()}:\n{'\n'.join([player.get_info() for player in story.active_players.values() if player.name != player_name])}'

    # Информация о выбранном персонаже
    def get_person_info(story, player_name):
        return f'{config.get(language, "you_are").capitalize()} {player_name}. {story.players[player_name].get_info(own=True)}'

    # Получить запрос
    def get_request(story, player_name, action, trait=''):
        if action == 'vote':
            return f'{Text.get_static_info(story)}\n{Text.get_players_info(story, player_name)}\n{Text.get_person_info(story, player_name)}\n{config.get(language, "vote")}'
        if action == 'explain trait':
            return f'{Text.get_static_info(story)}\n{trait} - {config.get(language, "explain_trait")} {player_name}'
        if action == 'choose trait':
            return f'{Text.get_static_info(story)}\n{config.get(language, "choose_trait")}\n{'\n'.join(story.players[player_name].get_traits_info_list(only="unknown"))}'
        


