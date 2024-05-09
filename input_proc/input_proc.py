import json
import pandas as pd
import streamlit as st
from src.task import Task  # Import the Task class
from src.visualizer import Visualizer
from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_core_tasks, save_tasks_to_json
import os

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

        # Display tasks and allow selection
        selected_task_ids = create_interactive_table(tasks)
        selected_tasks = [task for task in tasks if task.id in selected_task_ids]

    # Convert list of Task objects to a DataFrame
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

    # Create a DataFrame directly from the list of Task objects
    tasks_df = pd.DataFrame([task.__dict__ for task in tasks])

    # Create a collapsible section for the table
    with st.expander("View Tasks Table"):
        # Display the DataFrame as a table in Streamlit
        st.table(tasks_df)

    # Option to visualize tasks
    if st.button("Visualize Tasks", key="visualize_tasks_input_proc"):
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