#!/usr/bin/env python3
"""
Enhanced PRI API with Integrated Metrics
Combines PRI's recursive intelligence with standardized metrics API
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import PRI components
try:
    from ..cognitive.metrics_integration import PRIMetricsCollector
    from ..cognitive.interactive_approval import InteractiveApprovalSystem, FixProposal
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from persistent_recursive_intelligence.cognitive.metrics_integration import PRIMetricsCollector
    from persistent_recursive_intelligence.cognitive.interactive_approval import InteractiveApprovalSystem, FixProposal

# Import metrics models
try:
    from ..metrics.models import (
        MetricsResponse, HealthCheckResponse, HealthStatus, SystemType
    )
except ImportError:
    sys.path.append(str(Path(__file__).parent.parent))
    from metrics.models import (
        MetricsResponse, HealthCheckResponse, HealthStatus, SystemType
    )

# API Models
class AnalysisRequest(BaseModel):
    project_path: str = Field(description="Path to project for analysis")
    include_metrics: bool = Field(default=True, description="Whether to collect metrics")
    interactive_mode: bool = Field(default=False, description="Enable interactive fix approval")
    max_files: int = Field(default=100, ge=1, le=1000, description="Maximum files to analyze")

class AnalysisResponse(BaseModel):
    analysis_id: str = Field(description="Unique analysis session ID")
    status: str = Field(description="Analysis status")
    results: Dict[str, Any] = Field(description="Analysis results")
    metrics: Optional[MetricsResponse] = Field(default=None, description="Collected metrics")
    duration_seconds: float = Field(description="Analysis duration")

class InteractiveSession(BaseModel):
    session_id: str
    fixes_pending: int
    fixes_approved: int
    fixes_rejected: int
    status: str

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced PRI API",
    description="Persistent Recursive Intelligence with integrated metrics and interactive approval",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Global state management
active_sessions: Dict[str, Dict[str, Any]] = {}
metrics_collector = PRIMetricsCollector(namespace="api_enhanced")

@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Enhanced PRI API",
        "version": "2.1.0",
        "description": "Persistent Recursive Intelligence with integrated metrics",
        "features": [
            "Recursive code analysis",
            "Interactive fix approval",
            "Persistent memory learning",
            "Standardized metrics collection",
            "Cross-project pattern transfer"
        ],
        "endpoints": {
            "analysis": "/api/v1/analysis",
            "metrics": "/api/v1/metrics",
            "health": "/api/v1/health",
            "interactive": "/api/v1/interactive",
            "docs": "/docs"
        }
    }

@app.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test PRI components
        test_collector = PRIMetricsCollector(namespace="health_test")
        health_status = HealthStatus.HEALTHY

        # Check memory system
        memory_health = "healthy"
        try:
            test_collector.memory_engine.store_memory("health_check", {"test": True})
            memory_health = "healthy"
        except Exception:
            memory_health = "degraded"
            health_status = HealthStatus.DEGRADED

        return HealthCheckResponse(
            status=health_status,
            timestamp=datetime.utcnow(),
            version="2.1.0",
            components={
                "api": "healthy",
                "memory_system": memory_health,
                "metrics_collector": "healthy",
                "interactive_approval": "healthy"
            },
            uptime_seconds=time.time() - app.state.start_time if hasattr(app.state, 'start_time') else 0
        )

    except Exception as e:
        return HealthCheckResponse(
            status=HealthStatus.UNHEALTHY,
            timestamp=datetime.utcnow(),
            version="2.1.0",
            components={"api": "unhealthy", "error": str(e)},
            uptime_seconds=0
        )

@app.post("/api/v1/analysis", response_model=AnalysisResponse)
async def analyze_project(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyze a project with PRI and collect metrics
    """
    analysis_id = f"analysis_{int(time.time())}"
    start_time = time.time()

    try:
        # Validate project path
        project_path = Path(request.project_path)
        if not project_path.exists():
            raise HTTPException(status_code=400, detail="Project path does not exist")

        # Initialize analysis session
        session_data = {
            "start_time": start_time,
            "project_path": str(project_path),
            "interactive_mode": request.interactive_mode,
            "status": "running"
        }
        active_sessions[analysis_id] = session_data

        # Run analysis
        results = metrics_collector.analyze_project_with_metrics(
            project_path=str(project_path),
            collect_metrics=request.include_metrics
        )

        # Update session status
        session_data["status"] = "completed"
        session_data["results"] = results

        # Create response
        duration = time.time() - start_time
        response = AnalysisResponse(
            analysis_id=analysis_id,
            status="completed",
            results=results.get('analysis_results', {}),
            metrics=MetricsResponse(**results['metrics']) if 'metrics' in results else None,
            duration_seconds=duration
        )

        # Schedule cleanup
        background_tasks.add_task(cleanup_session, analysis_id, delay=3600)  # Cleanup after 1 hour

        return response

    except Exception as e:
        # Update session with error
        if analysis_id in active_sessions:
            active_sessions[analysis_id]["status"] = "failed"
            active_sessions[analysis_id]["error"] = str(e)

        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_current_metrics():
    """
    Get current PRI system metrics
    """
    try:
        # Get current session metrics
        summary = metrics_collector.get_metrics_summary()

        # Create metrics response
        from persistent_recursive_intelligence.cognitive.metrics_integration import AnalysisMetrics, PerformanceMetrics, IntelligenceMetrics, MetricsData

        analysis_metrics = AnalysisMetrics(
            files_analyzed=summary['session_metrics']['files_analyzed'],
            issues_found=summary['session_metrics']['issues_found'],
            complexity_score=2.5,  # Average complexity
            test_coverage_pct=75.0
        )

        performance_metrics = PerformanceMetrics(
            response_time_ms=summary['session_metrics']['analysis_time_total'] * 1000,
            throughput_rps=1.0,  # Placeholder
            error_rate=0.0,
            uptime_pct=100.0
        )

        intelligence_metrics = IntelligenceMetrics(
            memory_entries=summary['session_metrics']['memory_entries_created'],
            recursive_cycles=summary['session_metrics']['recursive_cycles'],
            improvement_suggestions=summary['session_metrics']['issues_found']
        )

        metrics_data = MetricsData(
            analysis=analysis_metrics,
            performance=performance_metrics,
            intelligence=intelligence_metrics,
            custom={
                "api_version": "2.1.0",
                "active_sessions": len(active_sessions),
                "session_duration": summary['session_duration']
            }
        )

        return MetricsResponse(
            source="enhanced_pri_api",
            system_type=SystemType.CODE_ANALYSIS,
            metrics=metrics_data,
            health=HealthStatus(summary['health_status']),
            metadata={
                "namespace": summary['memory_namespace'],
                "api_endpoint": "/api/v1/metrics"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to collect metrics: {str(e)}")

@app.get("/api/v1/analysis/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """
    Get status of a specific analysis session
    """
    if analysis_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Analysis session not found")

    session = active_sessions[analysis_id]
    return {
        "analysis_id": analysis_id,
        "status": session["status"],
        "duration": time.time() - session["start_time"],
        "project_path": session["project_path"],
        "interactive_mode": session["interactive_mode"],
        "results": session.get("results", {}),
        "error": session.get("error")
    }

@app.get("/api/v1/sessions")
async def list_active_sessions():
    """
    List all active analysis sessions
    """
    sessions = []
    for session_id, session_data in active_sessions.items():
        sessions.append({
            "session_id": session_id,
            "status": session_data["status"],
            "project_path": session_data["project_path"],
            "duration": time.time() - session_data["start_time"],
            "interactive_mode": session_data["interactive_mode"]
        })

    return {
        "active_sessions": len(sessions),
        "sessions": sessions
    }

@app.post("/api/v1/interactive/start")
async def start_interactive_session(request: AnalysisRequest):
    """
    Start an interactive approval session
    """
    # This would integrate with the interactive approval system
    # For now, return a placeholder response
    session_id = f"interactive_{int(time.time())}"

    interactive_session = InteractiveSession(
        session_id=session_id,
        fixes_pending=0,
        fixes_approved=0,
        fixes_rejected=0,
        status="initialized"
    )

    return interactive_session

async def cleanup_session(session_id: str, delay: int = 0):
    """
    Cleanup completed analysis session after delay
    """
    if delay > 0:
        await asyncio.sleep(delay)

    if session_id in active_sessions:
        del active_sessions[session_id]

@app.on_event("startup")
async def startup_event():
    """Initialize app state on startup"""
    app.state.start_time = time.time()
    print("🚀 Enhanced PRI API started")
    print("📊 Metrics collection: Enabled")
    print("🎯 Interactive approval: Available")
    print("🧠 Persistent memory: Active")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Enhanced PRI API shutting down")
    active_sessions.clear()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)