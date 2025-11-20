"""
Philosophy Notes Bot - Daily Summary Scheduler
Automatically generates and sends daily summaries at user-configured times
"""

import logging
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Optional
import pytz

logger = logging.getLogger(__name__)


class DailySummaryScheduler:
    """Manages automated daily summaries for all users"""

    def __init__(self, bot_instance):
        """
        Initialize scheduler with bot instance

        Args:
            bot_instance: The PhilosophyBot instance for sending messages
        """
        self.bot = bot_instance
        self.running = False
        self.thread = None

    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            logger.warning("Scheduler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("✓ Daily summary scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Daily summary scheduler stopped")

    def _run_scheduler(self):
        """Main scheduler loop - runs every minute to check for pending summaries"""
        logger.info("Scheduler thread running...")

        # Schedule the check to run every minute
        schedule.every(1).minutes.do(self._check_and_send_summaries)

        while self.running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds

    def _check_and_send_summaries(self):
        """Check all users and send summaries if it's their scheduled time"""
        try:
            from database import UserManager, Database
            from gemini_integration import GeminiAnalyzer
            from datetime import datetime
            import asyncio

            user_manager = UserManager()

            # Get all active users
            all_users = user_manager.get_all_users()

            for user in all_users:
                try:
                    user_id = user['telegram_id']
                    timezone = user.get('timezone', 'Asia/Tehran')
                    summary_time = user.get('summary_time', '23:00')

                    # Check if it's time for this user's summary
                    if self._is_summary_time(timezone, summary_time):
                        logger.info(f"Generating daily summary for user {user_id}")
                        self._generate_and_send_summary(user_id, timezone)

                except Exception as e:
                    logger.error(f"Error processing user {user.get('telegram_id')}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error in summary check: {e}")
            logger.exception("Scheduler error:")

    def _is_summary_time(self, timezone_str: str, summary_time: str) -> bool:
        """
        Check if current time matches the user's summary time

        Args:
            timezone_str: User's timezone (e.g., 'Asia/Tehran')
            summary_time: User's preferred time (e.g., '23:00')

        Returns:
            True if it's time to send summary
        """
        try:
            # Get current time in user's timezone
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)

            # Parse summary time
            hour, minute = map(int, summary_time.split(':'))

            # Check if current time matches (within 1 minute window)
            return (current_time.hour == hour and
                    current_time.minute == minute)

        except Exception as e:
            logger.error(f"Error checking time for {timezone_str} {summary_time}: {e}")
            return False

    def _generate_and_send_summary(self, user_id: int, timezone_str: str):
        """
        Generate daily summary and send to user

        Args:
            user_id: Telegram user ID
            timezone_str: User's timezone
        """
        try:
            from database import Database
            from gemini_integration import GeminiAnalyzer
            from vault_manager import VaultManager
            import asyncio

            # Get today's date in user's timezone
            tz = pytz.timezone(timezone_str)
            today = datetime.now(tz).strftime('%Y-%m-%d')

            # Get user's notes from today
            db = Database(user_id)
            notes = db.get_notes_by_date(today)

            if not notes:
                logger.info(f"No notes for user {user_id} on {today}, skipping summary")
                return

            # Generate AI summary
            logger.info(f"Generating AI summary for {len(notes)} notes...")
            ai = GeminiAnalyzer()
            summary_text = ai.generate_daily_reflection(notes, today)

            # Extract tags and concepts
            all_tags = set()
            all_concepts = set()
            for note in notes:
                all_tags.update(note.get('tags', []))
                all_concepts.update(note.get('concepts', []))

            # Save summary to database
            db.save_daily_summary(
                date=today,
                note_count=len(notes),
                tags=list(all_tags),
                concepts=list(all_concepts),
                summary=summary_text
            )

            # Update vault
            vault = VaultManager(user_id)
            vault.create_daily_note(today, notes, summary_text)

            # Send to user via Telegram
            message = f"🌙 *Daily Reflection for {today}*\n\n{summary_text}\n\n"
            message += f"📊 *Stats:* {len(notes)} notes, {len(all_tags)} tags, {len(all_concepts)} concepts"

            # Send via bot's async method
            asyncio.run(self._send_telegram_message(user_id, message))

            logger.info(f"✓ Daily summary sent to user {user_id}")

        except Exception as e:
            logger.error(f"Error generating summary for user {user_id}: {e}")
            logger.exception("Summary generation error:")

    async def _send_telegram_message(self, user_id: int, message: str):
        """
        Send message via Telegram bot

        Args:
            user_id: Telegram user ID
            message: Message text to send
        """
        try:
            await self.bot.app.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending Telegram message to {user_id}: {e}")


def create_scheduler(bot_instance):
    """
    Factory function to create and start scheduler

    Args:
        bot_instance: The PhilosophyBot instance

    Returns:
        DailySummaryScheduler instance
    """
    scheduler = DailySummaryScheduler(bot_instance)
    scheduler.start()
    return scheduler
