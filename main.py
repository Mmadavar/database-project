from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication, QTabWidget
from loginDialog import loginDialog
from customerListWidget import customerListWidget
from sys import argv
import oracledb

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        loginPopup = loginDialog()
        loginPopup.exec()

        self.widget = QTabWidget()

        self.widget.addTab(customerListWidget(), 'customer list')

        self.setCentralWidget(self.widget)

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()