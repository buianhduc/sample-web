import streamlit as st

import constants
from app_core import initialize_app


def main() -> None:
    st.set_page_config(page_title="Home | AI Contest Platform", page_icon="🏠", layout="wide")
    initialize_app()

    st.title("AI Contest Platform")
    st.markdown(constants.SAMPLE_TASK_OVERVIEW)
    st.markdown(
        """
---

## Hướng dẫn sử dụng

1. Chọn bài thi LLM hoặc DS để xem đề bài và tải dữ liệu mẫu.
2. Chuẩn bị file Excel hoặc CSV với các cột: `id`, `function`, `param`, `time`.
3. Chọn trang `Submit results` để đăng nhập và nộp kết quả.
4. Xem bảng xếp hạng và lịch sử điểm của đội.
"""
    )


if __name__ == "__main__":
    main()
