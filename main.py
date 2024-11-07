import sys
import os
import streamlit as st

# Set the page configuration immediately after Streamlit import (REQUIRED)  
st.set_page_config(layout='wide')

from src.tasklist import TaskList
from src.sidebar import display_sidebar
from input_proc.input_proc import InputProc

# Insert the path to the Prioritize_it directory at the beginning of the system path
sys.path.insert(0, os.path.join(os.environ['USERPROFILE'], 'Documents', 'GitHub', 'Prioritize_it'))

# Display the title with smaller font
st.markdown("<h1 style='text-align: center; color: DarkGray;font-size: 26px;'>★★ !!PRIORITIZE IT!! ★★</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: DarkGray;font-size: 18px;'>A PARETO PILOT APP FOR PROJECT MANAGERS</h2>", unsafe_allow_html=True)

task_list = TaskList()

# Ensure display_sidebar is called only once
if 'selected_section' not in st.session_state:
    st.session_state.selected_section = display_sidebar(task_list)

input_proc = InputProc(task_list)