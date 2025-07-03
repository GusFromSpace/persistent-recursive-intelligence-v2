"""
Pydantic models for REST API requests and responses
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class IsolationLevelAPI(str, Enum):
    """API enum for isolation levels"""
    ISOLATED = None


class RelationTypeAPI(str, Enum):
    """API enum for relationship types"""
    RELATES_TO = None


class ResultFormatAPI(str, Enum):
    """API enum for result formats"""
    FULL = None
    IDS_ONLY = None
    COMPACT = None


# Request Models
class StoreMemoryRequest(BaseModel):
    """Request to store a memory"""
    namespace: str = Field(default="default", max_length=50)
    content: str = Field(..., max_length=10000)
    memory_type: str = Field(default="general", max_length=50)
    relevance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)

    @validator("tags")
    def validate_tags(cls, v):
        if len(v) > 20:
            raise ValueError("Maximum 20 tags allowed")
        return v


class SearchMemoriesRequest(BaseModel):
    """Request to search memories"""
    namespace: str = Field(default="default", max_length=50)
    query: Optional[str] = Field(None, max_length=1000)
    filters: Dict[str, Any] = Field(default_factory=dict)
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    result_format: ResultFormatAPI = Field(default=ResultFormatAPI.FULL)
    include_relationships: bool = Field(default=False)
    include_metadata: bool = Field(default=True)


class CreateNamespaceRequest(BaseModel):
    """Request to create a namespace"""
    namespace_id: str = Field(..., max_length=50, regex=r"^[a-zA-Z0-9_-]+$")
    name: str = Field(..., max_length=100)
    description: str = Field(default="", max_length=500)
    isolation_level: IsolationLevelAPI = Field(default=IsolationLevelAPI.ISOLATED)
    max_memories: int = Field(default=10000, ge=1)
    max_storage_mb: int = Field(default=100, ge=1)
    max_requests_per_hour: int = Field(default=1000, ge=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CreateRelationshipRequest(BaseModel):
    """Request to create a memory relationship"""
    target_memory_id: int = Field(..., gt=0)
    relationship_type: RelationTypeAPI = Field(default=RelationTypeAPI.RELATES_TO)
    strength: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Response Models
class MemoryResponse(BaseModel):
    """Memory response model"""
    id: int
    namespace: str
    content: str
    timestamp: float
    memory_type: str
    relevance_score: float
    metadata: Dict[str, Any]
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class MemoryCompactResponse(BaseModel):
    """Compact memory response model"""
    id: int
    content: str
    relevance_score: float
    timestamp: float


class RelationshipResponse(BaseModel):
    """Relationship response model"""
    id: int
    source_id: int
    target_id: int
    relationship_type: str
    strength: float
    metadata: Dict[str, Any]
    created_at: datetime


class SearchResponse(BaseModel):
    """Search results response"""
    memories: List[MemoryResponse]
    total_count: int
    query_time_ms: float
    similarity_scores: Optional[List[float]] = None
    relationships: Optional[List[RelationshipResponse]] = None


class NamespaceResponse(BaseModel):
    """Namespace response model"""
    namespace_id: str
    name: str
    description: str
    isolation_level: str
    created_at: datetime
    updated_at: datetime
    memory_count: int
    storage_used_mb: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    components: Dict[str, Dict[str, Any]]
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    uptime_seconds: float


class MetricsResponse(BaseModel):
    """Metrics response"""
    timestamp: str
    service: str
    counters: Dict[str, float]
    gauges: Dict[str, float]
    histograms: Dict[str, Dict[str, float]]
    timers: Dict[str, Dict[str, float]]


class StoreResponse(BaseModel):
    """Response from storing a memory"""
    memory_id: int
    message: str = "Memory stored successfully"


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)