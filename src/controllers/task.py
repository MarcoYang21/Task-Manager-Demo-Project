# 首先導入所有需要的模組
from PySide6.QtCore import QObject, Slot  # 確保這行在最前面
from datetime import datetime
from models.task import Task, TaskStatus
from models.database import Database
from views.main_window import MainWindow


# 然後定義控制器類
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
        try:
            with self.db.get_connection() as conn:
                tasks = conn.execute('SELECT * FROM tasks').fetchall()
                self.view.taskList.clear()
                for task_data in tasks:
                    task_dict = dict(task_data)
                    task_dict['status'] = TaskStatus(task_dict['status'])
                    task_dict['due_date'] = datetime.fromisoformat(task_dict['due_date'])
                    task_dict['created_at'] = datetime.fromisoformat(task_dict['created_at'])
                    task = Task(**task_dict)
                    self.view.taskList.addTask(task)
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.view.statusBar.showMessage("載入任務失敗", 3000)

    @Slot(dict)
    def addTask(self, task_data):
        try:
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                due_date=task_data['due_date']
            )
        
            with self.db.get_connection() as conn:
                cursor = conn.execute(
                    '''
                    INSERT INTO tasks (title, description, status, due_date, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (
                        task.title,
                        task.description,
                        task.status.value,
                        task.due_date.isoformat(),
                        task.created_at.isoformat(),
                    )
                )
                task.id = cursor.lastrowid
                conn.commit()

            self.view.taskList.addTask(task)
            self.view.statusBar.showMessage("任務已新增", 3000)
        except Exception as e:
            print(f"Error adding task: {e}")
            self.view.statusBar.showMessage("新增任務失敗", 3000)

    @Slot(int, dict)
    def updateTask(self, task_id, task_data):
        try:
            task = Task(
                id=task_id,
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                due_date=task_data['due_date']
            )
            
            with self.db.get_connection() as conn:
                conn.execute(
                    '''
                    UPDATE tasks
                    SET title=?, description=?, status=?, due_date=?
                    WHERE id=?
                    ''',
                    (
                        task.title,
                        task.description,
                        task.status.value,
                        task.due_date.isoformat(),
                        task.id,
                    )
                )
                conn.commit()

            self.view.taskList.updateTask(task)
            self.view.statusBar.showMessage("任務已更新", 3000)
        except Exception as e:
            print(f"Error updating task: {e}")
            self.view.statusBar.showMessage("更新任務失敗", 3000)

    @Slot(int)
    def deleteTask(self, task_id):
        try:
            with self.db.get_connection() as conn:
                conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
                conn.commit()

            self.view.taskList.deleteTask(task_id)
            self.view.statusBar.showMessage("任務已刪除", 3000)
        except Exception as e:
            print(f"Error deleting task: {e}")
            self.view.statusBar.showMessage("刪除任務失敗", 3000)