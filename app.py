from db.models import session
from db.models import Organisation
from interface.index_interface import Ui_MainWindow, QtWidgets

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi


class IndexUi(QMainWindow):
    def __init__(self):
        super(IndexUi, self).__init__()
        loadUi("interface/interface_login.ui", self)
        self.log_as_ticketsman.triggered.connect(self.log_as_tick)
        self.log_as_admin.triggered.connect(self.log_as_ad)
        self.log_as_driver.triggered.connect(self.log_as_dr)

    def log_as_ad(self):
        self.initialize_page("admin")

    def log_as_tick(self):
        self.initialize_page("ticketsman")

    def log_as_dr(self):
        self.initialize_page("driver")

    def initialize_page(self, type):
        login_page = LoginUi()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginUi(QMainWindow):
    def __init__(self):
        super(LoginUi, self).__init__()
        loadUi("interface/login_ui.ui", self)
        self.login_button.clicked.connect(self.logout)

    def logout(self):
        index_page = IndexUi()
        widget.addWidget(index_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

app = QApplication(sys.argv)
mainwindow = IndexUi()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(777)
widget.setFixedHeight(569)
widget.show()
app.exec_()


