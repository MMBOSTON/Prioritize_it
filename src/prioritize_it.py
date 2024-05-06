from src.data_manager import DataManager
from src.visualizer import Visualizer
from src.task import Task
import pandas as pd
from docx import Document
import logging
import os
from datetime import datetime
import shutil

class PrioritizeIt:
    def __init__(self):
        self.data_manager = DataManager()
        self.visualizer = Visualizer()

    def add_task(self, description, value, effort):
        tasks = self.data_manager.load_tasks()
        # Check for duplicate tasks
        if any(task.description == description and task.value == value and task.effort == effort for task in tasks):
            logging.warning(f"Duplicate task: {description}")
            return
        task = Task(description, value, effort)
        tasks.append(task)
        self.data_manager.save_tasks(tasks)

    def remove_a_task(self, description):
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

    def view_tasks(self):
        return self.data_manager.load_tasks()

    def generate_Report(self):
        tasks = self.data_manager.load_tasks()
        tasks.sort(key=lambda task: task.ratio, reverse=True)

        # Start building the Report
        Report = "Detailed Task Report:\n\n"
        Report += "Task | Value | Effort | Ratio | Priority\n"
        Report += "-----|-------|--------|-------|---------\n"

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

            Report += f"{task.description} | {task.value} | {task.effort} | {task.ratio:.2f} | {priority}\n"

        # Ensure the "Report" folder exists
        Report_folder = "Report"
        if not os.path.exists(Report_folder):
            os.makedirs(Report_folder)

        # Generate a unique filename for the Report
        Report_filename = f"{Report_folder}/Report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        # Write the Report to a file
        with open(Report_filename, 'w') as f:
            f.write(Report)

        return Report

    def visualize_tasks(self, tasks):
        pareto_chart = self.visualizer.plot_pareto(tasks)
        burndown_chart = self.visualizer.plot_burndown(tasks)
        return pareto_chart, burndown_chart

    def get_task_string(self):
        tasks = self.view_tasks()
        task_strings = []
        if tasks:
            tasks.sort(key=lambda task: task.ratio, reverse=True)
            for task in tasks:
                task_strings.append(f"Task:\n{task.description}\nValue:\n{task.value}\nEffort:\n{task.effort}\nRatio:\n{task.ratio}")
        return task_strings

    def reset_tasks(self):
        self.data_manager.reset_tasks()

    def load_tasks_from_file(self, file):
        try:
            if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                # Handle Excel file
                df = pd.read_excel(file)
                # Basic check for expected columns
                if 'Description' not in df.columns or 'Value' not in df.columns or 'Effort' not in df.columns:
                    logging.error("Excel file does not have the expected columns: Description, Value, Effort")
                    return
                for index, row in df.iterrows():
                    self.add_task(row['Description'], row['Value'], row['Effort'])
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                # Handle Word file
                doc = Document(file)
                for paragraph in doc.paragraphs:
                    if paragraph.text.startswith("1.") or paragraph.text.startswith("2.") or paragraph.text.startswith("3."):
                        description, value, effort = self.parse_task_from_paragraph(paragraph.text)
                        self.add_task(description, value, effort)
            elif file.type == "text/csv":
                # Handle CSV file
                df = pd.read_csv(file)
                for index, row in df.iterrows():
                    self.add_task(row['Description'], row['Value'], row['Effort'])
        except Exception as e:
            logging.error(f"Error loading tasks from file: {e}")

    def parse_task_from_paragraph(self, text):
        parts = text.split(" - ")
        description = parts[0].split(". ")[1]
        value = int(parts[1])
        effort = int(parts[2])
        return description, value, effort

    def generate_Report(self):
        tasks = self.data_manager.load_tasks()
        total_tasks = len(tasks)
        total_value = sum(task.value for task in tasks)
        total_effort = sum(task.effort for task in tasks)
        avg_value = total_value / total_tasks if total_tasks > 0 else 0
        avg_effort = total_effort / total_tasks if total_tasks > 0 else 0

        # Start building the Report
        Report = f"Total tasks: {total_tasks}\n"
        Report += f"Total value: {total_value}\n"
        Report += f"Total effort: {total_effort}\n"
        Report += f"Average value: {avg_value}\n"
        Report += f"Average effort: {avg_effort}\n\n"

        # Add task prioritization
        tasks.sort(key=lambda task: task.ratio, reverse=True)
        Report += "Task Prioritization:\n"
        for task in tasks:
            Report += f"Task: {task.description}, Value: {task.value}, Effort: {task.effort}, Ratio: {task.ratio}\n"

        # Ensure the "Report" folder exists
        Report_folder = "Report"
        if not os.path.exists(Report_folder):
            os.makedirs(Report_folder)

        # Generate a unique filename for the Report
        Report_filename = f"{Report_folder}/Report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

        # Write the Report to a file
        with open(Report_filename, 'w') as f:
            f.write(Report)

        return Report
