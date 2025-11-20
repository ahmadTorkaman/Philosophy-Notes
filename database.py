"""
Philosophy Notes Bot - Database Management
Handles all database operations for users and notes
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import config

class Database:
    """Database manager for a single user"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user_dir = config.USERS_DIR / str(user_id)
        self.user_dir.mkdir(exist_ok=True)
        
        self.db_path = self.user_dir / "notes.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                concepts TEXT,
                note_type TEXT DEFAULT 'thought',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Daily summaries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                note_count INTEGER,
                tags TEXT,
                claude_reflection TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_note(self, content: str, tags: List[str], concepts: List[str], 
                  note_type: str = 'thought') -> int:
        """Save a new note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        tags_json = json.dumps(tags)
        concepts_json = json.dumps(concepts)
        
        cursor.execute("""
            INSERT INTO notes (timestamp, content, tags, concepts, note_type)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, content, tags_json, concepts_json, note_type))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_notes_by_date(self, date: str) -> List[Dict]:
        """Get all notes for a specific date (YYYY-MM-DD)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, content, tags, concepts, note_type
            FROM notes
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp ASC
        """, (date,))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                'id': row[0],
                'timestamp': row[1],
                'content': row[2],
                'tags': json.loads(row[3]) if row[3] else [],
                'concepts': json.loads(row[4]) if row[4] else [],
                'note_type': row[5]
            })
        
        conn.close()
        return notes
    
    def get_notes_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get notes within date range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, content, tags, concepts, note_type
            FROM notes
            WHERE DATE(timestamp) BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_date, end_date))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                'id': row[0],
                'timestamp': row[1],
                'content': row[2],
                'tags': json.loads(row[3]) if row[3] else [],
                'concepts': json.loads(row[4]) if row[4] else [],
                'note_type': row[5]
            })
        
        conn.close()
        return notes
    
    def search_notes(self, query: str, limit: int = 50) -> List[Dict]:
        """Search notes by content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, content, tags, concepts, note_type
            FROM notes
            WHERE content LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f'%{query}%', limit))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                'id': row[0],
                'timestamp': row[1],
                'content': row[2],
                'tags': json.loads(row[3]) if row[3] else [],
                'concepts': json.loads(row[4]) if row[4] else [],
                'note_type': row[5]
            })
        
        conn.close()
        return notes
    
    def get_notes_by_tag(self, tag: str, limit: int = 50) -> List[Dict]:
        """Get all notes with specific tag"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, content, tags, concepts, note_type
            FROM notes
            WHERE tags LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f'%"{tag}"%', limit))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                'id': row[0],
                'timestamp': row[1],
                'content': row[2],
                'tags': json.loads(row[3]) if row[3] else [],
                'concepts': json.loads(row[4]) if row[4] else [],
                'note_type': row[5]
            })
        
        conn.close()
        return notes
    
    def get_stats(self) -> Dict:
        """Get user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total notes
        cursor.execute("SELECT COUNT(*) FROM notes")
        total_notes = cursor.fetchone()[0]
        
        # Notes this week
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) FROM notes WHERE DATE(timestamp) >= ?", (week_ago,))
        notes_this_week = cursor.fetchone()[0]
        
        # Most used tags
        cursor.execute("SELECT tags FROM notes WHERE tags IS NOT NULL AND tags != '[]'")
        all_tags = []
        for row in cursor.fetchall():
            all_tags.extend(json.loads(row[0]))
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Most referenced concepts
        cursor.execute("SELECT concepts FROM notes WHERE concepts IS NOT NULL AND concepts != '[]'")
        all_concepts = []
        for row in cursor.fetchall():
            all_concepts.extend(json.loads(row[0]))
        
        concept_counts = {}
        for concept in all_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        top_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        conn.close()
        
        return {
            'total_notes': total_notes,
            'notes_this_week': notes_this_week,
            'top_tags': top_tags,
            'top_concepts': top_concepts
        }
    
    def save_daily_summary(self, date: str, note_count: int, tags: List[str], 
                          claude_reflection: str):
        """Save daily summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags)
        
        cursor.execute("""
            INSERT OR REPLACE INTO daily_summaries (date, note_count, tags, claude_reflection)
            VALUES (?, ?, ?, ?)
        """, (date, note_count, tags_json, claude_reflection))
        
        conn.commit()
        conn.close()
    
    def get_daily_summary(self, date: str) -> Optional[Dict]:
        """Get daily summary for a specific date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, note_count, tags, claude_reflection
            FROM daily_summaries
            WHERE date = ?
        """, (date,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'date': row[0],
                'note_count': row[1],
                'tags': json.loads(row[2]) if row[2] else [],
                'claude_reflection': row[3]
            }
        return None
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get user setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM user_settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def set_setting(self, key: str, value: str):
        """Set user setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO user_settings (key, value)
            VALUES (?, ?)
        """, (key, value))
        
        conn.commit()
        conn.close()


