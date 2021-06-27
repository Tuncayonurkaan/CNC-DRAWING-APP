# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(800, 600)
        main.setMaximumSize(QSize(800, 600))
        main.setStyleSheet(u"background-color:rgb(232, 232, 232)")
        self.label_image = QLabel(main)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setGeometry(QRect(90, 90, 231, 211))
        self.label_image.setPixmap(QPixmap(u"C:/Users/bentu/OneDrive/Masa\u00fcst\u00fc/photo.png"))
        self.label_image.setScaledContents(True)
        self.label_port = QLabel(main)
        self.label_port.setObjectName(u"label_port")
        self.label_port.setGeometry(QRect(440, 90, 231, 211))
        self.label_port.setPixmap(QPixmap(u"C:/Users/bentu/OneDrive/Masa\u00fcst\u00fc/port-150928_1280.png"))
        self.label_port.setScaledContents(True)
        self.comboBox = QComboBox(main)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(440, 360, 221, 22))
        self.label_serial = QLabel(main)
        self.label_serial.setObjectName(u"label_serial")
        self.label_serial.setGeometry(QRect(430, 310, 251, 16))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setBold(True)
        font.setItalic(True)
        self.label_serial.setFont(font)
        self.label_tau = QLabel(main)
        self.label_tau.setObjectName(u"label_tau")
        self.label_tau.setGeometry(QRect(730, 10, 71, 61))
        self.label_tau.setScaledContents(True)
        self.pushButton_take = QPushButton(main)
        self.pushButton_take.setObjectName(u"pushButton_take")
        self.pushButton_take.setGeometry(QRect(100, 430, 93, 28))
        self.pushButton_take.setFont(font)
        self.pushButton_take.setStyleSheet(u"border: none;")
        self.pushButton_run1 = QPushButton(main)
        self.pushButton_run1.setObjectName(u"pushButton_run1")
        self.pushButton_run1.setGeometry(QRect(240, 430, 121, 28))
        self.pushButton_run1.setFont(font)
        self.pushButton_run1.setStyleSheet(u"border: none;")
        self.pushButton_photo = QPushButton(main)
        self.pushButton_photo.setObjectName(u"pushButton_photo")
        self.pushButton_photo.setGeometry(QRect(80, 350, 121, 71))
        self.pushButton_photo.setFont(font)
        self.pushButton_photo.setStyleSheet(u"border:none")
        self.pushButton_run = QPushButton(main)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(250, 360, 101, 61))
        self.pushButton_run.setFont(font)
        self.pushButton_run.setStyleSheet(u"border-image: url(:/icons/a.png);\n"
"border:none")
        self.imgLabel = QLabel(main)
        self.imgLabel.setObjectName(u"imgLabel")
        self.imgLabel.setGeometry(QRect(20, 90, 371, 341))
        self.imgLabel.setScaledContents(True)
        self.pushButton_Back = QPushButton(main)
        self.pushButton_Back.setObjectName(u"pushButton_Back")
        self.pushButton_Back.setGeometry(QRect(200, 460, 121, 81))
        self.pushButton_Back.setStyleSheet(u"border:none\n"
"")
        self.pushButton_take2 = QPushButton(main)
        self.pushButton_take2.setObjectName(u"pushButton_take2")
        self.pushButton_take2.setGeometry(QRect(440, 450, 121, 81))
        self.pushButton_take2.setStyleSheet(u"border:none")
        self.label = QLabel(main)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 530, 101, 16))
        self.label.setFont(font)
        self.label2 = QLabel(main)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(240, 530, 101, 16))
        self.label2.setFont(font)
        self.imgLabel_2 = QLabel(main)
        self.imgLabel_2.setObjectName(u"imgLabel_2")
        self.imgLabel_2.setGeometry(QRect(410, 90, 371, 341))
        self.imgLabel_2.setScaledContents(True)
        self.label_warning = QLabel(main)
        self.label_warning.setObjectName(u"label_warning")
        self.label_warning.setGeometry(QRect(200, 160, 391, 191))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_warning.setFont(font1)
        self.label_warning.setStyleSheet(u"border: 5px solid black; background: white; color: black;")
        self.label_warning.setTextFormat(Qt.AutoText)
        self.label_warning.setScaledContents(True)
        self.label_warning.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(main)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(300, 290, 191, 23))
        self.progressBar.setStyleSheet(u"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"    \n"
"}")
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)

        self.retranslateUi(main)

        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"main", None))
        self.label_image.setText("")
        self.label_port.setText("")
        self.label_serial.setText(QCoreApplication.translate("main", u"W\u00e4hlen Sie eine serielle Schnittstelle", None))
        self.label_tau.setText("")
        self.pushButton_take.setText(QCoreApplication.translate("main", u"Mach ein Foto", None))
        self.pushButton_run1.setText(QCoreApplication.translate("main", u"Zeichne dieses Bild", None))
        self.pushButton_photo.setText("")
        self.pushButton_run.setText("")
        self.imgLabel.setText("")
        self.pushButton_Back.setText("")
        self.pushButton_take2.setText("")
        self.label.setText(QCoreApplication.translate("main", u"Mach ein Foto", None))
        self.label2.setText(QCoreApplication.translate("main", u"Zur\u00fcck", None))
        self.imgLabel_2.setText("")
        self.label_warning.setText(QCoreApplication.translate("main", u"Ihre Transaktion l\u00e4uft, bitte warten Sie ...", None))
    # retranslateUi

