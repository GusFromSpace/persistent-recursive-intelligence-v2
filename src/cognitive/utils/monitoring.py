"""Monitoring and metrics collection"""

import time
from contextlib import contextmanager
from typing import Dict, Any

class MetricsCollector:
    """Simple metrics collector for monitoring"""

    def __init__(self, name: str):
        self.name = name
        self.counters: Dict[str, int] = {}
        self.timers: Dict[str, float] = {}

    def increment(self, metric: str, value: int = 1):
        """Increment a counter metric"""
        self.counters[metric] = self.counters.get(metric, 0) + value

    @contextmanager
    def timer(self, metric: str):
        """Context manager for timing operations"""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            self.timers[metric] = self.timers.get(metric, 0) + duration

    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics stats"""
        return {
            "counters": self.counters.copy(),
            "timers": self.timers.copy()
        }

_collectors: Dict[str, MetricsCollector] = {}

def get_metrics_collector(name: str) -> MetricsCollector:
    """Get or create a metrics collector"""
    if name not in _collectors:
        _collectors[name] = MetricsCollector(name)
    return _collectors[name]