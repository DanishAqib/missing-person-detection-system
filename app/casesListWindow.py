import sys
import base64
from PIL import Image
import numpy as np
import io

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView
from PyQt5.QtWidgets import QLabel
from utils import customStyle, format_date_time

class CasesListWindow(QMainWindow):
    def __init__(self, cases=[], case_title=""):
        super().__init__()
        self.title = "Cases List"
        self.width = 1100
        self.height = 850
        self.icon_path = "../resources/icon.png"
        self.cases = cases
        self.case_title = case_title
        self.setStyleSheet(customStyle())

        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        if len(self.cases) == 0:
            self.display_no_cases()
        else:
            self.display_title(self.case_title)
            self.display_cases()

        btn_close = QPushButton("Close", self)
        btn_close.move(410, 720)
        btn_close.resize(292, 40)
        btn_close.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        btn_close.clicked.connect(self.close)
        
        self.show()

    def display_title(self, w_title):
        title = QLabel(w_title, self)
        title.move(400, 20)
        title.resize(292, 30)
        title.setFont(QtGui.QFont("Poppins", 20, QtGui.QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

    def display_cases(self):
        list_ = QListView(self)
        list_.setIconSize(QSize(150, 150))
        list_.setSpacing(20)
        list_.setMinimumSize(1020, 620)
        list_.move(40, 60)
        model = QStandardItemModel(list_)

        for case in self.cases:
            if self.case_title == "Submitted Cases":
                self.display_submitted_cases(case, model)
            else:
                self.display_found_cases(case, model)

        list_.setModel(model)
        list_.show()
        
    def display_submitted_cases(self, case, model):
            image = self.decode_base64(case[8])
            p_case_status = case[7]
            item = QStandardItem(
                "\tCase Status:\t" + p_case_status + 
                "\n\tPerson Name:\t" + case[2] + 
                "\n\tPerson Age:\t" + str(case[3]) +
                "\n\tPerson Gender:\t" + case[4] +
                "\n\tLast seen location:\t" + case[5] +
                "\n\tGuardian contact:\t" + case[6] +
                "\n\tCase Submitted At:\t" + format_date_time(case[10])
            )
            item.setFont(QtGui.QFont("Poppins", 8, QtGui.QFont.Bold))
            item.setText(item.text().title())
            if p_case_status == "found":
                item.setBackground(QtGui.QColor("#4caf50"))
            else:
                item.setBackground(QtGui.QColor("#e28743"))
            image = QtGui.QImage(image,
                                    image.shape[1],
                                    image.shape[0],
                                    image.shape[1] * 3,
                                    QtGui.QImage.Format_RGB888)
            icon = QPixmap(image)
            item.setIcon(QIcon(icon))
            model.appendRow(item)

    def display_found_cases(self, case, model):
        detected_image = self.decode_base64(case[10])
        p_name = case[1]
        p_age = case[2]
        p_gender = case[3]
        p_case_submitted_at = format_date_time(case[6])
        p_detected_location = case[8]
        p_guardian_contact = case[9]
        p_detected_at = format_date_time(case[11])

        item = QStandardItem(
            "\n\tPerson Name:\t" + p_name + 
            "\n\tPerson Age:\t" + str(p_age) +
            "\n\tPerson Gender:\t" + p_gender + 
            "\n\tCase Submitted At:\t" + p_case_submitted_at +
            "\n\tDetected Location:\t" + p_detected_location +
            "\n\tGuardian Contact:\t" + p_guardian_contact +
            "\n\tDetected At:\t" + p_detected_at
        )
        item.setFont(QtGui.QFont("Poppins", 8, QtGui.QFont.Bold))
        item.setText(item.text().title())
        item.setBackground(QtGui.QColor("#4caf50"))
        
        detected_image = QtGui.QImage(detected_image,
                                detected_image.shape[1],
                                detected_image.shape[0],
                                detected_image.shape[1] * 3,
                                QtGui.QImage.Format_RGB888)
        detected_icon = QPixmap(detected_image)
        item.setIcon(QIcon(detected_icon))
        model.appendRow(item)

    def display_no_cases(self):
        no_cases_label = QLabel("No cases found", self)
        no_cases_label.move(430, 250)
        no_cases_label.resize(292, 70)

    def decode_base64(self, img: str):
        img = np.array(Image.open(io.BytesIO(base64.b64decode(img))))
        return img

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec_())