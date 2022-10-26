import sys
import requests
import json
import base64
import io

import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QBoxLayout
from newCaseWindow import NewCaseWindow
from detectionWindow import DetectionWindow
from PyQt5.QtWidgets import QListWidget, QLabel, QLineEdit
from utils import customStyle

class AppWindow(QMainWindow):
    def __init__(self, user=""):
        super().__init__()
        self.title = "Application"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.user = user
        self.setStyleSheet(customStyle())

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.display_title()

        btn_new_case = QPushButton("Submit A New Case", self)
        btn_new_case.move(410, 250)
        btn_new_case.resize(292, 70)
        btn_new_case.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_new_case.clicked.connect(self.new_case)

        btn_view_submitted_cases = QPushButton("View Submitted Cases", self)
        btn_view_submitted_cases.move(410, 350)
        btn_view_submitted_cases.resize(292, 70)
        btn_view_submitted_cases.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        btn_view_found_cases = QPushButton("View Found Cases", self)
        btn_view_found_cases.move(410, 450)
        btn_view_found_cases.resize(292, 70)
        btn_view_found_cases.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        btn_start_detection = QPushButton("Start Detection", self)
        btn_start_detection.move(410, 550)
        btn_start_detection.resize(292, 70)
        btn_start_detection.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_start_detection.clicked.connect(self.start_detection)

        btn_logout = QPushButton("Log Out", self)
        btn_logout.move(410, 700)
        btn_logout.resize(292, 50)
        btn_logout.setStyleSheet("border: 2px solid black; background: red; color: #fff;")
        btn_logout.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_logout.clicked.connect(self.logout)

        self.show()

    def start_detection(self):
        self.detection_window = DetectionWindow()
        self.detection_window.show()

    def new_case(self):
        self.new_case_window = NewCaseWindow(self.user)
        self.new_case_window.show()

    def display_title(self):
        title = QLabel(self)
        title.setText("Missing Person Detection\nSystem")
        title.setStyleSheet("text-transform: uppercase; font-size: 55px; font-weight: bold;")
        title.move(0, 30)
        title.resize(self.width, 186)
        title.setAlignment(QtCore.Qt.AlignCenter)

    def view_submitted_cases(self):
        URL = "http://localhost:8000/get-cases"
        response = requests.get(URL)
        cases = response.json()
        print(cases)

    def logout(self):
        from loginWindow import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec())