from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from loginFormWidget import loginFormWidget
from sys import argv
import oracledb

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        

        self.stackedWidget = QStackedWidget()
        
        LoginFormWidget = loginFormWidget(self.stackedWidget)

        self.stackedWidget.setCurrentIndex(0)

        self.stackedWidget.addWidget(LoginFormWidget)

        self.setCentralWidget(self.stackedWidget)

        self.database = None

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()