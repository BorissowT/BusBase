from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from db.models import session
from db.models import Organisation, DriverReport, TicketsmanReport, Bus, Train

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
        self.button_routes_interface.clicked.connect(self.open_routes)
        self.button_personal_interface.clicked.connect(self.open_pm)
        self.button_reports_interface.clicked.connect(self.open_reports)
        self.button_income_recount.clicked.connect(self.recount_income)

    def get_organisation_title(self):
        organisation_title = self.organisation.Title
        return organisation_title

    def get_organisation_income(self) -> str:
        organisation_income = session.query(Organisation).first().Income
        return str(organisation_income)

    def get_user_name(self):
        fname = self.user.FirstName
        return fname

    def open_vehicle(self):
        from interface.vehicle_interface import VehicleUi
        vehicle_page = VehicleUi()
        self.widget.addWidget(vehicle_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def open_routes(self):
        from interface.routes_interface import RouteUi
        vehicle_page = RouteUi()
        self.widget.addWidget(vehicle_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def open_pm(self):
        from interface.pm_interface import PersonalManagementUi
        pm_page = PersonalManagementUi()
        self.widget.addWidget(pm_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def open_reports(self):
        from interface.reports_interface import ReportsUi
        reports_page = ReportsUi()
        self.widget.addWidget(reports_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def recount_income(self):
        ticketsman_reports = session.query(TicketsmanReport).all()
        driver_reports = session.query(DriverReport).all()
        income = 0
        for tick_rep in ticketsman_reports:
            income = income + tick_rep.Money
        for driv_rep in driver_reports:
            if driv_rep.Train_id:
                train = session.query(Train).filter(Train.id == driv_rep.Train_id).first()
                income = income-(train.ElectricityPerHour*driv_rep.Mileage)
            if driv_rep.Bus_id:
                bus = session.query(Bus).filter(Bus.id == driv_rep.Bus_id).first()
                income = income - (bus.FuelConsumption * driv_rep.Mileage)
        self.organisation.Income = income
        session.commit()
        self.label_current_income.setText(str(income))
