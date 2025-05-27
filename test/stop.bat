@echo off
setlocal enabledelayedexpansion

:: 函数：安全终止Python进程
:kill_python
echo.
echo 正在查找Python进程...
tasklist /FI "IMAGENAME eq python.exe" /FI "STATUS eq RUNNING" 2>nul | find "python.exe" >nul

if %errorlevel% equ 0 (
    echo 发现以下Python进程：
    tasklist /FI "IMAGENAME eq python.exe" /FI "STATUS eq RUNNING"

    :: 安全终止（SIGTERM）
    echo.
    echo 正在尝试安全终止...
    taskkill /IM "python.exe" /T /F
    timeout /t 3 >nul

    :: 检查是否终止成功
    tasklist /FI "IMAGENAME eq python.exe" 2>nul | find "python.exe" >nul
    if %errorlevel% equ 0 (
        echo 警告：仍有Python进程存活！
        goto force_kill
    ) else (
        echo 所有Python进程已安全终止
        goto end
    )
) else (
    echo 未找到运行的Python进程
    goto end
)

:: 函数：强制终止（SIGKILL）
:force_kill
echo.
echo 正在强制终止...
wmic process where "name='python.exe'" delete >nul 2>&1
timeout /t 2 >nul

:: 最终检查
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find "python.exe" >nul
if %errorlevel% equ 0 (
    echo 错误：无法终止以下Python进程：
    tasklist /FI "IMAGENAME eq python.exe"
) else (
    echo 所有Python进程已强制终止
)

:end
echo.
pause
