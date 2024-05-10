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
            pass  # Rest of your load_tasks_from_file code...

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