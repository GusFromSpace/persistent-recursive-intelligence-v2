"""
Simple API for Persistent Recursive Intelligence
Provides easy external program integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from typing import List, Optional, Dict, Any
import asyncio
import sys
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent.parent.parent))

from cognitive.memory.simple_memory import SimpleMemoryEngine
from cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveIntelligence


def create_simple_api() -> FastAPI:
    """Create simple API for external program integration"""

    app = FastAPI(
        title="Persistent Recursive Intelligence API",
        description="Simple API for external programs to interact with persistent recursive intelligence",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize components
    memory_engine = SimpleMemoryEngine()
    intelligence_engine = PersistentRecursiveIntelligence()
    logger = logging.getLogger(__name__)

    # Exception handlers
    @app.exception_handler(ValueError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"error": "Validation Error", "detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(exc)}
        )

    # Health endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        health = memory_engine.get_health_status()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": health,
            "api_version": "1.0.0"
        }

    # Memory operations
    @app.post("/api/v1/memory/store")
    async def store_memory(content: str, metadata: Optional[Dict[str, Any]] = None):
        """Store a new memory"""
        try:
            memory_id = memory_engine.store_memory(content, metadata or {})
            return {"memory_id": memory_id, "status": "stored"}
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/memory/search")
    async def search_memories(query: str, limit: int = 10, similarity_threshold: float = 0.5):
        """Search memories"""
        try:
            results = memory_engine.search_memories(query, limit, similarity_threshold)
            return {
                "memories": results,
                "total_count": len(results),
                "query": query
            }
        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Intelligence operations
    @app.post("/api/v1/intelligence/evolve")
    async def evolve_intelligence(project_path: str, max_iterations: int = 3):
        """Evolve intelligence on a project"""
        try:
            results = await intelligence_engine.evolve_with_persistence(project_path, max_iterations)
            return {
                "status": "completed",
                "results": results
            }
        except Exception as e:
            logger.error(f"Failed to evolve intelligence: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/intelligence/transfer")
    async def transfer_patterns(source_projects: List[str], target_project: str):
        """Transfer patterns between projects"""
        try:
            results = await intelligence_engine.cross_project_pattern_transfer(source_projects, target_project)
            return {
                "status": "completed",
                "results": results
            }
        except Exception as e:
            logger.error(f"Failed to transfer patterns: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # System operations
    @app.get("/api/v1/system/stats")
    async def get_system_stats():
        """Get system statistics"""
        try:
            memory_count = memory_engine.get_memory_count()
            health = memory_engine.get_health_status()
            return {
                "memory_count": memory_count,
                "health": health,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system stats: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/api/v1/system/clear")
    async def clear_system():
        """Clear all memories (use with caution)"""
        try:
            memory_engine.clear_memories()
            return {"status": "cleared", "message": "All memories cleared"}
        except Exception as e:
            logger.error(f"Failed to clear system: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


# Create app instance
app = create_simple_api()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)