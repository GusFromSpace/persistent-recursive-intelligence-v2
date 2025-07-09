#!/usr/bin/env python3
"""
Dynamic Connection Suggester with User Scoring and Reinforcement Learning

This module extends the Code Connector with:
1. Dynamic suggestion generation based on user feedback
2. Scoring system for connection quality
3. Reinforcement learning from user ratings
4. Pattern improvement over time
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

@dataclass
class ConnectionSuggestion:
    """Enhanced connection suggestion with scoring and feedback"""
    orphaned_file: str
    target_file: str
    connection_type: str
    confidence_score: float
    suggestion_text: str
    reasoning: List[str]
    semantic_similarity: float
    structural_compatibility: float
    need_detection_score: float
    
    # User feedback fields
    user_rating: Optional[int] = None  # 1-5 stars
    user_feedback: Optional[str] = None
    implemented: bool = False
    timestamp: str = None
    suggestion_id: str = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.suggestion_id:
            # Create unique ID based on content
            content = f"{self.orphaned_file}{self.target_file}{self.connection_type}"
            self.suggestion_id = hashlib.md5(content.encode()).hexdigest()[:12]

class DynamicConnectionSuggester:
    """Enhanced Code Connector with user feedback and learning"""
    
    def __init__(self, db_path: str = "connection_suggestions.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for storing suggestions and feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Suggestions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suggestions (
                suggestion_id TEXT PRIMARY KEY,
                orphaned_file TEXT,
                target_file TEXT,
                connection_type TEXT,
                confidence_score REAL,
                suggestion_text TEXT,
                reasoning TEXT,
                semantic_similarity REAL,
                structural_compatibility REAL,
                need_detection_score REAL,
                user_rating INTEGER,
                user_feedback TEXT,
                implemented BOOLEAN DEFAULT FALSE,
                timestamp TEXT
            )
        ''')
        
        # Pattern learning table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_learning (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                avg_rating REAL DEFAULT 0.0,
                last_updated TEXT,
                pattern_data TEXT
            )
        ''')
        
        # Connection types performance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_performance (
                connection_type TEXT PRIMARY KEY,
                total_suggestions INTEGER DEFAULT 0,
                successful_suggestions INTEGER DEFAULT 0,
                avg_rating REAL DEFAULT 0.0,
                success_rate REAL DEFAULT 0.0,
                last_updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_dynamic_suggestions(
        self, 
        orphaned_files: List[str], 
        main_files: List[str],
        max_suggestions: int = 10
    ) -> List[ConnectionSuggestion]:
        """Generate connection suggestions with dynamic learning"""
        
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"🧠 Generating dynamic suggestions for {len(orphaned_files)} orphaned files...")\n        
        suggestions = []
        
        # Get learned patterns to improve suggestions
        learned_patterns = self._get_successful_patterns()
        
        for orphaned_file in orphaned_files:
            for main_file in main_files:
                suggestion = self._create_enhanced_suggestion(
                    orphaned_file, 
                    main_file, 
                    learned_patterns
                )
                
                if suggestion and suggestion.confidence_score > 0.3:
                    suggestions.append(suggestion)
        
        # Sort by confidence score and learning-adjusted rating
        suggestions.sort(
            key=lambda x: self._calculate_adjusted_confidence(x), 
            reverse=True
        )
        
        return suggestions[:max_suggestions]
    
    def _create_enhanced_suggestion(
        self, 
        orphaned_file: str, 
        main_file: str, 
        learned_patterns: Dict[str, Any]
    ) -> Optional[ConnectionSuggestion]:
        """Create a connection suggestion enhanced by learned patterns"""
        
        # Basic analysis (simplified for demo)
        orphaned_content = self._analyze_file_content(orphaned_file)
        main_content = self._analyze_file_content(main_file)
        
        if not orphaned_content or not main_content:
            return None
        
        # Calculate similarity scores
        semantic_sim = self._calculate_semantic_similarity(orphaned_content, main_content)
        structural_compat = self._calculate_structural_compatibility(orphaned_content, main_content)
        need_score = self._detect_integration_need(orphaned_content, main_content)
        
        # Apply learned pattern adjustments
        pattern_boost = self._apply_pattern_learning(
            orphaned_content, main_content, learned_patterns
        )
        
        base_confidence = (semantic_sim + structural_compat + need_score) / 3
        adjusted_confidence = min(1.0, base_confidence + pattern_boost)
        
        if adjusted_confidence < 0.3:
            return None
        
        # Determine connection type based on analysis
        connection_type = self._determine_connection_type(orphaned_content, main_content)
        
        # Generate suggestion text
        suggestion_text = self._generate_suggestion_text(
            orphaned_file, main_file, connection_type, orphaned_content, main_content
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            semantic_sim, structural_compat, need_score, pattern_boost
        )
        
        return ConnectionSuggestion(
            orphaned_file=orphaned_file,
            target_file=main_file,
            connection_type=connection_type,
            confidence_score=adjusted_confidence,
            suggestion_text=suggestion_text,
            reasoning=reasoning,
            semantic_similarity=semantic_sim,
            structural_compatibility=structural_compat,
            need_detection_score=need_score
        )
    
    def _analyze_file_content(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Analyze file content for connection opportunities"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'functions': self._extract_functions(content),
                'classes': self._extract_classes(content),
                'imports': self._extract_imports(content),
                'todos': self._extract_todos(content),
                'file_type': Path(file_path).suffix,
                'size': len(content),
                'content_sample': content[:500]
            }
        except Exception as e:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"Error analyzing {file_path}: {e}")\n            return None
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from content"""
        import re
        # Simplified function extraction
        functions = re.findall(r'(?:def|function|void|int|float|string|bool)\s+(\w+)\s*\(', content)
        return list(set(functions))
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names from content"""
        import re
        classes = re.findall(r'class\s+(\w+)', content)
        return list(set(classes))
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements"""
        import re
        imports = re.findall(r'(?:import|#include|require)\s+["\']?([^"\';\n]+)', content)
        return list(set(imports))
    
    def _extract_todos(self, content: str) -> List[str]:
        """Extract TODO comments and NotImplementedError"""
        import re
        todos = re.findall(r'(?:TODO|FIXME|NotImplementedError)[:\s]*([^\n]*)', content)
        return todos
    
    def _calculate_semantic_similarity(self, content1: Dict, content2: Dict) -> float:
        """Calculate semantic similarity between files"""
        # Function name overlap
        func_overlap = len(set(content1['functions']) & set(content2['functions']))
        func_similarity = func_overlap / max(len(content1['functions']), len(content2['functions']), 1)
        
        # Class name similarity
        class_overlap = len(set(content1['classes']) & set(content2['classes']))
        class_similarity = class_overlap / max(len(content1['classes']), len(content2['classes']), 1)
        
        # Import similarity
        import_overlap = len(set(content1['imports']) & set(content2['imports']))
        import_similarity = import_overlap / max(len(content1['imports']), len(content2['imports']), 1)
        
        return (func_similarity + class_similarity + import_similarity) / 3
    
    def _calculate_structural_compatibility(self, content1: Dict, content2: Dict) -> float:
        """Calculate structural compatibility"""
        # File type compatibility
        type_compat = 1.0 if content1['file_type'] == content2['file_type'] else 0.5
        
        # Size compatibility (prefer similar sized files)
        size_ratio = min(content1['size'], content2['size']) / max(content1['size'], content2['size'])
        
        return (type_compat + size_ratio) / 2
    
    def _detect_integration_need(self, orphaned: Dict, main: Dict) -> float:
        """Detect if main file could benefit from orphaned file"""
        need_score = 0.0
        
        # Check if main file has TODOs that orphaned file might address
        if main['todos'] and orphaned['functions']:
            need_score += 0.3
        
        # Check if orphaned file has functionality that main file lacks
        orphaned_funcs = set(orphaned['functions'])
        main_funcs = set(main['functions'])
        
        unique_functionality = len(orphaned_funcs - main_funcs)
        if unique_functionality > 0:
            need_score += min(0.5, unique_functionality * 0.1)
        
        return min(1.0, need_score)
    
    def _determine_connection_type(self, orphaned: Dict, main: Dict) -> str:
        """Determine the type of connection to suggest"""
        if orphaned['classes'] and main['classes']:
            return "class_inheritance"
        elif orphaned['functions'] and not orphaned['classes']:
            return "function_import"
        elif orphaned['file_type'] in ['.h', '.hpp'] and main['file_type'] in ['.c', '.cpp']:
            return "header_include"
        else:
            return "module_integration"
    
    def _generate_suggestion_text(
        self, 
        orphaned_file: str, 
        main_file: str, 
        connection_type: str, 
        orphaned: Dict, 
        main: Dict
    ) -> str:
        """Generate human-readable suggestion text"""
        
        suggestions = {
            "function_import": f"Import functions {orphaned['functions'][:3]} from {Path(orphaned_file).name} into {Path(main_file).name}",
            "class_inheritance": f"Consider inheriting from or composing with classes in {Path(orphaned_file).name}",
            "header_include": f"Include {Path(orphaned_file).name} as header for {Path(main_file).name}",
            "module_integration": f"Integrate {Path(orphaned_file).name} as a module within {Path(main_file).name}"
        }
        
        return suggestions.get(connection_type, f"Consider integrating {Path(orphaned_file).name} with {Path(main_file).name}")
    
    def _generate_reasoning(
        self, 
        semantic_sim: float, 
        structural_compat: float, 
        need_score: float, 
        pattern_boost: float
    ) -> List[str]:
        """Generate reasoning for the suggestion"""
        reasoning = []
        
        if semantic_sim > 0.5:
            reasoning.append(f"High semantic similarity ({semantic_sim:.2f}) - files work in related domains")
        
        if need_score > 0.3:
            reasoning.append(f"Detected potential need ({need_score:.2f}) - main file has gaps that orphaned file might fill")
        
        if structural_compat > 0.7:
            reasoning.append(f"Good structural compatibility ({structural_compat:.2f}) - files are architecturally compatible")
        
        if pattern_boost > 0.1:
            reasoning.append(f"Pattern learning boost ({pattern_boost:.2f}) - similar successful connections found in history")
        
        return reasoning
    
    def _apply_pattern_learning(
        self, 
        orphaned: Dict, 
        main: Dict, 
        learned_patterns: Dict[str, Any]
    ) -> float:
        """Apply learned patterns to boost or reduce confidence"""
        boost = 0.0
        
        # Check if this type of connection has been successful before
        for pattern_type, pattern_data in learned_patterns.items():
            if self._pattern_matches(orphaned, main, pattern_data):
                # Boost based on historical success rate
                boost += pattern_data['success_rate'] * 0.2
        
        return min(0.3, boost)  # Cap boost at 0.3
    
    def _pattern_matches(self, orphaned: Dict, main: Dict, pattern_data: Dict) -> bool:
        """Check if current files match a learned pattern"""
        # Simplified pattern matching
        pattern = json.loads(pattern_data.get('pattern_json', '{}'))
        
        # Check file type pattern
        if pattern.get('file_types'):
            if (orphaned['file_type'], main['file_type']) in pattern['file_types']:
                return True
        
        # Check function pattern
        if pattern.get('function_keywords'):
            orphaned_funcs = ' '.join(orphaned['functions']).lower()
            for keyword in pattern['function_keywords']:
                if keyword in orphaned_funcs:
                    return True
        
        return False
    
    def _calculate_adjusted_confidence(self, suggestion: ConnectionSuggestion) -> float:
        """Calculate confidence score adjusted by historical performance"""
        base_confidence = suggestion.confidence_score
        
        # Get historical performance for this connection type
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT success_rate, avg_rating FROM connection_performance WHERE connection_type = ?",
            (suggestion.connection_type,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            success_rate, avg_rating = result
            # Adjust confidence based on historical performance
            performance_factor = (success_rate + avg_rating / 5) / 2
            return base_confidence * performance_factor
        
        return base_confidence
    
    def _get_successful_patterns(self) -> Dict[str, Any]:
        """Get patterns that have been successful in the past"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM pattern_learning WHERE success_count > failure_count AND avg_rating > 3.0"
        )
        
        patterns = {}
        for row in cursor.fetchall():
            pattern_id = row[0]
            patterns[pattern_id] = {
                'pattern_type': row[1],
                'success_count': row[2],
                'failure_count': row[3],
                'avg_rating': row[4],
                'success_rate': row[2] / max(row[2] + row[3], 1),
                'pattern_json': row[6]
            }
        
        conn.close()
        return patterns
    
    def save_suggestion(self, suggestion: ConnectionSuggestion):
        """Save suggestion to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO suggestions 
            (suggestion_id, orphaned_file, target_file, connection_type, confidence_score,
             suggestion_text, reasoning, semantic_similarity, structural_compatibility,
             need_detection_score, user_rating, user_feedback, implemented, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            suggestion.suggestion_id,
            suggestion.orphaned_file,
            suggestion.target_file,
            suggestion.connection_type,
            suggestion.confidence_score,
            suggestion.suggestion_text,
            json.dumps(suggestion.reasoning),
            suggestion.semantic_similarity,
            suggestion.structural_compatibility,
            suggestion.need_detection_score,
            suggestion.user_rating,
            suggestion.user_feedback,
            suggestion.implemented,
            suggestion.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def rate_suggestion(
        self, 
        suggestion_id: str, 
        rating: int, 
        feedback: str = None, 
        implemented: bool = False
    ):
        """Allow user to rate and provide feedback on suggestions"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update the suggestion
        cursor.execute('''
            UPDATE suggestions 
            SET user_rating = ?, user_feedback = ?, implemented = ?
            WHERE suggestion_id = ?
        ''', (rating, feedback, implemented, suggestion_id))
        
        # Get suggestion details for pattern learning
        cursor.execute(
            "SELECT connection_type, orphaned_file, target_file FROM suggestions WHERE suggestion_id = ?",
            (suggestion_id,)
        )
        
        suggestion_data = cursor.fetchone()
        
        if suggestion_data:
            connection_type, orphaned_file, target_file = suggestion_data
            
            # Update connection type performance
            self._update_connection_performance(cursor, connection_type, rating, implemented)
            
            # Learn from this feedback
            self._learn_from_feedback(cursor, suggestion_id, rating, implemented)
        
        conn.commit()
        conn.close()
        
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"✅ Suggestion {suggestion_id} rated {rating}/5 - Thank you for the feedback!")\n    
    def _update_connection_performance(self, cursor, connection_type: str, rating: int, implemented: bool):
        """Update performance metrics for connection types"""
        # Get current stats
        cursor.execute(
            "SELECT total_suggestions, successful_suggestions, avg_rating FROM connection_performance WHERE connection_type = ?",
            (connection_type,)
        )
        
        result = cursor.fetchone()
        
        if result:
            total, successful, avg_rating = result
            new_total = total + 1
            new_successful = successful + (1 if rating >= 4 or implemented else 0)
            new_avg_rating = ((avg_rating * total) + rating) / new_total
            new_success_rate = new_successful / new_total
            
            cursor.execute('''
                UPDATE connection_performance 
                SET total_suggestions = ?, successful_suggestions = ?, 
                    avg_rating = ?, success_rate = ?, last_updated = ?
                WHERE connection_type = ?
            ''', (new_total, new_successful, new_avg_rating, new_success_rate, 
                  datetime.now().isoformat(), connection_type))
        else:
            # First rating for this connection type
            cursor.execute('''
                INSERT INTO connection_performance 
                (connection_type, total_suggestions, successful_suggestions, avg_rating, success_rate, last_updated)
                VALUES (?, 1, ?, ?, ?, ?)
            ''', (connection_type, 1 if rating >= 4 or implemented else 0, 
                  rating, 1.0 if rating >= 4 or implemented else 0.0, datetime.now().isoformat()))
    
    def _learn_from_feedback(self, cursor, suggestion_id: str, rating: int, implemented: bool):
        """Learn patterns from user feedback"""
        # This is where we'd implement more sophisticated pattern learning
        # For now, just track basic success/failure
        
        # Get suggestion details
        cursor.execute(
            "SELECT orphaned_file, target_file, connection_type FROM suggestions WHERE suggestion_id = ?",
            (suggestion_id,)
        )
        
        result = cursor.fetchone()
        if not result:
            return
        
        orphaned_file, target_file, connection_type = result
        
        # Create a simple pattern based on file extensions
        orphaned_ext = Path(orphaned_file).suffix
        target_ext = Path(target_file).suffix
        pattern_id = f"{connection_type}_{orphaned_ext}_{target_ext}"
        
        # Update pattern learning
        cursor.execute(
            "SELECT success_count, failure_count, avg_rating FROM pattern_learning WHERE pattern_id = ?",
            (pattern_id,)
        )
        
        pattern_result = cursor.fetchone()
        
        success = 1 if rating >= 4 or implemented else 0
        failure = 1 if rating <= 2 and not implemented else 0
        
        if pattern_result:
            old_success, old_failure, old_avg = pattern_result
            new_success = old_success + success
            new_failure = old_failure + failure
            total_ratings = new_success + new_failure
            new_avg = ((old_avg * (old_success + old_failure)) + rating) / max(total_ratings, 1)
            
            cursor.execute('''
                UPDATE pattern_learning 
                SET success_count = ?, failure_count = ?, avg_rating = ?, last_updated = ?
                WHERE pattern_id = ?
            ''', (new_success, new_failure, new_avg, datetime.now().isoformat(), pattern_id))
        else:
            # New pattern
            pattern_data = {
                'file_types': [(orphaned_ext, target_ext)],
                'connection_type': connection_type
            }
            
            cursor.execute('''
                INSERT INTO pattern_learning 
                (pattern_id, pattern_type, success_count, failure_count, avg_rating, last_updated, pattern_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (pattern_id, connection_type, success, failure, rating, 
                  datetime.now().isoformat(), json.dumps(pattern_data)))
    
    def get_user_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of user feedback and learning progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Overall stats
        cursor.execute("SELECT COUNT(*), AVG(user_rating) FROM suggestions WHERE user_rating IS NOT NULL")
        total_rated, avg_rating = cursor.fetchone()
        
        # Implementation rate
        cursor.execute("SELECT COUNT(*) FROM suggestions WHERE implemented = 1")
        implemented_count = cursor.fetchone()[0]
        
        # Best connection types
        cursor.execute('''
            SELECT connection_type, avg_rating, success_rate 
            FROM connection_performance 
            ORDER BY success_rate DESC, avg_rating DESC
            LIMIT 5
        ''')
        best_types = cursor.fetchall()
        
        # Learning progress
        cursor.execute("SELECT COUNT(*) FROM pattern_learning WHERE success_count > failure_count")
        successful_patterns = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_rated_suggestions': total_rated or 0,
            'average_rating': round(avg_rating or 0, 2),
            'implementation_rate': implemented_count / max(total_rated or 1, 1),
            'best_connection_types': best_types,
            'successful_patterns_learned': successful_patterns,
            'learning_status': 'Active' if successful_patterns > 0 else 'Initial'
        }


def main():
    """Demo the dynamic connection suggester"""
    suggester = DynamicConnectionSuggester()
    
# DEBUG ELIMINATED BY MESOPREDATOR: print("🧠 Dynamic Connection Suggester with User Learning")\n# DEBUG ELIMINATED BY MESOPREDATOR\n    
    # Example usage
    orphaned_files = ["test_utils.py", "helper_functions.cpp"]
    main_files = ["main.py", "engine.cpp"]
    
    suggestions = suggester.generate_dynamic_suggestions(orphaned_files, main_files)
    
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n📋 Generated {len(suggestions)} suggestions:")\n    for i, suggestion in enumerate(suggestions, 1):
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n{i}. {suggestion.suggestion_text}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Confidence: {suggestion.confidence_score:.2f}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Reasoning: {', '.join(suggestion.reasoning)}")\n        
        # Save suggestion
        suggester.save_suggestion(suggestion)
        
        # Simulate user rating (in real usage, this would be interactive)
        if i == 1:  # Rate the first suggestion
            suggester.rate_suggestion(suggestion.suggestion_id, 4, "Great suggestion!", True)
    
    # Show learning summary
    summary = suggester.get_user_feedback_summary()
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n📊 Learning Summary:")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Rated suggestions: {summary['total_rated_suggestions']}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Average rating: {summary['average_rating']}/5")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Implementation rate: {summary['implementation_rate']:.1%}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   Successful patterns learned: {summary['successful_patterns_learned']}")\n

if __name__ == "__main__":
    main()