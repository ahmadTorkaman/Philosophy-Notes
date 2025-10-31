#!/bin/bash

echo "======================================"
echo "Philosophy Notes Bot - Quick Start"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✓ Python 3 found"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found"
    echo ""
    echo "Please create .env file with your credentials:"
    echo ""
    echo "  cp .env.example .env"
    echo "  nano .env"
    echo ""
    echo "You need:"
    echo "  1. TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "  2. ANTHROPIC_API_KEY (from console.anthropic.com)"
    echo ""
    exit 1
fi

# Load .env
export $(cat .env | grep -v '^#' | xargs)

# Check tokens are set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_telegram_bot_token_here" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set in .env"
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_anthropic_api_key_here" ]; then
    echo "❌ ANTHROPIC_API_KEY not set in .env"
    exit 1
fi

echo "✓ Environment configured"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start bot
echo ""
echo "======================================"
echo "Starting Philosophy Notes Bot..."
echo "======================================"
echo ""
echo "Bot will start in 3 seconds..."
echo "Press Ctrl+C to stop"
echo ""

sleep 3

python3 bot.py
