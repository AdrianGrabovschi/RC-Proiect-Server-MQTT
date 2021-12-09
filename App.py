import PyQt5.QtWidgets
#import PyQt5


class App(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "MQTT Server"
        self.width = 480
        self.height = 800

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.center()

        self.button = PyQt5.QtWidgets.QPushButton("Send Package", self)
        self.button.move(50, 200)
        self.button.setCheckable(True)
        #self.button.clicked.connect(self.button_clicked_SendPackage)

        self.show()