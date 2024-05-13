from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from src.task import Task
import pandas as pd

class Visualizer:
    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks: List[str], ratios: List[float]) -> plt.Figure:
        """Plot a Pareto chart of the tasks."""
        if not tasks:
            st.warning("No tasks to visualize.")
            return None

        values = ratios
        labels = tasks

        fig, ax = plt.subplots(figsize=(15, 15))  # Adjust the size as needed

        ax.bar(labels, values, color='blue')  # Added color
        ax.set_xlabel('Tasks', fontsize=12)  # Added fontsize
        ax.set_ylabel('Value/Effort Ratio', fontsize=12)  # Added fontsize
        ax.set_title('Pareto Chart', fontsize=14)  # Adjusted fontsize
        ax.grid(True)  # Added grid
        return fig

    def plot_burndown(self, tasks: List[str], cumulative_value: List[float]) -> plt.Figure:
        """Plot a burndown chart of the tasks."""
        if not tasks:
            st.warning("No tasks to visualize.")
            return None
    
        fig, ax = plt.subplots(figsize=(15, 15))
        ax.plot(range(1, len(tasks) + 1), cumulative_value, marker='o')  # Added marker
        ax.set_xlabel('Tasks Completed', fontsize=12)  # Added fontsize
        ax.set_ylabel('Total Value Delivered', fontsize=12)  # Added fontsize
        ax.set_title('Value Burndown Chart', fontsize=14)  # Added fontsize
        ax.grid(True)  # Added grid
        return fig

    def reset_visualization(self):
        """Reset the visualization by clearing any chart data stored in the session state."""
        if 'chart_data' in st.session_state:
            st.session_state['chart_data'] = None

    def visualize_tasks(self, tasks):
        """Visualize the tasks with a Pareto chart and a burndown chart."""
        if isinstance(tasks, pd.DataFrame):
            self.visualize_tasks_from_df(tasks)
        elif isinstance(tasks, list):
            self.visualize_tasks_from_list(tasks)
        else:
            raise TypeError("Tasks must be a DataFrame or a list.")

    def visualize_tasks_from_df(self, tasks_df: pd.DataFrame):
        """Visualize the tasks from a DataFrame with a Pareto chart and a burndown chart."""
        if tasks_df.empty:
            st.warning("No tasks to visualize.")
            return
    
        # Extract the necessary information from the DataFrame
        tasks = tasks_df['name'].tolist()
        values = tasks_df['task_value'].tolist()
        efforts = tasks_df['task_effort'].tolist()
    
        # Calculate the ratio for each task
        ratios = [v / e for v, e in zip(values, efforts)]
    
        # Sort the tasks based on their ratio
        tasks, ratios = zip(*sorted(zip(tasks, ratios), key=lambda x: x[1], reverse=True))
    
        # Plot the Pareto chart and the burndown chart
        pareto_chart = self.plot_pareto(tasks, ratios)
        burndown_chart = self.plot_burndown(tasks, ratios)
    
        # Display the Pareto chart
        st.pyplot(pareto_chart)
    
        # Display the burndown chart
        st.pyplot(burndown_chart)

    def visualize_tasks_from_list(self, tasks: List[Task]):
        """Visualize the tasks from a list with a Pareto chart and a burndown chart."""
        if not tasks:
            st.warning("No tasks to visualize.")
            return
    
        # Extract the necessary information from the list
        task_names = [task.name for task in tasks]
        values = [task.value for task in tasks]
        efforts = [task.effort for task in tasks]
    
        # Calculate the ratio for each task
        ratios = [v / e for v, e in zip(values, efforts)]
    
        # Sort the tasks based on their ratio
        tasks, ratios = zip(*sorted(zip(task_names, ratios), key=lambda x: x[1], reverse=True))
    
        # Calculate the cumulative values
        cumulative_value = [sum(ratios[:i+1]) for i in range(len(ratios))]
    
        # Plot the Pareto chart and the burndown chart
        pareto_chart = self.plot_pareto(tasks, ratios)
        burndown_chart = self.plot_burndown(tasks, cumulative_value)
    
        # Display the Pareto chart
        st.pyplot(pareto_chart)
    
        # Display the burndown chart
        st.pyplot(burndown_chart)