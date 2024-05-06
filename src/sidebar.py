import os
import shutil
import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.instructions import get_instructions


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

    # # Custom layout for buttons using markdown and HTML
    # st.sidebar.markdown("""
    # <div style="display: flex; justify-content: space-between;">
    #     <button style="margin-right: 10px;" onclick="location.href='#GenerateReport'">Generate Report</button>
    #     <button style="margin-right: 10px;" onclick="location.href='#VisualizeTasks'">Visualize Tasks</button>
    #     <button onclick="location.href='#RemoveAllTasks'">Remove All Tasks</button>
    # </div>
    # """, unsafe_allow_html=True)

    # Place the "Generate Report" button logic
    if st.sidebar.button('Generate Report'):
        Report = prioritize.generate_Report()
        st.session_state['Report'] = Report
        st.sidebar.success("Report generated successfully! Check the 'Report' folder.")

    # Place the "Visualize Tasks" button logic
    if st.sidebar.button('Visualize Tasks'):
        st.session_state['visualize'] = True

    # Place the "Remove All Tasks" button logic
    if st.sidebar.button('Remove All Tasks'):
        st.session_state['remove_all_tasks_clicked'] = True
    else:
        st.session_state['remove_all_tasks_clicked'] = False

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
        prioritize.remove_a_task(description)

    if reset_tasks_button:
        # This part is already handled in the display_sidebar function for the sidebar
        pass

    return add_task_button, remove_task_button, reset_tasks_button

