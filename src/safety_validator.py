#!/usr/bin/env python3
"""
Safety Validator - Prevents destructive fixes and false positives

This module provides validation logic to prevent the AI diagnostic toolkit
from applying harmful fixes, especially when running on itself.
"""

import sys
import re
import ast
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

# Import emergency controls if available
try:
    from .safety.emergency_controls import emergency_controller
    EMERGENCY_CONTROLS_AVAILABLE = True
except ImportError:
    EMERGENCY_CONTROLS_AVAILABLE = False

@dataclass
class ValidationResult:
    is_valid: bool
    confidence_score: int  # 0-100
    reason: str
    suggestions: List[str] = None

class SafetyValidator:
    """Validates proposed fixes to prevent destructive changes"""

    # Known problematic patterns that the toolkit has been creating
    PROBLEMATIC_PATTERNS = [
        r'^(\w+)_result = (.+)$',  # Generic _result assignments
        r"^(\w+)_result = (\w+\.\w+\(.*\))$",  # Method call assignments
        r"^(\w+)_result = (\w+\(.*\))$",  # Function call assignments
    ]

    # Patterns that indicate self-modification
    SELF_MODIFICATION_INDICATORS = [
        "ai_diagnostic_toolkit",
        "BaseLanguageAnalyzer",
        "MultiLanguageDiagnosticOrchestrator",
        "SafetyValidator",
        "PluginManager"
    ]

    # Known good patterns that should not be "fixed"
    GOOD_PATTERNS = [
        r"^\s*\w+\.\w+\(.*\)$",  # Simple method calls
        r"^\s*\w+\(.*\)$",       # Simple function calls
        r"^\s*logger\.\w+\(.*\)$",  # Logger calls
        r"^\s*self\.\w+\(.*\)$",    # Self method calls
    ]

    def __init__(self):
        self.validation_history = []

    def is_self_modification(self, file_path: Path) -> bool:
        """Detect if we're modifying our own diagnostic toolkit"""
        try:
            content = file_path.read_text()
            return any(indicator in content for indicator in self.SELF_MODIFICATION_INDICATORS)
        except Exception:
            return False

    def is_destructive_pattern(self, proposed_fix: str) -> bool:
        """Check if the proposed fix matches known destructive patterns"""
        for pattern in self.DESTRUCTIVE_PATTERNS:
            if re.match(pattern, proposed_fix.strip()):
                return True
        return False

    def is_protected_pattern(self, original_code: str) -> bool:
        """Check if the original code matches patterns that should be protected"""
        for pattern in self.PROTECTED_PATTERNS:
            if re.match(pattern, original_code.strip()):
                return True
        return False

    def is_syntactically_valid_python(self, code: str) -> bool:
        """Check if Python code is syntactically valid"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def creates_unused_variable(self, code: str) -> bool:
        """Check if code creates an unused variable (like our _result pattern)"""
        # Simple heuristic: if line assigns to variable ending in _result
        # and the variable name appears only once, it's likely unused
        lines = code.strip().split("\n")
        for line in lines:
            match = re.match(r"^(\w+_result)\s*=", line.strip())
            if match:
                var_name = match.group(1)
                # If variable appears only in this assignment, it's unused
                if code.count(var_name) == 1:
                    return True
        return False

    def validate_fix(self, original_code: str, proposed_fix: str, file_path: Path = None) -> ValidationResult:
        """Comprehensive validation of a proposed fix"""

        # Check for self-modification
        if file_path and self.is_self_modification(file_path):
            return ValidationResult(
                is_valid=False,
                confidence_score=0,
                reason="Self-modification detected - requires manual review",
                suggestions=["Review change manually", "Test in isolated environment"]
            )

        # Check for destructive patterns
        if self.is_destructive_pattern(proposed_fix):
            return ValidationResult(
                is_valid=False,
                confidence_score=0,
                reason="Matches known destructive pattern",
                suggestions=["Avoid creating _result variables", "Use original function call"]
            )

        # Check if we're "fixing" something that shouldn't be fixed
        if self.is_protected_pattern(original_code):
            return ValidationResult(
                is_valid=False,
                confidence_score=10,
                reason="Original code matches protected pattern",
                suggestions=["Leave original code unchanged"]
            )

        # Check for unused variable creation
        if self.creates_unused_variable(proposed_fix):
            return ValidationResult(
                is_valid=False,
                confidence_score=20,
                reason="Creates unused variable",
                suggestions=["Remove variable assignment", "Use return value if needed"]
            )

        # Syntax validation
        if not self.is_syntactically_valid_python(proposed_fix):
            return ValidationResult(
                is_valid=False,
                confidence_score=0,
                reason="Proposed fix has syntax errors",
                suggestions=["Fix syntax errors", "Validate indentation"]
            )

        # If we get here, the fix seems reasonable
        confidence = self.calculate_confidence_score(original_code, proposed_fix)

        return ValidationResult(
            is_valid=confidence > 50,
            confidence_score=confidence,
            reason="Fix appears valid" if confidence > 50 else "Low confidence in fix value",
            suggestions=["Apply with caution"] if confidence < 80 else ["Safe to apply"]
        )

    def calculate_confidence_score(self, original: str, proposed: str) -> int:
        """Calculate confidence score for a proposed fix"""
        score = 50  # Start with neutral

        # Increase confidence for clear improvements
        if len(proposed.strip()) < len(original.strip()):
            score += 10  # Simpler is often better

        if "import" in proposed and "import" not in original:
            score += 15  # Adding needed imports

        if "TODO" in original and "TODO" not in proposed:
            score += 20  # Resolving TODOs

        # Decrease confidence for suspicious changes
        if "_result" in proposed and "_result" not in original:
            score -= 30  # Creating _result variables

        if proposed.count("=") > original.count("="):
            score -= 15  # Adding assignments

        if "logger" in original and "logger" not in proposed:
            score -= 20  # Removing logging

        return max(0, min(100, score))

    def get_validation_summary(self) -> dict:
        """Get summary of all validations performed"""
        return {
            "total_validations": len(self.validation_history),
            "passed": sum(1 for v in self.validation_history if v.is_valid),
            "failed": sum(1 for v in self.validation_history if not v.is_valid),
            "average_confidence": sum(v.confidence_score for v in self.validation_history) / len(self.validation_history) if self.validation_history else 0
        }

def main():
    """Test the safety validator"""
    validator = SafetyValidator()

    # Test cases based on actual destructive patterns we found
    test_cases = [
        ("plugin_manager.discover_plugins()", "plugin_manage_result = plugin_manager.discover_plugins()"),
        ("self.logger.info('test')", "sel_result = self.logger.info('test')"),
        ("sys.exit(1)", "sy_result = sys.exit(1)"),
        ("import logging", "import logging"),  # Should be valid
    ]

    logger.info("Safety Validator Test Results:")
    logger.info("=" * 50)

    for original, proposed in test_cases:
        result = validator.validate_fix(original, proposed)
        logger.info(f"\nOriginal: {original}")
        logger.info(f"Proposed: {proposed}")
        logger.info(f"Valid: {result.is_valid}")
        logger.info(f"Confidence: {result.confidence_score}")
        logger.info(f"Reason: {result.reason}")
        logger.info(f"Suggestions: {result.suggestions}")

if __name__ == "__main__":
    main()
