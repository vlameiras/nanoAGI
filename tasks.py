from collections import deque
from typing import List


class Task:
    def __init__(self, task_id: str, task_name: str, task_description: str):
        self.task_id = task_id
        self.task_description = task_description
        self.task_name = task_name
