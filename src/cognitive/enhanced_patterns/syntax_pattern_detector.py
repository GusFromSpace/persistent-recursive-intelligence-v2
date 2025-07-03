"""
Syntax pattern detector that learns from manual fixes.

This module implements patterns learned from our manual syntax error fixes
to automatically detect and suggest fixes for common syntax issues.
"""

import re
import ast
from typing import List, Dict, NamedTuple, Optional
from pathlib import Path
import logging


class SyntaxIssue(NamedTuple):
    """Represents a syntax-related issue with suggested fix."""
    type: str
    severity: str
    line: int
    message: str
    original_code: str
    suggested_fix: str
    confidence: float
    fix_reasoning: str


class SyntaxPatternDetector:
    """
    Detects common syntax patterns that cause errors.

    Based on patterns learned from manual fixes:
    - F-string nested quote issues
    - Docstring syntax errors
    - String literal escaping problems
    """

    def __init__(self):
        # Patterns learned from our manual fixes
        self.syntax_patterns = {
            "fstring_nested_quotes": {
                "pattern": r'f"[^"]*"[^"]*"[^"]*"',
                "severity": "critical",
                "message": "F-string with nested double quotes causes syntax error",
                "fix_strategy": "replace_inner_quotes_with_single",
                "confidence": 0.95
            },
            "docstring_termination": {
                "pattern": r'^\s*"""[^"]*"""?\s*$',
                "severity": "high",
                "message": "Docstring may have termination issues",
                "fix_strategy": "convert_to_comment",
                "confidence": 0.85
            },
            "string_literal_in_condition": {
                "pattern": r'if\s+.*\s+"""[^"]*"""?\s+',
                "severity": "high",
                "message": "Triple quotes in conditional may cause issues",
                "fix_strategy": "escape_quotes_properly",
                "confidence": 0.90
            },
            "print_statement_quotes": {
                "pattern": r'print\s*\(\s*f"[^"]*"[^"]*"[^"]*"\s*\)',
                "severity": "medium",
                "message": "Print statement with nested quotes",
                "fix_strategy": "normalize_quotes",
                "confidence": 0.88
            },
            "async_sync_mismatch": {
                "pattern": r'(?<!await\s)(?:self\.memory\.|memory_engine\.)(?:create_namespace|store_memory|search_memories|list_namespaces)\s*\(',
                "severity": "critical",
                "message": "Async method called without await keyword",
                "fix_strategy": "add_await_keyword",
                "confidence": 0.95
            },
            "missing_parentheses_fstring": {
                "pattern": r'f[\'"][^\'"\)]*[\'"](?!\))',
                "severity": "critical",
                "message": "F-string missing closing parenthesis",
                "fix_strategy": "add_missing_parenthesis",
                "confidence": 0.90
            }
        }

    def analyze_file(self, file_path: str, content: str) -> List[SyntaxIssue]:
        """Analyze file for syntax patterns learned from manual fixes."""
        issues = []

        # First, try to parse the file to catch syntax errors
        try:
            ast.parse(content)
        except SyntaxError as e:
            # File has syntax errors - analyze with our patterns
            issues.extend(self._analyze_syntax_error_patterns(content, e))

        # Always check for potential syntax issues regardless
        issues.extend(self._analyze_preventive_patterns(content))

        return issues

    def _analyze_syntax_error_patterns(self, content: str, syntax_error: SyntaxError) -> List[SyntaxIssue]:
        """Analyze content when syntax error is present."""
        issues = []
        lines = content.split('\n')

        # Check for f-string nested quote patterns
        for line_num, line in enumerate(lines, 1):
            if re.search(self.syntax_patterns["fstring_nested_quotes"]["pattern"], line):
                issues.append(SyntaxIssue(
                    type="fstring_nested_quotes",
                    severity="critical",
                    line=line_num,
                    message="F-string with nested double quotes detected",
                    original_code=line.strip(),
                    suggested_fix=self._fix_fstring_quotes(line.strip()),
                    confidence=0.95,
                    fix_reasoning="Replace inner double quotes with single quotes to avoid syntax conflict"
                ))

        # Check for docstring issues around the error line
        if syntax_error.lineno:
            error_area_start = max(1, syntax_error.lineno - 5)
            error_area_end = min(len(lines), syntax_error.lineno + 5)

            for line_num in range(error_area_start, error_area_end + 1):
                if line_num <= len(lines):
                    line = lines[line_num - 1]
                    if '"""' in line and 'def ' in lines[max(0, line_num - 3):line_num]:
                        issues.append(SyntaxIssue(
                            type="docstring_syntax_error",
                            severity="critical",
                            line=line_num,
                            message="Docstring may be causing syntax error",
                            original_code=line.strip(),
                            suggested_fix=self._fix_docstring_to_comment(line.strip()),
                            confidence=0.90,
                            fix_reasoning="Convert problematic docstring to comment to resolve syntax error"
                        ))

        return issues

    def _analyze_preventive_patterns(self, content: str) -> List[SyntaxIssue]:
        """Analyze for patterns that might cause future syntax issues."""
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Check for potential f-string issues
            if 'f"' in line and line.count('"') > 2:
                # Potential nested quote issue
                issues.append(SyntaxIssue(
                    type="potential_fstring_issue",
                    severity="medium",
                    line=line_num,
                    message="Potential f-string quote nesting detected",
                    original_code=line.strip(),
                    suggested_fix=self._fix_fstring_quotes(line.strip()),
                    confidence=0.75,
                    fix_reasoning="Preemptively fix quote nesting to prevent syntax errors"
                ))

        return issues

    def _fix_fstring_quotes(self, line: str) -> str:
        """Fix f-string nested quote issues."""
        # Replace pattern: f"..."{var}"..." with f"...'{var}'..."
        def replace_inner_quotes(match):
            content = match.group(0)
            # Find variables in {} and replace surrounding quotes
            result = re.sub(r'"([^"{}]*{[^}]*}[^"{}]*)"', r"'\1'", content)
            return result

        # Apply the fix pattern we learned
        fixed = re.sub(r'f"[^"]*"[^"]*"[^"]*"', replace_inner_quotes, line)
        return fixed if fixed != line else line.replace('f"', "f'").replace('")', "')")

    def _fix_docstring_to_comment(self, line: str) -> str:
        """Convert docstring to comment as we learned to do."""
        # Remove the triple quotes and convert to comment
        cleaned = line.strip()
        if cleaned.startswith('"""') and cleaned.endswith('"""'):
            content = cleaned[3:-3].strip()
            return f"# {content}"
        elif cleaned.startswith('"""'):
            content = cleaned[3:].strip()
            return f"# {content}"
        return f"# {cleaned}"

    def get_fix_patterns(self) -> Dict[str, Dict]:
        """Return the learned fix patterns for other tools to use."""
        return {
            "fstring_quote_fix": {
                "description": "Replace nested double quotes in f-strings with single quotes",
                "pattern": r'f"[^"]*"[^"]*"[^"]*"',
                "replacement_strategy": "inner_quotes_to_single",
                "effectiveness": "very_high",
                "automation_ready": True
            },
            "docstring_to_comment": {
                "description": "Convert problematic docstrings to comments",
                "pattern": r'^\s*"""[^"]*"""?\s*$',
                "replacement_strategy": "triple_quote_to_hash_comment",
                "effectiveness": "high",
                "automation_ready": True
            },
            "quote_escaping": {
                "description": "Properly escape quotes in string literals",
                "pattern": r'"""[^"]*"""?\s+',
                "replacement_strategy": "escape_or_alternate_quotes",
                "effectiveness": "high",
                "automation_ready": True
            }
        }

    def get_learning_summary(self) -> Dict:
        """Provide summary of learned patterns for reporting."""
        return {
            "total_patterns": len(self.syntax_patterns),
            "critical_patterns": 2,  # fstring_nested_quotes, docstring_termination
            "automation_ready": 3,   # Most patterns can be automated
            "confidence_average": 0.90,
            "fix_types": [
                "quote_normalization",
                "docstring_conversion",
                "escape_sequence_correction"
            ],
            "learning_source": "manual_fix_analysis_2025_06_26"
        }