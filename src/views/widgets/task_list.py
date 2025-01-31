from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from models.task import Task


class TaskListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.SingleSelection)

    def addTask(self, task: Task):
        item = QListWidgetItem(self)
        item.setText(f"{task.title} - {task.status.value}")
        item.setData(Qt.UserRole, task.id)
        item.setData(Qt.UserRole + 1, task.to_dict())
        self.addItem(item)

    def updateTask(self, task: Task):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == task.id:
                item.setText(f"{task.title} - {task.status.value}")
                item.setData(Qt.UserRole + 1, task.to_dict())
                break

    def deleteTask(self, task_id: int):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == task_id:
                self.takeItem(i)
                break

    def getCurrentTask(self):
        item = self.currentItem()
        if item:
            return item.data(Qt.UserRole), item.data(Qt.UserRole + 1)
        return None, None