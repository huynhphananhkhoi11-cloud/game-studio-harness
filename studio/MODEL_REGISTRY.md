# GAME AI Studio V0.1 — Model / Runtime Registry

## 1. Mục đích
Tách rõ:

`AGENT ROLE != AI RUNTIME != MODEL != PROVIDER`

Ví dụ:
- `ENGINEERING-01` = role;
- Grok Build / Antigravity / Claude Code / Kimi Code / harness khác = runtime;
- model cụ thể = model;
- xAI / Google / Anthropic / Moonshot / DeepSeek... = provider.

Thay model không tự thay quyền, role hay project truth.

## 2. Không lưu secrets
File này không được chứa:
- API key;
- OAuth token;
- cookie;
- access token;
- secret URL;
- credential;
- thông tin thanh toán nhạy cảm.

Chỉ ghi metadata vận hành không bí mật.

## 3. Registry schema

| Field | Ý nghĩa |
|---|---|
| `agent_id` | Vai trò logic |
| `runtime` | CLI/app/harness |
| `provider` | Nhà cung cấp |
| `model` | Model cụ thể nếu xác minh được |
| `access_tier` | free / trial / paid / local / unknown |
| `availability_status` | usable / limited / exhausted / unknown |
| `assignment` | primary / fallback / experimental / unassigned |
| `evaluation_status` | untested / onboarding-pass / task-pass / restricted |
| `task_fit` | loại task đã chứng minh phù hợp |
| `tool_access` | git/web/files/terminal/... nếu đã xác minh |
| `last_verified` | ngày xác minh gần nhất |
| `review_after` | thời điểm cần kiểm lại nếu thông tin dễ đổi |
| `notes` | quan sát vận hành |

## 4. Assignment table — V0.1
Chưa có assignment vĩnh viễn.

| agent_id | runtime | provider | model | assignment | evaluation_status |
|---|---|---|---|---|---|
| PRODUCER-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |
| GAME-DESIGN-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |
| NARRATIVE-RESEARCH-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |
| ENGINEERING-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |
| QA-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |
| REVIEW-INTEGRATION-01 | UNASSIGNED | UNASSIGNED | UNASSIGNED | unassigned | untested |

## 5. Operational observations — 2026-08-10
Đây là FACT về phiên thiết lập, không phải quyết định kiến trúc.

| runtime/provider | observation | status |
|---|---|---|
| Grok Build / xAI | Đã mở đúng worktree `studio-v0.1`, hoàn thành read-only onboarding và thực hiện STUDIO-001 dưới cơ chế permission từng hành động | session observation |
| Antigravity CLI / Google | Đã cài và mở workspace; onboarding không chạy vì quota model khả dụng của tài khoản lúc đó đã exhausted | session observation |

Không suy ra quota vĩnh viễn, chu kỳ reset, “model tốt nhất” hoặc assignment lâu dài. Các trạng thái phải được re-check trước khi dùng làm quyết định vận hành.

## 6. Nguyên tắc tuyển model cho role
Không gán dựa vào marketing hoặc leaderboard đơn lẻ.

Đánh giá bằng task thật:
- chất lượng đầu ra;
- scope discipline;
- evidence discipline;
- historical accuracy khi liên quan;
- coding/test performance khi liên quan;
- tool compatibility;
- latency;
- quota/cost;
- handoff quality;
- error recovery.

Một model có thể giỏi department này nhưng kém department khác.

## 7. Free/low-tier-first
Ưu tiên:
1. free/low-tier đủ năng lực;
2. tool/context tốt;
3. deterministic checks;
4. fallback khác provider;
5. escalation sang model mạnh nếu thật sự cần.

Model mạnh hơn không được bypass governance.

## 8. Failover
Khi runtime/model hết quota hoặc lỗi:
1. dừng tại trạng thái an toàn;
2. ghi handoff;
3. không tự đổi accepted decision;
4. chọn runtime/model khác;
5. agent mới đọc task + repo + diff + tests + handoff;
6. tiếp tục cùng `agent_id` nếu mission không đổi.

## 9. Primary / fallback
Sau benchmark, mỗi agent có thể có:
- `primary` — lựa chọn mặc định;
- `fallback` — thay khi primary không khả dụng;
- `experimental` — đang đánh giá;
- `restricted` — chỉ dùng cho task cụ thể hoặc cần review tăng cường.

Không yêu cầu primary/fallback phải khác hãng, nhưng đa provider được ưu tiên để giảm single-point-of-failure.

## 10. Verification freshness
Model, free tier, quota, pricing và tool support thay đổi nhanh.

Trước quyết định vận hành:
- kiểm nguồn chính thức;
- cập nhật `last_verified`;
- không suy từ video/social post;
- không coi status cũ là hiện tại.
