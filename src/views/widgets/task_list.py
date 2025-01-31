from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


class TaskListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)

    def addTask(self, task):
        item = QListWidgetItem(task.title)
        item.setData(Qt.UserRole, task.id)
        item.setData(Qt.UserRole + 1, task.to_dict())
        self.addItem(item)

    def updateTask(self, task):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == task.id:
                item.setText(task.title)
                item.setData(Qt.UserRole + 1, task.to_dict())
                break

    def deleteTask(self, task_id):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == task_id:
                self.takeItem(i)
                break
