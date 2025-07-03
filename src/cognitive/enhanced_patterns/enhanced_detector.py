"""
Enhanced pattern detector that integrates all specialized detectors.

This is the main interface for the enhanced pattern detection system,
combining dependency validation, context analysis, interactive detection,
and other specialized analyzers.
"""

from typing import List, Dict, Any, NamedTuple
from pathlib import Path
import logging

from .dependency_validator import DependencyValidator, DependencyIssue
from .context_analyzer import ContextAnalyzer, FileContext
from .interactive_detector import InteractiveDetector, InteractiveIssue
from .syntax_pattern_detector import SyntaxPatternDetector, SyntaxIssue
from .dead_code_detector import detect_dead_code_in_file

logger = logging.getLogger(__name__)


class EnhancedIssue(NamedTuple):
    """Unified issue representation from enhanced pattern detection."""
    type: str
    category: str  # "dependency", "interactive", "context", etc.
    severity: str
    original_severity: str
    line: int
    message: str
    file_path: str
    context: str
    suggestion: str
    confidence: float


class EnhancedPatternDetector:
    """
    Main enhanced pattern detector that coordinates all specialized analyzers.

    This class provides the unified interface for the enhanced detection system,
    integrating context-aware analysis with specialized pattern detectors.
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.dependency_validator = DependencyValidator(str(project_path))
        self.context_analyzer = ContextAnalyzer()
        self.interactive_detector = InteractiveDetector()
        self.syntax_detector = SyntaxPatternDetector()

        # Issue category mapping for better organization
        self.category_mapping = {
            "missing_dependency": "dependency",
            "unused_dependency": "dependency",
            "circular_import_risk": "dependency",
            "unhandled_eof": "interactive",
            "infinite_loop_risk": "interactive",
            "input_loop_without_eof": "interactive",
            "missing_keyboard_interrupt": "interactive",
            "subprocess_without_cleanup": "interactive",
            "print_statements": "context",
            "debug_code": "context",
            "hardcoded_credentials": "context",
            "hardcoded_paths": "context",
            "bare_except": "context"
        }

    def analyze_file(self, file_path: str, content: str) -> List[EnhancedIssue]:
        """
        Perform comprehensive enhanced analysis on a single file.

        Args:
            file_path: Path to the file being analyzed
            content: File content as string

        Returns:
            List of enhanced issues with context-adjusted severity
        """
        all_issues = []

        try:
            # Get file context for severity adjustments
            file_context = self.context_analyzer.get_file_context(file_path)

            # Run specialized detectors
            dependency_issues = self._analyze_dependencies(file_path, content)
            interactive_issues = self._analyze_interactive(file_path, content)
            context_issues = self._analyze_context_patterns(file_path, content, file_context)
            syntax_issues = self._analyze_syntax_patterns(file_path, content)
            dead_code_analysis = self._analyze_dead_code(file_path, content)

            # Convert and adjust all issues
            all_issues.extend(self._convert_dependency_issues(dependency_issues, file_path, file_context))
            all_issues.extend(self._convert_interactive_issues(interactive_issues, file_path, file_context))
            all_issues.extend(context_issues)
            all_issues.extend(self._convert_syntax_issues(syntax_issues, file_path, file_context))
            all_issues.extend(self._convert_dead_code_issues(dead_code_analysis, file_path, file_context))

            logger.debug(f"Enhanced analysis found {len(all_issues)} issues in {file_path}")

        except Exception as e:
            logger.error(f"Error in enhanced analysis of {file_path}: {e}")

        return all_issues

    def _analyze_dependencies(self, file_path: str, content: str) -> List[DependencyIssue]:
        """Analyze file for dependency-related issues."""
        try:
            return self.dependency_validator.validate_file(file_path, content)
        except Exception as e:
            logger.debug(f"Dependency analysis failed for {file_path}: {e}")
            return []

    def _analyze_interactive(self, file_path: str, content: str) -> List[InteractiveIssue]:
        """Analyze file for interactive interface issues."""
        try:
            return self.interactive_detector.analyze_file(file_path, content)
        except Exception as e:
            logger.debug(f"Interactive analysis failed for {file_path}: {e}")
            return []

    def _analyze_syntax_patterns(self, file_path: str, content: str) -> List[SyntaxIssue]:
        """Analyze file for syntax patterns learned from manual fixes."""
        try:
            return self.syntax_detector.analyze_file(file_path, content)
        except Exception as e:
            logger.debug(f"Syntax pattern analysis failed for {file_path}: {e}")
            return []

    def _analyze_dead_code(self, file_path: str, content: str) -> Dict:
        """Analyze file for dead code patterns."""
        try:
            return detect_dead_code_in_file(file_path)
        except Exception as e:
            logger.debug(f"Dead code analysis failed for {file_path}: {e}")
            return {}

    def _analyze_context_patterns(self, file_path: str, content: str,
                                 file_context: FileContext) -> List[EnhancedIssue]:
        """Analyze file content for context-aware patterns."""
        issues = []

        try:
            pattern_matches = self.context_analyzer.analyze_content_for_patterns(content)

            for pattern_type, line_numbers in pattern_matches.items():
                for line_num in line_numbers:
                    original_severity = self._get_base_severity(pattern_type)

                    # Adjust severity based on context
                    adjustment = self.context_analyzer.adjust_severity(
                        pattern_type, original_severity, file_context
                    )

                    # Only create issue if severity is meaningful
                    if adjustment.new_severity not in ["info", "acceptable"]:
                        issues.append(EnhancedIssue(
                            type=pattern_type,
                            category="context",
                            severity=adjustment.new_severity,
                            original_severity=original_severity,
                            line=line_num,
                            message=self._get_pattern_message(pattern_type, line_num),
                            file_path=file_path,
                            context=file_context.value,
                            suggestion=self._get_pattern_suggestion(pattern_type, file_context),
                            confidence=0.8
                        ))

        except Exception as e:
            logger.debug(f"Context pattern analysis failed for {file_path}: {e}")

        return issues

    def _convert_dependency_issues(self, dep_issues: List[DependencyIssue],
                                  file_path: str, context: FileContext) -> List[EnhancedIssue]:
        """Convert dependency issues to enhanced issues."""
        enhanced = []

        for issue in dep_issues:
            # Adjust severity based on context if needed
            adjusted_severity = issue.severity
            if issue.type == "missing_dependency" and context == FileContext.TEST:
                adjusted_severity = "medium"  # Less critical in tests

            enhanced.append(EnhancedIssue(
                type=issue.type,
                category="dependency",
                severity=adjusted_severity,
                original_severity=issue.severity,
                line=issue.line,
                message=issue.message,
                file_path=file_path,
                context=context.value,
                suggestion=issue.suggestion or "See dependency documentation",
                confidence=0.9
            ))

        return enhanced

    def _convert_interactive_issues(self, int_issues: List[InteractiveIssue],
                                   file_path: str, context: FileContext) -> List[EnhancedIssue]:
        """Convert interactive issues to enhanced issues."""
        enhanced = []

        for issue in int_issues:
            enhanced.append(EnhancedIssue(
                type=issue.type,
                category="interactive",
                severity=issue.severity,
                original_severity=issue.severity,
                line=issue.line,
                message=issue.message,
                file_path=file_path,
                context=context.value,
                suggestion=issue.suggestion or "Improve interactive handling",
                confidence=0.7
            ))

        return enhanced

    def _convert_syntax_issues(self, syntax_issues: List[SyntaxIssue],
                              file_path: str, context: FileContext) -> List[EnhancedIssue]:
        """Convert syntax issues to enhanced issues."""
        enhanced = []

        for issue in syntax_issues:
            enhanced.append(EnhancedIssue(
                type=issue.type,
                category="syntax",
                severity=issue.severity,
                original_severity=issue.severity,
                line=issue.line,
                message=f"{issue.message}: {issue.original_code}",
                file_path=file_path,
                context=context.value,
                suggestion=f"Fix: {issue.suggested_fix} - {issue.fix_reasoning}",
                confidence=issue.confidence
            ))

        return enhanced

    def _convert_dead_code_issues(self, dead_code_analysis: Dict,
                                 file_path: str, context: FileContext) -> List[EnhancedIssue]:
        """Convert dead code analysis to enhanced issues."""
        enhanced = []

        if not dead_code_analysis:
            return enhanced

        # Convert unused imports
        for unused_import in dead_code_analysis.get('dead_imports', []):
            enhanced.append(EnhancedIssue(
                type="dead_code_import",
                category="dead_code",
                severity="low",
                original_severity="low",
                line=1,  # Would need line tracking in dead code detector
                message=f"Unused import: {unused_import}",
                file_path=file_path,
                context=context.value,
                suggestion=f"Remove unused import '{unused_import}'",
                confidence=0.8
            ))

        # Convert unused functions
        for unused_function in dead_code_analysis.get('dead_functions', []):
            enhanced.append(EnhancedIssue(
                type="dead_code_function",
                category="dead_code",
                severity="medium",
                original_severity="medium",
                line=1,  # Would need line tracking in dead code detector
                message=f"Unused function: {unused_function}",
                file_path=file_path,
                context=context.value,
                suggestion=f"Remove unused function '{unused_function}' or make it private",
                confidence=0.7
            ))

        # Convert unused classes
        for unused_class in dead_code_analysis.get('dead_classes', []):
            enhanced.append(EnhancedIssue(
                type="dead_code_class",
                category="dead_code",
                severity="medium",
                original_severity="medium",
                line=1,  # Would need line tracking in dead code detector
                message=f"Unused class: {unused_class}",
                file_path=file_path,
                context=context.value,
                suggestion=f"Remove unused class '{unused_class}' or export it",
                confidence=0.7
            ))

        return enhanced

    def _get_base_severity(self, pattern_type: str) -> str:
        """Get base severity for a pattern type."""
        base_severities = {
            "print_statements": "medium",
            "debug_code": "medium",
            "hardcoded_credentials": "critical",
            "hardcoded_paths": "medium",
            "bare_except": "high",
            "todo_comments": "low"
        }
        return base_severities.get(pattern_type, "medium")

    def _get_pattern_message(self, pattern_type: str, line_num: int) -> str:
        """Get descriptive message for pattern type."""
        messages = {
            "print_statements": f"Print statement found at line {line_num}",
            "debug_code": f"Debug code found at line {line_num}",
            "hardcoded_credentials": f"Potential hardcoded credential at line {line_num}",
            "hardcoded_paths": f"Hardcoded file path at line {line_num}",
            "bare_except": f"Bare except clause at line {line_num}",
            "todo_comments": f"TODO comment at line {line_num}"
        }
        return messages.get(pattern_type, f"Pattern {pattern_type} at line {line_num}")

    def _get_pattern_suggestion(self, pattern_type: str, context: FileContext) -> str:
        """Get contextual suggestion for pattern type."""
        suggestions = {
            "print_statements": "Replace with proper logging" if context == FileContext.PRODUCTION
                               else "Consider using logging for consistency",
            "debug_code": "Remove debug code before production" if context == FileContext.PRODUCTION
                         else "Ensure debug code is cleaned up",
            "hardcoded_credentials": "Use environment variables or secure credential storage",
            "hardcoded_paths": "Use pathlib or environment variables for paths",
            "bare_except": "Use specific exception types for better error handling",
            "todo_comments": "Address TODO items before release" if context == FileContext.PRODUCTION
                            else "Track TODO items for future improvements"
        }
        return suggestions.get(pattern_type, "Review and improve this pattern")

    def get_project_summary(self) -> Dict[str, Any]:
        """Get summary of enhanced analysis capabilities for this project."""
        try:
            # Get dependency summary
            unused_deps = self.dependency_validator.find_unused_dependencies()

            # Get context validation
            context_validation = self.context_analyzer.validate_context_rules()

            return {
                "project_path": str(self.project_path),
                "analyzers": {
                    "dependency_validator": "enabled",
                    "context_analyzer": "enabled",
                    "interactive_detector": "enabled"
                },
                "unused_dependencies": len(unused_deps),
                "context_validation_issues": len(context_validation),
                "supported_patterns": list(self.category_mapping.keys()),
                "file_contexts": [ctx.value for ctx in FileContext]
            }

        except Exception as e:
            logger.error(f"Error generating project summary: {e}")
            return {"error": str(e)}

    def validate_enhanced_patterns(self) -> List[str]:
        """Validate that enhanced pattern detection is working correctly."""
        issues = []

        try:
            # Validate context analyzer
            context_issues = self.context_analyzer.validate_context_rules()
            issues.extend(context_issues)

            # Validate dependency analyzer
            if not self.project_path.exists():
                issues.append(f"Project path does not exist: {self.project_path}")

            # Test basic functionality
            test_content = """
import os
logger.info("Hello world")
while True:
    user_input = input("Enter command: ")
"""
            test_issues = self.analyze_file("test.py", test_content)
            if not test_issues:
                issues.append("Enhanced pattern detection not finding expected test patterns")

            logger.info(f"Enhanced pattern validation found {len(issues)} configuration issues")

        except Exception as e:
            issues.append(f"Validation error: {e}")

        return issues