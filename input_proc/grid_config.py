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

importlib.reload(st_aggrid)

try:
    st.set_page_config(layout="wide")
except:
    pass

@st.cache_resource
def getData():
    # Adjust the path to point to the correct directory
    path = pathlib.Path(__file__).parent.parent / "data/sample_tasks.json"
    data = pd.read_json(path)
    print(data.columns)
    data['ratio'] = data['task_value'] / data['task_effort']  # Calculate 'ratio'
    data['Rank'] = data['ratio'].rank(ascending=False, method='min')  # Calculate the Rank
    data['Rank'] = data['Rank'].astype(int)  # Convert Rank to integer
    return data

if "data" not in st.session_state:
    st.session_state.data = getData()

data = st.session_state.data

if st.button('Update Rank'):
    data['ratio'] = data['task_value'] / data['task_effort']  # Calculate 'ratio'
    data['Rank'] = data['ratio'].rank(ascending=False, method='min')  # Calculate the Rank
    data['Rank'] = data['Rank'].astype(int)  # Convert Rank to integer
    st.session_state.data = data  # Update the session state

gridOptions = {
    "columnTypes": {
        "date": {"valueFormatter": "new Date(value).toLocaleDateString()"},
    },
    "columnDefs": [
        {
            "field": "Rank",
            "minWidth": 40,
            "maxWidth": 100,
            "editable": False,
        },
        {
            "field": "task_id",
            "minWidth": 50,
            "maxWidth": 100,
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "pinned": "left",
        },
        {
            "field": "name",
            "minWidth": 100,
            "maxWidth": 600,
            "cellStyle": {"fontWeight": "bold", "white-space": "normal"},
            #"tooltipField": "name",
            "tooltipComponent": JsCode("""
                function CustomTooltip() {}
                CustomTooltip.prototype.init = function(params) {
                    this.eGui = document.createElement('div');
                    this.eGui.innerHTML = params.value;
                };
                CustomTooltip.prototype.getGui = function() {
                    return this.eGui;
                };
            """),
        },
        {
            "field": "description",
            "minWidth": 200,
            "maxWidth": 800,
            "cellStyle": {"white-space": "normal"},
            #"tooltipField": "description",
            "tooltipComponent": JsCode("""
                function CustomTooltip() {}
                CustomTooltip.prototype.init = function(params) {
                    this.eGui = document.createElement('div');
                    this.eGui.innerHTML = params.value;
                };
                CustomTooltip.prototype.getGui = function() {
                    return this.eGui;
                };
            """),
        },
        {
            "field": "task_value",
            "minWidth": 20,
            "maxWidth": 200,
            "editable": True,
        },
        {
            "field": "task_effort",
            "minWidth": 20,
            "maxWidth": 200,
            "editable": True,
        },
        {
            "field": "ratio",
            "minWidth": 10,
            "maxWidth": 100,
            "type": "numericColumn",
            "valueGetter": "(data.task_value / data.task_effort).toFixed(2)",
        },
    ],
    "onCellValueChanged": JsCode("""
        function(params) {
            if (params.column.colId === 'task_value' || params.column.colId === 'task_effort') {
                var ratio = params.data.task_value / params.data.task_effort;
                params.node.setDataValue('ratio', ratio.toFixed(2));
            }
        }
    """),
    "onSelectionChanged": JsCode("""
        function() {
            var selectedRows = this.api.getSelectedRows();
            selectedRows.forEach(function(selectedRow, index) {
                console.log('Selected task: ' + selectedRow.name + ' Rank: ' + selectedRow.Rank);
            });
        }
    """),
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
        "filter": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "enableValue": True,
    },
    "enableRangeSelection": True,
    "pagination": True,
    "rowSelection": "multiple",
    "suppressRowClickSelection": True,
    "suppressColumnMoveAnimation": True,
    "statusBar": {
        "statusPanels": [
            {"statusPanel": "agTotalAndFilteredRowCountComponent"},
            {"statusPanel": "agTotalRowCountComponent"},
            {"statusPanel": "agFilteredRowCountComponent"},
            {"statusPanel": "agSelectedRowCountComponent"},
            {"statusPanel": "agAggregationComponent"},
        ]
    },
    "sideBar": {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel",
                "minWidth": 225,
                "maxWidth": 225,
                "width": 225,
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel",
                "minWidth": 180,
                "maxWidth": 400,
                "width": 250,
            },
        ],
        "position": "left",
        "defaultToolPanel": "filters",
    },
    "getContextMenuItems": JsCode(
        """function(params){
                                return [
                                    ...(params.defaultItems || []),
                                    "separator",
                                    "chartRange",
                                    "separator",
                                    {
                                    "name": "Shout this row!",
                                    "action": function(params) { console.dir(params); alert(`${params.node.data.name} has a value of ${params.node.data.value} and effort of ${params.node.data.effort}! \\nClicked Cell Value: ${params.value}`)},
                                    "icon": '<img src="https://cdn-icons-png.flaticon.com/128/77/77519.png" width="16" height="16">'
                                  }
                                ]}"""
    ),
}
custom_buttons = [
    {
        "name": "Save",
        "feather": "Save",
        "hasText": True,
        "commands": ["save-state", ["response", "saved"]],
        "response": "saved",
        "style": {"bottom": "calc(50% - 4.25rem)", "right": "0.4rem"},
    },
    {
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    },
    {
        "name": "Command",
        "feather": "Terminal",
        "primary": True,
        "hasText": True,
        "commands": ["openCommandPallete"],
        "style": {"bottom": "3.5rem", "right": "0.4rem"},
    },
]

options = {
    "displayIndentGuides": False,
    "highlightIndentGuides": True,
    "wrap": "free",
    "foldStyle": "markbegin",
    "enableLiveAutocompletion": True,
}

cols = st.columns([2, 3])

with cols[0]:
    tab = st.tabs(["GridOptions", "Data"])

with tab[0]:
    response_dict = code_editor(
        json.dumps(gridOptions, indent=2, cls=JsCodeEncoder, ensure_ascii=True),
        lang="json",
        buttons=custom_buttons,
        options=options,
    )

with tab[1]:
    grid0 = AgGrid(
        data,
        height=800,
        key="grid0",
        editable=True,
        suppressMovableColumns=True,
        filter=True,
        sortable=False,
        autoSizeStrategy=dict(type="fitGridWidth"),
        pagination=True,
    )


with cols[1]:
    opt = response_dict["text"] or gridOptions
    tabs = st.tabs(
        [
            "Grid",
            "Received Data ",
            "Response.grid_response",
            "Response.Data",
            "Response.selected_rows",
        ]
    )


from uuid import uuid4

dt = grid0.data.copy()

# dt.index = [str(uuid4()) for i in range(data.shape[0]) ]
dt.index = [i * 1000 for i in range(data.shape[0])]


with tabs[0]:
    grid1 = AgGrid(
        dt,
        opt,
        height=800,
        update_on=["stateChanged"],
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        key="fix3",
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        try_to_convert_back_to_original_types=True,
    )

with tabs[1]:
    st.markdown("#### Data Sample (top 100 records)")
    st.json(data.head(100).to_json(orient="records"), expanded=False)
    st.markdown("#### Data Description")
    st.markdown(data.describe().to_html(), unsafe_allow_html=True)

with tabs[2]:
    st.write(grid1.grid_response)

with tabs[3]:
    df = grid1.data
    st.write(df)

with tabs[4]:
    st.write(grid1.selected_rows)
