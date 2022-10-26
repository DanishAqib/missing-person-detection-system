from email import message
import sys
import requests

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QMessageBox, QLabel, QLineEdit
from appWindow import AppWindow
from PyQt5.QtGui import QCursor
from utils import customStyle

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Login"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.URL = "http://localhost:8000/login"
        self.username = None
        self.password = None
        self.setStyleSheet(customStyle())

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.display_login_title()
        self.get_username()
        self.get_password()

        btn_login = QPushButton("Login", self)
        btn_login.move(410, 550)
        btn_login.resize(292, 50)
        btn_login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_login.clicked.connect(self.login)

        self.show()

    def display_login_title(self):
        title = QLabel(self)
        title.setText("Login")
        title.move(0, 220)
        title.setStyleSheet("text-transform: uppercase; font-size: 60px;")
        title.resize(self.width, 70)
        title.setAlignment(QtCore.Qt.AlignCenter)

    def get_username(self):
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter Username")
        self.username.move(410, 350)
        self.username.resize(292, 50)

    def get_password(self):
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter Password")
        self.password.move(410, 420)
        self.password.resize(292, 50)
        self.password.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        if username == "" or password == "":
            QMessageBox.warning(self, "Error", "Please fill all entries")
            return
        try:
            response = requests.post(self.URL, json={"username": username, "password": password})
            resp_status = response.json()["status"]
            resp_message = response.json()["message"]
            if resp_status == "success":
                self.appWindow = AppWindow(user=self.username.text())
                self.close()
            elif resp_status == "pass_error":
                QMessageBox.about(self, "Error", resp_message)
            else:
                QMessageBox.about(self, "Error", resp_message)

        except Exception as e:
                QMessageBox.warning(self, "Error", "Connection with database failed")
                
app = QApplication(sys.argv)

if __name__ == "__main__":
    window = LoginWindow()
    sys.exit(app.exec_())
