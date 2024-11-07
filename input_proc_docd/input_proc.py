"""
Module for processing input data, including displaying tasks with AgGrid and saving updated tasks to files.

This module provides functionality for displaying tasks using the AgGrid interactive grid, saving updated tasks to JSON and CSV files, and handling input from various workflows such as spreadsheet data analysis, manual task entry, and demo data analysis.
"""

import json, os
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
import csv

from src.task import Task
from src.visualizer import Visualizer
from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_demo_tasks, save_tasks_to_json_and_csv
from .grid_config import data  # Make sure to import data
from .grid_config import custom_buttons, gridOptions  # Added data here
from src.file_handler import FileHandler

def save_updated_tasks_to_file(tasks):
    """
    Saves updated tasks to JSON and CSV files.

    Args:
        tasks (list): A list of task dictionaries to save.
    """
    try:
        with open('data/Updated_Tasks.json', 'w') as f:
            json.dump(tasks, f)
        with open('data/Updated_Tasks.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
            writer.writeheader()
            writer.writerows(tasks)
    except PermissionError:
        st.error("Please close 'Updated_Tasks.json' and 'Updated_Tasks.csv' before saving.")
        return False
    return True

def display_tasks_with_aggrid(tasks):
    """
    Displays tasks using the AgGrid interactive grid.

    Args:
        tasks (list): A list of task dictionaries to display.

    Returns:
        The grid response from AgGrid.
    """
    grid_response = AgGrid(
        tasks, 
        gridOptions=gridOptions, 
        height=800, 
        key="grid0", 
        editable=True, 
        suppressMovableColumns=True, 
        filter=True, 
        sortable=False, 
        autoSizeStrategy=dict(type="fitGridWidth"), 
        pagination=True
    )
    return grid_response

def display_tasks_with_st_table(tasks):
    """
    Displays tasks using Streamlit's table widget.

    Args:
        tasks (list): A list of Task objects to display.
    """
    task_dicts = [task.__dict__ for task in tasks]
    task_df = pd.DataFrame(task_dicts)
    st.table(task_df)

# TODO: MOHAMMAD OR RICH: 
# THIS FUNCTION InputProc() SEEMS TOO LONG AND COMPLEX. CONSIDER REFACTORING INTO SMALLER FUNCTIONS.
def InputProc(task_list, section):
    """
    Handles input processing based on the selected workflow section.

    Args:
        task_list (TaskList): The task list to manage.
        section (str): The selected workflow section.
    """
    visualizer = Visualizer()
    tasks = []

    if section == 'Spreadsheet Data Analyzer':
        grid_response = display_tasks_with_aggrid(tasks)
        selected_tasks = grid_response['selected_rows']
        col1, col2, col3 = st.columns(3)
        with col1:
            save_tasks = st.button("Save Updated Tasks", key="save_tasks_aggrid")
            if save_tasks:
                if selected_tasks is not None:
                    success = save_updated_tasks_to_file(selected_tasks.to_dict('records'))
                    if success:
                        st.success("Tasks saved successfully.")
                else:
                    st.warning("No tasks selected for saving.")
        with col2:
            visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_aggrid")
        with col3:
            generate_report = st.button("Generate Report", key="generate_report_aggrid")
        if visualize_tasks:
            if not selected_tasks.empty:
                selected_tasks['ratio'] = selected_tasks.apply(lambda row: row['task_value'] / row['task_effort'], axis=1)
                visualizer.visualize_tasks(selected_tasks)
            else:
                st.warning("No tasks selected for visualization.")
        if generate_report:
            if not selected_tasks.empty:
                for index, task in selected_tasks.iterrows():
                    # Add your code to generate a report for each task here
                    pass
            else:
                st.warning("No tasks selected for report generation.")
    elif section == 'Manual Task Analyzer':
        description = st.text_area("Task Description", height=100)
        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input("Task Value")
        with col2:
            effort = st.number_input("Task Effort")
        col3, col4, col5 = st.columns(3)
        with col3:
            add_task_button = st.button("Add Task")
        with col4:
            remove_task_button = st.button("Remove A Task")
        with col5:
            reset_tasks_button = st.button("Reset Tasks")
        if add_task_button:
            task_list.add_task(description, value, effort)
        if remove_task_button:
            task_list.remove_task(description)
    elif section == 'Demo Data Analyzer':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Demo Tasks"):
                tasks = generate_demo_tasks()
                save_tasks_to_json_and_csv(tasks)
                st.success("Demo tasks generated and saved.")
        with col2:
            if st.button("Delete Demo Tasks"):
                try:
                    os.remove('data/demo_tasks.json')
                    st.success("Demo tasks deleted.")
                except FileNotFoundError:
                    st.warning("No tasks found to delete.")
        try:
            with open('data/demo_tasks.json', 'r') as f:
                task_dicts = json.load(f)
                for task_dict in task_dicts:
                    task_dict['value'] = task_dict.pop('task_value')
                tasks = [Task(description=task_dict['description'], value=task_dict['value'], effort=task_dict['task_effort'], id=task_dict['task_id'], name=task_dict['name']) for task_dict in task_dicts]
        except FileNotFoundError:
            tasks = []
        except json.JSONDecodeError:
            st.error("Failed to decode JSON file. Please check the file content.")
        except KeyError as e:
            st.error(f"Failed to create tasks. Missing key in dictionary: {e}")
        if tasks:
            display_tasks_with_st_table(tasks)
            selected_task_indices = st.multiselect("Select Tasks", options=range(len(tasks)))
            selected_task_objects = [tasks[i] for i in selected_task_indices]
        else:
            st.warning("No tasks found. Generate some or use sample data.")
        if st.button("Visualize Demo Tasks"):
            if selected_task_objects:
                visualizer.visualize_tasks(selected_task_objects)
            else:
                st.warning("No tasks selected for visualization.")