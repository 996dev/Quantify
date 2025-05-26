#!/bin/bash
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

find . -name "*.py" -type f | while read script; do
    log_file="${LOG_DIR}/$(basename "$script").log"
    echo "执行: $script (日志: $log_file)"
    python "$script" > "$log_file" 2>&1 &
done

wait
echo "所有脚本执行完成"
