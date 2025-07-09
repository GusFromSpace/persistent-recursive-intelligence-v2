"""
Centralized Logging System for Persistent Recursive Intelligence
Replaces print statements with structured logging
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

class IntelligenceLogger:
    """
    Centralized logger for the persistent recursive intelligence system
    Provides structured logging with consistent formatting
    """

    _instance = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._initialized = None
        if not self._initialized:
            self._setup_logging()
            self._initialized = True

    def _setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Setup root logger
        self.logger = logging.getLogger("intelligence")
        self.logger.setLevel(logging.INFO)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler
        log_file = log_dir / f"intelligence_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        # IMPROVED: file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Prevent duplicate logs
        self.logger.propagate = False

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get a logger instance for a specific module"""
        if name:
            return logging.getLogger(f"intelligence.{name}")
        return self.logger

# Convenience functions for easy import
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance"""
    intelligence_logger = IntelligenceLogger()
    return intelligence_logger.get_logger(name)

def log_info(message: str, component: str = "system"):
    """Log info message"""
    logger = get_logger(component)
    logger.info(message)

def log_error(message: str, component: str = "system"):
    """Log error message"""
    logger = get_logger(component)
    logger.error(message)

def log_warning(message: str, component: str = "system"):
    """Log warning message"""
    logger = get_logger(component)
    logger.warning(message)

def log_debug(message: str, component: str = "system"):
    """Log debug message"""
    logger = get_logger(component)
    logger.debug(message)

def log_analysis_start(file_name: str, component: str = "analysis"):
    """Log start of file analysis"""
    logger = get_logger(component)
    logger.info(f"Starting analysis of {file_name}")

def log_analysis_complete(file_name: str, issues_found: int, component: str = "analysis"):
    """Log completion of file analysis"""
    logger = get_logger(component)
    logger.info(f"Completed analysis of {file_name}: {issues_found} issues found")

def log_memory_operation(operation: str, details: str, component: str = "memory"):
    """Log memory operations"""
    logger = get_logger(component)
    logger.info(f"Memory {operation}: {details}")

def log_pattern_learned(pattern_type: str, file_name: str, component: str = "learning"):
    """Log when a new pattern is learned"""
    logger = get_logger(component)
    logger.info(f"Learned pattern \"{pattern_type}\" from {file_name}")

def log_insight_generated(insight: str, component: str = "insights"):
    """Log when an insight is generated"""
    logger = get_logger(component)
    logger.info(f"Generated insight: {insight}")

def log_test_result(test_name: str, passed: bool, details: str = "", component: str = "testing"):
    """Log test results"""
    logger = get_logger(component)
    status = "PASSED" if passed else "FAILED"
    message = f'Test "{test_name}": {status}'
    if details:
        message += f" - {details}"
    logger.info(message)

def log_performance_metric(metric_name: str, value: float, unit: str = "", component: str = "performance"):
    """Log performance metrics"""
    logger = get_logger(component)
    logger.info(f'Performance metric "{metric_name}": {value}{unit}')

# Initialize logging system on import