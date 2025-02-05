from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox)
from database import db

class BooksManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_books()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Форма для добавления книги
        form_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Год издания (число)")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр")
        self.add_button = QPushButton("Добавить книгу")
        self.add_button.clicked.connect(self.add_book)

        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(QLabel("Автор:"))
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(QLabel("Год:"))
        form_layout.addWidget(self.year_input)
        form_layout.addWidget(QLabel("Жанр:"))
        form_layout.addWidget(self.genre_input)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        # Таблица для отображения книг
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(5)
        self.books_table.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Год", "Жанр"])
        layout.addWidget(self.books_table)

        self.setLayout(layout)

    def load_books(self):
        """Загружает книги из базы данных и отображает их в таблице"""
        query = "SELECT * FROM books"
        cursor = db.execute(query)
        if cursor:
            rows = cursor.fetchall()
            self.books_table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, item in enumerate(row):
                    self.books_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить книги из базы данных")

    def add_book(self):
        """Добавляет новую книгу в базу после валидации вводимых данных"""
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()
        genre = self.genre_input.text().strip()

        if not title or not author:
            QMessageBox.warning(self, "Ошибка", "Название и автор обязательны для заполнения")
            return

        # Если введён год проверяем что это число
        if year:
            if not year.isdigit():
                QMessageBox.warning(self, "Ошибка", "Год должен быть числом")
                return
            year = int(year)
        else:
            year = None

        query = "INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)"
        try:
            db.execute(query, (title, author, year, genre))
            QMessageBox.information(self, "Успех", "Книга успешно добавлена")
            self.load_books()  # Обновляем таблицу
            # Очистка формы
            self.title_input.clear()
            self.author_input.clear()
            self.year_input.clear()
            self.genre_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления книги: {e}")
