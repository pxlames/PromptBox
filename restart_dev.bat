@echo off
REM 重启前端开发服务器（解决跨域问题）

echo 正在清理 Vite 缓存...
cd /d "%~dp0frontend"
if exist node_modules/.vite (
    rmdir /s /q node_modules/.vite
    echo [OK] 缓存已清理
)

echo.
echo 正在重启开发服务器...
echo.
echo 注意：请确保后端服务正在运行在 8021 端口
echo.

npm run dev

