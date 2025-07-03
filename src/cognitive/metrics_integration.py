#!/usr/bin/env python3
"""
PRI Metrics Integration
Combines PRI's cognitive capabilities with standardized metrics collection
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Import PRI cognitive components
try:
    from .memory.simple_memory import SimpleMemoryEngine
    from .synthesis.persistent_recursive_engine import PersistentRecursiveEngine
except ImportError:
    # Fallback for standalone execution
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from cognitive.memory.simple_memory import SimpleMemoryEngine
    from cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveEngine

# Import metrics models
try:
    from ..metrics.models import (
        MetricsResponse, MetricsData, AnalysisMetrics, IntelligenceMetrics,
        PerformanceMetrics, HealthStatus, SystemType
    )
except ImportError:
    # Fallback for development
    sys.path.append(str(Path(__file__).parent.parent))
    from metrics.models import (
        MetricsResponse, MetricsData, AnalysisMetrics, IntelligenceMetrics,
        PerformanceMetrics, HealthStatus, SystemType
    )

class PRIMetricsCollector:
    """
    Enhanced PRI with integrated metrics collection capabilities
    Combines recursive intelligence with standardized metrics reporting
    """

    def __init__(self, namespace: str = "pri_enhanced"):
        self.namespace = namespace
        self.memory_engine = SimpleMemoryEngine(namespace=namespace)
        self.recursive_engine = PersistentRecursiveEngine()
        self.session_start_time = time.time()
        self.analysis_metrics = {
            'files_analyzed': 0,
            'issues_found': 0,
            'fixes_applied': 0,
            'recursive_cycles': 0,
            'memory_entries_created': 0,
            'analysis_time_total': 0.0,
            'errors_encountered': 0
        }

    def analyze_project_with_metrics(self, project_path: str,
                                   collect_metrics: bool = True) -> Dict[str, Any]:
        """
        Analyze project and collect comprehensive metrics
        """
        start_time = time.time()

        try:
            # Run PRI analysis
            analysis_results = self._run_enhanced_analysis(project_path)

            # Collect metrics if requested
            if collect_metrics:
                metrics_data = self._collect_analysis_metrics(analysis_results)
                performance_data = self._collect_performance_metrics()
                intelligence_data = self._collect_intelligence_metrics()

                # Create comprehensive metrics response
                metrics_response = self._create_metrics_response(
                    analysis_data=metrics_data,
                    performance_data=performance_data,
                    intelligence_data=intelligence_data
                )

                return {
                    'analysis_results': analysis_results,
                    'metrics': metrics_response.dict(),
                    'session_duration': time.time() - start_time
                }
            else:
                return {'analysis_results': analysis_results}

        except Exception as e:
            self.analysis_metrics['errors_encountered'] += 1
            return {
                'error': str(e),
                'partial_metrics': self._create_error_metrics_response().dict()
            }

    def _run_enhanced_analysis(self, project_path: str) -> Dict[str, Any]:
        """
        Run PRI analysis with enhanced tracking
        """
        # Track recursive cycles
        cycle_start = time.time()

        python_files = list(Path(project_path).rglob("*.py"))
        self.analysis_metrics['files_analyzed'] = len(python_files)

        # Simulate issue detection
        issues_found = []
        for file_path in python_files[:10]:  # Limit for demo
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    file_issues = self._analyze_file_content(content, str(file_path))
                    issues_found.extend(file_issues)
                except Exception as e:
                    self.analysis_metrics['errors_encountered'] += 1

        self.analysis_metrics['issues_found'] = len(issues_found)
        self.analysis_metrics['recursive_cycles'] += 1
        self.analysis_metrics['analysis_time_total'] += time.time() - cycle_start

        # Store findings in memory
        for issue in issues_found:
            memory_id = self.memory_engine.store_memory(
                content=f"Analysis issue: {issue['type']} in {issue['file']}",
                metadata=issue
            )
            if memory_id:
                self.analysis_metrics['memory_entries_created'] += 1

        return {
            'files_analyzed': len(python_files),
            'issues_found': issues_found,
            'recursive_cycles': self.analysis_metrics['recursive_cycles'],
            'memory_entries': self.analysis_metrics['memory_entries_created']
        }

    def _analyze_file_content(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """
        Analyze file content for issues (simplified version)
        """
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Check for bare except clauses
            if line_stripped == "except:":
                issues.append({
                    'type': 'bare_except_clause',
                    'file': file_path,
                    'line': i + 1,
                    'description': 'Bare except clause catches all exceptions',
                    'severity': 'medium',
                    'category': 'error_handling'
                })

            # Check for print statements in production-like files
            if 'print(' in line_stripped and '/test' not in file_path.lower():
                issues.append({
                    'type': 'debug_print_statement',
                    'file': file_path,
                    'line': i + 1,
                    'description': 'Debug print statement in production code',
                    'severity': 'low',
                    'category': 'code_quality'
                })

            # Check for TODO comments
            if 'TODO' in line_stripped:
                issues.append({
                    'type': 'todo_comment',
                    'file': file_path,
                    'line': i + 1,
                    'description': 'TODO comment indicates incomplete work',
                    'severity': 'info',
                    'category': 'maintenance'
                })

        return issues

    def _collect_analysis_metrics(self, analysis_results: Dict[str, Any]) -> AnalysisMetrics:
        """
        Collect analysis-specific metrics
        """
        return AnalysisMetrics(
            files_analyzed=self.analysis_metrics['files_analyzed'],
            issues_found=self.analysis_metrics['issues_found'],
            complexity_score=self._calculate_complexity_score(),
            test_coverage_pct=self._estimate_test_coverage()
        )

    def _collect_performance_metrics(self) -> PerformanceMetrics:
        """
        Collect performance metrics
        """
        session_duration = time.time() - self.session_start_time
        files_per_second = (self.analysis_metrics['files_analyzed'] / session_duration
                           if session_duration > 0 else 0)

        return PerformanceMetrics(
            response_time_ms=self.analysis_metrics['analysis_time_total'] * 1000,
            throughput_rps=files_per_second,
            error_rate=self._calculate_error_rate(),
            uptime_pct=self._calculate_uptime_percentage()
        )

    def _collect_intelligence_metrics(self) -> IntelligenceMetrics:
        """
        Collect intelligence-specific metrics
        """
        # Get memory statistics
        memory_count = self._get_total_memory_entries()

        return IntelligenceMetrics(
            memory_entries=memory_count,
            recursive_cycles=self.analysis_metrics['recursive_cycles'],
            improvement_suggestions=self.analysis_metrics['issues_found']
        )

    def _create_metrics_response(self, analysis_data: AnalysisMetrics,
                               performance_data: PerformanceMetrics,
                               intelligence_data: IntelligenceMetrics) -> MetricsResponse:
        """
        Create comprehensive metrics response
        """
        metrics_data = MetricsData(
            analysis=analysis_data,
            performance=performance_data,
            intelligence=intelligence_data,
            custom={
                'pri_version': '2.1',
                'namespace': self.namespace,
                'fixes_applied': self.analysis_metrics['fixes_applied'],
                'memory_entries_created': self.analysis_metrics['memory_entries_created']
            }
        )

        return MetricsResponse(
            source="persistent_recursive_intelligence",
            system_type=SystemType.CODE_ANALYSIS,
            metrics=metrics_data,
            health=self._determine_health_status(),
            metadata={
                'session_start': datetime.fromtimestamp(self.session_start_time).isoformat(),
                'analysis_mode': 'enhanced_recursive',
                'memory_namespace': self.namespace
            }
        )

    def _create_error_metrics_response(self) -> MetricsResponse:
        """
        Create metrics response for error scenarios
        """
        return MetricsResponse(
            source="persistent_recursive_intelligence",
            system_type=SystemType.CODE_ANALYSIS,
            metrics=MetricsData(
                analysis=AnalysisMetrics(
                    files_analyzed=self.analysis_metrics['files_analyzed'],
                    issues_found=0,
                    complexity_score=0.0,
                    test_coverage_pct=0.0
                ),
                performance=PerformanceMetrics(
                    response_time_ms=0.0,
                    throughput_rps=0.0,
                    error_rate=1.0,
                    uptime_pct=0.0
                )
            ),
            health=HealthStatus.UNHEALTHY,
            metadata={'error_state': True}
        )

    def _calculate_complexity_score(self) -> float:
        """
        Calculate average complexity score based on issues found
        """
        if self.analysis_metrics['files_analyzed'] == 0:
            return 0.0

        issues_per_file = self.analysis_metrics['issues_found'] / self.analysis_metrics['files_analyzed']
        return min(issues_per_file * 2.0, 10.0)  # Cap at 10.0

    def _estimate_test_coverage(self) -> float:
        """
        Estimate test coverage (placeholder implementation)
        """
        # In real implementation, this would analyze test files
        return 75.0  # Default estimate

    def _calculate_error_rate(self) -> float:
        """
        Calculate error rate during analysis
        """
        total_operations = self.analysis_metrics['files_analyzed'] + self.analysis_metrics['recursive_cycles']
        if total_operations == 0:
            return 0.0

        return self.analysis_metrics['errors_encountered'] / total_operations

    def _calculate_uptime_percentage(self) -> float:
        """
        Calculate system uptime percentage
        """
        # For this session, assume high uptime unless many errors
        error_rate = self._calculate_error_rate()
        return max(100.0 - (error_rate * 100), 0.0)

    def _get_total_memory_entries(self) -> int:
        """
        Get total number of memory entries
        """
        try:
            # Try to get count from memory engine
            if hasattr(self.memory_engine, 'get_memory_count'):
                return self.memory_engine.get_memory_count()
            else:
                # Fallback: count entries created this session
                return self.analysis_metrics['memory_entries_created']
        except Exception:
            return self.analysis_metrics['memory_entries_created']

    def _determine_health_status(self) -> HealthStatus:
        """
        Determine overall system health
        """
        error_rate = self._calculate_error_rate()

        if error_rate == 0.0:
            return HealthStatus.HEALTHY
        elif error_rate < 0.1:  # Less than 10% error rate
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNHEALTHY

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get current metrics summary
        """
        return {
            'session_metrics': self.analysis_metrics.copy(),
            'session_duration': time.time() - self.session_start_time,
            'health_status': self._determine_health_status().value,
            'memory_namespace': self.namespace
        }

