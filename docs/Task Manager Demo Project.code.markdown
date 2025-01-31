# Task Manager 示範專案

這是一個基於 PySide6 的任務管理應用程式，展示 MVC 架構設計和常用功能實現。

## 專案結構
```
task_manager/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 程式進入點
│   ├── config.py               # 配置檔案
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # 基礎資料模型
│   │   ├── task.py             # 任務模型
│   │   └── database.py         # 資料庫連接
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py      # 主視窗
│   │   ├── task_dialog.py      # 任務編輯對話框
│   │   └── widgets/
│   │       ├── __init__.py
│   │       └── task_list.py    # 任務列表元件
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── task.py             # 任務控制器
│   └── resources/
│       ├── icons/
│       │   ├── app.ico
│       │   └── actions/
│       │       ├── add.png
│       │       ├── edit.png
│       │       └── delete.png
│       ├── styles/
│       │   └── main.qss
│       └── resources.qrc
├── tests/
│   └── ...
├── README.md
└── requirements.txt
```

## 1. 基礎模型 (Model)

```python
# src/models/task.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    TODO = "待辦"
    IN_PROGRESS = "進行中"
    DONE = "完成"

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    status: TaskStatus
    due_date: datetime
    created_at: datetime = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'due_date': self.due_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
```

```python
# src/models/database.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path('tasks.db')
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.commit()
```

## 2. 視圖 (View)

```python
# src/views/main_window.py
from PySide6.QtWidgets import (QMainWindow, QToolBar, QStatusBar, 
                              QMessageBox)
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QIcon
from .widgets.task_list import TaskListWidget
from .task_dialog import TaskDialog

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
    def updateActions(self):
        has_selection = bool(self.taskList.currentItem())
        self.editAction.setEnabled(has_selection)
        self.deleteAction.setEnabled(has_selection)
```

## 3. 控制器 (Controller)

```python
# src/controllers/task.py
from PySide6.QtCore import QObject, Slot
from ..models.task import Task, TaskStatus
from ..models.database import Database
from ..views.main_window import MainWindow

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
            tasks = conn.execute('SELECT * FROM tasks').fetchall()
            self.view.taskList.clear()
            for task in tasks:
                self.view.taskList.addTask(Task(**task))

    @Slot(dict)
    def addTask(self, task_data):
        task = Task(**task_data)
        with self.db.get_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO tasks (title, description, status, due_date, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (task.title, task.description, task.status.value,
                 task.due_date, task.created_at))
            task.id = cursor.lastrowid
            conn.commit()
        
        self.view.taskList.addTask(task)
        self.view.statusBar.showMessage("任務已新增", 3000)

    @Slot(int, dict)
    def updateTask(self, task_id, task_data):
        task = Task(id=task_id, **task_data)
        with self.db.get_connection() as conn:
            conn.execute('''
                UPDATE tasks
                SET title=?, description=?, status=?, due_date=?
                WHERE id=?
            ''', (task.title, task.description, task.status.value,
                 task.due_date, task.id))
            conn.commit()
        
        self.view.taskList.updateTask(task)
        self.view.statusBar.showMessage("任務已更新", 3000)
```

## 4. 程式進入點

```python
# src/main.py
import sys
from PySide6.QtWidgets import QApplication
from controllers.task import TaskController

def main():
    app = QApplication(sys.argv)
    
    # 載入樣式表
    with open('resources/styles/main.qss', 'r') as f:
        app.setStyleSheet(f.read())
    
    # 創建控制器
    controller = TaskController()
    controller.view.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
```

## 5. 資源檔案

```qss
/* resources/styles/main.qss */
QMainWindow {
    background-color: #f5f5f5;
}

QToolBar {
    background: white;
    border-bottom: 1px solid #ddd;
    spacing: 5px;
    padding: 5px;
}

QToolButton {
    border: none;
    padding: 5px;
    border-radius: 3px;
}

QToolButton:hover {
    background-color: #e0e0e0;
}

QListWidget {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #eee;
}

QListWidget::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}
```

## 6. 使用說明

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 編譯資源
```bash
pyside6-rcc resources/resources.qrc -o resources_rc.py
```

### 運行程式
```bash
python src/main.py
```

## 7. 功能展示

1. 基本操作：
   - 新增任務
   - 編輯任務
   - 刪除任務
   - 查看任務列表

2. 特色功能：
   - MVC 架構設計
   - SQLite 資料庫儲存
   - 響應式使用者介面
   - 自訂樣式表
   - 圖示資源管理

## 8. 擴展建議

1. 新增功能：
   - 任務分類
   - 任務優先級
   - 任務搜尋
   - 任務篩選
   - 匯出/匯入功能

2. 改進建議：
   - 加入單元測試
   - 實作資料驗證
   - 加入日誌記錄
   - 支援多語言
   - 加入使用者認證

## 9. 注意事項

1. 程式碼風格：
   - 遵循 PEP 8 規範
   - 使用型別提示
   - 撰寫文件字串
   - 適當的註釋

2. 錯誤處理：
   - 使用 try-except 處理例外
   - 提供使用者友善的錯誤訊息
   - 記錄錯誤日誌

3. 效能考量：
   - 使用連接池管理資料庫連接
   - 避免不必要的資料庫查詢
   - 大量資料時使用分頁載入
```