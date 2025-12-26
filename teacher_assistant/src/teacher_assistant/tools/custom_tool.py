"""
Custom tools for the Teacher Assistant Crew.
These tools help analyze teaching notes and extract key information.
"""

from crewai.tools import BaseTool
from typing import Type, Optional, Dict, List
from pydantic import BaseModel, Field
import re


class NotesAnalysisInput(BaseModel):
    """Input schema for NotesAnalysisTool."""
    notes: str = Field(..., description="The teaching notes to analyze")


class NotesAnalysisTool(BaseTool):
    name: str = "Notes Analyzer"
    description: str = (
        "Analyzes teaching notes to extract key information including subject area, "
        "grade level, key concepts, learning objectives, vocabulary terms, and "
        "suggested teaching approaches. Useful for understanding the scope and "
        "focus of the lesson content before creating detailed plans."
    )
    args_schema: Type[BaseModel] = NotesAnalysisInput
    
    def run(self, notes: str) -> str:
        """
        Analyzes the notes and returns structured information.
        
        Args:
            notes: The teaching notes text
            
        Returns:
            A formatted string with analysis results
        """
        analysis = {
            "subject": self._identify_subject(notes),
            "grade_level": self._extract_grade_level(notes),
            "key_concepts": self._extract_key_concepts(notes),
            "learning_objectives": self._extract_objectives(notes),
            "vocabulary": self._extract_vocabulary(notes),
            "topics": self._extract_topics(notes),
            "prior_knowledge": self._extract_prior_knowledge(notes),
            "real_world_connections": self._extract_real_world(notes),
            "content_stats": {
                "total_words": len(notes.split()),
                "total_lines": len(notes.split('\n')),
                "has_objectives": "objective" in notes.lower(),
                "has_vocabulary": "vocabulary" in notes.lower() or "vocab" in notes.lower(),
                "has_standards": "standard" in notes.lower()
            }
        }
        
        # Format the analysis as a readable string
        result = "=== TEACHING NOTES ANALYSIS ===\n\n"
        result += f"Subject Area: {analysis['subject']}\n"
        result += f"Grade Level: {analysis['grade_level']}\n\n"
        
        if analysis['key_concepts']:
            result += "Key Concepts:\n"
            for concept in analysis['key_concepts']:
                result += f"  • {concept}\n"
            result += "\n"
        
        if analysis['learning_objectives']:
            result += "Learning Objectives Found:\n"
            for obj in analysis['learning_objectives']:
                result += f"  • {obj}\n"
            result += "\n"
        
        if analysis['vocabulary']:
            result += f"Vocabulary Terms: {', '.join(analysis['vocabulary'])}\n\n"
        
        if analysis['prior_knowledge']:
            result += "Prior Knowledge Required:\n"
            for item in analysis['prior_knowledge']:
                result += f"  • {item}\n"
            result += "\n"
        
        if analysis['real_world_connections']:
            result += "Real-World Connections:\n"
            for conn in analysis['real_world_connections']:
                result += f"  • {conn}\n"
            result += "\n"
        
        result += f"Content Statistics:\n"
        result += f"  • Total Words: {analysis['content_stats']['total_words']}\n"
        result += f"  • Has Objectives: {analysis['content_stats']['has_objectives']}\n"
        result += f"  • Has Vocabulary: {analysis['content_stats']['has_vocabulary']}\n"
        
        return result
    
    def _run(self, notes: str) -> str:
        return self.run(notes)
    
    def _identify_subject(self, notes: str) -> str:
        """Identify the subject area from notes."""
        notes_lower = notes.lower()
        
        subject_keywords = {
            'Mathematics': ['equation', 'solve', 'calculate', 'algebra', 'geometry', 
                          'theorem', 'formula', 'graph', 'function', 'variable',
                          'quadratic', 'polynomial', 'trigonometry', 'calculus'],
            'Science': ['experiment', 'hypothesis', 'cell', 'atom', 'chemistry', 
                       'biology', 'physics', 'photosynthesis', 'molecule', 'energy',
                       'reaction', 'organism', 'ecosystem', 'matter'],
            'English/Language Arts': ['grammar', 'writing', 'literature', 'essay', 
                                     'poem', 'reading', 'paragraph', 'sentence',
                                     'comprehension', 'vocabulary', 'author', 'theme'],
            'Social Studies/History': ['war', 'revolution', 'civilization', 'government', 
                                       'geography', 'culture', 'society', 'empire',
                                       'constitution', 'democracy', 'economy'],
            'Music': ['rhythm', 'melody', 'notation', 'tempo', 'scale', 'chord',
                     'instrument', 'beat', 'harmony', 'composition'],
            'Art': ['painting', 'drawing', 'sculpture', 'color theory', 'perspective',
                   'composition', 'medium', 'texture', 'artist'],
            'Physical Education': ['exercise', 'fitness', 'sport', 'movement', 'health',
                                  'coordination', 'athletics', 'wellness'],
            'Computer Science': ['code', 'programming', 'algorithm', 'software', 'computer',
                                'variable', 'function', 'loop', 'debug']
        }
        
        subject_scores = {}
        for subject, keywords in subject_keywords.items():
            score = sum(1 for keyword in keywords if keyword in notes_lower)
            if score > 0:
                subject_scores[subject] = score
        
        if subject_scores:
            return max(subject_scores, key=subject_scores.get)
        return "General/Multi-Subject"
    
    def _extract_grade_level(self, notes: str) -> str:
        """Extract or estimate grade level."""
        notes_lower = notes.lower()
        
        # Look for explicit grade level mentions
        grade_patterns = [
            r'grade\s*(\d+)',
            r'(\d+)(?:st|nd|rd|th)\s+grade',
            r'level[:\s]+(\d+)',
        ]
        
        for pattern in grade_patterns:
            match = re.search(pattern, notes_lower)
            if match:
                grade_num = match.group(1)
                return f"Grade {grade_num}"
        
        # Look for level indicators
        if any(word in notes_lower for word in ['elementary', 'primary', 'kindergarten']):
            return "K-5 (Elementary)"
        elif any(word in notes_lower for word in ['middle school', 'junior high']):
            return "6-8 (Middle School)"
        elif any(word in notes_lower for word in ['high school', 'secondary']):
            return "9-12 (High School)"
        elif any(word in notes_lower for word in ['college', 'university', 'undergraduate']):
            return "College/University"
        
        # Estimate based on complexity
        if any(word in notes_lower for word in ['basic', 'introduction', 'simple', 'beginner']):
            return "Elementary to Middle School (Est.)"
        elif any(word in notes_lower for word in ['advanced', 'complex', 'in-depth']):
            return "High School to College (Est.)"
        
        return "Not Specified (Grades 6-12 adaptable)"
    
    def _extract_key_concepts(self, notes: str) -> List[str]:
        """Extract key concepts from notes."""
        concepts = []
        lines = notes.split('\n')
        
        in_concepts_section = False
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're entering a concepts section
            if any(marker in line_lower for marker in ['key concept', 'main concept', 'concepts:']):
                in_concepts_section = True
                continue
            
            # Check if we're leaving the section
            if in_concepts_section and line.strip() and not line.startswith((' ', '\t', '-', '•', '*')):
                if ':' in line or line[0].isupper():
                    in_concepts_section = False
            
            # Extract concepts
            if in_concepts_section and line.strip():
                # Remove bullet points and clean up
                concept = re.sub(r'^[\s\-•*]+', '', line).strip()
                if concept and len(concept) > 5:
                    concepts.append(concept)
        
        return concepts[:10]  # Return top 10 concepts
    
    def _extract_objectives(self, notes: str) -> List[str]:
        """Extract learning objectives."""
        objectives = []
        lines = notes.split('\n')
        
        in_objectives_section = False
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if we're entering objectives section
            if any(marker in line_lower for marker in ['learning objective', 'objective', 
                                                       'students will', 'goal']):
                in_objectives_section = True
                # Check if objective is on same line
                if ':' in line:
                    continue
            
            # Check if we're leaving the section
            if in_objectives_section and line.strip() and not line.startswith((' ', '\t', '-', '•', '*')):
                if ':' in line or (line[0].isupper() and 'objective' not in line_lower):
                    in_objectives_section = False
            
            # Extract objectives
            if in_objectives_section and line.strip():
                objective = re.sub(r'^[\s\-•*]+', '', line).strip()
                if objective and len(objective) > 10:
                    objectives.append(objective)
        
        return objectives[:8]
    
    def _extract_vocabulary(self, notes: str) -> List[str]:
        """Extract vocabulary terms."""
        vocab = []
        lines = notes.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if 'vocabulary' in line_lower or 'vocab' in line_lower or 'terms' in line_lower:
                # Extract terms after the marker
                if ':' in line:
                    terms_text = line.split(':', 1)[1]
                    # Split by commas or semicolons
                    terms = re.split(r'[,;]', terms_text)
                    vocab.extend([term.strip() for term in terms if term.strip()])
        
        return vocab[:15]
    
    def _extract_topics(self, notes: str) -> List[str]:
        """Extract specific topics covered."""
        topics = []
        lines = notes.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            # Look for lines that start with numbers or bullets
            if line_stripped and (line_stripped[0].isdigit() or 
                                 line_stripped.startswith(('-', '•', '*'))):
                topic = re.sub(r'^[\d\.\)\-•*\s]+', '', line_stripped)
                if topic and len(topic) > 5 and len(topic) < 100:
                    topics.append(topic)
        
        return topics[:10]
    
    def _extract_prior_knowledge(self, notes: str) -> List[str]:
        """Extract prior knowledge requirements."""
        prior_knowledge = []
        lines = notes.split('\n')
        
        in_prior_section = False
        for line in lines:
            line_lower = line.lower()
            
            if 'prior knowledge' in line_lower or 'prerequisite' in line_lower:
                in_prior_section = True
                continue
            
            if in_prior_section:
                if line.strip() and not line.startswith((' ', '\t', '-', '•', '*')):
                    if ':' in line:
                        in_prior_section = False
                    continue
                
                if line.strip():
                    item = re.sub(r'^[\s\-•*]+', '', line).strip()
                    if item and len(item) > 5:
                        prior_knowledge.append(item)
        
        return prior_knowledge[:8]
    
    def _extract_real_world(self, notes: str) -> List[str]:
        """Extract real-world connections."""
        connections = []
        lines = notes.split('\n')
        
        in_realworld_section = False
        for line in lines:
            line_lower = line.lower()
            
            if any(marker in line_lower for marker in ['real-world', 'real world', 
                                                       'application', 'connection']):
                in_realworld_section = True
                continue
            
            if in_realworld_section:
                if line.strip() and not line.startswith((' ', '\t', '-', '•', '*')):
                    if ':' in line:
                        in_realworld_section = False
                    continue
                
                if line.strip():
                    item = re.sub(r'^[\s\-•*]+', '', line).strip()
                    if item and len(item) > 5:
                        connections.append(item)
        
        return connections[:8]


