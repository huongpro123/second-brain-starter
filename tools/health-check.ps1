#Requires -Version 5.1
<#
.SYNOPSIS
    Kiểm tra sức khoẻ vault: note mồ côi, link gãy, note cũ, frontmatter thiếu.
.DESCRIPTION
    Đọc toàn bộ wiki/*.md và so với index.md. Không sửa file nào.
.PARAMETER StaleDays
    Note có `updated` cũ hơn N ngày bị coi là cũ. Mặc định 60.
.PARAMETER Json
    Xuất JSON thay vì bảng cho người đọc.
.EXAMPLE
    pwsh -File tools\health-check.ps1
    pwsh -File tools\health-check.ps1 -StaleDays 30 -Json
#>
[CmdletBinding()]
param(
    [int]$StaleDays = 60,
    [switch]$Json
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$root      = Split-Path -Parent $PSScriptRoot
$wikiDir   = Join-Path $root 'wiki'
$indexPath = Join-Path $root 'index.md'

if (-not (Test-Path $wikiDir)) { throw "Không thấy thư mục wiki: $wikiDir" }

$linkPattern = [regex]'\[\[([^\]\|#]+)'

function Get-Links {
    param([string]$Text)
    # bỏ khối code (``` hoặc ~~~) để không bắt link ví dụ
    $stripped = [regex]::Replace($Text, '(?ms)^(```|~~~).*?^\1\s*$', '')
    $out = @()
    foreach ($m in $linkPattern.Matches($stripped)) {
        $target = $m.Groups[1].Value.Trim()
        if ($target) { $out += $target }
    }
    return $out
}

function Get-Basename {
    param([string]$Name)
    $n = ($Name -replace '\\', '/').Split('/')[-1]
    return ($n -replace '\.md$', '').Trim()
}

# ---- gom note ----
$notes = @(Get-ChildItem -Path $wikiDir -Recurse -Filter *.md -File -ErrorAction SilentlyContinue)
$allMd = @(Get-ChildItem -Path $root -Recurse -Filter *.md -File -ErrorAction SilentlyContinue)
$knownBasenames = @{}
foreach ($f in $allMd) { $knownBasenames[(Get-Basename $f.Name)] = $true }

# ---- index ----
$indexLinks = @()
if (Test-Path $indexPath) {
    $indexLinks = Get-Links (Get-Content -Path $indexPath -Raw -Encoding UTF8)
} else {
    Write-Warning "Không thấy index.md — mọi note sẽ bị coi là mồ côi."
}
$indexSet = @{}
foreach ($l in $indexLinks) { $indexSet[(Get-Basename $l)] = $true }

$now = Get-Date
$rows = @()

foreach ($f in $notes) {
    $rel    = Resolve-Path -Path $f.FullName -Relative
    $text   = Get-Content -Path $f.FullName -Raw -Encoding UTF8
    if (-not $text) { $text = '' }
    $base   = Get-Basename $f.Name

    $fm = [regex]::Match($text, '(?s)\A---\r?\n(.*?)\r?\n---')
    $meta = @{ title = $null; updated = $null; status = $null }
    $missing = @()
    if ($fm.Success) {
        $body = $fm.Groups[1].Value
        $t = [regex]::Match($body, '(?m)^title:\s*(.+)$')
        if ($t.Success) { $meta.title = $t.Groups[1].Value.Trim() } else { $missing += 'title' }
        $u = [regex]::Match($body, '(?m)^updated:\s*(\d{4}-\d{2}-\d{2})')
        if ($u.Success) { $meta.updated = $u.Groups[1].Value } else { $missing += 'updated' }
        $s = [regex]::Match($body, '(?m)^status:\s*(\w+)')
        if ($s.Success) { $meta.status = $s.Groups[1].Value } else { $missing += 'status' }
    } else {
        $missing += 'frontmatter'
    }

    $age = $null
    $stale = $false
    if ($meta.updated) {
        $dt = [datetime]::MinValue
        if ([datetime]::TryParseExact($meta.updated, 'yyyy-MM-dd', $null, [Globalization.DateTimeStyles]::None, [ref]$dt)) {
            $age = [int][math]::Floor(($now - $dt).TotalDays)
            $stale = ($age -gt $StaleDays)
        } else {
            $missing += 'updated-sai-dinh-dang'
        }
    }

    $links = Get-Links $text

    $rows += [pscustomobject]@{
        Note          = $base
        Path          = $rel
        Title         = $meta.title
        Status        = $meta.status
        Updated       = $meta.updated
        AgeDays       = $age
        Links         = $links.Count
        Orphan        = -not $indexSet.ContainsKey($base)
        Stale         = $stale
        MissingFields = ($missing | Sort-Object -Unique) -join ','
        OutLinks      = $links
    }
}

# ---- link gãy (tính trên toàn vault) ----
$broken = @()
foreach ($r in $rows) {
    foreach ($l in $r.OutLinks) {
        $b = Get-Basename $l
        if (-not $knownBasenames.ContainsKey($b)) {
            $broken += [pscustomobject]@{ From = $r.Note; To = $l }
        }
    }
}

$orphans = @($rows | Where-Object { $_.Orphan })
$stales  = @($rows | Where-Object { $_.Stale })
$badMeta = @($rows | Where-Object { $_.MissingFields })

$summary = [pscustomobject]@{
    Vault      = $root
    CheckedAt  = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
    Notes      = $rows.Count
    Orphans    = $orphans.Count
    BrokenLinks= $broken.Count
    Stale      = $stales.Count
    BadMeta    = $badMeta.Count
    StaleDays  = $StaleDays
}

if ($Json) {
    [pscustomobject]@{
        Summary = $summary
        Notes   = $rows
        Orphans = ($orphans | Select-Object Note, Path, Updated)
        Broken  = $broken
        Stale   = ($stales | Select-Object Note, Updated, AgeDays)
    } | ConvertTo-Json -Depth 6
    return
}

Write-Host ''
Write-Host "VAULT: $($summary.Vault)" -ForegroundColor Cyan
Write-Host ("{0} note · {1} mồ côi · {2} link gãy · {3} cũ >{4}d · {5} thiếu frontmatter" -f `
    $summary.Notes, $summary.Orphans, $summary.BrokenLinks, $summary.Stale, $StaleDays, $summary.BadMeta)
Write-Host ''

if ($rows.Count -eq 0) {
    Write-Host 'Chưa có note nào trong wiki/.' -ForegroundColor Yellow
    return
}

$rows | Sort-Object Path |
    Select-Object @{n='Note';e={$_.Note}}, Status, Updated, AgeDays, Links,
                  @{n='Orphan';e={ if ($_.Orphan) {'!'} else {''} }},
                  @{n='Stale';e={ if ($_.Stale) {'!'} else {''} }},
                  MissingFields |
    Format-Table -AutoSize

if ($orphans.Count -gt 0) {
    Write-Host 'MỒ CÔI (chưa có trong index.md):' -ForegroundColor Yellow
    $orphans | ForEach-Object { Write-Host ("  - {0}  ({1})" -f $_.Note, $_.Path) }
    Write-Host ''
}

if ($broken.Count -gt 0) {
    Write-Host 'LINK GÃY:' -ForegroundColor Red
    $broken | ForEach-Object { Write-Host ("  - {0}  ->  [[{1}]]" -f $_.From, $_.To) }
    Write-Host ''
}

if ($stales.Count -gt 0) {
    Write-Host ("CŨ HƠN {0} NGÀY (xác minh lại rồi mới cập nhật ngày):" -f $StaleDays) -ForegroundColor Yellow
    $stales | ForEach-Object { Write-Host ("  - {0}  (updated {1}, {2} ngày)" -f $_.Note, $_.Updated, $_.AgeDays) }
    Write-Host ''
}

if ($badMeta.Count -gt 0) {
    Write-Host 'FRONTMATTER THIẾU/SAI:' -ForegroundColor Yellow
    $badMeta | ForEach-Object { Write-Host ("  - {0}  ({1})" -f $_.Note, $_.MissingFields) }
    Write-Host ''
}

$ok = ($orphans.Count -eq 0 -and $broken.Count -eq 0 -and $badMeta.Count -eq 0)
if ($ok) { Write-Host 'Vault sạch.' -ForegroundColor Green }
