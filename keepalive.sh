#!/usr/bin/env bash
# 元宝 Bot 控制台 · 进程级心跳保活守护
#
# - 单例锁（PID 文件 /tmp/yuanbao_keepalive.pid）
# - 每 5 秒检查 app_脱敏.py 进程是否存在
# - 进程死了自动 start.sh 重新拉起
# - 检测到同一进程连续崩溃 ≥3 次：退避 30 秒，避免拉起风暴
# - 自身日志 /workspace/yuanbao-v65/logs/keepalive.log
#
# 启动方式（后台守护）：
#   setsid bash keepalive.sh >/dev/null 2>&1 &
# 停止：
#   kill $(cat /tmp/yuanbao_keepalive.pid)

set -u

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
PY="python3.11"
LOCK=/tmp/yuanbao_keepalive.pid
LOG_DIR="$PROJ_DIR/logs"
LOG="$LOG_DIR/keepalive.log"
START_SCRIPT="$PROJ_DIR/start.sh"

mkdir -p "$LOG_DIR"

# ─── 单例锁 ───
if [ -f "$LOCK" ]; then
    OLD_PID=$(cat "$LOCK" 2>/dev/null || echo "")
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "[$(date '+%F %T')] 已有一个 keepalive 在运行(PID $OLD_PID)，退出" >>"$LOG"
        exit 0
    fi
    rm -f "$LOCK"
fi
echo $$ >"$LOCK"

# ─── 进程查找（用 ps + grep -v grep 防自杀）───
find_target_pid() {
    ps aux | grep -E "[a]pp_脱敏\.py|[s]tart\.sh" | awk '{print $2}' | head -1
}

START_AT=$(date +%s)
LAST_CRASH_TS=0
CRASH_COUNT=0
RESTART_COUNT=0

echo "[$(date '+%F %T')] keepalive 启动 (PID $$，监控 $PROJ_DIR)" >>"$LOG"

cleanup() {
    rm -f "$LOCK"
    # 不杀目标进程，交给下一个 keepalive / 手动管理
    exit 0
}
trap cleanup INT TERM EXIT

# ─── 主循环 ───
while true; do
    TARGET_PID=$(find_target_pid)

    if [ -z "$TARGET_PID" ]; then
        # 进程不在了：判定是否需要退避
        NOW=$(date +%s)
        if [ $((NOW - LAST_CRASH_TS)) -lt 30 ] && [ $CRASH_COUNT -ge 3 ]; then
            # 30 秒内连崩 3 次：等待
            echo "[$(date '+%F %T')] 检测到 $CRASH_COUNT 次连续崩溃，退避 30 秒 ..." >>"$LOG"
            sleep 30
        fi

        echo "[$(date '+%F %T')] 目标进程不存在，拉起 ..." >>"$LOG"
        # 同步启动（非异步），避免本 keepalive 退出时进程被杀
        setsid bash "$START_SCRIPT" >>"$LOG_DIR/auto_restart.log" 2>&1 &
        sleep 5

        NEW_PID=$(find_target_pid)
        if [ -n "$NEW_PID" ]; then
            echo "[$(date '+%F %T')] ✅ 已重启，新进程 PID=$NEW_PID（第 $((++RESTART_COUNT)) 次重启）" >>"$LOG"
            CRASH_COUNT=0
        else
            CRASH_COUNT=$((CRASH_COUNT+1))
            LAST_CRASH_TS=$NOW
            echo "[$(date '+%F %T')] ❌ 拉起失败，累计 $CRASH_COUNT 次" >>"$LOG"
        fi
    else
        # 进程存在：每 5 秒巡检一次
        :
    fi

    sleep 5
done