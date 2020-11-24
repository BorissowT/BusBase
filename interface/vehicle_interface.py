from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db.models import session
from db.models import VehicleBase, Train, Bus
from interface.base_admin_interface import BaseAdmin


class VehicleUi(QMainWindow, BaseAdmin):

    def __init__(self):
        super(VehicleUi, self).__init__()
        loadUi("interface/vehicle_ui.ui", self)
        self.label.setPixmap(QtGui.QPixmap("interface/logos/bus1.png"))
        self.actionlogout.triggered.connect(self.logout)
        self.action_back_to_menu.triggered.connect(self.back_to_menu)
        self.table_bus.setColumnWidth(0, 200)
        self.table_bus.setColumnWidth(1, 200)
        self.table_bus.setColumnWidth(2, 200)
        self.table_bus.setColumnWidth(3, 90)
        self.table_tram.setColumnWidth(0, 200)
        self.table_tram.setColumnWidth(1, 200)
        self.table_tram.setColumnWidth(2, 200)
        self.table_tram.setColumnWidth(3, 90)
        self.loaddata()
        self.button_create.clicked.connect(self.add_vehicle)
        self.label_location.setText(self.get_location())

    def loaddata(self):
        buses = session.query(Bus).all()
        trains = session.query(Train).all()
        row = 0
        self.table_bus.setRowCount(len(buses))
        self.table_tram.setRowCount(len(trains))
        for bus in buses:
            self.table_bus.setItem(row, 0, QtWidgets.QTableWidgetItem(bus.Brand))
            self.table_bus.setItem(row, 1, QtWidgets.QTableWidgetItem(str(bus.ServiceBegin)))
            self.table_bus.setItem(row, 2, QtWidgets.QTableWidgetItem(str(bus.FuelConsumption)))
            self.table_bus.setItem(row, 3, QtWidgets.QTableWidgetItem(str(bus.Mileage)))
            row = row+1
        row = 0
        for train in trains:
            self.table_tram.setItem(row, 0, QtWidgets.QTableWidgetItem(train.Brand))
            self.table_tram.setItem(row, 1, QtWidgets.QTableWidgetItem(str(train.ServiceBegin)))
            self.table_tram.setItem(row, 2, QtWidgets.QTableWidgetItem(str(train.ElectricityPerHour)))
            self.table_tram.setItem(row, 3, QtWidgets.QTableWidgetItem(str(train.Mileage)))
            row = row+1


    def get_location(self):
        location = session.query(VehicleBase).first().Location
        return location

    def add_vehicle(self):
        brand = self.line_brand.text()
        mileage = self.line_milage.text()
        consumption = self.line_consumption.text()
        service_date = self.date_service.date().toPyDate()
        if self.radioBus.isChecked():
            vehicle_base = session.query(VehicleBase).first()
            new_bus = Bus(Brand=brand,
                          Mileage=int(mileage),
                          FuelConsumption=int(consumption),
                          ServiceBegin=service_date,
                          VehicleBase_id=vehicle_base.id)
            session.add(new_bus)
            session.commit()
            self.loaddata()
            self.show_message("SUCCESS")
        if self.radioTram.isChecked():
            vehicle_base = session.query(VehicleBase).first()
            new_bus = Train(Brand=brand,
                            Mileage=int(mileage),
                            ElectricityPerHour=int(consumption),
                            ServiceBegin=service_date,
                            VehicleBase_id=vehicle_base.id)
            session.add(new_bus)
            session.commit()
            self.loaddata()
            self.show_message("SUCCESS")