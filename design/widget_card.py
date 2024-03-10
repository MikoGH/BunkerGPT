import sys
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from player import Player
from modules import *


class Card(QWidget):
    def __init__(self, player : Player):
        super().__init__()

        margin_h_text = 10
        margin_v_text = 5

        # Размер 
        self.setMaximumSize(400,600)
        self.wordWrap = True;

        # Контейнеры
        # self.container = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout_name = QHBoxLayout()
        self.layout_traits = QVBoxLayout()
        self.layout_traits.setContentsMargins(margin_h_text, margin_v_text, margin_h_text, margin_v_text)
        self.layout.addLayout(self.layout_name, 1)
        self.layout.addLayout(self.layout_traits, 19)
        

        # Шрифты
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Bold.ttf")
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        fontId = QFontDatabase.addApplicationFont("./data/fonts/Finlandica-Regular.ttf")
        fontName_regular = QFontDatabase.applicationFontFamilies(fontId)[0]
        
        # Аватар
        imgpath = f"./data/avatars/{player.avatar}"
        if not(os.path.exists(imgpath)):
            imgpath = f"./data/avatars/None.jpg"
        imgdata = open(imgpath, 'rb').read() 
        pixmap = Card.mask_image(imgdata) 
        self.lbl_image = QLabel(self) 
        self.lbl_image.setPixmap(pixmap) 
        # self.lbl_image.move(500, 180)

        # Имя
        self.lbl_name = QLabel()
        self.lbl_name.setText(player.name)
        self.lbl_name.setFont(QFont(fontName, 16, weight=QFont.Bold))
        
        # Характеристики
        self.dct_lbl_traits = {}
        for trait in get_traits_keys():
            layout_trait = QHBoxLayout()
            lbl_trait = QLabel()
            if trait == 'phobia':
                text = player.get_trait_info(trait).split('—')[0]
            else:
                text = player.get_trait_info(trait)
            lbl_trait.setText(f"<b>{get_traits_text(trait).capitalize()}:</b> {text}")
            lbl_trait.setFont(QFont(fontName_regular, 9))
            lbl_trait.setMaximumWidth(self.width())
            lbl_trait.setWordWrap(True)
            layout_trait.addWidget(lbl_trait)  ##
            self.dct_lbl_traits.update({trait : layout_trait})

        # Расположение
        self.layout_name.addWidget(self.lbl_image, 1)
        self.layout_name.addWidget(self.lbl_name, 2)
        self.layout_traits.setSpacing(2)
        for trait in get_traits_keys():
            self.layout_traits.addLayout(self.dct_lbl_traits[trait])
        #     if trait == 'hobby':
        #         print('hobby')
        #         self.layout_traits.addLayout(self.dct_lbl_traits[trait], 2)
        #     else:
        #         self.layout_traits.addLayout(self.dct_lbl_traits[trait], 1)

        self.setLayout(self.layout)
        self.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.begin(self)
        painter.setBrush(QColor.fromRgb(242, 213, 187))
        painter.drawRoundedRect(self.rect(), 20.0, 20.0)
        painter.end()

    def mask_image(imgdata, imgtype = 'jpg', size = 64): 
        image = QImage.fromData(imgdata, imgtype) 
        image.convertToFormat(QImage.Format.Format_ARGB32) 
        # to square
        imgsize = min(image.width(), image.height()) 
        rect = QRect( 
            (image.width() - imgsize) // 2, 
            (image.height() - imgsize) // 2, 
            imgsize, 
            imgsize, 
        ) 
        image = image.copy(rect) 
        out_img = QImage(imgsize, imgsize, QImage.Format.Format_ARGB32) 
        out_img.fill(QColorConstants.Transparent) 

        brush = QBrush(image) 

        painter = QPainter(out_img) 
        painter.setBrush(brush) 
        painter.setPen(QPen())
        painter.drawEllipse(0, 0, imgsize, imgsize) 
        painter.end() 

        pr = QWindow().devicePixelRatio() 
        pm = QPixmap.fromImage(out_img) 
        pm.setDevicePixelRatio(pr) 
        size *= pr 
        size = int(size)
        pm = pm.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) 
        
        return pm 