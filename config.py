"""
Philosophy Notes Bot - Configuration
All configuration settings for the bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# BOT CONFIGURATION
# ============================================

# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    import warnings
    warnings.warn("TELEGRAM_BOT_TOKEN not found in environment variables. Bot features will be disabled.")

# ============================================
# GEMINI API CONFIGURATION
# ============================================

# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    import warnings
    warnings.warn("GEMINI_API_KEY not found. Gemini AI features will be disabled.")

# Gemini Model (default: gemini-1.5-pro)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# ============================================
# OPTIONAL: CLAUDE API (if you want to use Claude instead)
# ============================================

# Uncomment these in .env if you want to use Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

# Choose which AI to use: "gemini" or "claude"
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

# ============================================
# PATHS
# ============================================

BASE_DIR = Path(__file__).parent
USERS_DIR = BASE_DIR / "users"
USERS_DIR.mkdir(exist_ok=True)

# Logs directory
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# ============================================
# TIMEZONE & SCHEDULING
# ============================================

DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Tehran")
DEFAULT_SUMMARY_TIME = os.getenv("DEFAULT_SUMMARY_TIME", "23:00")  # 11:00 PM

# ============================================
# SYNC SERVER
# ============================================

SYNC_SERVER_HOST = os.getenv("SYNC_SERVER_HOST", "0.0.0.0")
SYNC_SERVER_PORT = int(os.getenv("SYNC_SERVER_PORT", "5000"))
SYNC_API_BASE = f"http://localhost:{SYNC_SERVER_PORT}"

# ============================================
# FEATURE FLAGS
# ============================================

# Future features (for Phase 2+)
ENABLE_NOTION_IMPORT = os.getenv("ENABLE_NOTION_IMPORT", "false").lower() == "true"
ENABLE_WEEKLY_SYNTHESIS = os.getenv("ENABLE_WEEKLY_SYNTHESIS", "false").lower() == "true"
ENABLE_CONCEPT_PAGES = os.getenv("ENABLE_CONCEPT_PAGES", "false").lower() == "true"

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

ABOUT_TEXT = f"""
🧠 *Philosophy Notes Bot*

Your personal AI philosophy assistant powered by Google Gemini.

*What I do:*
• Capture your thoughts throughout the day
• Organize them with tags and concepts
• Analyze with Gemini AI every evening
• Create beautiful daily summaries
• Build your personal knowledge graph
• Help you explore ideas over time

*Privacy:*
• Your notes are completely private
• Each user has isolated storage
• Your data never mixes with others
• Export/delete anytime

*Built with:*
• Google Gemini AI
• Python & SQLite
• Obsidian-compatible markdown
• Telegram Bot API

Version 2.0 - Gemini Edition
Created with ❤️ for deep thinkers
"""

WELCOME_TEXT = """
👋 *Welcome to Philosophy Notes Bot!*

I'm your personal AI philosophy assistant powered by Google Gemini. Here's what I do:

📝 Capture your thoughts throughout the day
🧠 Analyze them with Gemini AI
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
✓ Your sync token for Obsidian

*What's next?*

1️⃣ *Start capturing thoughts*
   Just message me anything!
   Use #tags and [[concepts]]

2️⃣ *Review tonight*
   I'll send your daily summary at {summary_time}
   With Gemini's reflection on your thinking

3️⃣ *Sync to Obsidian* (optional)
   Use /sync to get auto-sync instructions

*Example note:*
"Just read about [[Sartre]] and radical freedom. This connects to my thoughts on authenticity #existentialism #philosophy"

What's on your mind? 💭
"""

# ============================================
# VALIDATION
# ============================================

def validate_config():
    """Validate that all required configuration is present"""
    errors = []

    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is required")

    if AI_PROVIDER == "gemini" and not GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is required when using Gemini")

    if AI_PROVIDER == "claude" and not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is required when using Claude")

    if errors:
        raise ValueError("Configuration errors:\n" + "\n".join(f"- {e}" for e in errors))

    return True


# Validate configuration on import
# Disabled for Render deployment - validation happens in bot initialization
# if __name__ != "__main__":
#     validate_config()
