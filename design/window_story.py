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

class StoryWindow(QMainWindow):
    def setupUi(self, mainWindow, story):
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

        self.story = story

        spacing = 100
        spacing_v = 40
        margin_v = 30 
        margin_h = 120 
        stretch_top = 1
        stretch_bottom = 19

        self.layout_v = QVBoxLayout()
        
        self.layout_v.setSpacing(spacing)
        self.layout_v.setContentsMargins(margin_h, margin_v, margin_h, margin_v)


        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        # Бэкграунд
        self.background = QPixmap("./data/images/background.jpg")

        # Заголовок окна
        self.setWindowTitle("BunkerGPT")
        
        # Название катаклизма
        self.lbl_cataclysm = QLabel()
        self.lbl_cataclysm.setText(self.story.story_name)
        self.lbl_cataclysm.setFont(QFont(fontName, 24, weight=QFont.Bold))
        self.lbl_cataclysm.setStyleSheet("color: white") 

        # Описание катаклизма
        self.label_story = Label(self.story.story)

        # Кнопка далее
        self.lbl_next = QLabel()
        self.lbl_next.setText(config.get(language, "next").capitalize())
        self.lbl_next.setFont(QFont(fontName, 24))
        self.lbl_next.setStyleSheet("color: white") 

        # Расположение
        self.layout_v.addWidget(self.lbl_cataclysm)
        self.layout_v.addWidget(self.label_story)
        self.layout_v.addWidget(self.lbl_next, alignment=Qt.AlignRight)
        widget = QWidget()
        widget.setLayout(self.layout_v)
        self.setCentralWidget(widget)
        mainWindow.setCentralWidget(self)
 
    def paintEvent(self,e):
        background = self.background.scaled(self.size())
        p = QPainter(self)
        p.drawPixmap(0,0,background)
        
        