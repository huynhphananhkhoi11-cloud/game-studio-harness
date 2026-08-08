# Hệ thống kiểm soát nội dung lịch sử

## 1. Mục đích và phạm vi

Hệ thống này giúp đội sản xuất biến một cảnh, quest, đạo cụ, thuật ngữ, mốc thời gian hoặc cơ chế có yếu tố lịch sử thành nội dung có thể viết, thiết kế, sản xuất và QA. Mục tiêu là giữ rõ ranh giới giữa điều đã có chứng cứ, điều được phục dựng, điều suy luận, phần hư cấu và phần chưa biết.

Hệ thống không chọn engine, không dựng gameplay code, không viết lại toàn bộ GDD và không thay thế thẩm định sử liệu của con người.

## 2. Chuỗi sản xuất chuẩn

Luôn đi theo chuỗi:

1. **Scene Brief** — xác định đơn vị làm việc, mục tiêu người chơi, xung đột, thẩm quyền, động từ chơi, hậu quả bắt buộc và câu hỏi mở.
2. **Evidence Register** — tách từng claim có thể kiểm tra, ghi mức chứng cứ, nguồn, locator, allowed use và quyết định cụ thể.
3. **Evidence Gate** — chặn claim thiếu nguồn, quá cụ thể, dùng sai niên đại hoặc trộn hư cấu với sự thật lịch sử.
4. **Decision Log** — ghi quyết định giữ, sửa, bỏ hoặc giữ chờ cho từng thay đổi cụ thể.
5. **World/Quest/GDD Patch** — cập nhật nội dung theo thứ tự từ quy tắc thế giới/thuật ngữ đến quest, gameplay, treatment, dialogue, UI và prop.
6. **QA Gate** — kiểm tra độc lập sáu cổng trước khi bàn giao.

## 3. Năm mức chứng cứ

- **DIRECT:** nguồn trực tiếp hỗ trợ claim ở đúng mức cụ thể đang viết.
- **RECONSTRUCTION:** claim là phục dựng thận trọng từ nhiều nguồn tương thích hoặc khảo cứu chuyên môn.
- **INFERENCE:** claim là suy luận từ tiền đề đã nêu; không được viết như sự thật đã được nguồn nói thẳng.
- **FICTION:** yếu tố sáng tác cho game, phải có ràng buộc để không mâu thuẫn chứng cứ.
- **UNRESOLVED:** chưa đủ chứng cứ hoặc còn xung đột; không khóa production cuối.

## 4. Bốn quyết định cho thay đổi cụ thể

- **KEEP:** giữ nội dung cụ thể hiện có.
- **CHANGE:** sửa nội dung cụ thể để đúng chứng cứ hoặc hết mâu thuẫn.
- **REMOVE:** bỏ nội dung cụ thể vì sai, quá nguồn hoặc ngoài phạm vi.
- **HOLD:** giữ ở trạng thái chờ, greybox hoặc cần nghiên cứu thêm.

Các quyết định này áp dụng cho từng claim hoặc thay đổi, không dùng để phê duyệt lại toàn bộ GDD một lần.

## 5. Quy tắc nguồn và locator tối thiểu

Với `DIRECT` và `RECONSTRUCTION`, phải ghi đủ citation, locator và URL/identifier khi có. Citation tối thiểu gồm cơ quan/tác giả, tên tài liệu, năm hoặc ấn bản nếu có, locator như trang/dòng/chương/điều/mã lưu trữ và URL hoặc identifier. Locator phải đủ để reviewer khác tìm lại đúng đoạn.

Validator chỉ kiểm tra cấu trúc, enum, trường bắt buộc và hình thức URL. Nó không kiểm tra mạng, không xác nhận URL còn truy cập được và không thể tự chứng minh một claim là đúng về lịch sử.

## 6. Tài liệu hậu kỳ và LATER_ANALOGY

Tư liệu hậu kỳ có thể dùng làm `LATER_ANALOGY` để gợi ý hướng nghiên cứu, tham chiếu hình ảnh yếu hoặc nhắc rằng một thực hành tồn tại ở thời sau. Không được chuyển ngược niên đại để chứng minh rằng cùng hình thức, thuật ngữ, thủ tục hoặc đạo cụ đã tồn tại ở thời trước.

Nếu chỉ có hậu kỳ cho hình thức vật chất, quyết định nên là `HOLD` hoặc `REMOVE`, allowed use nên giới hạn như `visual analogy only` hoặc `production note only`.

## 7. Tách chức năng văn bản khỏi hình thức đạo cụ

