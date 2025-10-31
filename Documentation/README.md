# Productivity Reminder Telegram Bot

A Telegram bot that sends you scheduled reminders throughout your workday to keep you hydrated, focused, and on track with your productivity goals.

## Features

- 🌅 Morning wake-up call (5:30 AM)
- 💧 5 water reminders throughout the day
- 🍽️ Lunch break reminder
- ☕ Afternoon break reminder
- 🎯 Focus check-ins
- 😴 Bedtime reminder (9:45 PM)
- 🏁 Work transition notifications

## Setup Instructions

### Step 1: Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat and send: `/newbot`
3. Follow the prompts:
   - Choose a name for your bot (e.g., "My Productivity Bot")
   - Choose a username (must end in 'bot', e.g., "my_productivity_bot")
4. **Save the bot token** - it looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 2: Get Your Chat ID

1. Search for `@userinfobot` on Telegram
2. Start a chat with it
3. It will immediately show your user info
4. **Copy your ID number** (it's just numbers, like: `123456789`)

### Step 3: Start Your Bot

1. Search for your bot on Telegram (the username you created)
2. Click "Start" or send `/start` to activate it
3. This is important - the bot can't message you until you start it first!

### Step 4: Configure the Script

1. Open `telegram_reminder_bot.py` in a text editor
2. Find these lines near the top:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   CHAT_ID = "YOUR_CHAT_ID_HERE"
   ```
3. Replace them with your actual values:
   ```python
   BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your bot token
   CHAT_ID = "123456789"  # Your chat ID
   ```
4. Save the file

### Step 5: Install Dependencies

```bash
pip install schedule requests --break-system-packages
```

### Step 6: Run the Bot

```bash
python3 telegram_reminder_bot.py
```

The bot will:
- Confirm it's running
- Send you a startup message on Telegram
- Begin sending scheduled reminders

**Keep the terminal window open** - the bot runs as long as the script is running.

## Running the Bot Continuously

### Option 1: Run in Background (Linux/Mac)

```bash
# Run in background
nohup python3 telegram_reminder_bot.py > bot.log 2>&1 &

# Check if it's running
ps aux | grep telegram_reminder_bot

# Stop it
pkill -f telegram_reminder_bot.py
```

### Option 2: Use tmux/screen (Recommended)

```bash
# Start tmux session
tmux new -s reminder_bot

# Run the bot
python3 telegram_reminder_bot.py

# Detach from session: Press Ctrl+B, then D

# Reattach later
tmux attach -t reminder_bot

# Kill session
tmux kill-session -t reminder_bot
```

### Option 3: Create a systemd service (Linux)

Create `/etc/systemd/system/reminder-bot.service`:

```ini
[Unit]
Description=Productivity Reminder Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/bot/directory
ExecStart=/usr/bin/python3 /path/to/telegram_reminder_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable reminder-bot
sudo systemctl start reminder-bot
sudo systemctl status reminder-bot
```

## Customizing Reminders

### Change Reminder Times

Edit the `setup_schedule()` function:

```python
# Example: Change wake-up time to 6:00 AM
schedule.every().day.at("06:00").do(morning_wake)

# Change water reminder to 11:00 AM
schedule.every().day.at("11:00").do(water_reminder_1)
```

### Add New Reminders

1. Create a new function:
```python
def my_custom_reminder():
    message = """✨ *MY REMINDER*
    
    Your custom message here!"""
    send_message(message)
```

2. Schedule it:
```python
schedule.every().day.at("14:30").do(my_custom_reminder)
```

### Disable Specific Reminders

Just comment out the line in `setup_schedule()`:

```python
# schedule.every().day.at("05:30").do(morning_wake)  # Disabled
```

## Daily Reminder Schedule

| Time | Reminder | Purpose |
|------|----------|---------|
| 5:30 AM | Wake up | Get up for training |
| 8:00 AM | Morning arrival | Set up workspace |
| 9:30 AM | Focus check | Capture ozone ideas |
| 10:30 AM | Water #1 | Hydration + stretch |
| 12:00 PM | Water #2 | Pre-lunch check |
| 12:30 PM | Lunch break | Mandatory break |
| 1:30 PM | Water #3 | Afternoon energy |
| 2:00 PM | Focus check | Stay on track |
| 3:00 PM | Break + Water #4 | Major afternoon break |
| 4:00 PM | Focus check | Final push |
| 4:30 PM | Water #5 | Finish water bottle |
| 5:00 PM | Workday end | Transition to showroom |
| 8:30 PM | Evening prep | Prepare for ozone time |
| 9:45 PM | Bedtime warning | 15 min until sleep |

## Troubleshooting

### Bot doesn't send messages

1. **Check bot token**: Make sure it's correct and has no extra spaces
2. **Check chat ID**: Must be your numeric ID from @userinfobot
3. **Start the bot**: You must click "Start" in your bot's Telegram chat first
4. **Check internet**: Bot needs internet to send messages
5. **Test manually**: Try running this in Python:
   ```python
   import requests
   requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                 json={"chat_id": CHAT_ID, "text": "Test"})
   ```

### Wrong timezone

If reminders come at wrong times, adjust `TIMEZONE_OFFSET` in the script:

```python
# For UTC+1 (e.g., London during BST)
TIMEZONE_OFFSET = 1

# For UTC-5 (e.g., Eastern US)
TIMEZONE_OFFSET = -5
```

Or use your system's local time and the schedule library will handle it automatically (which is the default).

### Bot stopped working

Check if the process is still running:
```bash
ps aux | grep telegram_reminder_bot
```

If not, restart it. Consider using systemd or tmux for automatic restarts.

## Command Reference

Once running, the bot doesn't accept commands - it just sends scheduled reminders. But you can:

### Stop the bot
Press `Ctrl+C` in the terminal where it's running

### Check status
The terminal will show each time a message is sent

### Modify messages
Edit the reminder functions in the script and restart the bot

## Tips

1. **Don't skip reminders** - They're there to build habits
2. **Adjust times** if your schedule changes
3. **Add reminders** for specific goals (e.g., "Start ozone work at 7pm")
4. **Keep bot running** - Use tmux or systemd so it survives reboots
5. **Review weekly** - Are the reminders helping? Adjust as needed

## Files Included

- `telegram_reminder_bot.py` - Main bot script
- `README.md` - This file
- `daily_schedule.md` - Your complete daily schedule reference

## Support

If you have issues:
1. Check the troubleshooting section
2. Verify your bot token and chat ID
3. Make sure you started the bot on Telegram
4. Check the terminal for error messages

## Privacy & Security

- Your bot token is private - don't share it
- Your chat ID is just your Telegram user ID
- The bot only sends messages to you
- No data is stored or logged anywhere

---

Built to help you stay hydrated, focused, and productive while building ozone! 💪🚀
