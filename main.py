import sys
sys.path.insert(0, "C:\\Users\\16175\\Documents\\GitHub\\Prioritize_it")

import os
import streamlit as st

from src.prioritize_it import PrioritizeIt

from src.report_generator import ReportGenerator
from src.sidebar import display_sidebar, handle_form

# Display the title with smaller font
st.markdown("<h1 style='text-align: center; color: White;font-size: 26px;'>★★ !!PRIORITIZE IT!! ★★</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: White;font-size: 18px;'>A PARETO PILOT APP FOR PROJECT MANAGERS</h2>", unsafe_allow_html=True)

# Initialize session state
if 'Report' not in st.session_state:
    st.session_state['Report'] = None
if 'visualize' not in st.session_state:
    st.session_state['visualize'] = False

# Create an instance of PrioritizeIt
prioritize = PrioritizeIt()

# Display sidebar content
uploaded_file = display_sidebar(prioritize) # Capture the returned uploaded_file

# Initialize task_description at the beginning of your script
task_description = ""

# Add task form
st.markdown("<h2 style='font-size: 20px;'>Add a new task</h2>", unsafe_allow_html=True)
add_task_clicked, remove_task_clicked, reset_tasks_clicked = handle_form(prioritize)

# If add_task_clicked is True, add a new task
if add_task_clicked:
    value = st.number_input("Value")
    effort = st.number_input("Effort")
    prioritize.add_task(task_description, value, effort)

# If remove_task_clicked is True, remove a specific task
if remove_task_clicked:
    task_description = st.text_input("Enter the description of the task to remove:")
    prioritize.remove_task(task_description)

# If reset_tasks_clicked is True, reset tasks
if reset_tasks_clicked:
    prioritize.reset_tasks()
    st.markdown("<h2 style='font-size: 20px;'>Tasks have been reset. Please refresh the page to see the changes.</h2>", unsafe_allow_html=True)

# Add a button to generate a report
if st.button('Generate Report', key='generate_report_button'):
    try:
        report_generator = ReportGenerator(prioritize)
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
task_strings = prioritize.get_task_string()
for task_string in task_strings:
    st.markdown(task_string, unsafe_allow_html=True)

# Display figures if visualize is True
if st.session_state['visualize']:
    tasks = prioritize.view_tasks()
    pareto_chart, burndown_chart = prioritize.visualize_tasks(tasks)
    st.pyplot(pareto_chart)
    st.pyplot(burndown_chart)

# Handle the uploaded file if it's not None
if uploaded_file is not None:
    prioritize.load_tasks_from_file(uploaded_file)