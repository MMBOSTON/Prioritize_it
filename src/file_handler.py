import logging

import pandas as pd
from docx import Document
import re


class FileHandler:
    def __init__(self, task_manager):
        self.task_manager = task_manager
    
    def load_tasks_from_file(self, file):
        """
        Load tasks from a file.
        The file can be an Excel file, a Word file, a CSV file, or a plain text file.
        Tasks are added to the task manager.
        Args:
            file: The file to load tasks from.
        """
        try:
            if file.name.endswith('.csv'):
                # Read the file with pandas
                df = pd.read_csv(file)
    
                # Convert the DataFrame to a list of dictionaries
                tasks = df.to_dict('records')
    
                # Add tasks to the task manager
                for task in tasks:
                    self.task_manager.add_task(task['name'], task['priority'], task['effort'])
            else:
                # Handle plain text files
                tasks = []
                for line in file:
                    line = line.decode("utf-8")  # decode the line from bytes to string
                    parts = line.split(' - ', 1)
                    task_name = parts[0].strip()
                    description_parts = parts[1].split(',', 1)
                    task_description = description_parts[0].strip()
                    task_value = re.search(r'(\d+)$', description_parts[1]).group()
                    task_effort = int(task_value)
                    task = {'name': task_name, 'description': task_description, 'priority': int(task_value), 'effort': task_effort}
                    tasks.append(task)
                    self.task_manager.add_task(task['name'], task['priority'], task['effort'])    
        except Exception as e:
            print(f"An error occurred while loading tasks from file: {e}")