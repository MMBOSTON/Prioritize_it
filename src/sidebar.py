# sidebar.py
import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.instructions import get_instructions

def display_sidebar(prioritize, session_state):
    st.sidebar.title('Task Prioritizer')
    st.sidebar.markdown(get_instructions())

    # Place the "Generate Report" button in the sidebar
    if st.sidebar.button('Generate Report'):
        report = prioritize.generate_report()
        session_state['report'] = report # Corrected access

    # Place the "Visualize Tasks" button in the sidebar
    if st.sidebar.button('Visualize Tasks'):
        session_state['visualize'] = True # Corrected access