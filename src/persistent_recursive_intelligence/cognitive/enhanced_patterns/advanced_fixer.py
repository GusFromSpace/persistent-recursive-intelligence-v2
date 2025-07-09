#!/usr/bin/env python3
"""
Advanced Issue Fixer - Targets remaining high-impact issues
Focuses on issues that require more sophisticated analysis but can still be automated.
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Tuple


class AdvancedIssueFixer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.fixes_applied = []

    def fix_bare_except_blocks(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        # IMPROVED: """Fix bare except Exception as e: blocks that are unsafe."""
        fixes = []
        lines = content.split('\n')
        modified = False

        for i, line in enumerate(lines):
            # IMPROVED: # Find bare except Exception as e: without Exception
            if re.match(r"^(\s*)except\s*:\s*$", line):
                indent = len(line) - len(line.lstrip())
                # IMPROVED: lines[i] = " " * indent + "except Exception as e:"

                # Add logging if the next line doesn"t already have it
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if not any(x in next_line for x in ["logger", "logging", "print"]):
                        log_line = " " * (indent + 4) + "logger.error(f'Unexpected error: {e}', exc_info=True)"
                        lines.insert(i + 1, log_line)

                # IMPROVED: fixes.append(f"Line {i+1}: Fixed bare except Exception as e: block and added error logging")
                modified = True

        return '\n'.join(lines) if modified else content, fixes

    def fix_resource_leaks(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Fix common resource leak patterns."""
        fixes = []
        lines = content.split("\n")
        modified = False

        i = 0
        while i < len(lines):
            line = lines[i]

            # Find file open patterns without context managers
            open_match = re.search(r"(\s*)(\w+)\s*=\s*open\s*\(([^)]+)\)", line)
            if open_match and "with " not in line:
                indent = open_match.group(1)
                var_name = open_match.group(2)
                args = open_match.group(3)

                # Convert to context manager
                new_line = f"{indent}with open({args}) as {var_name}:"
                lines[i] = new_line

                # Indent the following block until we find the close() or end of scope
                j = i + 1
                while j < len(lines) and (lines[j].strip() == "" or len(lines[j]) - len(lines[j].lstrip()) > len(indent)):
                    if lines[j].strip():
                        lines[j] = "    " + lines[j]  # Add extra indent
                    j += 1

                # Remove explicit close() calls
                for k in range(i + 1, j):
                    if f"{var_name}.close()" in lines[k]:
                        lines[k] = ""  # Remove the close call

                fixes.append(f"Line {i+1}: Converted file open to context manager")
                modified = True

            i += 1

        return "\n".join(lines) if modified else content, fixes

    def fix_unused_imports(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Remove unused imports using AST analysis."""
        fixes = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content, fixes

        # Collect all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, alias.asname or alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append((alias.name, alias.asname or alias.name, node.lineno))

        # Find which imports are actually used
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                # For a.b.c, we want to track "a"
                while isinstance(node.value, ast.Attribute):
                    node = node.value
                if isinstance(node.value, ast.Name):
                    used_names.add(node.value.id)

        # Remove unused imports
        lines = content.split("\n")
        lines_to_remove = []

        for import_name, alias_name, line_no in imports:
            if alias_name not in used_names:
                # Skip common imports that might be used indirectly
                if import_name not in ["logging", "os", "sys", "json", "re"]:
                    lines_to_remove.append(line_no - 1)  # Convert to 0-based

        # Remove lines in reverse order to maintain line numbers
        for line_idx in sorted(lines_to_remove, reverse=True):
            if line_idx < len(lines):
                fixes.append(f"Line {line_idx + 1}: Removed unused import: {lines[line_idx].strip()}")
                lines.pop(line_idx)

        if fixes:
            return "\n".join(lines), fixes
        return content, fixes

    def fix_long_functions(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Identify and suggest fixes for overly long functions."""
        fixes = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return content, fixes

        lines = content.split("\n")

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno - 1
                end_line = node.end_lineno - 1 if node.end_lineno else len(lines)
                function_length = end_line - start_line

                if function_length > 50:  # Functions longer than 50 lines
                    fixes.append(f"Line {node.lineno}: Function '{node.name}' is {function_length} lines long - consider refactoring")

        return content, fixes

    def fix_missing_type_hints(self, file_path: str, content: str) -> Tuple[str, List[str]]:
        """Add basic type hints where they"re obviously missing."""
        fixes = []
        lines = content.split('\n')
        modified = False

        for i, line in enumerate(lines):
            # Look for function definitions without type hints
            func_match = re.match(r"^(\s*)def\s+(\w+)\s*\(([^)]*)\)\s*:\s*$", line)
            if func_match:
                indent = func_match.group(1)
                func_name = func_match.group(2)
                params = func_match.group(3).strip()

                # Skip if already has type hints or is special method
                if "->" in line or "__" in func_name or ":" in params:
                    continue

                # Add simple return type hint for common patterns
                next_lines = lines[i+1:i+10]  # Look at next few lines
                return_pattern = None

                for next_line in next_lines:
                    if "return True" in next_line or "return False" in next_line:
                        return_pattern = " -> bool"
                        break
                    elif "return []" in next_line or "return list(" in next_line:
                        return_pattern = " -> List"
                        break
                    elif "return {}" in next_line or "return dict(" in next_line:
                        return_pattern = " -> Dict"
                        break
                    elif "return None" in next_line:
                        return_pattern = " -> None"
                        break
                    elif re.search(r"return\s+\d+", next_line):
                        return_pattern = " -> int"
                        break
                    elif re.search(r"return\s+['\"]", next_line):
                        return_pattern = " -> str"
                        break

                if return_pattern:
                    lines[i] = line.rstrip(":") + return_pattern + ":"
                    fixes.append(f"Line {i+1}: Added return type hint to function '{func_name}'")
                    modified = True

        # Add imports if we added type hints
        if modified and "from typing import" not in content:
            # Find where to insert the import
            import_line = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    import_line = i + 1
                elif line.strip() and import_line > 0:
                    break

            lines.insert(import_line, "from typing import List, Dict, Optional, Any")
            fixes.append("Added typing imports for type hints")

        return '\n'.join(lines) if modified else content, fixes

    def fix_file(self, file_path: Path) -> Dict[str, List[str]]:
        """Apply all advanced fixes to a single file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            all_fixes = {}

            # Apply fixes in order
            content, fixes1 = self.fix_bare_except_blocks(str(file_path), content)
            if fixes1:
                all_fixes["bare_except_blocks"] = fixes1

            content, fixes2 = self.fix_resource_leaks(str(file_path), content)
            if fixes2:
                all_fixes["resource_leaks"] = fixes2

            content, fixes3 = self.fix_unused_imports(str(file_path), content)
            if fixes3:
                all_fixes["unused_imports"] = fixes3

            content, fixes4 = self.fix_long_functions(str(file_path), content)
            if fixes4:
                all_fixes["long_functions"] = fixes4

            content, fixes5 = self.fix_missing_type_hints(str(file_path), content)
            if fixes5:
                all_fixes["missing_type_hints"] = fixes5

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

                    _, fixes1 = self.fix_bare_except_blocks(str(py_file), content)
                    _, fixes2 = self.fix_resource_leaks(str(py_file), content)
                    _, fixes3 = self.fix_unused_imports(str(py_file), content)
                    _, fixes4 = self.fix_long_functions(str(py_file), content)
                    _, fixes5 = self.fix_missing_type_hints(str(py_file), content)

                    fixes = {}
                    if fixes1: fixes["bare_except_blocks"] = fixes1
                    if fixes2: fixes["resource_leaks"] = fixes2
                    if fixes3: fixes["unused_imports"] = fixes3
                    if fixes4: fixes["long_functions"] = fixes4
                    if fixes5: fixes["missing_type_hints"] = fixes5
                except Exception as e:
                    fixes = {"error": [f"Analysis failed: {e}"]}

            if fixes:
                results[str(py_file.relative_to(self.project_path))] = fixes

        return results

def main():
    import sys

    if len(sys.argv) < 2:
        logger.info("Usage: python advanced_fixer.py <project_path> [--apply]")
        sys.exit(1)

    project_path = sys.argv[1]
    apply_fixes = "--apply" in sys.argv

    fixer = AdvancedIssueFixer(project_path)
    results = fixer.fix_project(dry_run=not apply_fixes)

    total_fixes = sum(len(fixes) for file_fixes in results.values() for fixes in file_fixes.values())
    mode = "APPLIED" if apply_fixes else "DRY RUN"

    logger.info(f"🔧 Advanced Issue Fixer Results")
    logger.info(f"===============================")
    logger.info(f"🎯 Mode: {mode}")
    logger.info(f"📊 Total Fixes: {total_fixes}")
    logger.info(f"📁 Files Affected: {len(results)}")
    logger.info()

    for file_path, file_fixes in results.items():
        if file_fixes:
            logger.info(f"📄 {file_path}")
            for category, fixes in file_fixes.items():
                logger.info(f"   🔧 {category}: {len(fixes)} fixes")
                if len(fixes) <= 3:  # Show details for files with few fixes
                    for fix in fixes:
                        logger.info(f"      - {fix}")
                logger.info()

if __name__ == "__main__":
    main()