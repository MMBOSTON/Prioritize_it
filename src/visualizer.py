import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self):
        sns.set()

    def plot_pareto(self, tasks):
        # Sort tasks by ratio, treating None as the lowest possible value
        tasks.sort(key=lambda x: x.ratio if x.ratio is not None else -float('inf'), reverse=True)
        values = [task.value for task in tasks]
        labels = [task.description for task in tasks]
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel('Tasks')
        ax.set_ylabel('Value/Effort Ratio')
        ax.set_title('Pareto Chart')
        return fig

    def plot_burndown(self, tasks):
        # Sort tasks by ratio, treating None as the lowest possible value
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
        # Clear any chart data stored in the session state
        if 'chart_data' in st.session_state:
            st.session_state['chart_data'] = None