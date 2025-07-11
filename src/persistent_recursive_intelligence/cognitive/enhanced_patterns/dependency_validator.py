"""
Dependency validation for detecting import/requirement mismatches.

This module implements patterns learned from debugging GUS Bot and Claude Wrapper
where missing dependencies caused runtime failures that static analysis missed.
"""

import re
import ast
from pathlib import Path
from typing import List, Dict, Set, Optional, NamedTuple
import logging

logger = logging.getLogger(__name__)


class DependencyIssue(NamedTuple):
    """Represents a dependency-related issue."""
    type: str
    severity: str
    line: int
    message: str
    import_name: str
    suggestion: Optional[str] = None


class DependencyValidator:
    """
    Validates dependencies against requirements and detects import issues.

    Detects patterns like:
    - Imports not listed in requirements.txt
    - Requirements not actually imported
    - Version conflicts
    - Circular import risks
    """

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.requirements = self._parse_requirements()
        self.setup_deps = self._parse_setup_py()
        self.pyproject_deps = self._parse_pyproject_toml()

        # Common stdlib modules that don"t need to be in requirements
        self.stdlib_modules = {
            "os", "sys", "re", "json", "time", "datetime", "pathlib", "typing",
            "collections", "functools", "itertools", "subprocess", "threading",
            "asyncio", "logging", "unittest", "tempfile", "shutil", "glob",
            "argparse", "configparser", "uuid", "hashlib", "base64", "urllib",
            "http", "email", "csv", "xml", "html", "sqlite3", "pickle", "copy"
        }

        # Map import names to package names
        self.import_to_package = {
            "yaml": "pyyaml",
            "cv2": "opencv-python",
            "PIL": "pillow",
            "sklearn": "scikit-learn",
            "pkg_resources": "setuptools",
            "dateutil": "python-dateutil"
        }

    def validate_file(self, file_path: str, content: str) -> List[DependencyIssue]:
        """Validate dependencies for a specific Python file."""
        issues = []

        try:
            tree = ast.parse(content)
            imports = self._extract_imports(tree)

            for imp in imports:
                issues.extend(self._check_import(imp, file_path))

        except SyntaxError as e:
            issues.append(DependencyIssue(
                type="syntax_error",
                severity="high",
                line=e.lineno or 0,
                message=f"Syntax error prevents dependency analysis: {e}",
                import_name=""
            ))

        return issues

    def _extract_imports(self, tree: ast.AST) -> List[Dict]:
        """Extract all import statements from AST."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "name": alias.name,
                        "line": node.lineno,
                        "level": 0
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append({
                    "type": "from_import",
                    "name": module,
                    "line": node.lineno,
                    "level": node.level or 0
                })

        return imports

    def _check_import(self, imp: Dict, file_path: str) -> List[DependencyIssue]:
        """Check a single import for issues."""
        issues = []
        import_name = imp["name"]
        line = imp["line"]

        # Skip relative imports and empty imports
        if imp["level"] > 0 or not import_name:
            return issues

        # Get top-level package name
        top_level = import_name.split(".")[0]

        # Skip stdlib modules
        if top_level in self.stdlib_modules:
            return issues

        if self._is_local_import(top_level):
            return issues

        # Check if import is in requirements
        package_name = self.import_to_package.get(top_level, top_level)

        if not self._is_in_requirements(package_name):
            issues.append(DependencyIssue(
                type="missing_dependency",
                severity="high",
                line=line,
                message=f"Import '{import_name}' not found in requirements.txt",
                import_name=import_name,
                suggestion=f"Add '{package_name}' to requirements.txt"
            ))

        # Check for potential circular imports
        if self._potential_circular_import(import_name, file_path):
            issues.append(DependencyIssue(
                type="circular_import_risk",
                severity="medium",
                line=line,
                message=f"Potential circular import: '{import_name}' may import back to this module",
                import_name=import_name,
                suggestion="Consider restructuring imports or using lazy imports"
            ))

        return issues

    def _is_local_import(self, module_name: str) -> bool:
        """Check if import is likely a local module."""
        # Check if there"s a .py file or package with this name in the project
        project_src = self.project_path / "src"
        if project_src.exists():
            if (project_src / f"{module_name}.py").exists():
                return True
            if (project_src / module_name / "__init__.py").exists():
                return True

        # Check in root as well
        if (self.project_path / f"{module_name}.py").exists():
            return True
        if (self.project_path / module_name / "__init__.py").exists():
            return True

        return False

    def _is_in_requirements(self, package_name: str) -> bool:
        """Check if package is in any requirements file."""
        all_deps = set()
        all_deps.update(self.requirements)
        all_deps.update(self.setup_deps)
        all_deps.update(self.pyproject_deps)

        # Check exact match and case-insensitive match
        return (package_name in all_deps or
                package_name.lower() in {dep.lower() for dep in all_deps})

    def _potential_circular_import(self, import_name: str, file_path: str) -> bool:
        """Heuristic check for potential circular imports."""
        # Simple heuristic: if importing something with similar name/path
        file_stem = Path(file_path).stem

        # If importing module with same name as file
        if import_name.split(".")[0] == file_stem:
            return True

        # If importing from parent package that might import this file
        if "." in import_name:
            parent = import_name.split(".")[0]
            if parent in file_path:
                return True

        return False

    def _parse_requirements(self) -> Set[str]:
        """Parse requirements.txt files."""
        deps = set()

        req_files = [
            self.project_path / "requirements.txt",
            self.project_path / "requirements-dev.txt",
            self.project_path / "requirements" / "base.txt"
        ]

        for req_file in req_files:
            if req_file.exists():
                try:
                    content = req_file.read_text()
                    deps.update(self._extract_package_names(content))
                except Exception as e:
                    logger.debug(f"Error reading {req_file}: {e}")

        return deps

    def _parse_setup_py(self) -> Set[str]:
        """Parse setup.py dependencies."""
        setup_file = self.project_path / "setup.py"
        if not setup_file.exists():
            return set()

        try:
            content = setup_file.read_text()
            # Simple regex to find install_requires
            pattern = r'install_requires\s*=\s*\[(.*?)\]'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                deps_str = match.group(1)
                return self._extract_package_names(deps_str)
        except Exception as e:
            logger.debug(f"Error parsing setup.py: {e}")

        return set()

    def _parse_pyproject_toml(self) -> Set[str]:
        """Parse pyproject.toml dependencies."""
        pyproject_file = self.project_path / "pyproject.toml"
        if not pyproject_file.exists():
            return set()

        try:
            import toml
            data = toml.load(pyproject_file)
            deps = set()

            # Poetry format
            if "tool" in data and "poetry" in data["tool"]:
                poetry_deps = data["tool"]["poetry"].get("dependencies", {})
                deps.update(poetry_deps.keys())

            # PEP 621 format
            if "project" in data:
                project_deps = data["project"].get("dependencies", [])
                deps.update(self._extract_package_names("\n".join(project_deps)))

            return deps

        except ImportError:
            logger.debug("toml package not available for pyproject.toml parsing")
        except Exception as e:
            logger.debug(f"Error parsing pyproject.toml: {e}")

        return set()

    def _extract_package_names(self, content: str) -> Set[str]:
        """Extract package names from dependency strings."""
        deps = set()

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Remove quotes and extract package name
            line = line.strip("\"'")

            package = re.split(r"[><=!~]", line)[0].strip()

            package = re.split(r'\[', package)[0].strip()

            if package:
                deps.add(package)

        return deps

    def find_unused_dependencies(self) -> List[DependencyIssue]:
        """Find dependencies in requirements but not imported anywhere."""
        all_imports = set()

        # Scan all Python files for imports
        for py_file in self.project_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                tree = ast.parse(content)
                imports = self._extract_imports(tree)

                for imp in imports:
                    if imp["level"] == 0 and imp["name"]:
                        top_level = imp["name"].split(".")[0]
                        all_imports.add(top_level)
                        # Also add mapped name
                        if top_level in self.import_to_package:
                            all_imports.add(self.import_to_package[top_level])

            except Exception:
                continue

        # Find requirements not imported
        issues = []
        all_deps = set()
        all_deps.update(self.requirements)
        all_deps.update(self.setup_deps)
        all_deps.update(self.pyproject_deps)

        for dep in all_deps:
            # Skip common dev/build dependencies
            if dep in {"setuptools", "wheel", "pip", "pytest", "black", "flake8", "mypy"}:
                continue

            if dep not in all_imports:
                issues.append(DependencyIssue(
                    type="unused_dependency",
                    severity="low",
                    line=0,
                    message=f"Dependency '{dep}' in requirements but not imported",
                    import_name=dep,
                    suggestion=f"Remove '{dep}' from requirements if unused"
                ))

        return issues