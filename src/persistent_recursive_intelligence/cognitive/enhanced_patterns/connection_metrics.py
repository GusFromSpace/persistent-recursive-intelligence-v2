#!/usr/bin/env python3
"""
Code Connector Metrics Collection System

Tracks performance metrics during connection analysis to provide evidence
of improvements and identify optimization opportunities.
"""

import json
import logging
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ConnectionMetrics:
    """Metrics for a single connection analysis run"""
    run_id: str
    timestamp: float
    project_path: str
    orphaned_files_count: int
    main_files_count: int
    total_suggestions: int
    processing_time_seconds: float
    
    # Quality metrics
    excellent_connections: int  # >0.8
    high_quality_connections: int  # 0.6-0.8
    medium_quality_connections: int  # 0.4-0.6
    low_quality_connections: int  # <0.4
    
    # Performance metrics
    avg_connection_score: float
    max_connection_score: float
    min_connection_score: float
    score_std_deviation: float
    
    # Processing metrics
    files_analyzed_per_second: float
    suggestions_per_orphaned_file: float
    high_value_percentage: float
    
    # Detailed breakdowns
    connection_type_distribution: Dict[str, int]
    reasoning_type_distribution: Dict[str, int]
    
    # Comparison with previous runs
    score_improvement: Optional[float] = None
    quality_improvement: Optional[float] = None


@dataclass
class ConnectionSuggestionMetrics:
    """Detailed metrics for individual connection suggestions"""
    orphaned_file: str
    target_file: str
    connection_score: float
    connection_type: str
    semantic_score: float
    structural_score: float
    dependency_score: float
    need_score: float
    processing_time_ms: float


