from PyQt6.QtWidgets import QFormLayout, QLabel, QPushButton, QDialog

class infoPopup(QDialog):

    def __init__(self, parent, data: dict[str, str], closeAction):
        super().__init__(parent)
        
        layout = QFormLayout()

        for k, v in data.items():
            title = QLabel(self)
            title.setText(str(k))

            value = QLabel(self)
            value.setText(str(v))

            layout.addRow(title, value)
        
        closeButton = QPushButton()
        closeButton.clicked.connect(closeAction)
        layout.addWidget(closeButton)


