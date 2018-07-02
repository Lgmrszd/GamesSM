import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTableWidget, QPushButton, QAction
from PyQt5 import uic


class SettingsWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/Settings.ui", self)


class GSMMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/MainWindow.ui", self)

        self.settingsWindow = SettingsWindow()

        self.copyButton = self.findChild(QPushButton, "copyButton")
        self.replaceButton = self.findChild(QPushButton, "replaceButton")
        self.restoreButton = self.findChild(QPushButton, "restoreButton")

        self.pluginsList = self.findChild(QListWidget, "pluginsList")
        self.savedSlots = self.findChild(QTableWidget, "savedSlots")
        self.gameSlots = self.findChild(QListWidget, "gameSlots")

        self.actionSettings = self.findChild(QAction, "actionSettings")
        assert isinstance(self.actionSettings, QAction)
        self.actionSettings.triggered.connect(self.settingsWindow.show)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = GSMMainWindow()
    w.show()
    sys.exit(app.exec_())
