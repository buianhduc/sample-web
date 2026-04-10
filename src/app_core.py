import io
import zipfile
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import streamlit as st

import constants
import db


def initialize_app() -> None:
    constants.RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    db.initialize_database()


def get_resource_path(*path_segments: str) -> Path:
    return constants.RESOURCES_DIR.joinpath(*path_segments)


@st.cache_data
def load_task_description(task: str) -> str:
    markdown_path = get_resource_path(task.lower(), "problem.md")
    if markdown_path.exists():
        return markdown_path.read_text(encoding="utf-8")
    return constants.DEFAULT_TASK_DESCRIPTIONS.get(task, "Nội dung đề bài chưa được cấu hình.")


@st.cache_data
def load_answer_key(task: str) -> pd.DataFrame:
    key_path = get_resource_path(task.lower(), "answer_key.csv")
    if not key_path.exists():
        return pd.DataFrame([])
    return pd.read_csv(key_path, dtype=str)


def is_allowed_file(filename: str) -> bool:
    extension = Path(filename).suffix.lower().lstrip(".")
    return extension in constants.ALLOWED_UPLOAD_EXTENSIONS


def read_uploaded_file(uploaded_file: io.BytesIO, filename: str) -> pd.DataFrame:
    extension = Path(filename).suffix.lower().lstrip(".")
    if extension == "csv":
        return pd.read_csv(uploaded_file, dtype=str)

    try:
        return pd.read_excel(uploaded_file, dtype=str)
    except ImportError as exc:
        raise RuntimeError(
            "openpyxl is required to read Excel uploads. Add it to dependencies and restart the app."
        ) from exc


def normalize_upload_columns(df: pd.DataFrame) -> pd.DataFrame:
    lower_columns = {col: col.strip().lower() for col in df.columns}
    return df.rename(columns=lower_columns)


def create_sample_submission_zip(task: str) -> bytes:
    answer_key = load_answer_key(task)
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            f"{task.lower()}_readme.txt",
            """
Sample submission bundle for the contest.

Place your results file in the same archive before uploading.
The expected upload fields are: id, function, param, time.
""",
        )

        if not answer_key.empty:
            archive.writestr(
                f"{task.lower()}_answer_key.csv",
                answer_key.to_csv(index=False),
            )

        archive.writestr(
            f"{task.lower()}_sample_upload.csv",
            "id,function,param,time\n1,select_choice,A,20\n2,call_api,weather,18\n3,confirm,true,22\n",
        )

    buffer.seek(0)
    return buffer.read()


def compute_score(is_correct: bool, elapsed_time: float) -> float:
    if not is_correct:
        return 0.0

    penalty = abs(elapsed_time - constants.TIME_TARGET) / constants.TIME_PENALTY_DENOM
    raw_score = constants.SCORE_FOR_CORRECT - penalty ** 2
    return max(0.0, raw_score)


def evaluate_submission(uploaded: pd.DataFrame, answer_key: pd.DataFrame) -> dict:
    uploaded = normalize_upload_columns(uploaded)
    missing_columns = [col for col in constants.REQUIRED_UPLOAD_COLUMNS if col not in uploaded.columns]
    if missing_columns:
        raise ValueError(f"File thiếu cột: {', '.join(missing_columns)}")

    answer_key = normalize_upload_columns(answer_key)
    if {"id", "function", "param"} - set(answer_key.columns):
        raise ValueError("Tệp đáp án tham khảo không hợp lệ.")

    uploaded = uploaded[["id", "function", "param", "time"]].copy()
    uploaded["id"] = uploaded["id"].astype(str).str.strip()
    uploaded["function"] = uploaded["function"].astype(str).str.strip()
    uploaded["param"] = uploaded["param"].astype(str).str.strip()
    uploaded["time"] = uploaded["time"].astype(float)

    answer_key = answer_key[["id", "function", "param"]].copy()
    answer_key["id"] = answer_key["id"].astype(str).str.strip()
    answer_key["function"] = answer_key["function"].astype(str).str.strip()
    answer_key["param"] = answer_key["param"].astype(str).str.strip()

    merged = uploaded.merge(answer_key, on="id", how="left", suffixes=("", "_expected"))
    merged["is_correct"] = (
        merged["function"] == merged["function_expected"]
    ) & (merged["param"] == merged["param_expected"])
    merged["score"] = merged.apply(
        lambda row: compute_score(row["is_correct"], float(row["time"])), axis=1
    )

    correct_count = int(merged["is_correct"].sum())
    total_count = int(len(merged))
    accuracy = float(correct_count) / total_count if total_count else 0.0
    average_score = float(merged["score"].mean()) if total_count else 0.0
    total_score = float(round(average_score, 2))

    return {
        "correct_count": correct_count,
        "total_count": total_count,
        "accuracy": round(accuracy, 4),
        "score": total_score,
        "detail": merged,
    }


def set_logged_in_team(team: Dict) -> None:
    st.session_state["team"] = team


def get_logged_in_team() -> Optional[Dict]:
    return st.session_state.get("team")


def logout_team() -> None:
    st.session_state.pop("team", None)


def render_task_page(task: str) -> None:
    st.title(f"{task} task")
    st.markdown(load_task_description(task))
    sample_zip = create_sample_submission_zip(task)
    st.download_button(
        label="Download sample submission bundle",
        data=sample_zip,
        file_name=f"{task.lower()}_sample_bundle.zip",
        mime="application/zip",
    )
    st.info("Tệp zip mẫu chứa sample upload CSV và hướng dẫn định dạng.")