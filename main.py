import sys
import os
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st

from src.tasklist import TaskList
from input_proc.input_proc import InputProc
from src.sidebar import display_sidebar, handle_form
from src.instructions import get_instructions  # Import the get_instructions function
from src.report_generator import ReportGenerator

# Insert the path to the Prioritize_it directory at the beginning of the system path
sys.path.insert(0, os.path.join(os.environ['USERPROFILE'], 'Documents', 'GitHub', 'Prioritize_it'))

# Display the title with smaller font
st.markdown("<h1 style='text-align: center; color: DarkGray;font-size: 26px;'>★★ !!PRIORITIZE IT!! ★★</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: DarkGray;font-size: 18px;'>A PARETO PILOT APP FOR PROJECT MANAGERS</h2>", unsafe_allow_html=True)

# Initialize session state
if 'Report' not in st.session_state:
    st.session_state['Report'] = None
if 'visualize' not in st.session_state:
    st.session_state['visualize'] = False
if 'selected_section' not in st.session_state:
    st.session_state['selected_section'] = None

# Create an instance of TaskList
task_list = TaskList()
input_proc = InputProc(task_list)
selected_section = display_sidebar(task_list)

# Display sidebar content
st.session_state['selected_section'] = display_sidebar(task_list) # Capture the returned selected_section

# Call the InputProc function to display the "Spreadsheet Data Analyzer" and "Task Management" sections
task_list.use_input_proc()

# Initialize task_description at the beginning of your script
task_description = ""

# Add task form
st.markdown("<h2 style='font-size: 20px;'>Add a new task</h2>", unsafe_allow_html=True)
add_task_clicked, remove_task_clicked, reset_tasks_clicked = handle_form(task_list)

# If add_task_clicked is True, add a new task
if add_task_clicked:
    value = st.number_input("Value")
    effort = st.number_input("Effort")
    task_list.add_task(task_description, value, effort)

# If remove_task_clicked is True, remove a specific task
if remove_task_clicked:
    task_description = st.text_input("Enter the description of the task to remove:")
    task_list.remove_task(task_description)

# If reset_tasks_clicked is True, reset tasks
if reset_tasks_clicked:
    task_list.reset_tasks()
    st.markdown("<h2 style='font-size: 20px;'>Tasks have been reset. Please refresh the page to see the changes.</h2>", unsafe_allow_html=True)

# Add a button to generate a report
if st.button('Generate Report', key='generate_report_button'):
    try:
        report_generator = ReportGenerator(task_list)
        st.session_state['Report'] = report_generator.generate_report()

        # Write the report to a file
        print(f"Report: {st.session_state['Report']}")  # Print the report
        report_folder = 'Report'
        report_filename = os.path.join(report_folder, 'report.txt')
        print(f"Current working directory: {os.getcwd()}")  # Print the current working directory
        print(f"Report file path: {report_filename}")  # Print the report file path
        os.makedirs(report_folder, exist_ok=True)
        with open(report_filename, 'w') as f:
            f.write(st.session_state['Report'])
        print("Report written to file")  # Print a message after the report is written to the file
    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"Exception: {e}")  # Print the exception

# Display Report if generated
if st.session_state['Report']:
    # Use st.text instead of st.write to preserve line breaks
    st.text(st.session_state['Report'])

# Display tasks
st.markdown("<h2 style='font-size: 20px;'>View Tasks</h2>", unsafe_allow_html=True)
st.markdown("---") # Add a horizontal line for better visibility
task_strings = task_list.get_task_string()
for task_string in task_strings:
    st.markdown(task_string, unsafe_allow_html=True)

# Display figures if visualize is True
if st.session_state['visualize']:
    tasks = task_list.view_tasks()
    pareto_chart, burndown_chart = task_list.visualize_tasks(tasks)
    st.pyplot(pareto_chart)
    st.pyplot(burndown_chart)