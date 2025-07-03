#!/usr/bin/env python3
"""
Mesopredator Safe Workflow Manager - Executive Function Implementation

This module embodies the core executive function of Mesopredator"s dual awareness:
- Strategic decision-making with risk calculation before every action
- Copy-test-commit workflow represents strategic patience in practice
- Simultaneous hunter (opportunity detection) and hunted (threat scanning) modes
- Field shaping through environment protection and safe modification spaces

Generation 1.5: Current implementation provides basic dual awareness
Generation 2.0: Target for full cognitive integration with temporal intelligence
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import json
import re

# Import educational injection system
from educational_injector import (
    MesopredatorEducationalInjector,
    FixContext,
    AnnotationStyle,
    create_educational_fix_context
)

@dataclass
class SecurityScanResult:
    safe_files: List[Path]
    excluded_files: List[Path]
    sensitive_files: List[Path]
    large_files: List[Path]
    unclear_files: List[Path]
    total_size: int

@dataclass
class CognitiveAnalysis:
    """Mesopredator dual awareness analysis results"""
    hunter_findings: Dict[str, any]  # Opportunities detected
    hunted_findings: Dict[str, any]  # Threats detected
    executive_decision: str          # Action chosen
    strategic_patience_applied: bool # Whether timing optimization was used
    risk_calculation: float         # Risk/benefit ratio
    field_shaping_opportunities: List[str]  # Environmental improvements
    educational_annotations: List[str] = None  # Learning annotations injected

@dataclass
class WorkflowResult:
    success: bool
    test_directory: Path
    errors: List[str]
    warnings: List[str]
    changes_applied: int
    test_results: Dict[str, any]
    security_scan: Optional[SecurityScanResult] = None
    cognitive_analysis: Optional[CognitiveAnalysis] = None  # Gen 1.5 enhancement

class SafeWorkflowManager:
    """
    Mesopredator Executive Function - Generation 1.5

    Embodies strategic decision-making with dual awareness:
    - Hunter Mode: Scans for optimization opportunities and pattern extraction potential
    - Hunted Mode: Vigilant threat detection and boundary protection
    - Executive Function: Risk calculation before every action
    - Strategic Patience: Copy-test-commit represents optimal timing principles

    Future Gen 2.0: Full temporal intelligence and field shaping integration
    """

    # File extensions that are definitely safe for AI processing
    SAFE_EXTENSIONS = {'.py', '.js', '.html', '.css', '.txt', '.md', '.json'}

    # File extensions that contain sensitive data
    SENSITIVE_EXTENSIONS = {'.env', '.key', '.pem', '.p12', '.pfx'}

    # File patterns that often contain sensitive data
    SENSITIVE_PATTERNS = [
        r".*password.*", r".*secret.*", r".*token.*", r".*api[_-]?key.*",
        r".*private[_-]?key.*", r".*credential.*", r".*auth.*", r".*config.*",
        r".*\\.env.*", r".*\\.secret.*"
    ]

    # Directories that should always be excluded
    EXCLUDED_DIRECTORIES = [
        ".git", ".svn", ".hg", ".bzr",  # Version control
        "__pycache__", ".pytest_cache", "node_modules", ".cache",  # Cache directories
        ".venv", "venv", "env", "virtualenv",  # Virtual environments
        "build", "dist", "target", "bin", "obj",  # Build outputs
        ".idea", ".vscode", ".vs",  # IDE files
        "logs", "log",  # Log directories
        "tmp", "temp", "temporary",  # Temporary directories
        "backup", "backups",  # Backup directories
        "data", "database", "db",  # Data directories (potentially sensitive)
    ]

    # File patterns that should be excluded
    EXCLUDED_PATTERNS = [
        r".*\\.log$", r".*\\.sqlite$", r".*\\.db$", r".*\\.mdb$",  # Logs and databases
        r".*\\.dump$", r".*\\.sql$", r".*\\.backup$", r".*\\.bak$",  # Dumps and backups
        r".*\\.exe$", r".*\\.dll$", r".*\\.so$", r".*\\.dylib$",  # Binaries
        r".*\\.zip$", r".*\\.tar$", r".*\\.gz$", r".*\\.rar$", r".*\\.7z$",  # Archives
        r".*\\.jpg$", r".*\\.jpeg$", r".*\\.png$", r".*\\.gif$", r".*\\.bmp$",  # Images
        r".*\\.mp4$", r".*\\.avi$", r".*\\.mov$", r".*\\.wmv$",  # Videos
        r".*\\.mp3$", r".*\\.wav$", r".*\\.flac$",  # Audio
        r".*\\.pdf$", r".*\\.doc$", r".*\\.docx$", r".*\\.xls$", r".*\\.xlsx$",  # Documents
    ]

    def __init__(self, source_directory: Path, work_base_dir: Path = None, interactive: bool = True, max_file_size_mb: int = 10, enable_educational_injection: bool = True):
        self.source_directory = Path(source_directory)
        self.work_base_dir = work_base_dir or Path(tempfile.gettempdir()) / "ai-toolkit-safe-workflow"
        self.work_base_dir.mkdir(exist_ok=True)

        # Create timestamped working directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_directory = self.work_base_dir / f"test_{timestamp}"

        self.errors = []
        self.warnings = []
        self.interactive = interactive
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024

        # Track what we"ve excluded for reporting
        self.security_scan_result = None

        # Educational injection system - Generation 1.5 field shaping
        self.enable_educational_injection = enable_educational_injection
        if enable_educational_injection:
            self.educational_injector = MesopredatorEducationalInjector()
            self.injected_annotations = []

    def scan_for_security_issues(self) -> SecurityScanResult:
        """Scan source directory for security issues and large files"""
        safe_files = []
        excluded_files = []
        sensitive_files = []
        large_files = []
        unclear_files = []
        total_size = 0

        logger.info("🔍 Scanning for security issues and large files...")

        for root, dirs, files in os.walk(self.source_directory):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_DIRECTORIES]

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.source_directory)

                try:
                    file_size = file_path.stat().st_size
                    total_size += file_size

                    # Check if file is too large
                    if file_size > self.max_file_size_bytes:
                        large_files.append(relative_path)
                        continue

                    # Check if file should be excluded by pattern
                    if self._matches_excluded_patterns(file_path.name):
                        excluded_files.append(relative_path)
                        continue

                    # Check if file contains sensitive data
                    if self._is_sensitive_file(file_path):
                        sensitive_files.append(relative_path)
                        continue

                    # Check if file is definitely safe
                    if file_path.suffix.lower() in self.SAFE_EXTENSIONS:
                        safe_files.append(relative_path)
                        continue

                    # File is unclear - needs user decision
                    unclear_files.append(relative_path)

                except (OSError, PermissionError):
                    # Can"t access file, exclude it
                    excluded_files.append(relative_path)

        return SecurityScanResult(
            safe_files=safe_files,
            excluded_files=excluded_files,
            sensitive_files=sensitive_files,
            large_files=large_files,
            unclear_files=unclear_files,
            total_size=total_size
        )

    def _matches_excluded_patterns(self, filename: str) -> bool:
        """Check if filename matches excluded patterns"""
        return any(re.match(pattern, filename, re.IGNORECASE) for pattern in self.EXCLUDED_PATTERNS)

    def _is_sensitive_file(self, file_path: Path) -> bool:
        """Check if file potentially contains sensitive data"""
        # Check extension
        if file_path.suffix.lower() in self.SENSITIVE_EXTENSIONS:
            return True

        # Check filename patterns
        filename_lower = file_path.name.lower()
        return any(re.match(pattern, filename_lower, re.IGNORECASE) for pattern in self.SENSITIVE_PATTERNS)

    def _prompt_user_for_unclear_files(self, unclear_files: List[Path]) -> Tuple[List[Path], List[Path]]:
        """Prompt user to decide on unclear files"""
        if not self.interactive or not unclear_files:
            return [], unclear_files  # Default: exclude all unclear files

        logger.info(f"\n⚠️  Found {len(unclear_files)} files with unclear safety status:")
        logger.info("Please review each file to decide if it should be included in the AI analysis:")

        include_files = []
        exclude_files = []

        for file_path in unclear_files:
            logger.info(f"\n📁 File: {file_path}")

            # Show file info
            try:
                full_path = self.source_directory / file_path
                size = full_path.stat().st_size
                logger.info(f"   Size: {size:,} bytes")

                # Try to peek at content for text files
                if size < 1024:  # Only peek at small files
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            preview = f.read(200)
                            logger.info(f"   Preview: {preview[:100]}{'...' if len(preview) > 100 else ''}")
                    except UnicodeDecodeError:
                        logger.info("   Preview: [Binary file]")
                    except Exception:
                        logger.info("   Preview: [Cannot read]")
            except Exception:
                logger.info("   [Cannot access file info]")

            while True:
                choice = input("   Include in analysis? (y/n/s=skip all remaining): ").strip().lower()

                if choice == "y":
                    include_files.append(file_path)
                    break
                elif choice == "n":
                    exclude_files.append(file_path)
                    break
                elif choice == "s":
                    # Skip all remaining files
                    exclude_files.extend(unclear_files[unclear_files.index(file_path):])
                    return include_files, exclude_files
                else:
                    logger.info("   Please enter \"y\" for yes, \"n\" for no, or \"s\" to skip all remaining")

        return include_files, exclude_files

    def create_working_copy(self) -> bool:
        """Create a secure working copy of the source directory"""
        try:
            if self.test_directory.exists():
                shutil.rmtree(self.test_directory)

            # First, scan for security issues
            scan_result = self.scan_for_security_issues()
            self.security_scan_result = scan_result

            # Report findings
            logger.info(f"\n📊 Security scan results:")
            logger.info(f"   Safe files: {len(scan_result.safe_files)}")
            logger.info(f"   Excluded files: {len(scan_result.excluded_files)}")
            logger.info(f"   Sensitive files: {len(scan_result.sensitive_files)}")
            logger.info(f"   Large files: {len(scan_result.large_files)}")
            logger.info(f"   Unclear files: {len(scan_result.unclear_files)}")
            logger.info(f"   Total size: {scan_result.total_size / 1024 / 1024:.1f} MB")

            # Handle unclear files
            include_unclear, exclude_unclear = self._prompt_user_for_unclear_files(scan_result.unclear_files)

            # Combine all files to include
            files_to_include = set(scan_result.safe_files + include_unclear)

            # Create the filtered copy
            self.test_directory.mkdir(parents=True)

            copied_count = 0
            for file_path in files_to_include:
                source_file = self.source_directory / file_path
                dest_file = self.test_directory / file_path

                # Create parent directories
                dest_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy the file
                shutil.copy2(source_file, dest_file)
                copied_count += 1

            # Update scan result with final decisions
            scan_result.excluded_files.extend(exclude_unclear)
            scan_result.safe_files = list(files_to_include)
            scan_result.unclear_files = []

            logger.info(f"✅ Created secure working copy at: {self.test_directory}")
            logger.info(f"   Copied {copied_count} files")
            logger.info(f"   Excluded {len(scan_result.excluded_files) + len(scan_result.sensitive_files) + len(scan_result.large_files)} files for security")

            return True

        except Exception as e:
            self.errors.append(f"Failed to create working copy: {e}")
            return False

    def run_syntax_validation(self) -> Tuple[bool, List[str]]:
        """Run syntax validation on all Python files in the working copy"""
        errors = []
        python_files = list(self.test_directory.glob("**/*.py"))

        for py_file in python_files:
            try:
                with open(py_file, "r") as f:
                    content = f.read()

                # Try to compile
                compile(content, str(py_file), "exec")

            except SyntaxError as e:
                errors.append(f"Syntax error in {py_file.relative_to(self.test_directory)}: {e}")
            except Exception as e:
                errors.append(f"Error checking {py_file.relative_to(self.test_directory)}: {e}")

        return len(errors) == 0, errors

    def run_basic_import_test(self) -> Tuple[bool, List[str]]:
        """Test that main modules can be imported"""
        errors = []

        # Change to test directory for imports
        original_cwd = os.getcwd()
        os.chdir(self.test_directory)

        try:
            # Test main module imports
            import_tests = [
                "from core.orchestrator import MultiLanguageDiagnosticOrchestrator",
                "from core.plugin_manager import PluginManager",
                "from core.base_analyzer import BaseLanguageAnalyzer",
                "from analyzers.python_analyzer import PythonAnalyzer",
                "from analyzers.cpp_analyzer import CppAnalyzer"
            ]

            for import_test in import_tests:
                try:
                    exec(import_test)
                except Exception as e:
                    errors.append(f"Import failed: {import_test} -> {e}")

        finally:
            os.chdir(original_cwd)

        return len(errors) == 0, errors

    def apply_educational_fix(self, file_path: Path, pattern_name: str, old_code: str, new_code: str, fix_context: Dict = None) -> str:
        """
        Apply a fix with educational annotation injection

        Embodies field shaping principle - transform fixes into learning opportunities
        """
        if not self.enable_educational_injection:
            return new_code

        # Create fix context for educational injection
        fix_context_obj = create_educational_fix_context(
            pattern_name=pattern_name,
            old_code=old_code,
            new_code=new_code,
            language=self._detect_language(file_path),
            ai_generated=self._likely_ai_generated(old_code),
            severity=fix_context.get("severity", "medium") if fix_context else "medium",
            category=fix_context.get("category", "maintainability_problem") if fix_context else "maintainability_problem",
            complexity=self._assess_complexity(old_code, new_code)
        )

        file_context = {"line_count": self._count_lines(file_path)}

        if not self.educational_injector.should_inject_annotation(fix_context_obj, file_context):
            return new_code

        # Generate educational annotation
        annotation_style = self._choose_annotation_style(fix_context_obj, file_context)
        annotation = self.educational_injector.inject_learning_annotation(fix_context_obj, annotation_style)

        # Inject annotation before the fixed code
        annotated_code = f"{annotation}\n{new_code}"

        # Track annotation for reporting
        self.injected_annotations.append({
            "file": str(file_path),
            "pattern": pattern_name,
            "annotation": annotation,
            "timestamp": datetime.now().isoformat()
        })

        return annotated_code

    def inject_pattern_learning_comment(self, file_path: Path, line_number: int, pattern_info: Dict) -> bool:
        """
        Inject a learning comment at a specific location in a file

        Used for inserting educational content during automated fixes
        """
        if not self.enable_educational_injection:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Create educational annotation
            fix_context = create_educational_fix_context(
                pattern_name=pattern_info.get("pattern_name", "generic_improvement"),
                old_code=pattern_info.get("old_code", "// Original code"),
                new_code=pattern_info.get("new_code", "// Improved code"),
                language=self._detect_language(file_path),
                **pattern_info
            )

            annotation = self.educational_injector.inject_learning_annotation(
                fix_context,
                AnnotationStyle.STANDARD
            )

            # Insert annotation before the specified line
            annotation_lines = annotation.split('\n')
            for i, annotation_line in enumerate(reversed(annotation_lines)):
                lines.insert(line_number, annotation_line + "\n")

            # Write back to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            # Track injection
            self.injected_annotations.append({
                "file": str(file_path),
                "line": line_number,
                "pattern": pattern_info.get("pattern_name"),
                "type": "pattern_learning",
                "timestamp": datetime.now().isoformat()
            })

            return True

        except Exception as e:
            self.warnings.append(f"Failed to inject educational annotation in {file_path}: {e}")
            return False

    def generate_learning_report(self) -> Dict:
        """
        Generate report of educational annotations injected

        Provides metrics on field shaping effectiveness
        """
        if not self.enable_educational_injection or not self.injected_annotations:
            return {"educational_annotations": 0, "patterns_addressed": []}

        patterns_addressed = list(set(annotation["pattern"] for annotation in self.injected_annotations))

        report = {
            "educational_annotations": len(self.injected_annotations),
            "patterns_addressed": patterns_addressed,
            "files_enhanced": len(set(annotation["file"] for annotation in self.injected_annotations)),
            "annotation_details": self.injected_annotations,
            "field_shaping_metrics": {
                "learning_opportunities_created": len(self.injected_annotations),
                "pattern_diversity": len(patterns_addressed),
                "avg_annotations_per_file": len(self.injected_annotations) / max(1, len(set(annotation["file"] for annotation in self.injected_annotations)))
            }
        }

        return report

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            ".py": "python",
            ".cpp": "cpp", ".hpp": "cpp", ".cc": "cpp", ".cxx": "cpp", ".h": "cpp",
            ".js": "javascript", ".ts": "typescript",
            ".java": "java",
            ".rs": "rust",
            ".go": "go",
            ".rb": "ruby",
            ".php": "php"
        }
        return extension_map.get(file_path.suffix.lower(), "unknown")

    def _likely_ai_generated(self, code: str) -> bool:
        """
        Heuristically determine if code is likely AI-generated

        Looks for common AI patterns and indicators
        """
        ai_indicators = [
            "Implement",
            "placeholder",
            "example implementation",
            "sample code",
            "# Generated by",
            "// AI-generated",
            "def example_",
            "class Example",
            "function example"
        ]

        code_lower = code.lower()
        return any(indicator.lower() in code_lower for indicator in ai_indicators)

    def _assess_complexity(self, old_code: str, new_code: str) -> str:
        """Assess complexity of the fix for annotation style selection"""

        # Simple heuristics for complexity assessment
        old_lines = len(old_code.split("\n"))
        new_lines = len(new_code.split("\n"))

        # Large changes suggest complexity
        if abs(old_lines - new_lines) > 10:
            return "complex"

        # Security-related patterns are always complex
        security_keywords = ["eval", "exec", "subprocess", "shell=True", "sql", "query"]
        if any(keyword in old_code.lower() or keyword in new_code.lower() for keyword in security_keywords):
            return "complex"

        # Multiple function/class definitions suggest complexity
        if old_code.count("def ") + old_code.count("class ") > 2:
            return "complex"

        # Simple changes in short code blocks
        if old_lines <= 3 and new_lines <= 3:
            return "simple"

        return "medium"

    def _choose_annotation_style(self, fix_context: FixContext, file_context: Dict) -> AnnotationStyle:
        """
        Choose appropriate annotation style based on context

        Applies executive function - strategic decision about annotation depth
        """
        # Critical security issues get comprehensive annotations
        if fix_context.severity == "critical" and fix_context.category == "security":
            return AnnotationStyle.COMPREHENSIVE

        # Complex patterns in small files get detailed explanations
        if fix_context.complexity == "complex" and file_context.get("line_count", 0) < 200:
            return AnnotationStyle.DETAILED

        # Simple fixes in large files get concise annotations
        if fix_context.complexity == "simple" and file_context.get("line_count", 0) > 500:
            return AnnotationStyle.CONCISE

        # Default to standard annotation
        return AnnotationStyle.STANDARD

    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return len(f.readlines())
        except Exception as e:
            return 0

    def run_toolkit_analysis(self, mode: str = "analyze") -> Tuple[bool, str, str]:
        """Run the AI diagnostic toolkit on the working copy"""
        original_cwd = os.getcwd()
        os.chdir(self.test_directory)

        try:
            # Run the toolkit on itself
            cmd = ["python3", "ai_diagnostic_toolkit.py", f"--{mode}"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            return result.returncode == 0, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return False, "", "Toolkit execution timed out"
        except Exception as e:
            return False, "", f"Error running toolkit: {e}"
        finally:
            os.chdir(original_cwd)

    def run_comprehensive_tests(self) -> WorkflowResult:
        """Run comprehensive test suite on the working copy"""
        logger.info(f"🧪 Running comprehensive tests on working copy...")

        test_results = {
            "syntax_validation": {"passed": False, "errors": []},
            "import_test": {"passed": False, "errors": []},
            "toolkit_analysis": {"passed": False, "stdout": "", "stderr": ""},
            "self_modification_safety": {"passed": False, "changes_detected": 0}
        }

        # 1. Syntax validation
        logger.info("  📝 Running syntax validation...")
        syntax_ok, syntax_errors = self.run_syntax_validation()
        test_results["syntax_validation"] = {"passed": syntax_ok, "errors": syntax_errors}

        if not syntax_ok:
            self.errors.extend(syntax_errors)
            return WorkflowResult(
                success=False,
                test_directory=self.test_directory,
                errors=self.errors,
                warnings=self.warnings,
                changes_applied=0,
                test_results=test_results
            )

        # 2. Import test
        logger.info("  📦 Running import tests...")
        import_ok, import_errors = self.run_basic_import_test()
        test_results["import_test"] = {"passed": import_ok, "errors": import_errors}

        if not import_ok:
            self.errors.extend(import_errors)
            return WorkflowResult(
                success=False,
                test_directory=self.test_directory,
                errors=self.errors,
                warnings=self.warnings,
                changes_applied=0,
                test_results=test_results
            )

        # 3. Create backup snapshots before running toolkit
        backup_hashes = self._create_file_hashes()

        # 4. Run toolkit analysis
        logger.info("  🔍 Running toolkit analysis...")
        analysis_ok, stdout, stderr = self.run_toolkit_analysis("analyze")
        test_results["toolkit_analysis"] = {
            "passed": analysis_ok,
            "stdout": stdout,
            "stderr": stderr
        }

        # 5. Check for self-modification
        logger.info("  🛡️  Checking for self-modification...")
        after_hashes = self._create_file_hashes()
        changes_detected = self._compare_hashes(backup_hashes, after_hashes)
        test_results["self_modification_safety"] = {
            "passed": changes_detected == 0,
            "changes_detected": changes_detected
        }

        if changes_detected > 0:
            self.warnings.append(f"Toolkit modified {changes_detected} files during analysis")

        # Overall success determination
        success = all([
            syntax_ok,
            import_ok,
            analysis_ok,
            changes_detected == 0  # No self-modification during analysis
        ])

        return WorkflowResult(
            success=success,
            test_directory=self.test_directory,
            errors=self.errors,
            warnings=self.warnings,
            changes_applied=0,
            test_results=test_results,
            security_scan=self.security_scan_result
        )

    def apply_fixes_safely(self, max_iterations: int = 3) -> WorkflowResult:
        """Apply fixes safely with validation at each step"""
        logger.info(f"🔧 Applying fixes safely (max {max_iterations} iterations)...")

        total_changes = 0
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"  🔄 Iteration {iteration}/{max_iterations}")

            # Create snapshot before fixes
            before_hashes = self._create_file_hashes()

            # Run fixes
            fix_ok, stdout, stderr = self.run_toolkit_analysis("quick-fix")

            if not fix_ok:
                self.errors.append(f"Fix iteration {iteration} failed: {stderr}")
                break

            # Check what changed
            after_hashes = self._create_file_hashes()
            changes = self._compare_hashes(before_hashes, after_hashes)

            if changes == 0:
                logger.info(f"  ✅ No more changes in iteration {iteration}")
                break

            logger.info(f"  📊 {changes} files changed in iteration {iteration}")
            total_changes += changes

            # Validate syntax after fixes
            syntax_ok, syntax_errors = self.run_syntax_validation()
            if not syntax_ok:
                self.errors.append(f"Syntax errors introduced in iteration {iteration}")
                self.errors.extend(syntax_errors)
                break

            # Validate imports after fixes
            import_ok, import_errors = self.run_basic_import_test()
            if not import_ok:
                self.errors.append(f"Import errors introduced in iteration {iteration}")
                self.errors.extend(import_errors)
                break

        # Final comprehensive test
        final_result = self.run_comprehensive_tests()
        final_result.changes_applied = total_changes

        return final_result

    def commit_changes_to_source(self, test_result: WorkflowResult) -> bool:
        """Commit validated changes back to source directory"""
        if not test_result.success:
            logger.info("❌ Cannot commit - tests failed")
            return False

        logger.info("📤 Committing validated changes to source...")

        try:
            # Create backup of current source
            backup_dir = self.source_directory.parent / f"{self.source_directory.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S")}"
            shutil.copytree(self.source_directory, backup_dir)
            logger.info(f"📋 Created source backup at: {backup_dir}")

            # Copy validated changes
            for item in self.test_directory.iterdir():
                dest_item = self.source_directory / item.name

                if item.is_file():
                    shutil.copy2(item, dest_item)
                elif item.is_dir():
                    if dest_item.exists():
                        shutil.rmtree(dest_item)
                    shutil.copytree(item, dest_item)

            logger.info("✅ Changes committed successfully")
            return True

        except Exception as e:
            self.errors.append(f"Failed to commit changes: {e}")
            return False

    def cleanup_test_directory(self):
        """Clean up the test directory"""
        try:
            if self.test_directory.exists():
                shutil.rmtree(self.test_directory)
                logger.info(f"🧹 Cleaned up test directory: {self.test_directory}")
        except Exception as e:
            self.warnings.append(f"Failed to cleanup test directory: {e}")

    def _create_file_hashes(self) -> Dict[str, str]:
        """Create hash signatures of all files for change detection"""
        import hashlib

        hashes = {}
        for py_file in self.test_directory.glob("**/*.py"):
            try:
                content = py_file.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                relative_path = str(py_file.relative_to(self.test_directory))
                hashes[relative_path] = file_hash
            except Exception:
                pass  # Skip files that can"t be read

        return hashes

    def _compare_hashes(self, before: Dict[str, str], after: Dict[str, str]) -> int:
        """Compare hash dictionaries and return number of changes"""
        changes = 0

        # Check for modified files
        for file_path, hash_after in after.items():
            hash_before = before.get(file_path)
            if hash_before != hash_after:
                changes += 1

        # Check for new files
        new_files = set(after.keys()) - set(before.keys())
        changes += len(new_files)

        # Check for deleted files
        deleted_files = set(before.keys()) - set(after.keys())
        changes += len(deleted_files)

        return changes

def main():
    """Main interface for safe workflow manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Safe Workflow Manager for AI Diagnostic Toolkit")
    parser.add_argument("--source", type=str, default=".", help="Source directory")
    parser.add_argument("--test-only", action="store_true", help="Only test, don't commit")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply fixes during test")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max fix iterations")
    parser.add_argument("--non-interactive", action="store_true", help="Run without user prompts")
    parser.add_argument("--max-file-size", type=int, default=10, help="Max file size in MB")

    args = parser.parse_args()

    source_dir = Path(args.source).resolve()

    logger.info("🛡️  AI Diagnostic Toolkit - Safe Workflow Manager")
    logger.info("=" * 60)
    logger.info(f"Source directory: {source_dir}")

    workflow = SafeWorkflowManager(
        source_dir,
        interactive=not args.non_interactive,
        max_file_size_mb=args.max_file_size
    )

    # Create working copy
    if not workflow.create_working_copy():
        logger.info("❌ Failed to create working copy")
        return 1

    try:
        # Run tests
        if args.apply_fixes:
            result = workflow.apply_fixes_safely(args.max_iterations)
        else:
            result = workflow.run_comprehensive_tests()

        # Print results
        logger.info("\n📊 Test Results:")
        logger.info(f"  Success: {'✅' if result.success else '❌'}")
        logger.info(f"  Changes applied: {result.changes_applied}")
        logger.info(f"  Errors: {len(result.errors)}")
        logger.info(f"  Warnings: {len(result.warnings)}")

        if result.errors:
            logger.info("\n❌ Errors:")
            for error in result.errors:
                logger.info(f"  - {error}")

        if result.warnings:
            logger.info("\n⚠️  Warnings:")
            for warning in result.warnings:
                logger.info(f"  - {warning}")

        # Commit if successful and not test-only
        if result.success and not args.test_only:
            if workflow.commit_changes_to_source(result):
                logger.info("✅ Changes committed to source successfully!")
            else:
                logger.info("❌ Failed to commit changes")
                return 1
        elif not result.success:
            logger.info("❌ Tests failed - no changes committed")
            return 1
        else:
            logger.info("ℹ️  Test-only mode - no changes committed")

    finally:
        workflow.cleanup_test_directory()

    return 0

if __name__ == "__main__":
    exit(main())