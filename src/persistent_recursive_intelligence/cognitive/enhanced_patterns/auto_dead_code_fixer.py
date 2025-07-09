#!/usr/bin/env python3
"""
Automatic Dead Code Fixer for PRI System
Automatically removes safe dead code and identifies duplicates
"""

import ast
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import logging

try:
    from .dead_code_detector import detect_dead_code_in_file, scan_project_for_dead_code
except ImportError:
    # Handle when run as standalone script
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from dead_code_detector import detect_dead_code_in_file, scan_project_for_dead_code

logger = logging.getLogger(__name__)

class AutoDeadCodeFixer:
    """Automatically fix safe dead code issues"""

    def __init__(self, project_path: str, dry_run: bool = True):
        self.project_path = Path(project_path)
        self.dry_run = dry_run
        self.fixes_applied = []
        self.duplicates_found = []
        self.unsafe_removals = []

    def is_safe_to_remove_import(self, import_name: str, file_content: str) -> bool:
        """Check if an import is safe to remove automatically"""
        # Don"t remove imports that might be used dynamically
        unsafe_patterns = [
            r"getattr\s*\(",
            r"hasattr\s*\(",
            r"setattr\s*\(",
            r"__import__\s*\(",
            r"importlib\.",
            r"globals\s*\(\)",
            r"locals\s*\(\)",
            r"eval\s*\(",
            r"exec\s*\(",
            rf"['\"{import_name}['\"]",  # String references to the import
        ]

        for pattern in unsafe_patterns:
            if re.search(pattern, file_content, re.IGNORECASE):
                return False

        # Check if it"s a common library that might be used in ways we can"t detect
        dynamic_libraries = {
            "logging", "os", "sys", "json", "time", "datetime",
            "requests", "flask", "django", "numpy", "pandas"
        }

        if import_name.lower() in dynamic_libraries:
            return False

        return True

    def find_duplicate_functions(self, python_files: List[Path]) -> Dict[str, List[Tuple[str, str]]]:
        """Find duplicate functions across files"""
        function_signatures = defaultdict(list)

        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Create a signature based on function name and parameters
                        params = [arg.arg for arg in node.args.args]
                        signature = f"{node.name}({', '.join(params)})"

                        # Get function body hash for exact duplicate detection
                        func_source = ast.get_source_segment(content, node)
                        if func_source:
                            body_hash = hashlib.md5(func_source.encode()).hexdigest()
                            function_signatures[signature].append((str(py_file), body_hash, func_source))

            except Exception as e:
                logger.warning(f"Error analyzing {py_file}: {e}")

        duplicates = {}
        for signature, instances in function_signatures.items():
            if len(instances) > 1:
                # Group by body hash
                by_hash = defaultdict(list)
                for file_path, body_hash, source in instances:
                    by_hash[body_hash].append((file_path, source))

                # Report groups with multiple files
                for body_hash, files in by_hash.items():
                    if len(files) > 1:
                        duplicates[f"{signature}_{body_hash[:8]}"] = files

        return duplicates

    def find_duplicate_classes(self, python_files: List[Path]) -> Dict[str, List[Tuple[str, str]]]:
        """Find duplicate classes across files"""
        class_signatures = defaultdict(list)

        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        # Create a signature based on class name and methods
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        signature = f"{node.name}({', '.join(sorted(methods))})"

                        # Get class source for duplicate detection
                        class_source = ast.get_source_segment(content, node)
                        if class_source:
                            body_hash = hashlib.md5(class_source.encode()).hexdigest()
                            class_signatures[signature].append((str(py_file), body_hash, class_source))

            except Exception as e:
                logger.warning(f"Error analyzing {py_file}: {e}")

        # Find actual duplicates
        duplicates = {}
        for signature, instances in class_signatures.items():
            if len(instances) > 1:
                by_hash = defaultdict(list)
                for file_path, body_hash, source in instances:
                    by_hash[body_hash].append((file_path, source))

                for body_hash, files in by_hash.items():
                    if len(files) > 1:
                        duplicates[f"{signature}_{body_hash[:8]}"] = files

        return duplicates

    def remove_unused_imports(self, file_path: str, unused_imports: List[str]) -> int:
        """Remove unused imports from a file"""
        if not unused_imports:
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            removed_count = 0

            for line in lines:
                should_remove = False

                # Check for import statements
                for unused_import in unused_imports:
                    patterns = [
                        rf'^import\s+{re.escape(unused_import)}$',
                        rf"^import\s+{re.escape(unused_import)}\s*#",
                        rf"^from\s+\S+\s+import\s+{re.escape(unused_import)}$",
                        rf"^from\s+\S+\s+import\s+{re.escape(unused_import)}\s*#",
                        rf"^from\s+\S+\s+import\s+.*\b{re.escape(unused_import)}\b.*$",
                    ]

                    for pattern in patterns:
                        if re.match(pattern, line.strip()):
                            # Double-check it"s safe to remove
                            file_content = "".join(lines)
                            if self.is_safe_to_remove_import(unused_import, file_content):
                                should_remove = True
                                removed_count += 1
                                self.fixes_applied.append({
                                    "file": file_path,
                                    "type": "unused_import_removal",
                                    "item": unused_import,
                                    "line": line.strip()
                                })
                                break

                if not should_remove:
                    new_lines.append(line)

            # Write back the file if we made changes and not in dry-run mode
            if removed_count > 0 and not self.dry_run:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

                logger.info(f"Removed {removed_count} unused imports from {file_path}")

            return removed_count

        except Exception as e:
            logger.error(f"Error removing imports from {file_path}: {e}")
            return 0

    def remove_unused_variables(self, file_path: str, unused_variables: List[str]) -> int:
        """Remove unused variables (safe cases only)"""
        if not unused_variables:
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = f.readlines()

            # Parse AST to find variable assignments
            tree = ast.parse(content, filename=file_path)
            removed_count = 0
            lines_to_remove = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    # Only handle simple assignments
                    if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                        var_name = node.targets[0].id

                        if var_name in unused_variables:
                            # Check if it"s a simple, safe-to-remove assignment
                            if self.is_safe_variable_removal(node, content):
                                line_num = node.lineno - 1  # AST uses 1-based indexing
                                if 0 <= line_num < len(lines):
                                    lines_to_remove.add(line_num)
                                    removed_count += 1
                                    self.fixes_applied.append({
                                        "file": file_path,
                                        "type": "unused_variable_removal",
                                        "item": var_name,
                                        "line": lines[line_num].strip()
                                    })

            # Remove the lines and write back
            if removed_count > 0 and not self.dry_run:
                new_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

                logger.info(f"Removed {removed_count} unused variables from {file_path}")

            return removed_count

        except Exception as e:
            logger.error(f"Error removing variables from {file_path}: {e}")
            return 0

    def is_safe_variable_removal(self, assign_node: ast.Assign, file_content: str) -> bool:
        """Check if a variable assignment is safe to remove"""
        # Don"t remove if the assignment has side effects
        if isinstance(assign_node.value, (ast.Call, ast.ListComp, ast.DictComp, ast.SetComp)):
            return False

        # Don"t remove if it"s a constant that might be referenced elsewhere
        if isinstance(assign_node.value, (ast.Constant, ast.Str, ast.Num)):
            var_name = assign_node.targets[0].id
            # Check for string references
            if re.search(rf'["\'{var_name}["\']', file_content):
                return False

        return True

    def suggest_connections_for_orphaned_files(self, orphaned_files: List[Path]) -> Dict[str, List[Dict]]:
        """Analyze orphaned files and suggest intelligent connections to main codebase"""
        suggestions = {}
        
        # Get all main codebase files (excluding orphaned ones)
        all_files = [f for f in self.project_path.rglob("*.py")
                    if not any(skip in str(f) for skip in ["venv", "__pycache__", ".git"])]
        main_files = [f for f in all_files if f not in orphaned_files]
        
        for orphaned_file in orphaned_files:
            file_suggestions = []
            
            try:
                with open(orphaned_file, "r", encoding="utf-8") as f:
                    orphaned_content = f.read()
                
                orphaned_ast = ast.parse(orphaned_content)
                orphaned_analysis = self._analyze_file_capabilities(orphaned_ast, orphaned_content)
                
                # Analyze main codebase files for connection opportunities
                for main_file in main_files:
                    try:
                        with open(main_file, "r", encoding="utf-8") as f:
                            main_content = f.read()
                        
                        main_ast = ast.parse(main_content)
                        connection_score = self._calculate_connection_score(
                            orphaned_analysis, main_file, main_ast, main_content
                        )
                        
                        if connection_score > 0.3:  # Threshold for meaningful connections
                            suggestion = {
                                "target_file": str(main_file.relative_to(self.project_path)),
                                "score": connection_score,
                                "connection_type": self._determine_connection_type(orphaned_analysis, main_ast),
                                "integration_suggestions": self._generate_integration_suggestions(
                                    orphaned_analysis, main_file, main_ast, main_content
                                )
                            }
                            file_suggestions.append(suggestion)
                    
                    except Exception as e:
                        logger.debug(f"Error analyzing {main_file}: {e}")
                
                # Sort suggestions by score
                file_suggestions.sort(key=lambda x: x["score"], reverse=True)
                suggestions[str(orphaned_file.relative_to(self.project_path))] = file_suggestions[:5]  # Top 5
                
            except Exception as e:
                logger.error(f"Error analyzing orphaned file {orphaned_file}: {e}")
        
        return suggestions

    def _analyze_file_capabilities(self, ast_tree: ast.AST, content: str) -> Dict:
        """Analyze what capabilities an orphaned file provides"""
        capabilities = {
            "functions": [],
            "classes": [],
            "constants": [],
            "imports": [],
            "keywords": set(),
            "complexity_score": 0
        }
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._extract_return_type(node),
                    "docstring": ast.get_docstring(node),
                    "complexity": len([n for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While))])
                }
                capabilities["functions"].append(func_info)
                capabilities["complexity_score"] += func_info["complexity"]
            
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "docstring": ast.get_docstring(node)
                }
                capabilities["classes"].append(class_info)
            
            elif isinstance(node, ast.Assign):
                # Look for constants (uppercase variables)
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        capabilities["constants"].append(target.id)
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        capabilities["imports"].append(alias.name)
                else:
                    capabilities["imports"].append(node.module or "")
        
        # Extract keywords from comments and docstrings
        capabilities["keywords"] = self._extract_keywords(content)
        
        return capabilities

    def _calculate_connection_score(self, orphaned_analysis: Dict, main_file: Path, 
                                  main_ast: ast.AST, main_content: str) -> float:
        """Calculate how well an orphaned file could connect to a main file"""
        score = 0.0
        
        # Analyze main file capabilities
        main_analysis = self._analyze_file_capabilities(main_ast, main_content)
        
        # Function compatibility scoring
        orphaned_funcs = set(f["name"] for f in orphaned_analysis["functions"])
        main_funcs = set(f["name"] for f in main_analysis["functions"])
        
        # Check for complementary functions (not duplicates)
        if orphaned_funcs and not orphaned_funcs.intersection(main_funcs):
            score += 0.3
        
        # Keyword similarity (semantic relatedness)
        keyword_overlap = orphaned_analysis["keywords"].intersection(main_analysis["keywords"])
        if keyword_overlap:
            score += min(0.4, len(keyword_overlap) * 0.1)
        
        # Import similarity (shared dependencies suggest related functionality)
        orphaned_imports = set(orphaned_analysis["imports"])
        main_imports = set(main_analysis["imports"])
        import_overlap = orphaned_imports.intersection(main_imports)
        if import_overlap:
            score += min(0.3, len(import_overlap) * 0.05)
        
        # Check if orphaned file provides something main file might need
        missing_functionality_score = self._detect_missing_functionality(orphaned_analysis, main_content)
        score += missing_functionality_score
        
        return min(1.0, score)

    def _determine_connection_type(self, orphaned_analysis: Dict, main_ast: ast.AST) -> str:
        """Determine the type of connection that would be most appropriate"""
        if orphaned_analysis["classes"]:
            return "class_import"
        elif orphaned_analysis["functions"]:
            if len(orphaned_analysis["functions"]) == 1:
                return "function_import"
            else:
                return "module_import"
        elif orphaned_analysis["constants"]:
            return "constant_import"
        else:
            return "utility_import"

    def _generate_integration_suggestions(self, orphaned_analysis: Dict, main_file: Path,
                                        main_ast: ast.AST, main_content: str) -> List[str]:
        """Generate specific suggestions for how to integrate the orphaned file"""
        suggestions = []
        orphaned_rel_path = str(main_file.parent.relative_to(self.project_path))
        
        if orphaned_analysis["functions"]:
            func_names = [f["name"] for f in orphaned_analysis["functions"]]
            if len(func_names) == 1:
                suggestions.append(f"Import function: from .{orphaned_rel_path} import {func_names[0]}")
            else:
                suggestions.append(f"Import module: from . import {orphaned_rel_path}")
                suggestions.append(f"Import functions: from .{orphaned_rel_path} import {', '.join(func_names[:3])}")
        
        if orphaned_analysis["classes"]:
            class_names = [c["name"] for c in orphaned_analysis["classes"]]
            suggestions.append(f"Import classes: from .{orphaned_rel_path} import {', '.join(class_names)}")
        
        # Suggest specific integration points based on main file analysis
        integration_points = self._find_integration_points(main_ast)
        for point in integration_points:
            suggestions.append(f"Consider integrating at line {point['line']}: {point['suggestion']}")
        
        return suggestions

    def _extract_keywords(self, content: str) -> Set[str]:
        """Extract meaningful keywords from file content"""
        keywords = set()
        
        # Extract from comments
        comment_pattern = r'#\s*(.*?)(?:\n|$)'
        comments = re.findall(comment_pattern, content)
        for comment in comments:
            words = re.findall(r'\b\w{3,}\b', comment.lower())
            keywords.update(words)
        
        # Extract from docstrings  
        docstring_pattern = r'"""(.*?)"""'
        docstrings = re.findall(docstring_pattern, content, re.DOTALL)
        for docstring in docstrings:
            words = re.findall(r'\b\w{3,}\b', docstring.lower())
            keywords.update(words)
        
        # Filter out common programming words
        common_words = {'def', 'class', 'import', 'from', 'return', 'self', 'args', 'kwargs', 'true', 'false', 'none'}
        return keywords - common_words

    def _extract_return_type(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation if present"""
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

    def _detect_missing_functionality(self, orphaned_analysis: Dict, main_content: str) -> float:
        """Detect if orphaned file provides functionality that main file might need"""
        score = 0.0
        
        # Look for TODO comments that might indicate missing functionality
        todo_pattern = r'#\s*# ADDRESSED:?\s*(.*?)(?:\n|$)'
        todos = re.findall(todo_pattern, main_content, re.IGNORECASE)
        
        for todo in todos:
            todo_lower = todo.lower()
            for func in orphaned_analysis["functions"]:
                func_name_lower = func["name"].lower()
                if func_name_lower in todo_lower or any(word in todo_lower for word in func_name_lower.split('_')):
                    score += 0.2
        
        # Look for placeholder functions or NotImplementedError
        if "NotImplementedError" in main_content or "pass  # TODO" in main_content:
            score += 0.1
        
        return min(0.4, score)

    def _find_integration_points(self, main_ast: ast.AST) -> List[Dict]:
        """Find potential integration points in the main file"""
        points = []
        
        for node in ast.walk(main_ast):
            if isinstance(node, ast.FunctionDef):
                # Look for functions that might benefit from additional functionality
                if len(node.body) <= 3:  # Short functions might need more functionality
                    points.append({
                        "line": node.lineno,
                        "suggestion": f"Function '{node.name}' might benefit from additional functionality"
                    })
            elif isinstance(node, ast.Raise):
                if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                    if node.exc.func.id == "NotImplementedError":
                        points.append({
                            "line": node.lineno,
                            "suggestion": "NotImplementedError could be replaced with imported functionality"
                        })
        
        return points

    def auto_fix_project(self) -> Dict:
        """Automatically fix safe dead code issues and suggest connections for orphaned files"""
        logger.info(f"Starting automatic dead code fixing for {self.project_path}")

        # Get all Python files
        python_files = [f for f in self.project_path.rglob("*.py")
                       if not any(skip in str(f) for skip in ["venv", "__pycache__", ".git"])]

        # Find duplicates first
        logger.info("Scanning for duplicate functions...")
        duplicate_functions = self.find_duplicate_functions(python_files)

        logger.info("Scanning for duplicate classes...")
        duplicate_classes = self.find_duplicate_classes(python_files)

        # Identify orphaned files using dead file detector
        try:
            from .dead_file_detector import DeadFileDetector
            dead_detector = DeadFileDetector(str(self.project_path))
            dead_issues = dead_detector.analyze_project()
            
            orphaned_files = []
            for issue in dead_issues:
                if issue.issue_type in ["dead_file", "unconnected_file"]:
                    orphaned_files.append(self.project_path / issue.file_path)
            
            logger.info(f"Found {len(orphaned_files)} potentially orphaned files")
            
            # Generate connection suggestions for orphaned files
            connection_suggestions = {}
            if orphaned_files:
                logger.info("Generating connection suggestions for orphaned files...")
                connection_suggestions = self.suggest_connections_for_orphaned_files(orphaned_files)
        
        except ImportError:
            logger.warning("DeadFileDetector not available, skipping orphaned file analysis")
            connection_suggestions = {}

        # Process dead code for each file
        logger.info("Processing dead code issues...")
        total_fixes = 0
        files_processed = 0

        for py_file in python_files:
            try:
                # Skip test files and vendored code for safety
                if any(skip in str(py_file).lower() for skip in ["test_", "_test.py", "tests/", "vendor/", "site-packages/"]):
                    continue

                result = detect_dead_code_in_file(str(py_file))
                if result.get("dead_code_issues"):
                    # Auto-fix unused imports
                    import_fixes = self.remove_unused_imports(
                        str(py_file),
                        result.get("dead_imports", [])
                    )

                    var_fixes = self.remove_unused_variables(
                        str(py_file),
                        result.get("dead_variables", [])
                    )

                    total_fixes += import_fixes + var_fixes
                    if import_fixes + var_fixes > 0:
                        files_processed += 1

            except Exception as e:
                logger.error(f"Error processing {py_file}: {e}")

        results = {
            "total_fixes_applied": total_fixes,
            "files_processed": files_processed,
            "duplicate_functions": duplicate_functions,
            "duplicate_classes": duplicate_classes,
            "connection_suggestions": connection_suggestions,
            "fixes_applied": self.fixes_applied,
            "dry_run": self.dry_run
        }

        logger.info(f"Auto-fixing complete: {total_fixes} fixes applied to {files_processed} files")
        if connection_suggestions:
            logger.info(f"Generated connection suggestions for {len(connection_suggestions)} orphaned files")
        
        return results

def auto_fix_dead_code(project_path: str, dry_run: bool = True) -> Dict:
    """Main function to automatically fix dead code"""
    fixer = AutoDeadCodeFixer(project_path, dry_run=dry_run)
    return fixer.auto_fix_project()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Automatically fix dead code issues")
    parser.add_argument("project_path", help="Path to the project to fix")
    parser.add_argument("--apply", action="store_true", help="Actually apply fixes (default is dry-run)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    dry_run = not args.apply
    results = auto_fix_dead_code(args.project_path, dry_run=dry_run)

    logger.info(f"\n🔧 Automatic Dead Code Fixing Results")
    logger.info("=" * 50)
    logger.info(f"🎯 Mode: {'DRY RUN' if dry_run else 'APPLYING FIXES'}")
    logger.info(f"📊 Total Fixes: {results['total_fixes_applied']}")
    logger.info(f"📁 Files Processed: {results['files_processed']}")

    if results["duplicate_functions"]:
        logger.info(f"\n🔄 Duplicate Functions Found: {len(results['duplicate_functions'])}")
        for sig, files in list(results["duplicate_functions"].items())[:5]:  # Show first 5
            logger.info(f"   - {sig}: {len(files)} instances")

    if results["duplicate_classes"]:
        logger.info(f"\n🔄 Duplicate Classes Found: {len(results['duplicate_classes'])}")
        for sig, files in list(results["duplicate_classes"].items())[:5]:  # Show first 5
            logger.info(f"   - {sig}: {len(files)} instances")

    if results.get("connection_suggestions"):
        logger.info(f"\n🔗 Code Connector Suggestions: {len(results['connection_suggestions'])} orphaned files")
        for orphaned_file, suggestions in list(results["connection_suggestions"].items())[:3]:  # Show first 3
            logger.info(f"   📁 {orphaned_file}:")
            for suggestion in suggestions[:2]:  # Top 2 suggestions per file
                logger.info(f"      → {suggestion['target_file']} (score: {suggestion['score']:.2f})")
                if suggestion['integration_suggestions']:
                    logger.info(f"        💡 {suggestion['integration_suggestions'][0]}")

    if results["fixes_applied"] and args.verbose:
        logger.info(f"\n📋 Applied Fixes:")
        for fix in results["fixes_applied"][:10]:  # Show first 10
            logger.info(f"   {fix['type']}: {fix['item']} in {fix['file']}")