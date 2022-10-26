import sys
import face_recognition
import cv2
from matplotlib.pyplot import get
import requests
import base64
import json

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import QMessageBox, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from utils import customStyle

class DetectionWindow(QMainWindow):
    def __init__(self, user = ""):
        super().__init__()
        self.title = "Detection"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.setStyleSheet(customStyle())
        self.video_label = None
        self.video_location = None
        self.encoded_list = []

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        btn_upload_video = QPushButton("\t\tUpload CCTV Footage", self)
        btn_upload_video.move(410, 180)
        btn_upload_video.resize(282, 70)
        btn_upload_video.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_upload_video.clicked.connect(self.open_file_dialog)
        upload_icon = QIcon()
        upload_icon.addPixmap(QPixmap("../resources/upload-icon.png"), QIcon.Normal, QIcon.Off)
        btn_upload_video.setIcon(upload_icon)
        btn_upload_video.setIconSize(QSize(25, 25))


        self.get_video_location()

        btn_start_detection = QPushButton("START DETECTION", self)
        btn_start_detection.move(410, 460)
        btn_start_detection.resize(282, 40)
        btn_start_detection.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_start_detection.setStyleSheet("background-color: #FF9900")
        btn_start_detection.clicked.connect(self.start_detection)

        self.show()

    def get_video_location(self):
        self.video_location = QLineEdit(self)
        self.video_location.move(410, 300)
        self.video_location.resize(282, 50)
        self.video_location.setPlaceholderText("Enter Footage Location")

    def submit(self):
        QMessageBox.information(self, "Message", "Submitted Successfully")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",  "Video Files (*.mp4 *.avi *.flv *.wmv)", options=options)
        if self.fileName:
            print(self.fileName)

    def start_detection(self):
        self.get_encoded_faces()

    def get_encoded_faces(self):
        response = requests.get("http://127.0.0.1:8000/get-encodings")
        data = json.loads(response.text)
        for i in data:
            self.encoded_list.append(i["encoded_face"])

        print(self.encoded_list)

# if __name__ == "__main__":
app = QApplication(sys.argv)
window = DetectionWindow()
sys.exit(app.exec_())
