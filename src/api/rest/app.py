"""
FastAPI application for Memory Intelligence Service REST API
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from typing import List, Optional

from ...cognitive.memory.simple_memory import SimpleMemoryEngine
from ...cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveIntelligence
from .models import (
    StoreMemoryRequest, SearchMemoriesRequest, CreateNamespaceRequest,
    CreateRelationshipRequest, StoreResponse, SearchResponse,
    MemoryResponse, NamespaceResponse, HealthResponse, MetricsResponse,
    ErrorResponse, MemoryCompactResponse, RelationshipResponse,
    ResultFormatAPI
)


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""

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
    logger = logging.getLogger(__name__)


    # Exception handlers
    @app.exception_handler(ValueError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Validation Error", "detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error", "detail": str(exc)}
        )

    # Health endpoints
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        health = await memory_engine.health_check()
        return HealthResponse(
            status=health.status,
            timestamp=health.timestamp,
            components=health.components,
            performance_metrics=health.performance_metrics,
            uptime_seconds=health.uptime_seconds
        )

    @app.get("/metrics", response_model=MetricsResponse)
    async def get_metrics():
        """Metrics endpoint"""
        if not config.monitoring.metrics_enabled:
            raise HTTPException(status_code=404, detail="Metrics disabled")

        all_metrics = metrics.get_all_metrics()
        return MetricsResponse(**all_metrics)

    # Memory operations
    @app.post("/api/v1/memories", response_model=StoreResponse)
    async def store_memory(request: StoreMemoryRequest):
        """Store a new memory"""
        try:
            memory = MemoryEntry(
                namespace=request.namespace,
                content=request.content,
                memory_type=request.memory_type,
                relevance_score=request.relevance_score,
                metadata=request.metadata,
                tags=request.tags
            )

            memory_id = await memory_engine.store_memory(memory)
            metrics.increment("memories_stored")

            return StoreResponse(memory_id=memory_id)

        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            metrics.increment("store_errors")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/v1/memories/search", response_model=SearchResponse)
    async def search_memories(request: SearchMemoriesRequest):
        """Search memories"""
        try:
            # Build time range
            time_range = None
            if request.time_range_start or request.time_range_end:
                time_range = TimeRange(
                    start=request.time_range_start,
                    end=request.time_range_end
                )

            # Build query
            query = MemoryQuery(
                namespace=request.namespace,
                semantic_query=request.query,
                filters=request.filters,
                time_range=time_range,
                similarity_threshold=request.similarity_threshold,
                limit=request.limit,
                offset=request.offset,
                include_relationships=request.include_relationships,
                include_metadata=request.include_metadata
            )

            # Perform search
            result = await memory_engine.search_memories(query)
            metrics.increment("searches_performed")

            # Convert to response format
            if request.result_format == ResultFormatAPI.IDS_ONLY:
                return SearchResponse(
                    memories=[],  # Empty for IDs only
                    total_count=result.total_count,
                    query_time_ms=result.query_time_ms
                )

            memories = []
            for memory in result.memories:
                if request.result_format == ResultFormatAPI.COMPACT:
                    memories.append(MemoryCompactResponse(
                        id=memory.id,
                        content=memory.content,
                        relevance_score=memory.relevance_score,
                        timestamp=memory.timestamp
                    ))
                else:
                    memories.append(MemoryResponse(
                        id=memory.id,
                        namespace=memory.namespace,
                        content=memory.content,
                        timestamp=memory.timestamp,
                        memory_type=memory.memory_type,
                        relevance_score=memory.relevance_score,
                        metadata=memory.metadata,
                        tags=memory.tags,
                        created_at=memory.created_at,
                        updated_at=memory.updated_at
                    ))

            relationships = []
            if result.relationships:
                relationships = [
                    RelationshipResponse(
                        id=rel.id,
                        source_id=rel.source_id,
                        target_id=rel.target_id,
                        relationship_type=rel.relationship_type.value,
                        strength=rel.strength,
                        metadata=rel.metadata,
                        created_at=rel.created_at
                    )
                    for rel in result.relationships
                ]

            return SearchResponse(
                memories=memories,
                total_count=result.total_count,
                query_time_ms=result.query_time_ms,
                similarity_scores=result.similarity_scores,
                relationships=relationships if relationships else None
            )

        except Exception as e:
            logger.error(f"Failed to search memories: {e}")
            metrics.increment("search_errors")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/memories/{memory_id}")
    async def get_memory(memory_id: int):
        """Get a specific memory by ID"""
        try:
            # For now, use search to get by ID - can optimize later
            query = MemoryQuery(
                filters={"id": memory_id},
                limit=1
            )
            result = await memory_engine.search_memories(query)

            if not result.memories:
                raise HTTPException(status_code=404, detail="Memory not found")

            memory = result.memories[0]
            return MemoryResponse(
                id=memory.id,
                namespace=memory.namespace,
                content=memory.content,
                timestamp=memory.timestamp,
                memory_type=memory.memory_type,
                relevance_score=memory.relevance_score,
                metadata=memory.metadata,
                tags=memory.tags,
                created_at=memory.created_at,
                updated_at=memory.updated_at
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get memory {memory_id}: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    # Namespace operations
    @app.post("/api/v1/namespaces")
    async def create_namespace(request: CreateNamespaceRequest):
        """Create a new namespace"""
        try:
            namespace = MemoryNamespace(
                namespace_id=request.namespace_id,
                name=request.name,
                description=request.description,
                isolation_level=IsolationLevel(request.isolation_level.value),
                quota_limits=QuotaConfig(
                    max_memories=request.max_memories,
                    max_storage_mb=request.max_storage_mb,
                    max_requests_per_hour=request.max_requests_per_hour
                ),
                metadata=request.metadata
            )

            success = await memory_engine.create_namespace(namespace)
            if success:
                metrics.increment("namespaces_created")
                return {"message": f"Namespace {request.namespace_id} created successfully"}
            else:
                raise HTTPException(status_code=400, detail="Failed to create namespace")

        except Exception as e:
            logger.error(f"Failed to create namespace: {e}")
            metrics.increment("namespace_errors")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/namespaces", response_model=List[NamespaceResponse])
    async def list_namespaces():
        """List all namespaces"""
        try:
            namespaces = []
            for ns_id, namespace in memory_engine.namespaces.items():
                # Get memory count for this namespace
                query = MemoryQuery(namespace=ns_id, limit=0)
                result = await memory_engine.search_memories(query)

                namespaces.append(NamespaceResponse(
                    namespace_id=namespace.namespace_id,
                    name=namespace.name,
                    description=namespace.description,
                    isolation_level=namespace.isolation_level.value,
                    created_at=namespace.created_at,
                    updated_at=namespace.updated_at,
                    memory_count=result.total_count,
                    storage_used_mb=0.0  # Calculate actual storage usage
                ))

            return namespaces

        except Exception as e:
            logger.error(f"Failed to list namespaces: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app