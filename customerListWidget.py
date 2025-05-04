from PyQt6.QtWidgets import QScrollArea, QListWidget, QListWidgetItem, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
import database
from enterInfoWidget import infoPopup

class customerListWidget(QWidget):
    def __init__(self, parent = None):
        super(customerListWidget, self).__init__(parent)
        layout = QVBoxLayout()
        mainwidget = customerScrollArea()
        layout.addWidget(mainwidget)

        deleteButton = QPushButton(self)
        deleteButton.setText('Delete Selected')
        deleteButton.clicked.connect(mainwidget.deleteCustomer)

        addButton = QPushButton(self)
        addButton.setText('Add New User')
        addButton.clicked.connect(mainwidget.addCustomer)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(deleteButton)
        bottomLayout.addWidget(addButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

class customerScrollArea(QScrollArea):
    def __init__(self, parent = None):
        super(customerScrollArea, self).__init__(parent)        
        self.listWidget = QListWidget(self)
        self.listWidget.itemDoubleClicked.connect(self.handleDoubleClick)
        self.listWidget.itemClicked.connect(self.handleSingleClick)
        
        self.setWidget(self.listWidget)

        self.editing = None

        self.clients = None
        self.refresh()
    
    def refresh(self):
        self.clients = database.getClients()
        self.listWidget.clear()
        for i in self.clients:
            self.listWidget.addItem(
                f'id:{i[0]}, name: {i[1]} {i[2]}, income: {i[3]}'
            )
    
    def handleSingleClick(self, item):
        text = item.text()
        endidx = text.index(',')
        startidx = text.index(':')+1
        client_id = int(text[startidx:endidx])
        self.editing = client_id

    def handleDoubleClick(self, item: QListWidgetItem):
        text = item.text()
        endidx = text.index(',')
        startidx = text.index(':')+1
        client_id = int(text[startidx:endidx])
        target = None
        for i in self.clients:
            if i[0] == client_id:
                target = i
                break
        else:
            return
        
        data = {
            'First Name': target[1],
            'Last Name': target[2],
            'Income': target[3]
        }
        self.editing = client_id
        popup = infoPopup(self, data, self.saveData)
        popup.open()
            

    def saveData(self, data):
        database.updateClient(self.editing, data['First Name'], data['Last Name'], data['Income'])
        self.editing = None
        self.refresh()

    def newData(self, data):
        database.addClient(data['First Name'], data['Last Name'], data['Income'])
        self.refresh()
    
    def deleteCustomer(self):
        database.deleteClient(self.editing)
        self.editing = None
        self.refresh()

    def addCustomer(self):
        data = [
            'First Name',
            'Last Name',
            'Income'
        ]
        popup = infoPopup(self, data, self.newData)
        popup.open()