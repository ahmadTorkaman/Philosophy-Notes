from flask import Flask, jsonify, send_file, request, abort
from flask_cors import CORS
import zipfile
import io
from pathlib import Path
from database import db

app = Flask(__name__)
CORS(app)

@app.route('/api/sync/<token>/status')
def sync_status(token):
    user_id = db.verify_sync_token(token)
    if not user_id:
        abort(401)
    
    vault_path = Path(f"data/users/{user_id}/vault")
    files = []
    
    if vault_path.exists():
        for f in vault_path.rglob("*.md"):
            files.append({
                'path': str(f.relative_to(vault_path)),
                'modified': f.stat().st_mtime
            })
    
    return jsonify({'files': files})

@app.route('/api/sync/<token>/file')
def sync_file(token):
    user_id = db.verify_sync_token(token)
    if not user_id:
        abort(401)
    
    path = request.args.get('path')
    file_path = Path(f"data/users/{user_id}/vault/{path}")
    
    if not file_path.exists():
        abort(404)
    
    return send_file(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
