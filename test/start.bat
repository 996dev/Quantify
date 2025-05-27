@echo off
setlocal enabledelayedexpansion

:: 设置日志目录（自动创建）
set "LOG_DIR=%~dp0logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo 日志将保存到: %LOG_DIR%

:: 递归查找所有 .py 文件并执行
for /r %%f in (*.py) do (
    :: 提取不带扩展名的文件名作为日志名
    set "script_name=%%~nf"
    set "log_file=%LOG_DIR%\!script_name!_!date:~0,4!!date:~5,2!!date:~8,2!_!time:~0,2!!time:~3,2!!time:~6,2!.log"

    :: 显示执行信息
    echo [%time%] 正在执行: %%f
    echo [%time%] 日志文件: !log_file!

    :: 执行Python脚本并记录日志（追加模式）
    python "%%f" >> "!log_file!" 2>&1

    :: 检查执行状态
    if !errorlevel! neq 0 (
        echo [错误] %%f 执行失败！错误码: !errorlevel!
        echo [错误] 详见日志: !log_file!
    ) else (
        echo [成功] %%f 执行完成
    )
    echo.
)

echo 所有Python脚本执行完毕
pause
