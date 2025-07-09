import time
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from .models import (
        MetricsResponse,
        HealthCheckResponse,
        ErrorResponse,
        HealthStatus,
        SystemType,
        MetricsData,
        TradingMetrics,
        PerformanceMetrics,
        AnalysisMetrics,
        IntelligenceMetrics
    )
    from ..config.settings import settings
    from ..utils.circuit_breaker import CircuitBreaker, CircuitBreakerError
except ImportError:
    from models import (
        MetricsResponse,
        HealthCheckResponse,
        ErrorResponse,
        HealthStatus,
        SystemType,
        MetricsData,
        TradingMetrics,
        PerformanceMetrics,
        AnalysisMetrics,
        IntelligenceMetrics
    )
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from config.settings import settings
    from utils.circuit_breaker import CircuitBreaker, CircuitBreaker

# Initialize FastAPI app
app = FastAPI(
    title="Metrics Baseline API",
    description="Standardized metrics collection and exposure system for GUS development projects",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins if hasattr(settings, 'allowed_origins') else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

import threading
app_start_time = time.time()
_request_count_lock = threading.Lock()
_error_count_lock = threading.Lock()
_request_count = 0
_error_count = 0

def increment_request_count():
    global _request_count
    with _request_count_lock:
        _request_count += 1

def increment_error_count():
    global _error_count
    with _error_count_lock:
        _error_count += 1

def get_request_count():
    with _request_count_lock:
        return _request_count

def get_error_count():
    with _error_count_lock:
        return _error_count

# Circuit breaker for external services
external_service_breaker = CircuitBreaker(
    failure_threshold=settings.circuit_breaker_threshold,
    timeout=settings.circuit_breaker_timeout
)

@app.middleware("http")
async def request_monitoring_middleware(request: Request, call_next):
    """Middleware for request monitoring and performance tracking"""
    start_time = time.time()
    increment_request_count()

    try:
        response = await call_next(request)

        # Track response time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        if response.status_code >= 400:
            increment_error_count()

        return response
    except Exception as e:
        increment_error_count()
        # Log the error for monitoring but don't expose internal details
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Request processing error: {str(e)}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="Internal Server Error",
                message="An internal error occurred" if settings.environment == "production" else str(e)
            ).dict()
        )

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint following GUS monitoring standards
    Returns system health status and key operational metrics
    """
    uptime = time.time() - app_start_time
    current_request_count = get_request_count()
    current_error_count = get_error_count()
    error_rate = current_error_count / max(current_request_count, 1)

    # Determine health status based on error rate and uptime
    if error_rate > 0.1:  # >10% error rate
        status = HealthStatus.UNHEALTHY
    elif error_rate > 0.05:  # >5% error rate
        status = HealthStatus.DEGRADED
    else:
        status = HealthStatus.HEALTHY

    checks = {
        "api_responsive": True,
        "error_rate_acceptable": error_rate <= 0.1,
        "circuit_breaker_closed": external_service_breaker.is_closed
    }

    return HealthCheckResponse(
        status=status,
        uptime_seconds=uptime,
        version=settings.version,
        checks=checks
    )

@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics(source: Optional[str] = None):
    """
    Get current metrics from the system

    Args:
        source: Optional source system filter

    Returns:
        Standardized metrics response
    """
    try:
        # For now, return mock data - in production this would collect from actual systems
        uptime = time.time() - app_start_time
        current_request_count = get_request_count()
        current_error_count = get_error_count()
        error_rate = current_error_count / max(current_request_count, 1)

        # Performance metrics are always available
        performance_metrics = PerformanceMetrics(
            response_time_ms=25.0,  # Mock value
            throughput_rps=current_request_count / max(uptime, 1),
            error_rate=error_rate,
            uptime_pct=(uptime / (uptime + 1)) * 100  # Simple uptime calculation
        )

        metrics_data = MetricsData(performance=performance_metrics)

        # Add system-specific metrics based on source
        if source == "gus_bot":
            metrics_data.trading = TradingMetrics(
                trades_executed=15,
                win_rate=0.73,
                profit_loss_pct=2.45,
                drawdown_pct=-0.85,
                exposure_ratio=0.45
            )
            system_type = SystemType.TRADING_BOT

        elif source == "persistent_recursive_intelligence":
            metrics_data.analysis = AnalysisMetrics(
                files_analyzed=247,
                issues_found=12,
                complexity_score=6.8,
                test_coverage_pct=85.2
            )
            metrics_data.intelligence = IntelligenceMetrics(
                memory_entries=1543,
                recursive_cycles=8,
                improvement_suggestions=23
            )
            system_type = SystemType.CODE_ANALYSIS
        else:
            system_type = SystemType.GENERIC

        # Determine health status
        health_status = HealthStatus.HEALTHY
        if error_rate > 0.1:
            health_status = HealthStatus.UNHEALTHY
        elif error_rate > 0.05:
            health_status = HealthStatus.DEGRADED

        return MetricsResponse(
            source=source or "metrics-baseline",
            system_type=system_type,
            metrics=metrics_data,
            health=health_status,
            metadata={
                "uptime_seconds": uptime,
                "total_requests": current_request_count,
                "total_errors": current_error_count,
                "environment": settings.environment
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to collect metrics: {str(e)}")

@app.get("/metrics/trading", response_model=MetricsResponse)
async def get_trading_metrics():
    """Get trading-specific metrics"""
    return await get_metrics(source="gus_bot")

@app.get("/metrics/analysis", response_model=MetricsResponse)
async def get_analysis_metrics():
    """Get code analysis metrics"""
    return await get_metrics(source="persistent_recursive_intelligence")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Metrics Baseline API",
        "version": settings.version,
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "trading": "/metrics/trading",
            "analysis": "/metrics/analysis",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        reload=settings.environment == "development"
    )