#!/bin/bash

echo "Stopping Philosophy Notes Bot services..."

# Stop bot
if [ -f "logs/bot.pid" ]; then
    BOT_PID=$(cat logs/bot.pid)
    if kill -0 $BOT_PID 2>/dev/null; then
        kill $BOT_PID
        echo "✓ Stopped bot (PID: $BOT_PID)"
    else
        echo "✓ Bot not running"
    fi
    rm logs/bot.pid
else
    pkill -f "bot.py" && echo "✓ Stopped bot" || echo "✓ Bot not running"
fi

# Stop sync server
if [ -f "logs/sync_server.pid" ]; then
    SYNC_PID=$(cat logs/sync_server.pid)
    if kill -0 $SYNC_PID 2>/dev/null; then
        kill $SYNC_PID
        echo "✓ Stopped sync server (PID: $SYNC_PID)"
    else
        echo "✓ Sync server not running"
    fi
    rm logs/sync_server.pid
else
    pkill -f "sync_server.py" && echo "✓ Stopped sync server" || echo "✓ Sync server not running"
fi

echo ""
echo "All services stopped."
