#!/usr/bin/env python3
"""
Code Connector - Generative Dependency Synthesis for Enhanced Code Reuse

This module implements the "Code Connector" capability that transforms Mesopredator
from a strategic coordinator to a creative architect. It analyzes orphaned code files
and suggests intelligent ways to integrate them into the main codebase.

Architecture Decision: This bridges the gap between Strategic Intelligence (coordinating
existing tools) and Creative Intelligence (generating new solutions).
"""

import ast
import logging
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Optional, NamedTuple

# Import metrics collection
try:
    from .connection_metrics import (
        start_metrics_collection, record_suggestion_metrics, 
        finish_metrics_collection, get_real_time_stats, get_performance_trends
    )
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

logger = logging.getLogger(__name__)


class ConnectionSuggestion(NamedTuple):
    """Represents a suggested connection between an orphaned file and main codebase"""
    orphaned_file: str
    target_file: str
    connection_score: float
    connection_type: str
    integration_suggestions: List[str]
    reasoning: List[str]


class FileCapabilities(NamedTuple):
    """Represents the capabilities analysis of a file"""
    functions: List[Dict]
    classes: List[Dict]
    constants: List[str]
    imports: List[str]
    keywords: Set[str]
    complexity_score: int
    has_main_guard: bool
    file_size: int


