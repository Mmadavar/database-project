from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import database
from enterInfoDialog import enterInfoDialog
from showInfoDialog import showInfoDialog
from searchBarWidget import searchBarWidget
import datetime

class studentLoanListWidget(QWidget):
    def __init__(self, parent = None):
        super(studentLoanListWidget, self).__init__(parent)
        layout = QVBoxLayout()
        mainwidget = studentLoanList()
        layout.addWidget(mainwidget)

        if database.userid is None:
            deleteButton = QPushButton(self)
            deleteButton.setText('Delete Selected')
            deleteButton.clicked.connect(mainwidget.deleteLoan)

            addButton = QPushButton(self)
            addButton.setText('Add New Student Loan')
            addButton.clicked.connect(mainwidget.addLoan)

            bottomLayout = QHBoxLayout()
            bottomLayout.addWidget(deleteButton)
            bottomLayout.addWidget(addButton)
            layout.addLayout(bottomLayout)

        layout.addWidget(searchBarWidget(self, 'Search Loan ID', lambda x: mainwidget.openDialog(int(x))))

        self.setLayout(layout)

class studentLoanList(QListWidget):
    def __init__(self, parent = None):
        super(studentLoanList, self).__init__(parent)        
        self.itemDoubleClicked.connect(self.handleDoubleClick)
        self.itemClicked.connect(self.handleSingleClick)
        
        self.editing = None
        self.refresh()
    
    def refresh(self):
        self.data = database.getStudentLoans()
        self.clear()
        for i in self.data:
            self.addItem(
                f'id: {i[0]}, client: {i[1]}, Monthly Payment: {i[2]}'
            )
    
    def handleSingleClick(self, item):
        text = item.text()
        endidx = text.index(',')
        startidx = text.index(':')+2
        self.editing = int(text[startidx:endidx])

    def handleDoubleClick(self, item: QListWidgetItem):
        self.handleSingleClick(item)
        self.openDialog()

    def openDialog(self, loanId = None):
        if loanId is not None:
            self.editing = loanId
            self.clearSelection()

        target = None
        for i in self.data:
            if i[1] == self.editing:
                target = i
                break
        else:
            return

        data = {
            'Client ID': target[0],
            'Loan Term': target[2],
            'Disimbursement Date': target[3],
            'Repayment Start Date': target[4],
            'Repayment End Date': target[5],
            'Monthly Payment': target[6],
            'Grace Period': target[7],
            'Loan Type': target[8]
        }

        if database.userid is None:
            popup = enterInfoDialog(self, data, self.saveData)
        else:
            popup = showInfoDialog(self, data)
        
        popup.open()

    def saveData(self, data:dict):
        database.updateStudentLoan(
            int(data['Client ID']),
            data['Loan Term'],
            datetime.datetime.strptime(data['Disimbursement Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['Repayment Start Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['Repayment End Date'], '%Y-%m-%d %H:%M:%S'),
            float(data['Monthly Payment']),
            int(data['Grace Period']),
            data['Loan Type'],
            self.editing
        )

        self.editing = None
        self.refresh()

    def newData(self, data):
        database.addStudentLoan(
            int(data['Client ID']),
            data['Loan Term'],
            datetime.datetime.strptime(data['Disimbursement Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['Repayment Start Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['Repayment End Date'], '%Y-%m-%d %H:%M:%S'),
            float(data['Monthly Payment']),
            int(data['Grace Period']),
            data['Loan Type'],
        )
        self.refresh()
    
    def deleteLoan(self):
        database.deleteStudentLoan(self.editing)
        self.editing = None
        self.refresh()

    def addLoan(self):
        data = [
            'Client ID',
            'Loan Term',
            'Disimbursement Date',
            'Repayment Start Date',
            'Repayment End Date',
            'Monthly Payment',
            'Grace Period',
            'Loan Type'
        ]
        popup = enterInfoDialog(self, data, self.newData)
        popup.open()