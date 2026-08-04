# HAKIMI ERP 一键启动脚本 (PowerShell)
# 同时启动后端 (http://localhost:8000) 和前端 (http://localhost:5173)

$PROJECT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BACKEND_DIR = Join-Path $PROJECT_DIR "backend"
$FRONTEND_DIR = Join-Path $PROJECT_DIR "frontend"
$NODE_DIR = Join-Path $FRONTEND_DIR ".node-runtime\node-v20.15.1-win-x64"
$VENV_DIR = Join-Path $BACKEND_DIR ".venv"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "   HAKIMI ERP 本地开发环境启动" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 .env
Write-Host "[1/5] 检查后端数据库配置..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $BACKEND_DIR ".env"))) {
    Write-Host "[警告] 未找到 backend\.env 文件。" -ForegroundColor Red
    Write-Host "       请复制 backend\.env.example 为 backend\.env 并填写数据库密码。" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}

# 2. 检查 Node 运行时
Write-Host "[2/5] 检查前端 Node.js 运行时..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $NODE_DIR "node.exe"))) {
    Write-Host "[错误] 未找到本地 Node.js 运行时: $NODE_DIR" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}

# 3. 初始化后端虚拟环境
Write-Host "[3/5] 检查后端 Python 虚拟环境..." -ForegroundColor Yellow
$PythonExe = Join-Path $VENV_DIR "Scripts\python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Host "[提示] 正在创建后端虚拟环境..." -ForegroundColor Yellow
    python -m venv "$VENV_DIR"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 创建虚拟环境失败。" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
}

Write-Host "[提示] 安装/更新后端依赖..." -ForegroundColor Yellow
& (Join-Path $VENV_DIR "Scripts\activate.bat") | Out-Null
& $PythonExe -m pip install -q -r (Join-Path $BACKEND_DIR "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 后端依赖安装失败。" -ForegroundColor Red
    Read-Host "按 Enter 退出"
    exit 1
}

# 4. 启动后端
Write-Host "[4/5] 启动后端服务..." -ForegroundColor Yellow
$BackendJob = Start-Job -ScriptBlock {
    param($dir, $venv)
    Set-Location $dir
    & (Join-Path $venv "Scripts\activate.bat") | Out-Null
    python server.py
} -ArgumentList $BACKEND_DIR, $VENV_DIR

Write-Host "[提示] 等待后端初始化 (5 秒)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 5. 启动前端
Write-Host "[5/5] 启动前端服务..." -ForegroundColor Yellow
$FrontendJob = Start-Job -ScriptBlock {
    param($dir, $nodeDir)
    Set-Location $dir
    $env:PATH = "$nodeDir;$($env:PATH)"
    npm run dev
} -ArgumentList $FRONTEND_DIR, $NODE_DIR

# 6. 打开浏览器
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "   启动完成！正在打开浏览器..." -ForegroundColor Green
Write-Host "   前端: http://localhost:5173" -ForegroundColor Green
Write-Host "   后端: http://localhost:8000" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "[提示] 按 Ctrl+C 停止服务，或关闭本窗口。" -ForegroundColor Yellow

# 保持脚本运行并输出日志
while ($BackendJob.State -eq 'Running' -or $FrontendJob.State -eq 'Running') {
    Receive-Job -Job $BackendJob | Write-Host -ForegroundColor Blue
    Receive-Job -Job $FrontendJob | Write-Host -ForegroundColor Magenta
    Start-Sleep -Milliseconds 500
}

Stop-Job -Job $BackendJob, $FrontendJob -ErrorAction SilentlyContinue
Remove-Job -Job $BackendJob, $FrontendJob -ErrorAction SilentlyContinue
