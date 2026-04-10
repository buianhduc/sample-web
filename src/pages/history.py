"""
title: Submission History
icon: 📜
description: Team submission history and scores
"""

import pandas as pd
import streamlit as st

import db
from app_core import get_logged_in_team, initialize_app, logout_team, set_logged_in_team


def render_history_for_team(team: dict) -> None:
    history = db.get_submission_history(int(team["id"]))
    if not history:
        st.info("Chưa có bài nộp nào cho đội này.")
        return

    st.dataframe(
        pd.DataFrame(history).assign(
            accuracy=lambda df: df["accuracy"].astype(float),
            score=lambda df: df["score"].astype(float),
        )
    )


def show_history() -> None:
    st.title("My submissions")
    team = get_logged_in_team()

    if team:
        st.success(f"Logged in as {team['username']}")
        if st.button("Logout", key="logout_history"):
            logout_team()
            st.experimental_rerun()
        render_history_for_team(team)
        return

    username = st.text_input("Team username", key="history_username")
    password = st.text_input("Password", type="password", key="history_password")
    if st.button("Load history"):
        if not username or not password:
            st.error("Vui lòng nhập username và password để xem lịch sử.")
            return

        team = db.authenticate_team(username, password)
        if not team:
            st.error("Đăng nhập không thành công.")
            return

        set_logged_in_team(team)
        render_history_for_team(team)


initialize_app()
st.set_page_config(page_title="Submission History | AI Contest Platform", page_icon="📜")
show_history()
