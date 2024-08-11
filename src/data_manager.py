import json
import logging

from src.task import Task


class DataManager:
    def __init__(self, filename='data/tasks.json'):
        self.filename = filename

    def save_tasks(self, tasks):
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.__dict__ for task in tasks], f)
        except Exception as e:
            logging.error(f"Error saving tasks to file: {e}")

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_dict = json.load(f)
                return [Task(**task) for task in tasks_dict]
        except FileNotFoundError:
            return []
        except Exception as e:
            logging.error(f"Error loading tasks from file: {e}")
            return []


    def reset_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                f.write(json.dumps([])) # overwrite the file with an empty list
        except Exception as e:
            logging.error(f"Error resetting tasks: {e}")