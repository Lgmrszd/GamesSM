import plugins
import sys
from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTranslator, QLocale
from gui import GSMMainWindow, EXIT_CODE_RESTART


def main():
    plugins.load_plugins()
    plugins.import_plugins()

    app = QApplication(sys.argv)
    # qt_translator = QTranslator()
    # print(qt_translator.load("test"))
    # print(QLocale.system().name())
    # app.installTranslator(qt_translator)

    w = GSMMainWindow()
    w.show()
    return app.exec_()


if __name__ == '__main__':
    current_exit_code = EXIT_CODE_RESTART
    while current_exit_code == EXIT_CODE_RESTART:
        current_exit_code = main()
    sys.exit(current_exit_code)
