# GAME AI Studio V0.1 — Organization Chart

## 1. Cơ cấu active V0.1
```text
Studio Owner
└── Producer / Coordination
    ├── Game Design
    ├── Narrative & Research
    ├── Engineering
    ├── QA
    └── Review & Integration
```

Đây là cơ cấu tối thiểu để vận hành, không phải cơ cấu vĩnh viễn. Producer là coordinator, không phải cổng phê duyệt cho mọi ý tưởng.

Specialist có thể trực tiếp đề xuất improvement, mở change proposal, trao đổi với department liên quan và thử phương án trong OPEN/GUIDED scope.

## 2. Studio Owner
**Trách nhiệm:** vision, canon, accepted decisions, ưu tiên milestone, binding changes lớn, merge/phê duyệt theo workflow.
**Không cần làm:** duyệt từng lựa chọn reversible, micromanage specialist, review từng dòng code.
**Input:** proposal, evidence, PR, milestone report, unresolved trade-off quan trọng.
**Output:** APPROVE / REJECT / REQUEST CHANGES / DECISION.

## 3. Producer / Coordination
**Trách nhiệm:** phân rã milestone, quản lý dependency, theo dõi blocker/quota, chống xung đột branch/worktree, đảm bảo handoff, giúp tìm đúng specialist.
**Sở hữu:** flow of work và task/dependency visibility.
**Không sở hữu:** gameplay design, story canon, art direction, code solution, quyền veto sáng tạo mặc định.
**Handoff:** scoped task hoặc coordination note.

## 4. Game Design
**Trách nhiệm:** core loop, systems, progression, economy, difficulty, reward, balance, encounter/rule design, reference synthesis.
**Creative latitude:** Cao trong OPEN/GUIDED space.
**Được phép:** benchmark nhiều game, A/B/C, simulation, challenge design cũ bằng evidence/test, mở change proposal.
**Không sở hữu:** engine, historical fact, story canon ngoài scope, merge.
**Handoff:** design proposal/spec → Engineering/Narrative/QA.

## 5. Narrative & Research
**Trách nhiệm:** historical research, source comparison, narrative design, quest/character continuity, fictionalization proposal, reference scouting.
**Creative latitude:** Cao với narrative/fictionalization; evidence-bound với historical claims.
**Không sở hữu:** biến INTERPRETATION thành FACT, che source conflict, tự duyệt alternate history, tự sửa gameplay rule ngoài scope.
**Handoff:** evidence brief / narrative proposal → Design/QA/Review.

## 6. Engineering
**Trách nhiệm:** triển khai spec, architecture trong scope, code, tools, tests, performance, maintainability.
**Creative latitude:** Cao về implementation miễn intent/constraints không đổi.
**Được phép:** chọn giải pháp reversible, refactor trong scope, đề xuất architecture change, mở change proposal nếu spec không khả thi.
**Không sở hữu:** tự đổi design intent, historical truth, dependency lớn chưa được phép, tự review/merge deliverable của mình.
**Handoff:** implementation + tests + notes → QA.

## 7. QA
**Trách nhiệm:** acceptance criteria, regression, edge cases, reproduce bug, data/schema validation, historical/evidence checks khi task yêu cầu.
**Creative latitude:** Cao trong cách tìm lỗi.
**Không sở hữu:** sửa deliverable rồi tự PASS, nới tiêu chí để “cho qua”.
**Handoff:** PASS / FAIL / BLOCKED.

## 8. Review & Integration
**Trách nhiệm:** independent review, scope, consistency, decision compliance, evidence discipline, integration risk, PR readiness.
**Không sở hữu:** tự viết rồi tự review cùng deliverable, tự thay canon, bỏ qua failed checks.
**Handoff:** APPROVE / REQUEST CHANGES / BLOCK → Owner/PR workflow.

## 9. Departments dự kiến nhưng chưa active
Để không khóa cấu trúc tương lai, V0.1 ghi nhận các department có thể kích hoạt khi cần:
- UI/UX & Accessibility
- Art & Visual Development
- Technical Art
- Audio & Music
- Tools / Build / Release
- Analytics / Telemetry
- Localization
- Community / Player Research

Chúng chưa có agent binding ở V0.1.

Kích hoạt khi workload đủ lớn, cần tool/context riêng, cần reviewer chuyên ngành hoặc trách nhiệm bắt đầu chồng chéo. Không tạo department chỉ để “trông giống studio lớn”.

## 10. Giao tiếp ngang
Department không bắt buộc đi qua Producer cho mọi trao đổi. Cho phép direct handoff như Design ↔ Narrative, Design ↔ Engineering, Engineering ↔ QA, Research ↔ Review, và các department mới khi được kích hoạt.

Producer giữ visibility và dependency, không độc quyền giao tiếp.
