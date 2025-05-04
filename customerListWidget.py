from PyQt6.QtWidgets import QScrollArea, QListWidget, QListWidgetItem
import database
from enterInfoWidget import infoPopup

class customerListWidget(QScrollArea):
    def __init__(self, parent = None):
        super(customerListWidget, self).__init__(parent)        
        self.listWidget = QListWidget()
        self.listWidget.itemDoubleClicked.connect(self.handleDoubleClick)
        
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