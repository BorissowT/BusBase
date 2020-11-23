from PyQt5.QtWidgets import QMessageBox
from db.models import session
from db.models import Organisation

class BaseAdmin:
    widget = None
    user = None
    organisation = session.query(Organisation).first()

    def back_to_menu(self):
        from interface.admin_interface import AdminUi
        admin_page = AdminUi()
        admin_page.widget = self.widget
        self.widget.addWidget(admin_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def logout(self):
        from interface.index_interface import IndexUi
        index_page = IndexUi()
        self.widget.addWidget(index_page)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def show_message(self,text):
        msgBox = QMessageBox()
        msgBox.setText(text)
        msgBox.exec_()