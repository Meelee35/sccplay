# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(327, 243)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pathEdit = QLineEdit(self.centralwidget)
        self.pathEdit.setObjectName(u"pathEdit")
        self.pathEdit.setGeometry(QRect(10, 30, 221, 35))
        self.browseBtn = QPushButton(self.centralwidget)
        self.browseBtn.setObjectName(u"browseBtn")
        self.browseBtn.setGeometry(QRect(240, 28, 71, 38))
        self.loop = QCheckBox(self.centralwidget)
        self.loop.setObjectName(u"loop")
        self.loop.setGeometry(QRect(20, 80, 91, 23))
        self.shuffle = QCheckBox(self.centralwidget)
        self.shuffle.setObjectName(u"shuffle")
        self.shuffle.setGeometry(QRect(20, 110, 91, 23))
        self.play = QPushButton(self.centralwidget)
        self.play.setObjectName(u"play")
        self.play.setGeometry(QRect(110, 170, 41, 38))
        font = QFont()
        font.setPointSize(14)
        self.play.setFont(font)
        self.pause = QPushButton(self.centralwidget)
        self.pause.setObjectName(u"pause")
        self.pause.setGeometry(QRect(170, 170, 41, 38))
        font1 = QFont()
        font1.setPointSize(15)
        self.pause.setFont(font1)
        self.output = QLineEdit(self.centralwidget)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(-10, 210, 341, 35))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.browseBtn.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.loop.setText(QCoreApplication.translate("MainWindow", u"Loop", None))
        self.shuffle.setText(QCoreApplication.translate("MainWindow", u"Shuffle", None))
        self.play.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
        self.pause.setText(QCoreApplication.translate("MainWindow", u"\u23f9", None))
    # retranslateUi

