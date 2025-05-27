@echo off
setlocal enabledelayedexpansion
set LOG_DIR=logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: 遍历所有 .py 文件并记录日志
for /r %%f in (*.py) do (
    set "LOG_FILE=%%~nf.log"
    echo 执行: %%f (日志: !LOG_FILE!)
    python "%%f" > "%LOG_DIR%\!LOG_FILE!" 2>&1
)
echo 所有 Python 脚本执行完成（日志保存在 %LOG_DIR%）
pause
