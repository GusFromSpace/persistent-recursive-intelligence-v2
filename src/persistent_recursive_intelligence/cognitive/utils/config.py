"""Configuration management for memory system"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DatabaseConfig:
    db_path: str = field(default_factory=lambda: os.path.join(os.getcwd(), "memory.db"))
    connection_timeout: int = 30
    pragma_settings: Dict[str, Any] = field(default_factory=lambda: {
        "journal_mode": "WAL",
        "cache_size": -64000,  # 64MB cache
        "synchronous": "NORMAL",
        "temp_store": "MEMORY"
    })

@dataclass
class MemoryConfig:
    vector_model: str = "all-MiniLM-L6-v2"
    faiss_index_type: str = "IndexFlatIP"
    embedding_cache_size: int = 1000

@dataclass
class PerformanceConfig:
    thread_pool_size: int = 4
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: int = 60

@dataclass
class Config:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)

_config = None

def get_config() -> Config:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config