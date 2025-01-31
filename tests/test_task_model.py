import unittest
from datetime import datetime
from src.models.task import Task, TaskStatus

class TestTaskModel(unittest.TestCase):
    def setUp(self):
        self.task_data = {
            'id': 1,
            'title': "測試任務",
            'description': "這是一個測試任務",
            'status': TaskStatus.TODO,
            'due_date': datetime.now(),
        }
        self.task = Task(**self.task_data)

    def test_task_creation(self):
        self.assertEqual(self.task.id, 1)
        self.assertEqual(self.task.title, "測試任務")
        self.assertEqual(self.task.description, "這是一個測試任務")
        self.assertEqual(self.task.status, TaskStatus.TODO)

    def test_task_to_dict(self):
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict['id'], 1)
        self.assertEqual(task_dict['title'], "測試任務")
        self.assertEqual(task_dict['status'], "待辦")

if __name__ == '__main__':
    unittest.main()