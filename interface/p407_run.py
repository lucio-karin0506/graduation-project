import sys
from PySide2.QtWidgets import *
from p407_gui.interface.main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())