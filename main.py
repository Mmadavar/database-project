from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from loginFormWidget import loginFormWidget
from sys import argv


class MainWidget(QStackedWidget):
    def __init__(self, parent = ...):
        super().__init__(parent)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        

        self.stackedWidget = QStackedWidget()
        
        LoginFormWidget = loginFormWidget(self.stackedWidget)

        self.stackedWidget.setCurrentIndex(0)

        self.stackedWidget.addWidget(LoginFormWidget)

        self.setCentralWidget(self.stackedWidget)

# class App(QApplication):
#     def __init__(self, argv):
#         super().__init__(argv)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()