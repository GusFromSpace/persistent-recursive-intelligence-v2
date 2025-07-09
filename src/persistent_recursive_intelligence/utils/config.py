"""
Standalone Configuration Management for Memory Intelligence Service

Environment-based configuration following the Harmonic Doctrine:
- Opt-in configuration with sensible defaults
- Environment-specific overrides
- Validation and type checking
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration"""
    db_path: str = "memory_intelligence.db"
    wal_mode: bool = True
    cache_size_mb: int = 1024
    connection_timeout: int = 30
    max_connections: int = 20
    backup_interval_hours: int = 24
    auto_vacuum: bool = True
    pragma_settings: Dict[str, Any] = field(default_factory=lambda: {
        "journal_mode": "WAL",
        "synchronous": "NORMAL",
        "cache_size": -1000000,  # 1GB cache
        "temp_store": "MEMORY",
        "mmap_size": 268435456,  # 256MB
    })


@dataclass
class MemoryConfig:
    """Memory system configuration"""
    recent_limit: int = 10
    relevance_limit: int = 20
    min_relevance_score: float = 0.1
    max_results: int = 100
    vector_model: str = "all-MiniLM-L6-v2"
    vector_dimension: int = 384
    faiss_index_type: str = "IndexFlatIP"
    memory_retention_hours: int = 168  # 1 week default
    auto_prune_interval_hours: int = 6
    similarity_threshold: float = 0.7
    max_content_length: int = 10000
    batch_size: int = 100


@dataclass
class ApiConfig:
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 4
    timeout_seconds: int = 30
    max_request_size_mb: int = 10
    cors_enabled: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    docs_enabled: bool = True
    metrics_enabled: bool = True


@dataclass
class SecurityConfig:
    """Security configuration"""
    enable_auth: bool = False
    api_key_required: bool = True
    jwt_secret_key: str = ""  # Must be set via JWT_SECRET_KEY environment variable
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    rate_limit_requests_per_minute: int = 100
    rate_limit_burst: int = 20
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])
    input_validation: bool = True
    max_namespace_length: int = 50
    max_query_length: int = 1000


@dataclass
class CacheConfig:
    """Cache configuration"""
    enabled: bool = True
    redis_url: str = "redis://localhost:6379"
    redis_db: int = 0
    ttl_seconds: int = 300
    max_connections: int = 10
    socket_timeout: int = 5
    health_check_interval: int = 30


@dataclass
class MonitoringConfig:
    """Monitoring and observability configuration"""
    metrics_enabled: bool = True
    health_check_interval: int = 30
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    export_metrics: bool = False
    prometheus_port: int = 9090
    alert_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "response_time_p95_ms": 100.0,
        "error_rate": 0.01,
        "memory_usage": 0.8,
        "cpu_usage": 0.7,
        "disk_usage": 0.8
    })


@dataclass
class PerformanceConfig:
    """Performance optimization configuration"""
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: int = 60
    bulkhead_max_concurrent: int = 50
    async_processing: bool = True
    thread_pool_size: int = 10
    vector_search_timeout: int = 5
    database_timeout: int = 10


