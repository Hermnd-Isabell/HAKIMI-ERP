@echo off
chcp 65001 >nul
REM HAKIMI ERP 一键启动脚本 (Windows CMD)
REM 本脚本会同时启动后端 (http://localhost:8000) 和前端 (http://localhost:5173)

set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"
set "FRONTEND_DIR=%PROJECT_DIR%frontend"
set "NODE_DIR=%FRONTEND_DIR%\.node-runtime\node-v20.15.1-win-x64"
set "VENV_DIR=%BACKEND_DIR%\.venv"

echo =========================================
echo   HAKIMI ERP 本地开发环境启动
echo =========================================
echo.

REM 1. 检查 .env 文件
echo [1/5] 检查后端数据库配置...
if not exist "%BACKEND_DIR%\.env" (
  echo [警告] 未找到 backend\.env 文件。
  echo        请复制 backend\.env.example 为 backend\.env 并填写数据库密码。
  echo.
  pause
  exit /b 1
)

REM 2. 检查本地 Node 运行时
echo [2/5] 检查前端 Node.js 运行时...
if not exist "%NODE_DIR%\node.exe" (
  echo [错误] 未找到本地 Node.js 运行时。
  echo        路径: %NODE_DIR%
  echo        请确保 .node-runtime 目录存在。
  pause
  exit /b 1
)

REM 3. 初始化后端虚拟环境
echo [3/5] 检查后端 Python 虚拟环境...
if not exist "%VENV_DIR%\Scripts\python.exe" (
  echo [提示] 正在创建后端虚拟环境...
  python -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo [错误] 创建虚拟环境失败，请确认 Python 已安装并加入 PATH。
    pause
    exit /b 1
  )
)

echo [提示] 安装/更新后端依赖...
call "%VENV_DIR%\Scripts\activate.bat"
pip install -q -r "%BACKEND_DIR%\requirements.txt"
if errorlevel 1 (
  echo [错误] 后端依赖安装失败。
  pause
  exit /b 1
)

REM 4. 启动后端服务（新窗口）
echo [4/5] 启动后端服务...
start "HAKIMI ERP Backend" cmd /k "cd /d "%BACKEND_DIR%" && call "%VENV_DIR%\Scripts\activate.bat" && python server.py"

REM 等待后端启动
echo [提示] 等待后端初始化 (5 秒)...
timeout /t 5 /nobreak >nul

REM 5. 启动前端服务（新窗口）
echo [5/5] 启动前端服务...
start "HAKIMI ERP Frontend" cmd /k "cd /d "%FRONTEND_DIR%" && set "PATH=%NODE_DIR%;%PATH%" && npm run dev"

REM 6. 打开浏览器
echo.
echo =========================================
echo   启动完成！正在打开浏览器...
echo   前端: http://localhost:5173
echo   后端: http://localhost:8000
echo =========================================
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo [提示] 关闭两个弹出的命令行窗口即可停止服务。
pause
