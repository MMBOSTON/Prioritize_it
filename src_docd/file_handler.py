"""
Module for handling file operations related to tasks, including parsing JSON to TXT and CSV formats.

This module provides functionality to parse task data from a JSON file and write it to TXT and CSV files. It also includes a method for loading tasks from various file types into the task manager.
"""

import logging
import pandas as pd
from docx import Document
import re
import json
import csv

class FileHandler:
    """
    Handles file operations related to tasks, including parsing JSON to TXT and CSV formats and loading tasks from files.

    Attributes:
        task_manager (TaskManager): The task manager instance to interact with.

    Methods:
        parse_json_to_txt_csv: Parses a JSON file and writes the data to TXT and CSV files.
        load_tasks_from_file: Loads tasks from a file and adds them to the task manager.
    """

    def __init__(self, task_manager):
        """
        Initializes the FileHandler with a task manager.

        Args:
            task_manager (TaskManager): The task manager instance to use for task operations.
        """
        self.task_manager = task_manager

    def parse_json_to_txt_csv(self, json_file, txt_file, csv_file):
        """
        Parses a JSON file containing tasks and writes the data to TXT and CSV files.

        Args:
            json_file (str): The path to the JSON file to parse.
            txt_file (str): The path to the TXT file to write to.
            csv_file (str): The path to the CSV file to write to.
        """
        try:
            print(f"Opening JSON file: {json_file}")  # Debug print
            with open(json_file, 'r') as f:
                tasks = json.load(f)
                print(f"Loaded tasks: {tasks}")  # Debug print

            print(f"Writing to TXT file: {txt_file}")  # Debug print
            with open(txt_file, 'w') as f:
                for task in tasks:
                    f.write(f"Task_Name: {task['name']}\n")
                    f.write(f"Task Description: {task['description']}\n")
                    f.write(f"Task ID: {task['task_id']}\n")
                    f.write(f"Task Value: {task['task_value']}\n")
                    f.write(f"Task Effort: {task['task_effort']}\n")
                    ratio = task['task_value'] / task['task_effort']
                    rank = 1  # Placeholder, implement actual ranking logic
                    f.write(f"Ratio: {ratio}\n")
                    f.write(f"Rank: {rank}\n")
                    f.write("\n")

            print(f"Writing to CSV file: {csv_file}")  # Debug print
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Task_Name', 'Task Description', 'Task ID', 'Task Value', 'Task Effort', 'Ratio', 'Rank'])
                writer.writeheader()
                for task in tasks:
                    writer.writerow({
                        'Task_Name': task['name'],
                        'Task Description': task['description'],
                        'Task ID': task['task_id'],
                        'Task Value': task['task_value'],
                        'Task Effort': task['task_effort'],
                        'Ratio': ratio,
                        'Rank': rank,
                    })
        except Exception as e:
            print(f"An error occurred while parsing the JSON file: {e}")

    def load_tasks_from_file(self, file):
        """
        Loads tasks from a file and adds them to the task manager.
        The file format can be Excel, Word, CSV, or plain text. 

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