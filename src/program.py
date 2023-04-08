import sys
from mainUI import Ui_optionAtillaWindow
from optionAtilla import Atilla
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_optionAtillaWindow()
    ui.setupUi(window)
    atilla = Atilla(app, "config\\config.ini")
    atilla.setWindow(ui, window)
    window.show()
    sys.exit(app.exec())