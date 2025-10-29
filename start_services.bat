@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 工作目录为本脚本所在目录
pushd "%~dp0"

set "PROJECT_DIR=%cd%"
set "BACKEND_DIR=%PROJECT_DIR%\backend"
set "FRONTEND_DIR=%PROJECT_DIR%\frontend"
set "LOG_DIR=%PROJECT_DIR%\logs"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM 生成时间戳用于日志文件名（避免冒号非法字符）
for /f "tokens=1-3 delims=/-. " %%a in ("%date%") do (
  set YYYY=%%c
  set MM=%%a
  set DD=%%b
)
set HH=%time:~0,2%
set MN=%time:~3,2%
set SS=%time:~6,2%
set HH=%HH: =0%
set STAMP=%YYYY%-%MM%-%DD%_%HH%-%MN%-%SS%

REM 构造日志文件路径并预先创建空文件，避免子进程未立即输出导致看不到文件
set "LOG_BACKEND=%LOG_DIR%\backend_%STAMP%.log"
set "LOG_FRONTEND=%LOG_DIR%\frontend_%STAMP%.log"
type nul > "%LOG_BACKEND%" 2>nul
type nul > "%LOG_FRONTEND%" 2>nul

REM 后端端口，可按需修改
set "BACKEND_HOST=0.0.0.0"
set "BACKEND_PORT=8021"
REM 前端参数
REM 设置为 0.0.0.0 允许局域网访问，127.0.0.1 仅本地
set "FRONTEND_HOST=0.0.0.0"
set "FRONTEND_PORT=5173"

echo [INFO] Logs will be written to %LOG_DIR%

REM 启动后端（FastAPI + Uvicorn）到后台最小化窗口，并输出到日志
if exist "%BACKEND_DIR%" (
  start "Prompt Backend" /min cmd /c "cd /d \"%BACKEND_DIR%\" ^&^& python -m uvicorn backend.app.main:app --host %BACKEND_HOST% --port %BACKEND_PORT% >> \"%LOG_BACKEND%\" 2^>^&1"
  echo [OK] Backend starting on http://127.0.0.1:%BACKEND_PORT%
  REM 等待后端健康检查就绪（最多30次 * 1s）
  for /l %%i in (1,1,30) do (
    powershell -NoProfile -Command "try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:%BACKEND_PORT%/health' -UseBasicParsing -TimeoutSec 1; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"
    if not errorlevel 1 (
      echo [OK] Backend healthy.
      goto :after_backend_wait
    )
    timeout /t 1 >nul
  )
  echo [WARN] Backend health check did not pass yet, continuing...
  :after_backend_wait
) else (
  echo [WARN] Backend directory not found: %BACKEND_DIR%
)

REM 启动前端 Vite 开发服务到后台最小化窗口，并输出到日志
if exist "%FRONTEND_DIR%" (
  REM 写入前端运行时配置，确保指向后端端口
  > "%FRONTEND_DIR%\public\config.json" (
    echo {
    echo   "apiBase": "http://127.0.0.1:%BACKEND_PORT%"
    echo }
  )
  start "Prompt Frontend" /min cmd /c "cd /d \"%FRONTEND_DIR%\" ^&^& npm run dev -- --host %FRONTEND_HOST% --port %FRONTEND_PORT% --strictPort >> \"%LOG_FRONTEND%\" 2^>^&1"
  echo [OK] Frontend starting ^(Vite dev server^) on http://%FRONTEND_HOST%:%FRONTEND_PORT%/
  if "%FRONTEND_HOST%"=="0.0.0.0" (
    echo [INFO] To access from network, find your IP: ipconfig
    echo [INFO] Or use public tunnel: public_tunnel.cmd
  )
) else (
  echo [WARN] Frontend directory not found: %FRONTEND_DIR%
)

echo.
echo Started. Logs:
echo   %LOG_BACKEND%
echo   %LOG_FRONTEND%

popd
endlocal
exit /b 0


