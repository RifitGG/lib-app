from PyQt5.QtWidgets import (QDialog, QLineEdit, QLabel,
                             QPushButton, QVBoxLayout, QMessageBox)

class AuthDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setup_ui()

    def setup_ui(self):
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.check_credentials)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def check_credentials(self):
        """Проверка введённых данных"""
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        if login == "admin" and password == "admin": #Это можешь поменять, если не понравится
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
