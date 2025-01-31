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
    title: str
    description: str
    status: TaskStatus
    due_date: datetime
    id: Optional[int] = None  # 將 id 設為可選參數，默認為 None
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
