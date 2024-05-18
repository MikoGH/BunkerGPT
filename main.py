import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from design.ui import Ui_MainWindowActions
import nltk

# !!! download
# nltk.download('stopwords')

continue_game = False

app = QApplication(sys.argv)
mainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindowActions(mainWindow, app, continue_game)
mainWindow.show()

sys.exit(app.exec_())
