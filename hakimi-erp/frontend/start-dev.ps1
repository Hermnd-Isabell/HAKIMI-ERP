# HAKIMI ERP Frontend - 本地开发启动脚本 (PowerShell)
$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$NodeDir = Join-Path $ProjectDir ".node-runtime\node-v20.15.1-win-x64"

if (-not (Test-Path $NodeDir)) {
  Write-Error "未找到本地 Node.js 运行时: $NodeDir`n请先运行环境配置脚本，或删除 .node-runtime 后重新下载 Node.js。"
  exit 1
}

$env:PATH = "$NodeDir;$env:PATH"

Write-Host "[HAKIMI ERP] 启动开发服务器..."
Write-Host "Node 版本: $(node -v)"
Write-Host "npm 版本:  $(npm -v)"
Write-Host "项目目录: $ProjectDir"
Write-Host "访问地址: http://localhost:5173"
Write-Host ""

Set-Location $ProjectDir
npm run dev
