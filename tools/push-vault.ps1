# Đẩy vault lên GitHub remote đang cấu hình (1 lệnh). Chạy từ thư mục vault:
#   powershell -ExecutionPolicy Bypass -File tools\push-vault.ps1
# hoặc: .\tools\push-vault.ps1
$ErrorActionPreference = 'Stop'
$vault = Split-Path -Parent $PSScriptRoot
Set-Location $vault

$remote = (git remote get-url origin 2>$null)
if (-not $remote) {
    throw "Chưa cấu hình git remote 'origin'. Chạy: git remote add origin <URL_REPO>"
}

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if (-not $branch -or $branch -eq 'HEAD') {
    throw "Không xác định được nhánh git hiện tại."
}

git add -A
$pending = git status --porcelain
if ($pending) {
    $msg = "cap nhat vault: " + (Get-Date -Format 'yyyy-MM-dd HH:mm')
    git commit -m $msg | Out-Null
    Write-Host "Đã commit: $msg"
} else {
    Write-Host "Không có thay đổi mới, chỉ push."
}

git push -u origin $branch
Write-Host ""
Write-Host "Xong. Remote ($branch): $remote"
