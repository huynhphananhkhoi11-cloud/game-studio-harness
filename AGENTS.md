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

## Quy tắc theo phạm vi Project Studio `SITU-CH1`

Khi công việc thuộc `SITU-CH1` hoặc chạm vào `projects/si-tu-chapter-1/`:

1. Xác định Project Studio và nhiệm vụ được chấp nhận trước khi ghi tệp.
2. Đọc theo thứ tự tối thiểu: `projects/si-tu-chapter-1/PROJECT_STUDIO.md`, `SOURCE_AUTHORITY.md`, `DECISIONS.md`, hợp đồng nhiệm vụ hiện hành và—nếu đã kích hoạt—bốn tệp bộ nhớ theo `studio/MEMORY_PROTOCOL.md`.
3. Dùng `projects/si-tu-chapter-1/ARTIFACT_MAP.md` để tìm artifact; không đoán đường dẫn hoặc thẩm quyền từ tên hay số phiên bản.
4. Trước khi ghi, kiểm tra thẩm quyền nguồn, Git/HEAD hiện tại, thay đổi không liên quan, writer claim và các test liên quan.
5. Xem V22 và V23 là hai `AUTHOR_CREATED_WORKING_DRAFT`, `CO_EQUAL_INPUT` do Studio Owner tạo. Không bản nào tự động ưu tiên toàn cục hoặc cục bộ, kể cả với MQ01 và `DOC01`.
6. Không chỉnh sửa, thay thế, đổi tên, di chuyển, chuẩn hóa hoặc lưu lại hai tệp GDD DOCX nguồn.
7. So sánh nội dung theo đơn vị giới hạn; không chọn chỉ vì số phiên bản, độ mới, tên tệp, độ dài, độ hoàn chỉnh, vẻ trau chuốt hoặc sở thích của mô hình.
8. Luôn tách design provenance, historical evidence và official project authority.
9. Áp dụng `docs/HISTORICAL_CONTENT_SYSTEM.md` và content-promotion gate trong `SOURCE_AUTHORITY.md` trước mọi đề xuất chính thức. Không trình bày `INFERENCE`, `FICTION` hoặc `UNRESOLVED` như lịch sử đã được xác lập.
10. Không tự phê duyệt canon, không suy ra Studio Owner đã duyệt từ QA artifact, test pass, memory record hoặc nội dung chat.
11. Bàn giao công việc bền vững qua branch và Pull Request; chat output không phải trạng thái dự án đã được chấp nhận.

Các quy tắc theo phạm vi này bổ sung, không thay thế, hướng dẫn toàn repository ở trên.
