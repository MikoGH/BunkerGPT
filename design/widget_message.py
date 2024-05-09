import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from modules import *
from design.widget_card import Card
import re


class Message(QWidget):
    def __init__(self, player, message, action=None, template=''):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout_name = QHBoxLayout()
        self.layout_name_text = QVBoxLayout()
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout_name_text.setSpacing(5)

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
            self.lbl_name.setText(config.get(language, "system").capitalize())
        self.lbl_name.setFont(QFont(fontName, 16, weight=QFont.Bold))

        # Действие
        self.lbl_action = QLabel()
        if action != None:
            self.lbl_action.setText(action)
        else:
            self.lbl_action.setText("")
        self.lbl_action.setFont(QFont(fontName, 12))
        
        # Текст
        template_words = [re.sub(r'\W', '', word).lower() for word in template.split()]
        message_words = list(message.split())
        for i, word in enumerate(message_words):
            sub_word = re.sub(r'\W', '', word)
            if sub_word.lower() in template_words and not(sub_word.lower() in stop_words):
                message_words[i] = word.replace(sub_word, f'<b>{sub_word}</b>')


        self.lbl = QLabel()
        self.lbl.setText(' '.join(message_words))
        self.lbl.setFont(QFont(fontName, 12))
        self.lbl.setMaximumWidth(self.width())
        self.lbl.setWordWrap(True)

        # Расположение
        self.layout_name_text.addWidget(self.lbl_name, 2)
        self.layout_name_text.addWidget(self.lbl_action, 1)
        self.layout_name.addWidget(self.lbl_image, 1)
        self.layout_name.addLayout(self.layout_name_text, 9)
        self.layout_name.setSpacing(20)
        self.layout.addLayout(self.layout_name)
        self.layout.addWidget(self.lbl)
        
        self.setLayout(self.layout)
        # self.show()
        
    