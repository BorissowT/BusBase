from db.models import session
from db.models import Organisation
from interface.login_interface import Ui_MainWindow,QtWidgets

# new_ex = Organisation(Title="NEW")
# session.add(new_ex)
# session.commit()
#
# results = session.query(Organisation).all()
# list = list(map(lambda elem: elem.Title, results))
# print(list)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
