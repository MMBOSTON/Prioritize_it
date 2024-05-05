import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.instructions import get_instructions
##from src.data_manager import reset_tasks

def display_sidebar(prioritize):
    st.sidebar.title('Task Prioritizer')
    st.sidebar.markdown(get_instructions())

    # Create two columns in the sidebar
    col1, col2 = st.sidebar.columns(2)

    # Place the "Generate Report" button in the first column
    with col1:
        if st.button('Generate Report'):
            report = prioritize.generate_report()
            st.session_state['report'] = report

    # Place the "Visualize Tasks" button in the second column
    with col2:
        if st.button('Visualize Tasks'):
            st.session_state['visualize'] = True

def handle_form(prioritize):
    description = st.text_area('Description', height=200)
    value = st.number_input('Value', min_value=0)
    effort = st.number_input('Effort', min_value=0)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        add_task_clicked = st.button('Add Tasks')
        if add_task_clicked:
            prioritize.add_task(description, value, effort)
    
    with col4:
        reset_tasks_clicked = st.button('Reset Tasks')

        if reset_tasks_clicked:
            prioritize.reset_tasks()
            st.session_state['report'] = None
            st.session_state['visualize'] = False
            st.rerun()
    
    return add_task_clicked, reset_tasks_clicked