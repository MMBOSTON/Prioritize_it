import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List
from src.task import Task
import streamlit as st

class Visualizer:
    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks: List[str], ratios: List[float]) -> plt.Figure:
        if not tasks:
            st.warning("No tasks to visualize.")
            return None

        fig, ax = plt.subplots(figsize=(15, 15))
        ax.bar(tasks, ratios, color='blue')
        ax.set_xlabel('Tasks', fontsize=12)
        ax.set_ylabel('Value/Effort Ratio', fontsize=12)
        ax.set_title('Pareto Chart', fontsize=14)
        ax.grid(True)
        return fig

    def plot_burndown(self, tasks: List[str], cumulative_value: List[float]) -> plt.Figure:
        if not tasks:
            st.warning("No tasks to visualize.")
            return None

        fig, ax = plt.subplots(figsize=(15, 15))
        ax.plot(range(1, len(tasks) + 1), cumulative_value, marker='o')
        ax.set_xlabel('Tasks Completed', fontsize=12)
        ax.set_ylabel('Total Value Delivered', fontsize=12)
        ax.set_title('Value Burndown Chart', fontsize=14)
        ax.grid(True)
        return fig

    def plot_combined(self, tasks: List[str], ratios: List[float], cumulative_value: List[float]) -> plt.Figure:
        if not tasks:
            st.warning("No tasks to visualize.")
            return None
    
        fig, ax1 = plt.subplots(figsize=(15, 15))
    
        # Plot Pareto Chart
        color = 'tab:blue'
        ax1.set_xlabel('Tasks', fontsize=12)
        ax1.set_ylabel('Value/Effort Ratio', color=color, fontsize=12)
        ax1.bar(tasks, ratios, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
    
        # Instantiate a second axes that shares the same x-axis
        ax2 = ax1.twinx()
    
        # Plot Burndown curve
        color = 'tab:red'
        ax2.set_ylabel('Total Value Delivered', color=color, fontsize=12)  # we already handled the x-label with ax1
        ax2.plot(range(1, len(tasks) + 1), cumulative_value, color=color, marker='o')
        ax2.tick_params(axis='y', labelcolor=color)
    
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        ax1.grid(True)
        return fig
    
    def plot_cumulative_effort(self, tasks: List[str], cumulative_effort: List[float]) -> plt.Figure:
        if not tasks:
            st.warning("No tasks to visualize.")
            return None

        fig, ax = plt.subplots(figsize=(15, 15))
        ax.plot(range(1, len(tasks) + 1), cumulative_effort, marker='o')
        ax.set_xlabel('Tasks Completed', fontsize=12)
        ax.set_ylabel('Total Effort Expended', fontsize=12)
        ax.set_title('Cumulative Effort Curve', fontsize=14)
        ax.grid(True)
        return fig

    def visualize_tasks_from_df(self, tasks_df: pd.DataFrame):
        if tasks_df.empty:
            st.warning("No tasks to visualize.")
            return
    
        tasks = tasks_df['name'].tolist()
        values = tasks_df['task_value'].tolist()
        efforts = tasks_df['task_effort'].tolist()
        ratios = [v / e for v, e in zip(values, efforts)]
        tasks_df['ratio'] = ratios
        tasks_df['Rank'] = tasks_df['ratio'].rank(ascending=False)
        tasks_df.sort_values('Rank', inplace=True)
        tasks = tasks_df['name'].tolist()
        values = tasks_df['task_value'].tolist()
        efforts = tasks_df['task_effort'].tolist()
        ratios = tasks_df['ratio'].tolist()
        cumulative_value = [sum(values[:i+1]) for i in range(len(values))]
        cumulative_effort = [sum(efforts[:i+1]) for i in range(len(efforts))]
    
        combined_chart = self.plot_combined(tasks, ratios, cumulative_value)
        st.pyplot(combined_chart)
        cumulative_effort_chart = self.plot_cumulative_effort(tasks, cumulative_effort)
        st.pyplot(cumulative_effort_chart)
    
    def visualize_tasks_from_list(self, tasks: List[Task]):
        if not tasks:
            st.warning("No tasks to visualize.")
            return
    
        task_names = [task.name for task in tasks]
        values = [task.value for task in tasks]
        efforts = [task.effort for task in tasks]
        ratios = [v / e for v, e in zip(values, efforts)]
        tasks, ratios = zip(*sorted(zip(task_names, ratios), key=lambda x: x[1], reverse=True))
        cumulative_value = [sum(ratios[:i+1]) for i in range(len(ratios))]
        cumulative_effort = [sum(efforts[:i+1]) for i in range(len(efforts))]
    
        combined_chart = self.plot_combined(tasks, ratios, cumulative_value)
        st.pyplot(combined_chart)
        cumulative_effort_chart = self.plot_cumulative_effort(tasks, cumulative_effort)
        st.pyplot(cumulative_effort_chart)

    def visualize_tasks(self, tasks):
        if isinstance(tasks, pd.DataFrame):
            self.visualize_tasks_from_df(tasks)
        elif isinstance(tasks, list):
            self.visualize_tasks_from_list(tasks)
        else:
            raise TypeError("Tasks must be a DataFrame or a list.")

    def reset_visualization(self):
        if 'chart_data' in st.session_state:
            st.session_state['chart_data'] = None