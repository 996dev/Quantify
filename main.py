import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QStatusBar
from PySide6.QtGui import QIcon, QAction

from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
