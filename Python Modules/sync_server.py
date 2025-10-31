"""
Philosophy Notes Bot - Sync Server
Flask API for sync client to download vault files
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from pathlib import Path
import config
from database import UserManager

app = Flask(__name__)
CORS(app)

user_manager = UserManager()

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'philosophy-bot-sync'})

@app.route('/api/sync/<token>/status')
def sync_status(token):
    """Get current vault status for user"""
    # Verify token
    user_id = user_manager.verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    # Get vault path
    vault_path = config.USERS_DIR / str(user_id) / "vault"
    
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
    # Verify token
    user_id = user_manager.verify_token(token)
    
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    
    # Get file path from query
    file_path = request.args.get('path')
    
    if not file_path:
        return jsonify({'error': 'File path required'}), 400
    
    # Construct full path
    vault_path = config.USERS_DIR / str(user_id) / "vault"
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

def run_sync_server():
    """Run the sync server"""
    print("=" * 60)
    print("Philosophy Bot Sync Server")
    print("=" * 60)
    print(f"Running on http://{config.SYNC_SERVER_HOST}:{config.SYNC_SERVER_PORT}")
    print(f"API Base: {config.SYNC_API_BASE}")
    print("\nEndpoints:")
    print("  GET /api/health")
    print("  GET /api/sync/<token>/status")
    print("  GET /api/sync/<token>/file?path=<path>")
    print("  GET /api/sync/<token>/vault.zip")
    print("=" * 60)
    
    app.run(
        host=config.SYNC_SERVER_HOST,
        port=config.SYNC_SERVER_PORT,
        debug=False
    )

if __name__ == '__main__':
    run_sync_server()
