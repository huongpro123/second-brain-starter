#Requires -Version 5.1
<#
.SYNOPSIS
    Chạy setup nhanh ("Phòng Thời Gian") cho vault trên Windows PowerShell.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\setup.ps1 --check
    powershell -ExecutionPolicy Bypass -File tools\setup.ps1
#>
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$root = Split-Path -Parent $PSScriptRoot
$setupPy = Join-Path $PSScriptRoot 'setup.py'

Set-Location $root
python $setupPy @args
exit $LASTEXITCODE
