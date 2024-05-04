import json
from .task import Task

class DataManager:
    def __init__(self, filename='data/tasks.json'):
        self.filename = filename

    def save_tasks(self, tasks):
        with open(self.filename, 'w') as f:
            json.dump([task.__dict__ for task in tasks], f)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_dict = json.load(f)
                return [Task(**task) for task in tasks_dict]
        except FileNotFoundError:
            return []

def reset_tasks():
    tasks = []
    with open('data/tasks.json', 'w') as f:
        json.dump(tasks, f)