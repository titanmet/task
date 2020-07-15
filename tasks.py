import sys

from ui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtSql
from PyQt5 import QtCore


class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('task')
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('hierarhy')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "id_parent")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "name")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "image")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "state")
        self.ui.tableWidget.setModel(self.model)
        self.ui.tableWidget.hideColumn(0)
        self.ui.tableWidget.hideColumn(1)
        self.ui.tableWidget.hideColumn(4)
        self.ui.tableWidget.setColumnWidth(2, 300)
        self.ui.tableWidget.setColumnWidth(3, 333)

        self.ui.pushButton.clicked.connect(self.addToDb)
        self.show()
        self.ui.pushButton_2.clicked.connect(self.delrow)
        self.i = self.model.rowCount()

    def addToDb(self):
        print(self.i)
        self.model.insertRows(self.i, 1)
        self.model.setData(self.model.index(self.i, 1), self.ui.tableWidget.currentIndex())
        self.model.setData(self.model.index(self.i, 2), self.ui.tableWidget.currentIndex())
        self.model.setData(self.model.index(self.i, 4), self.ui.tableWidget.currentIndex())
        self.model.setData(self.model.index(self.i, 3), self.ui.tableWidget.currentIndex())
        self.model.submitAll()
        self.i += 1

    def delrow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            self.model.removeRow(self.ui.tableWidget.currentIndex().row())
            self.i -= 1
            self.model.select()
        else:
            QMessageBox.question(self, 'Message', "Пожалуйста, выберите строку, которую вы хотите удалить",
                                 QMessageBox.Ok)
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = Form()
    sys.exit(app.exec_())
