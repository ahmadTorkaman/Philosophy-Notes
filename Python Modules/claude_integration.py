"""
Philosophy Notes Bot - Claude Integration
Handles all Claude API interactions for note analysis
"""

import anthropic
from typing import List, Dict
import config

class ClaudeAnalyzer:
    """Handles Claude AI analysis of notes"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.CLAUDE_MODEL
    
    def generate_daily_reflection(self, notes: List[Dict], date: str) -> str:
        """Generate daily reflection on notes"""
        
        # Format notes for Claude
        notes_text = self._format_notes_for_claude(notes)
        
        prompt = f"""You are a philosophical companion analyzing someone's daily thoughts and notes from {date}.

Here are their notes from today:

{notes_text}

Please provide a thoughtful reflection on their thinking today. Your reflection should:

1. **Identify key themes** - What were they thinking about?
2. **Find connections** - How do their thoughts relate to each other?
3. **Philosophical context** - Connect their ideas to relevant philosophical concepts, thinkers, or traditions
4. **Patterns** - Any recurring questions, tensions, or insights?
5. **Questions to explore** - What deeper questions emerged? What might be worth exploring further?

Write in a warm, insightful tone - like a thoughtful friend who understands philosophy. Be specific to their actual notes, not generic. Keep it concise but meaningful (300-500 words).

Format your response as:

## Key Themes
[2-3 sentences]

## Connections & Insights  
[Main body - 2-3 paragraphs analyzing their thinking]

## Questions to Explore
- [Question 1]
- [Question 2]
- [Question 3]

## Philosophical Context
[1-2 sentences connecting to relevant philosophy, if applicable]
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
        
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return self._generate_fallback_reflection(notes)
    
    def _format_notes_for_claude(self, notes: List[Dict]) -> str:
        """Format notes into readable text for Claude"""
        if not notes:
            return "No notes recorded today."
        
        formatted = []
        
        for note in notes:
            time = note['timestamp'].split('T')[1].split('.')[0][:5]  # HH:MM
            content = note['content']
            tags = note.get('tags', [])
            concepts = note.get('concepts', [])
            
            note_text = f"**{time}**"
            
            if tags:
                note_text += f" {' '.join(tags)}"
            
            note_text += f"\n{content}"
            
            if concepts:
                note_text += f"\n_Concepts: {', '.join(concepts)}_"
            
            formatted.append(note_text)
        
        return "\n\n".join(formatted)
    
    def _generate_fallback_reflection(self, notes: List[Dict]) -> str:
        """Generate simple reflection if Claude API fails"""
        note_count = len(notes)
        
        # Extract tags and concepts
        all_tags = []
        all_concepts = []
        
        for note in notes:
            all_tags.extend(note.get('tags', []))
            all_concepts.extend(note.get('concepts', []))
        
        unique_tags = list(set(all_tags))
        unique_concepts = list(set(all_concepts))
        
        reflection = f"""## Daily Summary

Today you recorded {note_count} thought{'s' if note_count != 1 else ''}.
"""
        
        if unique_tags:
            reflection += f"\n**Topics explored:** {', '.join(unique_tags[:5])}"
        
        if unique_concepts:
            reflection += f"\n**Concepts referenced:** {', '.join(unique_concepts[:5])}"
        
        reflection += "\n\n*Note: Unable to generate detailed reflection. Your notes are saved and available for review.*"
        
        return reflection
    
    def analyze_trends(self, notes: List[Dict], timeframe: str = "week") -> str:
        """Analyze thinking patterns over time"""
        
        notes_text = self._format_notes_for_claude(notes)
        
        prompt = f"""Analyze these philosophy notes from the past {timeframe}:

{notes_text}

Identify:
1. Recurring themes and questions
2. Evolution of thinking over time
3. Philosophical territory being explored
4. Connections between different thoughts

Keep it concise (200-300 words) and insightful."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
        
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return "Unable to generate analysis at this time."
    
    def answer_question(self, question: str, relevant_notes: List[Dict]) -> str:
        """Answer user's question based on their notes"""
        
        notes_text = self._format_notes_for_claude(relevant_notes)
        
        prompt = f"""The user has asked about their philosophy notes:

**Question:** {question}

**Relevant notes:**
{notes_text}

Based on their actual notes, provide a thoughtful answer that:
- References their specific thoughts and ideas
- Helps them explore the question deeper
- Connects to relevant philosophical concepts if appropriate
- Is conversational and insightful

Keep it concise (200-400 words)."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
        
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return "Unable to process your question at this time."
