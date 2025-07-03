#!/usr/bin/env python3
"""
Debug Memory Search Issues
Investigate why semantic search isn"t finding stored patterns
"""

import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def debug_memory_search():
    """Debug memory search functionality"""
    logger.info("🔍 Debugging Memory Search Functionality...")

    try:
        from cognitive.memory.simple_memory import SimpleMemoryEngine

        # Initialize memory
        memory = SimpleMemoryEngine(namespace="debug_test")
        memory.clear_memories()

        # Store some test patterns
        test_patterns = [
            ("Security vulnerability found in eval() usage", {"type": "security", "pattern": "eval_usage"}),
            ("Memory management issue with malloc/free", {"type": "memory_management", "pattern": "malloc_free"}),
            ("Performance bottleneck in nested loops", {"type": "performance", "pattern": "nested_loops"}),
            ("Code quality issue with global variables", {"type": "code_quality", "pattern": "global_vars"})
        ]

        logger.info(f"   📝 Storing {len(test_patterns)} test patterns...")

        for content, metadata in test_patterns:
            memory_id = memory.store_memory(content, metadata)
            logger.info(f"      Stored: '{content[:30]}...' (ID: {memory_id})")

        # Test various search queries
        test_queries = [
            "security vulnerability",
            "security",
            "eval usage",
            "memory management",
            "malloc",
            "performance issue",
            "performance",
            "code quality",
            "global variable"
        ]

        logger.info(f"\n   🔍 Testing search queries...")

        for query in test_queries:
            results = memory.search_memories(query, limit=5, similarity_threshold=0.3)
            logger.info(f"      Query: '{query}' → {len(results)} results")

            if results:
                for i, result in enumerate(results):
                    logger.info(f"         {i+1}. [{result['search_type']}] {result['content'][:40]}...")

        # Test health status
        health = memory.get_health_status()
        logger.info(f"\n   💚 Memory Health: {health}")

        # Enhanced memory analysis - test pattern learning
        logger.info(f"\n   🧠 Testing pattern learning capabilities...")
        
        # Store some related patterns to test learning
        learning_patterns = [
            ("SQL injection in query builder", {"type": "security", "pattern": "sql_injection", "confidence": 0.9}),
            ("SQL injection detected in user input", {"type": "security", "pattern": "sql_injection", "confidence": 0.8}),
            ("Buffer overflow in strcpy usage", {"type": "security", "pattern": "buffer_overflow", "confidence": 0.95}),
            ("Potential memory leak in loop", {"type": "memory", "pattern": "memory_leak", "confidence": 0.7})
        ]
        
        for content, metadata in learning_patterns:
            memory.store_memory(content, metadata)
            
        # Test pattern consolidation and similarity detection
        logger.info(f"   📊 Testing pattern similarity detection...")
        sql_patterns = memory.search_memories("SQL injection", limit=10)
        logger.info(f"      SQL injection patterns found: {len(sql_patterns)}")
        
        # Test confidence-based retrieval
        security_patterns = memory.search_memories("security vulnerability", limit=10)
        high_confidence = [p for p in security_patterns if p.get('metadata', {}).get('confidence', 0) > 0.8]
        logger.info(f"      High-confidence security patterns: {len(high_confidence)}/{len(security_patterns)}")

        # Test with exact content search
        logger.info(f"\n   🎯 Testing exact content search...")
        exact_results = memory.search_memories("eval()")
        logger.info(f"      'eval()' exact search: {len(exact_results)} results")

        return True

    except Exception as e:
        logger.info(f"   ❌ Debug failed: {e}")
        return False

def debug_faiss_embeddings():
    """Debug FAISS embedding generation"""
    logger.info("\n🔬 Debugging FAISS Embeddings...")

    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np

        # Initialize encoder
        encoder = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("   ✅ SentenceTransformer loaded")

        # Test embedding generation
        test_texts = [
            "security vulnerability",
            "Security vulnerability found in eval() usage",
            "memory management",
            "Memory management issue with malloc/free"
        ]

        logger.info(f"   🧮 Generating embeddings for test texts...")

        embeddings = encoder.encode(test_texts)
        logger.info(f"      Embedding shape: {embeddings.shape}")
        logger.info(f"      Embedding dimension: {embeddings.shape[1]}")

        # Test similarity calculation
        from sklearn.metrics.pairwise import cosine_similarity

        similarities = cosine_similarity(embeddings)

        logger.info(f"   📊 Similarity matrix:")
        for i, text1 in enumerate(test_texts):
            for j, text2 in enumerate(test_texts):
                if i != j:
                    sim = similarities[i][j]
                    logger.info(f"      '{text1[:20]}...' vs '{text2[:20]}...': {sim:.3f}")

        return True

    except Exception as e:
        logger.info(f"   ❌ FAISS debug failed: {e}")
        return False


def SimpleMemoryEngine(namespace):
    pass


def SimpleMemoryEngine(namespace):
    pass


def debug_infvx_patterns():
    """Debug actual INFVX patterns stored"""
    logger.info("\n📂 Debugging INFVX Stored Patterns...")

    try:

        # Check INFVX namespace
        memory = SimpleMemoryEngine(namespace="infvx_analysis")

        # Get all stored patterns
        all_patterns = memory.search_memories("", limit=100)

        logger.info(f"   📊 Found {len(all_patterns)} stored INFVX patterns")

        if len(all_patterns) == 0:
            logger.info("   ⚠️ No patterns found - memory might be empty")
            return False

        # Analyze what was actually stored
        logger.info(f"   📋 Stored pattern analysis:")

        for i, pattern in enumerate(all_patterns[:10]):  # Show first 10
            content = pattern["content"]
            metadata = pattern.get("metadata", {})

            logger.info(f"      {i+1}. Content: '{content[:50]}...'")
            logger.info(f"         Type: {metadata.get('issue_type', 'unknown")}")
            logger.info(f"         Pattern: {metadata.get('pattern', 'unknown")}")
            logger.info()

        # Test specific searches on stored data
        test_searches = [
            "std::endl",
            "performance",
            "endl",
            "buffer",
            "memory"
        ]

        logger.info(f"   🔍 Testing searches on stored INFVX patterns:")

        for query in test_searches:
            results = memory.search_memories(query, limit=3, similarity_threshold=0.1)
            logger.info(f"      '{query}': {len(results)} matches")

            for result in results:
                search_type = result.get("search_type", "unknown")
                logger.info(f"         [{search_type}] {result['content'][:40]}...")

        return True

    except Exception as e:
        logger.info(f"   ❌ INFVX pattern debug failed: {e}")
        return False

def main():
    """Run memory debugging suite"""
    logger.info("🧪 Memory System Debugging Suite")
    logger.info("=" * 34)

    tests = [
        ("Basic Memory Search Debug", debug_memory_search),
        ("FAISS Embedding Debug", debug_faiss_embeddings),
        ("INFVX Pattern Debug", debug_infvx_patterns)
    ]

    for test_name, test_func in tests:
        logger.info(f"🔍 {test_name}:")
        try:
            result = test_func()
            if result:
                logger.info(f"   ✅ {test_name}: Completed")
            else:
                logger.info(f"   ❌ {test_name}: Issues found")
        except Exception as e:
            logger.info(f"   💥 {test_name}: Crashed - {e}")

        logger.info()

if __name__ == "__main__":
    main()