class CodeConnector:
    """
    Intelligent code connection system that suggests ways to integrate orphaned files.
    
    Implements the two-phase approach:
    Phase 1: Analysis and Opportunity Identification
    Phase 2: Generative Connection Synthesis
    """

    def __init__(self, project_path: str, confidence_threshold: float = 0.3):
        self.project_path = Path(project_path)
        self.confidence_threshold = confidence_threshold
        self.connection_cache = {}
        
        # Semantic analysis patterns
        self.semantic_patterns = {
            "utility_patterns": [
                r"\butil\b", r"\bhelper\b", r"\btool\b", r"\bcommon\b"
            ],
            "data_patterns": [
                r"\bdata\b", r"\bmodel\b", r"\bschema\b", r"\bentity\b"
            ],
            "service_patterns": [
                r"\bservice\b", r"\bapi\b", r"\bclient\b", r"\bhandler\b"
            ],
            "config_patterns": [
                r"\bconfig\b", r"\bsetting\b", r"\bconstant\b", r"\benv\b"
            ]
        }

    def analyze_orphaned_files(self, orphaned_files: List[Path], 
                             main_files: List[Path]) -> List[ConnectionSuggestion]:
        """
        Main entry point for Code Connector analysis with integrated metrics collection.
        
        Phase 1: Build capability maps for orphaned and main files
        Phase 2: Generate ranked connection suggestions
        """
        start_time = time.time()
        
        # Start metrics collection
        run_id = f"analysis_{int(start_time)}"
        if METRICS_AVAILABLE:
            start_metrics_collection(run_id, str(self.project_path), len(orphaned_files), len(main_files))
            logger.info(f"📊 Metrics collection started for run: {run_id}")
        
        logger.info(f"Analyzing {len(orphaned_files)} orphaned files against {len(main_files)} main files")
        
        # Phase 1: Analysis and Opportunity Identification
        logger.info("🔍 Phase 1: Analyzing file capabilities...")
        orphaned_capabilities = self._analyze_file_batch(orphaned_files)
        main_capabilities = self._analyze_file_batch(main_files)
        
        # Build dependency graph for main files
        dependency_graph = self._build_dependency_graph(main_files)
        
        # Phase 2: Generative Connection Synthesis
        logger.info("🧠 Phase 2: Generating connection suggestions...")
        suggestions = []
        for orphaned_file, orphaned_caps in orphaned_capabilities.items():
            file_start_time = time.time()
            
            file_suggestions = self._generate_file_suggestions(
                orphaned_file, orphaned_caps, main_capabilities, dependency_graph
            )
            
            # Record metrics for each suggestion
            if METRICS_AVAILABLE:
                file_processing_time = (time.time() - file_start_time) * 1000  # Convert to ms
                for suggestion in file_suggestions:
                    record_suggestion_metrics(suggestion, file_processing_time / len(file_suggestions))
            
            suggestions.extend(file_suggestions)
            
            # Show real-time progress if metrics available
            if METRICS_AVAILABLE and len(suggestions) % 5 == 0:  # Every 5 suggestions
                stats = get_real_time_stats()
                if stats.get('status') != 'no_run_active':
                    logger.info(f"   📈 Progress: {stats['suggestions_so_far']} suggestions, "
                              f"avg score: {stats['current_avg_score']:.3f}, "
                              f"max: {stats['current_max_score']:.3f}")
        
        # Sort by confidence and filter
        suggestions.sort(key=lambda x: x.connection_score, reverse=True)
        filtered_suggestions = [s for s in suggestions if s.connection_score >= self.confidence_threshold]
        
        # Finish metrics collection and log results
        if METRICS_AVAILABLE:
            metrics = finish_metrics_collection(filtered_suggestions)
            
            # Log performance summary
            logger.info(f"📊 Analysis completed with metrics:")
            logger.info(f"   ⏱️  Total time: {metrics.processing_time_seconds:.2f}s")
            logger.info(f"   🔗 Total suggestions: {metrics.total_suggestions}")
            logger.info(f"   📈 Average score: {metrics.avg_connection_score:.3f}")
            logger.info(f"   🎯 Max score: {metrics.max_connection_score:.3f}")
            logger.info(f"   ✨ Excellent (>0.8): {metrics.excellent_connections}")
            logger.info(f"   🟢 High-value %: {metrics.high_value_percentage:.1f}%")
            
            # Show improvement trends if available
            trends = get_performance_trends()
            if trends.get('status') != 'insufficient_data':
                score_trend = trends['score_trend']
                quality_trend = trends['quality_trend']
                
                if score_trend['improvement'] != 0:
                    trend_emoji = "📈" if score_trend['improvement'] > 0 else "📉"
                    logger.info(f"   {trend_emoji} Score trend: {score_trend['improvement']:+.3f} vs previous run")
                
                if quality_trend['improvement'] != 0:
                    quality_emoji = "📈" if quality_trend['improvement'] > 0 else "📉"
                    logger.info(f"   {quality_emoji} Quality trend: {quality_trend['improvement']:+.1f}% vs previous run")
        
        processing_time = time.time() - start_time
        logger.info(f"✅ Analysis complete: {len(filtered_suggestions)} suggestions in {processing_time:.2f}s")
        
        return filtered_suggestions

    def _analyze_file_batch(self, files: List[Path]) -> Dict[str, FileCapabilities]:
        """Analyze a batch of files to extract capabilities"""
        capabilities = {}
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                ast_tree = ast.parse(content)
                caps = self._analyze_file_capabilities(ast_tree, content, file_path)
                capabilities[str(file_path)] = caps
                
            except Exception as e:
                logger.debug(f"Error analyzing {file_path}: {e}")
        
        return capabilities

    def _analyze_file_capabilities(self, ast_tree: ast.AST, content: str, 
                                 file_path: Path) -> FileCapabilities:
        """Deep analysis of a single file's capabilities"""
        functions = []
        classes = []
        constants = []
        imports = []
        complexity_score = 0
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._extract_return_type(node),
                    "docstring": ast.get_docstring(node),
                    "line": node.lineno,
                    "complexity": self._calculate_function_complexity(node),
                    "is_public": not node.name.startswith('_'),
                    "decorators": self._extract_decorators(node)
                }
                functions.append(func_info)
                complexity_score += func_info["complexity"]
            
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "docstring": ast.get_docstring(node),
                    "line": node.lineno,
                    "is_public": not node.name.startswith('_'),
                    "decorators": self._extract_decorators(node),
                    "properties": self._extract_properties(node)
                }
                classes.append(class_info)
            
            elif isinstance(node, ast.Assign):
                constants.extend(self._extract_constants(node))
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.extend(self._extract_imports_from_node(node))
        
        keywords = self._extract_semantic_keywords(content, file_path)
        has_main_guard = '__name__ == "__main__"' in content
        file_size = len(content)
        
        return FileCapabilities(
            functions=functions,
            classes=classes,
            constants=constants,
            imports=imports,
            keywords=keywords,
            complexity_score=complexity_score,
            has_main_guard=has_main_guard,
            file_size=file_size
        )

    def _generate_file_suggestions(self, orphaned_file: str, orphaned_caps: FileCapabilities,
                                 main_capabilities: Dict[str, FileCapabilities],
                                 dependency_graph: Dict[str, Set[str]]) -> List[ConnectionSuggestion]:
        """Generate connection suggestions for a single orphaned file"""
        suggestions = []
        
        for main_file, main_caps in main_capabilities.items():
            # Calculate multiple connection scores
            semantic_score = self._calculate_semantic_similarity(orphaned_caps, main_caps)
            structural_score = self._calculate_structural_compatibility(orphaned_caps, main_caps)
            dependency_score = self._calculate_dependency_synergy(orphaned_caps, main_caps)
            need_score = self._calculate_need_score(orphaned_caps, main_caps, main_file)
            
            # Weighted composite score with boosted weights for strong signals
            composite_score = (
                semantic_score * 0.35 +      # Increased semantic weight
                structural_score * 0.25 +
                dependency_score * 0.20 +    # Reduced dependency weight
                need_score * 0.35            # Significantly increased need detection weight
            )
            
            # Boost score for high-confidence individual components
            if semantic_score > 0.5:
                composite_score += 0.1
            if need_score > 0.3:
                composite_score += 0.15  # Strong bonus for detected needs
            
            if composite_score >= self.confidence_threshold:
                connection_type = self._determine_optimal_connection_type(orphaned_caps, main_caps)
                integration_suggestions = self._generate_integration_suggestions(
                    orphaned_file, orphaned_caps, main_file, main_caps
                )
                reasoning = self._generate_reasoning(
                    semantic_score, structural_score, dependency_score, need_score
                )
                
                suggestion = ConnectionSuggestion(
                    orphaned_file=str(Path(orphaned_file).relative_to(self.project_path)),
                    target_file=str(Path(main_file).relative_to(self.project_path)),
                    connection_score=composite_score,
                    connection_type=connection_type,
                    integration_suggestions=integration_suggestions,
                    reasoning=reasoning
                )
                suggestions.append(suggestion)
        
        return suggestions

    def _calculate_semantic_similarity(self, orphaned_caps: FileCapabilities, 
                                     main_caps: FileCapabilities) -> float:
        """Calculate semantic similarity based on keywords, names, and purpose"""
        score = 0.0
        
        # Keyword overlap
        keyword_overlap = orphaned_caps.keywords.intersection(main_caps.keywords)
        if keyword_overlap:
            score += min(0.4, len(keyword_overlap) * 0.08)
        
        # Function name similarity (semantic analysis)
        orphaned_func_words = set()
        main_func_words = set()
        
        for func in orphaned_caps.functions:
            orphaned_func_words.update(self._extract_words_from_name(func["name"]))
        
        for func in main_caps.functions:
            main_func_words.update(self._extract_words_from_name(func["name"]))
        
        func_word_overlap = orphaned_func_words.intersection(main_func_words)
        if func_word_overlap:
            score += min(0.3, len(func_word_overlap) * 0.1)
        
        # Class name similarity
        orphaned_class_words = set()
        main_class_words = set()
        
        for cls in orphaned_caps.classes:
            orphaned_class_words.update(self._extract_words_from_name(cls["name"]))
        
        for cls in main_caps.classes:
            main_class_words.update(self._extract_words_from_name(cls["name"]))
        
        class_word_overlap = orphaned_class_words.intersection(main_class_words)
        if class_word_overlap:
            score += min(0.3, len(class_word_overlap) * 0.15)
        
        return min(1.0, score)

    def _calculate_structural_compatibility(self, orphaned_caps: FileCapabilities,
                                          main_caps: FileCapabilities) -> float:
        """Calculate how well the structures would fit together"""
        score = 0.0
        
        # Complementary functions (not duplicates)
        orphaned_func_names = {f["name"] for f in orphaned_caps.functions}
        main_func_names = {f["name"] for f in main_caps.functions}
        
        if orphaned_func_names and not orphaned_func_names.intersection(main_func_names):
            score += 0.4  # Good - no name conflicts
        elif orphaned_func_names.intersection(main_func_names):
            score -= 0.2  # Bad - name conflicts
        
        # Import compatibility
        orphaned_imports = set(orphaned_caps.imports)
        main_imports = set(main_caps.imports)
        import_overlap = orphaned_imports.intersection(main_imports)
        
        if import_overlap:
            score += min(0.3, len(import_overlap) * 0.05)
        
        # Complexity balance
        complexity_ratio = orphaned_caps.complexity_score / max(main_caps.complexity_score, 1)
        if 0.1 <= complexity_ratio <= 2.0:  # Reasonable complexity balance
            score += 0.2
        
        return min(1.0, score)

    def _calculate_dependency_synergy(self, orphaned_caps: FileCapabilities,
                                    main_caps: FileCapabilities) -> float:
        """Calculate how well dependencies would work together"""
        score = 0.0
        
        # Shared dependencies suggest compatibility
        orphaned_imports = set(orphaned_caps.imports)
        main_imports = set(main_caps.imports)
        shared_imports = orphaned_imports.intersection(main_imports)
        
        if shared_imports:
            score += min(0.5, len(shared_imports) * 0.1)
        
        # Look for complementary import patterns
        orphaned_external = {imp for imp in orphaned_imports if not imp.startswith('.')}
        main_external = {imp for imp in main_imports if not imp.startswith('.')}
        
        # Check for imports that suggest similar problem domains
        domain_overlap = self._calculate_domain_overlap(orphaned_external, main_external)
        score += domain_overlap * 0.3
        
        return min(1.0, score)

    def _calculate_need_score(self, orphaned_caps: FileCapabilities, 
                            main_caps: FileCapabilities, main_file: str) -> float:
        """Calculate how much the main file might need the orphaned functionality"""
        score = 0.0
        
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                main_content = f.read()
            
            # Look for TODO, FIXME, NotImplementedError
            need_indicators = [
                r'#\s*# ADDRESSED:?\s*(.*?)(?:\n|$)',
                r'#\s*FIXME:?\s*(.*?)(?:\n|$)',
                r'NotImplementedError',
                r'pass\s*#.*(?:TODO|FIXME|implement)'
            ]
            
            for pattern in need_indicators:
                matches = re.findall(pattern, main_content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    # Check if orphaned file might address these needs
                    for match in matches:
                        if isinstance(match, str):
                            match_lower = match.lower()
                            for func in orphaned_caps.functions:
                                func_words = self._extract_words_from_name(func["name"])
                                if any(word in match_lower for word in func_words):
                                    score += 0.3
            
            # Enhanced pattern matching for specific functionality
            functionality_patterns = {
                'cache': [r'cache\s*=\s*{}', r'#.*cache', r'TODO.*cach', r'simple.*cache'],
                'validation': [r'validate', r'TODO.*valid', r'#.*valid', r'email.*@'],
                'metrics': [r'TODO.*metric', r'#.*track', r'performance', r'monitoring'],
                'progress': [r'TODO.*progress', r'#.*track.*progress', r'processing.*progress']
            }
            
            orphaned_keywords = {word.lower() for word in orphaned_caps.keywords}
            
            for domain, patterns in functionality_patterns.items():
                if domain in orphaned_keywords or any(domain in func["name"].lower() for func in orphaned_caps.functions):
                    for pattern in patterns:
                        if re.search(pattern, main_content, re.IGNORECASE):
                            score += 0.25  # Strong domain match
            
            # Look for placeholder or stub functions
            stub_patterns = [
                r'def\s+\w+\s*\([^)]*\):\s*pass',
                r'def\s+\w+\s*\([^)]*\):\s*\.\.\.',
                r'def\s+\w+\s*\([^)]*\):\s*raise\s+NotImplementedError'
            ]
            
            for pattern in stub_patterns:
                if re.search(pattern, main_content):
                    score += 0.2
            
            # Bonus for simple implementations that could be enhanced
            simple_implementations = [
                r'self\.cache\s*=\s*{}',  # Simple dict cache
                r'return.*@.*in',        # Simple email check
                r'len\([^)]+\)',         # Simple size calculations
            ]
            
            for pattern in simple_implementations:
                if re.search(pattern, main_content):
                    score += 0.15  # Replacement opportunity
        
        except Exception:
            pass
        
        return min(1.0, score)

    def _determine_optimal_connection_type(self, orphaned_caps: FileCapabilities,
                                         main_caps: FileCapabilities) -> str:
        """Determine the best way to connect the orphaned file"""
        if orphaned_caps.classes and orphaned_caps.functions:
            return "module_import"
        elif orphaned_caps.classes:
            if len(orphaned_caps.classes) == 1:
                return "class_import"
            else:
                return "selective_class_import"
        elif orphaned_caps.functions:
            if len(orphaned_caps.functions) == 1:
                return "function_import"
            elif len(orphaned_caps.functions) <= 3:
                return "selective_function_import"
            else:
                return "module_import"
        elif orphaned_caps.constants:
            return "constant_import"
        else:
            return "utility_import"

    def _generate_integration_suggestions(self, orphaned_file: str, orphaned_caps: FileCapabilities,
                                        main_file: str, main_caps: FileCapabilities) -> List[str]:
        """Generate specific code suggestions for integration"""
        suggestions = []
        
        orphaned_path = Path(orphaned_file)
        main_path = Path(main_file)
        
        # Calculate relative import path
        try:
            rel_path = orphaned_path.relative_to(main_path.parent)
            import_name = str(rel_path.with_suffix('')).replace('/', '.')
        except ValueError:
            # Files in different parts of the tree
            try:
                common_parent = self._find_common_parent(orphaned_path, main_path)
                rel_path = orphaned_path.relative_to(common_parent)
                import_name = str(rel_path.with_suffix('')).replace('/', '.')
            except Exception as e:
                import_name = orphaned_path.stem
        
        # Generate import suggestions based on capabilities
        if orphaned_caps.functions:
            if len(orphaned_caps.functions) == 1:
                func_name = orphaned_caps.functions[0]["name"]
                suggestions.append(f"from {import_name} import {func_name}")
            elif len(orphaned_caps.functions) <= 3:
                func_names = [f["name"] for f in orphaned_caps.functions if f["is_public"]][:3]
                if func_names:
                    suggestions.append(f"from {import_name} import {', '.join(func_names)}")
            else:
                suggestions.append(f"import {import_name}")
        
        if orphaned_caps.classes:
            if len(orphaned_caps.classes) == 1:
                class_name = orphaned_caps.classes[0]["name"]
                suggestions.append(f"from {import_name} import {class_name}")
            else:
                class_names = [c["name"] for c in orphaned_caps.classes if c["is_public"]][:2]
                if class_names:
                    suggestions.append(f"from {import_name} import {', '.join(class_names)}")
        
        if orphaned_caps.constants:
            const_names = orphaned_caps.constants[:3]
            if const_names:
                suggestions.append(f"from {import_name} import {', '.join(const_names)}")
        
        # Suggest integration points in main file
        integration_points = self._find_integration_points(main_file, main_caps)
        for point in integration_points[:2]:  # Top 2 integration points
            suggestions.append(f"Consider integrating at line {point['line']}: {point['suggestion']}")
        
        return suggestions

    def _generate_reasoning(self, semantic_score: float, structural_score: float,
                          dependency_score: float, need_score: float) -> List[str]:
        """Generate human-readable reasoning for the connection suggestion"""
        reasoning = []
        
        if semantic_score > 0.3:
            reasoning.append(f"High semantic similarity (score: {semantic_score:.2f}) - files work in related domains")
        
        if structural_score > 0.3:
            reasoning.append(f"Good structural compatibility (score: {structural_score:.2f}) - no conflicts detected")
        
        if dependency_score > 0.3:
            reasoning.append(f"Synergistic dependencies (score: {dependency_score:.2f}) - shared imports suggest compatibility")
        
        if need_score > 0.2:
            reasoning.append(f"Detected potential need (score: {need_score:.2f}) - main file has TODOs or stubs that orphaned file might address")
        
        if not reasoning:
            reasoning.append("Connection based on general compatibility metrics")
        
        return reasoning

    # Helper methods
    def _build_dependency_graph(self, files: List[Path]) -> Dict[str, Set[str]]:
        """Build a simple dependency graph for the main files"""
        graph = {}
        for file_path in files:
            graph[str(file_path)] = set()
            # This is a simplified implementation
            # A full implementation would parse imports and resolve to actual files
        return graph

    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _extract_decorators(self, node) -> List[str]:
        """Extract decorator names from a function or class"""
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(decorator.attr)
        return decorators

    def _extract_properties(self, class_node: ast.ClassDef) -> List[str]:
        """Extract property names from a class"""
        properties = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                if any(isinstance(d, ast.Name) and d.id == 'property' for d in node.decorator_list):
                    properties.append(node.name)
        return properties

    def _extract_constants(self, assign_node: ast.Assign) -> List[str]:
        """Extract constant names from assignment"""
        constants = []
        for target in assign_node.targets:
            if isinstance(target, ast.Name) and target.id.isupper():
                constants.append(target.id)
        return constants

    def _extract_imports_from_node(self, node) -> List[str]:
        """Extract import names from import nodes"""
        imports = []
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        return imports

    def _extract_semantic_keywords(self, content: str, file_path: Path) -> Set[str]:
        """Extract semantic keywords from file content and path"""
        keywords = set()
        
        # Extract from file path
        path_words = re.findall(r'\b\w{3,}\b', str(file_path).lower())
        keywords.update(path_words)
        
        # Extract from comments
        comment_matches = re.findall(r'#\s*(.*?)(?:\n|$)', content)
        for comment in comment_matches:
            words = re.findall(r'\b\w{3,}\b', comment.lower())
            keywords.update(words)
        
        # Extract from docstrings
        docstring_matches = re.findall(r'"""(.*?)"""', content, re.DOTALL)
        for docstring in docstring_matches:
            words = re.findall(r'\b\w{3,}\b', docstring.lower())
            keywords.update(words)
        
        # Extract from string literals (often contain domain-specific terms)
        string_matches = re.findall(r'["\']([^"\']{3,})["\']', content)
        for string_val in string_matches:
            words = re.findall(r'\b\w{3,}\b', string_val.lower())
            keywords.update(words)
        
        # Extract from variable and function names
        var_matches = re.findall(r'\b([a-z_][a-z0-9_]{2,})\b', content.lower())
        keywords.update(var_matches)
        
        # Add domain-specific technical terms that indicate functionality
        domain_indicators = {
            'cache', 'caching', 'cached', 'memory', 'storage', 'store',
            'validate', 'validation', 'validator', 'check', 'verify',
            'metric', 'metrics', 'measure', 'track', 'monitor', 'performance',
            'progress', 'tracker', 'processing', 'status', 'completion',
            'data', 'process', 'processing', 'engine', 'handler',
            'config', 'configuration', 'settings', 'options',
            'log', 'logging', 'logger', 'debug', 'error', 'warning'
        }
        
        # Keep domain indicators that appear in content
        content_lower = content.lower()
        for indicator in domain_indicators:
            if indicator in content_lower:
                keywords.add(indicator)
        
        # Filter out common programming terms
        common_terms = {
            'def', 'class', 'import', 'from', 'return', 'self', 'args', 'kwargs',
            'true', 'false', 'none', 'and', 'not', 'with', 'for', 'while',
            'init', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple',
            'len', 'range', 'type', 'isinstance', 'hasattr', 'getattr'
        }
        
        return keywords - common_terms

    def _extract_words_from_name(self, name: str) -> Set[str]:
        """Extract meaningful words from function/class names"""
        # Handle camelCase and snake_case
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
        words.extend(name.split('_'))
        return {word.lower() for word in words if len(word) > 2}

    def _calculate_domain_overlap(self, imports1: Set[str], imports2: Set[str]) -> float:
        """Calculate domain overlap based on import patterns"""
        # Group imports by domain
        domains1 = self._categorize_imports(imports1)
        domains2 = self._categorize_imports(imports2)
        
        overlap_score = 0.0
        total_domains = len(set(domains1.keys()) | set(domains2.keys()))
        
        if total_domains == 0:
            return 0.0
        
        for domain in domains1:
            if domain in domains2:
                overlap_score += 1.0
        
        return overlap_score / total_domains

    def _categorize_imports(self, imports: Set[str]) -> Dict[str, List[str]]:
        """Categorize imports by domain"""
        categories = {
            'web': ['flask', 'django', 'requests', 'urllib', 'http'],
            'data': ['pandas', 'numpy', 'scipy', 'matplotlib', 'sqlite3'],
            'ml': ['sklearn', 'tensorflow', 'torch', 'keras'],
            'system': ['os', 'sys', 'subprocess', 'threading'],
            'testing': ['pytest', 'unittest', 'mock'],
            'parsing': ['json', 'xml', 'yaml', 'csv', 're']
        }
        
        result = defaultdict(list)
        for imp in imports:
            for category, patterns in categories.items():
                if any(pattern in imp.lower() for pattern in patterns):
                    result[category].append(imp)
                    break
            else:
                result['other'].append(imp)
        
        return dict(result)

    def _find_integration_points(self, main_file: str, main_caps: FileCapabilities) -> List[Dict]:
        """Find potential integration points in main file"""
        points = []
        
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Look for TODO comments
            for i, line in enumerate(lines):
                if re.search(r'#\s*TODO', line, re.IGNORECASE):
                    points.append({
                        'line': i + 1,
                        'suggestion': f"TODO comment suggests potential integration point"
                    })
            
            # Look for short functions that might need expansion
            for func in main_caps.functions:
                if func["complexity"] <= 2:  # Very simple functions
                    points.append({
                        'line': func["line"],
                        'suggestion': f"Function '{func['name']}' might benefit from additional functionality"
                    })
        
        except Exception:
            pass
        
        return points

    def _find_common_parent(self, path1: Path, path2: Path) -> Path:
        """Find common parent directory of two paths"""
        parts1 = path1.parts
        parts2 = path2.parts
        
        common_parts = []
        for p1, p2 in zip(parts1, parts2):
            if p1 == p2:
                common_parts.append(p1)
            else:
                break
        
        return Path(*common_parts) if common_parts else Path('.')

    def _extract_return_type(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation"""
        if func_node.returns:
            if isinstance(func_node.returns, ast.Name):
                return func_node.returns.id
            elif isinstance(func_node.returns, ast.Constant):
                return str(func_node.returns.value)
        return None

    def _get_base_name(self, base_node: ast.expr) -> str:
        """Get base class name from AST node"""
        if isinstance(base_node, ast.Name):
            return base_node.id
        elif isinstance(base_node, ast.Attribute):
            return base_node.attr
        return "Unknown"


def suggest_code_connections(project_path: str, orphaned_files: List[str], 
                           main_files: List[str], confidence_threshold: float = 0.3) -> List[ConnectionSuggestion]:
    """
    Main API function for generating code connection suggestions.
    
    Args:
        project_path: Root path of the project
        orphaned_files: List of orphaned file paths
        main_files: List of main codebase file paths
        confidence_threshold: Minimum confidence for suggestions
    
    Returns:
        List of connection suggestions sorted by confidence
    """
    connector = CodeConnector(project_path, confidence_threshold)
    
    orphaned_paths = [Path(f) for f in orphaned_files]
    main_paths = [Path(f) for f in main_files]
    
    return connector.analyze_orphaned_files(orphaned_paths, main_paths)


if __name__ == "__main__":
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Code Connector - Suggest intelligent code integrations")
    parser.add_argument("project_path", help="Path to the project")
    parser.add_argument("--orphaned", nargs="+", help="Orphaned file paths")
    parser.add_argument("--main", nargs="+", help="Main codebase file paths")
    parser.add_argument("--threshold", type=float, default=0.3, help="Confidence threshold")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    suggestions = suggest_code_connections(
        args.project_path,
        args.orphaned or [],
        args.main or [],
        args.threshold
    )
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump([s._asdict() for s in suggestions], f, indent=2)
    else:
        logger.info(f"\n🔗 Code Connector Analysis Results")
        logger.info("=" * 50)
        logger.info(f"📊 Total Suggestions: {len(suggestions)}")
        
        for suggestion in suggestions[:10]:  # Show top 10
            logger.info(f"\n📁 {suggestion.orphaned_file}")
            logger.info(f"   → {suggestion.target_file} (score: {suggestion.connection_score:.3f})")
            logger.info(f"   🔧 {suggestion.connection_type}")
            if suggestion.integration_suggestions:
                logger.info(f"   💡 {suggestion.integration_suggestions[0]}")
            if suggestion.reasoning:
                logger.info(f"   📝 {suggestion.reasoning[0]}")