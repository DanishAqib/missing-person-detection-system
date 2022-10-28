import sys
import face_recognition
import cv2
import numpy as np
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
    def __init__(self, cases = []):
        super().__init__()
        self.title = "Detection"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.cases = cases
        self.entries = {}
        self.person_detected = False
        self.encoded_list = []
        self.video_location = None
        self.image = None
        self.fileName = ""
        self.message_label = None
        self.setStyleSheet(customStyle())

        self.initialize()

    def get_encoded_list(self):
        if self.cases:
            for case in self.cases:
                self.encoded_list.append(case[8])
            return self.encoded_list
        else:
            return []

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.message_label = QLabel(self)
        self.message_label.setText("Video Uploaded")
        self.message_label.setStyleSheet("font-size: 16px; color: #fff; font-weight: bold; border-radius: 5px; background: rgba(255, 0, 0, 0.5);")
        self.message_label.move(450, 125)
        self.message_label.resize(200, 35)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.hide()

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

    def open_file_dialog(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",  "Video Files (*.mp4 *.avi *.flv *.wmv)", options=options)
        if self.fileName:
            self.message_label.show()

    def start_detection(self):
        if self.fileName == "":
            QMessageBox.warning(self, "Warning", "Please upload a video")
            return
        
        self.update_entries()
        if self.entries:
            self.get_encoded_list()
            if self.encoded_list:
                self.detect_face()
            else:
                QMessageBox.warning(self, "Warning", "No cases found")
        else:
            QMessageBox.warning(self, "Warning", "Please fill all the entries")

    def detect_face(self):
        cap = cv2.VideoCapture(self.fileName)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encoded_list, encodeFace)
                faceDis = face_recognition.face_distance(self.encoded_list, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    self.entries["dp_case_id"] = self.cases[matchIndex][0]
                    self.image = img
                    self.person_detected = True
                    name = self.cases[matchIndex][2]
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('CCTV Footage', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.save_to_db()
                self.close()
                break

    def save_to_db(self):
        URL = "http://localhost:8000/add-detected-person"
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        if self.person_detected == False:
            QMessageBox.warning(self, "Warning", "Person not detected")
            return
        else:
            _, buffer = cv2.imencode('.jpg', self.image)
            jpg_as_text = base64.b64encode(buffer)
            self.entries["dp_detected_image"] = jpg_as_text.decode('utf-8')
            try:
                response = requests.post(URL, json.dumps(self.entries), headers=headers)
                if response.status_code == 200:
                    QMessageBox.about(self, "Message", "Person Detected")
                else:
                    QMessageBox.about(self, "Error", "Something went wrong")
            except Exception as e:
                QMessageBox.about(self, "Error", "Couldn't connect to database")

    def update_entries(self):
        if self.video_location.text() != "":
            self.entries["dp_location"] = self.video_location.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetectionWindow()
    sys.exit(app.exec_())
