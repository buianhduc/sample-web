# Bài thi DS: Cục tần số

Bạn cần phân tích dữ liệu tần số và nộp kết quả theo định dạng Excel.

Yêu cầu bài thi:

- Hiển thị đề bài bằng markdown.
- Cung cấp tập tin zip chứa dữ liệu train/test để người thi tải về.
- Nộp kết quả theo file Excel gồm `id`, `function`, `param`, `time`.

Định dạng file upload:

- `id`: mã câu hỏi hoặc kết quả
- `function`: hàm hoặc lựa chọn được đưa ra
- `param`: tham số định lượng hoặc câu trả lời chi tiết
- `time`: thời gian xử lý (giây)

Chấm điểm:

- So sánh `function` và `param` với đáp án tham khảo.
- Nếu đúng, câu trả lời được 100 điểm trừ phạt thời gian.
- Phạt thời gian tính theo công thức: `(abs(time - 20) / 3) ** 2`.
