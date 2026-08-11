# AGENTS.md

## Phạm vi

Các hướng dẫn này áp dụng cho toàn bộ repository.

## Quy tắc bắt buộc

- Trước khi làm việc, phải đọc `docs/GAME_VISION.md` và `docs/DECISIONS.md` để hiểu tầm nhìn, phạm vi và các quyết định hiện có.
- Chỉ sửa các tệp nằm trong phạm vi nhiệm vụ được giao.
- Không tự ý sửa, tạo hoặc xóa tệp ngoài phạm vi nhiệm vụ.
- Không tự chọn game engine, ngôn ngữ lập trình, framework hoặc dependency nếu chưa có quyết định rõ ràng trong `docs/DECISIONS.md` hoặc yêu cầu trực tiếp từ người dùng.
- Không cài dependency, không chạy build, không tải mô hình AI và không tạo tệp nhị phân trừ khi người dùng yêu cầu rõ ràng.
- Không tự commit, push hoặc merge. Chỉ thực hiện các thao tác Git này khi người dùng yêu cầu rõ ràng trong cuộc hội thoại hiện tại.

## Quy trình làm việc đề xuất

1. Đọc `docs/GAME_VISION.md`.
2. Đọc `docs/DECISIONS.md`.
3. Xác nhận phạm vi nhiệm vụ và danh sách tệp được phép sửa.
4. Thực hiện thay đổi nhỏ, có thể kiểm tra được.
5. Ghi lại bằng chứng kiểm thử hoặc kiểm tra trong phần trả lời cuối.

Resuming tasks with an activated persistent memory package:

- Agents resuming such tasks must follow studio/MEMORY_PROTOCOL.md.
- Read the canonical task contract and docs/DECISIONS.md, then read TASK.md, STATE.md, WORKLOG.md (relevant entries), and RESUME.md from the package.
- Verify memory_schema_version, writer claim, durability state, memory claims, current Git, unrelated changes, and relevant tests before writing.
- Update memory files only at material checkpoints defined by the protocol and only within the authorized task scope recorded in TASK.md; do not make routine or ephemeral edits to memory outside those checkpoints.
- Avoid placing secrets, private transcripts, or private chain-of-thought into memory files.
