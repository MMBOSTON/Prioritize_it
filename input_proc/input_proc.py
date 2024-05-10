import json
import os
import sys

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from src.task import Task
from src.visualizer import Visualizer

from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_core_tasks, save_tasks_to_json
from .grid_config import data  # Make sure to import data
from .grid_config import custom_buttons, gridOptions  # Added data here


def display_tasks_with_aggrid(tasks):
    grid_response = AgGrid(tasks, gridOptions=gridOptions, height=800, key="grid0", editable=True, suppressMovableColumns=True, filter=True, sortable=False, autoSizeStrategy=dict(type="fitGridWidth"), pagination=True)
    return grid_response

def display_tasks_with_st_table(tasks):
    st.table(data)

def InputProc():
    visualizer = Visualizer()
    tasks = []

    with st.expander("Task Management"):
        col1, col2 = st.columns(2)

        # Option to generate core tasks
        with col1:
            if st.button("Generate Core Tasks"):
                tasks = generate_core_tasks()
                save_tasks_to_json(tasks)
                st.success("Core tasks generated and saved.")

        # Option to delete core tasks
        with col2:
            if st.button("Delete Core Tasks"):
                try:
                    os.remove('data/core_tasks.json')
                    st.success("Core tasks deleted.")
                except FileNotFoundError:
                    st.warning("No tasks found to delete.")
                tasks = []

        # Load tasks from JSON or use sample data
        try:
            with open('data/core_tasks.json', 'r') as f:
                task_dicts = json.load(f)
                for task_dict in task_dicts:
                    task_dict['value'] = task_dict.pop('task_value')
                tasks = [Task(description=task_dict['description'], value=task_dict['value'], effort=task_dict['task_effort'], id=task_dict['task_id'], name=task_dict['name']) for task_dict in task_dicts]
        except FileNotFoundError:
            st.warning("No tasks found. Generate some or use sample data.")
        except json.JSONDecodeError:
            st.error("Failed to decode JSON file. Please check the file content.")
        except KeyError as e:
            st.error(f"Failed to create tasks. Missing key in dictionary: {e}")

    # Display the tasks with ag-grid or st.table based on user's choice
    use_ag_grid = st.checkbox('Use AgGrid')
    if use_ag_grid:
        grid_response = display_tasks_with_aggrid(tasks)
    else:
        display_tasks_with_st_table(tasks)

    # Get selected row numbers from pull-down menu
    selected_row_numbers = st.multiselect("Select tasks", list(range(len(tasks))))

    # Get selected tasks
    selected_tasks = [tasks[i] for i in selected_row_numbers]

    # Create two columns for the buttons
    col1, col2, col3, col4 = st.columns(4)
    
    # Option to visualize tasks
    with col1:
        visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_input_proc")
    
    # Option to generate report
    with col4:
        generate_report = st.button("Generate Report", key="generate_report_input_proc")

    # Check if the "Visualize Tasks" button was pressed
    if visualize_tasks:
        # Check if there are selected tasks
        if selected_tasks:
            # Calculate ratio for each task
            for task in selected_tasks:
                task.calculate_ratio()
    
            # Plot Pareto chart and burndown chart for selected tasks
            pareto_chart = visualizer.plot_pareto(selected_tasks)
            st.pyplot(pareto_chart)
    
            burndown_chart = visualizer.plot_burndown(selected_tasks)
            st.pyplot(burndown_chart)
        else:
            st.warning("No tasks selected for visualization.")

    # Check if the "Generate Report" button was pressed
    if generate_report:
        # Check if there are selected tasks
        if selected_tasks:
            # Generate report for each task
            for task in selected_tasks:
                task.generate_report()
        else:
            st.warning("No tasks selected for report generation.")