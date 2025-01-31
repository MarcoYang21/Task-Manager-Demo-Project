from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDialogButtonBox,
    QDateTimeEdit
)
from PySide6.QtCore import Qt
from datetime import datetime
from models.task import TaskStatus

class TaskDialog(QDialog):
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setupUi()
        if task_data:
            self.loadTaskData()

    def setupUi(self):
        self.setWindowTitle("任務")
        self.setMinimumWidth(400)
        
        layout = QFormLayout(self)
        # 標題
        self.titleEdit = QLineEdit(self)
        self.titleEdit.setPlaceholderText("請輸入任務標題")
        layout.addRow("標題:", self.titleEdit)
        # 描述
        self.descriptionEdit = QTextEdit(self)
        self.descriptionEdit.setPlaceholderText("請輸入任務描述")
        layout.addRow("描述:", self.descriptionEdit)
        # 狀態
        self.statusCombo = QComboBox(self)
        for status in TaskStatus:
            self.statusCombo.addItem(status.value, status)
        layout.addRow("狀態:", self.statusCombo)

        # 截止日期
        self.dueDateEdit = QDateTimeEdit(self)
        self.dueDateEdit.setCalendarPopup(True)
        self.dueDateEdit.setDateTime(datetime.now())
        layout.addRow("截止日期:", self.dueDateEdit)

        # 按鈕
        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal,
            self
        )
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addRow(buttonBox)

    def getTaskData(self):
        return {
            'title': self.titleEdit.text(),
            'description': self.descriptionEdit.toPlainText(),
            'status': self.statusCombo.currentData(),
            'due_date': self.dueDateEdit.dateTime().toPython()
        }

    def loadTaskData(self):
        if not self.task_data:
            return
            
        self.titleEdit.setText(self.task_data.get('title', ''))
        self.descriptionEdit.setText(self.task_data.get('description', ''))
        
        status_value = self.task_data.get('status')
        if status_value:
            index = self.statusCombo.findText(status_value)
            if index >= 0:
                self.statusCombo.setCurrentIndex(index)
        due_date = self.task_data.get('due_date')
        if due_date:
            if isinstance(due_date, str):
                due_date = datetime.fromisoformat(due_date)
            self.dueDateEdit.setDateTime(due_date)
