import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QStatusBar
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Editor')
        self.setGeometry(100, 100, 500, 300)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.show()


