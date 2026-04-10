# Bài thi LLM: Chatbot

Bạn cần xây dựng một chatbot RAG để chọn đáp án đúng trong 4 phương án.

Yêu cầu bài thi:

- Hiển thị đề bài bằng markdown.
- Cung cấp tập tin zip chứa dữ liệu train/test để người thi tải về.
- Người thi nộp kết quả qua file Excel.

Định dạng file upload:

- `id`: mã câu hỏi
- `function`: hàm được gọi hoặc lựa chọn đáp án
- `param`: tham số hoặc đáp án chi tiết
- `time`: thời gian hoàn thành (giây)

Chấm điểm:

- So sánh `function` và `param` với đáp án tham khảo.
- Nếu đúng, câu trả lời được 100 điểm trừ phạt thời gian.
- Phạt thời gian tính theo công thức: `(abs(time - 20) / 3) ** 2`.
