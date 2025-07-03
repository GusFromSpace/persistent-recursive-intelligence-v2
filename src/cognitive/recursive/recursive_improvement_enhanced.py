#!/usr/bin/env python3
"""
Memory-Enhanced Recursive Improvement Engine

Enhanced version of the PRI recursive improvement system with integrated
memory intelligence for pattern learning and cross-session improvement.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Add memory intelligence - USE LOCAL MEMORY SYSTEM
from ..memory.simple_memory import SimpleMemoryEngine

# Add enhanced pattern detection
try:
    from ..enhanced_patterns import EnhancedPatternDetector
    ENHANCED_PATTERNS_AVAILABLE = True
except ImportError as e:
    logging.debug(f"Enhanced patterns not available: {e}")
    ENHANCED_PATTERNS_AVAILABLE = False

# Decorators for memory integration - stubbed out as SimpleMemoryEngine doesn't need them
def remember_calls(namespace):
    """Decorator stub - functionality integrated into SimpleMemoryEngine"""
    def decorator(func):
        return func
    return decorator

def remember_errors(namespace):
    """Decorator stub - functionality integrated into SimpleMemoryEngine"""
    def decorator(func):
        return func
    return decorator

def remember_performance(namespace, operation):
    """Decorator stub - functionality integrated into SimpleMemoryEngine"""
    def decorator(func):
        return func
    return decorator

class MemoryEnhancedRecursiveImprovement:
    """
    Recursive improvement engine enhanced with persistent memory intelligence

    This version learns from every improvement iteration and accumulates
    knowledge across sessions for compound intelligence growth.
    """

    def __init__(self, source_directory: Path):
        self.source_directory = Path(source_directory)

        # Initialize memory intelligence - LOCAL SYSTEM
        self.memory = SimpleMemoryEngine(
            db_path="memory_intelligence.db", 
            namespace="recursive-improvement-engine"
        )
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize enhanced pattern detector if available
        self.enhanced_detector = None
        if ENHANCED_PATTERNS_AVAILABLE:
            try:
                self.enhanced_detector = EnhancedPatternDetector(str(source_directory))
                self.logger.info("Enhanced pattern detection enabled")
            except Exception as e:
                self.logger.warning(f"Could not initialize enhanced patterns: {e}")
        
        # Initialize performance pattern detector for multi-domain analysis
        try:
            from ..enhanced_patterns.performance_pattern_detector import PerformancePatternDetector
            self.performance_detector = PerformancePatternDetector()
            self.logger.info("Performance pattern detection enabled")
        except Exception as e:
            self.performance_detector = None
            self.logger.warning(f"Could not initialize performance detector: {e}")

        # Remember initialization
        self.memory.store_memory("Recursive improvement engine initialized", {
            "source_directory": str(source_directory),
            "session_id": datetime.now().isoformat(),
            "enhanced_patterns": ENHANCED_PATTERNS_AVAILABLE and self.enhanced_detector is not None
        })

        self.improvement_log = []
        self.iteration_count = 0
        self.cognitive_metrics = {
            "files_processed": 0,
            "improvements_found": 0,
            "patterns_learned": 0,
            "recursive_depth": 0,
            "enhanced_issues_found": 0
        }

    def analyze_code_file(self, file_path: Path):
        """Analyze a code file with memory-enhanced pattern recognition"""
        try:
            # Try multiple encodings to handle various file types
            content = None
            for encoding in ["utf-8", "latin-1", "cp1252", "ascii"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue

            if content is None:
                self.logger.warning(f"Could not decode file {file_path} with any encoding")
                return []

            # Remember analysis
            self.memory.store_memory(f"Analyzing file: {file_path.name}", {
                "file_path": str(file_path),
                "file_size": len(content),
                "analysis_type": "code_analysis"
            })

            # Check for known patterns from memory
            similar_analyses = self.memory.search_memories(f"analyzing {file_path.suffix}", limit=5)

            # Perform analysis with enhanced patterns if available
            base_issues = self._detect_issues(content, file_path)
            
            # Store file path for later multi-domain analysis
            if not hasattr(self, '_analyzed_files'):
                self._analyzed_files = []
            self._analyzed_files.append(file_path)
            enhanced_issues = []

            if self.enhanced_detector:
                try:
                    enhanced_issues = self.enhanced_detector.analyze_file(str(file_path), content)
                    self.cognitive_metrics["enhanced_issues_found"] += len(enhanced_issues)
                    self.logger.debug(f"Enhanced detector found {len(enhanced_issues)} additional issues")
                except Exception as e:
                    self.logger.debug(f"Enhanced detection failed for {file_path}: {e}")

            # Combine base and enhanced issues
            all_issues = base_issues + self._convert_enhanced_issues(enhanced_issues)

            # Learn from new patterns - store pattern data
            if all_issues:
                pattern_data = {
                    "file_type": file_path.suffix,
                    "analysis_date": datetime.now().isoformat(),
                    "patterns": [issue["description"] for issue in all_issues]
                }
                self.memory.store_memory(f"code_issues_{file_path.suffix}", pattern_data)

            # Remember analysis results
            self.memory.store_memory(f"Analysis complete: {file_path.name}", {
                "issues_found": len(all_issues),
                "base_issues": len(base_issues),
                "enhanced_issues": len(enhanced_issues),
                "file_type": file_path.suffix,
                "has_similar_analyses": len(similar_analyses) > 0
            })

            return all_issues

        except Exception as e:
            # Store error in memory
            self.memory.store_memory(f"Error analyzing {file_path.name}", {
                "file_path": str(file_path),
                "operation": "analyze_code_file",
                "error": str(e)
            })
            raise

    def _convert_enhanced_issues(self, enhanced_issues):
        """Convert enhanced detector issues to standard PRI format."""
        converted = []

        if not ENHANCED_PATTERNS_AVAILABLE:
            return converted

        for issue in enhanced_issues:
            converted.append({
                "type": issue.category,
                "line": issue.line,
                "severity": issue.severity,
                "description": f"[{issue.category.upper()}] {issue.message}",
                "learned_from_memory": False,
                "enhanced_pattern": True,
                "context": issue.context,
                "suggestion": issue.suggestion,
                "confidence": issue.confidence,
                "original_severity": issue.original_severity,
                "file_path": issue.file_path
            })

        return converted

    def _detect_issues(self, content: str, file_path: Path):
        """Detect issues with memory-enhanced pattern recognition - universal for any project"""
        issues = []

        # Get known issue patterns from memory
        known_patterns = self.memory.search_memories("code issues", limit=20)

        # Enhanced issue detection with memory-guided patterns
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            # 1. Maintenance comments
            if any(keyword in line_stripped for keyword in ["TODO", "FIXME", "XXX", "HACK", "BUG"]):
                issues.append({
                    "type": "maintenance",
                    "line": i + 1,
                    "severity": "medium",
                    "description": f"Maintenance comment: {line_stripped[:100]}",
                    "learned_from_memory": False,
                    "file_path": str(file_path)
                })

            elif line_stripped.startswith("print(") and not self._is_test_file(file_path):
                issues.append({
                    "type": "debugging",
                    "line": i + 1,
                    "severity": "low",
                    "description": f"Debug print statement in production code",
                    "learned_from_memory": False,
                    "file_path": str(file_path)
                })

            # 3. Wildcard imports
            elif "import *" in line_stripped and "from" in line_stripped:
                issues.append({
                    "type": "code_quality",
                    "line": i + 1,
                    "severity": "medium",
                    "description": f"Wildcard import: {line_stripped}",
                    "learned_from_memory": False,
                    "file_path": str(file_path)
                })

            # 4. Bare except clauses
            elif line_stripped == "except:" or "except:" in line_stripped:
                issues.append({
                    "type": "exception_handling",
                    "line": i + 1,
                    "severity": "high",
                    "description": f"Bare except clause catches all exceptions",
                    "learned_from_memory": False,
                    "file_path": str(file_path)
                })

            # 5. Potential security issues
            elif any(sec_pattern in line_lower for sec_pattern in ["password", "secret", "key", "token"]) and "=" in line_stripped and (""" in line_stripped or """ in line_stripped):
                if not any(safe_pattern in line_lower for safe_pattern in ["getenv", "environ", "config", "input"]):
                    issues.append({
                        "type": "security",
                        "line": i + 1,
                        "severity": "critical",
                        "description": f"Potential hardcoded credential",
                        "learned_from_memory": False,
                        "file_path": str(file_path)
                    })

            # 6. SQL injection risks
            elif any(sql_word in line_lower for sql_word in ["execute(", "cursor.execute", "query"]) and ("+" in line_stripped or "%" in line_stripped):
                issues.append({
                    "type": "security",
                    "line": i + 1,
                    "severity": "critical",
                    "description": f"Potential SQL injection vulnerability",
                    "learned_from_memory": False,
                    "file_path": str(file_path)
                })

            # 7. File operations without error handling
            elif any(file_op in line_stripped for file_op in ["open(", "with open("]) and i > 0:
                # Look for try block in surrounding lines
                context_start = max(0, i - 5)
                context_lines = lines[context_start:i+1]
                if not any("try:" in context_line for context_line in context_lines):
                    issues.append({
                        "type": "error_handling",
                        "line": i + 1,
                        "severity": "medium",
                        "description": f"File operation without error handling",
                        "learned_from_memory": False,
                        "file_path": str(file_path)
                    })

            # 8. Memory patterns from previous analyses
            for pattern in known_patterns:
                pattern_content = pattern.get("content", "").lower()
                if pattern_content and len(pattern_content) > 10 and pattern_content in line_lower:
                    issues.append({
                        "type": "memory_pattern",
                        "line": i + 1,
                        "severity": "medium",
                        "description": f"Known issue pattern from memory: {pattern_content[:50]}",
                        "learned_from_memory": True,
                        "file_path": str(file_path)
                    })
                    break

        return issues

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file"""
        return (file_path.name.startswith("test_") or
                "/test" in str(file_path) or
                "tests/" in str(file_path) or
                file_path.name.endswith("_test.py"))

    def run_improvement_iteration(self, max_depth: int = 3, batch_size: int = 50):
        """Run improvement iteration with batching for full project analysis"""
        self.iteration_count += 1

        self.memory.store_memory(f"Starting improvement iteration {self.iteration_count}", {
            "iteration": self.iteration_count,
            "max_depth": max_depth,
            "batch_size": batch_size,
            "session_type": "improvement_iteration"
        })

        try:
            # Get insights from previous iterations
            previous_iterations = self.memory.search_memories("improvement iteration", limit=10)

            if previous_iterations:
                avg_improvements = sum(
                    iter_data.get("metadata", {}).get("improvements_found", 0)
                    for iter_data in previous_iterations
                ) / len(previous_iterations)

                self.memory.store_memory(f"Historical context: avg {avg_improvements:.1f} improvements per iteration", {
                    "average_improvements": avg_improvements,
                    "iterations_analyzed": len(previous_iterations)
                })

            # Find ALL files to analyze
            target_files = self._find_target_files()

            # Process files in batches for full project coverage
            all_issues = []
            total_files = len(target_files)
            batches_processed = 0

            self.logger.info(f"Processing {total_files} files in batches of {batch_size}")

            for batch_start in range(0, total_files, batch_size):
                batch_end = min(batch_start + batch_size, total_files)
                batch_files = target_files[batch_start:batch_end]
                batches_processed += 1

                self.logger.info(f"Batch {batches_processed}: Processing files {batch_start+1}-{batch_end} of {total_files}")

                # Analyze files in current batch
                batch_issues = []
                for file_path in batch_files:
                    try:
                        issues = self.analyze_code_file(file_path)
                        batch_issues.extend(issues)
                        self.cognitive_metrics["files_processed"] += 1

                        # Progress indicator
                        if self.cognitive_metrics["files_processed"] % 10 == 0:
                            self.logger.info(f"Processed {self.cognitive_metrics["files_processed"]}/{total_files} files...")

                    except Exception as e:
                        self.logger.warning(f"Failed to analyze {file_path}: {e}")
                        continue

                all_issues.extend(batch_issues)

                # Store batch results in memory
                if batch_issues:
                    self.memory.store_memory(f"Batch {batches_processed} analysis complete", {
                        "batch_number": batches_processed,
                        "files_in_batch": len(batch_files),
                        "issues_found": len(batch_issues),
                        "total_progress": f"{batch_end}/{total_files}"
                    })

            # Learn improvement patterns from all batches
            if all_issues:
                improvement_patterns = [issue["description"] for issue in all_issues]
                self.memory.store_memory(f"iteration_{self.iteration_count}_improvements", {
                    "iteration": self.iteration_count,
                    "patterns": improvement_patterns,
                    "pattern_count": len(improvement_patterns)
                })
                self.cognitive_metrics["patterns_learned"] += 1

            # Perform multi-domain performance analysis
            if self.performance_detector and hasattr(self, '_analyzed_files'):
                try:
                    performance_issues = self.performance_detector.analyze_files(self._analyzed_files)
                    performance_summary = self.performance_detector.get_analysis_summary(performance_issues)
                    
                    # Convert performance issues to standard format
                    for perf_issue in performance_issues:
                        all_issues.append({
                            "type": perf_issue.issue_type,
                            "line": perf_issue.evidence.get("line", 1),
                            "severity": perf_issue.severity,
                            "description": perf_issue.description,
                            "learned_from_memory": False,
                            "file_path": perf_issue.evidence.get("file", "multi-domain"),
                            "domain": perf_issue.evidence.get("domain", "performance"),
                            "correlation": perf_issue.correlation
                        })
                    
                    # Store multi-domain analysis results
                    self.memory.store_memory(f"Multi-domain analysis iteration {self.iteration_count}", {
                        "domains_analyzed": performance_summary["domains_analyzed"],
                        "correlations_found": performance_summary["correlations_found"],
                        "multi_domain_synthesis": performance_summary["multi_domain_synthesis"],
                        "performance_issues": len(performance_issues)
                    })
                    
                    self.logger.info(f"Multi-domain analysis: {len(performance_issues)} performance issues, "
                                   f"{performance_summary['correlations_found']} correlations found")
                    
                except Exception as e:
                    self.logger.warning(f"Multi-domain analysis failed: {e}")

            self.cognitive_metrics["improvements_found"] = len(all_issues)

            # Remember complete iteration results
            self.memory.store_memory(f"Full project iteration {self.iteration_count} complete", {
                "improvements_found": len(all_issues),
                "files_processed": total_files,
                "batches_processed": batches_processed,
                "cognitive_metrics": self.cognitive_metrics.copy()
            })

            self.logger.info(f"Full project analysis complete: {total_files} files, {len(all_issues)} issues found")

            return {
                "iteration": self.iteration_count,
                "issues_found": all_issues,
                "files_processed": total_files,
                "batches_processed": batches_processed,
                "cognitive_growth": self.cognitive_metrics
            }

        except Exception as e:
            # Store error in memory
            self.memory.store_memory(f"Error in iteration {self.iteration_count}", {
                "iteration": self.iteration_count,
                "operation": "run_improvement_iteration",
                "error": str(e)
            })
            raise

    def _find_target_files(self):
        """Find target files for analysis - generic for any project"""
        # Find ALL Python files in the project
        all_python_files = list(self.source_directory.rglob("*.py"))

        # Filter out common directories that shouldn"t be analyzed
        excluded_patterns = [
            "venv/", "__pycache__/", ".git/", "build/", "dist/",
            "node_modules/", ".pytest_cache/", ".tox/", "env/",
            "virtualenv/", ".venv/", "site-packages/"
        ]

        target_files = []
        for file_path in all_python_files:
            # Skip if file is in excluded directory
            if any(pattern in str(file_path) for pattern in excluded_patterns):
                continue

            # Skip if file is too large (>1MB) to avoid overwhelming analysis
            try:
                if file_path.stat().st_size > 1024 * 1024:
                    self.logger.info(f"Skipping large file: {file_path.name} ({file_path.stat().st_size} bytes)")
                    continue
            except OSError:
                continue

            target_files.append(file_path)

        self.logger.info(f"Found {len(target_files)} Python files for analysis")
        return target_files

    def get_intelligence_insights(self):
        """Get insights from accumulated memory intelligence"""
        insights = {
            "total_iterations": self.iteration_count,
            "cognitive_metrics": self.cognitive_metrics,
            "recent_patterns": self.memory.search_memories("pattern", limit=10),
            "improvement_history": self.memory.search_memories("improvement iteration", limit=5),
            "error_patterns": self.memory.search_memories("error", limit=5),
            "performance_data": self.memory.search_memories("performance", limit=5)
        }

        return insights

    def export_intelligence(self):
        """Export all accumulated intelligence"""
        # Get all memories from this namespace
        all_memories = self.memory.search_memories("", limit=10000)  # Large limit to get all
        return {
            "namespace": self.memory.namespace,
            "total_memories": len(all_memories),
            "memories": all_memories,
            "health_status": self.memory.get_health_status()
        }

