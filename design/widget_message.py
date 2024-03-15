import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from modules import *
from design.widget_card import Card
import re


class Message(QWidget):
    def __init__(self, player, message, template=''):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout_name = QHBoxLayout()
        self.layout.setContentsMargins(0, 10, 0, 10)

        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]

        # Аватар
        if player != None:
            imgpath = f"./data/avatars/{player.avatar}"
        else:
            imgpath = f"./data/avatars/None.jpg"
        if not(os.path.exists(imgpath)):
            imgpath = f"./data/avatars/None.jpg"
        imgdata = open(imgpath, 'rb').read() 
        pixmap = Card.mask_image(imgdata) 
        self.lbl_image = QLabel(self) 
        self.lbl_image.setPixmap(pixmap) 
        
        # Имя
        self.lbl_name = QLabel()
        if player != None:
            self.lbl_name.setText(player.name)
        else:
            self.lbl_name.setText('#')
        self.lbl_name.setFont(QFont(fontName, 16, weight=QFont.Bold))
        
        # Текст
        template_words = [word.lower() for word in template.split()]
        message_words = list(message.split())
        for i, word in enumerate(message_words):
            if word.replace(r'\W', '').lower() in template_words:
                message_words[i] = word.replace(word.replace(r'\W', ''), f'<b>{word.replace(r'\W', '')}</b>')
                print(message_words[i])


        self.lbl = QLabel()
        self.lbl.setText(' '.join(message_words))
        self.lbl.setFont(QFont(fontName, 12))
        self.lbl.setMaximumWidth(self.width())
        self.lbl.setWordWrap(True)

        # Расположение
        self.layout_name.addWidget(self.lbl_image, 1)
        self.layout_name.addWidget(self.lbl_name, 9)
        self.layout_name.setSpacing(20)
        self.layout.addLayout(self.layout_name)
        self.layout.addWidget(self.lbl)
        
        self.setLayout(self.layout)
        # self.show()
        
    