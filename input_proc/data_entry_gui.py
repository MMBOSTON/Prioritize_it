from typing import Dict, List

import pandas as pd
import streamlit as st
from itables import show


def get_selected_tasks(data: List[Dict]) -> List[Dict]:
    selected_tasks = [task for task in data if task['selected']]
    return selected_tasks

def create_interactive_table(data: List[Dict]):
    df = pd.DataFrame(data)
    st.dataframe(df)
    st.write("Select tasks:")
    selected_tasks = st.multiselect("Select tasks", df.index, key='selected_tasks')
    return selected_tasks

# def create_interactive_table(data: List[Dict]):
#     df = pd.DataFrame(data)
#     st.dataframe(df)
#     st.write("Select tasks:")

#     selected_tasks = []
#     for i in df.index:
#         checked = st.checkbox(f"Select task {i}", key=str(i))
#         if checked:
#             selected_tasks.append(i)

#     return selected_tasks

# Example usage
if __name__ == "__main__":
    # Assuming data is loaded from JSON or generated
    data = [{'name': 'Task 1', 'description': 'Description 1', 'selected': False},
            {'name': 'Task 2', 'description': 'Description 2', 'selected': True}]
    selected_tasks = create_interactive_table(data)
    st.write(selected_tasks)