#Requires -Version 5.1
<#
.SYNOPSIS
    Tạo note mới trong vault, frontmatter đúng chuẩn, tự thêm dòng vào index.md.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\new-note.ps1 -Title "Ghi chu moi" -Area he-thong -Tags tool,setup
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Title,
    [ValidateSet('du-an', 'he-thong', 'con-nguoi', 'quy-trinh', 'y-tuong')][string]$Area = 'he-thong',
    [string[]]$Tags = @(),
    [string[]]$Sources = @()
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$root = Split-Path -Parent $PSScriptRoot

function ConvertTo-Slug {
    param([string]$Text)
    $norm = $Text.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object Text.StringBuilder
    foreach ($ch in $norm.ToCharArray()) {
        $cat = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch)
        if ($cat -ne [Globalization.UnicodeCategory]::NonSpacingMark) { [void]$sb.Append($ch) }
    }
    $clean = $sb.ToString().Normalize([Text.NormalizationForm]::FormC)
    $clean = $clean -replace '[đĐ]', 'd'
    $clean = $clean.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    return $clean.Trim('-')
}

$slug = ConvertTo-Slug $Title
if (-not $slug) { throw "Tiêu đề không tạo được slug: '$Title'" }

$dir = Join-Path (Join-Path $root 'wiki') $Area
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

$path = Join-Path $dir "$slug.md"
if (Test-Path $path) { throw "Note đã tồn tại: $path" }

$tagLine = if ($Tags.Count -gt 0) { '[' + ($Tags -join ', ') + ']' } else { '[]' }
$srcLine = if ($Sources.Count -gt 0) { '[' + ($Sources -join ', ') + ']' } else { '[]' }
$today = Get-Date -Format 'yyyy-MM-dd'

$content = @"
---
title: $Title
updated: $today
status: active
tags: $tagLine
sources: $srcLine
---

# $Title

Một đoạn: note này trả lời câu hỏi gì.

## Nội dung

## Liên quan

- [[ ]]
"@

Set-Content -Path $path -Value $content -Encoding UTF8

# thêm vào index.md (cuối file nếu chưa chuyển vào đúng bảng mục)
$indexPath = Join-Path $root 'index.md'
if (Test-Path $indexPath) {
    Add-Content -Path $indexPath -Value "- [[$slug]] — $Title" -Encoding UTF8
    Write-Host "Đã thêm vào index.md (nhớ chuyển dòng vào đúng mục)." -ForegroundColor Yellow
}

Write-Host "Tạo: $path" -ForegroundColor Green
