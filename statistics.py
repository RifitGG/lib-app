from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLineEdit, QLabel,
                             QMessageBox, QTextEdit)
from database import db
from datetime import datetime

class StatisticsManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Форма для ввода периода отчёта
        form_layout = QHBoxLayout()
        self.start_date_input = QLineEdit()
        self.start_date_input.setPlaceholderText("Начало периода (ГГГГ-ММ-ДД)")
        self.end_date_input = QLineEdit()
        self.end_date_input.setPlaceholderText("Конец периода (ГГГГ-ММ-ДД)")
        self.report_button = QPushButton("Сформировать отчёт")
        self.report_button.clicked.connect(self.generate_report)
        form_layout.addWidget(QLabel("Период:"))
        form_layout.addWidget(self.start_date_input)
        form_layout.addWidget(self.end_date_input)
        form_layout.addWidget(self.report_button)

        layout.addLayout(form_layout)

        # Поле для отображения отчёта
        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        layout.addWidget(self.report_display)

        self.setLayout(layout)

    def generate_report(self):
        """Формирует отчёт по количеству выданных книг за указанный период"""
        start_date = self.start_date_input.text().strip()
        end_date = self.end_date_input.text().strip()

        # Проверка формата даты, вдруг наебали на время
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Даты должны быть в формате ГГГГ-ММ-ДД")
            return

        query = """
            SELECT COUNT(*) FROM issues
            WHERE issue_date BETWEEN ? AND ?
        """
        cursor = db.execute(query, (start_date, end_date))
        if cursor:
            count = cursor.fetchone()[0]
            report_text = f"Количество выданных книг с {start_date} по {end_date}: {count}"
            self.report_display.setText(report_text)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось сформировать отчёт")
