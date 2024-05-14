import json, os
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from src.task import Task
from src.visualizer import Visualizer

from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_core_tasks, save_tasks_to_json
from .grid_config import data  # Make sure to import data
from .grid_config import custom_buttons, gridOptions  # Added data here
from src.file_handler import FileHandler

def display_tasks_with_aggrid(tasks):
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
    st.table(data)

def InputProc(task_list):
    visualizer = Visualizer()
    tasks = []

    with st.expander("Spreadsheet Data Analyzer"):
        grid_response = display_tasks_with_aggrid(tasks)
        selected_tasks = grid_response['selected_rows']
    
        col1, col2 = st.columns(2)
    
        with col1:
            visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_aggrid")
    
        with col2:
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

    with st.expander("Task Management"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate Core Tasks"):
                tasks = generate_core_tasks()
                save_tasks_to_json(tasks)
                st.success("Core tasks generated and saved.")

        with col2:
            if st.button("Delete Core Tasks"):
                try:
                    os.remove('data/core_tasks.json')
                    st.success("Core tasks deleted.")
                except FileNotFoundError:
                    st.warning("No tasks found to delete.")

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

        if tasks:
            display_tasks_with_st_table(tasks)

        selected_row_numbers = st.multiselect("Select tasks", list(range(len(tasks))))
        selected_tasks = [tasks[i] for i in selected_row_numbers]

        col1, col2 = st.columns(2)

        with col1:
            visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_input_proc")

        with col2:
            generate_report = st.button("Generate Report", key="generate_report_input_proc")

        if visualize_tasks:
            if selected_tasks:
                for task in selected_tasks:
                    task.calculate_ratio()
                visualizer.visualize_tasks(selected_tasks)
            else:
                st.warning("No tasks selected for visualization.")

        if generate_report:
            if selected_tasks:
                for task in selected_tasks:
                    task.generate_report()
            else:
                st.warning("No tasks selected for report generation.")

    with st.expander("File Upload"):
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "text", "xlsx"])    
        if uploaded_file is not None:
            file_handler = FileHandler(task_list)
            tasks = file_handler.load_tasks_from_file(uploaded_file)
            st.success("Tasks loaded from file.")
    
        col1, col2 = st.columns(2)
    
        with col1:
            visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_file_upload")
    
        with col2:
            generate_report = st.button("Generate Report", key="generate_report_file_upload")
    
        if visualize_tasks:
            if tasks:
                for task in tasks:
                    task.calculate_ratio()
                visualizer.visualize_tasks(tasks)
            else:
                st.warning("No tasks loaded for visualization.")
    
        if generate_report:
            if tasks:
                for task in tasks:
                    task.generate_report()
            else:
                st.warning("No tasks loaded for report generation.")