import sys
import face_recognition
import cv2
import requests
import base64
import json

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QBoxLayout, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QListWidget, QLabel, QLineEdit, QComboBox
from utils import generate_uuid, customStyle

class NewCaseWindow(QMainWindow):
    def __init__(self, user = "admin"):
        super().__init__()
        self.title = "Register New Case"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.setStyleSheet(customStyle())
        self.user = user
        self.image = None
        self.encoded_image = None
        self.name = None
        self.age = None
        self.gender = None
        self.last_seen_location = None
        self.contact = None

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.show_dummy_image()

        btn_upload_image = QPushButton("\t\tUpload Image", self)
        btn_upload_image.move(700, 150)
        btn_upload_image.resize(282, 70)
        btn_upload_image.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        upload_icon = QIcon()
        upload_icon.addPixmap(QPixmap("../resources/upload-icon.png"), QIcon.Normal, QIcon.Off)
        btn_upload_image.setIcon(upload_icon)
        btn_upload_image.setIconSize(QSize(25, 25))
        btn_upload_image.clicked.connect(self.open_file_dialog)

        self.get_name()
        self.get_age()
        self.get_gender()
        self.get_last_seen_location()

        btn_submit = QPushButton("Submit", self)
        btn_submit.move(700, 650)
        btn_submit.resize(282, 50)
        btn_submit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_submit.clicked.connect(self.on_submit)

        self.show()

    def show_dummy_image(self):
        dummy_image = QPixmap("../resources/uploaded-file.png")
        self.image_label = QLabel(self)
        self.image_label.setPixmap(dummy_image)
        self.image_label.move(100, 200)
        self.image_label.resize(490, 430)
        self.image_label.setScaledContents(True)
        self.image_label.show()

    def get_name(self):
        self.name = QLineEdit(self)
        self.name.setPlaceholderText("Enter name")
        self.name.move(700, 270)
        self.name.resize(282, 55)

    def get_age(self):
        self.age = QLineEdit(self)
        self.age.setPlaceholderText("Enter age")
        self.age.move(700, 360)
        self.age.resize(282, 55)

    def get_gender(self):
        self.gender = QComboBox(self)
        self.gender.addItems(["Select Gender", "Male", "Female", "Other"])
        self.gender.setStyleSheet("QComboBox { padding: 5px 10px; font-size: 18px; border: 3px solid #000; border-radius: 25px; font-family: Poppins; background: #fff; }")
        self.gender.view().setStyleSheet("QListView { border: 0px; width: 0px; font-family: Poppins; background: #fff; }")
        self.gender.setCurrentIndex(0)
        self.gender.model().item(0).setEnabled(False)
        self.gender.move(700, 440)
        self.gender.resize(282, 55)

    def get_last_seen_location(self):
        self.last_seen_location = QLineEdit(self)
        self.last_seen_location.setPlaceholderText("Last location")
        self.last_seen_location.move(700, 520)
        self.last_seen_location.resize(282, 55)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(
                    self, "QFileDialog.getOpenFileName()",
                    "", "jpg file (*.jpg)", options=options)

        if self.fileName:
            img = cv2.cvtColor(cv2.imread(self.fileName), cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(img)
            if len(face_locations) == 0:
                QMessageBox.warning(self, "Error", "No face found in the image")
                return
            self.encoded_image = face_recognition.face_encodings(img)[0]
            self.image = QPixmap(self.fileName)
            self.show_image()

    def show_image(self):
        self.image_label.clear()
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.image)
        self.image_label.setScaledContents(True)
        self.image_label.move(100, 200)
        self.image_label.resize(490, 430)
        self.image_label.show()

    def get_entries(self):
        entries = {}
        if self.name.text() != "" and self.age.text() != "" and self.gender.currentText() != "Select Gender" and self.last_seen_location.text() != "":
            entries["sc_name"] = self.name.text()
            entries["sc_age"] = self.age.text()
            entries["sc_gender"] = self.gender.currentText()
            entries["sc_last_seen_location"] = self.last_seen_location.text()
            return entries
        else:
            return None

    def on_submit(self):
        if self.image is None:
            QMessageBox.about(self, "Error", "Please upload an image")
            return
        entries = self.get_entries()
        if entries:
            entries["sc_case_status"] = "not found"
            entries["sc_face_encoding"] = str(self.encoded_image.tolist())
            entries["sc_id"] = generate_uuid()
            self.save_to_db(entries, self.user)
        else:
            QMessageBox.about(self, "Error", "Please fill all entries")

    def save_to_db(self, entries, user):
        URL = "http://localhost:8000/submit-case"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        byte_content = open(self.fileName, "rb").read()
        base64_bytes = base64.b64encode(byte_content)
        base64_string = base64_bytes.decode('utf-8')

        entries['sc_case_image'] = base64_string
        entries['sc_submitted_by'] = user
        try:
            response = requests.post(URL, json.dumps(entries), headers=headers)
            if response.status_code == 200:
                QMessageBox.about(self, "Success", "Case submitted successfully")
                self.name.clear()
                self.age.clear()
                self.gender.setCurrentIndex(0)
                self.last_seen_location.clear()
                self.image_label.clear()
                self.image = None
                self.fileName = None
                self.show_dummy_image()
                self.close()
            else:
                QMessageBox.about(self, "Error", "Something went wrong")
        except Exception as e:
            QMessageBox.about(self, "Error", "Couldn't connect to database")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewCaseWindow()
    sys.exit(app.exec_())