# import os
# import shutil
import subprocess
import streamlit as st
from src.instructions import instructions
# from src.tasklist import TaskList
# from src.file_handler import FileHandler
from input_proc.grid_config import display_grid  # Adjust this import based on actual usage
from input_proc.input_proc import InputProc

def run_tests():
    command = "python -m unittest tests.test_task"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout

def display_sidebar(task_list):
    # Add a "Reset app" button at the top of the sidebar
    if st.sidebar.button('Reset app'):
        st.experimental_rerun()

    section = st.sidebar.selectbox(
        'Select a Workflow',
        ('Spreadsheet Data Analyzer', 'Manual Task Analyzer', 'Demo Data Analyzer'),
        key='workflow_select'  # Unique key
    )
    # Rest of the function...
    st.sidebar.markdown("---")  # Horizontal line
    InputProc(task_list, section)

    # Section One: Instructions
    st.sidebar.markdown("## Instructions")
    show_instructions = st.sidebar.checkbox('Show Instructions', key='show_instructions')
    if show_instructions:
        # Display the instructions in the sidebar
        st.sidebar.write(instructions)
    st.sidebar.markdown("---")  # Horizontal line

    # Section Three: File Conversion
    st.sidebar.markdown("## File Conversion")
    file_conversion = st.sidebar.button("Convert JSON to TXT and CSV")
    if file_conversion:
        # Your file conversion logic here
        pass
    st.sidebar.markdown("---")  # Horizontal line

        # Add an "Interactive Debug" checkbox
    interactive_debug = st.sidebar.checkbox('Interactive Debug', key='interactive_debug')
    # Call display_grid with the debug_flag
    display_grid(interactive_debug)    
    st.sidebar.markdown("---")  # Horizontal line
