# Tạo trang web thi AI
Khuyên nên dùng steamlit/gradio

Có 2 bài thi:

* LLM: Chatbot (rag - chọn đáp án đúng trong 4 đáp án, function calling - chọn đúng API và param) / Agent

* DS: Cục tần số

Mỗi bàu thi có 2 màn hình:

* Đề bài md + file zip (data train + test)

* Kết quả: username/password + upload file excel (chatbot có 4 cột: id, function, param, time)+ lịch sử điểm

* Bảng xếp hạng (thứ hạng, tên đội, độ chính xác, điểm tổng)

Chấm điểm:

* So sánh test với kết quả mình có

* Cách chấm điểm:

  * độ chính xác = kết quả đúng sai (function, param)

  * điểm tổng = nếu câu trả lời là đúng thì được 100 điểm, công thức tính phạt điểm thời gian (target là 20s, nếu hơn hoặc kém thì cộng/trừ với (delta/3)²)
