from src.data_manager import DataManager
from src.visualizer import Visualizer
from src.task import Task

class PrioritizeIt:
    def __init__(self):
        self.data_manager = DataManager()
        self.visualizer = Visualizer()

    def add_task(self, description, value, effort):
        task = Task(description, value, effort)
        tasks = self.data_manager.load_tasks()
        tasks.append(task)
        self.data_manager.save_tasks(tasks)

    def remove_task(self, description):
        tasks = self.data_manager.load_tasks()
        tasks = [task for task in tasks if task.description != description]
        self.data_manager.save_tasks(tasks)

    def view_tasks(self):
        return self.data_manager.load_tasks()

    def generate_report(self):
        tasks = self.data_manager.load_tasks()
        total_tasks = len(tasks)
        total_value = sum(task.value for task in tasks)
        total_effort = sum(task.effort for task in tasks)
        avg_value = total_value / total_tasks if total_tasks > 0 else 0
        avg_effort = total_effort / total_tasks if total_tasks > 0 else 0

        report = f"Total tasks: {total_tasks}\n"
        report += f"Total value: {total_value}\n"
        report += f"Total effort: {total_effort}\n"
        report += f"Average value: {avg_value}\n"
        report += f"Average effort: {avg_effort}\n\n"

        tasks.sort(key=lambda task: task.ratio, reverse=True)
        report += "Task Prioritization:\n"
        for task in tasks:
            report += f"Task: {task.description}, Value: {task.value}, Effort: {task.effort}, Ratio: {task.ratio}\n"

        return report

    def visualize_tasks(self, tasks):
        pareto_chart = self.visualizer.plot_pareto(tasks)
        burndown_chart = self.visualizer.plot_burndown(tasks)
        return pareto_chart, burndown_chart