# Demonstration function
def demonstrate_memory_enhanced_improvement():
    """Demonstrate the memory-enhanced recursive improvement"""
    logging.info("🧠 Memory-Enhanced Recursive Improvement Demo")
    logging.info("=" * 45)

    # Initialize the enhanced engine
    source_dir = Path(__file__).parent.parent.parent
    engine = MemoryEnhancedRecursiveImprovement(source_dir)

    # Run improvement iteration
    results = engine.run_improvement_iteration()

    logging.info(f"\n📊 Improvement Results:")
    logging.info(f"   Issues found: {len(results["issues_found"])}")
    logging.info(f"   Files processed: {results["files_processed"]}")
    logging.info(f"   Cognitive growth: {results["cognitive_growth"]}")

    # Get intelligence insights
    insights = engine.get_intelligence_insights()
    logging.info(f"\n🧠 Intelligence Insights:")
    logging.info(f"   Total patterns learned: {len(insights["recent_patterns"])}")
    logging.info(f"   Historical iterations: {len(insights["improvement_history"])}")
    logging.info(f"   Error patterns tracked: {len(insights["error_patterns"])}")

    return engine

def main():
    """Command-line interface for PRI analysis of any project"""
    import argparse

    parser = argparse.ArgumentParser(description="Persistent Recursive Intelligence - Analyze any codebase")
    parser.add_argument("--project", required=True, help="Path to project directory to analyze")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum recursive depth (default: 3)")
    parser.add_argument("--batch-size", type=int, default=50, help="Files per batch for processing (default: 50)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    project_path = Path(args.project).resolve()

    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        return 1

    if not project_path.is_dir():
        print(f"❌ Project path is not a directory: {project_path}")
        return 1

    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print(f"🌀 Persistent Recursive Intelligence Analysis")
    print(f"=" * 50)
    print(f"Project: {project_path}")
    print(f"Max depth: {args.max_depth}")
    print(f"Batch size: {args.batch_size}")
    print()

    try:
        # Initialize engine
        engine = MemoryEnhancedRecursiveImprovement(project_path)

        # Run analysis with batching
        print("🔍 Running full project analysis...")
        results = engine.run_improvement_iteration(max_depth=args.max_depth, batch_size=args.batch_size)

        # Report results
        print(f"\n📊 Full Project Analysis Results:")
        print(f"   Files processed: {results["files_processed"]}")
        print(f"   Batches processed: {results["batches_processed"]}")
        print(f"   Issues found: {len(results["issues_found"])}")
        print(f"   Patterns learned: {results["cognitive_growth"]["patterns_learned"]}")

        # Group by severity
        issues = results["issues_found"]
        critical = [i for i in issues if i.get("severity") == "critical"]
        high = [i for i in issues if i.get("severity") == "high"]
        medium = [i for i in issues if i.get("severity") == "medium"]
        low = [i for i in issues if i.get("severity") == "low"]

        print(f"\n🔥 Issue Breakdown:")
        print(f"   Critical: {len(critical)}")
        print(f"   High: {len(high)}")
        print(f"   Medium: {len(medium)}")
        print(f"   Low: {len(low)}")

        # Show top critical/high issues
        priority_issues = critical + high
        if priority_issues:
            print(f"\n⚠️  Top Priority Issues:")
            for i, issue in enumerate(priority_issues[:10], 1):
                print(f"   {i}. {issue["type"].upper()} ({issue.get("severity", "unknown").upper()})")
                print(f"      Line {issue["line"]}: {issue["description"]}")
                if issue.get("learned_from_memory"):
                    print(f"      🧠 Pattern learned from memory")
                print()

        # Intelligence insights
        insights = engine.get_intelligence_insights()
        print(f"🧠 Intelligence Growth:")
        print(f"   Total iterations: {insights["total_iterations"]}")
        print(f"   Historical patterns: {len(insights["recent_patterns"])}")
        print(f"   Error patterns tracked: {len(insights["error_patterns"])}")

        print(f"\n✅ Analysis complete! Knowledge stored for future sessions.")
        return 0

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
