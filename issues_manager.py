from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox, QComboBox)
from database import db
from datetime import datetime

class IssuesManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_issues()
        self.load_books_readers()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Форма для выдачи книги
        form_layout = QHBoxLayout()
        self.book_combo = QComboBox()
        self.reader_combo = QComboBox()
        self.issue_date_input = QLineEdit()
        self.issue_date_input.setPlaceholderText("Дата выдачи (ГГГГ-ММ-ДД)")
        self.return_date_input = QLineEdit()
        self.return_date_input.setPlaceholderText("Дата возврата (ГГГГ-ММ-ДД)")
        self.add_button = QPushButton("Выдать книгу")
        self.add_button.clicked.connect(self.issue_book)

        form_layout.addWidget(QLabel("Книга:"))
        form_layout.addWidget(self.book_combo)
        form_layout.addWidget(QLabel("Читатель:"))
        form_layout.addWidget(self.reader_combo)
        form_layout.addWidget(QLabel("Выдана:"))
        form_layout.addWidget(self.issue_date_input)
        form_layout.addWidget(QLabel("Возврат:"))
        form_layout.addWidget(self.return_date_input)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        # Таблица для отображения выданных книг
        self.issues_table = QTableWidget()
        self.issues_table.setColumnCount(5)
        self.issues_table.setHorizontalHeaderLabels(["ID", "Книга", "Читатель", "Дата выдачи", "Дата возврата"])
        layout.addWidget(self.issues_table)

        self.setLayout(layout)

    def load_books_readers(self):
        """Загружает книги и читателей для заполнения комбобоксов"""
        # Заполняем список книг
        self.book_combo.clear()
        query_books = "SELECT id, title FROM books"
        cursor_books = db.execute(query_books)
        if cursor_books:
            books = cursor_books.fetchall()
            for book in books:
                # Сохраним id книги как данные
                self.book_combo.addItem(f"{book[1]} (ID: {book[0]})", book[0])
        # Заполняем список читателей
        self.reader_combo.clear()
        query_readers = "SELECT id, full_name FROM readers"
        cursor_readers = db.execute(query_readers)
        if cursor_readers:
            readers = cursor_readers.fetchall()
            for reader in readers:
                self.reader_combo.addItem(f"{reader[1]} (ID: {reader[0]})", reader[0])

    def load_issues(self):
        """Загружает все операции выдачи книг и отображает их в таблице"""
        query = """
            SELECT issues.id, books.title, readers.full_name, issues.issue_date, issues.return_date
            FROM issues
            JOIN books ON issues.book_id = books.id
            JOIN readers ON issues.reader_id = readers.id
        """
        cursor = db.execute(query)
        if cursor:
            rows = cursor.fetchall()
            self.issues_table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, item in enumerate(row):
                    self.issues_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить операции выдачи книг")

    def issue_book(self):
        """Осуществляет операцию выдачи книги после проверки корректности дат"""
        book_id = self.book_combo.currentData()
        reader_id = self.reader_combo.currentData()
        issue_date = self.issue_date_input.text().strip()
        return_date = self.return_date_input.text().strip()

        # Проверка обязательного поля даты выдачи
        if not issue_date:
            QMessageBox.warning(self, "Ошибка", "Дата выдачи обязательна для заполнения")
            return

        # Валидация дат
        try:
            datetime.strptime(issue_date, "%Y-%m-%d")
            if return_date:
                datetime.strptime(return_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        query = "INSERT INTO issues (book_id, reader_id, issue_date, return_date) VALUES (?, ?, ?, ?)"
        try:
            db.execute(query, (book_id, reader_id, issue_date, return_date if return_date else None))
            QMessageBox.information(self, "Успех", "Операция выдачи выполнена")
            self.load_issues()
            # Очистка формы
            self.issue_date_input.clear()
            self.return_date_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка выдачи книги: {e}")
