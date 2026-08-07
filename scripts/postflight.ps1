# Báo cáo trạng thái Git sau khi làm việc.
# Script này chỉ hiển thị thông tin; không xóa tệp và không tắt tiến trình.

Write-Host "== Git Status =="
git status

Write-Host ""
Write-Host "== Git Diff Stat =="
git diff --stat
