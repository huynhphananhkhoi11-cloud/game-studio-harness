# Game Studio Harness

Bộ khung này dùng để quản lý ý tưởng, quyết định và nhiệm vụ cho một dự án game ở giai đoạn khởi tạo. Repository hiện **chưa phải là dự án game hoàn chỉnh** và **chưa chọn game engine, ngôn ngữ lập trình hoặc hệ sinh thái dependency**.

## Cấu trúc

```text
.
├── AGENTS.md                    # Quy tắc làm việc cho tác nhân AI và cộng tác viên
├── README.md                    # Hướng dẫn sử dụng bộ khung
├── docs/
│   ├── DECISIONS.md             # Nhật ký quyết định cấp studio/repository
│   ├── GAME_VISION.md           # Biểu mẫu tầm nhìn game để người dùng điền
│   ├── HISTORICAL_CONTENT_SYSTEM.md
│   └── design/                  # Các đặc tả thiết kế dẫn xuất hiện có
├── projects/
│   └── si-tu-chapter-1/         # Project Studio SITU-CH1 và trạng thái riêng của dự án
├── scripts/
│   ├── postflight.ps1           # Báo cáo trạng thái Git sau khi làm việc
│   ├── preflight.ps1            # Báo cáo thông tin máy Windows trước khi làm việc
│   ├── validate_evidence_register.py
│   └── validate_project_studio.py
├── source/                      # Nguồn GDD và hồ sơ MQ01 được bảo tồn tại chỗ
├── studio/                      # Hiến chương, topology, protocol và template của studio
├── tasks/                       # Hợp đồng nhiệm vụ
└── tests/                       # Kiểm thử tự động
```

## Project Studio `SITU-CH1`

`SITU-CH1` là container tổ chức đầu tiên cho dự án lịch sử **Sĩ Tử — Hành Trình Thi Cử — Chương 1**. Tên này là nhãn quản lý repository, chưa phải tên thương mại cuối cùng.

Các điểm vào chính:

- `projects/si-tu-chapter-1/PROJECT_STUDIO.md`: danh tính, phạm vi, ràng buộc và Cell đang hoạt động;
- `projects/si-tu-chapter-1/ARTIFACT_MAP.md`: bản đồ trung tâm để tìm nguồn, tài liệu thiết kế, dữ liệu, code, báo cáo, test, quyết định và bộ nhớ;
- `projects/si-tu-chapter-1/SOURCE_AUTHORITY.md`: quan hệ nguồn và content-promotion gate;
- `projects/si-tu-chapter-1/DECISIONS.md`: quyết định riêng của dự án;
- `projects/si-tu-chapter-1/memory/tasks/<TASK-ID>/`: các package bộ nhớ bốn tệp cho nhiệm vụ đã kích hoạt.

GDD V22 và V23 đều là bản thiết kế làm việc do Studio Owner tạo và có trạng thái `CO_EQUAL_INPUT`. Không bản nào tự động ưu tiên hơn bản kia, kể cả trong MQ01 hoặc `DOC01`. Tại bootstrap, `official_integrated_gdd: NOT_YET_DESIGNATED`.

Nội dung từ hai bản có thể được giữ, sao chép, kết hợp, sửa hoặc loại ở một nhiệm vụ sau, nhưng mỗi đơn vị nội dung phải qua so sánh logic, kiểm soát bằng chứng lịch sử, ghi rationale, review độc lập, Studio Owner phê duyệt và cập nhật artifact chính thức bền vững.

## Quy trình sử dụng đề xuất

1. **Điền tầm nhìn game** trong `docs/GAME_VISION.md` trước khi triển khai nội dung, gameplay hoặc kỹ thuật.
2. **Ghi quyết định quan trọng** vào đúng register: `docs/DECISIONS.md` cho studio/repository; `projects/si-tu-chapter-1/DECISIONS.md` cho quyết định riêng của `SITU-CH1`.
3. **Tạo nhiệm vụ từ mẫu** `tasks/TASK_TEMPLATE.md` để giới hạn mục tiêu, phạm vi, tệp được phép sửa và tiêu chí nghiệm thu.
4. **Đọc Project Studio và Artifact Map** trước khi làm việc trong `SITU-CH1`; dùng source-authority gate cho nội dung lịch sử.
5. **Chạy preflight trên Windows khi cần kiểm tra môi trường**:

   ```powershell
   ./scripts/preflight.ps1
   ```

   Script này chỉ báo cáo RAM, dung lượng ổ đĩa và GPU; không thay đổi hệ thống.

6. **Chạy các validator và test phù hợp với nhiệm vụ**. Với Project Studio:

   ```powershell
   python scripts/validate_project_studio.py
   python scripts/validate_evidence_register.py source/MQ01_evidence_register.csv
   python -m unittest discover -s tests -p "test*.py" -v
   ```

7. **Sau khi làm việc, chạy postflight để xem thay đổi Git**:

   ```powershell
   ./scripts/postflight.ps1
   ```

   Script này chỉ hiển thị `git status` và `git diff --stat`; không xóa tệp hoặc tắt tiến trình.

## Pull Request và trạng thái được chấp nhận

- Branch và Pull Request chứa công việc được đề xuất để kiểm tra và review.
- `main` được bảo vệ là trạng thái tích hợp đã được chấp nhận sau quyết định merge của Studio Owner.
- Một tệp có mặt trên branch, test pass, QA report, memory record hoặc chat output không tự động biến nội dung game thành canon chính thức.
- STUDIO-005 chưa hoàn thành game, chưa chỉ định GDD tích hợp chính thức, chưa chọn công nghệ và chưa tạo production pipeline.

## Nguyên tắc hiện tại

- Không cài dependency.
- Không chạy build.
- Không tải mô hình AI.
- Không tạo tệp nhị phân.
- Không tự chọn game engine hoặc ngôn ngữ lập trình khi chưa có quyết định được ghi nhận.
- Không mở rộng phạm vi ngoài nhiệm vụ đã được giao.
- Không chỉnh sửa hai GDD DOCX nguồn tại chỗ.
- Không dùng tên phiên bản, độ mới hoặc mô hình AI để tự chọn canon.
