#!/usr/bin/env bash
# 元宝 Bot 控制台 · 一键启动脚本
# - 自动 cd 到项目目录
# - 检查/安装依赖（flask requests）
# - 拉起 app_脱敏.py
# - 健康检查
set -e
PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJ_DIR"

PY=${PY:-python3.11}
LOG_FILE="${PROJ_DIR}/logs/start.log"
mkdir -p "$PROJ_DIR/logs"

# 依赖检查
echo "[start] 检查 Python 依赖 ..."
$PY -c "import flask, requests" 2>/dev/null || {
    echo "[start] 缺少依赖，尝试安装 ..."
    pip3 install --quiet flask requests || pip install --quiet flask requests || true
}

# 端口检查
PORT=$(python3.11 -c "import json; print(json.load(open('config.json')).get('PORT',5000))" 2>/dev/null || echo 5000)
echo "[start] 准备启动 (端口 $PORT) ..."
echo "[start] 日志: $LOG_FILE"
exec $PY app_脱敏.py >>"$LOG_FILE" 2>&1