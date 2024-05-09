from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from src.task import Task


class Visualizer:
    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks: List[Task]) -> plt.Figure:
        """Plot a Pareto chart of the tasks."""
        tasks.sort(key=lambda x: x.ratio if x.ratio is not None else -float('inf'), reverse=True)
        values = [task.value for task in tasks]
        labels = [task.description for task in tasks]
        
        fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the size as needed
        
        ax.bar(labels, values)
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Value/Effort Ratio')
        ax.set_title('Pareto Chart', fontsize=40)
        return fig

    def plot_burndown(self, tasks: List[Task]) -> plt.Figure:
        """Plot a burndown chart of the tasks."""
        tasks.sort(key=lambda x: x.ratio if x.ratio is not None else -float('inf'), reverse=True)
        cumulative_value = [sum(task.value for task in tasks[:i+1]) for i in range(len(tasks))]
        labels = range(1, len(tasks) + 1)
        fig, ax = plt.subplots()
        ax.plot(labels, cumulative_value)
        ax.set_xlabel('Tasks Completed')
        ax.set_ylabel('Total Value Delivered')
        ax.set_title('Value Burndown Chart')
        return fig

    def reset_visualization(self):
        """Reset the visualization by clearing any chart data stored in the session state."""
        if 'chart_data' in st.session_state:
            st.session_state['chart_data'] = None

    def visualize_tasks(self, tasks: List[Task]) -> (plt.Figure, plt.Figure):
        """Visualize the tasks with a Pareto chart and a burndown chart."""
        pareto_chart = self.plot_pareto(tasks)
        burndown_chart = self.plot_burndown(tasks)
        return pareto_chart, burndown_chart