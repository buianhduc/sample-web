"""
title: Submit Results
icon: 📤
description: Team login and submission upload page
"""

import streamlit as st

import constants
import db
from app_core import (
    evaluate_submission,
    get_logged_in_team,
    initialize_app,
    is_allowed_file,
    load_answer_key,
    logout_team,
    read_uploaded_file,
    set_logged_in_team,
)


def show_submit_page() -> None:
    st.title("Submit results")
    team = get_logged_in_team()

    if team:
        st.success(f"Logged in as {team['username']}")
        if st.button("Logout", key="logout_submit"):
            logout_team()
            st.rerun()

    with st.form("submission_form"):
        task = st.selectbox("Choose task", constants.TASKS)
        if not team:
            username = st.text_input("Team username")
            password = st.text_input("Password", type="password")
            register_new = st.checkbox("Register new team")
        else:
            st.write("Using current session for submission.")
            username = team["username"]
            password = None
            register_new = False

        uploaded_file = st.file_uploader(
            "Upload result file (Excel or CSV)",
            type=constants.ALLOWED_UPLOAD_EXTENSIONS,
        )
        submit_button = st.form_submit_button("Submit")

    if not submit_button:
        return

    if not team and (not username or not password):
        st.error("Vui lòng nhập username và password.")
        return

    if not uploaded_file:
        st.error("Vui lòng tải lên file kết quả của bạn.")
        return

    if not is_allowed_file(uploaded_file.name):
        st.error("Chỉ chấp nhận tệp .xls, .xlsx, .csv.")
        return

    if team:
        team_id = int(team["id"])
    else:
        if register_new:
            existing = db.get_team_by_username(username)
            if existing:
                st.error("Tên đội đã tồn tại. Hãy đăng nhập hoặc chọn tên khác.")
                return

            team_id = db.register_team(username, password)
            set_logged_in_team({"id": team_id, "username": username.strip()})
            st.success(f"Đăng ký thành công đội '{username}'. Bạn có thể nộp bài ngay bây giờ.")
        else:
            team_info = db.authenticate_team(username, password)
            if not team_info:
                st.error(
                    "Đăng nhập không thành công. Kiểm tra username/password hoặc chọn 'Register new team' để tạo đội mới."
                )
                return
            set_logged_in_team(team_info)
            team_id = int(team_info["id"])

    try:
        uploaded_df = read_uploaded_file(uploaded_file, uploaded_file.name)
    except Exception as exc:
        st.exception(exc)
        return

    answer_key = load_answer_key(task)
    if answer_key.empty:
        st.error("Đáp án tham khảo chưa được cấu hình cho bài này.")
        return

    try:
        evaluation = evaluate_submission(uploaded_df, answer_key)
    except ValueError as exc:
        st.error(str(exc))
        return

    db.save_submission(
        team_id=team_id,
        task=task,
        filename=uploaded_file.name,
        accuracy=evaluation["accuracy"],
        score=evaluation["score"],
        correct_count=evaluation["correct_count"],
        total_count=evaluation["total_count"],
    )

    st.success("Nộp kết quả thành công.")
    st.metric("Accuracy", f"{evaluation['accuracy'] * 100:.2f}%")
    st.metric("Score", f"{evaluation['score']:.2f}")
    st.write("### Summary")
    st.write(
        {
            "Correct rows": evaluation["correct_count"],
            "Total rows": evaluation["total_count"],
            "Average score": evaluation["score"],
        }
    )
    st.write("### Details")
    st.dataframe(
        evaluation["detail"][["id", "function", "param", "time", "score"]].fillna("")
    )


initialize_app()
st.set_page_config(page_title="Submit Results | AI Contest Platform", page_icon="📤")
show_submit_page()
