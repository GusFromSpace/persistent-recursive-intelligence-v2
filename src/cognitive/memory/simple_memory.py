"""
Simplified Memory System - Actually Working Implementation
"""

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

VECTOR_SEARCH_AVAILABLE = True
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False

class SimpleMemoryEngine:
    """
    Simplified but functional memory engine with FAISS integration
    """

    def __init__(self, db_path: str = "memory.db", namespace: str = "default"):
        self.db_path = db_path
        self.namespace = namespace
        self.logger = logging.getLogger(__name__)

        # Initialize database
        self._init_database()

        # Initialize vector search if available
        self.encoder = None
        self.vector_index = None
        self.vector_id_map = {}
        self.next_vector_id = 0

        if VECTOR_SEARCH_AVAILABLE:
            try:
                self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
                vector_dim = self.encoder.get_sentence_embedding_dimension()
                self.vector_index = faiss.IndexFlatIP(vector_dim)
                self.logger.info(f"Vector search initialized with dimension {vector_dim}")
            except Exception as e:
                self.logger.warning(f"Vector search initialization failed: {e}")
                self._vector_available = False

        self._vector_available = VECTOR_SEARCH_AVAILABLE and self.encoder is not None

        if not self._vector_available:
            self.logger.info("Operating in text-only mode (FAISS unavailable)")

    def _init_database(self):
        """Initialize SQLite database"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    namespace TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT DEFAULT "{}",
                    timestamp REAL NOT NULL,
                    vector_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_namespace_timestamp
                ON memories(namespace, timestamp DESC)
            """)

            conn.commit()

        self.logger.info(f"Database initialized at {self.db_path}")

    def store_memory(self, content: str, metadata: Dict[str, Any] = None) -> int:
        """Store a memory with optional vector embedding"""
        if metadata is None:
            metadata = {}

        timestamp = time.time()

        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO memories (namespace, content, metadata, timestamp)
                VALUES (?, ?, ?, ?)
            """, (self.namespace, content, json.dumps(metadata), timestamp))

            memory_id = cursor.lastrowid
            conn.commit()

        # Add to vector index if available
        if self.encoder and self.vector_index:
            try:
                embedding = self.encoder.encode([content]).astype("float32")
                faiss.normalize_L2(embedding)

                self.vector_index.add(embedding)
                self.vector_id_map[self.next_vector_id] = memory_id

                # Update database with vector ID
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        UPDATE memories SET vector_id = ? WHERE id = ?
                    """, (self.next_vector_id, memory_id))
                    conn.commit()

                self.next_vector_id += 1

            except Exception as e:
                self.logger.warning(f"Vector indexing failed for memory {memory_id}: {e}")

        return memory_id

    def search_memories(self, query: str, limit: int = 10, similarity_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search memories using semantic or text search"""

        # Try semantic search first if available
        if self.encoder and self.vector_index and self.vector_index.ntotal > 0:
            try:
                query_embedding = self.encoder.encode([query]).astype("float32")
                faiss.normalize_L2(query_embedding)

                # Search vector index
                distances, indices = self.vector_index.search(query_embedding, min(limit * 2, self.vector_index.ntotal))

                # Filter by similarity threshold
                memory_ids = []
                for distance, idx in zip(distances[0], indices[0]):
                    if idx != -1 and distance >= similarity_threshold and idx in self.vector_id_map:
                        memory_ids.append(self.vector_id_map[idx])

                if memory_ids:
                    # Get memories from database
                    # Validate that all memory_ids are integers
                    validated_ids = []
                    for mem_id in memory_ids:
                        if isinstance(mem_id, int):
                            validated_ids.append(mem_id)
                        elif isinstance(mem_id, str) and mem_id.isdigit():
                            validated_ids.append(int(mem_id))
                        else:
                            continue  # Skip invalid IDs

                    if not validated_ids:
                        return []

                    with sqlite3.connect(self.db_path) as conn:
                        conn.row_factory = sqlite3.Row
                        placeholders = ",".join("?" * len(validated_ids))
                        cursor = conn.execute(f"""
                            SELECT * FROM memories
                            WHERE id IN ({placeholders}) AND namespace = ?
                            ORDER BY timestamp DESC
                            LIMIT ?
                        """, validated_ids + [self.namespace, limit])

                        results = []
                        for row in cursor.fetchall():
                            results.append({
                                "id": row["id"],
                                "content": row["content"],
                                "metadata": json.loads(row["metadata"]),
                                "timestamp": row["timestamp"],
                                "search_type": "semantic"
                            })

                        if results:
                            return results

            except Exception as e:
                self.logger.warning(f"Semantic search failed: {e}")

        # Fallback to text search
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            # Sanitize query to prevent SQL wildcard injection
            sanitized_query = query.replace("%", "\\%").replace("_", "\\_")
            cursor = conn.execute("""
                SELECT * FROM memories
                WHERE namespace = ? AND content LIKE ? ESCAPE '\\'
                ORDER BY timestamp DESC
                LIMIT ?
            """, (self.namespace, f"%{sanitized_query}%", limit))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": json.loads(row["metadata"]),
                    "timestamp": row["timestamp"],
                    "search_type": "text"
                })

            return results

    def get_memory_count(self) -> int:
        """Get total number of memories in this namespace"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM memories WHERE namespace = ?", (self.namespace,))
            return cursor.fetchone()[0]

    def clear_memories(self):
        """Clear all memories in this namespace"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories WHERE namespace = ?", (self.namespace,))
            conn.commit()

        # Reset vector index
        if self.vector_index:
            vector_dim = self.encoder.get_sentence_embedding_dimension()
            self.vector_index = faiss.IndexFlatIP(vector_dim)
            self.vector_id_map = {}
            self.next_vector_id = 0

    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        status = {
            "database": "healthy",
            "vector_search": "unavailable",
            "memory_count": 0,
            "namespace": self.namespace
        }

        try:
            status["memory_count"] = self.get_memory_count()
        except Exception as e:
            status["database"] = f"error: {e}"

        if self._vector_available and self.encoder and self.vector_index:
            status["vector_search"] = "healthy"
            status["vector_index_size"] = self.vector_index.ntotal

        return status

    def cleanup(self):
        """
        Clean up memory engine resources to prevent memory leaks.
        Call this when analysis is complete to free RAM.
        """
        try:
            self.logger.info(f"🧹 Cleaning up SimpleMemoryEngine (namespace: {self.namespace})...")
            
            # Clear SentenceTransformer model
            if hasattr(self, 'encoder') and self.encoder is not None:
                try:
                    del self.encoder
                    self.encoder = None
                    self.logger.info("✅ SentenceTransformer model cleared")
                except Exception as e:
                    self.logger.warning(f"⚠️ Error clearing SentenceTransformer: {e}")
            
            # Clear FAISS vector index
            if hasattr(self, 'vector_index') and self.vector_index is not None:
                try:
                    self.vector_index.reset()
                    self.vector_index = None
                    self.logger.info("✅ FAISS vector index cleared")
                except Exception as e:
                    self.logger.warning(f"⚠️ Error clearing FAISS index: {e}")
            
            # Clear vector mappings
            if hasattr(self, 'vector_id_map'):
                self.vector_id_map.clear()
                self.logger.info("✅ Vector ID mappings cleared")
            
            # Mark vector search as unavailable
            self._vector_available = False
            
            # Force garbage collection
            import gc
            gc.collect()
            
            self.logger.info(f"🧹 SimpleMemoryEngine cleanup completed for {self.namespace}")
            
        except Exception as e:
            self.logger.error(f"❌ Error during SimpleMemoryEngine cleanup: {e}")

    def __del__(self):
        """Destructor to ensure cleanup on object deletion"""
        try:
            self.cleanup()
        except Exception:
            # Don't raise exceptions in destructor
            pass