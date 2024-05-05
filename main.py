###TODO: Readin the json and constuct the dataframe....  dipslay the dataframe in the app itable grid.

import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.sidebar import display_sidebar, handle_form
from src.data_manager import reset_tasks

# Display the title with smaller font
st.markdown("<h1 style='text-align: center; color: White;font-size: 26px;'>★ PRIORITIZE IT! ★&nbsp;&nbsp;&nbsp;PARETO PILOT App</h1>", unsafe_allow_html=True)

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
st.markdown("<h2 style='font-size: 20px;'>Add a new task</h2>", unsafe_allow_html=True)
##add_task_clicked, reset_tasks_clicked = display_sidebar.handle_form(prioritize)
add_task_clicked, reset_tasks_clicked = handle_form(prioritize)

# Display report if generated
if st.session_state['session_state']['report']:
    st.write(st.session_state['session_state']['report'])

# Display tasks
st.markdown("<h2 style='font-size: 20px;'>View Tasks</h2>", unsafe_allow_html=True)
st.markdown("---") # Add a horizontal line for better visibility
task_strings = prioritize.get_task_string()
for task_string in task_strings:
    st.write(task_string)

# Display figures if visualize is True
if st.session_state['session_state']['visualize']:
    tasks = prioritize.view_tasks()
    pareto_chart, burndown_chart = prioritize.visualize_tasks(tasks)
    st.pyplot(pareto_chart)
    st.pyplot(burndown_chart)