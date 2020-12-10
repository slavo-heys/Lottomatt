from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5 import QtGui

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Lottomat v 1.0"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 600

        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("lotto.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()


App = QApplication(sys.argv)
Window = Window()
sys.exit(App.exec())
