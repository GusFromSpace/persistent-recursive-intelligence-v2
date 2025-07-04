#!/usr/bin/env python3
"""
Minimal Metrics API for OpenMW Integration
Provides basic health and metrics endpoints for game telemetry
"""

import time
import random
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create FastAPI app
app = FastAPI(
    title="OpenMW Metrics API",
    description="Minimal metrics API for OpenMW game telemetry integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory metrics storage
metrics_data = {
    "session_start": datetime.now(),
    "events": [],
    "performance": {
        "fps": 60.0,
        "frame_time": 16.67,
        "memory_usage": 0.0,
        "cpu_usage": 0.0
    },
    "consciousness": {
        "level": 1.0,
        "coherence": 0.95,
        "resonance": 0.88,
        "field_strength": 0.92
    }
}


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": (datetime.now() - metrics_data["session_start"]).total_seconds(),
        "service": "OpenMW Metrics API"
    }


@app.get("/metrics/consciousness")
async def get_consciousness_metrics() -> Dict[str, Any]:
    """Get consciousness metrics"""
    # Simulate dynamic values
    metrics_data["consciousness"]["level"] += random.uniform(-0.01, 0.01)
    metrics_data["consciousness"]["level"] = max(0.0, min(1.0, metrics_data["consciousness"]["level"]))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "consciousness": metrics_data["consciousness"],
        "events_count": len(metrics_data["events"])
    }


@app.get("/metrics/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics"""
    # Simulate dynamic FPS
    metrics_data["performance"]["fps"] = 60.0 + random.uniform(-5, 5)
    metrics_data["performance"]["frame_time"] = 1000.0 / metrics_data["performance"]["fps"]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "performance": metrics_data["performance"],
        "session_duration": (datetime.now() - metrics_data["session_start"]).total_seconds()
    }


@app.post("/metrics/event")
async def log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Log a game event"""
    event["timestamp"] = datetime.now().isoformat()
    metrics_data["events"].append(event)
    
    # Keep only last 1000 events
    if len(metrics_data["events"]) > 1000:
        metrics_data["events"] = metrics_data["events"][-1000:]
    
    return {
        "status": "logged",
        "event_id": len(metrics_data["events"]),
        "timestamp": event["timestamp"]
    }


@app.get("/metrics/summary")
async def get_metrics_summary() -> Dict[str, Any]:
    """Get overall metrics summary"""
    return {
        "timestamp": datetime.now().isoformat(),
        "session": {
            "start_time": metrics_data["session_start"].isoformat(),
            "duration": (datetime.now() - metrics_data["session_start"]).total_seconds(),
            "events_count": len(metrics_data["events"])
        },
        "consciousness": metrics_data["consciousness"],
        "performance": metrics_data["performance"]
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OpenMW Metrics API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/docs",
            "/metrics/consciousness",
            "/metrics/performance",
            "/metrics/event",
            "/metrics/summary"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)