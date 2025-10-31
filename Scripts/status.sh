#!/bin/bash

# Philosophy Bot - Status Check

echo "========================================="
echo "Philosophy Bot - Status"
echo "========================================="
echo ""

# Function to check component status
check_component() {
    local name=$1
    local pidfile="logs/${name}.pid"
    
    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if ps -p $pid > /dev/null 2>&1; then
            echo "✓ $name: Running (PID: $pid)"
            return 0
        else
            echo "✗ $name: Not running (stale PID file)"
            return 1
        fi
    else
        echo "✗ $name: Not running"
        return 1
    fi
}

# Check all components
check_component "API Server"
check_component "Telegram Bot"
check_component "Daily Scheduler"

echo ""
echo "========================================="
echo "Log files:"
echo "========================================="

if [ -d "logs" ]; then
    for log in logs/*.log; do
        if [ -f "$log" ]; then
            lines=$(wc -l < "$log")
            size=$(du -h "$log" | cut -f1)
            echo "  $(basename "$log"): $lines lines, $size"
        fi
    done
else
    echo "  No logs yet"
fi

echo ""
echo "========================================="
echo "Database:"
echo "========================================="

if [ -f "data/bot.db" ]; then
    size=$(du -h data/bot.db | cut -f1)
    echo "  bot.db: $size"
    
    # Count users
    users=$(sqlite3 data/bot.db "SELECT COUNT(*) FROM users" 2>/dev/null || echo "N/A")
    notes=$(sqlite3 data/bot.db "SELECT COUNT(*) FROM notes" 2>/dev/null || echo "N/A")
    
    echo "  Users: $users"
    echo "  Notes: $notes"
else
    echo "  No database yet"
fi

echo ""
