"""
Filename: task.py
Updated_By: Rich Lysakowski
Updated_On: 2024.08.09

Defines the Task class for task management, each individual task has attributes: 
    description, value, effort, and a calculated ratio for prioritization. 

Includes methods for calculating the task's value-effort ratio and generating a simple report.

Classes:
    Task: Represents a task with attributes and methods for calculation and reporting.
"""

class Task:
    def __init__(self, description, value, effort, ratio=None, id=None, name=None):
        """
        Initializes a Task instance.

        Args:
            description (str): Description of the task.
            value (float): Value of the task.
            effort (float): Effort required for the task.
            ratio (float, optional): Pre-calculated ratio of value to effort. Defaults to None.
            id (str, optional): Unique identifier for the task. Defaults to None.
            name (str, optional): Name of the task. Defaults to None.
        """
        self.description = description
        self.value = value
        self.effort = effort
        self.id = id
        self.name = name
        self.calculate_ratio()  # Call calculate_ratio here

    def __str__(self):
        """Returns a string representation of the Task."""
        return f"Task(name={self.name}, description={self.description}, value={self.value}, effort={self.effort}, ratio={self.ratio}, id={self.id}"

    def calculate_ratio(self):
        """Calculates the task's ratio based on its value and effort."""
        if self.effort == 0:
            self.ratio = 0  # Or any other appropriate value for division by zero
        else:
            self.ratio = self.value / self.effort

    def generate_report(self):
        """Generates a simple report for the task."""
        print(f"Generating report for task: {self.name}")