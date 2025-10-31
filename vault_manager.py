"""
Philosophy Notes Bot - Vault Manager
Generates Obsidian-compatible markdown files
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict
import zipfile
import io
import config

class VaultManager:
    """Manages Obsidian vault creation and updates"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.vault_path = config.USERS_DIR / str(user_id) / "vault"
        self.vault_path.mkdir(exist_ok=True)
        
        # Create vault structure
        self._init_vault_structure()
    
    def _init_vault_structure(self):
        """Initialize Obsidian vault folder structure"""
        folders = [
            "Daily Notes",
            "Concepts",
            "Weekly Reviews",
            "Tags",
        ]
        
        for folder in folders:
            (self.vault_path / folder).mkdir(exist_ok=True)
    
    def create_daily_note(self, date: str, notes: List[Dict], 
                         claude_reflection: str) -> Path:
        """Create daily note in Obsidian format"""
        
        # Extract all tags and concepts
        all_tags = set()
        all_concepts = set()
        
        for note in notes:
            all_tags.update(note.get('tags', []))
            all_concepts.update(note.get('concepts', []))
        
        # Create frontmatter
        frontmatter = f"""---
date: {date}
type: daily-note
tags: [{', '.join(sorted(all_tags))}]
note_count: {len(notes)}
---

"""
        
        # Create header
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        readable_date = date_obj.strftime('%B %d, %Y')
        
        content = f"""# {readable_date}

"""
        
        # Add notes section
        content += "## Your Notes\n\n"
        
        for note in notes:
            time = note['timestamp'].split('T')[1].split('.')[0][:5]  # HH:MM
            note_content = note['content']
            note_tags = note.get('tags', [])
            
            # Format the note
            content += f"**{time}**"
            if note_tags:
                content += f" {' '.join(note_tags)}"
            content += f"\n{note_content}\n\n"
        
        # Add Claude's reflection
        content += "---\n\n## Claude's Reflection\n\n"
        content += claude_reflection
        content += "\n\n---\n\n"
        
        # Add metadata
        if all_tags:
            content += f"**Tags used today:** {' '.join(sorted(all_tags))}\n\n"
        
        if all_concepts:
            concepts_linked = [f"[[{c}]]" for c in sorted(all_concepts)]
            content += f"**Concepts referenced:** {', '.join(concepts_linked)}\n\n"
        
        # Write file
        filename = f"{date}.md"
        filepath = self.vault_path / "Daily Notes" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        return filepath
    
    def create_weekly_review(self, week_start: str, week_end: str, 
                            notes: List[Dict], claude_synthesis: str) -> Path:
        """Create weekly review note"""
        
        # Extract all tags and concepts
        all_tags = set()
        all_concepts = set()
        
        for note in notes:
            all_tags.update(note.get('tags', []))
            all_concepts.update(note.get('concepts', []))
        
        # Parse dates
        start_obj = datetime.strptime(week_start, '%Y-%m-%d')
        end_obj = datetime.strptime(week_end, '%Y-%m-%d')
        
        week_num = start_obj.isocalendar()[1]
        year = start_obj.year
        
        # Frontmatter
        frontmatter = f"""---
type: weekly-review
week: {year}-W{week_num:02d}
start_date: {week_start}
end_date: {week_end}
note_count: {len(notes)}
---

"""
        
        # Content
        content = f"""# Week {week_num} - {start_obj.strftime('%B %d')} to {end_obj.strftime('%B %d, %Y')}

## Overview

This week you recorded {len(notes)} thoughts across {len(all_tags)} topics.

**Topics explored:** {', '.join(sorted(all_tags)) if all_tags else 'None'}

**Concepts referenced:** {', '.join(f'[[{c}]]' for c in sorted(all_concepts)) if all_concepts else 'None'}

---

## Claude's Weekly Synthesis

{claude_synthesis}

---

## Daily Notes

"""
        
        # Link to daily notes
        current_date = start_obj
        while current_date <= end_obj:
            date_str = current_date.strftime('%Y-%m-%d')
            readable = current_date.strftime('%A, %B %d')
            content += f"- [[{date_str}|{readable}]]\n"
            current_date += timedelta(days=1)
        
        # Write file
        filename = f"{year}-W{week_num:02d}.md"
        filepath = self.vault_path / "Weekly Reviews" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        return filepath
    
    def create_concept_page(self, concept: str, related_notes: List[Dict]) -> Path:
        """Create a concept page with backlinks"""
        
        # Frontmatter
        frontmatter = f"""---
type: concept
concept: {concept}
note_count: {len(related_notes)}
---

"""
        
        # Content
        content = f"""# {concept}

## Notes mentioning {concept}

"""
        
        # Add related notes
        for note in related_notes:
            date = note['timestamp'].split('T')[0]
            time = note['timestamp'].split('T')[1].split('.')[0][:5]
            note_content = note['content']
            
            content += f"### [[{date}]] - {time}\n\n"
            content += f"{note_content}\n\n"
        
        content += "---\n\n"
        content += f"*This concept appears in {len(related_notes)} note(s)*\n"
        
        # Write file
        safe_filename = concept.replace('/', '-').replace('\\', '-')
        filename = f"{safe_filename}.md"
        filepath = self.vault_path / "Concepts" / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        return filepath
    
    def create_vault_zip(self) -> io.BytesIO:
        """Create ZIP file of entire vault"""
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Walk through vault directory
            for file_path in self.vault_path.rglob('*'):
                if file_path.is_file():
                    # Get relative path for ZIP
                    arcname = file_path.relative_to(self.vault_path)
                    zip_file.write(file_path, arcname=arcname)
        
        zip_buffer.seek(0)
        return zip_buffer
    
    def get_vault_stats(self) -> Dict:
        """Get statistics about the vault"""
        
        stats = {
            'daily_notes': len(list((self.vault_path / "Daily Notes").glob('*.md'))),
            'concept_pages': len(list((self.vault_path / "Concepts").glob('*.md'))),
            'weekly_reviews': len(list((self.vault_path / "Weekly Reviews").glob('*.md'))),
            'total_files': len(list(self.vault_path.rglob('*.md')))
        }
        
        return stats


# Import timedelta
from datetime import timedelta
