from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QWidget
from books_manager import BooksManager
from readers_manager import ReadersManager
from issues_manager import IssuesManager
from statistics import StatisticsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление библиотечным фондом")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        # Создание меню
        menubar = self.menuBar()

        books_menu = menubar.addMenu("Управление книгами")
        readers_menu = menubar.addMenu("Управление читателями")
        stats_menu = menubar.addMenu("Статистика")

        # Действия для меню
        action_books = QAction("Книги", self)
        action_books.triggered.connect(self.show_books_manager)
        books_menu.addAction(action_books)

        action_readers = QAction("Читатели", self)
        action_readers.triggered.connect(self.show_readers_manager)
        readers_menu.addAction(action_readers)

        action_issues = QAction("Выдача книг", self)
        action_issues.triggered.connect(self.show_issues_manager)
        books_menu.addAction(action_issues)

        action_stats = QAction("Отчёты", self)
        action_stats.triggered.connect(self.show_statistics)
        stats_menu.addAction(action_stats)

        # Центральное виджет-окно с менеджером компоновки для адаптивности
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def clear_layout(self):
        """Очищает центральный layout перед добавлением нового виджета"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_books_manager(self):
        self.clear_layout()
        books_manager = BooksManager()
        self.layout.addWidget(books_manager)

    def show_readers_manager(self):
        self.clear_layout()
        readers_manager = ReadersManager()
        self.layout.addWidget(readers_manager)

    def show_issues_manager(self):
        self.clear_layout()
        issues_manager = IssuesManager()
        self.layout.addWidget(issues_manager)

    def show_statistics(self):
        self.clear_layout()
        stats_manager = StatisticsManager()
        self.layout.addWidget(stats_manager)
