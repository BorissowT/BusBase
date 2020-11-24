from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtGui

from db.models import Administrator, Ticketsman, Driver
from db.models import session

from interface.base_admin_interface import BaseAdmin
from interface.base_user_interface import BaseUser


class LoginUi(QMainWindow, BaseAdmin):
    log_type = None

    def __init__(self):
        super(LoginUi, self).__init__()
        loadUi("interface/login_ui.ui", self)
        self.login_button.clicked.connect(self.login)
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
        self.widget.addWidget(login_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def login(self):
        if self.log_type == "admin":
            self.admin_login()

        if self.log_type == "ticketsman":
            self.ticketsman_login()

        if self.log_type == "driver":
            self.driver_login()

    def admin_login(self):
        first_name = self.First_name_input.text()
        last_name = self.last_name_input.text()
        admin = session.query(Administrator).filter(Administrator.FirstName == first_name,
                                                    Administrator.LastName == last_name).first()
        if not admin:
            self.show_message("Wrong firstname or lastname!")
        else:
            from interface.admin_interface import AdminUi
            BaseAdmin.user = admin
            admin_page = AdminUi()
            self.widget.addWidget(admin_page)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def ticketsman_login(self):
        first_name = self.First_name_input.text()
        last_name = self.last_name_input.text()
        ticketsman = session.query(Ticketsman).filter(Ticketsman.FirstName == first_name,
                                                      Ticketsman.LastName == last_name).first()
        if not ticketsman:
            self.show_message("Wrong firstname or lastname!")
        else:
            from interface.ticketsman_interface import TicketsmanUi
            BaseUser.user = ticketsman
            ticketsman_page = TicketsmanUi()
            self.widget.addWidget(ticketsman_page)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def driver_login(self):
        first_name = self.First_name_input.text()
        last_name = self.last_name_input.text()
        driver = session.query(Driver).filter(Driver.FirstName == first_name,
                                              Driver.LastName == last_name).first()
        if not driver:
            self.show_message("Wrong firstname or lastname!")
        else:
            pass





