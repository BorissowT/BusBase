from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db.models import session
from db.models import Organisation

from interface.base_admin_interface import BaseAdmin


class AdminUi(QMainWindow, BaseAdmin):

    def __init__(self):
        super(AdminUi, self).__init__()
        loadUi("interface/admin_ui.ui", self)
        self.actionlogout.triggered.connect(self.logout)
        self.label_organisation_name.setText(self.get_organisation_title())
        self.label_admin_name.setText(self.get_user_name())
        self.label_current_income.setText(self.get_organisation_income())
        self.button_vehicle_interface.clicked.connect(self.open_vehicle)

    def get_organisation_title(self):
        organisation_title = session.query(Organisation).first().Title
        return organisation_title

    def get_organisation_income(self):
        organisation_income = session.query(Organisation).first().Income
        return organisation_income

    def get_user_name(self):
        fname = self.user.FirstName
        return fname

    def logout(self):
        from interface.index_interface import IndexUi
        index_page = IndexUi()
        self.widget.addWidget(index_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def open_vehicle(self):
        from interface.vehicle_interface import VehicleUi
        vehicle_page = VehicleUi()
        self.widget.addWidget(vehicle_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
