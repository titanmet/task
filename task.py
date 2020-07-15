from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtSql import QSqlQueryModel, QSqlDatabase
from PyQt5.QtWidgets import QTableView, QApplication, QMessageBox, qApp


def createConnection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('task')
    if not db.open():
        QMessageBox.critical(None, qApp.tr("Cannot open database"),
                             qApp.tr("Unable to establish a database connection."),
                             QMessageBox.Cancel)
        return False
    return True


class CustomSqlModel(QSqlQueryModel):
    def __init__(self):
        QSqlQueryModel.__init__(self)
        self.setQuery("Select * from hierarhy")
        self.setHeaderData(0, Qt.Horizontal, "id")
        self.setHeaderData(1, Qt.Horizontal, "id_parent")
        self.setHeaderData(2, Qt.Horizontal, "Name")
        self.setHeaderData(3, Qt.Horizontal, "Image")
        self.setHeaderData(4, Qt.Horizontal, "state")

    def data(self, item, role):
        if role == Qt.BackgroundRole:
            if QSqlQueryModel.data(self, self.index(item.row(), 4), Qt.DisplayRole) == 0:
                return QBrush(Qt.red)
            elif QSqlQueryModel.data(self, self.index(item.row(), 4), Qt.DisplayRole) == 1:
                return QBrush(Qt.yellow)
            elif QSqlQueryModel.data(self, self.index(item.row(), 4), Qt.DisplayRole) == 2:
                return QBrush(Qt.green)
        return QSqlQueryModel.data(self, item, role)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    if not createConnection():
        sys.exit(1)
    model = CustomSqlModel()
    view = QTableView()
    view.resizeColumnsToContents()
    view.setModel(model)
    view.setWindowTitle("List")
    view.hideColumn(0)
    view.hideColumn(1)
    view.hideColumn(4)
    view.setColumnWidth(2, 300)
    view.setColumnWidth(3, 300)
    view.resize(650, 500)
    view.show()
    sys.exit(app.exec_())
