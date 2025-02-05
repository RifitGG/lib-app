from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox)
from database import db
from datetime import datetime

class ReadersManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_readers()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Форма для добавления читателя
        form_layout = QHBoxLayout()
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("ФИО")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Адрес")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setPlaceholderText("Дата рождения (ГГГГ-ММ-ДД)")
        self.add_button = QPushButton("Добавить читателя")
        self.add_button.clicked.connect(self.add_reader)

        form_layout.addWidget(QLabel("ФИО:"))
        form_layout.addWidget(self.full_name_input)
        form_layout.addWidget(QLabel("Адрес:"))
        form_layout.addWidget(self.address_input)
        form_layout.addWidget(QLabel("Телефон:"))
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(QLabel("Дата рождения:"))
        form_layout.addWidget(self.birth_date_input)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        # Таблица для отображения читателей
        self.readers_table = QTableWidget()
        self.readers_table.setColumnCount(5)
        self.readers_table.setHorizontalHeaderLabels(["ID", "ФИО", "Адрес", "Телефон", "Дата рождения"])
        layout.addWidget(self.readers_table)

        self.setLayout(layout)

    def load_readers(self):
        """Загружает читателей из базы данных и отображает их в таблице"""
        query = "SELECT * FROM readers"
        cursor = db.execute(query)
        if cursor:
            rows = cursor.fetchall()
            self.readers_table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, item in enumerate(row):
                    self.readers_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить читателей из базы данных")

    def add_reader(self):
        """Добавляет нового читателя после валидации введённых данных"""
        full_name = self.full_name_input.text().strip()
        address = self.address_input.text().strip()
        phone = self.phone_input.text().strip()
        birth_date = self.birth_date_input.text().strip()

        if not full_name:
            QMessageBox.warning(self, "Ошибка", "ФИО обязательно для заполнения")
            return

        # Валидация формата даты (если введена)
        if birth_date:
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Дата рождения должна быть в формате ГГГГ-ММ-ДД")
                return

        query = "INSERT INTO readers (full_name, address, phone, birth_date) VALUES (?, ?, ?, ?)"
        try:
            db.execute(query, (full_name, address, phone, birth_date))
            QMessageBox.information(self, "Успех", "Читатель успешно добавлен")
            self.load_readers()  # Обновляем таблицу
            # Очистка формы
            self.full_name_input.clear()
            self.address_input.clear()
            self.phone_input.clear()
            self.birth_date_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления читателя: {e}")
