import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

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

        # Convert the figure to a PNG image
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')

        # Create a scrollable div to display the chart
        st.markdown(f"""
            <div style="height:400px; overflow-y:auto; border:1px solid #ddd; padding:10px;">
                <img src="data:image/png;base64,{img_str}" style="width:100%;">
            </div>
        """, unsafe_allow_html=True)

        return fig

    # Other methods...

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