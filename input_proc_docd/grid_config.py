"""
grid_config.py: Module for managing and displaying task data in an interactive grid format using Streamlit and st_aggrid.

This module facilitates the loading of task data from either a JSON file or an uploaded CSV file, calculates a priority score (ratio) for each task based on its value and effort, and displays the tasks in an interactive grid. Users can update the ranking of tasks directly within the grid. The module also includes functionality for saving and updating the grid's state, allowing for persistent data manipulation across sessions.
"""

import importlib
import json
import pathlib

import pandas as pd
import st_aggrid
import streamlit as st
from code_editor import code_editor
from st_aggrid import AgGrid, JsCode
from st_aggrid.shared import DataReturnMode, JsCodeEncoder

import numpy as np
import streamlit as st

importlib.reload(st_aggrid)

try:
    st.set_page_config(layout="wide")
except:
    pass

def getData(data_choice=None, uploaded_file=None):
    """
    Loads data from a specified source, calculates a priority score (ratio), and assigns ranks to tasks.

    Parameters:
    - data_choice (str, optional): Method to load data. Defaults to None.
      - 'Load from JSON': Loads data from a predefined JSON file.
      - 'Upload CSV': Expects an uploaded CSV file.
    - uploaded_file (streamlit.uploaded_file_manager.UploadedFile, optional): File uploader for CSV files. Required if data_choice is 'Upload CSV'.

    Returns:
    - pd.DataFrame: Dataframe containing tasks with additional columns for 'ratio' and 'Rank' based on task value and effort.
    """
    path = pathlib.Path(__file__).parent.parent / "data/sample_tasks_ALL.json"
    if data_choice == 'Load from JSON':
        data = pd.read_json(path)
    elif data_choice == 'Upload CSV' and uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        st.warning("No data loaded.")
        return None

    data['ratio'] = data['task_value'] / data['task_effort']
    data['Rank'] = data['ratio'].rank(ascending=False, method='min').astype(int)
    return data

data_options = ['Load from JSON', 'Upload CSV']
data_choice = st.selectbox('Choose how to load data:', data_options)

uploaded_file = None
if data_choice == 'Upload CSV':
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if st.button('Load data'):
    if "data" not in st.session_state or st.session_state.data is None:
        st.session_state.data = getData(data_choice, uploaded_file)

if "data" in st.session_state:
    data = st.session_state.data

if st.button('Update Rank'):
    data['ratio'] = data['task_effort']
    data['Rank'] = data['ratio'].rank(ascending=False, method='min').astype(int)
    st.session_state.data = data

gridOptions = {
    "columnTypes": {"date": {"valueFormatter": "new Date(value).toLocaleDateString()}"},
    "columnDefs": [
        {"field": "Rank", "minWidth": 40, "maxWidth": 100, "editable": False},
        {"field": "task_id", "minWidth": 50, "headerCheckboxSelection": True, "checkboxSelection": True, "pinned": "left"},
        {"field": "name", "minWidth": 100, "cellStyle": {"fontWeight": "bold", "white-space": "normal"}},
        {"field": "description", "minWidth": 200, "editable": True},
        {"field": "task_value", "minWidth": 20, "editable": True},
        {"field": "task_effort", "minWidth": 20, "editable": True},
        {"field": "ratio", "minWidth": 10, "maxWidth": 100, "type": "numericColumn", "valueGetter": "(data.task_value / data.task_effort).toFixed(2)"},
    ],
    "onCellValueChanged": JsCode("""
        "function(params) {
            if (params.column.colId === 'task_value' || params.column.colId === 'task_effort') {
                var ratio = params.data.task_value / params.data.task_effort;
                params.node.setDataValue('ratio', ratio.toFixed(2));
            }
        }
    """),
    "defaultColDef": {"flex": 1, "minWidth": 100, "filter": True, "enableRowGroup": True, "enablePivot": True, "enableValue": True},
    "displayIndentGuides": False, "highlightIndentGuides": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True},
    "getContextMenus": True, "highlightIndentGuides": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True},
	
    "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True,wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "fold": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "markBegin", "enableLiveAutocompletion": True, "wrap": "free", "foldStyle": "free", "foldStyle": 