#!/bin/bash
# Check status of Philosophy Notes services

echo "📊 Philosophy Notes - Service Status"
echo "===================================="
echo ""

cd "$(dirname "$0")/.." || exit 1

# Check bot
if pgrep -f "python3 bot.py" > /dev/null; then
    BOT_PID=$(pgrep -f "python3 bot.py")
    echo "✅ Bot: Running (PID: $BOT_PID)"
else
    echo "❌ Bot: Not running"
fi

# Check sync server
if pgrep -f "python3 sync_server.py" > /dev/null; then
    SYNC_PID=$(pgrep -f "python3 sync_server.py")
    echo "✅ Sync Server: Running (PID: $SYNC_PID)"
else
    echo "❌ Sync Server: Not running"
fi

echo ""
echo "Logs:"
echo "  Bot: logs/bot.log"
echo "  Sync: logs/sync_server.log"
echo ""

# Show recent log entries if files exist
if [ -f logs/bot.log ]; then
    echo "Recent bot activity:"
    tail -n 3 logs/bot.log | sed 's/^/  /'
    echo ""
fi

if [ -f logs/sync_server.log ]; then
    echo "Recent sync activity:"
    tail -n 3 logs/sync_server.log | sed 's/^/  /'
    echo ""
fi
