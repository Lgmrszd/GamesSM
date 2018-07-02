import plugins
import sys
from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTranslator, QLocale
from gui import GSMMainWindow


def main():
    plugins.load_plugins()
    
    app = QApplication(sys.argv)
    # qt_translator = QTranslator()
    # print(qt_translator.load("test"))
    # print(QLocale.system().name())
    # app.installTranslator(qt_translator)

    w = GSMMainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
