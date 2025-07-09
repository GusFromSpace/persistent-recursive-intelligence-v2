#!/usr/bin/env python3
"""
Adversarial Test for Code Connector - Building Block Integration Challenge
Similar in spirit to orchestrator_synthesis_test.py but focused on connection generation

This test evaluates the Code Connector's ability to intelligently suggest connections
for a "box of building blocks" - orphaned files with no clear integration path.
"""

import json
import logging
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List, Dict

# Add the project root to the path for imports
current_dir = Path(__file__).parent
project_root = current_dir
sys.path.insert(0, str(project_root / "src"))

from cognitive.enhanced_patterns.code_connector import CodeConnectorAdversarialTest, suggest_code_connections
from cognitive.interactive_approval import ConnectionProposal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeConnectorAdversarialTest:
    """
    Test the Code Connector's ability to handle complex "building block" scenarios.
    
    This test creates realistic orphaned files that could legitimately be integrated
    into a main codebase, then evaluates the quality of connection suggestions.
    """

    def __init__(self):
        self.test_dir = None
        self.test_results = {
            "total_orphaned_files": 0,
            "suggestions_generated": 0,
            "high_quality_suggestions": 0,
            "false_positives": 0,
            "missed_opportunities": 0,
            "test_scenarios": []
        }

    def setup_test_environment(self) -> Path:
        """Create a realistic test project with orphaned files"""
        self.test_dir = Path(tempfile.mkdtemp(prefix="code_connector_test_"))
        
        # Create main project structure
        self._create_main_project_files()
        
        # Create orphaned "building block" files
        self._create_orphaned_files()
        
        logger.info(f"Created test environment in {self.test_dir}")
        return self.test_dir

    def _create_main_project_files(self):
        """Create a realistic main project with various integration opportunities"""
        
        # Main application entry point
        main_py = self.test_dir / "main.py"
        main_py.write_text('''#!/usr/bin/env python3
"""
Main application entry point
"""
import logging
from config import settings
from core.engine import ProcessingEngine
from utils.logger import setup_logging

def main():
    """Main application function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Add data validation
    # Implement caching layer
    # Add metrics collection
    
    engine = ProcessingEngine()
    
    try:
        engine.run()
    except Exception as e:
        logger.error(f"Application failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
''')

        # Core processing engine
        core_dir = self.test_dir / "core"
        core_dir.mkdir()
        (core_dir / "__init__.py").write_text("")
        
        engine_py = core_dir / "engine.py"
        engine_py.write_text('''"""
Core processing engine
"""
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ProcessingEngine:
    """Main processing engine for the application"""
    
    def __init__(self):
        self.processors = []
        self.cache = {}  # Simple in-memory cache
        
    def add_processor(self, processor):
        """Add a data processor"""
        self.processors.append(processor)
    
    def run(self):
        """Run the processing pipeline"""
        logger.info("Starting processing engine...")
        
        # Implement parallel processing
        # Add progress tracking
        # Implement retry logic
        
        for processor in self.processors:
            try:
                processor.process()
            except NotImplementedError:
                logger.warning(f"Processor {processor} not implemented")
        
        logger.info("Processing complete")
        
    def get_cache_stats(self):
        """Get cache statistics - STUB"""
        # This is a placeholder that could be enhanced
        return {"size": len(self.cache), "hits": 0, "misses": 0}
''')

        # Configuration module
        config_py = self.test_dir / "config.py"
        config_py.write_text('''"""
Application configuration
"""
import os

class Settings:
    """Application settings"""
    
    def __init__(self):
        # IMPROVED: self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
        
        # Add environment-specific configs
        # Add validation for required settings
        
    def validate(self):
        """Validate configuration - NOT IMPLEMENTED"""
        raise NotImplementedError("Configuration validation not implemented")

settings = Settings()
''')

        # Utilities directory
        utils_dir = self.test_dir / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        
        logger_py = utils_dir / "logger.py"
        logger_py.write_text('''"""
Logging utilities
"""
import logging
import sys

def setup_logging(level=logging.INFO):
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
def create_logger(name: str):
    """Create a logger with the given name"""
    return logging.getLogger(name)

# Add file logging
# Add log rotation
# Add structured logging (JSON)
''')

        # Data processing module
        data_dir = self.test_dir / "data"
        data_dir.mkdir()
        (data_dir / "__init__.py").write_text("")
        
        processor_py = data_dir / "processor.py"
        processor_py.write_text('''"""
Data processing utilities
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseProcessor(ABC):
    """Base class for data processors"""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process the input data"""
        pass

class TextProcessor(BaseProcessor):
    """Process text data"""
    
    def process(self, text: str) -> str:
        """Basic text processing"""
        # Add text cleaning
        # Add tokenization
        # Add encoding detection
        return text.strip().lower()

class DataValidator:
    """Validate input data - INCOMPLETE"""
    
    def validate_email(self, email: str) -> bool:
        """Validate email format - STUB"""
        # This needs proper implementation
        return "@" in email
        
    def validate_data_schema(self, data: Dict) -> bool:
        """Validate data against schema - NOT IMPLEMENTED"""
        raise NotImplementedError("Schema validation not implemented")
''')

    def _create_orphaned_files(self):
        """Create orphaned files that could be integrated into the main project"""
        
        # Orphaned file 1: Cache implementation that could be used by the engine
        cache_utils_py = self.test_dir / "cache_utils.py"
        cache_utils_py.write_text('''"""
Advanced caching utilities - ORPHANED FILE
"""
import time
from typing import Any, Dict, Optional
from functools import wraps

class AdvancedCache:
    """Advanced caching with TTL and eviction policies"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.cache = {}
        self.timestamps = {}
        self.access_counts = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache with TTL check"""
        if key not in self.cache:
            return None
            
        # Check TTL
        if time.time() - self.timestamps[key] > self.default_ttl:
            self.delete(key)
            return None
            
        self.access_counts[key] = self.access_counts.get(key, 0) + 1
        return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set item in cache with optional TTL"""
        if len(self.cache) >= self.max_size:
            self._evict_lru()
            
        self.cache[key] = value
        self.timestamps[key] = time.time()
        self.access_counts[key] = 0
        
    def delete(self, key: str):
        """Delete item from cache"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        self.access_counts.pop(key, None)
        
    def _evict_lru(self):
        """Evict least recently used item"""
        if not self.cache:
            return
            
        lru_key = min(self.access_counts.keys(), key=lambda k: self.access_counts[k])
        self.delete(lru_key)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": self._calculate_hit_rate(),
            "oldest_entry": min(self.timestamps.values()) if self.timestamps else None
        }
        
    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total_accesses = sum(self.access_counts.values())
        return total_accesses / len(self.cache) if self.cache else 0.0

def cached(ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func):
        cache = AdvancedCache(default_ttl=ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result)
                
            return result
        return wrapper
    return decorator
''')

        # Orphaned file 2: Data validation that could enhance the processor
        validation_py = self.test_dir / "validation.py"
        validation_py.write_text('''"""
Comprehensive data validation utilities - ORPHANED FILE
"""
import re
import json
from typing import Any, Dict, List, Optional, Union
from email.utils import parseaddr

class DataValidator:
    """Comprehensive data validation with detailed error reporting"""
    
    def __init__(self):
        self.errors = []
        
    def validate_email(self, email: str) -> bool:
        """Validate email format using RFC-compliant parsing"""
        if not email or not isinstance(email, str):
            self.errors.append(f"Email must be a non-empty string")
            return False
            
        parsed = parseaddr(email)
        if not parsed[1] or '@' not in parsed[1]:
            self.errors.append(f"Invalid email format: {email}")
            return False
            
        local, domain = parsed[1].split('@', 1)
        if not local or not domain:
            self.errors.append(f"Email missing local or domain part: {email}")
            return False
            
        # Basic domain validation
        if not re.match(r'^[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', domain):
            self.errors.append(f"Invalid domain format: {domain}")
            return False
            
        return True
        
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            self.errors.append("URL must be a non-empty string")
            return False
            
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
        if not url_pattern.match(url):
            self.errors.append(f"Invalid URL format: {url}")
            return False
            
        return True
        
    def validate_json_schema(self, data: Dict, schema: Dict) -> bool:
        """Validate data against a JSON schema"""
        try:
            return self._validate_schema_recursive(data, schema)
        except Exception as e:
            self.errors.append(f"Schema validation error: {e}")
            return False
            
    def _validate_schema_recursive(self, data: Any, schema: Dict) -> bool:
        """Recursively validate data against schema"""
        schema_type = schema.get('type')
        
        if schema_type == 'object':
            if not isinstance(data, dict):
                self.errors.append(f"Expected object, got {type(data).__name__}")
                return False
                
            required = schema.get('required', [])
            for field in required:
                if field not in data:
                    self.errors.append(f"Missing required field: {field}")
                    return False
                    
            properties = schema.get('properties', {})
            for field, value in data.items():
                if field in properties:
                    if not self._validate_schema_recursive(value, properties[field]):
                        return False
                        
        elif schema_type == 'string':
            if not isinstance(data, str):
                self.errors.append(f"Expected string, got {type(data).__name__}")
                return False
                
        elif schema_type == 'number':
            if not isinstance(data, (int, float)):
                self.errors.append(f"Expected number, got {type(data).__name__}")
                return False
                
        return True
        
    def validate_file_path(self, path: str) -> bool:
        """Validate file path format and existence"""
        if not path or not isinstance(path, str):
            self.errors.append("Path must be a non-empty string")
            return False
            
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in path for char in invalid_chars):
            self.errors.append(f"Path contains invalid characters: {path}")
            return False
            
        return True
        
    def get_errors(self) -> List[str]:
        """Get all validation errors"""
        return self.errors.copy()
        
    def clear_errors(self):
        """Clear all validation errors"""
        self.errors.clear()

def validate_config_data(config: Dict) -> tuple[bool, List[str]]:
    """Validate configuration data structure"""
    validator = DataValidator()
    
    schema = {
        'type': 'object',
        'required': ['database_url', 'log_level'],
        'properties': {
            'database_url': {'type': 'string'},
            'log_level': {'type': 'string'},
            'debug': {'type': 'string'}
        }
    }
    
    is_valid = validator.validate_json_schema(config, schema)
    return is_valid, validator.get_errors()
''')

        # Orphaned file 3: Metrics collection that could be used throughout the app
        metrics_py = self.test_dir / "metrics.py"
        metrics_py.write_text('''"""
Application metrics collection and reporting - ORPHANED FILE
"""
import time
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
from threading import Lock

class MetricsCollector:
    """Thread-safe metrics collection with various metric types"""
    
    def __init__(self, max_history: int = 1000):
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(lambda: deque(maxlen=max_history))
        self.timers = {}
        self.lock = Lock()
        
    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict] = None):
        """Increment a counter metric"""
        with self.lock:
            key = self._make_key(name, tags)
            self.counters[key] += value
            
    def set_gauge(self, name: str, value: float, tags: Optional[Dict] = None):
        """Set a gauge metric value"""
        with self.lock:
            key = self._make_key(name, tags)
            self.gauges[key] = value
            
    def record_histogram(self, name: str, value: float, tags: Optional[Dict] = None):
        """Record a value in a histogram"""
        with self.lock:
            key = self._make_key(name, tags)
            self.histograms[key].append({
                'value': value,
                'timestamp': time.time()
            })
            
    def start_timer(self, name: str, tags: Optional[Dict] = None) -> str:
        """Start a timer and return timer ID"""
        timer_id = f"{name}_{time.time()}_{id(self)}"
        key = self._make_key(name, tags)
        
        with self.lock:
            self.timers[timer_id] = {
                'key': key,
                'start_time': time.time()
            }
            
        return timer_id
        
    def stop_timer(self, timer_id: str):
        """Stop a timer and record the duration"""
        with self.lock:
            if timer_id in self.timers:
                timer_info = self.timers.pop(timer_id)
                duration = time.time() - timer_info['start_time']
                
                # Record as histogram
                if timer_info['key'] not in self.histograms:
                    self.histograms[timer_info['key']] = deque(maxlen=1000)
                    
                self.histograms[timer_info['key']].append({
                    'value': duration,
                    'timestamp': time.time()
                })
                
    def get_counter_value(self, name: str, tags: Optional[Dict] = None) -> int:
        """Get current counter value"""
        key = self._make_key(name, tags)
        return self.counters.get(key, 0)
        
    def get_gauge_value(self, name: str, tags: Optional[Dict] = None) -> Optional[float]:
        """Get current gauge value"""
        key = self._make_key(name, tags)
        return self.gauges.get(key)
        
    def get_histogram_stats(self, name: str, tags: Optional[Dict] = None) -> Dict[str, float]:
        """Get histogram statistics"""
        key = self._make_key(name, tags)
        values = [entry['value'] for entry in self.histograms.get(key, [])]
        
        if not values:
            return {}
            
        values.sort()
        count = len(values)
        
        return {
            'count': count,
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / count,
            'median': values[count // 2],
            'p95': values[int(count * 0.95)] if count > 0 else 0,
            'p99': values[int(count * 0.99)] if count > 0 else 0
        }
        
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics as a dictionary"""
        with self.lock:
            metrics = {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'histograms': {}
            }
            
            for key, _ in self.histograms.items():
                metrics['histograms'][key] = self.get_histogram_stats(key)
                
        return metrics
        
    def _make_key(self, name: str, tags: Optional[Dict] = None) -> str:
        """Create a metric key with tags"""
        if not tags:
            return name
            
        tag_str = ','.join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_str}]"

# Global metrics instance
metrics = MetricsCollector()

def timed(metric_name: str, tags: Optional[Dict] = None):
    """Decorator to time function execution"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            timer_id = metrics.start_timer(metric_name, tags)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                metrics.stop_timer(timer_id)
        return wrapper
    return decorator

def count_calls(metric_name: str, tags: Optional[Dict] = None):
    """Decorator to count function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            metrics.increment_counter(metric_name, 1, tags)
            return func(*args, **kwargs)
        return wrapper
    return decorator
''')

        # Orphaned file 4: Progress tracking that could be used in the engine
        progress_tracker_py = self.test_dir / "progress_tracker.py"
        progress_tracker_py.write_text('''"""
Progress tracking and reporting utilities - ORPHANED FILE
"""
import time
from typing import Optional, Callable, Any
from dataclasses import dataclass

@dataclass
class ProgressInfo:
    """Information about operation progress"""
    current: int
    total: int
    start_time: float
    elapsed_time: float
    estimated_total_time: Optional[float]
    estimated_remaining_time: Optional[float]
    rate: float
    percentage: float

class ProgressTracker:
    """Track and report progress of long-running operations"""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.update_callback: Optional[Callable] = None
        
    def update(self, increment: int = 1):
        """Update progress by increment"""
        self.current = min(self.current + increment, self.total)
        self.last_update_time = time.time()
        
        if self.update_callback:
            self.update_callback(self.get_progress_info())
            
    def set_progress(self, current: int):
        """Set absolute progress value"""
        self.current = min(max(current, 0), self.total)
        self.last_update_time = time.time()
        
        if self.update_callback:
            self.update_callback(self.get_progress_info())
            
    def get_progress_info(self) -> ProgressInfo:
        """Get detailed progress information"""
        elapsed = time.time() - self.start_time
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        rate = self.current / elapsed if elapsed > 0 else 0
        
        # Estimate remaining time
        estimated_total_time = None
        estimated_remaining_time = None
        
        if rate > 0 and self.current > 0:
            estimated_total_time = self.total / rate
            estimated_remaining_time = (self.total - self.current) / rate
            
        return ProgressInfo(
            current=self.current,
            total=self.total,
            start_time=self.start_time,
            elapsed_time=elapsed,
            estimated_total_time=estimated_total_time,
            estimated_remaining_time=estimated_remaining_time,
            rate=rate,
            percentage=percentage
        )
        
    def set_update_callback(self, callback: Callable[[ProgressInfo], None]):
        """Set callback for progress updates"""
        self.update_callback = callback
        
    def is_complete(self) -> bool:
        """Check if progress is complete"""
        return self.current >= self.total
        
    def format_progress(self) -> str:
        """Format progress as a human-readable string"""
        info = self.get_progress_info()
        
        bar_width = 40
        filled_width = int(bar_width * info.percentage / 100)
        bar = '█' * filled_width + '░' * (bar_width - filled_width)
        
        time_str = ""
        if info.estimated_remaining_time:
            remaining_mins = int(info.estimated_remaining_time / 60)
            remaining_secs = int(info.estimated_remaining_time % 60)
            time_str = f" ETA: {remaining_mins:02d}:{remaining_secs:02d}"
        
        return f"{self.description}: |{bar}| {info.current}/{info.total} ({info.percentage:.1f}%){time_str}"

def track_progress(iterable, description: str = "Processing", 
                  update_callback: Optional[Callable] = None):
    """Generator that tracks progress over an iterable"""
    total = len(iterable) if hasattr(iterable, '__len__') else None
    
    if total is None:
        # Convert to list to get length
        iterable = list(iterable)
        total = len(iterable)
        
    tracker = ProgressTracker(total, description)
    if update_callback:
        tracker.set_update_callback(update_callback)
    
    for item in iterable:
        yield item
        tracker.update(1)

class RetryWithProgress:
    """Retry operations with progress tracking"""
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay
        
    def execute(self, operation: Callable, *args, **kwargs) -> Any:
        """Execute operation with retries and progress tracking"""
        tracker = ProgressTracker(self.max_retries + 1, "Retry Operation")
        
        for attempt in range(self.max_retries + 1):
            try:
                tracker.update(1)
                return operation(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    raise e
                    
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {self.delay} seconds...")
                time.sleep(self.delay)
                
        return None
''')

    def run_test(self) -> Dict:
        """Run the comprehensive Code Connector test"""
        
        logger.info("🧪 Starting Code Connector Adversarial Test")
        
        # Set up test environment
        test_dir = self.setup_test_environment()
        
        try:
            # Identify orphaned files
            orphaned_files = [
                test_dir / "cache_utils.py",
                test_dir / "validation.py", 
                test_dir / "metrics.py",
                test_dir / "progress_tracker.py"
            ]
            
            # Identify main project files
            main_files = [
                test_dir / "main.py",
                test_dir / "core" / "engine.py",
                test_dir / "config.py",
                test_dir / "utils" / "logger.py",
                test_dir / "data" / "processor.py"
            ]
            
            # Run Code Connector analysis
            logger.info(f"🔍 Analyzing {len(orphaned_files)} orphaned files against {len(main_files)} main files")
            
            connector = CodeConnectorAdversarialTest(str(test_dir), confidence_threshold=0.3)
            suggestions = connector.analyze_orphaned_files(orphaned_files, main_files)
            
            # Evaluate results
            self.test_results["total_orphaned_files"] = len(orphaned_files)
            self.test_results["suggestions_generated"] = len(suggestions)
            
            # Analyze each suggestion
            for suggestion in suggestions:
                scenario_result = self._evaluate_suggestion(suggestion)
                self.test_results["test_scenarios"].append(scenario_result)
                
                if scenario_result["is_high_quality"]:
                    self.test_results["high_quality_suggestions"] += 1
                if scenario_result["is_false_positive"]:
                    self.test_results["false_positives"] += 1
            
            # Check for expected connections that might have been missed
            expected_connections = self._get_expected_connections()
            found_connections = {(s.orphaned_file, s.target_file) for s in suggestions}
            
            for expected in expected_connections:
                if expected not in found_connections:
                    self.test_results["missed_opportunities"] += 1
                    logger.warning(f"❌ Missed expected connection: {expected[0]} → {expected[1]}")
            
            # Calculate quality metrics
            self._calculate_quality_metrics()
            
            logger.info("✅ Code Connector Adversarial Test Complete")
            return self.test_results
            
        finally:
            # Clean up test environment
            if test_dir.exists():
                shutil.rmtree(test_dir)

    def _evaluate_suggestion(self, suggestion) -> Dict:
        """Evaluate the quality of a single connection suggestion"""
        
        scenario = {
            "orphaned_file": suggestion.orphaned_file,
            "target_file": suggestion.target_file,
            "connection_score": suggestion.connection_score,
            "connection_type": suggestion.connection_type,
            "is_high_quality": False,
            "is_false_positive": False,
            "evaluation_notes": []
        }
        
        # Define expected high-quality connections
        expected_high_quality = {
            ("cache_utils.py", "core/engine.py"): "AdvancedCache could replace simple cache in engine",
            ("validation.py", "data/processor.py"): "DataValidator could enhance validation in processor",
            ("validation.py", "config.py"): "validate_config_data could be used for settings validation",
            ("metrics.py", "main.py"): "MetricsCollector could be used for application metrics",
            ("metrics.py", "core/engine.py"): "Metrics decorators could track engine performance",
            ("progress_tracker.py", "core/engine.py"): "ProgressTracker could track processing progress"
        }
        
        connection_key = (suggestion.orphaned_file, suggestion.target_file)
        
        # Check if this is an expected high-quality connection
        if connection_key in expected_high_quality:
            scenario["is_high_quality"] = True
            scenario["evaluation_notes"].append(f"✅ {expected_high_quality[connection_key]}")
        
        # Check for false positives (nonsensical connections)
        false_positive_patterns = [
            # Connections that don't make semantic sense
            ("cache_utils.py", "utils/logger.py"),  # Cache utils doesn't fit with logging
            ("progress_tracker.py", "config.py"),   # Progress tracking doesn't fit with config
        ]
        
        if connection_key in false_positive_patterns:
            scenario["is_false_positive"] = True
            scenario["evaluation_notes"].append("❌ False positive - connection doesn't make semantic sense")
        
        # Evaluate connection quality based on score and reasoning
        if suggestion.connection_score > 0.7:
            scenario["evaluation_notes"].append(f"✅ High confidence score: {suggestion.connection_score:.3f}")
        elif suggestion.connection_score < 0.4:
            scenario["evaluation_notes"].append(f"⚠️ Low confidence score: {suggestion.connection_score:.3f}")
        
        # Check reasoning quality
        if suggestion.reasoning:
            for reason in suggestion.reasoning:
                if "semantic similarity" in reason.lower():
                    scenario["evaluation_notes"].append("✅ Good semantic analysis")
                if "todo" in reason.lower() or "notimplementederror" in reason.lower():
                    scenario["evaluation_notes"].append("✅ Detected integration opportunities")
        
        return scenario

    def _get_expected_connections(self) -> List[tuple]:
        """Get list of expected high-quality connections"""
        return [
            ("cache_utils.py", "core/engine.py"),
            ("validation.py", "data/processor.py"),
            ("validation.py", "config.py"),
            ("metrics.py", "core/engine.py"),
            ("progress_tracker.py", "core/engine.py")
        ]

    def _calculate_quality_metrics(self):
        """Calculate overall quality metrics for the test"""
        total_suggestions = self.test_results["suggestions_generated"]
        
        if total_suggestions > 0:
            self.test_results["precision"] = (self.test_results["high_quality_suggestions"] / total_suggestions)
            self.test_results["false_positive_rate"] = (self.test_results["false_positives"] / total_suggestions)
        else:
            self.test_results["precision"] = 0.0
            self.test_results["false_positive_rate"] = 0.0
        
        expected_connections = len(self._get_expected_connections())
        if expected_connections > 0:
            found_high_quality = self.test_results["high_quality_suggestions"]
            self.test_results["recall"] = found_high_quality / expected_connections
        else:
            self.test_results["recall"] = 0.0

    def cleanup(self):
        """Clean up test environment"""
        if self.test_dir and self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def analyze_orphaned_files(self, orphaned_files, main_files):
        pass


