import json
import pandas as pd
import streamlit as st
from src.task import Task  # Import the Task class
from src.visualizer import Visualizer
from .data_entry_gui import create_interactive_table
from .generate_tasks import generate_core_tasks, save_tasks_to_json


def InputProc():
    visualizer = Visualizer()

    with st.expander("Task Management"):
        # Option to generate core tasks
        if st.button("Generate Core Tasks"):
            tasks = generate_core_tasks()
            save_tasks_to_json(tasks)
            st.success("Core tasks generated and saved.")

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

        # Check if the tasks list is empty
        if tasks:
            # If the list is not empty, access its elements
            first_task = tasks[0]
            print(f"Task: {first_task}")
            print(f"Name: {first_task.name}")
            print(f"Description: {first_task.description}")
            print(f"Value: {first_task.value}")
            print(f"Effort: {first_task.effort}")
            print(f"ID: {first_task.id}")
        else:
            # If the list is empty, print an error message or handle the error in some other way
            print("Error: The tasks list is empty.")

        # Create a DataFrame directly from the list of Task objects
        tasks_df = pd.DataFrame([task.__dict__ for task in tasks])

        # Print out the DataFrame to the console
        print(tasks_df)

    # Create a collapsible section for the table
    with st.expander("View Tasks Table"):
        # Display the DataFrame as a table in Streamlit
        st.table(tasks_df)

    # Plot Pareto chart and burndown chart for selected tasks
    if selected_tasks:
        pareto_chart = visualizer.plot_pareto(selected_tasks)
        st.pyplot(pareto_chart)

        burndown_chart = visualizer.plot_burndown(selected_tasks)
        st.pyplot(burndown_chart)