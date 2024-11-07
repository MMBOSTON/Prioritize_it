"""
Filename: sidebar.py
Updated_By: Rich Lysakowski
Updated_On: 2024.08.09

Module to handle the sidebar interface interactions in the Streamlit app, including 
workflow selection, instructions display, file conversion options, and interactive debugging settings. 
Integrates with the main application to manage user inputs and preferences from the sidebar.

Functions:
    run_tests: Executes unit tests for the application.
    display_sidebar: Displays sidebar components and manages user interactions for task list operations and settings.
"""

import subprocess
import streamlit as st
from src.instructions import instructions
from input_proc.grid_config import display_grid  # Adjust this import based on actual usage
from input_proc.input_proc import InputProc

def run_tests():
    """
    Executes unit tests for the application.

    Runs unittests for the application and returns the stdout of the test execution command.

    Returns:
        str: The output of the unittest command.
    """
    command = "python -m unittest tests.test_task"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout

def display_sidebar(task_list):
    """
    Displays sidebar components and manages user interactions related to task list operations and settings.

    Args:
        task_list: A list of tasks to be displayed and managed in the sidebar.

    Side effects:
        Modifies the Streamlit sidebar with widgets for workflow selection, instructions display, 
        file conversion options, and interactive debugging settings.
    """
    if st.sidebar.button('Reset app'):
        st.experimental_rerun()

    section = st.sidebar.selectbox(
        'Select a Workflow',
        ('Spreadsheet Data Analyzer', 'Manual Task Analyzer', 'Demo Data Analyzer'),
        key='workflow_select'  # Unique key
    )
    st.sidebar.markdown("---")  # Horizontal line
    InputProc(task_list, section)

    st.sidebar.markdown("## Instructions")
    show_instructions = st.sidebar.checkbox('Show Instructions', key='show_instructions')
    if show_instructions:
        st.sidebar.write(instructions)
    st.sidebar.markdown("---")  # Horizontal line

    st.sidebar.markdown("## File Conversion")
    file_conversion = st.sidebar.button("Convert JSON to TXT and CSV")
    if file_conversion:
        pass  # Placeholder for file conversion logic
    st.sidebar.markdown("---")  # Horizontal line

    interactive_debug = st.sidebar.checkbox('Interactive Debug', key='interactive_debug')
    display_grid(interactive_debug)
    st.sidebar.markdown("---")  # Horizontal line