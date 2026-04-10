"""
title: LLM Task
icon: 🤖
description: LLM contest instructions and sample bundle download
"""

import streamlit as st

import constants
from app_core import initialize_app, render_task_page


initialize_app()
st.set_page_config(page_title="LLM Task | AI Contest Platform", page_icon="🤖")
render_task_page(constants.TASK_LLM)
