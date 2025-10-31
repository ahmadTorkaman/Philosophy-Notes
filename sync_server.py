"""
Philosophy Notes Bot - Sync Server
Flask API for syncing notes with Obsidian
"""

from flask import Flask, jsonify, send_file, request, abort
from flask_cors import CORS
import zipfile
import io
from pathlib import Path
import logging

# Local imports
from database import UserManager
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOGS_DIR / 'sync_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# User manager
user_manager = UserManager()


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'philosophy-notes-sync'})


@app.route('/api/sync/<token>/status')
def sync_status(token):
    """Get sync status - list of files and their timestamps"""
    user_id = user_manager.verify_token(token)

    if not user_id:
        logger.warning(f"Invalid token attempt: {token[:10]}...")
        abort(401, description="Invalid sync token")

    vault_path = config.USERS_DIR / str(user_id) / "vault"
    files = []

    if vault_path.exists():
        for f in vault_path.rglob("*.md"):
            files.append({
                'path': str(f.relative_to(vault_path)),
                'modified': f.stat().st_mtime
            })

    logger.info(f"Sync status requested by user {user_id}: {len(files)} files")
    return jsonify({'files': files, 'count': len(files)})


@app.route('/api/sync/<token>/file')
def sync_file(token):
    """Get a specific file"""
    user_id = user_manager.verify_token(token)

    if not user_id:
        logger.warning(f"Invalid token attempt: {token[:10]}...")
        abort(401, description="Invalid sync token")

    path = request.args.get('path')
    if not path:
        abort(400, description="Missing 'path' parameter")

    # Security: prevent directory traversal
    if '..' in path or path.startswith('/'):
        logger.warning(f"Directory traversal attempt by user {user_id}: {path}")
        abort(400, description="Invalid path")

    file_path = config.USERS_DIR / str(user_id) / "vault" / path

    if not file_path.exists():
        logger.warning(f"File not found for user {user_id}: {path}")
        abort(404, description="File not found")

    logger.info(f"File requested by user {user_id}: {path}")
    return send_file(file_path)


@app.route('/api/sync/<token>/vault.zip')
def sync_vault_zip(token):
    """Get entire vault as ZIP file"""
    user_id = user_manager.verify_token(token)

    if not user_id:
        logger.warning(f"Invalid token attempt: {token[:10]}...")
        abort(401, description="Invalid sync token")

    vault_path = config.USERS_DIR / str(user_id) / "vault"

    if not vault_path.exists():
        abort(404, description="Vault not found")

    # Create ZIP in memory
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in vault_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(vault_path)
                zip_file.write(file_path, arcname=arcname)

    zip_buffer.seek(0)

    logger.info(f"Vault ZIP requested by user {user_id}")

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'philosophy_vault_{user_id}.zip'
    )


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({'error': 'Unauthorized', 'message': str(e)}), 401


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not Found', 'message': str(e)}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad Request', 'message': str(e)}), 400


if __name__ == '__main__':
    logger.info(f"🚀 Starting Philosophy Notes Sync Server")
    logger.info(f"📡 Host: {config.SYNC_SERVER_HOST}")
    logger.info(f"🔌 Port: {config.SYNC_SERVER_PORT}")

    app.run(
        host=config.SYNC_SERVER_HOST,
        port=config.SYNC_SERVER_PORT,
        debug=False
    )
