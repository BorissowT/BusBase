from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db.models import session
from db.models import DayReport, DriverReport, TicketsmanReport, Driver, Ticketsman, Bus, Train, Route
from interface.base_admin_interface import BaseAdmin


class ReportsUi(QMainWindow, BaseAdmin):

    def __init__(self):
        super(ReportsUi, self).__init__()
        loadUi("interface/reports_managment_ui.ui", self)
        self.label.setPixmap(QtGui.QPixmap("interface/logos/bus1.png"))
        self.actionlogout.triggered.connect(self.logout)
        self.action_back_to_menu.triggered.connect(self.back_to_menu)

        self.loadallreports()
        self.button_loadall.clicked.connect(self.loadallreports)
        self.button_load_all_tick.clicked.connect(self.load_all_tick)
        self.button_load_all_driv.clicked.connect(self.load_all_driv)
        self.button_search_by_data.clicked.connect(self.load_by_data)
        self.button_search_by_name.clicked.connect(self.load_by_name)

    def loadallreports(self):
        tick_reports = session.query(TicketsmanReport).all()
        driver_reports = session.query(DriverReport).all()
        row = 0
        self.table_reports.setRowCount(len(tick_reports)+len(driver_reports))
        for tick in tick_reports:
            date = session.query(DayReport).filter(DayReport.TicketsmanReport_id == tick.id).first().Date
            worker = session.query(Ticketsman).filter(Ticketsman.id == tick.Ticketsman_id).first().LastName
            vehicle = "-"
            route = "-"
            mileage = "-"
            problems = "-"
            worktime = tick.WorkTime
            money = tick.Money
            self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
            row = row +1
        for driver in driver_reports:
            date = session.query(DayReport).filter(DayReport.DriverReport_id == driver.id).first().Date
            worker = session.query(Driver).filter(Driver.id == driver.Driver_id).first().LastName
            tram = driver.Train_id
            bus = driver.Bus_id
            if tram:
                vehicle = session.query(Train).filter(Train.id == tram).first().Brand
            if bus:
                vehicle = session.query(Bus).filter(Bus.id == bus).first().Brand
            route = session.query(Route).filter(Route.id == driver.Route_id).first().Title
            mileage = driver.Mileage
            problems = driver.Problems
            worktime = "-"
            money = "-"
            self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
            row = row + 1

    def load_all_tick(self):
        tick_reports = session.query(TicketsmanReport).all()
        row = 0
        self.table_reports.setRowCount(len(tick_reports))
        for tick in tick_reports:
            date = session.query(DayReport).filter(DayReport.TicketsmanReport_id == tick.id).first().Date
            worker = session.query(Ticketsman).filter(Ticketsman.id == tick.Ticketsman_id).first().LastName
            vehicle = "-"
            route = "-"
            mileage = "-"
            problems = "-"
            worktime = tick.WorkTime
            money = tick.Money
            self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
            row = row + 1

    def load_all_driv(self):
        driver_reports = session.query(DriverReport).all()
        row = 0
        self.table_reports.setRowCount(len(driver_reports))
        for driver in driver_reports:
            date = session.query(DayReport).filter(DayReport.DriverReport_id == driver.id).first().Date
            worker = session.query(Driver).filter(Driver.id == driver.Driver_id).first().LastName
            tram = driver.Train_id
            bus = driver.Bus_id
            if tram:
                vehicle = session.query(Train).filter(Train.id == tram).first().Brand
            if bus:
                vehicle = session.query(Bus).filter(Bus.id == bus).first().Brand
            route = session.query(Route).filter(Route.id == driver.Route_id).first().Title
            mileage = driver.Mileage
            problems = driver.Problems
            worktime = "-"
            money = "-"
            self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
            row = row + 1

    def load_by_data(self):
        date = self.data_search.date().toPyDate()
        day_reports = session.query(DayReport).filter(DayReport.Date == date).all()
        self.table_reports.setRowCount(len(day_reports)*2)
        self.clear_all_rows(len(day_reports)*2)
        row = 0
        for report in day_reports:
            tick_report = session.query(TicketsmanReport).filter(TicketsmanReport.id == report.TicketsmanReport_id)\
                .first()
            driver_report = session.query(DriverReport).filter(DriverReport.id == report.DriverReport_id).first()
            if tick_report:
                worker = session.query(Ticketsman).filter(Ticketsman.id == tick_report.Ticketsman_id).first().LastName
                vehicle = "-"
                route = "-"
                mileage = "-"
                problems = "-"
                worktime = tick_report.WorkTime
                money = tick_report.Money
                self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
                row = row + 1
            if driver_report:
                worker = session.query(Driver).filter(Driver.id == driver_report.Driver_id).first().LastName
                tram = driver_report.Train_id
                bus = driver_report.Bus_id
                if tram:
                    vehicle = session.query(Train).filter(Train.id == tram).first().Brand
                if bus:
                    vehicle = session.query(Bus).filter(Bus.id == bus).first().Brand
                route = session.query(Route).filter(Route.id == driver_report.Route_id).first().Title
                mileage = driver_report.Mileage
                problems = driver_report.Problems
                worktime = "-"
                money = "-"
                self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
                row = row + 1

    def load_by_name(self):
        firstname = self.line_firstname.text()
        lastname = self.line_lastname.text()
        ticketsman = session.query(Ticketsman).filter(Ticketsman.FirstName == firstname,
                                                      Ticketsman.LastName == lastname).first()
        driver = session.query(Driver).filter(Driver.FirstName == firstname,
                                              Driver.LastName == lastname).first()
        if ticketsman:
            reports = session.query(TicketsmanReport).filter(TicketsmanReport.Ticketsman_id == ticketsman.id).all()
            self.table_reports.setRowCount(len(reports))
            row = 0
            for report in reports:
                date = session.query(DayReport).filter(DayReport.TicketsmanReport_id == report.id).first().Date
                worker = ticketsman.LastName
                vehicle = "-"
                route = "-"
                mileage = "-"
                problems = "-"
                worktime = report.WorkTime
                money = report.Money
                self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
                row = row + 1
        if driver:
            reports = session.query(DriverReport).filter(DriverReport.Driver_id == driver.id).all()
            self.table_reports.setRowCount(len(reports))
            row = 0
            for report in reports:
                date = session.query(DayReport).filter(DayReport.DriverReport_id == report.id).first().Date
                worker = driver.LastName
                tram = report.Train_id
                bus = report.Bus_id
                if tram:
                    vehicle = session.query(Train).filter(Train.id == tram).first().Brand
                if bus:
                    vehicle = session.query(Bus).filter(Bus.id == bus).first().Brand
                route = session.query(Route).filter(Route.id == report.Route_id).first().Title
                mileage = report.Mileage
                problems = report.Problems
                worktime = "-"
                money = "-"
                self.fill_row(date, worker, vehicle, route, mileage, problems, worktime, money, row)
                row = row + 1

    def clear_all_rows(self, count):
        for row in range(count):
            self.table_reports.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 4, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 5, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 6, QtWidgets.QTableWidgetItem(""))
            self.table_reports.setItem(row, 7, QtWidgets.QTableWidgetItem(""))

    def fill_row(self, date, worker, vehicle, route, mileage, problems, worktime, money, row):
        self.table_reports.setItem(row, 0, QtWidgets.QTableWidgetItem(str(date)))
        self.table_reports.setItem(row, 1, QtWidgets.QTableWidgetItem(worker))
        self.table_reports.setItem(row, 2, QtWidgets.QTableWidgetItem(vehicle))
        self.table_reports.setItem(row, 3, QtWidgets.QTableWidgetItem(route))
        self.table_reports.setItem(row, 4, QtWidgets.QTableWidgetItem(str(mileage)))
        self.table_reports.setItem(row, 5, QtWidgets.QTableWidgetItem(problems))
        self.table_reports.setItem(row, 6, QtWidgets.QTableWidgetItem(str(worktime)))
        self.table_reports.setItem(row, 7, QtWidgets.QTableWidgetItem(str(money)))