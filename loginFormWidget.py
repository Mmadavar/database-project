from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget, QFormLayout

class loginFormWidget(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__(parent=parent)
        layout = QFormLayout(self)

        serverAddressLabel = QLabel(self)
        serverAddressLabel.setText('Database Server')
        serverAddressInput = QLineEdit(self)
        layout.addRow(serverAddressLabel, serverAddressInput)

        serverAccountLabel = QLabel(self)
        serverAccountLabel.setText('Database Account')
        serverAccountInput = QLineEdit(self)
        layout.addRow(serverAccountLabel, serverAccountInput)

        serverPasswordLabel = QLabel(self)
        serverPasswordLabel.setText('Database Password')
        serverPasswordInput = QLineEdit(self)
        serverPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(serverPasswordLabel, serverPasswordInput)

        userIdLabel = QLabel(self)
        userIdLabel.setText('User ID')
        userIdInput = QLineEdit(self)
        layout.addRow(userIdLabel, userIdInput)

        loginUserButton = QPushButton(self)
        loginUserButton.setText('Login As User')

        loginAdminButton = QPushButton(self)
        loginAdminButton.setText('Login As Admin')
        layout.addRow(loginUserButton, loginAdminButton)

        self.setLayout(layout)


        