class CodeConnectorMetricsCollector:
    """
    Collects and analyzes metrics during Code Connector runs.
    
    Provides real-time performance tracking and historical comparison.
    """
    
    def __init__(self, metrics_file: str = "code_connector_metrics.json"):
        self.metrics_file = Path(metrics_file)
        self.current_run_metrics: Optional[ConnectionMetrics] = None
        self.suggestion_metrics: List[ConnectionSuggestionMetrics] = []
        self.historical_metrics: List[ConnectionMetrics] = []
        
        # Load historical data
        self._load_historical_metrics()
        
        # Real-time tracking
        self.start_time: Optional[float] = None
        self.connection_scores: List[float] = []
        
    def start_run(self, run_id: str, project_path: str, orphaned_count: int, main_count: int):
        """Start tracking a new connection analysis run"""
        self.start_time = time.time()
        self.connection_scores = []
        self.suggestion_metrics = []
        
        logger.info(f"📊 Starting metrics collection for run: {run_id}")
        logger.info(f"   📁 Project: {project_path}")
        logger.info(f"   🔗 Analyzing {orphaned_count} orphaned files against {main_count} main files")
        
        # Initialize current run tracking
        self.current_run_metrics = ConnectionMetrics(
            run_id=run_id,
            timestamp=self.start_time,
            project_path=project_path,
            orphaned_files_count=orphaned_count,
            main_files_count=main_count,
            total_suggestions=0,
            processing_time_seconds=0.0,
            excellent_connections=0,
            high_quality_connections=0,
            medium_quality_connections=0,
            low_quality_connections=0,
            avg_connection_score=0.0,
            max_connection_score=0.0,
            min_connection_score=1.0,
            score_std_deviation=0.0,
            files_analyzed_per_second=0.0,
            suggestions_per_orphaned_file=0.0,
            high_value_percentage=0.0,
            connection_type_distribution={},
            reasoning_type_distribution={}
        )
        
    def record_suggestion(self, suggestion, processing_time_ms: float = 0.0):
        """Record metrics for a single connection suggestion"""
        if not self.current_run_metrics:
            return
            
        score = suggestion.connection_score
        self.connection_scores.append(score)
        
        # Record detailed suggestion metrics
        suggestion_metric = ConnectionSuggestionMetrics(
            orphaned_file=suggestion.orphaned_file,
            target_file=suggestion.target_file,
            connection_score=score,
            connection_type=suggestion.connection_type,
            semantic_score=0.0,  # Would be extracted from reasoning
            structural_score=0.0,
            dependency_score=0.0,
            need_score=0.0,
            processing_time_ms=processing_time_ms
        )
        
        self.suggestion_metrics.append(suggestion_metric)
        
        # Update connection type distribution
        conn_type = suggestion.connection_type
        if conn_type not in self.current_run_metrics.connection_type_distribution:
            self.current_run_metrics.connection_type_distribution[conn_type] = 0
        self.current_run_metrics.connection_type_distribution[conn_type] += 1
        
        # Update reasoning type distribution
        for reason in suggestion.reasoning:
            if "semantic" in reason.lower():
                self._increment_reasoning_count("semantic_analysis")
            if "structural" in reason.lower():
                self._increment_reasoning_count("structural_compatibility")
            if "dependency" in reason.lower():
                self._increment_reasoning_count("dependency_synergy")
            if "need" in reason.lower() or "todo" in reason.lower():
                self._increment_reasoning_count("need_detection")
        
        # Real-time quality tracking
        if score > 0.8:
            self.current_run_metrics.excellent_connections += 1
        elif score > 0.6:
            self.current_run_metrics.high_quality_connections += 1
        elif score > 0.4:
            self.current_run_metrics.medium_quality_connections += 1
        else:
            self.current_run_metrics.low_quality_connections += 1
    
    def finish_run(self, suggestions: List) -> ConnectionMetrics:
        """Complete the current run and calculate final metrics"""
        if not self.current_run_metrics or not self.start_time:
            raise ValueError("No run in progress")
        
        end_time = time.time()
        processing_time = end_time - self.start_time
        
        # Calculate final metrics
        self.current_run_metrics.total_suggestions = len(suggestions)
        self.current_run_metrics.processing_time_seconds = processing_time
        
        if self.connection_scores:
            self.current_run_metrics.avg_connection_score = sum(self.connection_scores) / len(self.connection_scores)
            self.current_run_metrics.max_connection_score = max(self.connection_scores)
            self.current_run_metrics.min_connection_score = min(self.connection_scores)
            
            # Calculate standard deviation
            avg = self.current_run_metrics.avg_connection_score
            variance = sum((score - avg) ** 2 for score in self.connection_scores) / len(self.connection_scores)
            self.current_run_metrics.score_std_deviation = variance ** 0.5
        
        # Calculate performance metrics
        total_files = self.current_run_metrics.orphaned_files_count + self.current_run_metrics.main_files_count
        self.current_run_metrics.files_analyzed_per_second = total_files / processing_time if processing_time > 0 else 0
        
        if self.current_run_metrics.orphaned_files_count > 0:
            self.current_run_metrics.suggestions_per_orphaned_file = (
                self.current_run_metrics.total_suggestions / self.current_run_metrics.orphaned_files_count
            )
        
        # Calculate high-value percentage
        high_value = (self.current_run_metrics.excellent_connections + 
                     self.current_run_metrics.high_quality_connections)
        if self.current_run_metrics.total_suggestions > 0:
            self.current_run_metrics.high_value_percentage = (
                high_value / self.current_run_metrics.total_suggestions * 100
            )
        
        # Compare with previous runs
        self._calculate_improvements()
        
        # Save metrics
        self.historical_metrics.append(self.current_run_metrics)
        self._save_metrics()
        
        # Log summary
        self._log_run_summary()
        
        completed_metrics = self.current_run_metrics
        self.current_run_metrics = None
        return completed_metrics
    
    def get_performance_trends(self, last_n_runs: int = 10) -> Dict[str, Any]:
        """Get performance trends over recent runs"""
        if len(self.historical_metrics) < 2:
            return {"status": "insufficient_data", "runs_count": len(self.historical_metrics)}
        
        recent_runs = self.historical_metrics[-last_n_runs:]
        
        # Calculate trends
        scores = [run.avg_connection_score for run in recent_runs]
        high_value_percentages = [run.high_value_percentage for run in recent_runs]
        processing_times = [run.processing_time_seconds for run in recent_runs]
        
        return {
            "runs_analyzed": len(recent_runs),
            "score_trend": {
                "current": scores[-1] if scores else 0,
                "previous": scores[-2] if len(scores) > 1 else 0,
                "improvement": scores[-1] - scores[-2] if len(scores) > 1 else 0,
                "average": sum(scores) / len(scores) if scores else 0
            },
            "quality_trend": {
                "current": high_value_percentages[-1] if high_value_percentages else 0,
                "previous": high_value_percentages[-2] if len(high_value_percentages) > 1 else 0,
                "improvement": (high_value_percentages[-1] - high_value_percentages[-2]) 
                             if len(high_value_percentages) > 1 else 0
            },
            "performance_trend": {
                "current_time": processing_times[-1] if processing_times else 0,
                "average_time": sum(processing_times) / len(processing_times) if processing_times else 0
            }
        }
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Get current run statistics in real-time"""
        if not self.current_run_metrics:
            return {"status": "no_run_active"}
        
        current_time = time.time()
        elapsed = current_time - self.start_time if self.start_time else 0
        
        return {
            "run_id": self.current_run_metrics.run_id,
            "elapsed_seconds": elapsed,
            "suggestions_so_far": len(self.connection_scores),
            "current_avg_score": sum(self.connection_scores) / len(self.connection_scores) if self.connection_scores else 0,
            "current_max_score": max(self.connection_scores) if self.connection_scores else 0,
            "excellent_count": self.current_run_metrics.excellent_connections,
            "high_quality_count": self.current_run_metrics.high_quality_connections,
            "suggestions_per_second": len(self.connection_scores) / elapsed if elapsed > 0 else 0
        }
    
    def _increment_reasoning_count(self, reasoning_type: str):
        """Helper to increment reasoning type counters"""
        if reasoning_type not in self.current_run_metrics.reasoning_type_distribution:
            self.current_run_metrics.reasoning_type_distribution[reasoning_type] = 0
        self.current_run_metrics.reasoning_type_distribution[reasoning_type] += 1
    
    def _calculate_improvements(self):
        """Calculate improvements compared to previous runs"""
        if len(self.historical_metrics) < 1:
            return
        
        previous_run = self.historical_metrics[-1]
        current_run = self.current_run_metrics
        
        # Score improvement
        current_run.score_improvement = (
            current_run.avg_connection_score - previous_run.avg_connection_score
        )
        
        # Quality improvement
        current_run.quality_improvement = (
            current_run.high_value_percentage - previous_run.high_value_percentage
        )
    
    def _load_historical_metrics(self):
        """Load historical metrics from file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    self.historical_metrics = [
                        ConnectionMetrics(**run_data) for run_data in data.get('runs', [])
                    ]
                logger.info(f"📊 Loaded {len(self.historical_metrics)} historical runs")
            except Exception as e:
                logger.warning(f"Could not load historical metrics: {e}")
                self.historical_metrics = []
    
    def _save_metrics(self):
        """Save current metrics to file"""
        try:
            data = {
                "metadata": {
                    "last_updated": time.time(),
                    "total_runs": len(self.historical_metrics)
                },
                "runs": [asdict(run) for run in self.historical_metrics]
            }
            
            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")
    
    def _log_run_summary(self):
        """Log a summary of the completed run"""
        metrics = self.current_run_metrics
        
        logger.info(f"📊 Run {metrics.run_id} completed:")
        logger.info(f"   ⏱️  Processing time: {metrics.processing_time_seconds:.2f}s")
        logger.info(f"   🔗 Total suggestions: {metrics.total_suggestions}")
        logger.info(f"   📈 Average score: {metrics.avg_connection_score:.3f}")
        logger.info(f"   🎯 Max score: {metrics.max_connection_score:.3f}")
        logger.info(f"   ✨ Excellent connections: {metrics.excellent_connections}")
        logger.info(f"   🟢 High-value percentage: {metrics.high_value_percentage:.1f}%")
        
        if metrics.score_improvement is not None:
            improvement_indicator = "📈" if metrics.score_improvement > 0 else "📉" if metrics.score_improvement < 0 else "➡️"
            logger.info(f"   {improvement_indicator} Score improvement: {metrics.score_improvement:+.3f}")
        
        if metrics.quality_improvement is not None:
            quality_indicator = "📈" if metrics.quality_improvement > 0 else "📉" if metrics.quality_improvement < 0 else "➡️"
            logger.info(f"   {quality_indicator} Quality improvement: {metrics.quality_improvement:+.1f}%")


