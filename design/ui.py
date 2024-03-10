from design.window_main import MainWindow
from design.window_story import StoryWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap,QPicture,QMouseEvent
from PyQt5.QtWidgets import QApplication
from PIL.ImageQt import ImageQt
from story import Story
from actions import choose_player, choose_trait
from design.widget_message import Message


class Worker(QObject):
    signal_trait = pyqtSignal(str, str)  # player_name, trait
    signal_trait_explanation = pyqtSignal(str, str)  # player_name, trait explanation
    signal_vote = pyqtSignal(str, str)  # player_name, player chosen
    signal_vote_explanation = pyqtSignal(str, str)  # player_name, player chosen
    signal_vote_results = pyqtSignal(str)  # vote results
    
    def __init__(self, story):
        super().__init__()
        self.story = story

    @pyqtSlot()
    def run(self):
        # Круг
        for i in range(self.story.n_players - self.story.places):
            # Выбор черты для раскрытия
            for player_name in self.story.active_players.keys():
                for _ in range(3 if i == 0 else 1):
                    trait, message = choose_trait(self.story, player_name)
                    if trait != '':
                        self.signal_trait.emit(player_name, trait)
                        self.signal_trait_explanation.emit(player_name, message)
            # Голосование за исключение
            while True:
                # словарь имя : голосов против
                voting = {}
                # из каких имён выбирать
                # при равном голосовании - заново среди тех, за кого больше голосов, иначе среди всех
                if names == []:
                    names = self.story.active_players.keys()
                # голосование только за тех, кто ещё активный
                for name in names:
                    voting.update({name : 0})
                    # цикл по активным игрокам
                    for player_name in self.story.active_players.keys():
                        vote, message, voting = choose_player(self.story, player_name)
                        if vote != '':
                            self.signal_vote.emit(player_name, vote)
                            self.signal_vote_explanation.emit(player_name, message)
                        
                # сколько против кого проголосовали
                text_results = ''
                for name in voting.keys():
                    text_results += f'{name} : {voting[name]}'
                    self.signal_vote_results.emit(text_results)

                # поиск сколько макс.числа голосов
                max_value = max(voting.values())   
                count = 0
                player_name = ''
                for name in voting.keys():
                    if voting[name] == max_value:
                        count += 1
                        player_name = name
                # если макс.числа голосов несколько, переголосование только среди тех, у кого макс.число голосов. Иначе игрок с макс.числом голосов выбывает
                if count == 1:
                    break

            self.story.players[player_name].active = False
        

''' Класс обработчик событий '''
class Ui_MainWindowActions(MainWindow, QObject):
    def __init__(self, mainWindow, app):  
        super().__init__()
        self.app = app      
        self.story = Story(n_players=6) 

        self.mainWindow = mainWindow
        self.ui = StoryWindow()
        self.ui.setupUi(self.mainWindow, self.story)
        self.ui.lbl_next.mousePressEvent = self.to_main_window

        # self.ui = MainWindow()
        # self.ui.setupUi(self.mainWindow, self.story)

        # self.to_main_window()


        
    def to_main_window(self, event):
        self.ui = MainWindow()
        self.ui.setupUi(self.mainWindow, self.story)
        self.ui.update()
        
        # thread
        self.thread = QThread()
        self.worker = Worker(self.story)
        # signals
        self.worker.signal_trait.connect(self.signal_trait)
        self.worker.signal_trait_explanation.connect(self.signal_trait_explanation)
        # start
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

        # self.do()
 
    def signal_trait(self, player_name, trait):
        # print(self.story.players[player_name].known)
        pass

    def signal_trait_explanation(self, player_name, message):
        widget_message = Message(self.story.players[player_name], message)
        self.ui.chat.scrollLayout.addWidget(widget_message, alignment=Qt.AlignTop)
        
    def signal_vote(self, player_name, vote):
        pass
        
    def signal_vote_explanation(self, player_name, message):
        widget_message = Message(self.story.players[player_name], message)
        self.ui.chat.scrollLayout.addWidget(widget_message, alignment=Qt.AlignTop)
        
    def signal_vote_results(self, message):
        widget_message = Message(None, message)
        self.ui.chat.scrollLayout.addWidget(widget_message, alignment=Qt.AlignTop)
