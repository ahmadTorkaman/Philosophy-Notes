"""
Philosophy Notes Bot - Utilities
Helper functions for note parsing and text processing
"""

import re
from typing import List, Tuple


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text"""
    # Match #word patterns
    hashtag_pattern = r'#(\w+)'
    hashtags = re.findall(hashtag_pattern, text)

    # Return unique hashtags with # prefix
    return [f"#{tag}" for tag in hashtags]


def extract_concepts(text: str) -> List[str]:
    """Extract [[concept]] wikilinks from text"""
    # Match [[text]] patterns
    concept_pattern = r'\[\[([^\]]+)\]\]'
    concepts = re.findall(concept_pattern, text)

    # Return unique concepts
    return list(set(concepts))


def detect_note_type(text: str) -> str:
    """Detect the type of note based on content"""
    text_lower = text.lower()

    # Quote detection
    if '"' in text or '"' in text or '"' in text or "'" in text or "'" in text:
        if any(word in text_lower for word in ['said', 'wrote', 'stated', ' - ']):
            return 'quote'

    # Question detection
    if '?' in text:
        return 'question'

    # Idea detection
    if any(word in text_lower for word in ['what if', 'idea:', 'maybe', 'could', 'should']):
        return 'idea'

    # Dream detection
    if any(word in text_lower for word in ['dream', 'dreamt', 'dreamed', 'nightmare']):
        return 'dream'

    # Default to thought
    return 'thought'


def parse_note(text: str) -> Tuple[str, List[str], List[str], str]:
    """
    Parse a note and extract all metadata

    Returns:
        (content, tags, concepts, note_type)
    """
    content = text.strip()
    tags = extract_hashtags(content)
    concepts = extract_concepts(content)
    note_type = detect_note_type(content)

    return content, tags, concepts, note_type


def format_note_for_display(note: dict, include_time: bool = True) -> str:
    """Format a note for display in Telegram"""
    timestamp = note['timestamp']
    content = note['content']
    tags = note.get('tags', [])
    concepts = note.get('concepts', [])

    if include_time:
        time = timestamp.split('T')[1].split('.')[0][:5]  # HH:MM
        date = timestamp.split('T')[0]
        display = f"📅 {date} {time}\n"
    else:
        display = ""

    display += f"{content}\n"

    if tags:
        display += f"\n🏷️ {' '.join(tags)}"

    if concepts:
        display += f"\n🔗 {', '.join(concepts)}"

    return display


def create_markdown_list(items: List[str], bullet: str = "-") -> str:
    """Create markdown list from items"""
    if not items:
        return "None"

    return "\n".join([f"{bullet} {item}" for item in items])


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text

    return text[:max_length-3] + "..."


def format_date_readable(date_str: str) -> str:
    """Format YYYY-MM-DD to readable format"""
    from datetime import datetime

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str


def get_week_date_range(date_str: str) -> Tuple[str, str]:
    """Get start and end dates for the week containing date_str"""
    from datetime import datetime, timedelta

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # Get Monday of the week
    start_of_week = date_obj - timedelta(days=date_obj.weekday())

    # Get Sunday of the week
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')


def get_month_date_range(date_str: str) -> Tuple[str, str]:
    """Get start and end dates for the month containing date_str"""
    from datetime import datetime
    from calendar import monthrange

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    # First day of month
    start_of_month = date_obj.replace(day=1)

    # Last day of month
    last_day = monthrange(date_obj.year, date_obj.month)[1]
    end_of_month = date_obj.replace(day=last_day)

    return start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be safe for file systems"""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')

    return filename


def escape_markdown(text: str) -> str:
    """Escape markdown special characters for Telegram"""
    # Characters that need escaping in Telegram's MarkdownV2
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    return text
