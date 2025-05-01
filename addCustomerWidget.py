from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QFormLayout
import database

class addCustomerWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QFormLayout(self)

        firstnameLabel = QLabel(self)
        firstnameLabel.setText('First Name')
        self.firstnameInput = QLineEdit(self)
        layout.addRow(firstnameLabel, self.firstnameInput)

        lastnameLabel = QLabel(self)
        lastnameLabel.setText('Last Name')
        self.lastnameInput = QLineEdit(self)
        layout.addRow(lastnameLabel, self.lastnameInput)

        incomeLabel = QLabel(self)
        incomeLabel.setText('Income')
        self.incomeInput = QLineEdit(self)
        layout.addRow(incomeLabel, self.incomeInput)

        addCustomerButton = QPushButton(self)
        addCustomerButton.clicked.connect(self.addCustomer)
    
    def addCustomer(self):
        first = self.firstnameInput.text()
        last = self.lastnameInput.text()
        income = self.incomeInput.text()
        database.addClient(first, last, income)

