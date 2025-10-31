# Philosophy Notes Bot - Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your Credentials (2 minutes)

**A. Telegram Bot Token**
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name: "My Philosophy Bot"
5. Choose username: "my_philosophy_bot"  
6. Copy the token (looks like: `1234567890:ABCdef...`)

**B. Anthropic API Key**
1. Go to https://console.anthropic.com/
2. Sign up/log in
3. Click "API Keys"
4. Create new key
5. Copy the key (starts with `sk-ant-...`)

### Step 2: Configure (1 minute)

```bash
cd philosophy_notes_bot

# Create environment file
cp .env.example .env

# Edit with your credentials
nano .env
# Or use your favorite editor
```

Put in your tokens:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
ANTHROPIC_API_KEY=sk-ant-...
```

Save and close.

### Step 3: Run (30 seconds)

```bash
# Quick start (just the bot)
./start_bot.sh

# Or full stack (bot + sync server)
./start_all.sh
```

### Step 4: Use It! (2 minutes)

1. Open Telegram
2. Search for your bot (the username you chose)
3. Send `/start`
4. Send `/setup` and follow prompts
5. Start sending thoughts!

**Examples:**
```
Just realized training is like [[Sisyphus]] #philosophy

What if BIM could reflect [[Wittgenstein]]'s clarity? #ozone #idea

Reading [[Camus]] on absurdism #existentialism
```

---

## 📖 Daily Workflow

**Morning:**
- Send thoughts as they come

**Throughout day:**
- Capture ideas, questions, quotes
- Use #tags and [[concepts]]

**Evening (11 PM by default):**
- Bot sends daily summary with Claude's reflection
- Download to Obsidian or review in Telegram

**Weekly:**
- Use `/week` to see patterns
- Use `/stats` to see your thinking trends

---

## 🔄 Obsidian Sync Setup

### Option 1: Manual (Easy)

```bash
# When you want to sync
/vault    # in Telegram

# Download the ZIP
# Extract to your Obsidian vault folder
# Done!
```

### Option 2: Auto-Sync (Best)

**First time:**
```bash
# 1. Make sure sync server is running
./start_all.sh    # or python3 sync_server.py

# 2. Get your sync token in Telegram
/sync

# 3. Run sync client
python3 philosophy_sync.py \
  --token YOUR_TOKEN \
  --vault ~/Documents/PhilosophyVault
```

**Keep it running:**
```bash
# Linux/Mac: Use tmux or screen
tmux new -s philosophy-sync
python3 philosophy_sync.py --token TOKEN --vault PATH

# Detach: Ctrl+B then D
# Reattach: tmux attach -t philosophy-sync
```

**Or run once daily:**
```bash
# Add to crontab
0 23 * * * cd /path/to/bot && python3 philosophy_sync.py --token TOKEN --vault PATH --once
```

---

## 🛠️ Management Commands

```bash
# Start services
./start_all.sh        # Bot + Sync Server
./start_bot.sh        # Just bot

# Stop services
./stop_all.sh         # Stop everything

# Check status
./status.sh           # See what's running

# View logs
tail -f logs/bot.log
tail -f logs/sync_server.log
```

---

## 📱 Telegram Commands

```
/start      - Welcome message
/setup      - First-time setup
/help       - All commands
/today      - Today's notes
/week       - This week's notes
/search X   - Search for X
/tag #X     - Notes tagged with #X
/stats      - Your statistics
/vault      - Download as ZIP
/sync       - Get sync token
/settings   - View settings
/about      - About the bot
```

---

## 🎯 Tips for Best Results

**1. Be consistent**
- Send notes daily
- Don't overthink - just capture

**2. Use tags strategically**
- `#philosophy` `#existentialism` `#question`
- `#ozone` `#work` `#training` `#idea`

**3. Link concepts**
- `[[Camus]]` `[[Sisyphus]]` `[[Authenticity]]`
- Creates connections in Obsidian

**4. Note types**
- Questions end with `?`
- Ideas start with "What if"
- Quotes use `"..."` or `– Author`
- Just write naturally!

**5. Review regularly**
- Daily summary at night
- Weekly `/week` review
- Monthly `/stats` check

---

## ⚠️ Troubleshooting

**Bot doesn't respond:**
```bash
# Check it's running
./status.sh

# Check logs
tail logs/bot.log

# Restart
./stop_all.sh && ./start_all.sh
```

**Sync doesn't work:**
```bash
# Verify sync server is running
./status.sh

# Get new token
/sync (in Telegram)

# Try manual sync first
python3 philosophy_sync.py --token TOKEN --vault PATH --once
```

**Can't see files in Obsidian:**
- Check vault path is correct
- Try reopening Obsidian
- Use `/vault` and extract manually

---

## 🌍 Deployment (VPS/Server)

**Quick Deploy:**
```bash
# 1. Clone to server
git clone [your-repo] /opt/philosophy-bot
cd /opt/philosophy-bot

# 2. Configure
cp .env.example .env
nano .env  # Add your tokens

# 3. Install
pip3 install -r requirements.txt

# 4. Start
./start_all.sh

# 5. Make it persistent (systemd)
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl enable philosophy-bot
sudo systemctl enable philosophy-sync-server
sudo systemctl start philosophy-bot
sudo systemctl start philosophy-sync-server
```

**Check it worked:**
```bash
sudo systemctl status philosophy-bot
sudo systemctl status philosophy-sync-server
```

---

## 📊 File Structure

```
philosophy_notes_bot/
├── bot.py                 # Main bot
├── sync_server.py         # Sync API
├── philosophy_sync.py     # Sync client
├── config.py             # Configuration
├── database.py           # Database ops
├── claude_integration.py  # Claude AI
├── vault_manager.py      # Obsidian files
├── utils.py              # Utilities
├── requirements.txt      # Dependencies
├── .env                  # Your credentials
├── start_bot.sh          # Quick start script
├── start_all.sh          # Start everything
├── stop_all.sh           # Stop everything
├── status.sh             # Check status
└── users/                # User data (auto-created)
    ├── users.db          # User registry
    └── [telegram_id]/    # Each user
        ├── notes.db      # Their notes
        └── vault/        # Their vault
```

---

## 🎉 You're Ready!

1. Bot is running → ✓
2. Credentials configured → ✓
3. First user set up → ✓
4. Notes capturing → ✓
5. Daily summaries incoming → ✓

**Start your philosophy practice now! 🧠**

Questions? Check README.md for detailed docs.

Happy thinking! 💭
