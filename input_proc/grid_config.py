import importlib
import json

import pandas as pd
import st_aggrid
import streamlit as st
from code_editor import code_editor
from st_aggrid import AgGrid, JsCode
from st_aggrid.shared import DataReturnMode, JsCodeEncoder

importlib.reload(st_aggrid)

try:
    st.set_page_config(layout="wide")
except:
    pass

gridOptions = {
    "columnTypes": {
        "date": {"valueFormatter": "new Date(value).toLocaleDateString()"},
    },
    "columnDefs": [
        {
            "field": "task_id",
            "minWidth": 150,
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "pinned": "left",
        },
        {
            "field": "name",
            "maxWidth": 90,
            "cellStyle": {"fontWeight": "bold"},
        },
        {
            "field": "description",
            "minWidth": 150,
        },
        {"field": "task_value", "minWidth": 150},
        {"field": "task_effort", "maxWidth": 90},
        {"field": "ratio", "minWidth": 150, "type": "numericColumn"},
    ],    
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


@st.cache_data()
def getData():
    import pathlib

    # Adjust the path to point to the correct directory
    path = pathlib.Path(__file__).parent.parent / "data/pre-saved-tasks.json"
    data = pd.read_json(path)
    return data

data = getData()

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
