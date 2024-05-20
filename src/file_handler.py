import logging

import pandas as pd
from docx import Document
import re
import json
import csv

class FileHandler:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def parse_json_to_txt_csv(self, json_file, txt_file, csv_file):
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