Một quy định pháp luật hoặc văn bản thể chế có thể chứng minh rằng một loại văn tự tồn tại, có chức năng pháp lý hoặc có liên quan đến người tham gia. Bằng chứng đó không tự chứng minh bố cục, câu chữ, giấy, mực, dấu, chữ ký, điểm chỉ, kích thước hoặc chất liệu của đạo cụ.

Ví dụ kiểm chuẩn từ MQ01/DOC01: DOC01 chỉ được giữ ở mức greybox cho đến khi có chứng cứ riêng về hình thức vật chất phù hợp niên đại và địa bàn. Không chép nguyên, sửa hoặc mở rộng nội dung nguồn MQ01 khi áp dụng quy tắc này.

## 8. Bốn vai trò tuần tự

1. **Historical Research:** tách claim, tìm nguồn khi được phép, ghi citation và locator.
2. **Narrative Design:** giữ theme, nhân vật, nhịp cảnh và giới hạn thẩm quyền.
3. **Game Design:** biến claim hợp lệ thành động từ chơi, feedback, biến và fail-forward.
4. **Historical QA:** kiểm tra lại chứng cứ, niên đại, thiết chế, thẩm quyền, tài liệu và asset.

## 9. Sáu QA gate

1. **Evidence:** mọi assertion lịch sử có claim_id; nguồn và locator đủ cho `DIRECT`/`RECONSTRUCTION`.
2. **Historical Fit:** niên đại, địa bàn, chính thể, thiết chế, thuật ngữ và vật chất không quá nguồn.
3. **Narrative & Authority:** nhân vật không nhận quyền sai vai; xung đột không ép kết luận quá chứng cứ.
4. **Gameplay:** người chơi có hành động có nghĩa, feedback và fail-forward.
5. **Cross-document Consistency:** ngày, vai trò, thuật ngữ, biến, quest, UI và asset thống nhất.
6. **Delivery:** tệp đúng schema, nguồn gốc không bị sửa, restriction còn lại được bàn giao rõ.

## 10. Stop conditions

Dừng, hạ mức claim hoặc giảm độ cụ thể khi:

- thiếu citation, quote, locator, URL hoặc identifier cần thiết;
- nguồn chỉ hỗ trợ điểm rộng hơn claim;
- nguồn xung đột mà chưa có nguồn mạnh hơn giải quyết;
- tư liệu hậu kỳ bị dùng như chứng cứ đồng đại;
- asset hoặc UI cụ thể hơn evidence level;
- gameplay yêu cầu nhân vật có thẩm quyền không được chứng minh;
- tệp nguồn đang được bảo vệ khỏi sửa đổi.

Khi dừng, ghi rõ cần chứng cứ gì để gỡ chặn và đề xuất giải pháp gameplay an toàn hơn nếu có.

## 11. Quy ước đặt tên theo SCENE_ID

Dùng `SCENE_ID` làm gốc nhất quán:

- Scene Brief: `[SCENE_ID]_scene_brief.md`
- Evidence Register: `[SCENE_ID]_evidence_register.csv`
- Decision Log: `[SCENE_ID]_decision_log.md`
- QA Report: `[SCENE_ID]_qa_report.md`
- Claim ID: `[SCENE_ID]-E01`, `[SCENE_ID]-E02`, ...
- Decision ID: `[SCENE_ID]-D01`, `[SCENE_ID]-D02`, ...

## 12. Chạy validator và đọc exit code

Chạy một hoặc nhiều tệp CSV:

```bash
python scripts/validate_evidence_register.py PATH [PATH ...]
```

- Exit code `0`: tất cả tệp hợp lệ theo cấu trúc bắt buộc.
- Exit code `1`: có ít nhất một lỗi. Output `FAIL` sẽ ghi đường dẫn, dòng, `claim_id` nếu có và lý do cụ thể.
- Header-only template được phép pass nhưng có warning rõ rằng chưa có data row.

Validator không gọi mạng, không xác minh URL sống, không đọc nội dung nguồn và không thay thế reviewer lịch sử.

## 13. MQ01/DOC01 làm ví dụ giới hạn sản xuất

MQ01 là trường hợp kiểm chuẩn cho schema vì có Scene Brief, Evidence Register, Decision Log và QA Report thực tế. Khi dùng MQ01, chỉ kiểm tra tương thích hệ thống; không sửa các tệp nguồn. Giới hạn production quan trọng là DOC01 vẫn ở mức greybox: chưa khóa bố cục, câu chữ, giấy, mực, dấu, chữ ký, điểm chỉ, kích thước hoặc chất liệu nếu chưa có chứng cứ riêng phù hợp niên đại và địa bàn.
