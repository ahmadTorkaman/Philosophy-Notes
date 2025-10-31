#!/bin/bash
# Stop all Philosophy Notes services

echo "🛑 Stopping Philosophy Notes services..."

cd "$(dirname "$0")/.." || exit 1

# Stop bot
echo "  Stopping bot..."
pkill -f "python3 bot.py" 2>/dev/null

# Stop sync server
echo "  Stopping sync server..."
pkill -f "python3 sync_server.py" 2>/dev/null

# Wait a moment
sleep 1

# Check if anything is still running
if pgrep -f "bot.py\|sync_server.py" > /dev/null; then
    echo "⚠️  Some processes may still be running"
    echo "  Use: ps aux | grep -E 'bot.py|sync_server.py'"
else
    echo "✅ All services stopped"
fi
