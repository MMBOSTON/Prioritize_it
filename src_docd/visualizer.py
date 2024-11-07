"""
############################################################################################
WARNING !!! THIS FILE WAS SIGNIFICANTLY ALTERED DURING THE PHIND DOCS GENERATION PROCESS.  

TODO: IT NEEDS TO BE CHECKED FOR CORRECTNESS.  

IT MAY BE MORE CORRECT THAN THE ORIGINAL BUT COULD ALSO BE TOTALLY WRONG.  

THINGS TO WATCH OUT FOR... 

	IT DOES NOT USE STREAMLIT.  IT DOES NOT EVEN IMPORT STREAMLIT !!
	IT USES A matplotlib "plt" object instead of "ax" axes objects.  
	It has MAJOR differences in the following function.
		def visualize_tasks_from_df(self, tasks_df: pd.DataFrame):

############################################################################################
Module for visualizing task data using matplotlib and seaborn.

This module provides functionality to visualize task data through various charts, including Pareto charts, burndown charts, and cumulative effort curves. It supports visualizing tasks from both pandas DataFrames and lists of Task objects.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List
from src.task import Task

class Visualizer:
    """
    Visualizes task data using matplotlib and seaborn.

    Methods:
        plot_pareto: Plots a Pareto chart of tasks.
        plot_burndown: Plots a burndown chart of tasks.
        plot_combined: Plots a combined Pareto and burndown chart.
        plot_cumulative_effort: Plots a cumulative effort curve.
        visualize_tasks_from_df: Visualizes tasks from a pandas DataFrame.
        visualize_tasks_from_list: Visualizes tasks from a list of Task objects.
        visualize_tasks: Determines the type of input and calls the appropriate visualization method.
        reset_visualization: Resets the visualization state in Streamlit.
    """

    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks: List[str], ratios: List[float]) -> plt.Figure:
        """
        Plots a Pareto chart of tasks.

        Args:
            tasks (List[str]): A list of task names.
            ratios (List[float]): A list of value/effort ratios for each task.

        Returns:
            plt.Figure: The figure object of the Pareto chart.
        """
        if not tasks:
            plt.figure(figsize=(15, 15))
            plt.bar(tasks, ratios, color='blue')
            plt.xlabel('Tasks', fontsize=12)
            plt.ylabel('Value/Effort Ratio', fontsize=12)
            plt.title('Pareto Chart', fontsize=14)
            plt.grid(True)
            return plt.gcf()

    def plot_burndown(self, tasks: List[str], cumulative_value: List[float]) -> plt.Figure:
        """
        Plots a burndown chart of tasks.

        Args:
            tasks (List[str]): A list of task names.
            cumulative_value (List[float]): A list of cumulative values for each task.

        Returns:
            plt.Figure: The figure object of the burndown chart.
        """
        if not tasks:
            plt.figure(figsize=(15, 15))
            plt.plot(range(1, len(tasks) + 1), cumulative_value, marker='o')
            plt.xlabel('Tasks Completed', fontsize=12)
            plt.ylabel('Total Value Delivered', fontsize=12)
            plt.title('Value Burndown Chart', fontsize=14)
            plt.grid(True)
            return plt.gcf()

    def plot_combined(self, tasks: List[str], ratios: List[float], cumulative_value: List[float]) -> plt.Figure:
        """
        Plots a combined Pareto and burndown chart.

        Args:
            tasks (List[str]): A list of task names.
            ratios (List[float]): A list of value/effort ratios for each task.
            cumulative_value (List[float]): A list of cumulative values for each task.

        Returns:
            plt.Figure: The figure object of the combined chart.
        """
        if not tasks:
            fig, ax1 = plt.subplots(figsize=(15, 15))
            color = 'tab:blue'
            ax1.set_xlabel('Tasks', fontsize=12)
            ax1.set_ylabel('Value/Effort Ratio', color=color, fontsize=12)
            ax1.bar(tasks, ratios, color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax2 = ax1.twinx()
            color = 'tab:red'
            ax2.set_ylabel('Total Value Delivered', color=color, fontsize=12)
            ax2.plot(range(1, len(tasks) + 1), cumulative_value, color=color, marker='o')
            ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()
            ax1.grid(True)
            return fig

    def plot_cumulative_effort(self, tasks: List[str], cumulative_effort: List[float]) -> plt.Figure:
        """
        Plots a cumulative effort curve.

        Args:
            tasks (List[str]): A list of task names.
            cumulative_effort (List[float]): A list of cumulative efforts for each task.

        Returns:
            plt.Figure: The figure object of the cumulative effort curve.
        """
        if not tasks:
            plt.figure(figsize=(15, 15))
            plt.plot(range(1, len(tasks) + 1), cumulative_effort, marker='o')
            plt.xlabel('Tasks Completed', fontsize=12)
            plt.ylabel('Total Effort Expended', fontsize=12)
            plt.title('Cumulative Effort Curve', fontsize=14)
            plt.grid(True)
            return plt.gcf()

    def visualize_tasks_from_df(self, tasks_df: pd.DataFrame):
        """
        Visualizes tasks from a pandas DataFrame.

        Args:
            tasks_df (pd.DataFrame): A DataFrame containing task data.
        """
        if tasks_df.empty:
            plt.figure(figsize=(15, 15))
            plt.plot(range(1, len(tasks_df) + 1), tasks_df['cumulative_value'].tolist(), marker='o')
            plt.xlabel('Tasks Completed', fontsize=12)
            plt.ylabel('Total Value Delivered', fontsize=12)
            plt.title('Value Burndown Chart', fontsize=14)
            plt.grid(True)
            plt.show()

    def visualize_tasks_from_list(self, tasks: List[Task]):
        """
        Visualizes tasks from a list of Task objects.

        Args:
            tasks (List[Task]): A list of Task objects.
        """
        if not tasks:
            values = [task.value for task in tasks]
            efforts = [task.effort for task in tasks]
            ratios = [v / e for v, e in zip(values, efforts)]
            tasks, ratios = zip(*sorted(zip(tasks, ratios), key=lambda x: x[1], reverse=True)
            cumulative_value = [sum(ratios[:i+1] for i in range(len(ratios))]
            cumulative_effort = [sum(efforts[:i+1] for i in range(len(efforts))]
            self.plot_combined(tasks, ratios, cumulative_value)

    def visualize_tasks(self, tasks):
        """
        Determines the type of input and calls the appropriate visualization method.

        Args:
            tasks (Union[pd.DataFrame, List[Task]): Either a DataFrame or a list of Task objects.
        """
        if isinstance(tasks, pd.DataFrame):
            self.visualize_tasks_from_df(tasks)
        elif isinstance(tasks, list):
            self.visualize_tasks_from_list(tasks)
        else:
            raise TypeError("Tasks must be a DataFrame or a list.")

    def reset_visualization(self):
        """
        Resets the visualization state in Streamlit.
        """
        if 'chart_data' in st.session_state:
            st.session_state['chart_data'] = None