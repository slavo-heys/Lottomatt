from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore

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

        
        self.UiComponents()
        self.show()

    def UiComponents(self):
        button = QPushButton("  Dodaj wyniki losowania", self)
        #button.move(10,20)
        button.setGeometry(QRect(10,10,160,40))
        button.setIcon(QtGui.QIcon("lotto_1.png"))
        button.setIconSize(QtCore.QSize(50,50))
        button.setToolTip("<h3>Dodaj wyniki nowego losowania</h3>")

        button_1 = QPushButton("       Dodaj moje liczby", self)
        button_1.setGeometry(QRect(10,55,160,40))
        button_1.setIcon(QtGui.QIcon("lottery.png"))
        button_1.setIconSize(QtCore.QSize(50,50))
        button_1.setToolTip("<h3>Dodaj swój zestaw wytypowanych liczb</h3>")

        button_2 = QPushButton("  Sprawdź powtórzenia", self)
        button_2.setGeometry(QRect(10,100,160,40))
        button_2.setIcon(QtGui.QIcon("lotto_2.png"))
        button_2.setIconSize(QtCore.QSize(40,40))
        button_2.setToolTip("<h3>Sprawdź powtórzenia liczb we wszystkich losowaniach.</h3>")






App = QApplication(sys.argv)
Window = Window()
sys.exit(App.exec())
