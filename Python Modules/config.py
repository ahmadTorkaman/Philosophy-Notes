"""
Philosophy Notes Bot - Configuration
"""

import os
from pathlib import Path

# ============================================
# BOT CONFIGURATION
# ============================================

# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Anthropic API Key for Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY_HERE")

# Claude Model
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# ============================================
# PATHS
# ============================================

BASE_DIR = Path(__file__).parent
USERS_DIR = BASE_DIR / "users"
USERS_DIR.mkdir(exist_ok=True)

# ============================================
# TIMEZONE
# ============================================

DEFAULT_TIMEZONE = "Asia/Tehran"
DEFAULT_SUMMARY_TIME = "23:00"  # 11:00 PM

# ============================================
# FEATURES
# ============================================

# Future feature flags (for Phase 2+)
ENABLE_NOTION_IMPORT = False  # Will enable in Phase 2
ENABLE_WEEKLY_SYNTHESIS = False  # Will enable in Phase 2
ENABLE_CONCEPT_PAGES = False  # Will enable in Phase 2

# ============================================
# SYNC SERVER
# ============================================

SYNC_SERVER_HOST = "0.0.0.0"
SYNC_SERVER_PORT = 5000
SYNC_API_BASE = f"http://localhost:{SYNC_SERVER_PORT}"

# ============================================
# USER SETTINGS DEFAULTS
# ============================================

DEFAULT_USER_SETTINGS = {
    "timezone": DEFAULT_TIMEZONE,
    "summary_time": DEFAULT_SUMMARY_TIME,
    "interests": [],
    "export_format": "obsidian",
}

# ============================================
# HELP TEXT
# ============================================

HELP_TEXT = """
📖 *Philosophy Notes Bot - Commands*

📝 *Capture Notes*
Just send me any message - I'll save it automatically!
Use #tags to organize (e.g., #philosophy #ideas)
Use [[concepts]] to link ideas (e.g., [[Camus]])

🔍 *Search & Review*
/today - Today's notes
/week - This week's notes  
/month - This month's notes
/search [term] - Find notes containing term
/tag #philosophy - All notes with specific tag
/stats - Your thinking patterns

📤 *Export & Sync*
/vault - Download your vault as ZIP
/sync - Get sync token for auto-sync

⚙️ *Settings*
/settings - View your settings
/timezone - Set your timezone
/summary_time - Change daily summary time

❓ *Help*
/help - Show this message
/about - About this bot

💡 *Examples*
"Just realized training is like [[Sisyphus]] pushing the boulder #philosophy #training"

"What if [[Ozone]] could reflect [[Wittgenstein]]'s clarity principle? #ozone #design"

"Reading [[Camus]] on absurdism - resonates with my work situation #existentialism #question"
"""

ABOUT_TEXT = """
🧠 *Philosophy Notes Bot*

Your personal AI philosophy assistant powered by Claude.

*What I do:*
• Capture your thoughts throughout the day
• Organize them with tags and concepts
• Analyze with Claude AI every evening
• Create beautiful daily summaries
• Build your personal knowledge graph
• Help you explore ideas over time

*Privacy:*
• Your notes are completely private
• Each user has isolated storage
• Your data never mixes with others
• Export/delete anytime

*Built with:*
• Claude AI by Anthropic
• Python & SQLite
• Obsidian-compatible markdown

Version 1.0 - Phase 1
Created with ❤️ for deep thinkers
"""

WELCOME_TEXT = """
👋 *Welcome to Philosophy Notes Bot!*

I'm your personal AI philosophy assistant. Here's what I do:

📝 Capture your thoughts throughout the day
🧠 Analyze them with Claude AI
📊 Build your personal knowledge graph  
📖 Create beautiful daily summaries
🔍 Help you explore your ideas over time

Everything is completely private - your notes, your vault, your insights.

Ready to begin your philosophy journey?

Type /setup to get started! (takes 30 seconds)
"""

SETUP_COMPLETE_TEXT = """
🎉 *Setup Complete!*

Your personal philosophy vault is ready!

I've created:
✓ Your note database
✓ Your Obsidian vault structure
✓ Your first concept pages

*What's next?*

1️⃣ *Start capturing thoughts*
   Just message me anything!
   Use #tags and [[concepts]]

2️⃣ *Review tonight*
   I'll send your daily summary at {summary_time}
   With Claude's reflection on your thinking

3️⃣ *Sync to Obsidian* (optional)
   Use /sync to get auto-sync instructions

*Example note:*
"Just read about [[Sartre]] and radical freedom. This connects to my thoughts on authenticity #existentialism #philosophy"

What's on your mind? 💭
"""
