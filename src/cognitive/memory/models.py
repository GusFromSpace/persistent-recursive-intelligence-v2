"""
Core data models for the Memory Intelligence Service

Defines the fundamental data structures used throughout the service.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import time


class IsolationLevel(Enum):
    """Memory namespace isolation levels"""
    ISOLATED = "isolated"
    SHARED = "shared"
    GLOBAL = "global"


class RelationType(Enum):
    """Types of relationships between memories"""
    SIMILAR = "similar"
    RELATED = "related" 
    RELATES_TO = "relates_to"
    DERIVED = "derived"
    SEQUENTIAL = "sequential"


class ResultFormat(Enum):
    """Result format options"""
    JSON = "json"
    TEXT = "text"
    SUMMARY = "summary"
    FULL = "full"


@dataclass
class TimeRange:
    """Time range for queries"""
    start: Optional[datetime] = None
    end: Optional[datetime] = None


@dataclass
class Aggregation:
    """Aggregation specification for queries"""
    field: str
    operation: str  # count, sum, avg, min, max
    group_by: Optional[str] = None


@dataclass
class QuotaConfig:
    """Quota configuration for namespaces"""
    max_memories: int = 10000
    max_storage_mb: int = 100
    max_requests_per_hour: int = 1000


@dataclass
class AccessConfig:
    """Access configuration for namespaces"""
    read_only: bool = False
    allowed_operations: List[str] = field(default_factory=lambda: ["store", "search", "delete"])
    ip_whitelist: Optional[List[str]] = None


@dataclass
class MemoryNamespace:
    """Isolated memory space for different applications/users"""
    namespace_id: str
    name: str = ""
    description: str = ""
    isolation_level: IsolationLevel = IsolationLevel.ISOLATED
    quota_limits: QuotaConfig = field(default_factory=QuotaConfig)
    access_patterns: AccessConfig = field(default_factory=AccessConfig)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryEntry:
    """Structured memory entry with metadata"""
    id: Optional[int] = None
    namespace: str = "default"
    content: str = ""
    timestamp: float = 0.0
    memory_type: str = "general"
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    vector_id: Optional[int] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


@dataclass
class MemoryRelationship:
    """Connections between memories"""
    id: Optional[int] = None
    source_id: int = 0
    target_id: int = 0
    relationship_type: RelationType = RelationType.RELATES_TO
    strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    namespace: str = "default"


@dataclass
class MemoryQuery:
    """Rich query interface for memory retrieval"""
    namespace: str = "default"
    semantic_query: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)
    time_range: Optional[TimeRange] = None
    similarity_threshold: float = 0.7
    limit: int = 10
    offset: int = 0
    aggregations: List[Aggregation] = field(default_factory=list)
    result_format: ResultFormat = ResultFormat.FULL
    include_relationships: bool = False
    include_metadata: bool = True


@dataclass
class MemorySearchResult:
    """Results from memory search operations"""
    memories: List[MemoryEntry]
    total_count: int
    query_time_ms: float
    similarity_scores: Optional[List[float]] = None
    relationships: Optional[List[MemoryRelationship]] = None
    aggregations: Optional[Dict[str, Any]] = None


@dataclass
class MemoryStats:
    """Statistics about memory usage"""
    namespace: str
    total_memories: int
    total_size_bytes: int
    average_relevance: float
    oldest_memory: Optional[datetime] = None
    newest_memory: Optional[datetime] = None
    memory_types: Dict[str, int] = field(default_factory=dict)
    tag_distribution: Dict[str, int] = field(default_factory=dict)


@dataclass
class HealthStatus:
    """Health status of the memory service"""
    status: str = "healthy"  # healthy, degraded, unhealthy
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    components: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    error_count: int = 0
    uptime_seconds: float = 0.0