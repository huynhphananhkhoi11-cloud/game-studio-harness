# GAME AI Studio — Organization Chart

## 1. Cấu trúc phân cấp

```text
Studio Owner (final binding / non-reversible authority)
└── GAME AI Studio
    ├── Platform Studio
    ├── Project Studios
    │   └── Dynamic Cross-Functional Cells
    └── Shared Expert Guilds
```

Đây là sơ đồ năng lực tổ chức, không phải yêu cầu biên chế thường trực. Chi tiết quan hệ và ranh giới nằm tại `studio/STUDIO_TOPOLOGY.md`; vòng đời Cell, Guild và trạng thái kích hoạt nằm ở các tài liệu chuẩn tương ứng.

Studio Owner giữ thẩm quyền binding/khó đảo ngược theo `studio/STUDIO_CONSTITUTION.md`. Các lớp, container và pool năng lực trong sơ đồ không tạo thêm thẩm quyền điều hành cấp Owner.

## 2. Sáu vai trò logic trong cấu trúc mới

Sáu hồ sơ STUDIO-002 tiếp tục có hiệu lực. Chúng được triển khai theo outcome và chỉ kích hoạt khi cần; vị trí sử dụng không thay mission, authority boundary, input/output, handoff hoặc yêu cầu độc lập của hồ sơ.

| Vai trò logic | Bối cảnh có thể hoạt động khi task cần | Bất biến |
| --- | --- | --- |
| Producer / Coordination | Toàn Studio, công việc Platform, Project Studio hoặc Cell có dependency đáng kể | Điều phối và giữ visibility; không phải universal gate |
| Game Design | Project Studio, Cell hoặc Guild chuyên môn phù hợp | Giữ creative latitude và ranh giới proposal/accepted design |
| Narrative & Research | Project Studio, Cell hoặc Guild chuyên môn phù hợp | Giữ kỷ luật evidence và ranh giới lịch sử/hư cấu |
| Engineering | Công việc Platform, Project Studio, Cell hoặc Guild chuyên môn phù hợp | Tự chủ implementation cục bộ trong scope |
| QA | Công việc cấp Studio, Platform, Project Studio hoặc Cell cần falsification | Không tự chứng nhận bản sửa do cùng phiên tạo ra |
| Review & Integration | Cấp Studio hoặc bất kỳ outcome nào cần independent readiness review | Độc lập với phiên tác giả và không thay Studio Owner |

Không phải mọi vai trò đều hoạt động trong mọi task. Áp dụng `LARGE ORGANIZATION, SMALL ACTIVE TEAM` và minimum-sufficient-team tại `studio/ACTIVATION_POLICY.md`.

## 3. Bộ vai trò vận hành kế thừa từ V0.1

```text
Reusable logical roles
├── Producer / Coordination
├── Game Design
├── Narrative & Research
├── Engineering
├── QA
└── Review & Integration
```

Đây là bộ năng lực vận hành tối thiểu có thể kích hoạt, không phải cơ cấu vĩnh viễn hay chuỗi phê duyệt. Producer là coordinator, không phải cổng phê duyệt cho mọi ý tưởng.

Specialist có thể trực tiếp đề xuất improvement, mở change proposal, trao đổi với department liên quan và thử phương án trong OPEN/GUIDED scope.

## 4. Studio Owner
**Trách nhiệm:** vision, canon, accepted decisions, ưu tiên milestone, binding changes lớn, merge/phê duyệt theo workflow.
**Không cần làm:** duyệt từng lựa chọn reversible, micromanage specialist, review từng dòng code.
**Input:** proposal, evidence, PR, milestone report, unresolved trade-off quan trọng.
**Output:** APPROVE / REJECT / REQUEST CHANGES / DECISION.

## 5. Producer / Coordination
**Trách nhiệm:** phân rã milestone, quản lý dependency, theo dõi blocker/quota, chống xung đột branch/worktree, đảm bảo handoff, giúp tìm đúng specialist.
**Sở hữu:** flow of work và task/dependency visibility.
**Không sở hữu:** gameplay design, story canon, art direction, code solution, quyền veto sáng tạo mặc định.
**Handoff:** scoped task hoặc coordination note.

## 6. Game Design
**Trách nhiệm:** core loop, systems, progression, economy, difficulty, reward, balance, encounter/rule design, reference synthesis.
**Creative latitude:** Cao trong OPEN/GUIDED space.
**Được phép:** benchmark nhiều game, A/B/C, simulation, challenge design cũ bằng evidence/test, mở change proposal.
**Không sở hữu:** engine, historical fact, story canon ngoài scope, merge.
**Handoff:** design proposal/spec → Engineering/Narrative/QA.

## 7. Narrative & Research
**Trách nhiệm:** historical research, source comparison, narrative design, quest/character continuity, fictionalization proposal, reference scouting.
**Creative latitude:** Cao với narrative/fictionalization; evidence-bound với historical claims.
**Không sở hữu:** biến INTERPRETATION thành FACT, che source conflict, tự duyệt alternate history, tự sửa gameplay rule ngoài scope.
**Handoff:** evidence brief / narrative proposal → Design/QA/Review.

## 8. Engineering
**Trách nhiệm:** triển khai spec, architecture trong scope, code, tools, tests, performance, maintainability.
**Creative latitude:** Cao về implementation miễn intent/constraints không đổi.
**Được phép:** chọn giải pháp reversible, refactor trong scope, đề xuất architecture change, mở change proposal nếu spec không khả thi.
**Không sở hữu:** tự đổi design intent, historical truth, dependency lớn chưa được phép, tự review/merge deliverable của mình.
**Handoff:** implementation + tests + notes → QA.

## 9. QA
**Trách nhiệm:** acceptance criteria, regression, edge cases, reproduce bug, data/schema validation, historical/evidence checks khi task yêu cầu.
**Creative latitude:** Cao trong cách tìm lỗi.
**Không sở hữu:** sửa deliverable rồi tự PASS, nới tiêu chí để “cho qua”.
**Handoff:** PASS / FAIL / BLOCKED.

## 10. Review & Integration
**Trách nhiệm:** independent review, scope, consistency, decision compliance, evidence discipline, integration risk, PR readiness.
**Không sở hữu:** tự viết rồi tự review cùng deliverable, tự thay canon, bỏ qua failed checks.
**Handoff:** APPROVE / REQUEST CHANGES / BLOCK → Owner/PR workflow.

## 11. Departments dự kiến nhưng chưa active
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

Khi phù hợp, các năng lực này có thể được tổ chức thành Cell hoặc Shared Expert Guild thay vì department thường trực. Việc tạo và kích hoạt vẫn cần một nhu cầu thực, scope rõ và minimum-sufficient-team check.

## 12. Giao tiếp ngang
Department không bắt buộc đi qua Producer cho mọi trao đổi. Cho phép direct handoff như Design ↔ Narrative, Design ↔ Engineering, Engineering ↔ QA, Research ↔ Review, và các department mới khi được kích hoạt.

Producer giữ visibility và dependency, không độc quyền giao tiếp.
