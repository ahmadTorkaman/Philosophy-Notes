# Philosophy Notes Bot - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User A (Telegram)                 User B (Telegram)            │
│       │                                  │                      │
│       │ Notes                            │ Notes                │
│       ├─────────────┐                    ├─────────────┐        │
│       │             │                    │             │        │
│       ▼             │                    ▼             │        │
│  ┌─────────────┐    │               ┌─────────────┐   │        │
│  │  Obsidian   │◄───┼───sync────────┤  Obsidian   │◄──┼────    │
│  │   Vault A   │    │               │   Vault B   │   │        │
│  └─────────────┘    │               └─────────────┘   │        │
│                     │                                 │        │
└─────────────────────┼─────────────────────────────────┼────────┘
                      │                                 │
                      │                                 │
┌─────────────────────┼─────────────────────────────────┼────────┐
│                     │    BOT LAYER                    │        │
├─────────────────────┼─────────────────────────────────┼────────┤
│                     │                                 │        │
│                     ▼                                 ▼        │
│              ┌──────────────────────────────────────────┐      │
│              │      Telegram Bot (bot.py)              │      │
│              │  - Message handling                      │      │
│              │  - Command processing                    │      │
│              │  - User management                       │      │
│              │  - Scheduled tasks                       │      │
│              └──────────────────────────────────────────┘      │
│                     │                │                         │
│                     │                │                         │
│         ┌───────────┴──┐        ┌───┴──────────┐              │
│         │              │        │               │              │
│         ▼              ▼        ▼               ▼              │
│   ┌──────────┐   ┌─────────────────┐    ┌──────────────┐     │
│   │ Database │   │ Claude AI       │    │ Vault        │     │
│   │ Manager  │   │ Integration     │    │ Manager      │     │
│   └──────────┘   └─────────────────┘    └──────────────┘     │
│         │              │                        │              │
└─────────┼──────────────┼────────────────────────┼──────────────┘
          │              │                        │
          │              │                        │
┌─────────┼──────────────┼────────────────────────┼──────────────┐
│         │     STORAGE & API LAYER               │              │
├─────────┼──────────────┼────────────────────────┼──────────────┤
│         │              │                        │              │
│         ▼              ▼                        ▼              │
│   ┌──────────────────────────────────────────────────────┐    │
│   │           User Data Storage                          │    │
│   │                                                       │    │
│   │  users/                                               │    │
│   │  ├── users.db (central registry)                     │    │
│   │  ├── user_123456789/                                 │    │
│   │  │   ├── notes.db                                    │    │
│   │  │   └── vault/                                      │    │
│   │  │       ├── Daily Notes/                            │    │
│   │  │       ├── Concepts/                               │    │
│   │  │       └── Weekly Reviews/                         │    │
│   │  └── user_987654321/                                 │    │
│   │      ├── notes.db                                    │    │
│   │      └── vault/                                      │    │
│   │          └── ...                                     │    │
│   └──────────────────────────────────────────────────────┘    │
│                                                                │
│   ┌──────────────────────────────────────────────────────┐    │
│   │       Sync Server (Flask API)                        │    │
│   │  Endpoints:                                           │    │
│   │  - GET  /api/sync/<token>/status                     │    │
│   │  - GET  /api/sync/<token>/file?path=X                │    │
│   │  - GET  /api/sync/<token>/vault.zip                  │    │
│   └──────────────────────────────────────────────────────┘    │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               │ HTTP
                               │
┌──────────────────────────────┼─────────────────────────────────┐
│                              ▼   CLIENT LAYER                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────┐          │
│   │  Sync Client (philosophy_sync.py)               │          │
│   │  - Polls server for updates                     │          │
│   │  - Downloads new/changed files                  │          │
│   │  - Writes to local Obsidian vault               │          │
│   └─────────────────────────────────────────────────┘          │
│                              │                                  │
│                              │ File writes                      │
│                              ▼                                  │
│                    User's Local Obsidian Vault                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. Note Capture Flow

```
User sends message in Telegram
         │
         ▼
Telegram Bot receives message
         │
         ▼
Parse note (extract #tags, [[concepts]])
         │
         ▼
Save to user's SQLite database
         │
         ▼
Confirm to user with metadata
```

### 2. Daily Summary Flow

```
11 PM Tehran time (scheduled)
         │
         ▼
For each user:
  │
  ├─ Get today's notes from database
  │
  ├─ Send to Claude API for reflection
  │      │
  │      ▼
  │  Claude analyzes and generates insight
  │      │
  │      ▼
  │  Return reflection text
  │
  ├─ Create Obsidian markdown file
  │      │
  │      ├─ Frontmatter (YAML)
  │      ├─ User's notes
  │      ├─ Claude's reflection
  │      └─ Metadata
  │
  ├─ Save to user's vault/
  │
  └─ Send file to user via Telegram
```

### 3. Sync Flow

```
User's Sync Client running
         │
         ├─ Every hour (or custom interval)
         │
         ▼
Poll Sync Server API
         │
         ├─ GET /api/sync/<token>/status
         │
         ▼
Get list of files and timestamps
         │
         ▼
Compare with local state
         │
         ├─ New files?
         ├─ Modified files?
         │
         ▼
Download changed files
         │
         ├─ GET /api/sync/<token>/file?path=X
         │
         ▼
Write to local Obsidian vault
         │
         ▼
Update local state
         │
         ▼
Done! Obsidian auto-detects new files
```

