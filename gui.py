import sys
import PyQt5.QtWidgets
from PyQt5.QtGui import QColor, QBrush
from PyQt5 import uic
from PyQt5.QtCore import QObject, QCoreApplication
import plugins

EXIT_CODE_RESTART = -123


class PluginSettingsRow(QObject):
    columns = ["Name", "Enabled"]

    class PluginWidgetItem(PyQt5.QtWidgets.QTableWidgetItem):
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

    def insert_into_table(self, table: PyQt5.QtWidgets.QTableWidget):
        r = table.rowCount()
        table.insertRow(r)
        table.setItem(r, 0, self.name_widg)
        table.setItem(r, 1, self.enab_widg)


class SettingsWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/Settings.ui", self)

        self.current_plugin = None  # type: plugins.Plugin

        self.pluginLabel: PyQt5.QtWidgets.QLabel = self.findChild(PyQt5.QtWidgets.QLabel, "pluginLabel")

        self.toggleButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "toggleButton")
        self.toggleButton.setDisabled(True)
        self.toggleButton.clicked.connect(self.on_toggle_button_clicked)

        self.restartButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "restartButton")
        self.restartButton.clicked.connect(self.on_restart_button_clicked)

        self.pluginsTable: PyQt5.QtWidgets.QTableWidget = self.findChild(PyQt5.QtWidgets.QTableWidget, "pluginsTable")

        # self.pluginsTable.setFixedWidth(300)
        self.pluginsTable.setColumnCount(len(PluginSettingsRow.columns))
        # self.pluginsTable.setColumnWidth(1, 20)
        self.pluginsTable.setHorizontalHeaderLabels(PluginSettingsRow.columns)
        self.pluginsTable.itemClicked.connect(self.on_item_selected)
        self.load_plugins()

    def update_label(self):
        text = ("<b>Name</b>: {}<br>"
                "<b>Description</b>: {}")
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

    def on_restart_button_clicked(self, _):
        qapp = QCoreApplication.instance()
        qapp.exit(EXIT_CODE_RESTART)

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


class GSMMainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/MainWindow.ui", self)

        self.current_plugin: plugins.Plugin = None

        self.settingsWindow = SettingsWindow()

        self.copyButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "copyButton")
        self.restoreButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "restoreButton")
        self.replaceButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "replaceButton")

        self.pluginSettingsButton: PyQt5.QtWidgets.QPushButton = self.findChild(PyQt5.QtWidgets.QPushButton, "pluginSettingsButton")
        self.pluginSettingsButton.clicked.connect(self.on_pluigin_settings_button_clicked)

        self.pluginsList: PyQt5.QtWidgets.QListWidget = self.findChild(PyQt5.QtWidgets.QListWidget, "pluginsList")
        self.pluginsList.itemClicked.connect(self.on_plugin_select)

        self.savedSlots: PyQt5.QtWidgets.QTableWidget = self.findChild(PyQt5.QtWidgets.QTableWidget, "savedSlots")
        self.gameSlots: PyQt5.QtWidgets.QListWidget = self.findChild(PyQt5.QtWidgets.QListWidget, "gameSlots")

        self.pluginLabel: PyQt5.QtWidgets.QLabel = self.findChild(PyQt5.QtWidgets.QLabel, "pluginLabel")

        self.actionSettings: PyQt5.QtWidgets.QAction = self.findChild(PyQt5.QtWidgets.QAction, "actionSettings")
        self.actionSettings.triggered.connect(self.settingsWindow.show)

        self.load_plugins()

    def on_pluigin_settings_button_clicked(self):
        show_about_dialog(self)
        # self.settingsWindow.show()
        tabWidget: PyQt5.QtWidgets.QTabWidget = self.settingsWindow.findChild(PyQt5.QtWidgets.QTabWidget, "settingsTabWidget")
        pluginsTab = self.settingsWindow.findChild(PyQt5.QtWidgets.QWidget, "pluginsTab")
        if tabWidget and pluginsTab:
            tabWidget.setCurrentWidget(pluginsTab)

    def update_label(self):
        text = ("<b>Name</b>: {}<br>"
                "<b>Description</b>: {}")
        text = text.format(self.current_plugin.name, self.current_plugin.description)
        self.pluginLabel.setText(text)
        print(self.current_plugin.get_module().MAX_SLOTS_NUMBER)

    def on_plugin_select(self, item):
        self.current_plugin = plugins.Plugin.get_by_id(item.text())
        self.update_label()

    def load_plugins(self):
        # self.pluginsList.insertItem()
        enabled_plugins = plugins.get_enabled_plugins_list()

        for enabled_plugin in enabled_plugins:
            item = PyQt5.QtWidgets.QListWidgetItem(enabled_plugin.name)
            self.pluginsList.addItem(item)

    def closeEvent(self, QCloseEvent):
        PyQt5.QtWidgets.QApplication.closeAllWindows()


def show_about_dialog(parent):
    PyQt5.QtWidgets.QMessageBox.about(parent, "A", "B")
