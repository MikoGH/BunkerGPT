import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from modules import *
from design.widget_card import Card
from design.widget_label import Label
from design.widget_chat import Chat


config, language = set_locale()

class MainWindow(QMainWindow):
    def setupUi(self, mainWindow, story):
        # super().__init__()
        mainWindow.setObjectName("MainWindow")
        mainWindow.setWindowModality(QtCore.Qt.NonModal)
        mainWindow.setEnabled(True)
        mainWindow.resize(983, 614)
        mainWindow.setMouseTracking(False)
        mainWindow.setTabletTracking(False)
        mainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        mainWindow.setAcceptDrops(False)
        mainWindow.setAutoFillBackground(False)
        mainWindow.setAnimated(True)
        mainWindow.setDocumentMode(False)
        mainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        mainWindow.setDockNestingEnabled(False)
        mainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        mainWindow.setUnifiedTitleAndToolBarOnMac(False)
        # self.centralwidget = QtWidgets.QWidget(mainWindow)

        self.story = story

        spacing = 100
        spacing_v = 40
        margin_v = 30 
        margin_h = 120 
        stretch_top = 1
        stretch_bottom = 19

        self.layout_h = QHBoxLayout()
        self.layout_v_left = QVBoxLayout()
        self.layout_v_right = QVBoxLayout()
        self.layout_h.addLayout(self.layout_v_left, 2)
        self.layout_h.addLayout(self.layout_v_right, 1)
        
        self.layout_h.setSpacing(spacing)
        self.layout_v_left.setSpacing(spacing_v)
        self.layout_v_right.setSpacing(spacing_v-10)
        self.layout_h.setContentsMargins(margin_h, margin_v, margin_h, margin_v)


        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        # Бэкграунд
        self.background = QPixmap("./data/images/background.jpg")
        
        # Название катаклизма
        self.lbl_cataclysm = QLabel()
        self.lbl_cataclysm.setText(self.story.story_name)
        self.lbl_cataclysm.setFont(QFont(fontName, 24, weight=QFont.Bold))
        self.lbl_cataclysm.setStyleSheet("color: white") 

        # Карточки персонажей
        self.grid_cards = QGridLayout() 
        self.grid_cards.setVerticalSpacing(spacing // 2)
        self.grid_cards.setHorizontalSpacing(spacing)
        self.cards = {}
        for i, player_name in enumerate(self.story.players.keys()):
            self.cards.update({player_name : Card(self.story.players[player_name])})
            self.grid_cards.addWidget(self.cards[player_name], i//3, i%3)

        # Чат
        self.chat = Chat()

        # Расположение
        self.layout_v_left.addWidget(self.lbl_cataclysm, stretch_top, alignment=Qt.AlignCenter)
        self.layout_v_left.addLayout(self.grid_cards, stretch_bottom)
        self.layout_v_right.addWidget(Label(config.get(language, "chat").capitalize()), stretch_top)
        self.layout_v_right.addWidget(self.chat, stretch_bottom)
        widget = QWidget()
        # widget = QWidget(mainWindow)
        widget.setLayout(self.layout_h)
        self.setCentralWidget(widget)
        mainWindow.setCentralWidget(self)
 
    def paintEvent(self,e):
        background = self.background.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0,0,background)
        
        