"""
Dead File Detector - Identifies unconnected and potentially dead files.

This module implements sophisticated dead file detection with robust false positive
filtering, following the Mesopredator Design Philosophy of dual awareness.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, NamedTuple, Optional
import logging

logger = logging.getLogger(__name__)


class DeadFileIssue(NamedTuple):
    """Represents a potentially dead file with confidence scoring."""
    file_path: str
    issue_type: str  # 'dead_file', 'unconnected_file', 'unused_import_file'
    severity: str
    confidence: float
    evidence: List[str]
    false_positive_reasons: List[str]
    suggestions: List[str]


class DeadFileDetector:
    """
    Detects dead, unconnected, or unused files with robust false positive filtering.

    Uses multiple heuristics to determine file connectivity and filters out
    common false positives like test files, configuration, and entry points.
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.file_map = {}  # file_path -> FileInfo
        self.import_graph = {}  # file -> set of files it imports
        self.reverse_import_graph = {}  # file -> set of files that import it

        # False positive exclusion patterns
        self.false_positive_patterns = {
            # Entry points and executables
            "entry_points": [
                r"main\.py$", r"__main__\.py$", r"run\.py$", r"start\.py$",
                r"app\.py$", r"server\.py$", r"cli\.py$", r"manage\.py$"
            ],

            # Test files
            "test_files": [
                r"test_.*\.py$", r".*_test\.py$", r"tests?/.*\.py$",
                r"conftest\.py$", r".*_tests\.py$"
            ],

            # Configuration files
            "config_files": [
                r"config\.py$", r"settings\.py$", r".*_config\.py$",
                r"setup\.py$", r"conftest\.py$", r"__init__\.py$"
            ],

            # Build and deployment
            "build_files": [
                r"setup\.py$", r"build\.py$", r"deploy\.py$", r"install\.py$",
                r"requirements\.py$", r"version\.py$"
            ],

            # Documentation and examples
            "docs_examples": [
                r"docs?/.*\.py$", r"examples?/.*\.py$", r"demo.*\.py$",
                r"tutorial.*\.py$", r"sample.*\.py$"
            ],

            # Scripts and utilities
            "scripts": [
                r"scripts?/.*\.py$", r"utils?/.*\.py$", r"tools?/.*\.py$",
                r"bin/.*\.py$", r".*_script\.py$"
            ],

            # Framework specific
            "framework_files": [
                r"migrations?/.*\.py$", r"models\.py$", r"views\.py$",
                r"urls\.py$", r"admin\.py$", r"forms\.py$", r"signals\.py$"
            ]
        }

        # Dynamic import patterns that are hard to track statically
        self.dynamic_import_indicators = [
            r"importlib\.import_module",
            r"__import__\s*\(",
            r"exec\s*\(",
            r"eval\s*\(",
            r"getattr\s*\(\s*\w+\s*,.*\)",
            r"plugins?.*load",
            r"dynamic.*import"
        ]

    def analyze_project(self) -> List[DeadFileIssue]:
        """Analyze the entire project for dead files."""
        issues = []

        # First, build the file map and import graph
        self._build_file_map()
        self._build_import_graph()

        # Detect different types of dead files
        issues.extend(self._detect_completely_dead_files())
        issues.extend(self._detect_unconnected_files())
        issues.extend(self._detect_unused_import_only_files())

        # Filter false positives
        filtered_issues = []
        for issue in issues:
            if not self._is_false_positive(issue):
                filtered_issues.append(issue)
            else:
                logger.debug(f"Filtered false positive: {issue.file_path}")

        return filtered_issues

    def _build_file_map(self):
        """Build a map of all Python files in the project."""
        for py_file in self.project_path.rglob("*.py"):
            if self._should_analyze_file(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    self.file_map[str(py_file)] = {
                        'path': py_file,
                        'content': content,
                        'ast': self._safe_parse_ast(content),
                        'size': len(content),
                        'has_main_guard': '__name__ == "__main__"' in content,
                        'has_dynamic_imports': any(re.search(pattern, content)
                                                 for pattern in self.dynamic_import_indicators)
                    }
                except Exception as e:
                    logger.debug(f"Failed to analyze {py_file}: {e}")

    def _build_import_graph(self):
        """Build import dependency graph."""
        for file_path, file_info in self.file_map.items():
            imports = self._extract_imports(file_info['ast'], file_info['content'])
            self.import_graph[file_path] = set()

            for import_name in imports:
                # Try to resolve import to actual file
                resolved_file = self._resolve_import_to_file(import_name, file_path)
                if resolved_file:
                    self.import_graph[file_path].add(resolved_file)

                    # Build reverse graph
                    if resolved_file not in self.reverse_import_graph:
                        self.reverse_import_graph[resolved_file] = set()
                    self.reverse_import_graph[resolved_file].add(file_path)

    def _detect_completely_dead_files(self) -> List[DeadFileIssue]:
        """Detect files that are never imported and have no entry point characteristics."""
        issues = []

        for file_path, file_info in self.file_map.items():
            # Skip if file is imported by others
            if file_path in self.reverse_import_graph and self.reverse_import_graph[file_path]:
                continue

            if file_info['has_main_guard']:
                continue

            if file_info['has_dynamic_imports']:
                continue

            if file_info['size'] < 100:
                continue

            evidence = [
                "File is never imported by other modules",
                "No __main__ guard found",
                f"File size: {file_info['size']} bytes"
            ]

            # Check for other indicators that it might not be dead
            false_positive_reasons = []
            if self._has_class_definitions(file_info['ast']):
                false_positive_reasons.append("Contains class definitions (might be used via dynamic import)")
            if self._has_function_definitions(file_info['ast']):
                false_positive_reasons.append("Contains function definitions")
            if self._has_global_assignments(file_info['ast']):
                false_positive_reasons.append("Contains global variable assignments")

            confidence = self._calculate_dead_file_confidence(file_info, evidence, false_positive_reasons)

            if confidence > 0.6:  # Only report if fairly confident
                issues.append(DeadFileIssue(
                    file_path=str(file_info['path'].relative_to(self.project_path)),
                    issue_type="dead_file",
                    severity="medium" if confidence > 0.8 else "low",
                    confidence=confidence,
                    evidence=evidence,
                    false_positive_reasons=false_positive_reasons,
                    suggestions=[
                        "Consider removing this file if it's truly unused",
                        "Or add it to an __init__.py to make it discoverable",
                        "Or add a __main__ guard if it's meant to be executable"
                    ]
                ))

        return issues

    def _detect_unconnected_files(self) -> List[DeadFileIssue]:
        """Detect files that form isolated clusters or are completely disconnected."""
        issues = []

        # Find connected components in the import graph
        visited = set()
        components = []

        for file_path in self.file_map.keys():
            if file_path not in visited:
                component = self._dfs_component(file_path, visited)
                if len(component) > 0:
                    components.append(component)

        # Look for small isolated components
        for component in components:
            if len(component) == 1:
                file_path = list(component)[0]
                file_info = self.file_map[file_path]

                # Skip entry points and special files
                if file_info['has_main_guard']:
                    continue

                evidence = [
                    "File forms an isolated component in import graph",
                    f"Component size: {len(component)} files"
                ]

                issues.append(DeadFileIssue(
                    file_path=str(file_info['path'].relative_to(self.project_path)),
                    issue_type="unconnected_file",
                    severity="low",
                    confidence=0.7,
                    evidence=evidence,
                    false_positive_reasons=[],
                    suggestions=[
                        "Consider connecting this file to the main application",
                        "Or verify if it's meant to be a standalone utility"
                    ]
                ))

        return issues

    def _detect_unused_import_only_files(self) -> List[DeadFileIssue]:
        """Detect files that only contain imports but export nothing useful."""
        issues = []

        for file_path, file_info in self.file_map.items():
            ast_tree = file_info['ast']
            if not ast_tree:
                continue

            # Analyze what the file contains
            imports = sum(1 for node in ast.walk(ast_tree)
                         if isinstance(node, (ast.Import, ast.ImportFrom)))
            functions = sum(1 for node in ast.walk(ast_tree)
                           if isinstance(node, ast.FunctionDef))
            classes = sum(1 for node in ast.walk(ast_tree)
                         if isinstance(node, ast.ClassDef))
            assignments = sum(1 for node in ast.walk(ast_tree)
                             if isinstance(node, ast.Assign))

            # If file is mostly imports with little actual content
            if imports > 0 and (functions + classes + assignments) <= 2:
                evidence = [
                    f"File contains {imports} imports but only {functions + classes + assignments} definitions",
                    "Might be an unused import aggregation file"
                ]

                issues.append(DeadFileIssue(
                    file_path=str(file_info['path'].relative_to(self.project_path)),
                    issue_type="unused_import_file",
                    severity="low",
                    confidence=0.6,
                    evidence=evidence,
                    false_positive_reasons=["Might be a legitimate module aggregator"],
                    suggestions=[
                        "Consider removing if imports are unused",
                        "Or document the purpose of this aggregation file"
                    ]
                ))

        return issues

    def _is_false_positive(self, issue: DeadFileIssue) -> bool:
        """Check if an issue is likely a false positive."""
        file_path = issue.file_path

        # Check against false positive patterns
        for category, patterns in self.false_positive_patterns.items():
            for pattern in patterns:
                if re.search(pattern, file_path, re.IGNORECASE):
                    logger.debug(f"False positive ({category}): {file_path}")
                    return True

        # Additional contextual checks
        if self._is_framework_file(file_path):
            return True

        if self._is_configuration_file(file_path):
            return True

        return False

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determine if a file should be included in analysis."""
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            return False

        # Skip common directories that contain non-application code
        skip_dirs = {'__pycache__', '.pytest_cache', 'node_modules', '.git',
                    'build', 'dist', '.tox', '.venv', 'venv'}

        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return False

        return True

    def _safe_parse_ast(self, content: str) -> Optional[ast.AST]:
        """Safely parse Python content to AST."""
        try:
            return ast.parse(content)
        except SyntaxError:
            return None

    def _extract_imports(self, ast_tree: Optional[ast.AST], content: str) -> Set[str]:
        """Extract import names from AST."""
        imports = set()

        if not ast_tree:
            return imports

        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
                    for alias in node.names:
                        imports.add(f"{node.module}.{alias.name}")

        return imports

    def _resolve_import_to_file(self, import_name: str, current_file: str) -> Optional[str]:
        """Try to resolve an import name to an actual file path."""
        # This is a simplified implementation
        # A complete version would handle package structure, __init__.py files, etc.

        current_dir = Path(current_file).parent

        # Try relative imports
        possible_files = [
            current_dir / f"{import_name}.py",
            current_dir / import_name / "__init__.py",
            self.project_path / f"{import_name.replace('.', '/')}.py",
            self.project_path / import_name.replace('.', '/') / "__init__.py"
        ]

        for possible_file in possible_files:
            if possible_file.exists() and str(possible_file) in self.file_map:
                return str(possible_file)

        return None

    def _dfs_component(self, start_file: str, visited: Set[str]) -> Set[str]:
        """DFS to find connected component."""
        component = set()
        stack = [start_file]

        while stack:
            file_path = stack.pop()
            if file_path in visited:
                continue

            visited.add(file_path)
            component.add(file_path)

            if file_path in self.import_graph:
                stack.extend(self.import_graph[file_path])
            if file_path in self.reverse_import_graph:
                stack.extend(self.reverse_import_graph[file_path])

        return component

    def _calculate_dead_file_confidence(self, file_info: Dict, evidence: List[str],
                                      false_positive_reasons: List[str]) -> float:
        """Calculate confidence that a file is actually dead."""
        confidence = 0.8  # Base confidence

        # Reduce confidence for false positive indicators
        confidence -= len(false_positive_reasons) * 0.15

        # Increase confidence for strong evidence
        if file_info['size'] > 1000:  # Large files are more suspicious if unused
            confidence += 0.1

        if not file_info['has_dynamic_imports']:
            confidence += 0.1

        return max(0.0, min(1.0, confidence))

    def _has_class_definitions(self, ast_tree: Optional[ast.AST]) -> bool:
        """Check if AST contains class definitions."""
        if not ast_tree:
            return False
        return any(isinstance(node, ast.ClassDef) for node in ast.walk(ast_tree))

    def _has_function_definitions(self, ast_tree: Optional[ast.AST]) -> bool:
        """Check if AST contains function definitions."""
        if not ast_tree:
            return False
        return any(isinstance(node, ast.FunctionDef) for node in ast.walk(ast_tree))

    def _has_global_assignments(self, ast_tree: Optional[ast.AST]) -> bool:
        """Check if AST contains global variable assignments."""
        if not ast_tree:
            return False
        return any(isinstance(node, ast.Assign) for node in ast.walk(ast_tree))

    def _is_framework_file(self, file_path: str) -> bool:
        """Check if file is a framework-specific file."""
        framework_indicators = [
            'models.py', 'views.py', 'urls.py', 'admin.py', 'forms.py',
            'serializers.py', 'signals.py', 'apps.py', 'middleware.py'
        ]
        return any(indicator in file_path for indicator in framework_indicators)

    def _is_configuration_file(self, file_path: str) -> bool:
        """Check if file is a configuration file."""
        config_indicators = [
            'config', 'settings', 'constants', 'version', '__init__'
        ]
        return any(indicator in file_path.lower() for indicator in config_indicators)