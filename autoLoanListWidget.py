from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import database
from enterInfoDialog import enterInfoDialog
from showInfoDialog import showInfoDialog
from searchBarWidget import searchBarWidget
import datetime

class autoLoanListWidget(QWidget):
    def __init__(self, parent = None):
        super(autoLoanListWidget, self).__init__(parent)
        layout = QVBoxLayout()
        mainwidget = autoLoanList()
        layout.addWidget(mainwidget)

        if database.userid is None:
            deleteButton = QPushButton(self)
            deleteButton.setText('Delete Selected')
            deleteButton.clicked.connect(mainwidget.deleteLoan)

            addButton = QPushButton(self)
            addButton.setText('Add New Auto Loan')
            addButton.clicked.connect(mainwidget.addLoan)

            bottomLayout = QHBoxLayout()
            bottomLayout.addWidget(deleteButton)
            bottomLayout.addWidget(addButton)
            layout.addLayout(bottomLayout)

        layout.addWidget(searchBarWidget(self, 'Search VIN', lambda x: mainwidget.openDialog(x)))

        self.setLayout(layout)

class autoLoanList(QListWidget):
    def __init__(self, parent = None):
        super(autoLoanList, self).__init__(parent)        
        self.itemDoubleClicked.connect(self.handleDoubleClick)
        self.itemClicked.connect(self.handleSingleClick)
        
        self.editing = None
        self.refresh()
    
    def refresh(self):
        self.data = database.getAutoLoans()
        self.clear()
        for i in self.data:
            self.addItem(
                f'vin: {i[0]}, client: {i[1]}, car: {i[2]} {i[3]} {i[4]}'
            )
        self.clearSelection()

    
    def handleSingleClick(self, item):
        self.editing = self.data[self.selectedIndexes()[0].row()][0]

    def handleDoubleClick(self, item: QListWidgetItem):
        self.handleSingleClick(item)
        self.openDialog()

    def openDialog(self, loanId = None):
        if loanId is not None:
            self.editing = loanId
            self.clearSelection()

        target = database.getAutoLoan(self.editing)
        if target is None:
            return

        data = {
            'Client ID': target[0],
            'Loan Amount': target[2],
            'Interest Rate': target[3],
            'Start Date': target[4],
            'End Date': target[5],
            'Number of Payments': target[6],
            'Amount Paid': target[9],
            'Year': target[10],
            'Make': target[7],
            'Model': target[8]
        }

        if database.userid is None:
            popup = enterInfoDialog(self, data, self.saveData)
        else:
            popup = showInfoDialog(self, data)
        popup.open()

    def saveData(self, data:dict):
        vals = list(data.values())

        database.updateAutoLoan(
            int(data['Client ID']),
            self.editing,
            float(data['Loan Amount']),
            float(data['Interest Rate']),
            datetime.datetime.strptime(data['Start Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['End Date'], '%Y-%m-%d %H:%M:%S'),
            int(data['Number of Payments']),
            data['Make'],
            data['Model'],
            float(data['Amount Paid']),
            int(data['Year'])
        )

        self.editing = None
        self.refresh()

    def newData(self, data):
        database.addAutoLoan(
            int(data['Client ID']),
            data['VIN'].replace(',',''),
            float(data['Loan Amount']),
            float(data['Interest Rate']),
            datetime.datetime.strptime(data['Start Date'], '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(data['End Date'], '%Y-%m-%d %H:%M:%S'),
            int(data['Number of Payments']),
            data['Make'],
            data['Model'],
            float(data['Amount Paid']),
            int(data['Year'])
        )
        self.refresh()
    
    def deleteLoan(self):
        database.deleteAutoLoan(self.editing)
        self.editing = None
        self.refresh()

    def addLoan(self):
        data = [
            'VIN',
            'Client ID',
            'Loan Amount',
            'Interest Rate',
            'Start Date',
            'End Date',
            'Number of Payments',
            'Amount Paid',
            'Year',
            'Make',
            'Model'
        ]
        popup = enterInfoDialog(self, data, self.newData)
        popup.open()