class GradeLevelAnalyzer(BaseTool):
    name: str = "Grade Level Analyzer"
    description: str = (
        "Analyzes text complexity and suggests appropriate grade levels. "
        "Useful for ensuring content matches student readiness."
    )
    args_schema: Type[BaseModel] = NotesAnalysisInput
    
    def run(self, notes: str) -> str:
        """Analyze grade level appropriateness."""
        words = notes.split()
        sentences = notes.split('.')
        
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Simple complexity scoring
        if avg_word_length < 4.5 and avg_sentence_length < 10:
            grade_range = "Elementary (K-5)"
            complexity = "Low"
        elif avg_word_length < 5.5 and avg_sentence_length < 15:
            grade_range = "Middle School (6-8)"
            complexity = "Medium"
        else:
            grade_range = "High School+ (9-12+)"
            complexity = "High"
        
        result = f"Content Complexity Analysis:\n"
        result += f"  • Suggested Grade Range: {grade_range}\n"
        result += f"  • Complexity Level: {complexity}\n"
        result += f"  • Average Word Length: {avg_word_length:.1f} characters\n"
        result += f"  • Average Sentence Length: {avg_sentence_length:.1f} words\n"
        
        return result

    def _run(self, notes: str) -> str:
        return self.run(notes)


__all__ = [
    "NotesAnalysisTool",
    "GradeLevelAnalyzer",
]
