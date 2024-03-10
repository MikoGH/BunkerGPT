import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from design.ui import Ui_MainWindowActions

# story = Story(n_players=6)
# window = MainWindow(story)
# window.showFullScreen()

app = QApplication(sys.argv)

mainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindowActions(mainWindow, app)
mainWindow.show()

sys.exit(app.exec_())

# # Круг
# for i in range(story.n_players - story.places):
#     # Выбор черты для раскрытия
#     for player_name in story.active_players.keys():
#         # print(player_name)
#         # print(story.players[player_name].get_info(own=True))
#         for _ in range(3 if i == 0 else 1):
#             choose_trait(player_name)
#     window.update()
        
#     # Голосование за исключение
#     choose_player()
