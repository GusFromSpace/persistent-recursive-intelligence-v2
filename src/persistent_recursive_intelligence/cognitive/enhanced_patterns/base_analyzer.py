"""
Base Language Analyzer for Multi-Language Support
Implements the foundation for the Multi-Language Support Standard
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
import json
import os


class BaseLanguageAnalyzer(ABC):
    """
    Abstract base class for language-specific analyzers
    Follows the Multi-Language Support Standard architecture
    """
    
    def __init__(self, language: str, memory_engine):
        self.language = language
        self.memory_engine = memory_engine
        self.file_extensions = []
        self.language_family = 'unknown'
        self.database_name = f'pri_{language}.db'
        self.pattern_categories = {}
        
    @abstractmethod
    def analyze_file(self, file_path: str) -> List[Dict]:
        """
        Analyze a single file and return list of issues/patterns found
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            List of dictionaries containing issue details:
            {
                'type': str,                    # Issue type identifier
                'severity': str,                # high, medium, low, info
                'line': int,                    # Line number
                'description': str,             # Human readable description
                'suggestion': str,              # Improvement suggestion
                'pattern_category': str,        # Category from pattern_categories
                'file_path': str               # File path
            }
        """
        pass
    
    @abstractmethod
    def get_language_metrics(self, project_path: str) -> Dict:
        """
        Get language-specific metrics for a project
        
        Args:
            project_path: Path to project root
            
        Returns:
            Dictionary with language-specific metrics
        """
        pass
    
    def can_analyze_file(self, file_path: str) -> bool:
        """Check if this analyzer can handle the given file"""
        return any(file_path.endswith(ext) for ext in self.file_extensions)
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of file extensions this analyzer supports"""
        return self.file_extensions.copy()
    
    def get_language_info(self) -> Dict:
        """Get information about this language analyzer"""
        return {
            'language': self.language,
            'family': self.language_family,
            'extensions': self.file_extensions,
            'database': self.database_name,
            'categories': list(self.pattern_categories.keys())
        }
    
    def store_pattern_in_memory(self, pattern_data: Dict) -> Optional[int]:
        """Store a pattern in the language-specific memory database"""
        if not self.memory_engine:
            return None
            
        # Use SimpleMemoryEngine interface
        description = f"{self.language}_pattern_{pattern_data.get('type', 'unknown')}"
        return self.memory_engine.store_memory(description, pattern_data)
    
    def search_similar_patterns(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for similar patterns in this language's memory"""
        if not self.memory_engine:
            return []
            
        # Use SimpleMemoryEngine interface
        search_query = f"{self.language}_pattern {query}"
        return self.memory_engine.search_memories(search_query, limit)
    
    def suggest_improvements(self, analysis_results: List[Dict]) -> List[Dict]:
        """
        Suggest improvements based on analysis results
        
        Args:
            analysis_results: Results from analyze_file()
            
        Returns:
            List of improvement suggestions
        """
        # Default implementation - can be overridden by specific analyzers
        suggestions = []
        
        # Group issues by type
        issue_counts = {}
        for result in analysis_results:
            issue_type = result.get('type', 'unknown')
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Generate generic suggestions based on frequency
        for issue_type, count in issue_counts.items():
            if count > 3:  # If we see the same issue multiple times
                suggestions.append({
                    'type': 'pattern_improvement',
                    'priority': 'medium',
                    'description': f'Multiple instances of {issue_type} found ({count} times)',
                    'implementation': f'Consider addressing {issue_type} pattern across the codebase',
                    'rationale': 'Recurring patterns often indicate systematic issues'
                })
        
        return suggestions
    
    def get_cross_language_correlations(self) -> List[str]:
        """Get list of languages this analyzer correlates with"""
        # This would be implemented based on language family relationships
        # defined in the Multi-Language Support Standard
        correlations = {
            'scripting': ['python', 'javascript', 'ruby', 'lua'],
            'systems': ['cpp', 'rust', 'c', 'go'],
            'managed': ['java', 'csharp', 'kotlin', 'scala'],
            'functional': ['haskell', 'ocaml', 'clojure', 'erlang']
        }
        
        family_languages = correlations.get(self.language_family, [])
        return [lang for lang in family_languages if lang != self.language]
    
    def search_cross_language_patterns(self, query: str, limit: int = 5) -> Dict[str, List[Dict]]:
        """
        Search for similar patterns across related languages (READ-ONLY)
        
        This enables cross-language pattern correlation by scanning other
        language databases without writing to them, following the principle
        of letting FAISS scan other language DBs while working.
        
        Args:
            query: Pattern to search for
            limit: Maximum results per language
            
        Returns:
            Dictionary mapping language names to lists of correlated patterns
        """
        correlations = {}
        
        if not self.memory_engine:
            return correlations
            
        # Get languages to correlate with
        related_languages = self.get_cross_language_correlations()
        
        for language in related_languages:
            try:
                # Search in the related language's pattern space (read-only)
                # Try multiple search strategies
                search_queries = [
                    f"{language}_pattern {query}",
                    f"{language}_pattern_{query}",
                    f"{query} {language}",
                    query  # Fallback to generic search
                ]
                
                for search_query in search_queries:
                    patterns = self.memory_engine.search_memories(search_query, limit)
                    if patterns:
                        # Filter patterns that actually relate to the target language
                        filtered_patterns = []
                        for pattern in patterns:
                            pattern_content = str(pattern.get('content', '')) + str(pattern.get('metadata', {}))
                            if language in pattern_content.lower() or query in pattern_content.lower():
                                filtered_patterns.append(pattern)
                        
                        if filtered_patterns:
                            correlations[language] = filtered_patterns
                            break  # Found patterns for this language
                    
            except Exception as e:
                # Don't fail the whole operation if one language search fails
                continue
                
        return correlations
    
    def analyze_with_cross_language_context(self, file_path: str) -> Dict:
        """
        Analyze a file with cross-language pattern context
        
        This method combines local analysis with insights from related languages,
        providing richer context for pattern detection and suggestions.
        
        Returns:
            Dictionary containing:
            - local_analysis: Results from this language's analyzer
            - cross_language_correlations: Patterns found in related languages
            - synthesis: Combined insights and recommendations
        """
        # Perform local analysis
        local_issues = self.analyze_file(file_path)
        
        # Search for cross-language correlations for each issue type
        correlations = {}
        issue_types = set(issue.get('type', 'unknown') for issue in local_issues)
        
        for issue_type in issue_types:
            cross_lang_patterns = self.search_cross_language_patterns(issue_type, 3)
            if cross_lang_patterns:
                correlations[issue_type] = cross_lang_patterns
        
        # Generate synthesis insights
        synthesis = self._synthesize_cross_language_insights(local_issues, correlations)
        
        return {
            'local_analysis': local_issues,
            'cross_language_correlations': correlations,
            'synthesis': synthesis
        }
    
    def _synthesize_cross_language_insights(self, local_issues: List[Dict], 
                                          correlations: Dict) -> List[Dict]:
        """Synthesize insights from cross-language pattern analysis"""
        insights = []
        
        # Look for patterns that appear across multiple languages
        for issue_type, cross_patterns in correlations.items():
            if len(cross_patterns) > 1:  # Pattern exists in multiple languages
                insight = {
                    'type': 'cross_language_pattern',
                    'issue_type': issue_type,
                    'description': f'Pattern "{issue_type}" found across {len(cross_patterns)} related languages',
                    'languages': list(cross_patterns.keys()),
                    'recommendation': f'Consider implementing consistent solutions across all languages',
                    'correlation_strength': len(cross_patterns)
                }
                insights.append(insight)
        
        # Look for language-specific solutions that could be adapted
        for issue_type, cross_patterns in correlations.items():
            for language, patterns in cross_patterns.items():
                for pattern in patterns:
                    pattern_content = pattern.get('content', '')
                    if 'solution' in pattern_content.lower() or 'fix' in pattern_content.lower():
                        insight = {
                            'type': 'adaptable_solution',
                            'issue_type': issue_type,
                            'source_language': language,
                            'description': f'Solution pattern from {language} may be adaptable',
                            'pattern_summary': pattern_content[:100] + '...' if len(pattern_content) > 100 else pattern_content,
                            'recommendation': f'Review {language} approach for potential adaptation'
                        }
                        insights.append(insight)
        
        return insights


class LanguageAnalyzerRegistry:
    """Registry for managing multiple language analyzers"""
    
    def __init__(self):
        self.analyzers = {}
        self.extension_map = {}
    
    def register_analyzer(self, analyzer: BaseLanguageAnalyzer):
        """Register a language analyzer"""
        self.analyzers[analyzer.language] = analyzer
        
        # Update extension mapping
        for ext in analyzer.get_supported_extensions():
            if ext not in self.extension_map:
                self.extension_map[ext] = []
            self.extension_map[ext].append(analyzer.language)
    
    def get_analyzer_for_file(self, file_path: str) -> Optional[BaseLanguageAnalyzer]:
        """Get the appropriate analyzer for a file"""
        for ext, languages in self.extension_map.items():
            if file_path.endswith(ext):
                # Return the first analyzer that can handle this extension
                for language in languages:
                    analyzer = self.analyzers.get(language)
                    if analyzer and analyzer.can_analyze_file(file_path):
                        return analyzer
        return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.analyzers.keys())
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions"""
        return list(self.extension_map.keys())
    
    def analyze_project(self, project_path: str) -> Dict:
        """Analyze entire project with all applicable analyzers"""
        results = {
            'languages_detected': [],
            'analysis_results': {},
            'cross_language_insights': [],
            'project_metrics': {}
        }
        
        # Find all files in project
        all_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        
        # Analyze with appropriate analyzers
        for file_path in all_files:
            analyzer = self.get_analyzer_for_file(file_path)
            if analyzer:
                if analyzer.language not in results['languages_detected']:
                    results['languages_detected'].append(analyzer.language)
                
                if analyzer.language not in results['analysis_results']:
                    results['analysis_results'][analyzer.language] = []
                
                file_results = analyzer.analyze_file(file_path)
                results['analysis_results'][analyzer.language].extend(file_results)
        
        # Get metrics for each detected language
        for language in results['languages_detected']:
            analyzer = self.analyzers[language]
            results['project_metrics'][language] = analyzer.get_language_metrics(project_path)
        
        return results


# Global registry instance
language_registry = LanguageAnalyzerRegistry()