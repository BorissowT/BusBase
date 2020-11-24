from PyQt5.QtWidgets import QMessageBox
from db.models import session
from db.models import Organisation, DayReport


class BaseUser:
    widget = None
    user = None
    organisation = session.query(Organisation).first()

    def logout(self):
        from interface.index_interface import IndexUi
        index_page = IndexUi()
        self.widget.addWidget(index_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def show_message(self, text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.exec_()

    def get_organisation_name(self):
        return self.organisation.Title

    def get_user_name(self):
        return "{0} {1}".format(self.user.LastName, self.user.FirstName)

    def check_dayreports_by_date(self, date):
        day_report = session.query(DayReport).filter(DayReport.Date == date).first()
        if day_report:
            return True
        else:
            return False
