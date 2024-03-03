import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Chat(QWidget):
    def __init__(self):
        super().__init__()

        # Размер 
        # self.setMaximumSize(600,200)

        self.container = QWidget(self)
        self.layout = QVBoxLayout(self.container)
        self.layout.setGeometry(self.geometry())

        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName_bold = QFontDatabase.applicationFontFamilies(fontId)[0]
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Regular.ttf")
        fontName_regular = QFontDatabase.applicationFontFamilies(fontId)[0]
        
        # Текст
        self.scrollArea = QScrollArea()
        self.layout.addWidget(self.scrollArea, alignment=Qt.AlignCenter)
        
        self.setLayout(self.layout)
        self.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.begin(self)
        painter.setBrush(QColor.fromRgb(242, 213, 187))
        painter.drawRoundedRect(self.rect(), 20.0, 20.0)
        painter.end()
    