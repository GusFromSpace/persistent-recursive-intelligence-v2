"""
Memory Engine - Core memory management and retrieval system

Enhanced version of the original memory service, extracted and optimized
for standalone use with multi-tenancy and improved performance.
"""

import sqlite3
import json
import time
import logging
import threading
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple, Any
from contextlib import contextmanager
import asyncio
from concurrent.futures import ThreadPoolExecutor

import numpy as np

# Optional FAISS import
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    faiss = None
    FAISS_AVAILABLE = False

# Optional sentence transformers import
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from ..models import (
    MemoryEntry, MemoryQuery, MemorySearchResult, MemoryRelationship,
    MemoryNamespace, MemoryStats, HealthStatus, TimeRange
)
from .exceptions import MemoryError, StorageError, VectorSearchError, NamespaceError
from ...utils.config import get_config
from ...utils.monitoring import get_metrics_collector
from ...utils.circuit_breaker import CircuitBreaker, CircuitBreakerError


class MemoryEngine:
    """
    Enhanced memory engine implementing hybrid architecture with multi-tenancy

    Follows Mesopredator principles:
    - Dual awareness: monitors both data integrity and semantic coherence
    - Cognitive flexibility: supports multiple query patterns and namespaces
    - Graceful degradation: operates even when vector search fails
    - Asymmetric leverage: one engine serves multiple applications
    """

    def __init__(self):
        self.config = get_config()
        self.logger = logging.getLogger(__name__)
        self.metrics = get_metrics_collector("memory_engine")

        # Thread safety
        self._db_lock = threading.RLock()
        self._vector_lock = threading.RLock()
        self._namespace_lock = threading.RLock()

        # Thread pool for async operations
        self.thread_pool = ThreadPoolExecutor(
            max_workers=self.config.performance.thread_pool_size
        )

        # Circuit breakers for graceful degradation
        self._init_circuit_breakers()

        # Initialize components
        self.namespaces: Dict[str, MemoryNamespace] = {}
        self._init_database()
        self._init_vector_search()
        self._load_namespaces()

        self.logger.info("Memory engine initialized successfully")

    def _init_circuit_breakers(self):
        """Initialize circuit breakers for different components"""
        self.db_circuit = CircuitBreaker(
            failure_threshold=self.config.performance.circuit_breaker_failure_threshold,
            recovery_timeout=self.config.performance.circuit_breaker_recovery_timeout,
            expected_exception=sqlite3.Error
        )

        self.vector_circuit = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=60,
            expected_exception=Exception
        )

    def _init_database(self):
        """Initialize SQLite database with optimizations for standalone use"""
        with self._db_lock:
            conn = sqlite3.connect(self.config.database.db_path)

            # Apply PRAGMA settings with validation
            allowed_pragmas = {
                'journal_mode': ['DELETE', 'TRUNCATE', 'PERSIST', 'MEMORY', 'WAL', 'OFF'],
                'synchronous': ['OFF', 'NORMAL', 'FULL', 'EXTRA'],
                'cache_size': lambda x: isinstance(x, (int, str)) and str(x).lstrip('-').isdigit(),
                'temp_store': ['DEFAULT', 'FILE', 'MEMORY'],
                'mmap_size': lambda x: isinstance(x, (int, str)) and str(x).isdigit(),
                'foreign_keys': ['ON', 'OFF', '1', '0'],
                'auto_vacuum': ['NONE', 'FULL', 'INCREMENTAL'],
                'page_size': lambda x: isinstance(x, (int, str)) and str(x).isdigit()
            }

            for pragma, value in self.config.database.pragma_settings.items():
                if pragma in allowed_pragmas:
                    validator = allowed_pragmas[pragma]
                    if callable(validator):
                        if validator(value):
                            conn.execute(f"PRAGMA {pragma}={value}")
                        else:
                            self.logger.warning(f"Invalid value for PRAGMA {pragma}: {value}")
                    elif str(value).upper() in validator:
                        conn.execute(f"PRAGMA {pragma}={value}")
                    else:
                        self.logger.warning(f"Invalid value for PRAGMA {pragma}: {value}")
                else:
                    self.logger.warning(f"Disallowed PRAGMA statement: {pragma}")

            # Create tables with enhanced schema
            self._create_tables(conn)

            conn.commit()
            conn.close()

        self.logger.info(f"Database initialized at {self.config.database.db_path}")

    def _create_tables(self, conn: sqlite3.Connection):
        """Create database tables with enhanced schema"""

        # Memory entries table with namespace support
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                namespace TEXT NOT NULL DEFAULT "default",
                content TEXT NOT NULL,
                timestamp REAL NOT NULL,
                memory_type TEXT DEFAULT "general",
                relevance_score REAL DEFAULT 0.0,
                metadata TEXT DEFAULT "{}",
                tags TEXT DEFAULT "[]",
                vector_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Namespaces table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS namespaces (
                namespace_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT DEFAULT "",
                isolation_level TEXT DEFAULT "isolated",
                quota_limits TEXT DEFAULT "{}",
                access_patterns TEXT DEFAULT "{}",
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT DEFAULT "{}"
            )
        """)

        # Memory relationships table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                namespace TEXT NOT NULL DEFAULT "default",
                source_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL DEFAULT 1.0,
                metadata TEXT DEFAULT "{}",
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES memory_entries (id),
                FOREIGN KEY (target_id) REFERENCES memory_entries (id)
            )
        """)

        # Create optimized indexes
        self._create_indexes(conn)

    def _create_indexes(self, conn: sqlite3.Connection):
        """Create optimized indexes for enhanced performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_memory_namespace_timestamp ON memory_entries(namespace, timestamp DESC)",
            "CREATE INDEX IF NOT EXISTS idx_memory_type_relevance ON memory_entries(memory_type, relevance_score DESC)",
            "CREATE INDEX IF NOT EXISTS idx_memory_content_fts ON memory_entries(content)",
            "CREATE INDEX IF NOT EXISTS idx_memory_tags ON memory_entries(tags)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_source ON memory_relationships(source_id)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_target ON memory_relationships(target_id)",
            "CREATE INDEX IF NOT EXISTS idx_relationships_type ON memory_relationships(relationship_type)",
            "CREATE INDEX IF NOT EXISTS idx_namespace_isolation ON namespaces(isolation_level)"
        ]

        for index_sql in indexes:
            conn.execute(index_sql)

    def _init_vector_search(self):
        """Initialize FAISS vector search with enhanced capabilities"""
        try:
            if not FAISS_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
                self.logger.info("Operating in text-only mode (FAISS or SentenceTransformers unavailable)")
                self.encoder = None
                self.vector_index = None
                self.vector_id_maps: Dict[str, Dict[int, int]] = {}
                self.next_vector_ids: Dict[str, int] = {}
                return

            self.encoder = SentenceTransformer(self.config.memory.vector_model)
            vector_dim = self.encoder.get_sentence_embedding_dimension()

            # Initialize FAISS index
            if self.config.memory.faiss_index_type == "IndexFlatIP":
                self.vector_index = faiss.IndexFlatIP(vector_dim)
            else:
                # Future: support other index types
                self.vector_index = faiss.IndexFlatIP(vector_dim)

            # Vector ID mapping per namespace
            self.vector_id_maps: Dict[str, Dict[int, int]] = {}
            self.next_vector_ids: Dict[str, int] = {}

            self.logger.info(f"Vector search initialized with dimension {vector_dim}")

        except Exception as e:
            self.logger.warning(f"Vector search initialization failed: {e}")
            self.encoder = None
            self.vector_index = None

    def _load_namespaces(self):
        """Load existing namespaces from database"""
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute("SELECT * FROM namespaces")
                for row in cursor.fetchall():
                    namespace = self._row_to_namespace(row)
                    self.namespaces[namespace.namespace_id] = namespace

                    # Initialize vector mappings for this namespace
                    if namespace.namespace_id not in self.vector_id_maps:
                        self.vector_id_maps[namespace.namespace_id] = {}
                        self.next_vector_ids[namespace.namespace_id] = 0

            self.logger.info(f"Loaded {len(self.namespaces)} namespaces")

        except Exception as e:
            self.logger.error(f"Failed to load namespaces: {e}")

    @contextmanager
    def get_db_connection(self):
        """Thread-safe database connection context manager"""
        with self._db_lock:
            conn = sqlite3.connect(
                self.config.database.db_path,
                timeout=self.config.database.connection_timeout
            )
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()

    async def create_namespace(self, namespace: MemoryNamespace) -> bool:
        """Create a new memory namespace"""
        with self._namespace_lock:
            if namespace.namespace_id in self.namespaces:
                raise NamespaceError(f"Namespace {namespace.namespace_id} already exists")

            try:
                with self.get_db_connection() as conn:
                    conn.execute("""
                        INSERT INTO namespaces
                        (namespace_id, name, description, isolation_level, quota_limits, access_patterns, metadata)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        namespace.namespace_id,
                        namespace.name,
                        namespace.description,
                        namespace.isolation_level.value,
                        json.dumps(namespace.quota_limits.__dict__),
                        json.dumps(namespace.access_patterns.__dict__),
                        json.dumps(namespace.metadata)
                    ))
                    conn.commit()

                # Initialize vector mappings
                self.vector_id_maps[namespace.namespace_id] = {}
                self.next_vector_ids[namespace.namespace_id] = 0

                self.namespaces[namespace.namespace_id] = namespace
                self.logger.info(f"Created namespace: {namespace.namespace_id}")
                return True

            except Exception as e:
                raise StorageError(f"Failed to create namespace: {e}")

    async def store_memory(self, memory: MemoryEntry) -> int:
        """Store memory with automatic vector embedding and namespace isolation"""
        with self.metrics.timer("store_memory"):
            # Validate namespace
            if memory.namespace not in self.namespaces and memory.namespace != "default":
                raise NamespaceError(f"Namespace {memory.namespace} does not exist")

            # Store in database
            memory_id = await self._store_to_database(memory)

            # Add to vector index if available
            if self.encoder and self.vector_index:
                try:
                    await self._add_to_vector_index(memory_id, memory.content, memory.namespace)
                except Exception as e:
                    self.logger.warning(f"Vector indexing failed for memory {memory_id}: {e}")

            self.metrics.increment("memories_stored")
            return memory_id

    async def _store_to_database(self, memory: MemoryEntry) -> int:
        """Store memory entry to SQLite database"""
        with self.db_circuit:
            with self.get_db_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO memory_entries
                    (namespace, content, timestamp, memory_type, relevance_score, metadata, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    memory.namespace,
                    memory.content,
                    memory.timestamp,
                    memory.memory_type,
                    memory.relevance_score,
                    json.dumps(memory.metadata),
                    json.dumps(memory.tags)
                ))

                memory_id = cursor.lastrowid
                conn.commit()
                return memory_id

    async def _add_to_vector_index(self, memory_id: int, content: str, namespace: str):
        """Add content to FAISS vector index with namespace isolation"""
        with self.vector_circuit:
            def _encode_and_add():
                with self._vector_lock:
                    embedding = self.encoder.encode([content])
                    embedding = embedding.astype("float32")

                    # Normalize for cosine similarity
                    faiss.normalize_L2(embedding)

                    # Use namespace-specific vector ID
                    if namespace not in self.next_vector_ids:
                        self.next_vector_ids[namespace] = 0
                        self.vector_id_maps[namespace] = {}

                    vector_id = self.next_vector_ids[namespace]
                    self.vector_index.add(embedding)
                    self.vector_id_maps[namespace][vector_id] = memory_id
                    self.next_vector_ids[namespace] += 1

            # Run encoding in thread pool to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                self.thread_pool, _encode_and_add
            )

    async def search_memories(self, query: MemoryQuery) -> MemorySearchResult:
        """Search memories using hybrid approach with namespace isolation"""
        start_time = time.time()

        with self.metrics.timer("search_memories"):
            # Validate namespace
            if query.namespace not in self.namespaces and query.namespace != "default":
                raise NamespaceError(f"Namespace {query.namespace} does not exist")

            memories = []
            similarity_scores = None

            # Try semantic search first
            if (query.semantic_query and self.encoder and
                self.vector_index and self.vector_index.ntotal > 0):
                try:
                    memories, similarity_scores = await self._semantic_search(query)
                except Exception as e:
                    self.logger.warning(f"Semantic search failed: {e}")

            # Fallback to text-based search if no semantic results
            if not memories:
                memories = await self._text_search(query)

            # Get relationships if requested
            relationships = None
            if query.include_relationships and memories:
                relationships = await self._get_relationships([m.id for m in memories if m.id])

            query_time_ms = (time.time() - start_time) * 1000

            result = MemorySearchResult(
                memories=memories,
                total_count=len(memories),
                query_time_ms=query_time_ms,
                similarity_scores=similarity_scores,
                relationships=relationships
            )

            self.metrics.increment("memories_retrieved", len(memories))
            return result

    async def _semantic_search(self, query: MemoryQuery) -> Tuple[List[MemoryEntry], List[float]]:
        """Semantic search using FAISS with namespace isolation"""
        def _search():
            with self.vector_circuit:
                with self._vector_lock:
                    query_embedding = self.encoder.encode([query.semantic_query]).astype("float32")
                    faiss.normalize_L2(query_embedding)

                    # Search in vector index
                    distances, indices = self.vector_index.search(
                        query_embedding,
                        min(query.limit * 2, self.vector_index.ntotal)  # Get more candidates
                    )

                    # Filter by namespace and similarity threshold
                    namespace_memory_ids = []
                    scores = []

                    if query.namespace in self.vector_id_maps:
                        vector_map = self.vector_id_maps[query.namespace]

                        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                            if idx != -1 and idx in vector_map:
                                similarity = float(distance)  # Already normalized
                                if similarity >= query.similarity_threshold:
                                    namespace_memory_ids.append(vector_map[idx])
                                    scores.append(similarity)

                    return namespace_memory_ids[:query.limit], scores[:query.limit]

        memory_ids, scores = await asyncio.get_event_loop().run_in_executor(
            self.thread_pool, _search
        )

        memories = await self._get_memories_by_ids(memory_ids)
        return memories, scores

    async def _text_search(self, query: MemoryQuery) -> List[MemoryEntry]:
        """Fallback text-based search with namespace isolation"""
        with self.db_circuit:
            with self.get_db_connection() as conn:
                where_conditions = ["namespace = ?"]
                params = [query.namespace]

                if query.semantic_query:
                    where_conditions.append("content LIKE ?")
                    params.append(f"%{query.semantic_query}%")

                # Apply filters
                for key, value in query.filters.items():
                    if key == "memory_type":
                        where_conditions.append("memory_type = ?")
                        params.append(value)
                    elif key == "tags":
                        where_conditions.append("tags LIKE ?")
                        params.append(f"%{value}%")
                    # Add more filter conditions as needed

                # Apply time range
                if query.time_range:
                    if query.time_range.start:
                        where_conditions.append("timestamp >= ?")
                        params.append(query.time_range.start.timestamp())
                    if query.time_range.end:
                        where_conditions.append("timestamp <= ?")
                        params.append(query.time_range.end.timestamp())

                where_clause = " AND ".join(where_conditions)

                cursor = conn.execute(f"""
                    SELECT * FROM memory_entries
                    WHERE {where_clause}
                    ORDER BY timestamp DESC
                    LIMIT ? OFFSET ?
                """, params + [query.limit, query.offset])

                return [self._row_to_memory_entry(row) for row in cursor.fetchall()]

    async def _get_memories_by_ids(self, memory_ids: List[int]) -> List[MemoryEntry]:
        """Retrieve memories by database IDs"""
        if not memory_ids:
            return []

        with self.get_db_connection() as conn:
            placeholders = ",".join("?" * len(memory_ids))
            cursor = conn.execute(f"""
                SELECT * FROM memory_entries
                WHERE id IN ({placeholders})
                ORDER BY timestamp DESC
            """, memory_ids)

            return [self._row_to_memory_entry(row) for row in cursor.fetchall()]

    async def _get_relationships(self, memory_ids: List[int]) -> List[MemoryRelationship]:
        """Get relationships for given memory IDs"""
        if not memory_ids:
            return []

        # Validate that all memory_ids are integers
        validated_ids = []
        for mem_id in memory_ids:
            if isinstance(mem_id, int):
                validated_ids.append(mem_id)
            elif isinstance(mem_id, str) and mem_id.isdigit():
                validated_ids.append(int(mem_id))
            else:
                self.logger.warning(f"Invalid memory ID: {mem_id}")
                continue

        if not validated_ids:
            return []

        with self.get_db_connection() as conn:
            placeholders = ",".join("?" * len(validated_ids))
            cursor = conn.execute(f"""
                SELECT * FROM memory_relationships
                WHERE source_id IN ({placeholders}) OR target_id IN ({placeholders})
            """, validated_ids + validated_ids)

            return [self._row_to_relationship(row) for row in cursor.fetchall()]

    def _row_to_memory_entry(self, row) -> MemoryEntry:
        """Convert database row to MemoryEntry"""
        return MemoryEntry(
            id=row["id"],
            namespace=row["namespace"],
            content=row["content"],
            timestamp=row["timestamp"],
            memory_type=row["memory_type"],
            relevance_score=row["relevance_score"],
            metadata=json.loads(row["metadata"]),
            tags=json.loads(row["tags"]),
            vector_id=row["vector_id"] if "vector_id" in row.keys() else None,
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None
        )

    def _row_to_namespace(self, row) -> MemoryNamespace:
        """Convert database row to MemoryNamespace"""
        from ..models import IsolationLevel, QuotaConfig, AccessConfig

        return MemoryNamespace(
            namespace_id=row["namespace_id"],
            name=row["name"],
            description=row["description"],
            isolation_level=IsolationLevel(row["isolation_level"]),
            quota_limits=QuotaConfig(**json.loads(row["quota_limits"])),
            access_patterns=AccessConfig(**json.loads(row["access_patterns"])),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            metadata=json.loads(row["metadata"])
        )

    def _row_to_relationship(self, row) -> MemoryRelationship:
        """Convert database row to MemoryRelationship"""
        from ..models import RelationType

        return MemoryRelationship(
            id=row["id"],
            namespace=row["namespace"],
            source_id=row["source_id"],
            target_id=row["target_id"],
            relationship_type=RelationType(row["relationship_type"]),
            strength=row["strength"],
            metadata=json.loads(row["metadata"]),
            created_at=datetime.fromisoformat(row["created_at"])
        )

    async def health_check(self) -> HealthStatus:
        """Comprehensive health check for monitoring"""
        health = HealthStatus()

        # Database health
        try:
            with self.get_db_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM memory_entries")
                count = cursor.fetchone()[0]
                health.components["database"] = {
                    "status": "healthy",
                    "memory_count": count,
                    "circuit_breaker": self.db_circuit.state
                }
        except Exception as e:
            health.components["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health.status = "degraded"

        # Vector search health
        if self.encoder and self.vector_index:
            health.components["vector_search"] = {
                "status": "healthy",
                "index_size": self.vector_index.ntotal,
                "circuit_breaker": self.vector_circuit.state
            }
        else:
            health.components["vector_search"] = {
                "status": "unavailable",
                "note": "Operating in text-only mode"
            }

        # Namespace health
        health.components["namespaces"] = {
            "status": "healthy",
            "count": len(self.namespaces),
            "active_namespaces": list(self.namespaces.keys())
        }

        return health

    def cleanup(self):
        """
        Clean up memory engine resources to prevent memory leaks.
        Call this when shutting down the application.
        """
        try:
            self.logger.info("Starting MemoryEngine cleanup...")
            
            # Clear FAISS vector index
            if hasattr(self, 'vector_index') and self.vector_index is not None:
                try:
                    # Reset FAISS index to free memory
                    self.vector_index.reset()
                    self.vector_index = None
                    self.logger.info("✅ FAISS vector index cleared")
                except Exception as e:
                    self.logger.warning(f"⚠️ Error clearing FAISS index: {e}")
            
            # Clear SentenceTransformer model
            if hasattr(self, 'encoder') and self.encoder is not None:
                try:
                    # Delete the model to free GPU/CPU memory
                    del self.encoder
                    self.encoder = None
                    self.logger.info("✅ SentenceTransformer model cleared")
                except Exception as e:
                    self.logger.warning(f"⚠️ Error clearing SentenceTransformer: {e}")
            
            # Clear vector ID mappings
            if hasattr(self, 'vector_id_maps'):
                self.vector_id_maps.clear()
                self.logger.info("✅ Vector ID mappings cleared")
            
            if hasattr(self, 'next_vector_ids'):
                self.next_vector_ids.clear()
                self.logger.info("✅ Next vector IDs cleared")
            
            # Clear namespaces
            if hasattr(self, 'namespaces'):
                self.namespaces.clear()
                self.logger.info("✅ Namespaces cleared")
            
            # Force garbage collection
            import gc
            gc.collect()
            self.logger.info("✅ Garbage collection forced")
            
            self.logger.info("🧹 MemoryEngine cleanup completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error during MemoryEngine cleanup: {e}")

    def __del__(self):
        """Destructor to ensure cleanup on object deletion"""
        try:
            self.cleanup()
        except Exception:
            # Don't raise exceptions in destructor
            pass