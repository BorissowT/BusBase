from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from db.models import session, DayReport, TicketsmanReport
from interface.base_admin_interface import BaseAdmin
from interface.base_user_interface import BaseUser


class TicketsmanUi(QMainWindow, BaseUser):

    def __init__(self):
        super(TicketsmanUi, self).__init__()
        loadUi("interface/ticketsman_ui.ui", self)
        self.label.setPixmap(QtGui.QPixmap("interface/logos/bus1.png"))
        self.actionlogout.triggered.connect(self.logout)
        self.label_organisation_name.setText(self.get_organisation_name())
        self.label_user_name.setText(self.get_user_name())
        self.button_create.clicked.connect(self.add_report)

    def add_report(self):
        money = self.line_money.text()
        hours = self.spin_hours.value()
        date = self.date.date().toPyDate()
        if self.check_dayreports_by_date(date):
            if self.check_if_dayreport_has_ticketsmans_report(date):
                self.create_new_dayreport_and_ticketsman_report(date, money, hours)
            else:
                day_report = session.query(DayReport).filter(DayReport.Date == date).first()
                new_ticketsman_report = self.commit_and_get_report_back(money, hours)
                day_report.TicketsmanReport_id = new_ticketsman_report.id
                session.commit()
                self.show_message("SUCCESS")
        else:
            self.create_new_dayreport_and_ticketsman_report(date, money, hours)

    def create_new_dayreport_and_ticketsman_report(self, date, money, hours):
        new_ticketsman_report = self.commit_and_get_report_back(money, hours)
        new_day_report = DayReport(
            Organisation_id=self.organisation.id,
            Date=date,
            TicketsmanReport_id=new_ticketsman_report.id)
        session.add(new_day_report)
        session.commit()
        self.show_message("SUCCESS")

    def commit_and_get_report_back(self, money, hours):
        new_ticketsman_report = TicketsmanReport(Ticketsman_id=self.user.id, Money=money, WorkTime=hours)
        session.add(new_ticketsman_report)
        ##to get id of added report
        session.flush()
        session.commit()
        return new_ticketsman_report

    def check_if_dayreport_has_ticketsmans_report(self,date):
        day_report = session.query(DayReport).filter(DayReport.Date == date).first()
        if day_report.TicketsmanReport_id:
            return True
        else:
            return False