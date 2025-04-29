from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QFormLayout
import database

class loginFormWidget(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__(parent=parent)
        layout = QFormLayout(self)

        serverAccountLabel = QLabel(self)
        serverAccountLabel.setText('Database Account')
        self.serverAccountInput = QLineEdit(self)
        layout.addRow(serverAccountLabel, self.serverAccountInput)

        serverPasswordLabel = QLabel(self)
        serverPasswordLabel.setText('Database Password')
        self.serverPasswordInput = QLineEdit(self)
        self.serverPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(serverPasswordLabel, self.serverPasswordInput)

        userIdLabel = QLabel(self)
        userIdLabel.setText('User ID')
        self.userIdInput = QLineEdit(self)
        layout.addRow(userIdLabel, self.userIdInput)

        self.loginUserButton = QPushButton(self)
        self.loginUserButton.setText('Login As User')
        self.loginUserButton.clicked.connect(self.connect_to_database)

        self.loginAdminButton = QPushButton(self)
        self.loginAdminButton.setText('Login As Admin')
        layout.addRow(self.loginUserButton, self.loginAdminButton)

        self.setLayout(layout)
    
    def connect_to_database(self):

        self.parent().parent()

        account = self.serverAccountInput.text()
        password = self.serverPasswordInput.text()

        database.connect(account, password)