import sys
import requests

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QMessageBox, QLabel, QLineEdit
from PyQt5.QtGui import QCursor
from loginWindow import LoginWindow
from utils import customStyle

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Register"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.URL = "http://localhost:8000/register"
        self.username = None
        self.password = None
        self.confirm_password = None
        self.setStyleSheet(customStyle())

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.display_register_title()
        self.get_username()
        self.get_password()
        self.get_confirm_password()

        btn_register = QPushButton("Register", self)
        btn_register.move(410, 600)
        btn_register.resize(292, 50)
        btn_register.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_register.clicked.connect(self.register)

        login_text = QLabel(self)
        login_text.setText("Already have an account?")
        login_text.move(-20, 670)
        login_text.setStyleSheet("font-size: 16px; color: #fff; font-weight: bold;")
        login_text.resize(self.width, 50)
        login_text.setAlignment(QtCore.Qt.AlignCenter)

        btn_login = QPushButton("Login", self)
        btn_login.move(642, 677)
        btn_login.resize(50, 30)
        btn_login.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_login.setStyleSheet("background-color: transparent; color: #ab85ff; font-size: 16px; font-weight: bold; border: none;")
        btn_login.clicked.connect(self.login)
        

        self.show()

    def login(self):
        self.login_window = LoginWindow()
        self.close()

    def display_register_title(self):
        title = QLabel(self)
        title.setText("Register")
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

    def get_confirm_password(self):
        self.confirm_password = QLineEdit(self)
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.move(410, 490)
        self.confirm_password.resize(292, 50)
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.returnPressed.connect(self.register)

    def register(self):
        username = self.username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if username == "" or password == "" or confirm_password == "":
            QMessageBox.about(self, "Error", "Please fill all the fields")
            return

        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password):
            QMessageBox.about(self, "Error", "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number")
            return

        if password != confirm_password:
            QMessageBox.about(self, "Error", "Passwords do not match")
            return

        try:
            response = requests.post(self.URL, json={"username": username, "password": password})
            resp_message = response.json()["message"]
            if response.json()["status"] == "error":
                QMessageBox.about(self, "Error", resp_message)
            else:
                QMessageBox.about(self, "Success", resp_message)
                self.login_window = LoginWindow()
                self.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", "Connection with database failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    sys.exit(app.exec_())