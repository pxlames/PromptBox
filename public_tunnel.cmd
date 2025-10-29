@echo off
REM 启动带有公网隧道的服务

echo ========================================
echo   公网隧道启动工具
echo   使用 Cloudflare Tunnel 创建公网访问
echo ========================================
echo.

REM 检查 cloudflared 是否已安装
where cloudflared >nul 2>nul
if errorlevel 1 (
    echo [ERROR] cloudflared 未安装！
    echo.
    echo 请先安装 cloudflared：
    echo 1. 下载：https://github.com/cloudflare/cloudflared/releases
    echo 2. 或者运行: winget install --id=Cloudflare.cloudflared -e
    echo.
    echo 正在尝试自动安装...
    winget install --id=Cloudflare.cloudflared -e
    if errorlevel 1 (
        echo [ERROR] 自动安装失败，请手动安装 cloudflared
        pause
        exit /b 1
    )
)

echo [OK] cloudflared 已就绪
echo.

REM 检查服务是否运行
echo 检查本地服务状态...
powershell -NoProfile -Command "try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:5173' -UseBasicParsing -TimeoutSec 2; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo [INFO] 前端服务未运行，正在启动...
    start "" "%~dp0start_services.bat"
    echo 等待服务启动...
    timeout /t 5 >nul
)

powershell -NoProfile -Command "try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8021' -UseBasicParsing -TimeoutSec 2; exit 0 } catch { exit 1 }"
if errorlevel 1 (
    echo [WARN] 后端服务未运行，可能需要启动 start_services.bat
)

echo.
echo ========================================
echo   正在创建公网隧道...
echo   按 Ctrl+C 停止隧道
echo ========================================
echo.

REM 启动 cloudflared 隧道
cloudflared tunnel --url http://127.0.0.1:5173

pause
