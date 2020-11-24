from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from interface.base_admin_interface import BaseAdmin

from db.models import session
from db.models import Department, Driver, Ticketsman


class PersonalManagementUi(QMainWindow, BaseAdmin):
    department = None

    def __init__(self):
        super(PersonalManagementUi, self).__init__()
        loadUi("interface/pm_ui.ui", self)
        self.actionlogout.triggered.connect(self.logout)
        self.action_back_to_menu.triggered.connect(self.back_to_menu)

        self.label.setPixmap(QtGui.QPixmap("interface/logos/bus1.png"))
        self.spin_experience.setDisabled(True)
        self.radio_ticketsman.toggled.connect(self.radio_toggled)
        self.radio_driver.toggled.connect(self.radio_toggled)
        self.label_department_location.setText(self.get_location())
        self.table_personal.setColumnWidth(0, 142)
        self.table_personal.setColumnWidth(1, 142)
        self.table_personal.setColumnWidth(2, 142)
        self.table_personal.setColumnWidth(3, 142)
        self.table_personal.setColumnWidth(4, 142)
        self.loadpersonal()
        self.button_create.clicked.connect(self.add_worker)

    def get_location(self):
        department = session.query(Department).first()
        self.department = department
        location = department.Location
        return location

    def loadpersonal(self):
        drivers = session.query(Driver).all()
        ticketsmen = session.query(Ticketsman).all()
        row = 0
        self.table_personal.setRowCount(len(drivers)+len(ticketsmen))
        for driver in drivers:
            self.table_personal.setItem(row, 0, QtWidgets.QTableWidgetItem(driver.FirstName))
            self.table_personal.setItem(row, 1, QtWidgets.QTableWidgetItem(driver.LastName))
            self.table_personal.setItem(row, 2, QtWidgets.QTableWidgetItem(str(driver.Salary)))
            self.table_personal.setItem(row, 3, QtWidgets.QTableWidgetItem(str(driver.Experience)))
            self.table_personal.setItem(row, 4, QtWidgets.QTableWidgetItem("Driver"))
            row = row + 1
        for tick in ticketsmen:
            self.table_personal.setItem(row, 0, QtWidgets.QTableWidgetItem(tick.FirstName))
            self.table_personal.setItem(row, 1, QtWidgets.QTableWidgetItem(tick.LastName))
            self.table_personal.setItem(row, 2, QtWidgets.QTableWidgetItem(str(tick.Salary)))
            self.table_personal.setItem(row, 4, QtWidgets.QTableWidgetItem("Ticketsman"))
            row = row + 1

    def radio_toggled(self):
        if self.radio_ticketsman.isChecked():
            self.spin_experience.setDisabled(True)
        if self.radio_driver.isChecked():
            self.spin_experience.setDisabled(False)

    def add_worker(self):
        firstname = self.line_firstname.text()
        lastname = self.line_lastname.text()
        salary = self.line_salary.text()
        if self.radio_ticketsman.isChecked():
            self.add_ticketsman(firstname, lastname, salary)
        if self.radio_driver.isChecked():
            self.add_driver(firstname, lastname, salary)

    def add_ticketsman(self, firstname, lastname, salary):
        new_ticketsman = Ticketsman(
            FirstName=firstname,
            LastName=lastname,
            Salary=salary,
            Department_id=self.department.id
        )
        session.add(new_ticketsman)
        session.commit()
        self.loadpersonal()
        self.show_message("SUCCESS")

    def add_driver(self, firstname, lastname, salary):
        experience = self.spin_experience.value()
        new_driver = Driver(
            FirstName=firstname,
            LastName=lastname,
            Salary=salary,
            Experience=experience,
            Department_id=self.department.id
        )
        session.add(new_driver)
        session.commit()
        self.loadpersonal()
        self.show_message("SUCCESS")


