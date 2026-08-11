# GAME AI Studio V0.1 — Handoff Protocol

## 1. Mục tiêu
AI mới phải tiếp quản được task từ repository evidence, không cần lịch sử chat riêng hoặc chain-of-thought của AI trước.

Handoff chỉ cần chứa trạng thái, rationale tóm tắt cần thiết, evidence, diff/checks, blockers và next action.

## 2. Ba mức handoff để tránh bureaucracy

### LEVEL 0 — Micro handoff
Dùng cho thay đổi nhỏ, rõ, reversible.

Chỉ cần:
- task;
- changed files;
- checks;
- next action/blocker nếu có.

### LEVEL 1 — Standard handoff
Dùng cho feature/task thông thường.

Cần:
- goal;
- scope;
- completed/not completed;
- changed files;
- checks;
- assumptions/unresolved;
- next action.

### LEVEL 2 — High-risk / historical / architectural
Dùng khi task ảnh hưởng canon, historical claims, architecture, dependency, migration, security, nhiều department hoặc decision khó đảo ngược.

Cần đầy đủ evidence/source map, trade-off, risk và reviewer target.

Không bắt mọi micro-task làm hồ sơ nặng.

## 3. Workflow tối thiểu
```text
Task
  ↓
Assigned Specialist
  ↓
Scoped branch/worktree
  ↓
Deliverable
  ↓
Deterministic checks
  ↓
QA (khi cần)
  ↓
Independent Review (theo risk)
  ↓
PR
  ↓
Studio Owner / merge workflow
```

Không phải mọi chỉnh sửa nhỏ đều cần full QA department; mức review phải tương xứng rủi ro.

## 4. Standard Handoff Package

### Identity
- `task_id`
- `agent_id`
- branch/worktree
- runtime/model nếu hữu ích cho debugging

### Scope
- goal
- allowed scope
- actual changed files
- non-goals

### State
- completed
- remaining
- current status
- diff/commit ref nếu có

### Evidence
- tests
- validators
- benchmark
- citations/sources nếu research/history

### Knowledge labels
- FACT
- INTERPRETATION
- ASSUMPTION
- UNRESOLVED
- FICTIONALIZATION
- PROPOSAL

### Blockers
- bug
- dependency
- quota
- missing source
- ambiguous decision
- tool limitation

### Next action
Một câu rõ: **Agent tiếp theo nên làm gì trước?**

## 5. Historical / Research Handoff
Nếu task có lịch sử, ghi theo mức cần thiết:
- claim đang dùng;
- source hỗ trợ;
- source phản bác nếu có;
- confidence;
- fictionalization;
- unresolved question.

Không dùng “AI trước nói vậy” làm evidence.

Với lời thoại/hành động của nhân vật lịch sử có thật, phải rõ: có nguồn hay là fictionalized dialogue/action.

## 6. Game-reference Handoff
Nếu tham khảo game khác, ghi:
- game/source;
- pattern/nguyên lý tham khảo;
- vì sao phù hợp;
- điều muốn tránh;
- cách GAME biến đổi/kết hợp nó.

Mục tiêu là truyền nguyên lý, không truyền bản sao.

## 7. Change Proposal Handoff
Nếu agent muốn thay LOCKED/GUIDED constraint:
- current constraint;
- proposed change;
- evidence/reference;
- impact;
- trade-off;
- affected departments/files;
- rollback.

Agent tiếp theo không được coi proposal là accepted cho tới khi workflow phê duyệt.

## 8. Quota / Runtime Failure Handoff
Khi AI hết quota/lỗi:
1. dừng write nếu trạng thái không rõ;
2. ghi hành động cuối đã hoàn tất;
3. ghi hành động đang dở;
4. ghi file có thể dirty;
5. nếu được, chạy:
   ```powershell
   git status --short
   git diff --stat
   ```
6. bàn giao;
7. reassign runtime/model.

Quota exhaustion là operational state, không phải lý do thay project truth.

## 9. QA Handoff
QA trả:
- `PASS`
- `FAIL`
- `BLOCKED`

FAIL nên có expected, actual, reproduction, evidence và acceptance criterion bị ảnh hưởng.

QA không sửa deliverable rồi tự PASS.

## 10. Review Handoff
Reviewer trả:
- `APPROVE`
- `REQUEST CHANGES`
- `BLOCK`

Review theo risk: scope, decision compliance, tests, evidence, historical integrity, unresolved risk và integration readiness.

## 11. Resume Checklist cho AI mới
- [ ] Đọc `AGENTS.md`.
- [ ] Đọc task.
- [ ] Kiểm accepted decisions/spec liên quan.
- [ ] Đọc handoff ở level cần thiết.
- [ ] Kiểm `git status`.
- [ ] Kiểm diff.
- [ ] Xác nhận scope.
- [ ] Xác nhận assumptions/unresolved.
- [ ] Không dựa hidden chat history.
- [ ] Không tự nâng proposal thành decision.

## 12. Mẫu handoff ngắn
```markdown
# HANDOFF — <TASK-ID>

Level: 0 / 1 / 2
Agent: <AGENT-ID>
Branch/worktree:
Runtime/model: <optional>

## Goal
...

## Completed / Remaining
...

## Files changed
...

## Checks / Evidence
...

## Assumptions / Unresolved / Fictionalization
...

## Blockers
...

## Next action
...
```

## 13. Chưa khóa ở V0.1
UNRESOLVED:
- branch naming chi tiết;
- file handoff riêng hay task/PR comment;
- CI provider;
- automatic worktree provisioning;
- shared memory implementation;
- code graph implementation;
- staffing nhiều instance;
- department-specific benchmark suite.

Note: For persistent memory guidance and package semantics, see studio/MEMORY_PROTOCOL.md. RESUME.md may point to a LEVEL 0/1/2 handoff but does not replace the handoff protocol; a memory package should be refreshed at handoff where appropriate.

When a memory package is active, the protocol and the handoff process are complementary:

- Persistent memory is continuous repository-visible operational state (the four-file package). Handoff is a discrete transfer event (LEVEL 0/1/2) that may be referenced by RESUME.md but is not replaced by it.
- Planned interruption or runtime replacement: the outgoing writer must refresh STATE.md, append a final WORKLOG checkpoint, regenerate RESUME.md, and attempt to release or transfer the writer claim prior to handoff. The outcome (success or failure) must be recorded as a WORKLOG entry and referenced by the handoff package.
- Unplanned interruption: follow the canonical `Unplanned interruption and recovery` procedure in `studio/MEMORY_PROTOCOL.md`.
