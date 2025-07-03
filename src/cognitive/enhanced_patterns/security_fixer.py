#!/usr/bin/env python3
"""
Security and Quality Fixer - Targets specific high-impact issues
Focuses on critical security vulnerabilities and high-priority quality issues.
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityQualityFixer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.fixes_applied = []

    def fix_broad_exceptions(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Fix overly broad exception handling patterns."""
        fixes = []
        lines = content.split('\n')
        modified = False

        for i, line in enumerate(lines):
            # Replace bare except Exception: with more specific patterns
            if "except Exception:" in line and "as e" not in line:
                indent = len(line) - len(line.lstrip())
                lines[i] = line.replace("except Exception as e:", "except Exception as e:")
                # Add logging if not present
                if i + 1 < len(lines) and "logger" not in lines[i + 1] and "logging" not in lines[i + 1]:
                    next_line = lines[i + 1]
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent > indent:  # Inside the except block
                        log_line = " " * (indent + 4) + f"logger.error(f'Unexpected error: {{e}}', exc_info=True)"
                        lines.insert(i + 1, log_line)
                fixes.append(f"Line {i+1}: Added error logging to broad exception handler")
                modified = True

        return "\n".join(lines) if modified else content, fixes

    def fix_print_statements(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Replace print statements with proper logging in production code."""
        fixes = []

        # Skip test files and scripts that legitimately use print
        if any(x in str(file_path).lower() for x in ["test_", "tests/", "scripts/", "demo", "example"]):
            return content, fixes

        lines = content.split("\n")
        modified = False
        needs_logger_import = False
        has_logger_import = "import logging" in content or "from logging import" in content

        for i, line in enumerate(lines):
            # Match print statements but not in comments
            if re.match(r"^\s*print\s*\(", line) and not line.strip().startswith("#"):
                indent = len(line) - len(line.lstrip())

                # Extract print content
                print_match = re.search(r"print\s*\((.*)\)", line)
                if print_match:
                    print_content = print_match.group(1)

                    # Convert to logger call
                    if "error" in print_content.lower() or "fail" in print_content.lower():
                        log_level = "error"
                    elif "warn" in print_content.lower():
                        log_level = "warning"
                    elif "debug" in print_content.lower():
                        log_level = "debug"
                    else:
                        log_level = "info"

                    new_line = " " * indent + f"logger.{log_level}({print_content})"
                    lines[i] = new_line
                    fixes.append(f"Line {i+1}: Converted print to logger.{log_level}")
                    modified = True
                    needs_logger_import = True

        # Add logger import if needed
        if modified and needs_logger_import and not has_logger_import:
            # Find a good place to add the import
            import_line = None
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    import_line = i
                elif line.strip() and import_line is not None:
                    break

            if import_line is not None:
                lines.insert(import_line + 1, "import logging")
                # Add logger initialization
                lines.insert(import_line + 2, "")
                lines.insert(import_line + 3, "logger = logging.getLogger(__name__)")
                fixes.append("Added logging import and logger initialization")

        return "\n".join(lines) if modified else content, fixes

    def fix_mutable_defaults(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Fix mutable default argument patterns."""
        fixes = []

        # Pattern to match function definitions with mutable defaults
        mutable_patterns = [
            (r"def\s+\w+\([^)]*=\s*\[\s*\]", "empty list"),
            (r"def\s+\w+\([^)]*=\s*\{\s*\}", "empty dict"),
            (r"def\s+\w+\([^)]*=\s*set\(\)", "empty set")
        ]

        lines = content.split("\n")
        modified = False

        for i, line in enumerate(lines):
            for pattern, desc in mutable_patterns:
                if re.search(pattern, line):
                    # This is a complex fix that requires AST parsing
                    # For now, just flag it
                    fixes.append(f"Line {i+1}: Found mutable default argument ({desc}) - manual fix needed")

        return content, fixes

    def remove_hardcoded_secrets(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Remove or flag hardcoded secrets."""
        fixes = []

        # Skip config files and examples
        if any(x in str(file_path).lower() for x in ["config.yml", ".example", "example", "demo"]):
            return content, fixes

        secret_patterns = [
            (r"API_KEY\s*=\s*['\"][^'\"]+['\"]", "hardcoded API key"),
            (r"API_SECRET\s*=\s*['\"][^'\"]+['\"]", "hardcoded API secret"),
            (r"PASSWORD\s*=\s*['\"][^'\"]+['\"]", "hardcoded password"),
            (r"TOKEN\s*=\s*['\"][^'\"]+['\"]", "hardcoded token")
        ]

        lines = content.split('\n')

        for i, line in enumerate(lines):
            for pattern, desc in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    fixes.append(f"Line {i+1}: Found {desc} - should use environment variables")

        return content, fixes

    def fix_file(self, file_path: Path) -> Dict[str, List[str]]:
        """Apply all fixes to a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            all_fixes = {}

            # Apply fixes in order
            content, fixes1 = self.fix_broad_exceptions(str(file_path), content)
            if fixes1:
                all_fixes["broad_exceptions"] = fixes1

            content, fixes2 = self.fix_print_statements(str(file_path), content)
            if fixes2:
                all_fixes["print_statements"] = fixes2

            content, fixes3 = self.fix_mutable_defaults(str(file_path), content)
            if fixes3:
                all_fixes["mutable_defaults"] = fixes3

            content, fixes4 = self.remove_hardcoded_secrets(str(file_path), content)
            if fixes4:
                all_fixes["hardcoded_secrets"] = fixes4

            # Write back if modified
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            return all_fixes

        except Exception as e:
            return {"error": [f"Failed to process file: {e}"]}

    def fix_project(self, dry_run: bool = True) -> Dict[str, Dict[str, List[str]]]:
        """Fix all Python files in the project."""
        results = {}

        for py_file in self.project_path.rglob("*.py"):
            # Skip virtual environments and .git
            if any(part in str(py_file) for part in ["venv", ".git", "__pycache__", ".env"]):
                continue

            if not dry_run:
                fixes = self.fix_file(py_file)
            else:
                # Dry run - just analyze
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    _, fixes1 = self.fix_broad_exceptions(str(py_file), content)
                    _, fixes2 = self.fix_print_statements(str(py_file), content)
                    _, fixes3 = self.fix_mutable_defaults(str(py_file), content)
                    _, fixes4 = self.remove_hardcoded_secrets(str(py_file), content)

                    fixes = {}
                    if fixes1: fixes["broad_exceptions"] = fixes1
                    if fixes2: fixes["print_statements"] = fixes2
                    if fixes3: fixes["mutable_defaults"] = fixes3
                    if fixes4: fixes["hardcoded_secrets"] = fixes4
                except Exception as e:
                    fixes = {"error": [f"Analysis failed: {e}"]}

            if fixes:
                results[str(py_file.relative_to(self.project_path))] = fixes

        return results

def main():
    import sys
    import json

    if len(sys.argv) < 2:
        logger.info("Usage: python security_fixer.py <project_path> [--apply]")
        sys.exit(1)

    project_path = sys.argv[1]
    apply_fixes = "--apply" in sys.argv

    fixer = SecurityQualityFixer(project_path)
    results = fixer.fix_project(dry_run=not apply_fixes)

    total_fixes = sum(len(fixes) for file_fixes in results.values() for fixes in file_fixes.values())
    mode = "APPLIED" if apply_fixes else "DRY RUN"

    logger.info(f"🔒 Security & Quality Fixer Results")
    logger.info(f"==================================")
    logger.info(f"🎯 Mode: {mode}")
    logger.info(f"📊 Total Fixes: {total_fixes}")
    logger.info(f"📁 Files Affected: {len(results)}")
    logger.info()

    for file_path, file_fixes in results.items():
        if file_fixes:
            logger.info(f"📄 {file_path}")
            for category, fixes in file_fixes.items():
                logger.info(f"   🔧 {category}: {len(fixes)} fixes")
                if len(fixes) <= 5:  # Show details for files with few fixes
                    for fix in fixes:
                        logger.info(f"      - {fix}")
                logger.info()

if __name__ == "__main__":
    main()