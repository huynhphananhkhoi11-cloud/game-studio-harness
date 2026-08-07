# Báo cáo môi trường Windows trước khi làm việc.
# Script này chỉ đọc thông tin và hiển thị báo cáo; không thay đổi hệ thống.

Write-Host "== Preflight Report =="
Write-Host ""

Write-Host "== RAM =="
try {
    Get-CimInstance Win32_ComputerSystem |
        Select-Object @{Name = "TotalPhysicalMemoryGB"; Expression = { [math]::Round($_.TotalPhysicalMemory / 1GB, 2) } } |
        Format-Table -AutoSize
} catch {
    Write-Warning "Không thể đọc thông tin RAM: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "== Disk Space =="
try {
    Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" |
        Select-Object DeviceID, VolumeName,
            @{Name = "SizeGB"; Expression = { [math]::Round($_.Size / 1GB, 2) } },
            @{Name = "FreeGB"; Expression = { [math]::Round($_.FreeSpace / 1GB, 2) } },
            @{Name = "FreePercent"; Expression = { if ($_.Size) { [math]::Round(($_.FreeSpace / $_.Size) * 100, 2) } else { 0 } } } |
        Format-Table -AutoSize
} catch {
    Write-Warning "Không thể đọc thông tin dung lượng ổ đĩa: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "== GPU =="
try {
    Get-CimInstance Win32_VideoController |
        Select-Object Name, DriverVersion,
            @{Name = "AdapterRAMGB"; Expression = { if ($_.AdapterRAM) { [math]::Round($_.AdapterRAM / 1GB, 2) } else { "Unknown" } } } |
        Format-Table -AutoSize
} catch {
    Write-Warning "Không thể đọc thông tin GPU: $($_.Exception.Message)"
}
