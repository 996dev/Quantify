from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QLineEdit, QVBoxLayout


class Config(QtWidgets.QLayout):
    def __init__(self):
        super().__init__()
        # self.line_edit_account = QLineEdit()
        line_edit_account = QLineEdit( placeholderText='请输入期货账户账号', clearButtonEnabled=True)
        line_edit_account.placeholderText()
        line_edit_account_password = QLineEdit(self, placeholderText='请输入期货账户账号密码', clearButtonEnabled=True)

        layout = QVBoxLayout()
        layout.addWidget(line_edit_account)
        layout.addWidget(line_edit_account_password)
        # self.setLayout(layout)


