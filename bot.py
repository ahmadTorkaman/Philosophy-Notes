"""
Philosophy Bot - Main Telegram Bot
Multi-user bot for capturing philosophy notes
"""

import logging
import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Local imports
from database import Database, UserManager
from gemini_integration import GeminiAnalyzer
from vault_manager import VaultManager
from utils import extract_hashtags, extract_concepts, format_note_for_display
import config

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOGS_DIR / 'bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PhilosophyBot:
    """Main Telegram bot for philosophy notes"""

    def __init__(self):
        self.app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.user_manager = UserManager()
        self.ai_analyzer = GeminiAnalyzer()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup all command and message handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("setup", self.cmd_setup))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("about", self.cmd_about))
        self.app.add_handler(CommandHandler("today", self.cmd_today))
        self.app.add_handler(CommandHandler("week", self.cmd_week))
        self.app.add_handler(CommandHandler("search", self.cmd_search))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        self.app.add_handler(CommandHandler("sync", self.cmd_sync))
        self.app.add_handler(CommandHandler("vault", self.cmd_vault))

        # Message handler (for notes)
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user

        if not self.user_manager.user_exists(user.id):
            self.user_manager.create_user(user.id, user.username, user.first_name)
            await update.message.reply_text(config.WELCOME_TEXT, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                f"Welcome back, {user.first_name}! 👋\n\n"
                "Send me your thoughts or use /help to see commands."
            )

    async def cmd_setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setup command"""
        user_id = update.effective_user.id

        # Complete setup for user
        self.user_manager.complete_setup(user_id, [])

        # Generate sync token
        sync_token = self.user_manager.generate_sync_token(user_id)

        # Create vault structure
        vault_mgr = VaultManager(user_id)

        await update.message.reply_text(
            config.SETUP_COMPLETE_TEXT.format(
                summary_time=config.DEFAULT_SUMMARY_TIME
            ),
            parse_mode='Markdown'
        )

    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(config.HELP_TEXT, parse_mode='Markdown')

    async def cmd_about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        await update.message.reply_text(config.ABOUT_TEXT, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages (notes)"""
        user_id = update.effective_user.id

        # Check if user exists
        if not self.user_manager.user_exists(user_id):
            await self.cmd_start(update, context)
            return

        # Check if setup is complete
        if not self.user_manager.is_setup_completed(user_id):
            await update.message.reply_text(
                "Please complete setup first! Use /setup"
            )
            return

        # Parse note
        content = update.message.text
        tags = extract_hashtags(content)
        concepts = extract_concepts(content)

        # Save note
        db = Database(user_id)
        note_id = db.save_note(content, tags, concepts)

        # Get today's count
        today = datetime.now().strftime('%Y-%m-%d')
        today_notes = db.get_notes_by_date(today)
        count = len(today_notes)

        # Send confirmation
        reply = f"✓ Saved (note #{count} today)"

        if tags:
            reply += f"\n🏷️ {' '.join(tags)}"

        if concepts:
            reply += f"\n🔗 {', '.join(concepts)}"

        await update.message.reply_text(reply)

        # Update last active
        self.user_manager.update_last_active(user_id)

    async def cmd_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /today command"""
        user_id = update.effective_user.id
        db = Database(user_id)

        today = datetime.now().strftime('%Y-%m-%d')
        notes = db.get_notes_by_date(today)

        if not notes:
            await update.message.reply_text("No notes today yet! Start writing your thoughts.")
            return

        # Format notes for display
        text = f"📝 *Today* ({len(notes)} notes)\n\n"

        for note in notes[:10]:  # Show max 10
            time = note['timestamp'].split('T')[1].split('.')[0][:5]
            content = note['content'][:100]
            if len(note['content']) > 100:
                content += "..."

            text += f"**{time}** - {content}\n\n"

        if len(notes) > 10:
            text += f"_...and {len(notes) - 10} more. Use /vault to see all notes._"

        await update.message.reply_text(text, parse_mode='Markdown')

    async def cmd_week(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /week command"""
        user_id = update.effective_user.id
        db = Database(user_id)

        from datetime import timedelta
        from utils import get_week_date_range

        today = datetime.now().strftime('%Y-%m-%d')
        start_date, end_date = get_week_date_range(today)

        notes = db.get_notes_range(start_date, end_date)

        if not notes:
            await update.message.reply_text("No notes this week yet!")
            return

        # Get stats
        all_tags = set()
        all_concepts = set()
        for note in notes:
            all_tags.update(note.get('tags', []))
            all_concepts.update(note.get('concepts', []))

        text = f"📅 *This Week*\n\n"
        text += f"**Notes:** {len(notes)}\n"
        text += f"**Tags:** {', '.join(sorted(all_tags)[:5]) if all_tags else 'None'}\n"
        text += f"**Concepts:** {', '.join(sorted(all_concepts)[:5]) if all_concepts else 'None'}\n\n"
        text += "Use /vault to download all your notes in Obsidian format."

        await update.message.reply_text(text, parse_mode='Markdown')

    async def cmd_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command"""
        user_id = update.effective_user.id

        if not context.args:
            await update.message.reply_text("Usage: /search <term>\n\nExample: /search Camus")
            return

        query = " ".join(context.args)
        db = Database(user_id)
        notes = db.search_notes(query, limit=10)

        if not notes:
            await update.message.reply_text(f"No notes found for '{query}'")
            return

        text = f"🔍 *Search results for '{query}'*\n\n"
        text += f"Found {len(notes)} notes:\n\n"

        for note in notes[:5]:
            date = note['timestamp'].split('T')[0]
            time = note['timestamp'].split('T')[1].split('.')[0][:5]
            content = note['content'][:80]
            if len(note['content']) > 80:
                content += "..."

            text += f"📅 {date} {time}\n{content}\n\n"

        if len(notes) > 5:
            text += f"_...and {len(notes) - 5} more results_"

        await update.message.reply_text(text, parse_mode='Markdown')

    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        db = Database(user_id)

        stats = db.get_stats()

        text = f"📊 *Your Statistics*\n\n"
        text += f"**Total notes:** {stats['total_notes']}\n"
        text += f"**This week:** {stats['notes_this_week']}\n\n"

        if stats['top_tags']:
            text += "**Top tags:**\n"
            for tag, count in stats['top_tags'][:5]:
                text += f"  • {tag}: {count}\n"
            text += "\n"

        if stats['top_concepts']:
            text += "**Top concepts:**\n"
            for concept, count in stats['top_concepts'][:5]:
                text += f"  • {concept}: {count}\n"

        await update.message.reply_text(text, parse_mode='Markdown')

    async def cmd_sync(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sync command"""
        user_id = update.effective_user.id

        # Get or generate sync token
        token = self.user_manager.generate_sync_token(user_id)

        text = f"🔄 *Sync Setup*\n\n"
        text += f"Your sync token:\n`{token}`\n\n"
        text += f"To sync with Obsidian:\n\n"
        text += f"1. Make sure sync server is running\n"
        text += f"2. Run sync client:\n\n"
        text += f"```\npython3 sync_client.py \\\n"
        text += f"  --token {token} \\\n"
        text += f"  --vault ~/MyVault\n```\n\n"
        text += f"Or download manually with /vault"

        await update.message.reply_text(text, parse_mode='Markdown')

    async def cmd_vault(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /vault command - send vault as ZIP"""
        user_id = update.effective_user.id

        await update.message.reply_text("📦 Preparing your vault... This may take a moment.")

        try:
            vault_mgr = VaultManager(user_id)
            zip_buffer = vault_mgr.create_vault_zip()

            await update.message.reply_document(
                document=zip_buffer,
                filename=f"philosophy_vault_{datetime.now().strftime('%Y%m%d')}.zip",
                caption="📦 Your Philosophy Vault\n\nExtract this to your Obsidian folder!"
            )

        except Exception as e:
            logger.error(f"Error creating vault ZIP: {e}")
            await update.message.reply_text(
                "Sorry, there was an error creating your vault. Please try again later."
            )

    def run(self):
        """Run the bot"""
        logger.info(f"🤖 Philosophy Bot starting...")
        logger.info(f"📡 AI Provider: {config.AI_PROVIDER.upper()}")
        logger.info(f"🗄️  Users directory: {config.USERS_DIR}")

        self.app.run_polling()


if __name__ == "__main__":
    try:
        bot = PhilosophyBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
