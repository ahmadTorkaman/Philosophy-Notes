# 🧠 Philosophy Notes Bot

> Your personal AI-powered philosophy assistant using Google Gemini

A Telegram bot that captures your daily thoughts, analyzes them with Google Gemini AI, and creates beautiful Obsidian-compatible notes.

## ✨ Features

- 📝 **Capture thoughts instantly** via Telegram
- 🤖 **AI-powered reflections** using Google Gemini
- 📊 **Organize with tags** (`#philosophy #ideas`)
- 🔗 **Link concepts** (`[[Camus]] [[existentialism]]`)
- 📖 **Daily summaries** with deep AI analysis
- 📁 **Obsidian integration** with auto-sync
- 🔍 **Search & statistics** for your notes
- 🔒 **Private & secure** - your data stays yours
- 👥 **Multi-user support** with complete isolation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram account
- Google account (for Gemini API - free tier available)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Philosophy-Notes
```

### 2. Get Your API Keys

#### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Copy the token (looks like `1234567890:ABCdef...`)

#### Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key (looks like `AIzaSy...`)

**Detailed guide**: [docs/GEMINI_SETUP.md](docs/GEMINI_SETUP.md)

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys
nano .env
```

Add your keys:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro
```

### 4. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
# Just the bot
./scripts/start_bot.sh

# Or bot + sync server (for Obsidian integration)
./scripts/start_all.sh
```

### 6. Start Using

1. Find your bot on Telegram (the username you chose)
2. Send `/start`
3. Send `/setup` to complete setup
4. Start sending your thoughts!

## 📖 Usage Examples

### Capture a Note

Just send any message to the bot:

```
Just realized training is like [[Sisyphus]] pushing the boulder #philosophy #training
```

The bot will:
- ✅ Save your note
- 🏷️ Extract tags: `#philosophy #training`
- 🔗 Link concepts: `[[Sisyphus]]`
- 📊 Update your statistics

### Daily Summary

Every evening (default 11 PM), you'll receive:
- 📋 Summary of all your notes from the day
- 🤖 Gemini's philosophical reflection
- 📄 Obsidian-formatted markdown file
- 📊 Tags and concepts from the day

### Commands

```
📝 Note Capture:
   Just send any message!

🔍 Review & Search:
   /today           - Today's notes
   /week            - This week's notes
   /search <term>   - Search your notes
   /stats           - Your statistics

📤 Export & Sync:
   /vault           - Download as ZIP
   /sync            - Get sync token

⚙️ Settings:
   /settings        - View settings
   /help            - Show help
   /about           - About the bot
```

## 🗂️ Project Structure

```
Philosophy-Notes/
├── .env.example         # Environment template (copy to .env)
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── requirements.txt     # Python dependencies
│
├── config.py            # Configuration
├── bot.py               # Main Telegram bot
├── database.py          # Database management
├── gemini_integration.py # Google Gemini AI
├── vault_manager.py     # Obsidian file generator
├── utils.py             # Utility functions
├── sync_server.py       # Flask sync API
├── sync_client.py       # Obsidian sync client
│
├── scripts/             # Management scripts
│   ├── start_bot.sh     # Start just the bot
│   ├── start_all.sh     # Start bot + sync server
│   ├── stop_all.sh      # Stop all services
│   └── status.sh        # Check service status
│
├── docs/                # Documentation
│   ├── GEMINI_SETUP.md  # Gemini API setup guide
│   ├── QUICK_START.md   # 5-minute setup
│   └── ARCHITECTURE.md  # System design
│
└── users/               # User data (auto-created)
    ├── users.db         # User registry
    └── <user_id>/       # Individual user data
        ├── notes.db     # User's notes database
        └── vault/       # Obsidian vault files
```

## 🔄 Obsidian Integration

### Option 1: Manual Sync

1. Send `/vault` to your bot
2. Download the ZIP file
3. Extract to your Obsidian vault folder

### Option 2: Auto-Sync (Recommended)

1. Make sure sync server is running:
   ```bash
   ./scripts/start_all.sh
   ```

2. Get your sync token from the bot:
   ```
   /sync
   ```

