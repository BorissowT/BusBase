from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from interface.base_admin_interface import BaseAdmin
from db.models import session
from db.models import Route, Station


class RouteUi(QMainWindow, BaseAdmin):
    current_route = None

    def __init__(self):
        super(RouteUi, self).__init__()
        loadUi("interface/routes_ui.ui", self)
        self.actionlogout.triggered.connect(self.logout)
        self.action_back_to_menu.triggered.connect(self.back_to_menu)

        self.table_routes.setColumnWidth(0, 140)
        self.table_routes.setColumnWidth(1, 140)
        self.table_stations.setColumnWidth(0, 140)
        self.table_stations.setColumnWidth(1, 140)
        self.button_add_station.setDisabled(True)
        self.button_add_route.clicked.connect(self.add_route)
        self.button_add_station.clicked.connect(self.add_station)
        self.loadroutes()

    def loadroutes(self):
        routes = session.query(Route).all()
        row = 0
        self.table_routes.setRowCount(len(routes))
        self.table_routes.itemClicked.connect(self.edit_route)
        for route in routes:
            stations = session.query(Station).filter(Station.Route_id == int(route.id)).all()
            self.table_routes.setItem(row, 0, QtWidgets.QTableWidgetItem(route.Title))
            self.table_routes.setItem(row, 1, QtWidgets.QTableWidgetItem(str(len(stations))))
            row = row + 1

    def loadstations(self, stations):
        row = 0
        self.table_stations.setRowCount(len(stations))
        self.button_add_station.setDisabled(False)
        for station in stations:
            self.table_stations.setItem(row, 0, QtWidgets.QTableWidgetItem(station.Title))
            self.table_stations.setItem(row, 1, QtWidgets.QTableWidgetItem(station.Zone))
            row = row + 1

    def edit_route(self, item):
        route = session.query(Route).filter(Route.Title == str(item.text())).first()
        self.current_route = route
        try:
            stations = session.query(Station).filter(Station.Route_id == self.current_route.id).all()
            self.loadstations(stations)
        except:
            self.show_message("choose by Title!")

    def add_route(self):
        title = self.line_route_title.text()
        new_route = Route(Title=title, Organisation_id=self.organisation.id)
        session.add(new_route)
        session.commit()
        self.loadroutes()
        self.show_message("SUCCESS")

    def add_station(self):
        title = self.line_station_title.text()
        if self.radioA.isChecked():
            self.station_transaction(title=title, zone="A")

        if self.radioB.isChecked():
            self.station_transaction(title=title, zone="B")

        if self.radioC.isChecked():
            self.station_transaction(title=title, zone="C")

    def station_transaction(self, zone, title):
        new_station = Station(Title=title, Zone=zone, Route_id=self.current_route.id)
        session.add(new_station)
        session.commit()
        stations = session.query(Station).filter(Station.Route_id == self.current_route.id).all()
        self.loadstations(stations)
        self.loadroutes()
        self.show_message("SUCCESS")


