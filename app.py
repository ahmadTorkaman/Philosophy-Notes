"""
Philosophy Notes Bot - Unified Entry Point for Render.com
Runs both Telegram bot and Flask API server
"""

import os
import sys
import logging
import threading
from pathlib import Path

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# FLASK APP SETUP
# ============================================

app = Flask(__name__)
CORS(app)

# Import after Flask app is created
try:
    from database import UserManager
    from config import USERS_DIR
    user_manager = UserManager()
except Exception as e:
    logger.warning(f"Could not import user manager: {e}")
    user_manager = None

# ============================================
# ROOT ROUTES (for Render health checks)
# ============================================

@app.route('/')
def index():
    """Root endpoint - required for Render.com health checks"""
    return jsonify({
        'service': 'Philosophy Notes Bot',
        'status': 'running',
        'version': '1.0',
        'endpoints': {
            'health': '/health',
            'api_health': '/api/health',
            'sync_status': '/api/sync/<token>/status',
            'sync_file': '/api/sync/<token>/file',
            'vault_zip': '/api/sync/<token>/vault.zip'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'philosophy-bot'})

@app.route('/api/health')
def api_health():
    """API health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'philosophy-bot-api'})

# ============================================
# SYNC API ROUTES
# ============================================

@app.route('/api/sync/<token>/status')
def sync_status(token):
    """Get current vault status for user"""
    if not user_manager:
        return jsonify({'error': 'Service not initialized'}), 503

    # Verify token
    user_id = user_manager.verify_token(token)

    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    # Get vault path
    vault_path = USERS_DIR / str(user_id) / "vault"

    if not vault_path.exists():
        return jsonify({'error': 'Vault not found'}), 404

    # Get all markdown files
    files = []
    for filepath in vault_path.rglob('*.md'):
        rel_path = filepath.relative_to(vault_path)
        files.append({
            'path': str(rel_path),
            'modified': filepath.stat().st_mtime,
            'size': filepath.stat().st_size
        })

    return jsonify({
        'user_id': user_id,
        'file_count': len(files),
        'files': files
    })

@app.route('/api/sync/<token>/file')
def sync_file(token):
    """Download specific file"""
    if not user_manager:
        return jsonify({'error': 'Service not initialized'}), 503

    # Verify token
    user_id = user_manager.verify_token(token)

    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    # Get file path from query
    file_path = request.args.get('path')

    if not file_path:
        return jsonify({'error': 'File path required'}), 400

    # Construct full path
    vault_path = USERS_DIR / str(user_id) / "vault"
    full_path = vault_path / file_path

    # Security check - ensure path is within vault
    try:
        full_path = full_path.resolve()
        vault_path = vault_path.resolve()

        if not str(full_path).startswith(str(vault_path)):
            return jsonify({'error': 'Invalid file path'}), 403
    except:
        return jsonify({'error': 'Invalid file path'}), 403

    if not full_path.exists():
        return jsonify({'error': 'File not found'}), 404

    return send_file(full_path, as_attachment=True)

@app.route('/api/sync/<token>/vault.zip')
def download_vault_zip(token):
    """Download entire vault as ZIP"""
    if not user_manager:
        return jsonify({'error': 'Service not initialized'}), 503

    # Verify token
    user_id = user_manager.verify_token(token)

    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    from vault_manager import VaultManager
    from datetime import datetime

    vault = VaultManager(user_id)
    zip_buffer = vault.create_vault_zip()

    filename = f"philosophy_vault_{datetime.now().strftime('%Y%m%d')}.zip"

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

# ============================================
# BOT RUNNER
# ============================================

def run_flask_server():
    """Run Flask in background thread"""
    port = int(os.getenv('PORT', 5000))
    host = '0.0.0.0'

    logger.info(f"✓ Starting Flask API on {host}:{port}")
    app.run(
        host=host,
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False  # Important: disable reloader in thread
    )

def run_telegram_bot():
    """Run Telegram bot in main thread"""
    try:
        from bot import PhilosophyBot
        logger.info("Starting Telegram Bot...")
        bot = PhilosophyBot()
        logger.info("✓ Bot initialized, starting polling...")
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        logger.exception("Bot error traceback:")
        raise

# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    """Main entry point for Render.com deployment"""
    logger.info("=" * 60)
    logger.info("Philosophy Notes Bot - Starting on Render.com")
    logger.info("=" * 60)

    # Check required environment variables
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')

    if not telegram_token:
        logger.warning("⚠️  TELEGRAM_BOT_TOKEN not set - bot will not function")
    else:
        logger.info("✓ Telegram bot token configured")

    if not gemini_key and not anthropic_key:
        logger.warning("⚠️  No AI API key set - AI summaries will not work")
        logger.warning("⚠️  Set either GEMINI_API_KEY or ANTHROPIC_API_KEY")
    elif gemini_key:
        logger.info("✓ Gemini API key configured")
    elif anthropic_key:
        logger.info("✓ Anthropic API key configured")

    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    logger.info("✓ Flask API thread started")

    # Give Flask a moment to start
    import time
    time.sleep(2)

    logger.info("=" * 60)

    # Run Telegram bot in main thread (needs main thread for signal handlers)
    if telegram_token:
        run_telegram_bot()
    else:
        logger.error("Cannot start bot without TELEGRAM_BOT_TOKEN")
        # Keep Flask running even without bot
        logger.info("Flask API will continue running...")
        while True:
            time.sleep(60)

if __name__ == '__main__':
    main()
