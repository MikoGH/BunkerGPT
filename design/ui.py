from design.window_main import MainWindow
from design.window_story import StoryWindow
from PyQt5.QtCore import Qt, QRunnable, pyqtSlot, QThreadPool, QThread
from PyQt5.QtGui import QPixmap,QPicture,QMouseEvent
from PyQt5.QtWidgets import QApplication
from PIL.ImageQt import ImageQt
from story import Story
from actions import choose_player, choose_trait


from design.widget_message import Message

class Worker(QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def run(self):
        for player_name in self.ui.story.active_players.keys():
            print(player_name)
            # widget_message = Message(None, "szxdcfvghjbkn")
            widget_message = Message(self.ui.story.players[player_name], "szxdcfvghjbkn")
            self.ui.ui.chat.scrollLayout.addWidget(widget_message)
            # widget_message.show()
        # Круг
        # for i in range(self.ui.story.n_players - self.ui.story.places):
        #     # Выбор черты для раскрытия
        #     for player_name in self.ui.story.active_players.keys():
        #         print(player_name)
        #         for _ in range(3 if i == 0 else 1):
        #             choose_trait(self.ui.ui, self.ui.story, player_name)
        #             print('chosen')
        #         self.ui.update()
        #         self.mainWindow.show()
                
        #     # Голосование за исключение
        #     choose_player(self.ui.ui, self.ui.story)
        

''' Класс обработчик событий '''
class Ui_MainWindowActions(MainWindow):
    def __init__(self, mainWindow):
        
        self.story = Story(n_players=6) 

        self.mainWindow = mainWindow
        self.ui = StoryWindow()
        self.ui.setupUi(self.mainWindow, self.story)

        # self.ui = MainWindow()
        # self.ui.setupUi(self.mainWindow, self.story)

        # self.keyPressed.connect(self.go)
        self.ui.lbl_next.mousePressEvent = self.to_main_window

        
    def to_main_window(self, event):
        self.ui = MainWindow()
        self.ui.setupUi(self.mainWindow, self.story)
        self.ui.update()

        # self.threadpool = QThreadPool()
        self.worker = Worker(self)
        # self.threadpool.start(worker)
        # self.worker.start()
