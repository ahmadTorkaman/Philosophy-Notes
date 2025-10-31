#!/bin/bash
# Start both Bot and Sync Server

echo "🚀 Starting Philosophy Notes - Full Stack"

# Change to project directory
cd "$(dirname "$0")/.." || exit 1

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy .env.example to .env and add your API keys"
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Create logs and users directories
mkdir -p logs users

# Start sync server in background
echo "🌐 Starting sync server..."
nohup python3 sync_server.py > logs/sync_server.log 2>&1 &
SYNC_PID=$!
echo "  Sync Server PID: $SYNC_PID"

# Wait a moment for sync server to start
sleep 2

# Start bot in foreground
echo "🤖 Starting bot..."
echo "📝 Logs: logs/bot.log"
echo "🌐 Sync Server: logs/sync_server.log"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 bot.py

# Cleanup on exit
echo ""
echo "🛑 Stopping services..."
kill $SYNC_PID 2>/dev/null
deactivate
