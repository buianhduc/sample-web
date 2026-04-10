from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_FILE = "contest.db"
DB_PATH = ROOT_DIR / DB_FILE
RESOURCES_DIR = ROOT_DIR / "resources"

TASK_LLM = "LLM"
TASK_DS = "DS"
TASKS = [TASK_LLM, TASK_DS]

PAGE_HOME = "Home"
PAGE_TASK_LLM = "LLM task"
PAGE_TASK_DS = "DS task"
PAGE_SUBMIT = "Submit results"
PAGE_LEADERBOARD = "Leaderboard"
PAGE_HISTORY = "My submissions"
PAGE_OPTIONS = [
    PAGE_HOME,
    PAGE_TASK_LLM,
    PAGE_TASK_DS,
    PAGE_SUBMIT,
    PAGE_LEADERBOARD,
    PAGE_HISTORY,
]

ALLOWED_UPLOAD_EXTENSIONS = ["xls", "xlsx", "csv"]
REQUIRED_UPLOAD_COLUMNS = ["id", "function", "param", "time"]

SCORE_FOR_CORRECT = 100.0
TIME_TARGET = 20.0
TIME_PENALTY_DENOM = 3.0

DEFAULT_TASK_DESCRIPTIONS = {
    TASK_LLM: """
# Bài thi LLM: Chatbot

- Mục tiêu: phát triển chatbot RAG để chọn đáp án đúng trong 4 lựa chọn.
- Yêu cầu: gửi đầu vào đúng API và tham số.
- Giao diện: Màn hình đề bài + zip chứa dữ liệu train/test.
- Nộp kết quả: file Excel gồm `id`, `function`, `param`, `time`.

Khi nộp kết quả, hệ thống sẽ so sánh giá trị `function` và `param` với đáp án đúng.
""",
    TASK_DS: """
# Bài thi DS: Cục tần số

- Mục tiêu: phân tích dữ liệu tần số và nộp kết quả theo định dạng Excel.
- Giao diện: Màn hình đề bài + zip dữ liệu train/test.
- Nộp kết quả: file Excel gồm `id`, `function`, `param`, `time`.

Bài thi DS trong ứng dụng này được đánh giá với file dữ liệu mẫu và đáp án tham khảo.
""",
}

SAMPLE_TASK_OVERVIEW = """
# AI Contest Platform

Chào mừng đến với trang web thi AI.

Hai bài thi chính:

- **LLM**: Chatbot RAG, lựa chọn đáp án đúng trong 4 phương án, function calling.
- **DS**: Cục tần số, xử lý dữ liệu và nộp kết quả.

Mỗi bài thi có hai màn hình:

- Đề bài `md` và file zip chứa dữ liệu train/test.
- Kết quả: đăng nhập bằng username/password, upload file Excel, xem lịch sử điểm.

Bảng xếp hạng theo thứ hạng, tên đội, độ chính xác và điểm tổng.
"""
