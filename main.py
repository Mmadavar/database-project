from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication, QTabWidget
from loginDialog import loginDialog
from customerListWidget import customerListWidget
from autoLoanListWidget import autoLoanListWidget
from personalLoanListWidget import personalLoanListWidget
from studentLoanListWidget import studentLoanListWidget
from mortgageListWidget import mortgageListWidget
from sys import argv
import database

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        loginPopup = loginDialog()
        loginPopup.exec()

        # if popup closed without logging in
        if database.connection is None:
            exit()

        self.widget = QTabWidget()

        # only show customer list when logged in as admin
        if not database.userid:
            self.widget.addTab(customerListWidget(), 'Customer List')

        self.widget.addTab(autoLoanListWidget(), 'Auto Loans')
        self.widget.addTab(personalLoanListWidget(), 'Personal Loans')
        self.widget.addTab(studentLoanListWidget(), 'Student Loans')
        self.widget.addTab(mortgageListWidget(), 'Mortgage List')

        self.setCentralWidget(self.widget)

if __name__ == '__main__':
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()