import logging

import pandas as pd
from docx import Document


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
                    description, value_effort = line.rsplit(" ", 1)  # split the line into description and value/effort
                    value, effort = value_effort.split(",")  # split the value/effort into value and effort
                    task = {'name': description.strip(), 'priority': int(value.strip()), 'effort': int(effort.strip())}  # create a new task
                    tasks.append(task)  # add the task to the tasks list
                    self.task_manager.add_task(task['name'], task['priority'], task['effort'])

        except Exception as e:
            print(f"An error occurred while loading tasks from file: {e}")

    def parse_task_from_paragraph(self, text):
        """
        Parse a task from a paragraph of text.
        The text is expected to be in the format "1. Description - Value - Effort".
        Args:
            text: The text to parse.
        Returns:
            A tuple containing the description, value, and effort of the task.
        Raises:
            ValueError: If the text cannot be parsed into exactly three parts.
        """
        parts = text.split(" - ")
        if len(parts) != 3:
            raise ValueError(f"Cannot parse task from text: {text}")
        description = parts[0].split(". ")[1]
        value = int(parts[1])
        effort = int(parts[2])
        return description, value, effort