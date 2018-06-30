import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QPushButton
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QStringListModel
from PyQt5 import uic


class GSMMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/MainWindow.ui", self)

        self.copyButton = self.findChild(QPushButton, "copyButton")
        self.replaceButton = self.findChild(QPushButton, "replaceButton")
        self.restoreButton = self.findChild(QPushButton, "restoreButton")

        self.pluginsList = self.findChild(QListView, "pluginsList")
        # self.pluginsList.setEditTriggers(QListView.NoEditTriggers)

        self.setWindowTitle("GamesSM")
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = GSMMainWindow()

    m = QStandardItemModel()
    for i in range(50):
        m.appendRow(QStandardItem(QIcon.fromTheme("edit-undo"), str(i)))
    w.pluginsList.setModel(m)

    sys.exit(app.exec_())
