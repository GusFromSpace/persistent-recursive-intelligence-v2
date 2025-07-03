"""
Interactive mode and CLI interface issue detection.

This module detects issues that commonly occur in interactive applications,
based on the infinite loop issue found in Claude Wrapper"s interactive mode.
"""

import ast
import logging
from typing import List, NamedTuple, Optional

logger = logging.getLogger(__name__)


class InteractiveIssue(NamedTuple):
    """Represents an interactive interface issue."""
    type: str
    severity: str
    line: int
    message: str
    suggestion: Optional[str] = None


class InteractiveDetector:
    """
    Detects issues common in interactive CLI applications.

    Based on real-world issues found during Claude Wrapper debugging:
    - EOF handling missing from input() calls
    - Infinite loops without proper exit conditions
    - Missing signal handling
    - Resource cleanup in long-running processes
    """

    def __init__(self):
        self.input_functions = {
            "input", "raw_input", "sys.stdin.readline",
            "sys.stdin.read", "click.prompt"
        }

        self.loop_keywords = {
            "while", "for"
        }

    def analyze_file(self, file_path: str, content: str) -> List[InteractiveIssue]:
        """Analyze a file for interactive interface issues."""
        issues = []

        try:
            tree = ast.parse(content)

            # Check for input handling issues
            issues.extend(self._check_input_handling(tree, content))

            # Check for infinite loop risks
            issues.extend(self._check_infinite_loops(tree, content))

            # Check for signal handling
            issues.extend(self._check_signal_handling(tree, content))

            # Check for resource cleanup
            issues.extend(self._check_resource_cleanup(tree, content))

        except SyntaxError as e:
            logger.debug(f"Syntax error in {file_path}: {e}")

        return issues

    def _check_input_handling(self, tree: ast.AST, content: str) -> List[InteractiveIssue]:
        """Check for input() calls without proper EOF handling."""
        issues = []

        # Find all input() calls
        input_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.input_functions:
                    input_calls.append(node)
                elif isinstance(node.func, ast.Attribute):
                    full_name = self._get_full_attr_name(node.func)
                    if full_name in self.input_functions:
                        input_calls.append(node)

        # Check if input calls are in try/except blocks that handle EOF
        for call in input_calls:
            if not self._is_in_eof_handler(call, tree):
                issues.append(InteractiveIssue(
                    type="unhandled_eof",
                    severity="medium",
                    line=call.lineno,
                    message="input() call without EOF exception handling",
                    suggestion="Wrap in try/except to handle EOFError and KeyboardInterrupt"
                ))

        return issues

    def _check_infinite_loops(self, tree: ast.AST, content: str) -> List[InteractiveIssue]:
        """Check for potential infinite loops in interactive code."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                # Check for while True without break conditions
                if self._is_while_true(node) and not self._has_proper_exit(node):
                    issues.append(InteractiveIssue(
                        type="infinite_loop_risk",
                        severity="medium",
                        line=node.lineno,
                        message="while True loop without clear exit conditions",
                        suggestion="Ensure loop has proper break conditions or exception handling"
                    ))

                # Check for input in while loop without EOF handling
                if self._has_input_in_loop(node) and not self._loop_handles_eof(node):
                    issues.append(InteractiveIssue(
                        type="input_loop_without_eof",
                        severity="high",
                        line=node.lineno,
                        message="Input in loop without EOF handling - can cause infinite error loop",
                        suggestion="Add try/except around input() to handle EOF and break loop"
                    ))

        return issues

    def _check_signal_handling(self, tree: ast.AST, content: str) -> List[InteractiveIssue]:
        """Check for missing signal handling in interactive applications."""
        has_signal_handler = False
        has_keyboard_interrupt = False

        for node in ast.walk(tree):
            # Check for signal module import
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "signal":
                        signal_imports.append(node.lineno)

            # Check for signal handlers
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and
                        node.func.value.id == "signal" and
                        node.func.attr == "signal"):
                        has_signal_handler = True

            # Check for KeyboardInterrupt handling
            if isinstance(node, ast.ExceptHandler):
                if node.type and isinstance(node.type, ast.Name):
                    if node.type.id == "KeyboardInterrupt":
                        has_keyboard_interrupt = True

        issues = []

        if self._appears_interactive(tree):
            if not has_keyboard_interrupt:
                issues.append(InteractiveIssue(
                    type="missing_keyboard_interrupt",
                    severity="medium",
                    line=1,
                    message="Interactive application without KeyboardInterrupt handling",
                    suggestion="Add try/except KeyboardInterrupt for graceful exit"
                ))

            if not has_signal_handler and self._has_long_running_loop(tree):
                issues.append(InteractiveIssue(
                    type="missing_signal_handler",
                    severity="low",
                    line=1,
                    message="Long-running application without signal handlers",
                    suggestion="Consider adding signal handlers for SIGTERM/SIGINT"
                ))

        return issues

    def _check_resource_cleanup(self, tree: ast.AST, content: str) -> List[InteractiveIssue]:
        """Check for resource cleanup in interactive applications."""
        issues = []

        # Look for subprocess creation without cleanup
        subprocess_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    full_name = self._get_full_attr_name(node.func)
                    if "subprocess." in full_name and "Popen" in full_name:
                        subprocess_calls.append(node)

        for call in subprocess_calls:
            if not self._has_process_cleanup(call, tree):
                issues.append(InteractiveIssue(
                    type="subprocess_without_cleanup",
                    severity="medium",
                    line=call.lineno,
                    message="Subprocess creation without cleanup handling",
                    suggestion="Ensure subprocess is properly terminated and waited for"
                ))

        return issues

    def _is_in_eof_handler(self, call_node: ast.AST, tree: ast.AST) -> bool:
        """Check if a call is inside a try/except that handles EOF."""
        # Find the try/except block containing this call
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                # Check if call is in this try block
                if self._node_contains(node, call_node):
                    # Check if any except handler catches EOF
                    for handler in node.handlers:
                        if handler.type:
                            if isinstance(handler.type, ast.Name):
                                if handler.type.id in ["EOFError", "KeyboardInterrupt"]:
                                    return True
                            elif isinstance(handler.type, ast.Tuple):
                                for elt in handler.type.elts:
                                    if isinstance(elt, ast.Name):
                                        if elt.id in ["EOFError", "KeyboardInterrupt"]:
                                            return True
        return False

    def _is_while_true(self, while_node: ast.While) -> bool:
        """Check if this is a "while True' loop."""
        return (isinstance(while_node.test, ast.Constant) and
                while_node.test.value is True) or \
               (isinstance(while_node.test, ast.NameConstant) and
                while_node.test.value is True) or \
               (isinstance(while_node.test, ast.Name) and
                while_node.test.id == "True")

    def _has_proper_exit(self, while_node: ast.While) -> bool:
        """Check if while loop has proper exit conditions."""
        # Look for break statements
        for node in ast.walk(while_node):
            if isinstance(node, ast.Break):
                return True
            # Look for return statements
            if isinstance(node, ast.Return):
                return True
            # Look for sys.exit or quit
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    full_name = self._get_full_attr_name(node.func)
                    if "sys.exit" in full_name or "quit" in full_name:
                        return True
        return False

    def _has_input_in_loop(self, loop_node: ast.AST) -> bool:
        """Check if loop contains input() calls."""
        for node in ast.walk(loop_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.input_functions:
                    return True
        return False

    def _loop_handles_eof(self, loop_node: ast.AST) -> bool:
        """Check if loop properly handles EOF exceptions."""
        for node in ast.walk(loop_node):
            if isinstance(node, ast.ExceptHandler):
                if node.type and isinstance(node.type, ast.Name):
                    if node.type.id in ["EOFError", "KeyboardInterrupt"]:
                        return True
        return False

    def _appears_interactive(self, tree: ast.AST) -> bool:
        """Heuristic to determine if this appears to be an interactive application."""
        has_input = False
        has_loop = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.input_functions:
                    has_input = True
            if isinstance(node, (ast.While, ast.For)):
                has_loop = True

        return has_input and has_loop

    def _has_long_running_loop(self, tree: ast.AST) -> bool:
        """Check if there are loops that appear to run indefinitely."""
        for node in ast.walk(tree):
            if isinstance(node, ast.While):
                if self._is_while_true(node):
                    return True
        return False

    def _has_process_cleanup(self, call_node: ast.AST, tree: ast.AST) -> bool:
        """Check if subprocess has proper cleanup."""
        # This is a simplified check - in practice would need more sophisticated analysis
        # Look for .wait(), .terminate(), .kill() calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ["wait", "terminate", "kill", "communicate"]:
                        return True
        return False

    def _node_contains(self, parent: ast.AST, child: ast.AST) -> bool:
        """Check if parent node contains child node."""
        for node in ast.walk(parent):
            if node is child:
                return True
        return False

    def _get_full_attr_name(self, node: ast.Attribute) -> str:
        """Get the full dotted name of an attribute."""
        parts = [node.attr]
        current = node.value

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)

        return ".".join(reversed(parts))