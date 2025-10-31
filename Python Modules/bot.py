"""
Philosophy Bot - Main Telegram Bot
Multi-user bot for capturing philosophy notes
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from database import db
from vault_manager import extract_hashtags, extract_concepts
import os

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

class PhilosophyBot:
    def __init__(self):
        self.app = Application.builder().token(BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("setup", self.cmd_setup))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("today", self.cmd_today))
        self.app.add_handler(CommandHandler("week", self.cmd_week))
        self.app.add_handler(CommandHandler("search", self.cmd_search))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        self.app.add_handler(CommandHandler("sync", self.cmd_sync))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if not db.user_exists(user.id):
            db.create_user(user.id, user.username or "", user.first_name or "User")
            await update.message.reply_text(
                f"👋 Welcome {user.first_name}!\n\n"
                "I'm your philosophy assistant. Type /setup to begin!"
            )
        else:
            await update.message.reply_text(f"Welcome back, {user.first_name}! 👋")
    
    async def cmd_setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        db.update_user(update.effective_user.id, setup_completed=1)
        await update.message.reply_text(
            "🎉 Setup complete!\n\n"
            "Just send me your thoughts anytime.\n"
            "Use #tags and [[concepts]] to organize.\n\n"
            "Example: Just read [[Camus]] #philosophy\n\n"
            "Commands: /help"
        )
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📚 Commands:\n\n"
            "/today - Today's notes\n"
            "/week - This week\n"
            "/search [term] - Search\n"
            "/stats - Statistics\n"
            "/sync - Sync setup\n"
            "/help - This message"
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not db.user_exists(user_id):
            await self.cmd_start(update, context)
            return
        
        content = update.message.text
        tags = extract_hashtags(content)
        concepts = extract_concepts(content)
        
        db.save_note(user_id, content, tags, concepts)
        count = len(db.get_today_notes(user_id))
        
        reply = f"✓ Saved ({count} today)"
        if tags:
            reply += f"\n{' '.join(tags)}"
        
        await update.message.reply_text(reply)
    
    async def cmd_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        notes = db.get_today_notes(update.effective_user.id)
        if not notes:
            await update.message.reply_text("No notes today yet!")
            return
        
        text = f"📝 Today ({len(notes)} notes)\n\n"
        for n in notes[:5]:
            text += f"{n['timestamp'].split()[1][:5]}: {n['content'][:100]}\n\n"
        
        await update.message.reply_text(text)
    
    async def cmd_week(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Implementation here
        await update.message.reply_text("Week view coming soon!")
    
    async def cmd_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Usage: /search term")
            return
        # Implementation here
        await update.message.reply_text("Search coming soon!")
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        stats = db.get_user_stats(update.effective_user.id)
        await update.message.reply_text(
            f"📊 Statistics\n\n"
            f"Total notes: {stats['total_notes']}\n"
            f"This week: {stats['notes_this_week']}"
        )
    
    async def cmd_sync(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = db.get_user(update.effective_user.id)
        await update.message.reply_text(
            f"🔄 Sync Token:\n`{user['sync_token']}`\n\n"
            "Download sync client and run:\n"
            "python3 sync_client.py --token YOUR_TOKEN --vault ~/Vault",
            parse_mode='Markdown'
        )
    
    def run(self):
        logger.info("Starting Philosophy Bot...")
        self.app.run_polling()

if __name__ == "__main__":
    PhilosophyBot().run()