def main():
    """Run the Code Connector adversarial test"""
    
    test = CodeConnectorAdversarialTest()
    
    try:
        results = test.run_test()
        
        # Print detailed results
        print("\n" + "="*80)
        print("🧪 CODE CONNECTOR ADVERSARIAL TEST RESULTS")
        print("="*80)
        
        print(f"\n📊 SUMMARY METRICS:")
        print(f"   📁 Total Orphaned Files: {results['total_orphaned_files']}")
        print(f"   🔗 Suggestions Generated: {results['suggestions_generated']}")
        print(f"   ✅ High Quality Suggestions: {results['high_quality_suggestions']}")
        print(f"   ❌ False Positives: {results['false_positives']}")
        print(f"   ⏭️  Missed Opportunities: {results['missed_opportunities']}")
        
        print(f"\n📈 QUALITY METRICS:")
        print(f"   🎯 Precision: {results.get('precision', 0):.3f}")
        print(f"   📡 Recall: {results.get('recall', 0):.3f}")
        print(f"   ⚠️ False Positive Rate: {results.get('false_positive_rate', 0):.3f}")
        
        if results.get('precision', 0) > 0.7 and results.get('recall', 0) > 0.6:
            print(f"\n🎉 TEST RESULT: ✅ PASS - Code Connector shows strong performance")
        elif results.get('precision', 0) > 0.5 and results.get('recall', 0) > 0.4:
            print(f"\n🤔 TEST RESULT: ⚠️ MARGINAL - Code Connector shows acceptable performance")
        else:
            print(f"\n😞 TEST RESULT: ❌ FAIL - Code Connector needs improvement")
        
        print(f"\n📋 DETAILED SCENARIO RESULTS:")
        for i, scenario in enumerate(results['test_scenarios'], 1):
            print(f"\n   Scenario {i}: {scenario['orphaned_file']} → {scenario['target_file']}")
            print(f"      Score: {scenario['connection_score']:.3f} | Type: {scenario['connection_type']}")
            for note in scenario['evaluation_notes']:
                print(f"      {note}")
        
        # Save results to file
        with open(current_dir / "code_connector_test_results.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: code_connector_test_results.json")
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        raise
    finally:
        test.cleanup()


if __name__ == "__main__":
    main()