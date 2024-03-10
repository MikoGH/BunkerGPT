import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from design.widget_message import Message


class Chat(QWidget):
    def __init__(self):
        super().__init__()

        # Размер 
        self.layout = QVBoxLayout()
        self.layout.setGeometry(self.geometry())

        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        
        # Текст
        self.scrollArea = QScrollArea(self)
        self.layout.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        scrollContent = QWidget(self.scrollArea)

        self.scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(self.scrollLayout)
        #
        self.scrollArea.setStyleSheet('background : #F2D5BB')
        self.scrollArea.setWidget(scrollContent)

        self.layout.addWidget(self.scrollArea, alignment=Qt.AlignCenter)
        
        self.setLayout(self.layout)
        self.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.begin(self)
        painter.setBrush(QColor.fromRgb(242, 213, 187))
        painter.drawRoundedRect(self.rect(), 20.0, 20.0)
        painter.end()
        margin = 10
        self.scrollArea.setGeometry(self.rect().left()+margin, self.rect().top()+margin, self.rect().width()-margin*2, self.rect().height()-margin*2)
    