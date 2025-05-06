from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import database
from enterInfoDialog import enterInfoDialog
from showInfoDialog import showInfoDialog
from searchBarWidget import searchBarWidget
import datetime

class mortgageListWidget(QWidget):
    def __init__(self, parent = None):
        super(mortgageListWidget, self).__init__(parent)
        layout = QVBoxLayout()
        mainwidget = mortgageList()
        layout.addWidget(mainwidget)

        deleteButton = QPushButton(self)
        deleteButton.setText('Delete Selected')
        deleteButton.clicked.connect(mainwidget.deleteLoan)

        addButton = QPushButton(self)
        addButton.setText('Add New Mortgage')
        addButton.clicked.connect(mainwidget.addLoan)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(deleteButton)
        bottomLayout.addWidget(addButton)
        layout.addLayout(bottomLayout)

        layout.addWidget(searchBarWidget(self, 'Search Address', lambda x: mainwidget.openDialog(x)))

        self.setLayout(layout)

class mortgageList(QListWidget):
    def __init__(self, parent = None):
        super(mortgageList, self).__init__(parent)        
        self.itemDoubleClicked.connect(self.handleDoubleClick)
        self.itemClicked.connect(self.handleSingleClick)
        
        self.editing = None
        self.refresh()
    
    def refresh(self):
        self.data = database.getMortgages()
        self.clear()
        for i in self.data:
            self.addItem(
                f'address: {i[1]}, client: {i[0]}'
            )
        self.clearSelection()
    
    def handleSingleClick(self, item):
        text = item.text()
        endidx = text.index(',')
        startidx = text.index(':')+2
        self.editing = text[startidx:endidx]

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
            'Loan Amount': target[5],
            'Interest Rate': target[6],
            'Start Date': target[8],
            'End Date': target[10],
            'Number of Payments': target[9],
            'Amount Paid': target[7],
            'House Area': target[2],
            'Bedrooms': target[3],
            'House Price': target[4]
        }

        if database.userid is not None:
            popup = enterInfoDialog(self, data, self.saveData)
        else:
            popup = showInfoDialog(self, data)
        popup.open()

    def saveData(self, data:dict):
        
        database.updateMortgage(
            int(data['Client ID']),
            self.editing,
            float(data['House Area']),
            int(data['Bedrooms']),
            float(data['House Price']),
            float(data['Loan Amount']),
            float(data['Interest Rate']),
            float(data['Amount Paid']),
            datetime.datetime.strptime(data['Start Date'], '%Y-%m-%d %H:%M:%S'),
            int(data['Number of Payments']),
            datetime.datetime.strptime(data['End Date'], '%Y-%m-%d %H:%M:%S')
        )

        self.editing = None
        self.refresh()

    def newData(self, data):
        database.addMortgage(
            int(data['Client ID']),
            data['House Address'].replace(',', ''),
            float(data['House Area']),
            int(data['Bedrooms']),
            float(data['House Price']),
            float(data['Loan Amount']),
            float(data['Interest Rate']),
            float(data['Amount Paid']),
            datetime.datetime.strptime(data['Start Date'], '%Y-%m-%d %H:%M:%S'),
            int(data['Number of Payments']),
            datetime.datetime.strptime(data['End Date'], '%Y-%m-%d %H:%M:%S')
        )
        self.refresh()
    
    def deleteLoan(self):
        database.deleteMortgage(self.editing)
        self.editing = None
        self.refresh()

    def addLoan(self):
        data = [
            'Client ID',
            'Loan Amount',
            'Interest Rate',
            'Start Date',
            'End Date',
            'Number of Payments',
            'Amount Paid',
            'House Address',
            'House Area',
            'Bedrooms',
            'House Price'
        ]
        popup = enterInfoDialog(self, data, self.newData)
        popup.open()