"""
Module for generating a report of tasks, including:
	total number of tasks, total value, total effort, 
	average value, average effort, and a prioritization of tasks.
"""

import logging
import os
from datetime import datetime

class ReportGenerator:
    """
    Generates a report of tasks.

    Attributes:
        data_manager (DataManager): The data manager instance to interact with for loading tasks.

    Methods:
        generate_report: Generates a report of tasks.
    """

    def __init__(self, data_manager):
        """
        Initializes the ReportGenerator with a data manager.

        Args:
            data_manager (DataManager): The data manager instance to use for loading tasks.
        """
        self.data_manager = data_manager

    def generate_report(self) -> str:
        """
        Generate a report of tasks.

        The report includes the total number of tasks, total value, total effort, average value, average effort, and a prioritization of tasks.

        Returns:
            The report as a string.
        """
        tasks = self.data_manager.load_tasks()
        total_tasks = len(tasks)
        total_value = sum(task.value for task in tasks)
        total_effort = sum(task.effort for task in tasks)
        avg_value = total_value / total_tasks if total_tasks > 0 else 0
        avg_effort = total_effort / total_tasks if total_tasks > 0 else 0

        # Calculate the ratio for each task
        for task in tasks:
            task.calculate_ratio()

        # Start building the report
        report = f"Total tasks: {total_tasks}\n"
        report += f"Total value: {total_value}\n"
        report += f"Total effort: {total_effort}\n"
        report += f"Average value: {avg_value}\n"
        report += f"Average effort: {avg_effort}\n\n"

        # Add task prioritization
        tasks.sort(key=lambda task: task.ratio, reverse=True)
        report += "Task Prioritization:\n"
        for i, task in enumerate(tasks, start=1):
            # Example categorization logic
            if i <= len(tasks) // 4:
                priority = "Prio1"
            elif i <= len(tasks) // 2:
                priority = "Prio2"
            elif i <= 3 * len(tasks) // 4:
                priority = "Prio3"
            else:
                priority = "Prio4"

            # Calculate the formatted ratio string
            formatted_ratio = f"{task.ratio:.2f}" if task.ratio is not None else "0"

            report += f"{task.description} | {task.value} | {task.effort} | {formatted_ratio} | {priority}\n"

        # Ensure the "Report" folder exists
        report_folder = "Report"
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        # Generate a unique filename for the report
        report_filename = f"{report_folder}/Report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        # Write the report to a file
        with open(report_filename, 'w') as f:
            f.write(report)

        return report