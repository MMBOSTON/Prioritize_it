import logging
import os
import shutil
from typing import List

import streamlit as st

from input_proc.generate_tasks import TaskCore
from src.data_manager import DataManager
from src.report_generator import ReportGenerator
from src.task import Task
from src.visualizer import Visualizer


class TaskManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.visualizer = Visualizer()  # Create an instance of Visualizer
        self.report_generator = ReportGenerator(self.data_manager)

    def add_task(self, description, value, effort):
        tasks = self.data_manager.load_tasks()
        # Check for duplicate tasks
        if any(task.description == description and task.value == value and task.effort == effort for task in tasks):
            logging.warning(f"Duplicate task: {description}")
            return
        task = Task(description, value, effort)
        tasks.append(task)
        self.data_manager.save_tasks(tasks)

    def remove_task(self, description):
        """Remove a specific task based on its description."""
        tasks = self.data_manager.load_tasks()
        tasks = [task for task in tasks if task.description != description]
        self.data_manager.save_tasks(tasks)

    def remove_all_tasks(self):
        """Remove all inserted tasks, delete the generated Report folder, and clear visualization."""
        self.data_manager.reset_tasks()
        
        # Define the path to the Report folder
        report_folder_path = "Report"
        
        # Check if the Report folder exists
        if os.path.exists(report_folder_path):
            try:
                # Delete the Report folder and all its contents
                shutil.rmtree(report_folder_path)
                print("Report folder and its contents have been deleted.")
            except Exception as e:
                print(f"Error deleting the Report folder: {e}")
        else:
            print("Report folder does not exist.")
        
        # Reset the session state for visualization
        if 'visualize' in st.session_state:
            st.session_state['visualize'] = False

    def generate_Report(self):
        """Generate a report."""
        return self.report_generator.generate_report()

    def view_tasks(self):
        return self.data_manager.load_tasks()

    def reset_tasks(self):
        # Clear tasks from the data manager
        self.data_manager.reset_tasks()
        
        # Reset visualization state
        self.visualizer.reset_visualization()
        
        # Clear Streamlit session state related to tasks and visualizations
        if 'pareto_chart' in st.session_state:
            st.session_state['pareto_chart'] = None
        if 'burndown_chart' in st.session_state:
            st.session_state['burndown_chart'] = None
        if 'Report' in st.session_state:
            st.session_state['Report'] = None
        if 'visualize' in st.session_state:
            st.session_state['visualize'] = False
        # Clear the task description field
        if 'task_description' in st.session_state:
            st.session_state['task_description'] = ""

def save_tasks_to_json(tasks):
    with open('data/core_tasks.json', 'w') as f:
        for task in tasks:
            json.dump(task.__dict__, f)
            f.write('\n')
    
    task_data = [task.__dict__ for task in tasks]
    with open(filename, 'w') as f:
        json.dump(task_data, f)