class UserManager:
    """Manages all users"""
    
    def __init__(self):
        self.users_db_path = config.USERS_DIR / "users.db"
        self.init_database()
    
    def init_database(self):
        """Initialize users database"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                setup_completed INTEGER DEFAULT 0,
                interests TEXT,
                timezone TEXT DEFAULT 'Asia/Tehran',
                summary_time TEXT DEFAULT '23:00',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sync tokens table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_tokens (
                telegram_id INTEGER PRIMARY KEY,
                token TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def user_exists(self, telegram_id: int) -> bool:
        """Check if user exists"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def create_user(self, telegram_id: int, username: str = None, 
                   first_name: str = None) -> bool:
        """Create new user"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (telegram_id, username, first_name)
                VALUES (?, ?, ?)
            """, (telegram_id, username, first_name))
            
            conn.commit()
            
            # Create user's database
            db = Database(telegram_id)
            
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def complete_setup(self, telegram_id: int, interests: List[str]):
        """Mark user setup as complete"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        interests_json = json.dumps(interests)
        
        cursor.execute("""
            UPDATE users 
            SET setup_completed = 1, interests = ?
            WHERE telegram_id = ?
        """, (interests_json, telegram_id))
        
        conn.commit()
        conn.close()
    
    def is_setup_completed(self, telegram_id: int) -> bool:
        """Check if user completed setup"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT setup_completed FROM users WHERE telegram_id = ?
        """, (telegram_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row and row[0] == 1
    
    def update_last_active(self, telegram_id: int):
        """Update user's last active timestamp"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users 
            SET last_active = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
        """, (telegram_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_info(self, telegram_id: int) -> Optional[Dict]:
        """Get user information"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT telegram_id, username, first_name, interests, timezone, summary_time
            FROM users
            WHERE telegram_id = ?
        """, (telegram_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'telegram_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'interests': json.loads(row[3]) if row[3] else [],
                'timezone': row[4],
                'summary_time': row[5]
            }
        return None
    
    def generate_sync_token(self, telegram_id: int) -> str:
        """Generate sync token for user"""
        import secrets
        
        token = secrets.token_urlsafe(32)
        
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO sync_tokens (telegram_id, token)
            VALUES (?, ?)
        """, (telegram_id, token))
        
        conn.commit()
        conn.close()
        
        return token
    
    def verify_token(self, token: str) -> Optional[int]:
        """Verify sync token and return user_id"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT telegram_id FROM sync_tokens WHERE token = ?
        """, (token,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_all_users_for_daily_summary(self) -> List[int]:
        """Get all users who need daily summaries"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT telegram_id FROM users WHERE setup_completed = 1
        """)

        users = [row[0] for row in cursor.fetchall()]
        conn.close()

        return users

    def get_all_users(self) -> List[Dict]:
        """Get all users with full information"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT telegram_id, username, first_name, timezone, summary_time, setup_completed
            FROM users
        """)

        users = []
        for row in cursor.fetchall():
            users.append({
                'telegram_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'timezone': row[3],
                'summary_time': row[4],
                'setup_completed': row[5]
            })

        conn.close()
        return users

    def update_user_timezone(self, telegram_id: int, timezone: str):
        """Update user's timezone setting"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET timezone = ?
            WHERE telegram_id = ?
        """, (timezone, telegram_id))

        conn.commit()
        conn.close()

    def update_user_summary_time(self, telegram_id: int, summary_time: str):
        """Update user's daily summary time"""
        conn = sqlite3.connect(self.users_db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET summary_time = ?
            WHERE telegram_id = ?
        """, (summary_time, telegram_id))

        conn.commit()
        conn.close()
