# Game Studio Harness

Bộ khung này dùng để quản lý ý tưởng, quyết định và nhiệm vụ cho một dự án game ở giai đoạn khởi tạo. Repository hiện **chưa phải là dự án game hoàn chỉnh** và **chưa chọn game engine, ngôn ngữ lập trình hoặc hệ sinh thái dependency**.

## Cấu trúc

```text
.
├── AGENTS.md              # Quy tắc làm việc cho tác nhân AI và cộng tác viên
├── README.md              # Hướng dẫn sử dụng bộ khung
├── docs/
│   ├── DECISIONS.md       # Nhật ký quyết định dự án
│   └── GAME_VISION.md     # Biểu mẫu tầm nhìn game để người dùng điền
├── scripts/
│   ├── postflight.ps1     # Báo cáo trạng thái Git sau khi làm việc
│   └── preflight.ps1      # Báo cáo thông tin máy Windows trước khi làm việc
└── tasks/
    └── TASK_TEMPLATE.md   # Mẫu mô tả nhiệm vụ
```

## Quy trình sử dụng đề xuất

1. **Điền tầm nhìn game** trong `docs/GAME_VISION.md` trước khi triển khai nội dung, gameplay hoặc kỹ thuật.
2. **Ghi quyết định quan trọng** vào `docs/DECISIONS.md`, kèm lý do, bằng chứng và trạng thái.
3. **Tạo nhiệm vụ từ mẫu** `tasks/TASK_TEMPLATE.md` để giới hạn mục tiêu, phạm vi, tệp được phép sửa và tiêu chí nghiệm thu.
4. **Chạy preflight trên Windows khi cần kiểm tra môi trường**:

   ```powershell
   ./scripts/preflight.ps1
   ```

   Script này chỉ báo cáo RAM, dung lượng ổ đĩa và GPU; không thay đổi hệ thống.

5. **Sau khi làm việc, chạy postflight để xem thay đổi Git**:

   ```powershell
   ./scripts/postflight.ps1
   ```

   Script này chỉ hiển thị `git status` và `git diff --stat`; không xóa tệp hoặc tắt tiến trình.

## Nguyên tắc hiện tại

- Không cài dependency.
- Không chạy build.
- Không tải mô hình AI.
- Không tạo tệp nhị phân.
- Không tự chọn game engine hoặc ngôn ngữ lập trình khi chưa có quyết định được ghi nhận.
- Không mở rộng phạm vi ngoài nhiệm vụ đã được giao.
