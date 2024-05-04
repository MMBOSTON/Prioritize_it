###TODO: Readin the json and constuct the dataframe....  dipslay the dataframe in the app itable grid.

# main.py
import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.sidebar import display_sidebar
from src.data_manager import reset_tasks

# Initialize session state
if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {
        'report': None,
        'visualize': False
    }

# Create an instance of PrioritizeIt
prioritize = PrioritizeIt()

# Display sidebar content
display_sidebar(prioritize, st.session_state['session_state'])

# Add task form
st.subheader('Add a new task')
description = st.text_area('Description', height=200)
value = st.number_input('Value', min_value=0)
effort = st.number_input('Effort', min_value=0)

# Create two columns for the buttons
col1, col2 = st.columns(2)

# Place the "Add Task" button in the first column
with col1:
    if st.button('Add Task'):
        prioritize.add_task(description, value, effort)

# Place the "Reset Tasks" button in the second column
with col2:
    if st.button('Reset Tasks'):
        reset_tasks()
        st.rerun() # Rerun the app to reflect the changes

# Display report if generated
if st.session_state['session_state']['report']:
    st.write(st.session_state['session_state']['report'])

# Display figures if visualize is True
if st.session_state['session_state']['visualize']:
    tasks = prioritize.view_tasks()
    pareto_chart, burndown_chart = prioritize.visualize_tasks(tasks)
    st.pyplot(pareto_chart)
    st.pyplot(burndown_chart)

# Display tasks
st.subheader('View tasks')
st.markdown("---") # Add a horizontal line for better visibility
tasks = prioritize.view_tasks()
if tasks:
    # Sort tasks by value-to-effort ratio
    tasks.sort(key=lambda task: task.ratio, reverse=True)
    for task in tasks:
        st.write(f"Task: {task.description}, Value: {task.value}, Effort: {task.effort}, Ratio: {task.ratio}")
else:
    st.write("No tasks added yet.")