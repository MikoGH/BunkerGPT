import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from modules import *

config, language = set_locale()


class Label(QWidget):
    def __init__(self, text):
        super().__init__()

        self.layout = QVBoxLayout()
        # self.layout.setGeometry(self.geometry())
        self.layout.setContentsMargins(0, 10, 0, 10)

        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        
        # Текст
        self.lbl = QLabel()
        self.lbl.setText(text)
        self.lbl.setFont(QFont(fontName, 20, weight=QFont.Bold))
        self.layout.addWidget(self.lbl, alignment=Qt.AlignCenter)
        
        self.setLayout(self.layout)
        self.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.begin(self)
        painter.setBrush(QColor.fromRgb(242, 194, 153))
        painter.drawRoundedRect(self.rect(), 20.0, 20.0)
        painter.end()
    