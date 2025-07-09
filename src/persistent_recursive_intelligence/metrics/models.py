from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """Health status enumeration for system monitoring"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class SystemType(str, Enum):
    """System type enumeration for categorizing metrics sources"""
    CODE_ANALYSIS = "code_analysis"
    TRADING_BOT = "trading_bot"
    AI_ANALYSIS = "ai_analysis"
    COGNITIVE_ENGINE = "cognitive_engine"
    MEMORY_INTELLIGENCE = "memory_intelligence"
    SAFETY_VALIDATOR = "safety_validator"
    RECURSIVE_IMPROVEMENT = "recursive_improvement"
    GENERIC = "generic"

class TradingMetrics(BaseModel):
    trades_executed: int = Field(ge=0, description="Number of trades executed")
    win_rate: float = Field(ge=0.0, le=1.0, description="Win rate as decimal (0.0-1.0)")
    profit_loss_pct: float = Field(description="Profit/loss percentage")
    drawdown_pct: float = Field(le=0.0, description="Maximum drawdown percentage (negative)")
    exposure_ratio: float = Field(ge=0.0, le=1.0, description="Current market exposure ratio")

class PerformanceMetrics(BaseModel):
    response_time_ms: float = Field(ge=0.0, description="Average response time in milliseconds")
    throughput_rps: float = Field(ge=0.0, description="Requests per second")
    error_rate: float = Field(ge=0.0, le=1.0, description="Error rate as decimal")
    uptime_pct: float = Field(ge=0.0, le=100.0, description="Uptime percentage")

class AnalysisMetrics(BaseModel):
    files_analyzed: int = Field(ge=0, description="Number of files analyzed")
    issues_found: int = Field(ge=0, description="Issues detected")
    complexity_score: float = Field(ge=0.0, description="Code complexity score")
    test_coverage_pct: float = Field(ge=0.0, le=100.0, description="Test coverage percentage")

class IntelligenceMetrics(BaseModel):
    memory_entries: int = Field(ge=0, description="Number of memory entries")
    recursive_cycles: int = Field(ge=0, description="Recursive improvement cycles")
    improvement_suggestions: int = Field(ge=0, description="Generated improvement suggestions")

class RiskMetrics(BaseModel):
    max_position_size_pct: float = Field(ge=0.0, le=100.0, description="Maximum position size percentage")
    exposure_ratio: float = Field(ge=0.0, le=1.0, description="Current exposure ratio")
    risk_score: Optional[float] = Field(ge=0.0, le=10.0, description="Risk assessment score")

class MetricsData(BaseModel):
    trading: Optional[TradingMetrics] = None
    performance: Optional[PerformanceMetrics] = None
    analysis: Optional[AnalysisMetrics] = None
    intelligence: Optional[IntelligenceMetrics] = None
    risk: Optional[RiskMetrics] = None
    custom: Optional[Dict[str, Any]] = Field(default=None, description="Custom metrics for extensibility")

class MetricsResponse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = Field(description="Source system identifier")
    system_type: SystemType = Field(default=SystemType.GENERIC)
    metrics: MetricsData
    health: HealthStatus = Field(default=HealthStatus.HEALTHY)
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class HealthCheckResponse(BaseModel):
    status: HealthStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    uptime_seconds: float
    version: str = "1.0.0"
    checks: Dict[str, bool] = Field(default_factory=dict, description="Individual health checks")

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)