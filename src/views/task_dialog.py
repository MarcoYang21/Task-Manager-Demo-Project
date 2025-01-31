from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDialogButtonBox,
    QDateTimeEdit,
    QFormLayout,
)
from PySide6.QtCore import Qt
from datetime import datetime
from models.task import TaskStatus  # 改為絕對導入


class TaskDialog(QDialog):
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setupUi()

        if task_data:
            self.setWindowTitle("編輯任務")
            self.loadTaskData()
        else:
            self.setWindowTitle("新增任務")

    def setupUi(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.titleEdit = QLineEdit()
        self.descEdit = QTextEdit()
        self.statusCombo = QComboBox()
        self.dueDateEdit = QDateTimeEdit()

        # 設置狀態選項
        for status in TaskStatus:
            self.statusCombo.addItem(status.value, status)

        # 設置日期時間編輯器
        self.dueDateEdit.setCalendarPopup(True)
        self.dueDateEdit.setDateTime(datetime.now())

        form.addRow("標題:", self.titleEdit)
        form.addRow("描述:", self.descEdit)
        form.addRow("狀態:", self.statusCombo)
        form.addRow("截止日期:", self.dueDateEdit)

        # 按鈕
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(buttons)

    def loadTaskData(self):
        self.titleEdit.setText(self.task_data["title"])
        self.descEdit.setText(self.task_data["description"])

        # 設置狀態
        index = self.statusCombo.findText(self.task_data["status"])
        if index >= 0:
            self.statusCombo.setCurrentIndex(index)

        # 設置日期
        due_date = datetime.fromisoformat(self.task_data["due_date"])
        self.dueDateEdit.setDateTime(due_date)

    def getTaskData(self):
        return {
            "title": self.titleEdit.text(),
            "description": self.descEdit.toPlainText(),
            "status": TaskStatus(self.statusCombo.currentData()).value,
            "due_date": self.dueDateEdit.dateTime().toPython(),
        }
