import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QStatusBar, QLineEdit, QVBoxLayout, \
    QHBoxLayout
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Editor')
        self.setGeometry(500, 500, 1080, 720)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.layout = QVBoxLayout(self)

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText('请输入期货账户')
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setMinimumWidth(200)

        self.search_box1 = QLineEdit(self)
        self.search_box1.setPlaceholderText("请输入期货账户密码")
        self.search_box1.setClearButtonEnabled(True)
        self.search_box1.setMinimumWidth(200)

        # self.layout.setSpacing(20)
        # self.layout.addWidget(self.search_box)
        # self.layout.addWidget(self.search_box1)
        self.setLayout(self.layout)

        self.show()
