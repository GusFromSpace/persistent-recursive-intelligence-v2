"""
Simple API for Persistent Recursive Intelligence
Provides easy external program integration
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project paths
sys.path.append(str(Path(__file__).parent.parent.parent))

from persistent_recursive_intelligence.cognitive.memory.simple_memory import SimpleMemoryEngine
from persistent_recursive_intelligence.cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveIntelligence
from persistent_recursive_intelligence.cognitive.enhanced_patterns.dynamic_connection_suggester import DynamicConnectionSuggester


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
    connection_suggester = DynamicConnectionSuggester()
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

    # Connection Suggester endpoints
    @app.post("/api/v1/connections/suggest")
    async def generate_connection_suggestions(
        orphaned_files: List[str], 
        main_files: List[str], 
        max_suggestions: int = 10
    ):
        """Generate dynamic connection suggestions"""
        try:
            suggestions = connection_suggester.generate_dynamic_suggestions(
                orphaned_files, main_files, max_suggestions
            )
            
            # Save suggestions to database
            for suggestion in suggestions:
                connection_suggester.save_suggestion(suggestion)
            
            # Convert to API-friendly format
            suggestion_data = []
            for suggestion in suggestions:
                suggestion_data.append({
                    "suggestion_id": suggestion.suggestion_id,
                    "orphaned_file": suggestion.orphaned_file,
                    "target_file": suggestion.target_file,
                    "connection_type": suggestion.connection_type,
                    "confidence_score": suggestion.confidence_score,
                    "suggestion_text": suggestion.suggestion_text,
                    "reasoning": suggestion.reasoning,
                    "semantic_similarity": suggestion.semantic_similarity,
                    "structural_compatibility": suggestion.structural_compatibility,
                    "need_detection_score": suggestion.need_detection_score,
                    "timestamp": suggestion.timestamp
                })
            
            return {
                "suggestions": suggestion_data,
                "total_count": len(suggestion_data),
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Failed to generate suggestions: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/connections/rate")
    async def rate_connection_suggestion(
        suggestion_id: str,
        rating: int,
        feedback: Optional[str] = None,
        implemented: bool = False
    ):
        """Rate a connection suggestion and provide feedback"""
        try:
            if not 1 <= rating <= 5:
                raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
            
            connection_suggester.rate_suggestion(suggestion_id, rating, feedback, implemented)
            
            return {
                "status": "success",
                "message": f"Suggestion {suggestion_id} rated {rating}/5",
                "suggestion_id": suggestion_id,
                "rating": rating,
                "feedback": feedback,
                "implemented": implemented
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Failed to rate suggestion: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/connections/learning-progress")
    async def get_learning_progress():
        """Get learning progress and statistics"""
        try:
            summary = connection_suggester.get_user_feedback_summary()
            return {
                "status": "success",
                "learning_progress": summary
            }
        except Exception as e:
            logger.error(f"Failed to get learning progress: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/connections/suggestions/{suggestion_id}")
    async def get_suggestion_details(suggestion_id: str):
        """Get details for a specific suggestion"""
        try:
            import sqlite3
            conn = sqlite3.connect(connection_suggester.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT suggestion_id, orphaned_file, target_file, connection_type, 
                       confidence_score, suggestion_text, reasoning, semantic_similarity,
                       structural_compatibility, need_detection_score, user_rating,
                       user_feedback, implemented, timestamp
                FROM suggestions WHERE suggestion_id = ?
            """, (suggestion_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                raise HTTPException(status_code=404, detail="Suggestion not found")
            
            import json
            reasoning = json.loads(result[6]) if result[6] else []
            
            return {
                "suggestion_id": result[0],
                "orphaned_file": result[1],
                "target_file": result[2],
                "connection_type": result[3],
                "confidence_score": result[4],
                "suggestion_text": result[5],
                "reasoning": reasoning,
                "semantic_similarity": result[7],
                "structural_compatibility": result[8],
                "need_detection_score": result[9],
                "user_rating": result[10],
                "user_feedback": result[11],
                "implemented": bool(result[12]),
                "timestamp": result[13]
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get suggestion details: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/connections/suggestions")
    async def list_all_suggestions(
        limit: int = 50,
        offset: int = 0,
        connection_type: Optional[str] = None,
        min_rating: Optional[int] = None
    ):
        """List all suggestions with optional filtering"""
        try:
            import sqlite3
            conn = sqlite3.connect(connection_suggester.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT suggestion_id, orphaned_file, target_file, connection_type,
                       confidence_score, suggestion_text, user_rating, implemented, timestamp
                FROM suggestions
                WHERE 1=1
            """
            params = []
            
            if connection_type:
                query += " AND connection_type = ?"
                params.append(connection_type)
            
            if min_rating:
                query += " AND user_rating >= ?"
                params.append(min_rating)
            
            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            suggestions = []
            for row in results:
                suggestions.append({
                    "suggestion_id": row[0],
                    "orphaned_file": row[1],
                    "target_file": row[2],
                    "connection_type": row[3],
                    "confidence_score": row[4],
                    "suggestion_text": row[5],
                    "user_rating": row[6],
                    "implemented": bool(row[7]),
                    "timestamp": row[8]
                })
            
            # Get total count
            count_query = "SELECT COUNT(*) FROM suggestions WHERE 1=1"
            count_params = []
            
            if connection_type:
                count_query += " AND connection_type = ?"
                count_params.append(connection_type)
            
            if min_rating:
                count_query += " AND user_rating >= ?"
                count_params.append(min_rating)
            
            cursor.execute(count_query, count_params)
            total_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "suggestions": suggestions,
                "total_count": total_count,
                "limit": limit,
                "offset": offset,
                "filters": {
                    "connection_type": connection_type,
                    "min_rating": min_rating
                }
            }
        except Exception as e:
            logger.error(f"Failed to list suggestions: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


# Create app instance
app = create_simple_api()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)