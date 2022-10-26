# import sys
# import numpy as np

# from PyQt5 import QtGui, QtCore
# from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QCursor
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListView, QBoxLayout, QFileDialog
# from PyQt5.QtWidgets import QMessageBox, QListWidget, QLabel, QLineEdit, QComboBox

# class CasesListWindow(QMainWindow):
#     def __init__(self, cases = []):
#         super().__init__()
#         self.title = "Cases List"
#         self.width = 1100
#         self.height = 850
#         self.icon_path = "../resources/icon.png"
#         self.cases = cases

#         self.initialize()

#     def initialize(self):
#         self.setWindowIcon(QtGui.QIcon(self.icon_path))
#         self.setWindowTitle(self.title)
#         self.setFixedSize(self.width, self.height)

#         # display cases in a list
#         self.cases_list = QListWidget(self)
#         self.cases_list.move(50, 50)
#         self.cases_list.resize(1000, 700)

#         # add cases to the list
#         for case in self.cases:
#             self.cases_list.addItem(case)


#         self.show()

# app = QApplication(sys.argv)
# style = """
#         QWidget{
#             background-image: url(../resources/bg.png);
#         }
#         QLabel{
#             font-family: Poppins;
#             font-size: 30px;
#             font-weight: 600;
#             color: #fff;
#         }
#         QPushButton
#         {
#             background: #00FFE6;
#             border: 3px solid #000;
#             color: #000;
#             text-transform: uppercase;
#             font-size: 18px;
#             font-weight: bold;
#             border-radius: 25px;
#             outline: none;
#         }
#         QPushButton:hover{
#             background: #000;
#             color: #00FFE6;
#         }
#         QLineEdit {
#             padding: 5px 10px;
#             font-size: 18px;
#             border: 3px solid #000;
#             background: #fff;
#             font-family: Poppins;
#             border-radius: 25px;
#         }
#         QMessageBox {
#             background: #fff;
#             color: #000;
#         }
#         QMessageBox QLabel {
#             font-size: 16px;
#             font-weight: normal;
#             background: #fff;
#             color: #000;
#         }
#     """

# # make dummy cases list
# cases = [{
#     "id": 1,
#     "name": "Case 1",
#     "description": "This is case 1",
#     "created_at": "2020-01-01 00:00:00",
#     "updated_at": "2020-01-01 00:00:00"
# }, {
#     "id": 2,
#     "name": "Case 2",
#     "description": "This is case 2",
#     "created_at": "2020-01-01 00:00:00",
#     "updated_at": "2020-01-01 00:00:00"
# }, {
#     "id": 3,
#     "name": "Case 3",
#     "description": "This is case 3",
#     "created_at": "2020-01-01 00:00:00",
#     "updated_at": "2020-01-01 00:00:00"
# }]
# app.setStyleSheet(style)
# window = CasesListWindow(cases)
# sys.exit(app.exec_())