from PyQt6.QtWidgets import QFormLayout, QLabel, QPushButton, QDialog, QLineEdit

class infoPopup(QDialog):

    def __init__(self, parent, data: dict[str, str] | list[str], saveAction):

        super().__init__(parent)
        
        layout = QFormLayout()

        if isinstance(data, list):
            data = {i: '' for i in data}

        self.labels: list[QLabel] = []
        self.values: list[QLineEdit] = []

        for k, v in data.items():
            title = QLabel(self)
            title.setText(str(k))
            self.labels.append(title)

            value = QLineEdit(self)
            value.setText(str(v))
            self.values.append(value)

            layout.addRow(title, value)
        
        saveButton = QPushButton()
        saveButton.setText('Save')
        saveButton.clicked.connect(self.returnSave)

        cancelButton = QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(self.close)
        layout.addRow(saveButton, cancelButton)
        self.setLayout(layout)
        self.saveAction = saveAction


    def getData(self):
        return { self.labels[i].text(): self.values[i].text()  for i in range(len(self.labels))}
    
    def returnSave(self):
        self.saveAction(self.getData())
        self.close()
