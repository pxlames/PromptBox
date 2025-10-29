@echo off
REM 显示本机IP地址（局域网访问地址）

echo ========================================
echo   局域网访问地址
echo ========================================
echo.
echo 正在查找本机IP地址...
echo.

REM 获取IPv4地址
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set "IP=%%a"
    setlocal enabledelayedexpansion
    set "IP=!IP:~1!"
    echo   http://!IP!:5173
    endlocal
)

echo.
echo ========================================
echo   使用说明
echo ========================================
echo.
echo 局域网访问: 在同一网络的其他设备上使用上述地址
echo 公网访问: 运行 public_tunnel.cmd 创建公网隧道
echo.
echo ========================================
echo.

pause
