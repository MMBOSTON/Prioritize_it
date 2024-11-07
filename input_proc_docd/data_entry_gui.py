"""
Provides GUI components for data entry and selection.

Functions to display tasks in an interactive table format and select tasks in a Streamlit interface. 
It leverages pandas for data manipulation and Streamlit for UI components.

Functions:
- get_selected_tasks():       Filters selected tasks from the dataset.
- create_interactive_table(): Creates an interactive table for task selection.
"""

from typing import Dict, List

import pandas as pd
import streamlit as st
from itables import show

def get_selected_tasks(data: List[Dict]) -> List[Dict]:
    """
    Filters the input data to only include tasks marked as selected.

    Parameters:
    - data (List[Dict]): A list of dictionaries representing tasks, where each dictionary contains a 'selected' key indicating whether the task is selected.

    Returns:
    - List[Dict]: A list of dictionaries representing only the selected tasks.
    """
    selected_tasks = [task for task in data if task['selected']]
    return selected_tasks

def create_interactive_table(data: List[Dict]):
    """
    Creates an interactive table in Streamlit using the provided data,
    calculates a rank for each task based on its value and effort,
    and allows users to select tasks through a multiselect widget.

    Parameters:
    - data (List[Dict]): A list of dictionaries representing tasks, where each dictionary should contain keys for 'name', 'description', 'task_value', 'task_effort', and optionally 'selected'.

    Returns:
    - dict: The data converted back to a list of dictionaries after interaction, including selections made by the user.
    """
    df = pd.DataFrame(data)
    df['Rank'] = df['task_value'] / df['task_effort'] * df['ratio']
    st.dataframe(df)
    st.write("Select tasks:")
    selected_tasks = st.multiselect("Select tasks", df.index, key='selected_tasks')
    return df.to_dict('records')  # Convert the DataFrame back to a list of dictionaries

# Example usage
if __name__ == "__main__":
    """
    Demonstrates the use of get_selected_tasks and create_interactive_table functions
    with sample data.
    """
    # Assuming data is loaded from JSON or generated
    data = [{'name': 'Task 1', 'description': 'Description 1', 'selected': False},
            {'name': 'Task 2', 'description': 'Description 2', 'selected': True}]
    selected_tasks = create_interactive_table(data)
    st.write(selected_tasks)