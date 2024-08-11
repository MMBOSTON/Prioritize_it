"""
Module for managing task data, including saving, loading, and resetting tasks.

This module provides functionality to save tasks to a file, load tasks from a file, and reset tasks. It uses JSON for data serialization and deserialization.
Tasks are represented as dictionaries and stored in a file specified by the filename attribute of the DataManager class.
"""

from ..src.task import Task  # Phind added this line during documentation generation.
import json
import logging

# from .task import Task     # Phind removed this line during documentation generation.


class DataManager:
    """
    Manages task data, including saving, loading, and resetting tasks.

    Attributes:
        filename (str): The filename where tasks are stored.

    Methods:
        save_tasks: Saves a list of tasks to a file.
        load_tasks: Loads tasks from a file.
        reset_tasks: Resets the tasks file to an empty state.
    """

    def __init__(self, filename='data/tasks.json'):
        """
        Initializes the DataManager with a filename.

        Args:
            filename (str): The filename where tasks are stored. Defaults to 'data/tasks.json'.
        """
        self.filename = filename

    def save_tasks(self, tasks):
        """
        Saves a list of tasks to a file.

        Args:
            tasks (list): A list of Task objects to save.
        """
        try:
            with open(self.filename, 'w') as f:
                json.dump([task.__dict__ for task in tasks], f)
        except Exception as e:
            logging.error(f"Error saving tasks to file: {e}")

    def load_tasks(self):
        """
        Loads tasks from a file.

        Returns:
            list: A list of Task objects loaded from the file. Returns an empty list if the file does not exist or an error occurs.
        """
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
        """
        Resets the tasks file to an empty state.
        """
        try:
            with open(self.filename, 'w') as f:
                f.write(json.dumps([])) # overwrite the file with an empty list
        except Exception as e:
            logging.error(f"Error resetting tasks: {e}")