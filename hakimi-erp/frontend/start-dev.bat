@echo off
chcp 65001 >nul
REM HAKIMI ERP Frontend - 本地开发启动脚本 (Windows CMD)

set "PROJECT_DIR=%~dp0"
set "NODE_DIR=%PROJECT_DIR%.node-runtime\node-v20.15.1-win-x64"

if not exist "%NODE_DIR%" (
  echo [错误] 未找到本地 Node.js 运行时: %NODE_DIR%
  echo 请先运行环境配置脚本，或删除 .node-runtime 后重新下载 Node.js。
  exit /b 1
)

set "PATH=%NODE_DIR%;%PATH%"

echo [HAKIMI ERP] 启动开发服务器...
for /f "delims=" %%i in ('node -v') do echo Node 版本: %%i
for /f "delims=" %%i in ('npm -v') do echo npm 版本:  %%i
echo 项目目录: %PROJECT_DIR%
echo 访问地址: http://localhost:5173
echo.

cd /d "%PROJECT_DIR%"
npm run dev
