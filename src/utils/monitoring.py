"""
Monitoring and Metrics Collection

Implements comprehensive observability following the Harmonic Doctrine
of making performance and health visible.
"""

import time
import threading
import psutil
from collections import defaultdict, deque
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging


@dataclass
class MetricPoint:
    """Single metric data point"""
    timestamp: float
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class TimerContext:
    """Context for timing operations"""
    start_time: float
    metric_name: str
    collector: "MetricsCollector"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.collector.record_timer(self.metric_name, duration)


class MetricsCollector:
    """
    Thread-safe metrics collection system

    Supports counters, gauges, histograms, and timers with
    automatic system metrics collection.
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(__name__)

        # Thread-safe storage
        self._lock = threading.RLock()

        # Metric storage
        self._counters: Dict[str, float] = defaultdict(float)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._timers: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))

        # System metrics
        self._system_metrics_enabled = True
        self._last_system_check = 0
        self._system_check_interval = 30  # seconds

    def increment(self, metric_name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            self._counters[full_name] += value

    def gauge(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric value"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            self._gauges[full_name] = value

    def histogram(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Add value to histogram metric"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            self._histograms[full_name].append(value)

            # Keep only recent values to prevent memory growth
            if len(self._histograms[full_name]) > 10000:
                self._histograms[full_name] = self._histograms[full_name][-5000:]

    def record_timer(self, metric_name: str, duration: float, labels: Optional[Dict[str, str]] = None):
        """Record timing measurement"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            self._timers[full_name].append(duration)

            # Also add to histogram for percentile calculations
            self.histogram(f"{metric_name}_duration", duration, labels)

    @contextmanager
    def timer(self, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """Context manager for timing operations"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.record_timer(metric_name, duration, labels)

    def _get_metric_name(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        """Generate full metric name with labels"""
        if not labels:
            return f"{self.service_name}_{name}"

        label_str = "_".join(f"{k}_{v}" for k, v in sorted(labels.items()))
        return f"{self.service_name}_{name}_{label_str}"

    def get_counter(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """Get counter value"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            return self._counters.get(full_name, 0.0)

    def get_gauge(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> Optional[float]:
        """Get gauge value"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            return self._gauges.get(full_name)

    def get_histogram_stats(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """Get histogram statistics"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            values = self._histograms.get(full_name, [])

            if not values:
                return {}

            sorted_values = sorted(values)
            count = len(sorted_values)

            return {
                "count": count,
                "min": sorted_values[0],
                "max": sorted_values[-1],
                "mean": sum(sorted_values) / count,
                "p50": sorted_values[int(count * 0.5)],
                "p90": sorted_values[int(count * 0.9)],
                "p95": sorted_values[int(count * 0.95)],
                "p99": sorted_values[int(count * 0.99)] if count >= 100 else sorted_values[-1]
            }

    def get_timer_stats(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        """Get timer statistics"""
        with self._lock:
            full_name = self._get_metric_name(metric_name, labels)
            values = list(self._timers.get(full_name, []))

            if not values:
                return {}

            return self.get_histogram_stats(f"{metric_name}_duration", labels)

    def collect_system_metrics(self):
        """Collect system performance metrics"""
        if not self._system_metrics_enabled:
            return

        current_time = time.time()
        if current_time - self._last_system_check < self._system_check_interval:
            return

        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=None)
            self.gauge("system_cpu_percent", cpu_percent)

            # Memory metrics
            memory = psutil.virtual_memory()
            self.gauge("system_memory_percent", memory.percent)
            self.gauge("system_memory_available_bytes", memory.available)
            self.gauge("system_memory_used_bytes", memory.used)

            # Disk metrics
            disk = psutil.disk_usage("/")
            self.gauge("system_disk_percent", (disk.used / disk.total) * 100)
            self.gauge("system_disk_free_bytes", disk.free)
            self.gauge("system_disk_used_bytes", disk.used)

            # Process metrics
            process = psutil.Process()
            self.gauge("process_memory_bytes", process.memory_info().rss)
            self.gauge("process_cpu_percent", process.cpu_percent())
            self.gauge("process_threads", process.num_threads())

            self._last_system_check = current_time

        except Exception as e:
            self.logger.warning(f"Failed to collect system metrics: {e}")

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics"""
        self.collect_system_metrics()

        with self._lock:
            metrics = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": self.service_name,
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {},
                "timers": {}
            }

            # Add histogram statistics
            for metric_name in self._histograms:
                base_name = metric_name.replace(f"{self.service_name}_", "")
                metrics["histograms"][base_name] = self.get_histogram_stats(base_name)

            # Add timer statistics
            for metric_name in self._timers:
                base_name = metric_name.replace(f"{self.service_name}_", "")
                metrics["timers"][base_name] = self.get_timer_stats(base_name)

            return metrics

    def reset(self):
        """Reset all metrics"""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._timers.clear()
            self.logger.info("All metrics reset")

    def health_summary(self) -> Dict[str, Any]:
        """Get health summary based on metrics"""
        self.collect_system_metrics()

        health = {
            "status": "healthy",
            "checks": []
        }

        # Check system resources
        cpu_percent = self.get_gauge("system_cpu_percent")
        if cpu_percent and cpu_percent > 90:
            health["status"] = "degraded"
            health["checks"].append(f"High CPU usage: {cpu_percent:.1f}%")

        memory_percent = self.get_gauge("system_memory_percent")
        if memory_percent and memory_percent > 90:
            health["status"] = "degraded"
            health["checks"].append(f"High memory usage: {memory_percent:.1f}%")

        disk_percent = self.get_gauge("system_disk_percent")
        if disk_percent and disk_percent > 90:
            health["status"] = "degraded"
            health["checks"].append(f"High disk usage: {disk_percent:.1f}%")

        # Check error rates
        error_count = self.get_counter("errors")
        request_count = self.get_counter("requests")
        if request_count and error_count:
            error_rate = error_count / request_count
            if error_rate > 0.05:  # 5% error rate threshold
                health["status"] = "degraded"
                health["checks"].append(f"High error rate: {error_rate:.2%}")

        if not health["checks"]:
            health["checks"] = ["All systems operational"]

        return health


# Global metrics collector instance
_global_collector = None


def get_metrics_collector(service_name: str = "memory_service") -> MetricsCollector:
    """Get or create global metrics collector"""
    global _global_collector
    if _global_collector is None:
        _global_collector = MetricsCollector(service_name)
    return _global_collector