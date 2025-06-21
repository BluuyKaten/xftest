@echo off
echo 启动前后端服务...

echo.
echo 1. 启动后端服务...
start "Backend" cmd /k "cd backend && python app.py"

echo.
echo 2. 等待后端启动...
timeout /t 3 /nobreak > nul

echo.
echo 3. 启动前端服务...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo 服务启动完成！
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:5173
echo.
echo 按任意键退出...
pause > nul 