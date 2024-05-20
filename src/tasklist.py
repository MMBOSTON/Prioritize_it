import logging
import os
import shutil
from typing import List

import streamlit as st

from .task import Task
from input_proc.input_proc import InputProc
from src.data_manager import DataManager
from src.report_generator import ReportGenerator
from src.visualizer import Visualizer
from src.sidebar import display_sidebar

class TaskList:

    def __init__(self):
        """Initialize the PrioritizeIt application."""
        self.data_manager = DataManager()
        self.visualizer = Visualizer()
        self.report_generator = ReportGenerator(self.data_manager)
        self.tasks = self.data_manager.load_tasks()  # Load tasks from data manager
        section = display_sidebar(self.tasks)  # Pass self.tasks as an argument
        self.input_proc = InputProc(self, section)  # Pass section as an argument

    def use_input_proc(self):
        """Use InputProc."""
        return self.input_proc()

    def add_task(self, description, value, effort):
        """Add a task."""
        tasks = self.data_manager.load_tasks()
        if any(task.description == description and task.value == value and task.effort == effort for task in tasks):
            logging.warning(f"Duplicate task: {description}")
            return
        task = Task(description, value, effort)
        tasks.append(task)
        self.data_manager.save_tasks(tasks)

    def view_tasks(self):
        """View all tasks."""
        return self.data_manager.load_tasks()

    def visualize_tasks(self, tasks):
        """Visualize tasks."""
        return self.visualizer.visualize_tasks(tasks)

    def load_tasks_from_file(self, file):
        """Load tasks from a file."""
        self.data_manager.filename = file
        return self.data_manager.load_tasks()

    def get_task_string(self) -> list:
        """
        Get a list of task strings.

        Each task string includes the task's description, value, effort, and ratio.
        Tasks are sorted by ratio in descending order, with tasks having a ratio of None at the end.

        Returns:
            A list of task strings.
        """
        tasks = self.view_tasks()
        task_strings = []
        if tasks:
            tasks.sort(key=lambda task: task.ratio if task.ratio is not None else -float('inf'), reverse=True)
            for task in tasks:
                task_strings.append(f"Task:\n{task.description}\nValue:\n{task.value}\nEffort:\n{task.effort}\nRatio:\n{task.ratio}")
        return task_strings

    def reset_tasks(self):
        """Reset all tasks."""
        self.data_manager.reset_tasks()
        self.visualizer.reset_visualization()
        if 'pareto_chart' in st.session_state:
            st.session_state['pareto_chart'] = None
        if 'burndown_chart' in st.session_state:
            st.session_state['burndown_chart'] = None
        if 'Report' in st.session_state:
            st.session_state['Report'] = None
        if 'visualize' in st.session_state:
            st.session_state['visualize'] = False
        if 'task_description' in st.session_state:
            st.session_state['task_description'] = ""

    def remove_task(self, description):
        """Remove a task."""
        tasks = self.data_manager.load_tasks()
        tasks = [task for task in tasks if task.description != description]
        self.data_manager.save_tasks(tasks)

    def generate_Report(self):
        """Generate a report."""
        return self.report_generator.generate_report()
