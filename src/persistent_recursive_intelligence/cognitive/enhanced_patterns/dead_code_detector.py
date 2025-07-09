#!/usr/bin/env python3
"""
Dead Code Detector for PRI System
Identifies unused imports, functions, classes, and variables
"""

import ast
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)

class DeadCodeDetector(ast.NodeVisitor):
    """AST visitor to detect dead code patterns"""

    def __init__(self):
        self.imports = set()
        self.definitions = set()
        self.usage = set()
        self.dead_imports = set()
        self.dead_functions = set()
        self.dead_classes = set()
        self.dead_variables = set()

    def visit_Import(self, node):
        """Track import statements"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Track from ... import statements"""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Track function definitions"""
        if not node.name.startswith("_"):  # Ignore private functions
            self.definitions.add(f"function:{node.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Track class definitions"""
        self.definitions.add(f"class:{node.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Track variable assignments"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                if not target.id.startswith("_"):  # Ignore private variables
                    self.definitions.add(f"variable:{target.id}")
        self.generic_visit(node)

    def visit_Name(self, node):
        """Track name usage"""
        if isinstance(node.ctx, ast.Load):
            self.usage.add(node.id)
            # Also check if it"s a defined function/class/variable
            self.usage.add(f"function:{node.id}")
            self.usage.add(f"class:{node.id}")
            self.usage.add(f"variable:{node.id}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Track attribute access"""
        if isinstance(node.value, ast.Name):
            self.usage.add(node.value.id)
        self.generic_visit(node)

    def analyze_dead_code(self):
        """Identify dead code after AST traversal"""
        # Find unused imports
        self.dead_imports = self.imports - self.usage

        # Find unused definitions
        unused_definitions = self.definitions - self.usage

        for item in unused_definitions:
            if item.startswith("function:"):
                self.dead_functions.add(item[9:])  # Remove "function:" prefix
            elif item.startswith("class:"):
                self.dead_classes.add(item[6:])    # Remove "class:" prefix
            elif item.startswith("variable:"):
                self.dead_variables.add(item[9:])  # Remove "variable:" prefix

def detect_dead_code_in_file(file_path: str) -> Dict:
    """Detect dead code in a single Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)
        detector = DeadCodeDetector()
        detector.visit(tree)
        detector.analyze_dead_code()

        issues = []

        # Add dead code issues
        for import_name in detector.dead_imports:
            issues.append({
                "type": "dead_code",
                "category": "unused_import",
                "message": f"Unused import: {import_name}",
                "severity": "medium"
            })

        for func_name in detector.dead_functions:
            issues.append({
                "type": "dead_code",
                "category": "unused_function",
                "message": f"Unused function: {func_name}",
                "severity": "medium"
            })

        for class_name in detector.dead_classes:
            issues.append({
                "type": "dead_code",
                "category": "unused_class",
                "message": f"Unused class: {class_name}",
                "severity": "medium"
            })

        for var_name in detector.dead_variables:
            issues.append({
                "type": "dead_code",
                "category": "unused_variable",
                "message": f"Unused variable: {var_name}",
                "severity": "low"
            })

        return {
            "file": file_path,
            "dead_code_issues": issues,
            "dead_imports": list(detector.dead_imports),
            "dead_functions": list(detector.dead_functions),
            "dead_classes": list(detector.dead_classes),
            "dead_variables": list(detector.dead_variables)
        }

    except Exception as e:
        logger.error(f"Dead code detection failed for {file_path}: {e}")
        return {"file": file_path, "error": str(e), "dead_code_issues": []}

def scan_project_for_dead_code(project_path: str) -> List[Dict]:
    """Scan entire project for dead code"""
    results = []
    project_path = Path(project_path)

    # Find all Python files
    python_files = list(project_path.rglob("*.py"))

    logger.info(f"Scanning {len(python_files)} Python files for dead code...")

    total_issues = 0
    for py_file in python_files:
        try:
            # Skip certain directories
            if any(skip_dir in str(py_file) for skip_dir in ["venv", "__pycache__", ".git", "node_modules"]):
                continue

            result = detect_dead_code_in_file(str(py_file))
            if result["dead_code_issues"]:
                results.append(result)
                total_issues += len(result["dead_code_issues"])

        except Exception as e:
            logger.error(f"Error processing {py_file}: {e}")

    logger.info(f"Dead code analysis complete: {total_issues} issues found across {len(results)} files")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        logger.info("Usage: python dead_code_detector.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    results = scan_project_for_dead_code(project_path)

    logger.info(f"\n🔍 Dead Code Analysis Results for {project_path}")
    logger.info("=" * 60)

    total_issues = sum(len(r["dead_code_issues"]) for r in results)
    logger.info(f"📊 Total Dead Code Issues: {total_issues}")

    if results:
        logger.info(f"📁 Files with Issues: {len(results)}")
        logger.info("\n📋 Detailed Results:")

        for result in results:
            if result["dead_code_issues"]:
                logger.info(f"\n📄 {result['file']}:")
                for issue in result["dead_code_issues"]:
                    logger.info(f"   ⚠️  {issue['category']}: {issue['message']} ({issue['severity']})")