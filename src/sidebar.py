import os
import shutil
import subprocess

import streamlit as st

from src.instructions import instructions
from .tasklist import TaskList


def run_tests():
    # Define the command to run the tests
    command = "python -m unittest tests.test_task"
    
    # Run the command in a separate process and capture the output
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Return the output of the test run
    return process.stdout

def display_sidebar(tasklist):
    st.sidebar.title('Task Prioritizer')

    # Define the sections
    sections = ["AgGrid Tasks Management", "Automatic Tasks Generation","File Upload", "Manual Task Definition"]

    # Create a radio button group in the sidebar
    selected_section = st.sidebar.radio("Sections", sections)

    # Add a checkbox to show or hide the instructions
    show_instructions = st.sidebar.checkbox('Show Instructions', key='show_instructions')

    if show_instructions:
        # Display the instructions in the sidebar
        st.sidebar.write(instructions)

    if selected_section == "Manual Task Definition":
        with st.expander("Manual Task Definition"):
            # Use st.text_area for a larger, multi-line text input field for the description
            description = st.text_area("Task Description", height=100)
    
            # Create two columns for the value and effort fields with equal widths
            col1, col2 = st.columns(2)
    
            # Place the "Task Value" field in the first column
            with col1:
             value = st.number_input("Task Value")
    
            # Place the "Task Effort" field in the second column
            with col2:
                effort = st.number_input("Task Effort")
    
            # Create three columns for the buttons
            col3, col4, col5 = st.columns(3)
    
            # Place the "Add Task" button in the first column
            with col3:
                add_task_button = st.button("Add Task")
    
            # Place the "Remove A Task" button in the second column
            with col4:
                remove_task_button = st.button("Remove A Task")
    
            # Place the "Reset Tasks" button in the third column
            with col5:
                reset_tasks_button = st.button("Reset Tasks")
    
            if add_task_button:
                tasklist.add_task(description, value, effort)
    
            if remove_task_button:
                tasklist.remove_task(description)
    
            if reset_tasks_button:
                # This part is already handled in the display_sidebar function for the sidebar
                pass

    return selected_section  # Return the selected section

def handle_form(tasklist):
    # Use st.text_area for a larger, multi-line text input field for the description
    description = st.text_area("Task Description", height=100)

    # Create two columns for the value and effort fields with equal widths
    col1, col2 = st.columns(2)

    # Place the "Task Value" field in the first column
    with col1:
        value = st.number_input("Task Value")

    # Place the "Task Effort" field in the second column
    with col2:
        effort = st.number_input("Task Effort")

    # Create three columns for the buttons
    col3, col4, col5 = st.columns(3)

    # Place the "Add Task" button in the first column
    with col3:
        add_task_button = st.button("Add Task")

    # Place the "Remove A Task" button in the second column
    with col4:
        remove_task_button = st.button("Remove A Task")

    # Place the "Reset Tasks" button in the third column
    with col5:
        reset_tasks_button = st.button("Reset Tasks")

    if add_task_button:
        tasklist.add_task(description, value, effort)

    if remove_task_button:
        tasklist.remove_task(description)

    if reset_tasks_button:
        # This part is already handled in the display_sidebar function for the sidebar
        pass

    return add_task_button, remove_task_button, reset_tasks_button

