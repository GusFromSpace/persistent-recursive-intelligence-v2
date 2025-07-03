"""
Context-aware analysis for adjusting issue severity based on file location and purpose.

This module implements the key insight from debugging: print statements are acceptable
in test/demo files but critical in production code.
"""

import re
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional
from enum import Enum


class FileContext(Enum):
    """Categories of file contexts with different issue severity rules."""
    PRODUCTION = "production"
    TEST = "test"
    DEMO = "demo"
    CONFIG = "config"
    DOCUMENTATION = "documentation"
    SCRIPT = "script"
    BUILD = "build"
    UNKNOWN = "unknown"


class SeverityAdjustment(NamedTuple):
    """Represents how to adjust issue severity based on context."""
    pattern: str
    original_severity: str
    new_severity: str
    reason: str


class ContextAnalyzer:
    """
    Analyzes file context to provide intelligent severity adjustments.

    Key insight: Same code patterns have different severity depending on
    where they appear in the codebase.
    """

    def __init__(self):
        # Define context rules based on real debugging experience
        self.context_rules = {
            FileContext.PRODUCTION: {
                "print_statements": "high",
                "debug_code": "critical",
                "hardcoded_credentials": "critical",
                "hardcoded_paths": "high",
                "bare_except": "high",
                "todo_comments": "medium"
            },
            FileContext.TEST: {
                "print_statements": "low",
                "debug_code": "low",
                "hardcoded_credentials": "low",  # Test credentials are often fake
                "hardcoded_paths": "medium",
                "bare_except": "medium",
                "todo_comments": "low"
            },
            FileContext.DEMO: {
                "print_statements": "acceptable",
                "debug_code": "acceptable",
                "hardcoded_credentials": "low",  # Demo credentials
                "hardcoded_paths": "low",
                "bare_except": "low",
                "todo_comments": "acceptable"
            },
            FileContext.CONFIG: {
                "print_statements": "medium",
                "debug_code": "medium",
                "hardcoded_credentials": "critical",
                "hardcoded_paths": "critical",
                "bare_except": "high",
                "todo_comments": "medium"
            },
            FileContext.SCRIPT: {
                "print_statements": "low",
                "debug_code": "low",
                "hardcoded_credentials": "high",
                "hardcoded_paths": "medium",
                "bare_except": "medium",
                "todo_comments": "low"
            },
            FileContext.BUILD: {
                "print_statements": "acceptable",
                "debug_code": "acceptable",
                "hardcoded_credentials": "medium",
                "hardcoded_paths": "low",
                "bare_except": "low",
                "todo_comments": "acceptable"
            }
        }

        # Patterns for detecting different issue types
        self.issue_patterns = {
            "print_statements": [
                r'\bprint\s*\(',
                r"\bpprint\s*\(",
                r"console\.print\s*\("
            ],
            "legitimate_logging": [
                r'logging\.(info|debug|warning|error|critical)',
                r'logger\.(info|debug|warning|error|critical)',
                r'log\.(info|debug|warning|error|critical)',
                r'print\s*\(\s*f?"[^"]*{[^}]*}[^"]*"',  # f-string prints (often legitimate output)
                r'print\s*\(\s*"[A-Z🌀🎯📊🧠🚀✅❌⚠️📚📋🔍🛡️🎊🦾🔧🔄💾📁🎯][^"]*"'  # Emoji/status prints
            ],
            "debug_code": [
                r"\bdebugger\b",
                r"\bbreakpoint\s*\(",
                r"import\s+pdb",
                r"pdb\.set_trace\s*\(",
                # IMPROVED: r"#\s*DEBUG",
                r"#\s*FIXME",
                # IMPROVED: r"#\s*HACK"
            ],
            "hardcoded_credentials": [
                r"password\s*=\s*[\"'][^\"']+[\"']",
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']'
            ],
            "hardcoded_paths": [
                r'["\']\/home\/[^"\']+["\']',
                r'["\']C:\\[^"\']+["\']',
                r'["\']\/Users\/[^"\']+["\']'
            ],
            "bare_except": [
                r'except\s*:'
            ],
            "todo_comments": [
                r"#\s*TODO",
                r"#\s*FIXME",
                # IMPROVED: r"#\s*XXX"
            ]
        }

    def get_file_context(self, file_path: str) -> FileContext:
        """Determine the context category for a file."""
        path = Path(file_path)
        path_str = str(path).lower()

        # Test files
        if any(pattern in path_str for pattern in [
            "/test", "/tests", "_test.py", "test_", "/spec/", "_spec.py"
        ]):
            return FileContext.TEST

        # Demo/example files
        if any(pattern in path_str for pattern in [
            "/demo", "/demos", "/example", "/examples", "demo_", "example_",
            "tutorial", "sample", "/docs/", "readme"
        ]):
            return FileContext.DEMO

        # Configuration files
        if any(pattern in path_str for pattern in [
            "config", "settings", ".env", "setup.py", "pyproject.toml",
            "requirements", "dockerfile", "makefile"
        ]):
            return FileContext.CONFIG

        # Build/deployment scripts
        if any(pattern in path_str for pattern in [
            "/scripts/", "/bin/", "/deploy/", "build.py", "install.py",
            ".github/", "ci.py", "deploy.py"
        ]):
            return FileContext.BUILD

        # Standalone scripts
        if path.parent.name in ["scripts", "bin", "tools"] or path_str.endswith("_script.py"):
            return FileContext.SCRIPT

        # Documentation
        if any(pattern in path_str for pattern in [
            ".md", ".rst", "/docs/", "documentation"
        ]):
            return FileContext.DOCUMENTATION

        if any(pattern in path_str for pattern in [
            "/src/", "/lib/", "main.py", "__init__.py"
        ]) and not any(test_pattern in path_str for test_pattern in [
            "test", "demo", "example"
        ]):
            return FileContext.PRODUCTION

        return FileContext.UNKNOWN

    def adjust_severity(self, issue_type: str, original_severity: str,
                       file_context: FileContext) -> SeverityAdjustment:
        """Adjust issue severity based on file context."""

        # Get context rules for this file type
        context_rules = self.context_rules.get(file_context, {})
        new_severity = context_rules.get(issue_type, original_severity)

        if new_severity == "acceptable":
            new_severity = "info"

        reason = self._get_adjustment_reason(issue_type, file_context, original_severity, new_severity)

        return SeverityAdjustment(
            pattern=issue_type,
            original_severity=original_severity,
            new_severity=new_severity,
            reason=reason
        )

    def _get_adjustment_reason(self, issue_type: str, context: FileContext,
                             original: str, new: str) -> str:
        """Generate human-readable reason for severity adjustment."""

        if original == new:
            return f"No adjustment needed for {issue_type} in {context.value} files"

        if new == "info":
            return f"{issue_type} acceptable in {context.value} files"

        if new > original:  # Severity increased
            return f"{issue_type} more critical in {context.value} files"
        else:  # Severity decreased
            return f"{issue_type} less critical in {context.value} files"

    def analyze_content_for_patterns(self, content: str) -> Dict[str, List[int]]:
        """Find pattern matches in file content."""
        matches = {}

        for pattern_type, regexes in self.issue_patterns.items():
            matches[pattern_type] = []

            for regex in regexes:
                for match in re.finditer(regex, content, re.IGNORECASE | re.MULTILINE):
                    line_num = content[:match.start()].count("\n") + 1
                    matches[pattern_type].append(line_num)

        return matches

    def is_legitimate_print(self, line_content: str) -> bool:
        """Check if a print statement is legitimate logging rather than debug code."""
        line = line_content.strip()

        # Check for legitimate logging patterns
        for regex in self.issue_patterns["legitimate_logging"]:
            if re.search(regex, line, re.IGNORECASE):
                return True

        # Check for user interface outputs
        ui_indicators = [
            "input(", "Enter", "Choose", "Select", "Menu",
            "Success", "Complete", "Error:", "Warning:", "Info:",
            "Progress", "Status", "Loading", "Saving"
        ]

        if any(indicator in line for indicator in ui_indicators):
            return True

        if re.search(r'print\s*\(\s*f?["\'][^"\']*:\s*{[^}]*}', line):
            return True

        return False

    def get_context_summary(self, file_path: str) -> Dict[str, str]:
        """Get a summary of file context and applicable rules."""
        context = self.get_file_context(file_path)
        rules = self.context_rules.get(context, {})

        return {
            "file_path": file_path,
            "context": context.value,
            "rules": rules,
            "description": self._get_context_description(context)
        }

    def _get_context_description(self, context: FileContext) -> str:
        """Get human-readable description of file context."""
        descriptions = {
            FileContext.PRODUCTION: "Core application code - highest standards apply",
            FileContext.TEST: "Test code - debugging patterns acceptable",
            FileContext.DEMO: "Demo/example code - educational patterns acceptable",
            FileContext.CONFIG: "Configuration - security critical",
            FileContext.SCRIPT: "Utility script - moderate standards",
            FileContext.BUILD: "Build/deployment - automation patterns acceptable",
            FileContext.DOCUMENTATION: "Documentation - formatting focused",
            FileContext.UNKNOWN: "Unknown context - default standards apply"
        }
        return descriptions.get(context, "Unknown context")

    def validate_context_rules(self) -> List[str]:
        """Validate that context rules are properly defined."""
        issues = []

        # Check that all contexts have rules
        for context in FileContext:
            if context not in self.context_rules:
                issues.append(f"Missing rules for context: {context.value}")

        # Check that all issue types are covered
        all_issue_types = set(self.issue_patterns.keys())
        for context, rules in self.context_rules.items():
            missing_types = all_issue_types - set(rules.keys())
            if missing_types:
                issues.append(f"Context {context.value} missing rules for: {missing_types}")

        return issues