# Global metrics collector instance
metrics_collector = CodeConnectorMetricsCollector()


def start_metrics_collection(run_id: str, project_path: str, orphaned_count: int, main_count: int):
    """Start collecting metrics for a Code Connector run"""
    metrics_collector.start_run(run_id, project_path, orphaned_count, main_count)


def record_suggestion_metrics(suggestion, processing_time_ms: float = 0.0):
    """Record metrics for a connection suggestion"""
    metrics_collector.record_suggestion(suggestion, processing_time_ms)


def finish_metrics_collection(suggestions: List) -> ConnectionMetrics:
    """Finish collecting metrics and return summary"""
    return metrics_collector.finish_run(suggestions)


def get_performance_trends(last_n_runs: int = 10) -> Dict[str, Any]:
    """Get performance trends over recent runs"""
    return metrics_collector.get_performance_trends(last_n_runs)


def get_real_time_stats() -> Dict[str, Any]:
    """Get real-time statistics for current run"""
    return metrics_collector.get_real_time_stats()


if __name__ == "__main__":
    # Demo the metrics system
    logger.info("📊 Code Connector Metrics System Demo")
    logger.info("=" * 50)
    
    # Simulate a run
    start_metrics_collection("demo_run", "/test/project", 3, 15)
    
    # Simulate some suggestions
    class MockSuggestion:
        def __init__(self, score, conn_type):
            self.connection_score = score
            self.connection_type = conn_type
            self.orphaned_file = "test.py"
            self.target_file = "main.py"
            self.reasoning = ["High semantic similarity", "Good structural compatibility"]
    
    suggestions = [
        MockSuggestion(0.95, "module_import"),
        MockSuggestion(0.78, "function_import"),
        MockSuggestion(0.65, "class_import"),
        MockSuggestion(0.42, "utility_import")
    ]
    
    for suggestion in suggestions:
        record_suggestion_metrics(suggestion, 150.0)
        stats = get_real_time_stats()
        logger.info(f"Real-time: {stats['suggestions_so_far']} suggestions, avg score: {stats['current_avg_score']:.3f}")
    
    # Finish and get summary
    final_metrics = finish_metrics_collection(suggestions)
    logger.info(f"\nFinal metrics: {final_metrics.high_value_percentage:.1f}% high-value suggestions")
    
    # Show trends
    trends = get_performance_trends()
    logger.info(f"Trends: {trends}")