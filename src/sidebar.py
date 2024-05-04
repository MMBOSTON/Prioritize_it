import streamlit as st
from src.prioritize_it import PrioritizeIt
from src.instructions import get_instructions

def display_sidebar(prioritize):
    st.sidebar.title('Task Prioritizer')
    st.sidebar.markdown(get_instructions())

    # Create two columns for the buttons in the sidebar
    col1, col2 = st.sidebar.columns(2)

    # Place the "Generate Report" button in the first column
    with col1:
        if st.button('Generate Report'):
            report = prioritize.generate_report()
            st.sidebar.write(report)

    # Place the "Visualize Tasks" button in the second column
    with col2:
        if st.button('Visualize Tasks'):
            tasks = prioritize.view_tasks()
            pareto_chart, burndown_chart = prioritize.visualize_tasks(tasks)
            st.sidebar.pyplot(pareto_chart)
            st.sidebar.pyplot(burndown_chart)