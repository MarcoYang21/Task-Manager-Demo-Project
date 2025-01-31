from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QMessageBox
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from views.widgets.task_list import TaskListWidget  # 改為絕對導入
from views.task_dialog import TaskDialog  # 改為絕對導入


class MainWindow(QMainWindow):
    taskAdded = Signal(dict)
    taskUpdated = Signal(int, dict)
    taskDeleted = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("任務管理系統")
        self.resize(800, 600)
        self.setupUi()
        self.loadIcons()
        self.connectSignals()

    def setupUi(self):
        # 建立工具列
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # 建立動作
        self.addAction = QAction("新增任務", self)
        self.editAction = QAction("編輯任務", self)
        self.deleteAction = QAction("刪除任務", self)

        self.toolbar.addAction(self.addAction)
        self.toolbar.addAction(self.editAction)
        self.toolbar.addAction(self.deleteAction)

        # 建立任務列表
        self.taskList = TaskListWidget()
        self.setCentralWidget(self.taskList)

        # 建立狀態列
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def loadIcons(self):
        self.addAction.setIcon(QIcon(":/icons/actions/add.png"))
        self.editAction.setIcon(QIcon(":/icons/actions/edit.png"))
        self.deleteAction.setIcon(QIcon(":/icons/actions/delete.png"))

    def connectSignals(self):
        self.addAction.triggered.connect(self.onAddTask)
        self.editAction.triggered.connect(self.onEditTask)
        self.deleteAction.triggered.connect(self.onDeleteTask)
        self.taskList.itemSelectionChanged.connect(self.updateActions)

    @Slot()
    def onAddTask(self):
        dialog = TaskDialog(self)
        if dialog.exec():
            task_data = dialog.getTaskData()
            self.taskAdded.emit(task_data)

    @Slot()
    def onEditTask(self):
        current_item = self.taskList.currentItem()
        if not current_item:
            return

        task_id = current_item.data(0)
        dialog = TaskDialog(self, current_item.data(1))
        if dialog.exec():
            task_data = dialog.getTaskData()
            self.taskUpdated.emit(task_id, task_data)

    @Slot()
    def onDeleteTask(self):
        current_item = self.taskList.currentItem()
        if not current_item:
            return

        task_id = current_item.data(0)
        reply = QMessageBox.question(
            self,
            "確認刪除",
            "確定要刪除這個任務嗎?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.taskDeleted.emit(task_id)

    @Slot()
    def updateActions(self):
        has_selection = bool(self.taskList.currentItem())
        self.editAction.setEnabled(has_selection)
        self.deleteAction.setEnabled(has_selection)
