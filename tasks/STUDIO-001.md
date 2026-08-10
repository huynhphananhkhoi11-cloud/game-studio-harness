# Task STUDIO-001 — Thiết lập bộ khung quản trị GAME AI Studio V0.1

## Mục tiêu
Thiết lập bộ khung quản trị tối thiểu để nhiều AI agent làm việc như một game studio chuyên nghiệp mà không biến governance thành micromanagement.

Bộ khung phải:
1. Giữ quyền quyết định cuối cùng cho Studio Owner đối với canon, quyết định binding và merge vào `main`.
2. Cho specialist đủ không gian nghiên cứu, thử nghiệm, benchmark và sáng tạo trong phần chưa bị khóa.
3. Ngăn AI tự biến proposal/prototype/assumption thành project truth.
4. Bảo vệ tính toàn vẹn lịch sử bằng evidence nhưng vẫn cho phép hư cấu có chủ ý.
5. Cho phép đổi runtime/model/provider khi hết quota hoặc chất lượng không đạt.
6. Đảm bảo AI khác tiếp quản được từ repository evidence mà không cần lịch sử chat riêng.

## Phạm vi
Tạo đúng sáu tệp:
- `tasks/STUDIO-001.md`
- `studio/STUDIO_CONSTITUTION.md`
- `studio/ORG_CHART.md`
- `studio/AGENT_REGISTRY.md`
- `studio/MODEL_REGISTRY.md`
- `studio/HANDOFF_PROTOCOL.md`

## Không làm
- Không chọn engine/ngôn ngữ/framework/dependency/art-audio pipeline.
- Không xác lập game vision, canon, economy, combat system, lịch phát hành.
- Không gán vĩnh viễn một hãng/model cho một department.
- Không biến draft/prototype/assumption thành accepted decision.
- Không cấm AI tham khảo game khác, research, tài liệu lịch sử, postmortem, GDC talk, review hoặc nguồn cộng đồng.
- Không sao chép biểu đạt có bản quyền.
- Không commit, push hoặc merge trong task này.

## Nguyên tắc bắt buộc

### Ba vùng tự do
- **LOCKED** — đã có decision/canon/ràng buộc. Không tự thay nhưng được mở `CHANGE PROPOSAL`.
- **GUIDED** — có định hướng nhưng còn chỗ thiết kế. Được đề xuất, thử nghiệm, chọn lựa reversible trong scope.
- **OPEN** — chưa có quyết định ràng buộc. Được tự do khám phá, reference và prototype.

Nếu không có nhãn và không tìm thấy decision binding, mặc định OPEN cho research/proposal, không mặc định được phép sửa canon hoặc `main`.

### Reversible vs binding
Agent được tự quyết lựa chọn reversible, cục bộ, trong scope nếu không xung đột decision/spec.

Lựa chọn binding, khó đảo ngược, ảnh hưởng canon, architecture, dependency, chi phí hoặc nhiều department cần review/change proposal.

### Historical labels
- FACT
- INTERPRETATION
- ASSUMPTION
- UNRESOLVED
- FICTIONALIZATION
- PROPOSAL

Hư cấu được phép nếu ghi rõ nội bộ và không giả làm evidence lịch sử.

### Reference use
Được tham khảo nguồn sơ cấp/lưu trữ, nghiên cứu học thuật, cơ quan nhà nước/bảo tàng/viện nghiên cứu, sách/chuyên khảo, game, postmortem/GDC talk, review/telemetry/phản hồi người chơi, và nguồn cộng đồng để tìm manh mối.

Mục tiêu là học nguyên lý và tổng hợp, không clone biểu đạt.

## Tệp được phép sửa
Chỉ sáu tệp đã liệt kê.

## Tiêu chí nghiệm thu
- [ ] Chỉ đúng sáu file.
- [ ] Có LOCKED / GUIDED / OPEN.
- [ ] Có CHANGE PROPOSAL.
- [ ] Reversible decisions trong scope không phải xin Owner cho từng chi tiết.
- [ ] Canon/binding decision vẫn có governance.
- [ ] Historical evidence và fictionalization tách rõ.
- [ ] Có quyền tham khảo nhiều nguồn/game mà không clone.
- [ ] Agent role tách runtime/model/provider.
- [ ] Handoff không yêu cầu chain-of-thought hoặc lịch sử chat riêng.
- [ ] Có failover khi AI hết quota.
- [ ] QA/review độc lập với tác giả.
- [ ] Handoff có mức nhẹ/chuẩn/rủi ro cao để tránh bureaucracy.
- [ ] Unresolved vẫn là unresolved.

## Xác minh
```powershell
git status --short --untracked-files=all
git diff --stat
```

Nếu đã stage:
```powershell
git diff --cached --check
```

## Definition of Done
Sáu tài liệu được review độc lập, không có thay đổi ngoài scope, không tạo game decision mới, và Studio Owner chấp nhận hoặc yêu cầu sửa trước commit/PR.
