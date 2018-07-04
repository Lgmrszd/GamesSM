import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QPushButton, QAction, QLabel
from PyQt5.QtGui import QColor, QBrush
from PyQt5 import uic
from PyQt5.QtCore import QObject, Qt
import plugins


class PluginSettingsRow(QObject):
    columns = ["Name", "Enabled"]

    class PluginWidgetItem(QTableWidgetItem):
        def __init__(self, plugin_row, *args):
            super().__init__(*args)
            self.plugin_row = plugin_row
            self.plugin = plugin_row.plugin

    def __init__(self, plugin: plugins.Plugin):
        super().__init__()
        self.plugin = plugin
        self.name_widg = self.PluginWidgetItem(self, self.plugin.name)
        self.enab_widg = self.PluginWidgetItem(self, self._str_enabled())
        if self.plugin.broken:
            self.mark_broken()

    def mark_broken(self):
        self.name_widg.setBackground(QColor(255, 100, 100))
        self.enab_widg.setBackground(QColor(255, 100, 100))

    def mark_normal(self):
        self.name_widg.setBackground(QBrush())
        self.enab_widg.setBackground(QBrush())

    def _str_enabled(self):
        if self.plugin.enabled:
            return self.tr("Yes")
        return self.tr("No")

    def update_status(self):
        self.enab_widg.setText(self._str_enabled())

    def insert_into_table(self, table: QTableWidget):
        r = table.rowCount()
        table.insertRow(r)
        table.setItem(r, 0, self.name_widg)
        table.setItem(r, 1, self.enab_widg)


class SettingsWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/Settings.ui", self)

        self.current_plugin = None  # type: plugins.Plugin

        self.pluginLabel: QLabel = self.findChild(QLabel, "pluginLabel")

        self.toggleButton: QPushButton = self.findChild(QPushButton, "toggleButton")
        self.toggleButton.setDisabled(True)
        self.toggleButton.clicked.connect(self.on_toggle_button_clicked)

        self.pluginsTable: QTableWidget = self.findChild(QTableWidget, "pluginsTable")

        # self.pluginsTable.setFixedWidth(300)
        self.pluginsTable.setColumnCount(len(PluginSettingsRow.columns))
        # self.pluginsTable.setColumnWidth(1, 20)
        self.pluginsTable.setHorizontalHeaderLabels(PluginSettingsRow.columns)
        self.pluginsTable.itemClicked.connect(self.on_item_selected)
        self.load_plugins()

    def update_label(self):
        text = ("Name: {}\n"
                "Description: {}")
        text = text.format(self.current_plugin.name, self.current_plugin.description)
        if self.current_plugin.broken:
            text = "Name: {}\n".format(self.current_plugin.name)
            text = text + "This plugin is broken; please, reinstall this plugin"
        self.pluginLabel.setText(text)

    def update_button(self):
        if self.current_plugin.broken:
            self.toggleButton.setDisabled(True)
            self.toggleButton.setText(self.tr("Select plugin..."))
        elif self.current_plugin.enabled:
            self.toggleButton.setDisabled(False)
            self.toggleButton.setText(self.tr("Disable"))
        else:
            self.toggleButton.setDisabled(False)
            self.toggleButton.setText(self.tr("Enable"))

    def on_toggle_button_clicked(self, _):
        self.current_plugin.enabled = not self.current_plugin.enabled
        self.current_plugin.save()
        self.update_button()
        self.pluginsTable.currentItem().plugin_row.update_status()

    def on_item_selected(self, item: PluginSettingsRow.PluginWidgetItem):
        self.toggleButton.setDisabled(False)
        self.current_plugin = item.plugin
        self.update_button()
        self.update_label()

    def load_plugins(self):
        plugins_rows = []
        for plugin in plugins.get_plugins_list():
            plugins_rows.append(PluginSettingsRow(plugin))

        for plugin_row in plugins_rows:
            plugin_row.insert_into_table(self.pluginsTable)


class GSMMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/MainWindow.ui", self)

        self.settingsWindow = SettingsWindow()

        self.copyButton: QPushButton = self.findChild(QPushButton, "copyButton")
        self.restoreButton: QPushButton = self.findChild(QPushButton, "restoreButton")
        self.replaceButton: QPushButton = self.findChild(QPushButton, "replaceButton")

        self.pluginsList: QListWidget = self.findChild(QListWidget, "pluginsList")
        self.savedSlots: QTableWidget = self.findChild(QTableWidget, "savedSlots")
        self.gameSlots: QListWidget = self.findChild(QListWidget, "gameSlots")

        self.actionSettings: QAction = self.findChild(QAction, "actionSettings")
        self.actionSettings.triggered.connect(self.settingsWindow.show)

        self.load_plugins()

    def load_plugins(self):
        # self.pluginsList.insertItem()
        enabled_plugins = plugins.get_enabled_plugins_list()

        for enabled_plugin in enabled_plugins:
            item = QListWidgetItem(enabled_plugin.name)
            self.pluginsList.addItem(item)

    def closeEvent(self, QCloseEvent):
        QApplication.closeAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GSMMainWindow()
    w.show()
    sys.exit(app.exec_())
