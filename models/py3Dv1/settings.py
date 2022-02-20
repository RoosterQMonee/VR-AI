import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

vert = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setFixedSize(QSize(400, 300))

        self.button = QPushButton("Verticies")
        self.button.clicked.connect(self.change_vert)

        self.setCentralWidget(self.button)

    def change_vert(self):
        global vert
        if vert == True:
            vert = False

        else:
            vert = True

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()