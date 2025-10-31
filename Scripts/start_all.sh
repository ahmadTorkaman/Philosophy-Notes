#!/bin/bash

echo "=========================================="
echo "Philosophy Notes Bot - Full Stack Start"
echo "=========================================="
echo ""
echo "This will start:"
echo "  1. Telegram Bot (main bot)"
echo "  2. Sync Server (for auto-sync)"
echo ""
echo "Both will run in the background."
echo "Use 'stop_all.sh' to stop them."
echo ""

# Check if already running
if pgrep -f "bot.py" > /dev/null; then
    echo "⚠️  Bot is already running!"
    echo "   Stop it first: ./stop_all.sh"
    exit 1
fi

# Load environment
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start bot in background
echo "Starting Telegram Bot..."
nohup python3 bot.py > logs/bot.log 2>&1 &
BOT_PID=$!
echo "✓ Bot started (PID: $BOT_PID)"

# Wait a moment
sleep 2

# Start sync server in background
echo "Starting Sync Server..."
nohup python3 sync_server.py > logs/sync_server.log 2>&1 &
SYNC_PID=$!
echo "✓ Sync Server started (PID: $SYNC_PID)"

# Create logs directory
mkdir -p logs

# Save PIDs
echo $BOT_PID > logs/bot.pid
echo $SYNC_PID > logs/sync_server.pid

echo ""
echo "=========================================="
echo "✓ All services started!"
echo "=========================================="
echo ""
echo "Logs:"
echo "  Bot: tail -f logs/bot.log"
echo "  Sync: tail -f logs/sync_server.log"
echo ""
echo "Stop all: ./stop_all.sh"
echo "Status: ./status.sh"
echo ""
