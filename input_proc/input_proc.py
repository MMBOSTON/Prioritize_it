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
    # Check if files are open
    try:
        with open('data/Updated_Tasks.json', 'a') as f:
            pass
        with open('data/Updated_Tasks.csv', 'a') as f:
            pass
    except PermissionError:
        st.error("Please close 'Updated_Tasks.json' and 'Updated_Tasks.csv' before saving.")
        return False

    # Save to JSON
    with open('data/Updated_Tasks.json', 'w') as f:
        json.dump(tasks, f)

    # Save to CSV
    with open('data/Updated_Tasks.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)

    return True

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

# def display_tasks_with_st_table(tasks):
#     st.table(data)

import pandas as pd

def display_tasks_with_st_table(tasks):
    # Convert tasks to a list of dictionaries
    task_dicts = [task.__dict__ for task in tasks]

    # Convert the list of dictionaries to a DataFrame
    task_df = pd.DataFrame(task_dicts)

    # Display the DataFrame as a table
    st.table(task_df)
    
def InputProc(task_list):
    visualizer = Visualizer()
    tasks = []

    with st.expander("Spreadsheet Data Analyzer"):
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

    with st.expander("Demo Data Analyzer"):
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
                
        if st.button("Visualize Tasks"):
            if selected_task_objects:
                visualizer.visualize_tasks(selected_task_objects)
            else:
                st.warning("No tasks selected for visualization.")

    with st.expander("File Upload"):
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "text", "xlsx"])    
        if uploaded_file is not None:
            file_handler = FileHandler(task_list)
            tasks = file_handler.load_tasks_from_file(uploaded_file)
            if tasks is not None:
                st.success("Tasks loaded from file.")
                
                # Print the tasks
                print(tasks)
                
                # Display the uploaded tasks
                st.dataframe(tasks)
        
                # Add a multi-select box for the user to select tasks for visualization
                selected_tasks = st.multiselect('Select tasks for visualization', tasks['Task Name'].tolist())    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            save_tasks = st.button("Save Updated Tasks", key="save_tasks_file_upload")
            if save_tasks:
                save_updated_tasks_to_file([task.to_dict() for task in tasks])
    
        with col2:
            visualize_tasks = st.button("Visualize Tasks", key="visualize_tasks_file_upload")
    
        with col3:
            generate_report = st.button("Generate Report", key="generate_report_file_upload")
    
        if visualize_tasks:
            if selected_tasks:
                for task in selected_tasks:
                    task.calculate_ratio()
                visualizer.visualize_tasks(selected_tasks)
            else:
                st.warning("No tasks selected for visualization.")    

        if generate_report:
            if tasks:
                for task in tasks:
                    task.generate_report()
            else:
                st.warning("No tasks loaded for report generation.")