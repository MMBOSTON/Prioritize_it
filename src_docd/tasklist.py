"""
Manages a list of tasks and provides functionalities for task operations.

This module encapsulates the operations related to a list of tasks, including adding, viewing, visualizing, and removing tasks. It integrates with DataManager for task persistence and ReportGenerator for report creation.

Classes:
    TaskList: Manages operations on a collection of tasks, including loading, adding, viewing, visualizing, and generating reports.
"""

import logging
from typing import List
import streamlit as st
from .task import Task
# from input_proc.input_proc import InputProc        # Phind removed this import statement.
from src.data_manager import DataManager
from src.report_generator import ReportGenerator
from src.visualizer import Visualizer
from src.sidebar import display_sidebar

class TaskList:
    """
    Manages operations on a collection of tasks, including loading, adding, viewing, visualizing, and generating reports.
    """

    def __init__(self):
        """Initializes the PrioritizeIt application."""
        self.data_manager = DataManager()
        self.visualizer = Visualizer()
        self.report_generator = ReportGenerator(self.data_manager)
        self.tasks = self.data_manager.load_tasks()  # Load tasks from data manager
        #section = display_sidebar(self.tasks)  # Pass self.tasks as an argument    #Phine removed this during docs generation.
        self.input_proc = InputProc(self, section)  # Pass section as an argument

    def use_input_proc(self):
        """Uses InputProc for processing input."""
        return self.input_proc()

    def add_task(self, description, value, effort):
        """Adds a task to the task list.

        Args:
            description (str): Description of the task.
            value (float): Value of the task.
            effort (float): Effort required for the task.
        """
        tasks = self.data_manager.load_tasks()
        if any(task.description == description and task.value == value and task.effort == effort for task in tasks):
            logging.warning(f"Duplicate task: {description}")
            return
        task = Task(description, value, effort)
        tasks.append(task)
        self.data_manager.save_tasks(tasks)

    def view_tasks(self):
        """Views all tasks."""
        return self.data_manager.load_tasks()

    def visualize_tasks(self, tasks):
        """Visualizes tasks."""
        return self.visualizer.visualize_tasks(tasks)

    def load_tasks_from_file(self, file):
        """Loads tasks from a file."""
        self.data_manager.filename = file
        return self.data_manager.load_tasks()

    def get_task_string(self) -> List[str]:     #Phind changed annotation from "list" to "List[str]" during docs gen.
        """Gets a list of task strings."""
        tasks = self.view_tasks()
        task_strings = []
        if tasks:
            tasks.sort(key=lambda task: task.ratio if task.ratio is not None else -float('inf'), reverse=True)
            for task in tasks:
                task_strings.append(f"Task:\n{task.description}\nValue:\n{task.value}\nEffort:\n{task.effort}\nRatio:\n{task.ratio}")
        return task_strings

    def reset_tasks(self):
        """Resets all tasks."""
        self.data_manager.reset_tasks()
        self.visualizer.reset_visualization()
        # Reset session_state keys...

    def remove_task(self, description):
        """Removes a task."""
        tasks = self.data_manager.load_tasks()
        tasks = [task for task in tasks if task.description != description]
        self.data_manager.save_tasks(tasks)

    def generate_Report(self):
        """Generates a report."""
        return self.report_generator.generate_report()