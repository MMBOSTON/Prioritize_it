import os
import shutil
import streamlit as st
import subprocess
from src.prioritize_it import PrioritizeIt
from src.instructions import get_instructions

def run_tests():
    # Define the command to run the tests
    command = "python -m unittest tests.test_task"
    
    # Run the command in a separate process and capture the output
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Return the output of the test run
    return process.stdout

def display_sidebar(prioritize):
    st.sidebar.title('Task Prioritizer')
    st.sidebar.markdown(get_instructions(), unsafe_allow_html=True)

    # Add a horizontal line
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # Add file uploader
    st.sidebar.header('Upload Tasks')
    uploaded_file = st.sidebar.file_uploader("Upload your tasks file", type=["xlsx", "docx", "csv", "txt"])
    if uploaded_file is not None:
        prioritize.load_tasks_from_file(uploaded_file)

    # Create two columns for the buttons
    col1, col2 = st.sidebar.columns(2)

    # Place the "Generate Report" button in the first column
    with col1:
        if st.button('Generate Report'):
            Report = prioritize.generate_Report()
            st.session_state['Report'] = Report
            st.success("Report generated successfully! Check the 'Report' folder.")

    # Place the "Visualize Tasks" button in the second column
    with col2:
        if st.button('Visualize Tasks'):
            st.session_state['visualize'] = True

    # Create two more columns for the next set of buttons
    col3, col4 = st.sidebar.columns(2)

    # Place the "Remove All Tasks" button in the first column
    with col3:
        if st.button('Remove All Tasks'):
            st.session_state['remove_all_tasks_clicked'] = True
        else:
            st.session_state['remove_all_tasks_clicked'] = False

    # Place the "Run Tests" button in the second column
    with col4:
        if st.button("Run Tests"):
            # Run the tests and get the output
            test_output = run_tests()
            
            # Display the test output in the main content area
            st.write("Test Output:")
            st.text(test_output)
            
            # Check if the test.log file exists
            test_log_path = "tests/test.log"
            if os.path.exists(test_log_path):
                # Display a "View Test Results" button that provides a download link
                if st.sidebar.button("View Test Results"):
                    st.sidebar.markdown(f"""
                        <a href="{test_log_path}" download>Download Test Results</a>
                    """, unsafe_allow_html=True)

    # Display the "OK" and "Cancel" buttons in the sidebar only if the "Remove All Tasks" button was clicked
    if 'remove_all_tasks_clicked' in st.session_state and st.session_state['remove_all_tasks_clicked']:
        if st.sidebar.button('OK'):
            try:
                # Remove all tasks
                prioritize.remove_all_tasks()
                # Remove the "Report" folder and all its content
                Report_folder = "Report" # Ensure this path is correct
                if os.path.exists(Report_folder):
                    shutil.rmtree(Report_folder)
                # Display a message to the user
                st.sidebar.success("All Tasks and Reports have been removed.")
            except Exception as e:
                st.sidebar.error(f"Failed to remove tasks and Reports: {e}")
        elif st.sidebar.button('Cancel'):
            # Do nothing, just cancel the operation
            pass

    return uploaded_file

def handle_form(prioritize):
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
        prioritize.add_task(description, value, effort)

    if remove_task_button:
        prioritize.remove_task(description)

    if reset_tasks_button:
        # This part is already handled in the display_sidebar function for the sidebar
        pass

    return add_task_button, remove_task_button, reset_tasks_button

