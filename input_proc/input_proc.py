import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now you can import using absolute imports from the project root
from src.task import Task
from src.visualizer import Visualizer

# Continue with the rest of your imports and code

import json
import pandas as pd
import streamlit as st

from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_core_tasks, save_tasks_to_json
from st_aggrid import AgGrid

# def display_tasks_with_aggrid(tasks):
#     task_dicts = [
#         {
#             "Name": task.name,
#             "Description": task.description,
#             "Value": task.value,
#             "Effort": task.effort,
#             "ID": task.id,
#         }
#         for task in tasks
#     ]

#     gridOptions = {
#         'enableSorting': True,
#         'enableFilter': False,
#         #'rowSelection': 'multiple',  # Enable multiple row selection
#         'defaultColDef': {
#             'sortable': True,
#             'filter': False,
#             'resizable': True,
#             'width': 100,
#         },
#         'columnDefs': [
#             {'headerName': "Task Name", 'field': "Name", 'width': 150},
#             {'headerName': "Task Description", 'field': "Description", 'width': 300},
#             {'headerName': "Task Value", 'field': "Value", 'width': 100, 'cellRenderer': 'agProgressBarCellRenderer'},
#             {'headerName': "Task Effort", 'field': "Effort", 'width': 100},
#             {'headerName': "Task ID", 'field': "ID", 'width': 100, 'resizable': False},
#         ],
#         'getRowStyle': lambda params: {'background-color': '#f4f4f4'} if params.node.rowIndex % 2 else {}
#     }

#     response = AgGrid(pd.DataFrame(task_dicts), gridOptions=gridOptions, return_mode='AS_INPUT', update_mode='VALUE_CHANGED')

#     selected_rows = response['selected_rows']
#     return selected_rows

def display_tasks_with_aggrid(tasks):
    task_dicts = [
        {
            "Name": task.name,
            "Description": task.description,
            "Value": task.value,
            "Effort": task.effort,
            "ID": task.id,
        }
        for task in tasks
    ]

    response = AgGrid(pd.DataFrame(task_dicts), return_mode='AS_INPUT', update_mode='VALUE_CHANGED')

    selected_rows = response['selected_rows']
    return selected_rows

def display_tasks_with_st_table(tasks):
    task_dicts = [
        {
            "Name": task.name,
            "Description": task.description,
            "Value": task.value,
            "Effort": task.effort,
            "ID": task.id,
        }
        for task in tasks
    ]

    st.table(pd.DataFrame(task_dicts))

def InputProc():
    visualizer = Visualizer()

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
            tasks = []
        except json.JSONDecodeError:
            st.error("Failed to decode JSON file. Please check the file content.")
            tasks = []
        except KeyError as e:
            st.error(f"Failed to create tasks. Missing key in dictionary: {e}")
            tasks = []

    # Display the tasks with ag-grid or st.table based on user's choice
    use_ag_grid = st.checkbox('Use AgGrid')
    if use_ag_grid:
        selected_rows = display_tasks_with_aggrid(tasks)
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