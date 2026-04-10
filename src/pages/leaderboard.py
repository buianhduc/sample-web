"""
title: Leaderboard
icon: 🥇
description: Contest ranking by task and score
"""

import streamlit as st

import pandas as pd
from app_core import initialize_app
import constants
import db


def show_leaderboard() -> None:
    st.title("Leaderboard")
    task_filter = st.selectbox("Filter by task", ["All tasks"] + constants.TASKS)
    task = None if task_filter == "All tasks" else task_filter
    leaderboard = db.get_leaderboard(task=task)

    if not leaderboard:
        st.info("Chưa có bài nộp nào. Hãy nộp bài và kiểm tra lại sau.")
        return

    st.dataframe(
        pd.DataFrame(leaderboard)
        .assign(
            best_score=lambda df: df["best_score"].astype(float),
            best_accuracy=lambda df: df["best_accuracy"].astype(float),
        )
        .sort_values(["best_score", "best_accuracy"], ascending=[False, False])
    )


initialize_app()
st.set_page_config(page_title="Leaderboard | AI Contest Platform", page_icon="🥇")
show_leaderboard()
