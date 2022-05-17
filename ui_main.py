# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainaiOaCp.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(990, 832)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 10, 991, 771))
        self.mainLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.videoLayout = QHBoxLayout()
        self.videoLayout.setObjectName(u"videoLayout")
        self.videoText = QLabel(self.verticalLayoutWidget)
        self.videoText.setObjectName(u"videoText")

        self.videoLayout.addWidget(self.videoText)

        self.videoSource = QLineEdit(self.verticalLayoutWidget)
        self.videoSource.setObjectName(u"videoSource")
        self.videoSource.setClearButtonEnabled(True)

        self.videoLayout.addWidget(self.videoSource)

        self.chooseText = QLabel(self.verticalLayoutWidget)
        self.chooseText.setObjectName(u"chooseText")

        self.videoLayout.addWidget(self.chooseText)

        self.algorithmList = QComboBox(self.verticalLayoutWidget)
        self.algorithmList.addItem("")
        self.algorithmList.setObjectName(u"algorithmList")

        self.videoLayout.addWidget(self.algorithmList)


        self.mainLayout.addLayout(self.videoLayout)

        self.serviceLayout = QHBoxLayout()
        self.serviceLayout.setObjectName(u"serviceLayout")
        self.serviceUrlText = QLabel(self.verticalLayoutWidget)
        self.serviceUrlText.setObjectName(u"serviceUrlText")

        self.serviceLayout.addWidget(self.serviceUrlText)

        self.serviceUrl = QLineEdit(self.verticalLayoutWidget)
        self.serviceUrl.setObjectName(u"serviceUrl")
        self.serviceUrl.setClearButtonEnabled(True)

        self.serviceLayout.addWidget(self.serviceUrl)

        self.accountLayout = QHBoxLayout()
        self.accountLayout.setObjectName(u"accountLayout")
        self.username = QLineEdit(self.verticalLayoutWidget)
        self.username.setObjectName(u"username")
        self.username.setClearButtonEnabled(True)

        self.accountLayout.addWidget(self.username)

        self.password = QLineEdit(self.verticalLayoutWidget)
        self.password.setObjectName(u"password")
        self.password.setClearButtonEnabled(True)

        self.accountLayout.addWidget(self.password)


        self.serviceLayout.addLayout(self.accountLayout)


        self.mainLayout.addLayout(self.serviceLayout)

        self.video = QLabel(self.verticalLayoutWidget)
        self.video.setObjectName(u"video")
        self.video.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.video)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.openVideo = QPushButton(self.verticalLayoutWidget)
        self.openVideo.setObjectName(u"openVideo")

        self.buttonsLayout.addWidget(self.openVideo)

        self.closeVideo = QPushButton(self.verticalLayoutWidget)
        self.closeVideo.setObjectName(u"closeVideo")

        self.buttonsLayout.addWidget(self.closeVideo)

        self.startAnalyze = QPushButton(self.verticalLayoutWidget)
        self.startAnalyze.setObjectName(u"startAnalyze")

        self.buttonsLayout.addWidget(self.startAnalyze)

        self.stopAnalyze = QPushButton(self.verticalLayoutWidget)
        self.stopAnalyze.setObjectName(u"stopAnalyze")

        self.buttonsLayout.addWidget(self.stopAnalyze)


        self.mainLayout.addLayout(self.buttonsLayout)

        self.description = QLabel(self.verticalLayoutWidget)
        self.description.setObjectName(u"description")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.description)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 990, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.videoText.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u6e90", None))
        self.videoSource.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u89c6\u9891\u5730\u5740", None))
        self.chooseText.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u7b97\u6cd5", None))
        self.algorithmList.setItemText(0, QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u7b97\u6cd5", None))

        self.serviceUrlText.setText(QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5\u670d\u52a1\u5730\u5740", None))
        self.serviceUrl.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165\u7b97\u6cd5\u670d\u52a1\u5668\u5730\u5740", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"\u8d26\u53f7", None))
        self.password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.video.setText(QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u9884\u89c8\u533a", None))
        self.openVideo.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u89c6\u9891\u6d41", None))
        self.closeVideo.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u89c6\u9891\u6d41", None))
        self.startAnalyze.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u7b97\u6cd5\u5206\u6790", None))
        self.stopAnalyze.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u7b97\u6cd5\u5206\u6790", None))
        self.description.setText(QCoreApplication.translate("MainWindow", u"\u7b97\u6cd5\u6d4b\u8bd5v0.1 \u7248\u6743@\u65b0\u822a\u7269\u8054\u7f51 2022 by QILIN", None))
    # retranslateUi