---

## 🗄️ Database Schema

### Central Users Database (`users.db`)

```sql
users
├─ telegram_id (PRIMARY KEY)
├─ username
├─ first_name
├─ setup_completed
├─ interests (JSON)
├─ timezone
├─ summary_time
├─ created_at
└─ last_active

sync_tokens
├─ telegram_id (FOREIGN KEY)
├─ token (UNIQUE)
└─ created_at
```

### Per-User Database (`users/{user_id}/notes.db`)

```sql
notes
├─ id (PRIMARY KEY)
├─ timestamp
├─ content
├─ tags (JSON)
├─ concepts (JSON)
├─ note_type
└─ created_at

daily_summaries
├─ id (PRIMARY KEY)
├─ date (UNIQUE)
├─ note_count
├─ tags (JSON)
├─ claude_reflection (TEXT)
└─ created_at

user_settings
├─ key (PRIMARY KEY)
└─ value
```

---

## 🔐 Security & Isolation

### Multi-User Isolation

1. **Database Level**
   - Each user has separate SQLite database
   - No shared tables between users
   - Users table only stores metadata

2. **File System Level**
   - Each user has separate directory
   - Path: `users/{telegram_id}/`
   - No access to other users' files

3. **API Level**
   - Sync tokens are unique per user
   - Token verification before any operation
   - Path traversal protection

### Data Protection

- SQLite databases are local (not cloud)
- Vault files are server-side only (not shared)
- Telegram messages encrypted in transit
- Claude API calls use HTTPS
- No logging of note content

---

## 📦 Module Responsibilities

### `bot.py` (Main Bot)
- Telegram message handling
- Command processing (`/start`, `/help`, etc.)
- User onboarding flow
- Scheduled daily summaries
- Message parsing and note capture

### `database.py` (Data Layer)
- User registration and management
- Note CRUD operations
- Search and filtering
- Statistics generation
- Sync token management

### `claude_integration.py` (AI Layer)
- Claude API communication
- Daily reflection generation
- Trend analysis
- Question answering (Phase 2)

### `vault_manager.py` (File Generation)
- Obsidian markdown creation
- Daily note formatting
- Weekly review generation (Phase 2)
- Concept page creation (Phase 2)
- ZIP file creation

### `sync_server.py` (Sync API)
- Flask REST API
- Token verification
- File serving
- Status endpoints

### `philosophy_sync.py` (Client)
- Server polling
- File downloading
- Local state management
- Obsidian vault updates

### `utils.py` (Utilities)
- Text parsing (#tags, [[concepts]])
- Note type detection
- Date formatting
- Markdown utilities

### `config.py` (Configuration)
- Environment variables
- Default settings
- Feature flags
- Help text

---

## 🚀 Deployment Options

### 1. Local Development

```
User's Computer:
├─ bot.py (running)
├─ sync_server.py (running)
└─ users/ (local storage)

User's Computer (same or different):
└─ philosophy_sync.py (connecting to localhost)
    └─ Writes to Obsidian vault
```

### 2. VPS Deployment (Recommended)

```
VPS Server:
├─ bot.py (systemd service)
├─ sync_server.py (systemd service)
└─ users/ (persistent storage)
         │
         │ HTTPS/WSS
         │
User's Computer:
└─ philosophy_sync.py (connecting to server)
    └─ Writes to Obsidian vault
```

### 3. Docker Deployment

```
Docker Container:
├─ bot.py
├─ sync_server.py
└─ Volume mount: ./users/
         │
         │
User's Computer:
└─ philosophy_sync.py
    └─ Obsidian vault
```

---

## 🔧 Extensibility (Phase 2+)

### Planned Enhancements

**Database:**
- Add `concepts` table for concept pages
- Add `relationships` table for concept links
- Add `weekly_summaries` table

**Vault Structure:**
- Auto-generate concept pages
- Create weekly review files
- Build tag index pages
- Generate graph data

**Claude Integration:**
- `/ask` command for conversations
- Weekly synthesis generation
- Concept explanations
- Connection discovery

**Import/Export:**
- Notion import
- Roam Research import
- Standard markdown import
- PDF export with formatting

---

## 📊 Performance Characteristics

**Scalability:**
- SQLite: Good for ~100 concurrent users per database
- Can shard by user (already implemented)
- Each user's data is independent
- No blocking operations

**Storage:**
- ~1 MB per user per month (average)
- Markdown files are tiny
- SQLite databases are compact
- Can add cleanup for old data

**API Rate Limits:**
- Claude API: Depends on your tier
- Telegram: 30 messages/second per bot
- Sync Server: No built-in limits (add if needed)

---

## 🎯 Design Principles

1. **Privacy First**: User data never mixes
2. **Local Control**: SQLite, not cloud databases
3. **Simple & Reliable**: Minimal dependencies
4. **Extensible**: Feature flags for gradual rollout
5. **Obsidian-Native**: Full compatibility
6. **AI-Powered**: Claude for deep insights
7. **User-Friendly**: Natural note capture

---

This architecture supports:
- ✅ Multiple users with complete isolation
- ✅ Real-time note capture
- ✅ Daily AI analysis
- ✅ Obsidian sync
- ✅ Easy deployment
- ✅ Future expansion

Next: Phase 2 features! 🚀