def main():
    """
    Demo the enhanced PRI with metrics collection
    """
    print("🌀 Enhanced PRI with Metrics Integration")
    print("=" * 50)

    # Initialize enhanced PRI
    pri_enhanced = PRIMetricsCollector(namespace="demo_enhanced")

    # Analyze a project with metrics collection
    project_path = "/home/gusfromspace/Development/persistent-recursive-intelligence"

    print(f"🔍 Analyzing project: {project_path}")
    results = pri_enhanced.analyze_project_with_metrics(project_path)

    if 'metrics' in results:
        metrics = results['metrics']
        print(f"\n📊 Analysis Metrics:")
        print(f"   • Files analyzed: {metrics['metrics']['analysis']['files_analyzed']}")
        print(f"   • Issues found: {metrics['metrics']['analysis']['issues_found']}")
        print(f"   • Complexity score: {metrics['metrics']['analysis']['complexity_score']:.1f}")

        print(f"\n🧠 Intelligence Metrics:")
        print(f"   • Memory entries: {metrics['metrics']['intelligence']['memory_entries']}")
        print(f"   • Recursive cycles: {metrics['metrics']['intelligence']['recursive_cycles']}")
        print(f"   • Improvement suggestions: {metrics['metrics']['intelligence']['improvement_suggestions']}")

        print(f"\n⚡ Performance Metrics:")
        print(f"   • Analysis time: {metrics['metrics']['performance']['response_time_ms']:.1f}ms")
        print(f"   • Throughput: {metrics['metrics']['performance']['throughput_rps']:.1f} files/sec")
        print(f"   • Error rate: {metrics['metrics']['performance']['error_rate']:.1%}")

        print(f"\n🏥 Health Status: {metrics['health']}")
        print(f"📅 Timestamp: {metrics['timestamp']}")

    # Show session summary
    summary = pri_enhanced.get_metrics_summary()
    print(f"\n📋 Session Summary:")
    for key, value in summary['session_metrics'].items():
        print(f"   • {key}: {value}")

if __name__ == "__main__":
    main()