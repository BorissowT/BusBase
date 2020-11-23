import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi


def start_interface():
    app = QApplication(sys.argv)
    mainwindow = IndexUi()
    global widget
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(777)
    widget.setFixedHeight(569)
    widget.show()
    app.exec_()


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
        login_page.log_type = type
        login_page.widget = widget
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

from interface.login_interface import LoginUi


