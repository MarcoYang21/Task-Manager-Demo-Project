from PySide6.QtCore import QObject, Slot
from models.task import Task, TaskStatus
from models.database import Database
from views.main_window import MainWindow


class TaskController(QObject):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.view = MainWindow()
        self.setupConnections()
        self.loadTasks()

    def setupConnections(self):
        self.view.taskAdded.connect(self.addTask)
        self.view.taskUpdated.connect(self.updateTask)
        self.view.taskDeleted.connect(self.deleteTask)

    def loadTasks(self):
        with self.db.get_connection() as conn:
            tasks = conn.execute("SELECT * FROM tasks").fetchall()
            self.view.taskList.clear()
            for task in tasks:
                self.view.taskList.addTask(Task(**task))

    @Slot(dict)
    def addTask(self, task_data):
        task = Task(**task_data)
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tasks (title, description, status, due_date, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    task.title,
                    task.description,
                    task.status.value,
                    task.due_date,
                    task.created_at,
                ),
            )
            task.id = cursor.lastrowid
            conn.commit()

        self.view.taskList.addTask(task)
        self.view.statusBar.showMessage("任務已新增", 3000)

    @Slot(int, dict)
    def updateTask(self, task_id, task_data):
        task = Task(id=task_id, **task_data)
        with self.db.get_connection() as conn:
            conn.execute(
                """
                UPDATE tasks
                SET title=?, description=?, status=?, due_date=?
                WHERE id=?
            """,
                (
                    task.title,
                    task.description,
                    task.status.value,
                    task.due_date,
                    task.id,
                ),
            )
            conn.commit()

        self.view.taskList.updateTask(task)
        self.view.statusBar.showMessage("任務已更新", 3000)

    @Slot(int)
    def deleteTask(self, task_id):
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()

        self.view.taskList.deleteTask(task_id)
        self.view.statusBar.showMessage("任務已刪除", 3000)
