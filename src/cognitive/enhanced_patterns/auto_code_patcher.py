#!/usr/bin/env python3
"""
Automatic Code Patcher for PRI System
Automatically patches obvious missing code patterns and fixes incomplete implementations
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

class AutoCodePatcher:
    """Automatically patch obvious missing code patterns"""

    def __init__(self, project_path: str, dry_run: bool = True):
        self.project_path = Path(project_path)
        self.dry_run = dry_run
        self.patches_applied = []
        self.common_patterns = self._load_common_patterns()

    def _load_common_patterns(self) -> Dict:
        """Load common code patterns for auto-patching"""
        return {
            "missing_imports": {
                "logging": ["logging.getLogger", "logger.info", "logger.error", "logger.warning"],
                "os": ["os.path", "os.environ", "os.getcwd"],
                "sys": ["sys.exit", "sys.argv", "sys.path"],
                "json": ["json.loads", "json.dumps"],
                "time": ["time.time", "time.sleep"],
                "datetime": ["datetime.now", "datetime.datetime"],
                "pathlib": ["Path(", "pathlib.Path"],
                "re": ["re.search", "re.match", "re.findall", "re.compile"],
                "typing": ["List[", "Dict[", "Optional[", "Union[", "Tuple["],
            },
            "incomplete_functions": {
                "pass_only": r'def\s+\w+\([^)]*\):\s*pass\s*$',
                "todo_only": r"def\s+\w+\([^)]*\):\s*#\s*TODO",
                "empty_except": r"except\s+[^:]*:\s*pass\s*$",
                "empty_try": r"try:\s*pass\s*except",
            },
            "missing_docstrings": {
                "class_no_doc": r"class\s+\w+[^:]*:\s*(?!\"\"\")",
                "function_no_doc": r"def\s+\w+\([^)]*\):\s*(?!\"\"\")",
            },
            "common_fixes": {
                "missing_main_guard": "__name__ == '__main__'",
                "missing_return": r"def.*->.*:\s*(?!.*return)",
                "unfinished_string": r"['\"].*[^'\"]$",
                "missing_close_paren": r'\([^)]*$',
                "missing_close_bracket": r"\[[^\]]*$",
                "missing_close_brace": r"\{[^}]*$",
            }
        }

    def detect_missing_imports(self, file_path: str, content: str) -> List[str]:
        """Detect missing imports based on usage patterns"""
        missing_imports = []

        for import_name, usage_patterns in self.common_patterns["missing_imports"].items():
            # Check if import already exists
            import_patterns = [
                rf"^import\s+{import_name}",
                rf"^from\s+{import_name}\s+import",
                rf"import.*\b{import_name}\b",
            ]

            has_import = any(re.search(pattern, content, re.MULTILINE) for pattern in import_patterns)

            if not has_import:
                # Check if any usage patterns are found
                for usage in usage_patterns:
                    if usage in content:
                        missing_imports.append(import_name)
                        break

        return missing_imports

    def detect_incomplete_functions(self, file_path: str, content: str) -> List[Dict]:
        """Detect incomplete function implementations"""
        incomplete_functions = []

        try:
            tree = ast.parse(content, filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check for functions with only "pass"
                    if (len(node.body) == 1 and
                        isinstance(node.body[0], ast.Pass)):
                        incomplete_functions.append({
                            "type": "pass_only_function",
                            "name": node.name,
                            "lineno": node.lineno,
                            "suggestion": self._suggest_function_implementation(node)
                        })

                    # Check for functions with missing return statements when they should have them
                    if node.returns and not self._has_return_statement(node):
                        incomplete_functions.append({
                            "type": "missing_return",
                            "name": node.name,
                            "lineno": node.lineno,
                            "suggestion": self._suggest_return_statement(node)
                        })

                # Check for empty except blocks
                if isinstance(node, ast.ExceptHandler):
                    if (len(node.body) == 1 and
                        isinstance(node.body[0], ast.Pass)):
                        incomplete_functions.append({
                            "type": "empty_except",
                            "lineno": node.lineno,
                            "suggestion": "logger.error(f'Error in exception handling: {e}')"
                        })

        except SyntaxError as e:
            logger.warning(f"Syntax error in {file_path}: {e}")

        return incomplete_functions

    def _suggest_function_implementation(self, func_node: ast.FunctionDef) -> str:
        """Suggest a basic implementation for a function based on its name and signature"""
        func_name = func_node.name.lower()

        # Common patterns based on function names
        if "get_" in func_name:
            if func_node.returns:
                return f"    '''Get {func_name[4:].replace('_', ' ')}'''\n    # Implement getter logic\n    return None"
            else:
                return f"    '''Get {func_name[4:].replace('_', ' ')}'''\n    # Implement getter logic\n    pass"

        elif "set_" in func_name:
            return f"    '''Set {func_name[4:].replace('_', ' ')}'''\n    # Implement setter logic\n    pass"

        elif "init" in func_name:
            return f"    '''Initialize {func_name.replace('_', ' ')}'''\n    # Implement initialization logic\n    pass"

        elif "create" in func_name:
            return f"    '''Create {func_name[7:].replace('_', ' ') if func_name.startswith('create_') else 'resource'}'''\n    # TODO: Implement creation logic\n    return None"

        elif "validate" in func_name:
            return f"    '''Validate input parameters'''\n    # Implement validation logic\n    return True"

        elif "process" in func_name:
            return f"    '''Process {func_name[8:].replace('_', ' ') if func_name.startswith('process_') else 'data'}'''\n    # TODO: Implement processing logic\n    pass"

        else:
            return f"    '''{func_name.replace('_', ' ').title()}'''\n    # Implement function logic\n    pass"

    def _has_return_statement(self, func_node: ast.FunctionDef) -> bool:
        """Check if function has any return statements"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return):
                return True
        return False

    def _suggest_return_statement(self, func_node: ast.FunctionDef) -> str:
        """Suggest appropriate return statement based on function annotation"""
        if func_node.returns:
            if isinstance(func_node.returns, ast.Name):
                type_name = func_node.returns.id
                if type_name in ["bool", "Boolean"]:
                    return "return False  # Return appropriate boolean value"
                elif type_name in ["int", "Integer"]:
                    return "return 0  # Return appropriate integer value"
                elif type_name in ["str", "String"]:
                    return "return ""  # Return appropriate string value"
                elif type_name in ["list", "List"]:
                    return "return []  # Return appropriate list"
                elif type_name in ["dict", "Dict"]:
                    return "return {}  # Return appropriate dictionary"

        return "return None  # Return appropriate value"

    def detect_syntax_errors(self, file_path: str, content: str) -> List[Dict]:
        """Detect and suggest fixes for obvious syntax errors"""
        syntax_issues = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for unmatched parentheses, brackets, braces
            if line.count("(") > line.count(")"):
                syntax_issues.append({
                    "type": "unmatched_parentheses",
                    "lineno": i,
                    "line": line,
                    "suggestion": line + ")"
                })

            if line.count("[") > line.count("]"):
                syntax_issues.append({
                    "type": "unmatched_brackets",
                    "lineno": i,
                    "line": line,
                    "suggestion": line + "]"
                })

            if line.count("{") > line.count("}"):
                syntax_issues.append({
                    "type": "unmatched_braces",
                    "lineno": i,
                    "line": line,
                    "suggestion": line + "}"
                })

            # Check for incomplete strings
            if re.search(r"['\"][^'\"]*$", line.strip()) and not line.strip().endswith('\\'):
                quote_char = '"' if '"' in line else "'"
                syntax_issues.append({
                    "type": "incomplete_string",
                    "lineno": i,
                    "line": line,
                    "suggestion": line + quote_char
                })

        return syntax_issues

    def apply_missing_imports_fix(self, file_path: str, missing_imports: List[str]) -> int:
        """Apply missing imports fix"""
        if not missing_imports:
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith(("import ", "from ")):
                    insert_index = i + 1
                elif line.strip() and not line.strip().startswith("#"):
                    break

            # Add missing imports
            import_lines = []
            for import_name in missing_imports:
                import_lines.append(f'import {import_name}\n')

            new_lines = lines[:insert_index] + import_lines + lines[insert_index:]

            if not self.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

            for import_name in missing_imports:
                self.patches_applied.append({
                    "file": file_path,
                    "type": "missing_import_added",
                    "item": import_name,
                    "line_added": insert_index
                })

            logger.info(f"Added {len(missing_imports)} missing imports to {file_path}")
            return len(missing_imports)

        except Exception as e:
            logger.error(f"Error adding imports to {file_path}: {e}")
            return 0

    def apply_function_completion_fix(self, file_path: str, incomplete_functions: List[Dict]) -> int:
        """Apply fixes for incomplete functions"""
        if not incomplete_functions:
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Sort by line number in reverse order to avoid index shifting
            incomplete_functions.sort(key=lambda x: x["lineno"], reverse=True)

            fixes_applied = 0
            for func_info in incomplete_functions:
                line_idx = func_info["lineno"] - 1

                if func_info["type"] == "pass_only_function":
                    # Replace "pass" with suggested implementation
                    for i in range(line_idx, len(lines)):
                        if "pass" in lines[i]:
                            lines[i] = lines[i].replace("pass", func_info["suggestion"])
                            fixes_applied += 1
                            break

                elif func_info["type"] == "missing_return":
                    # Add return statement before function end
                    # Find function end
                    indent_level = len(lines[line_idx]) - len(lines[line_idx].lstrip())
                    for i in range(line_idx + 1, len(lines)):
                        if (lines[i].strip() and
                            len(lines[i]) - len(lines[i].lstrip()) <= indent_level):
                            # Insert return statement before this line
                            return_line = " " * (indent_level + 4) + func_info["suggestion"] + "\n"
                            lines.insert(i, return_line)
                            fixes_applied += 1
                            break

                self.patches_applied.append({
                    "file": file_path,
                    "type": f"function_completion_{func_info['type']}",
                    "item": func_info.get("name", "unknown"),
                    "line": func_info["lineno"]
                })

            if fixes_applied > 0 and not self.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                logger.info(f"Applied {fixes_applied} function completion fixes to {file_path}")

            return fixes_applied

        except Exception as e:
            logger.error(f"Error fixing functions in {file_path}: {e}")
            return 0

    def auto_patch_project(self) -> Dict:
        """Automatically patch obvious issues in the project"""
        logger.info(f"Starting automatic code patching for {self.project_path}")

        # Get all Python files
        python_files = [f for f in self.project_path.rglob("*.py")
                       if not any(skip in str(f) for skip in ["venv", "__pycache__", ".git", "site-packages"])]

        total_patches = 0
        files_patched = 0

        for py_file in python_files:
            try:
                # Skip certain files for safety
                if any(skip in str(py_file).lower() for skip in ["test_", "_test.py", "vendor/"]):
                    continue

                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Detect and fix missing imports
                missing_imports = self.detect_missing_imports(str(py_file), content)
                import_fixes = self.apply_missing_imports_fix(str(py_file), missing_imports)

                # Detect and fix incomplete functions
                incomplete_functions = self.detect_incomplete_functions(str(py_file), content)
                function_fixes = self.apply_function_completion_fix(str(py_file), incomplete_functions)

                syntax_issues = self.detect_syntax_errors(str(py_file), content)

                file_patches = import_fixes + function_fixes
                total_patches += file_patches

                if file_patches > 0:
                    files_patched += 1

                if syntax_issues:
                    logger.warning(f"Found {len(syntax_issues)} syntax issues in {py_file}")

            except Exception as e:
                logger.error(f"Error processing {py_file}: {e}")

        results = {
            "total_patches_applied": total_patches,
            "files_patched": files_patched,
            "patches_applied": self.patches_applied,
            "dry_run": self.dry_run
        }

        logger.info(f"Auto-patching complete: {total_patches} patches applied to {files_patched} files")
        return results

def auto_patch_code(project_path: str, dry_run: bool = True) -> Dict:
    """Main function to automatically patch code issues"""
    patcher = AutoCodePatcher(project_path, dry_run=dry_run)
    return patcher.auto_patch_project()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automatically patch obvious code issues")
    parser.add_argument("project_path", help="Path to the project to patch")
    parser.add_argument("--apply", action="store_true", help="Actually apply patches (default is dry-run)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    dry_run = not args.apply
    results = auto_patch_code(args.project_path, dry_run=dry_run)

    logger.info(f"\n🔧 Automatic Code Patching Results")
    logger.info("=" * 50)
    logger.info(f"🎯 Mode: {'DRY RUN' if dry_run else 'APPLYING PATCHES'}")
    logger.info(f'📊 Total Patches: {results['total_patches_applied']}')
    logger.info(f'📁 Files Patched: {results["files_patched"]}')

    if results["patches_applied"] and args.verbose:
        logger.info(f"\n📋 Applied Patches:")
        for patch in results["patches_applied"][:10]:  # Show first 10
            logger.info(f"   {patch['type']}: {patch['item']} in {patch['file']}")