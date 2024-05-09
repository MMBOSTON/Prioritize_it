import logging

from input_proc.input_proc import InputProc  # Import InputProc
from src.data_manager import DataManager
from src.task import Task
from src.tasks_manager import TaskManager
from src.visualizer import Visualizer


class PrioritizeIt:
    """Main class for the PrioritizeIt application."""

    def __init__(self):
        """Initialize the PrioritizeIt application."""
        self.data_manager = DataManager()
        self.visualizer = Visualizer()
        self.task_manager = TaskManager()  # Create an instance of TaskManager
        self.data_manager = DataManager()  # Create an instance of DataManager
        self.input_proc = InputProc()  # Create an instance of InputProc

    def use_input_proc(self):
        """Use InputProc."""
        return self.input_proc()

    def add_task(self, description, value, effort):
        """Add a task."""
        self.task_manager.add_task(description, value, effort)  # Call add_task from TaskManager

    def view_tasks(self):
        """View all tasks."""
        return self.task_manager.view_tasks()  # Call view_tasks from TaskManager

    def visualize_tasks(self, tasks):
        """Visualize tasks."""
        return self.visualizer.visualize_tasks(tasks)  # Call visualize_tasks from Visualizer

    def load_tasks_from_file(self, file):
        """Load tasks from a file."""
        self.data_manager.filename = file  # Set the filename in DataManager
        return self.data_manager.load_tasks()  # Call load_tasks from DataManager

    def get_task_string(self) -> list:
        """
        Get a list of task strings.

        Each task string includes the task's description, value, effort, and ratio.
        Tasks are sorted by ratio in descending order, with tasks having a ratio of None at the end.

        Returns:
            A list of task strings.
        """
        tasks = self.task_manager.view_tasks()  # Call view_tasks from TaskManager
        task_strings = []
        if tasks:
            # Modify the sorting key to handle None values
            tasks.sort(key=lambda task: task.ratio if task.ratio is not None else -float('inf'), reverse=True)
            for task in tasks:
                task_strings.append(f"Task:\n{task.description}\nValue:\n{task.value}\nEffort:\n{task.effort}\nRatio:\n{task.ratio}")
        return task_strings

    def reset_tasks(self):
        """Reset all tasks."""
        self.task_manager.reset_tasks()  # Call reset_tasks from TaskManager

    def remove_task(self, description):
        """Remove a task."""
        self.task_manager.remove_task(description)  # Call remove_task from TaskManager

    def generate_Report(self):
        """Generate a report."""
        # Call generate_Report from TaskManager
        return self.task_manager.generate_Report()
