#!/bin/bash
# 1. 查看所有 Python 进程
ps aux | grep "python"

# 2. 确认要终止的进程（无关键服务）
# 3. 尝试正常终止
pkill -f "python"

# 4. 检查是否仍有残留进程
ps aux | grep "python"

# 5. 强制终止（必要时）
pkill -9 -f "python"
