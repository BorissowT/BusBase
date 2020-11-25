from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtGui

from interface.base_user_interface import BaseUser
from db.models import session
from db.models import Bus, Train, Route, DayReport, DriverReport, Driver
import re

class DriverUi(QMainWindow, BaseUser):

    def __init__(self):
        super(DriverUi, self).__init__()
        loadUi("interface/driver_ui.ui", self)
        self.label.setPixmap(QtGui.QPixmap("interface/logos/bus1.png"))
        self.actionlogout.triggered.connect(self.logout)
        self.label_organisation_name.setText(self.get_organisation_name())
        self.label_user_name.setText(self.get_user_name())

        self.load_items_to_tram_cb()
        self.load_items_to_bus_cb()
        self.load_items_to_route_cb()
        self.combo_bus.setDisabled(True)
        self.combo_tram.setDisabled(True)
        self.radio_tram.toggled.connect(self.radio_toggled)
        self.radio_bus.toggled.connect(self.radio_toggled)
        self.button_add_report.clicked.connect(self.add_report)

    def load_items_to_tram_cb(self):
        trains = session.query(Train).all()
        for tram in trains:
            self.combo_tram.addItem("{0} id={1}".format(tram.Brand, tram.id))

    def load_items_to_bus_cb(self):
        buses = session.query(Bus).all()
        for bus in buses:
            self.combo_bus.addItem("{0} id={1}".format(bus.Brand, bus.id))

    def load_items_to_route_cb(self):
        routes = session.query(Route).all()
        for route in routes:
            self.combo_route.addItem("{0} id={1}".format(route.Title, route.id))

    def radio_toggled(self):
        if self.radio_tram.isChecked():
            self.combo_tram.setDisabled(False)
            self.combo_bus.setDisabled(True)
        if self.radio_bus.isChecked():
            self.combo_tram.setDisabled(True)
            self.combo_bus.setDisabled(False)

    def add_report(self):
        date = self.date.date().toPyDate()
        day_report = session.query(DayReport).filter(DayReport.Date == date).first()
        mileage = self.spin_mileage.value()
        problems = self.line_problems.text()
        route = self.get_route_object(self.combo_route.currentText())
        vehicle = None
        type = None
        if self.radio_bus.isChecked():
            bus = self.combo_bus.currentText()
            type = "bus"
            vehicle = self.get_vehicle_object(bus, type)
        if self.radio_tram.isChecked():
            tram = self.combo_tram.currentText()
            type = "tram"
            vehicle = self.get_vehicle_object(tram, type)
        data = {"date": date, "mileage": mileage, "problems": problems, "route": route, "vehicle": vehicle,
                "type": type}
        if not day_report:
            self.create_day_report_with_driverreport_inside(data)
        if day_report:
            if not day_report.DriverReport_id:
                self.create_driverreport_and_add_to_existing_dayreport(day_report, data)
            else:
                self.create_day_report_with_driverreport_inside(data)

    def get_vehicle_object(self, string, type):
        line = string.split()
        id = line[len(line)-1][3:]
        if type == "bus":
            vehicle = session.query(Bus).filter(Bus.id == id).first()
        if type == "tram":
            vehicle = session.query(Train).filter(Train.id == id).first()
        return vehicle

    def get_route_object(self, string):
        line = string.split()
        id = line[len(line) - 1][3:]
        route = session.query(Route).filter(Route.id == id).first()
        return route

    def create_day_report_with_driverreport_inside(self, data):
        new_driverreport = None
        if data["type"] == "bus":
            new_driverreport = DriverReport(
                Problems=data["problems"],
                Mileage=data["mileage"],
                Bus_id=data["vehicle"].id,
                Route_id=data["route"].id,
                Driver_id=self.user.id
            )
        if data["type"] == "tram":
            new_driverreport = DriverReport(
                Problems=data["problems"],
                Mileage=data["mileage"],
                Train_id=data["vehicle"].id,
                Route_id=data["route"].id,
                Driver_id=self.user.id
            )
        session.add(new_driverreport)
        session.flush()
        new_dayreport = DayReport(
            Organisation_id=self.organisation.id,
            Date=data["date"],
            DriverReport_id=new_driverreport.id
        )
        session.add(new_dayreport)
        session.commit()

    def create_driverreport_and_add_to_existing_dayreport(self, day_report, data):
        new_driverreport = None
        if data["type"] == "bus":
            new_driverreport = DriverReport(
                Problems=data["problems"],
                Mileage=data["mileage"],
                Bus_id=data["vehicle"].id,
                Route_id=data["route"].id,
                Driver_id=self.user.id
            )
        if data["type"] == "tram":
            new_driverreport = DriverReport(
                Problems=data["problems"],
                Mileage=data["mileage"],
                Train_id=data["vehicle"].id,
                Route_id=data["route"].id,
                Driver_id=self.user.id
            )
        session.add(new_driverreport)
        session.flush()
        day_report.DriverReport_id = new_driverreport.id
        session.commit()