3. Run the sync client:
   ```bash
   python3 sync_client.py \
     --token YOUR_TOKEN \
     --vault ~/Documents/ObsidianVault
   ```

4. Keep it running with tmux/screen:
   ```bash
   tmux new -s philosophy-sync
   python3 sync_client.py --token TOKEN --vault PATH
   # Detach: Ctrl+B then D
   ```

## 📊 How It Works

1. **You send a note** via Telegram
2. **Bot parses it** - extracts tags (#) and concepts ([[]])
3. **Saves to SQLite** - in your isolated user database
4. **Daily at 11 PM**:
   - Collects all your notes from the day
   - Sends to Gemini for analysis
   - Generates philosophical reflection
   - Creates Obsidian markdown file
   - Sends summary to you via Telegram
5. **Sync client** (optional) downloads new files to your Obsidian vault

## 🔐 Privacy & Security

- ✅ **Local database** - SQLite, not cloud
- ✅ **User isolation** - each user has separate database
- ✅ **No data mixing** - your notes are completely private
- ✅ **API security** - sync tokens are unique and revocable
- ✅ **Git safe** - `.env` is in `.gitignore`
- ⚠️ **Note**: Your notes are sent to Google Gemini API for analysis

## 🛠️ Management

### Check Status

```bash
./scripts/status.sh
```

### View Logs

```bash
# Bot logs
tail -f logs/bot.log

# Sync server logs
tail -f logs/sync_server.log
```

### Stop Services

```bash
./scripts/stop_all.sh
```

### Restart

```bash
./scripts/stop_all.sh
./scripts/start_all.sh
```

## 🎯 Advanced Configuration

### Change Summary Time

In `.env`:
```bash
DEFAULT_SUMMARY_TIME=21:00  # 9 PM instead of 11 PM
```

### Change Timezone

```bash
DEFAULT_TIMEZONE=America/New_York
```

### Use Claude Instead of Gemini

```bash
ANTHROPIC_API_KEY=sk-ant-your_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514
AI_PROVIDER=claude
```

### Switch Gemini Models

```bash
# For deep analysis (slower, more thoughtful)
GEMINI_MODEL=gemini-1.5-pro

# For faster responses
GEMINI_MODEL=gemini-1.5-flash
```

## 📚 Documentation

- [Gemini API Setup Guide](docs/GEMINI_SETUP.md) - Detailed Gemini configuration
- [Quick Start Guide](docs/QUICK_START.md) - 5-minute setup
- [Architecture Overview](docs/ARCHITECTURE.md) - System design

## 🐛 Troubleshooting

### Bot doesn't respond

```bash
# Check if running
./scripts/status.sh

# Check logs
tail logs/bot.log

# Restart
./scripts/stop_all.sh && ./scripts/start_all.sh
```

### "Invalid API Key"

1. Check `.env` file has correct `GEMINI_API_KEY`
2. Verify key at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Make sure no extra spaces or quotes in `.env`

### Sync not working

1. Verify sync server is running: `./scripts/status.sh`
2. Get new token: `/sync` in Telegram
3. Test manually: `python3 sync_client.py --token TOKEN --vault PATH --once`

### Can't see files in Obsidian

1. Check vault path is correct
2. Reopen Obsidian
3. Use `/vault` and extract manually

## 🚧 Roadmap

- [ ] Weekly synthesis generation
- [ ] Concept page auto-generation
- [ ] Voice note support
- [ ] Image/photo note capture
- [ ] Notion import/export
- [ ] Web interface
- [ ] Mobile app

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Google Gemini** - AI-powered analysis
- **Telegram** - Bot platform
- **Obsidian** - Knowledge management
- **Python Telegram Bot** - Bot framework
- **Flask** - Sync server

## 💬 Support

Having issues? Check:
1. [Troubleshooting section](#-troubleshooting)
2. [Gemini Setup Guide](docs/GEMINI_SETUP.md)
3. [GitHub Issues](../../issues)

---

Built with ❤️ for deep thinkers and philosophy enthusiasts.

**Start capturing your thoughts today!** 🚀🧠
