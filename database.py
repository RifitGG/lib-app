# database.py
import sqlite3

DB_NAME = "library.db"

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Устанавливаем соединение с базой данных."""
        try:
            self.connection = sqlite3.connect(DB_NAME)
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def create_tables(self):
        """Создаём таблицы, если они ещё не созданы."""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    birth_date TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    reader_id INTEGER NOT NULL,
                    issue_date TEXT NOT NULL,
                    return_date TEXT,
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (reader_id) REFERENCES readers(id)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка создания таблиц: {e}")

    def execute(self, query, parameters=None):
        """
        Выполняет запрос к базе данных.
        Возвращает курсор, либо None в случае ошибки.
        """
        parameters = parameters or ()
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def close(self):
        """Закрываем соединение с базой данных."""
        if self.connection:
            self.connection.close()

db = Database()
