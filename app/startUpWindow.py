import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QCursor
from registerWindow import RegisterWindow
from loginWindow import LoginWindow
from utils import customStyle

class StartUpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Welcome"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png" 
        self.app_logo = "../resources/app-logo.png"
        self.setStyleSheet(customStyle())

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.display_app_logo()

        btn_login = QPushButton("Login", self)
        btn_login.move(410, 550)
        btn_login.resize(292, 50)
        btn_login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_login.clicked.connect(self.login)

        btn_register = QPushButton("Register", self)
        btn_register.move(410, 620)
        btn_register.resize(292, 50)
        btn_register.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_register.clicked.connect(self.register)
        self.show()

    def display_app_logo(self):
        app_logo = QLabel(self)
        app_logo.setPixmap(QtGui.QPixmap(self.app_logo))
        app_logo.move(260, 10)
        app_logo.resize(588, 588)
        app_logo.setScaledContents(True)

    def login(self):
        self.login_window = LoginWindow()
        self.close()

    def register(self):
        self.register_window = RegisterWindow()
        self.close()

app = QApplication(sys.argv)
window = StartUpWindow()
sys.exit(app.exec_())