class ConfigManager:
    """
    Centralized configuration manager for standalone memory service

    Follows the principle of "opt-in participation" - defaults work
    out of the box, but everything can be customized.
    """

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.getenv("CONFIG_FILE")
        self.logger = logging.getLogger(__name__)

        # Initialize configurations
        self.database = DatabaseConfig()
        self.memory = MemoryConfig()
        self.api = ApiConfig()
        self.security = SecurityConfig()
        self.cache = CacheConfig()
        self.monitoring = MonitoringConfig()
        self.performance = PerformanceConfig()

        # Load configurations
        self._load_from_environment()
        if self.config_file and Path(self.config_file).exists():
            self._load_from_file(self.config_file)

        self._validate_config()
        self._setup_logging()

    def _load_from_environment(self):
        """Load configuration from environment variables"""

        # Database configuration
        self.database.db_path = os.getenv("DATABASE_PATH", self.database.db_path)
        self.database.cache_size_mb = int(os.getenv("DB_CACHE_SIZE_MB", self.database.cache_size_mb))

        # Memory configuration
        self.memory.vector_model = os.getenv("VECTOR_MODEL", self.memory.vector_model)
        self.memory.max_results = int(os.getenv("MEMORY_MAX_RESULTS", self.memory.max_results))
        self.memory.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", self.memory.similarity_threshold))

        # API configuration
        self.api.host = os.getenv("API_HOST", self.api.host)
        self.api.port = int(os.getenv("API_PORT", self.api.port))
        self.api.workers = int(os.getenv("API_WORKERS", self.api.workers))

        # Security configuration
        self.security.enable_auth = os.getenv("ENABLE_AUTH", "false").lower() == "true"
        self.security.api_key_required = os.getenv("API_KEY_REQUIRED", "true").lower() == "true"
        self.security.jwt_secret_key = os.getenv("JWT_SECRET_KEY", self.security.jwt_secret_key)
        self.security.rate_limit_requests_per_minute = int(
            os.getenv("RATE_LIMIT_RPM", self.security.rate_limit_requests_per_minute)
        )

        # Cache configuration
        self.cache.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache.redis_url = os.getenv("REDIS_URL", self.cache.redis_url)

        # Monitoring configuration
        self.monitoring.log_level = os.getenv("LOG_LEVEL", self.monitoring.log_level)
        self.monitoring.metrics_enabled = os.getenv("METRICS_ENABLED", "true").lower() == "true"

        # Performance configuration
        self.performance.circuit_breaker_enabled = os.getenv("CIRCUIT_BREAKER", "true").lower() == "true"
        self.performance.thread_pool_size = int(os.getenv("THREAD_POOL_SIZE", self.performance.thread_pool_size))

    def _load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, "r") as f:
                config_data = json.load(f)

            # Update configurations from file
            for section, values in config_data.items():
                if hasattr(self, section):
                    config_obj = getattr(self, section)
                    for key, value in values.items():
                        if hasattr(config_obj, key):
                            setattr(config_obj, key, value)
                        else:
                            self.logger.warning(f"Unknown config key: {section}.{key}")
                else:
                    self.logger.warning(f"Unknown config section: {section}")

        except Exception as e:
            self.logger.error(f"Failed to load config file {config_file}: {e}")

    def _validate_config(self):
        """Validate configuration values"""
        errors = []

        # Database validation
        db_dir = Path(self.database.db_path).parent
        if not db_dir.exists():
            try:
                db_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create database directory: {e}")

        # Memory validation
        if self.memory.min_relevance_score < 0 or self.memory.min_relevance_score > 1:
            errors.append("Relevance score must be between 0 and 1")

        if self.memory.similarity_threshold < 0 or self.memory.similarity_threshold > 1:
            errors.append("Similarity threshold must be between 0 and 1")

        # API validation
        if self.api.port < 1 or self.api.port > 65535:
            errors.append("API port must be between 1 and 65535")

        # Security validation
        if self.security.rate_limit_requests_per_minute <= 0:
            errors.append("Rate limit must be positive")

        if self.security.enable_auth and (not self.security.jwt_secret_key or self.security.jwt_secret_key == "change-me-in-production"):
            errors.append("JWT secret key must be set via JWT_SECRET_KEY environment variable")

        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            raise ValueError(error_msg)

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.monitoring.log_level.upper()),
            format=self.monitoring.log_format
        )

    def export_config(self, file_path: str):
        """Export current configuration to file"""
        config_dict = {
            "database": self.database.__dict__,
            "memory": self.memory.__dict__,
            "api": self.api.__dict__,
            "security": self.security.__dict__,
            "cache": self.cache.__dict__,
            "monitoring": self.monitoring.__dict__,
            "performance": self.performance.__dict__
        }

        with open(file_path, "w") as f:
            json.dump(config_dict, f, indent=2)

        self.logger.info(f"Configuration exported to {file_path}")

    def reload_config(self):
        """Reload configuration from sources"""
        self.__init__(self.config_file)
        self.logger.info("Configuration reloaded")


# Global configuration instance
config = ConfigManager()


def get_config() -> ConfigManager:
    """Get the global configuration instance"""
    return config


def reload_config():
    """Reload the global configuration"""
    global config
    config.reload_config()