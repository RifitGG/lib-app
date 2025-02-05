import sys
from PyQt5.QtWidgets import QApplication
from auth import AuthDialog
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Окно авторизации
    auth_dialog = AuthDialog()
    if auth_dialog.exec_() == AuthDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
