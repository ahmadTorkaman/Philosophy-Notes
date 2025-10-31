#!/bin/bash
# Start Philosophy Notes Bot

echo "🤖 Starting Philosophy Notes Bot..."

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

# Create logs directory
mkdir -p logs

# Start bot
echo "🚀 Starting bot..."
python3 bot.py

deactivate
