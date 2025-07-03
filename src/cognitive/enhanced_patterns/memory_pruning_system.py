#!/usr/bin/env python3
"""
Memory Pruning System for PRI

This module provides intelligent pruning capabilities for PRI's memory system
to prevent unbounded growth while preserving valuable patterns and insights.

Key Features:
- Age-based pruning with confidence weighting
- Redundancy elimination using semantic similarity
- Quality-based retention scoring
- Pattern consolidation and summarization
- Namespace-aware pruning strategies
- User feedback preservation
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Tuple

from ..memory.memory.engine import MemoryEngine
from ..memory.models import MemoryEntry, MemoryQuery

logger = logging.getLogger(__name__)


class PruningStrategy(Enum):
    """Different pruning strategies"""
    REDUNDANCY_BASED = None
    AGE_BASED = "age_based"
    QUALITY_BASED = "quality_based"
    SIMILARITY_BASED = "similarity_based"
    HYBRID = "hybrid"


@dataclass
class PruningConfig:
    """Configuration for memory pruning"""
    max_memories_per_namespace: int = 10000
    max_age_days: int = 365
    min_confidence_threshold: float = 0.3
    similarity_threshold: float = 0.9
    preserve_user_feedback: bool = True
    consolidation_threshold: int = 5
    quality_score_threshold: float = 0.5


@dataclass
class PruningResult:
    """Result of pruning operation"""
    total_memories_before: int
    total_memories_after: int
    memories_removed: int
    memories_consolidated: int
    space_saved_mb: float
    pruning_time_seconds: float
    strategy_used: PruningStrategy
    namespace_results: Dict[str, Dict]


class MemoryPruningSystem:
    """
    Intelligent memory pruning system that maintains quality while reducing storage.

    This system uses multiple strategies to identify and remove low-value memories
    while preserving important patterns, user feedback, and high-quality insights.
    """

    def __init__(self, memory_engine: MemoryEngine, config: PruningConfig = None):
        self.memory = memory_engine
        self.config = config or PruningConfig()

        # Namespaces that should be preserved more aggressively
        self.protected_namespaces = {
            "user_feedback", "false_positive_patterns", "validation_results"
        }

        # Quality indicators for different memory types
        self.quality_indicators = {
            "user_feedback": ["confidence", "user_validated"],
            "false_positive_pattern": ["confidence", "similarity_score"],
            "fp_analysis": ["confidence", "cross_project_validation"],
            "context_rule": ["effectiveness", "usage_count"]
        }

    async def prune_all_namespaces(self, strategy: PruningStrategy = PruningStrategy.HYBRID) -> PruningResult:
        """Prune all namespaces using the specified strategy"""

        start_time = datetime.now()
        logger.info(f"Starting comprehensive memory pruning with strategy: {strategy}")

        # Get initial memory statistics
        initial_stats = await self._get_memory_statistics()

        namespace_results = {}
        total_removed = 0
        total_consolidated = 0

        # Get all namespaces
        namespaces = await self.memory.list_namespaces()

        for namespace in namespaces:
            try:
                logger.info(f"Pruning namespace: {namespace.namespace_id}")

                result = await self._prune_namespace(namespace.namespace_id, strategy)
                namespace_results[namespace.namespace_id] = result
                total_removed += result["memories_removed"]
                total_consolidated += result["memories_consolidated"]

            except Exception as e:
                logger.error(f"Error pruning namespace {namespace.namespace_id}: {e}")
                namespace_results[namespace.namespace_id] = {"error": str(e)}

        # Get final memory statistics
        final_stats = await self._get_memory_statistics()

        end_time = datetime.now()
        pruning_time = (end_time - start_time).total_seconds()

        result = PruningResult(
            total_memories_before=initial_stats["total_memories"],
            total_memories_after=final_stats["total_memories"],
            memories_removed=total_removed,
            memories_consolidated=total_consolidated,
            space_saved_mb=self._estimate_space_saved(total_removed, total_consolidated),
            pruning_time_seconds=pruning_time,
            strategy_used=strategy,
            namespace_results=namespace_results
        )

        logger.info(f"Pruning completed: {total_removed} removed, {total_consolidated} consolidated")
        return result

    async def _prune_namespace(self, namespace_id: str, strategy: PruningStrategy) -> Dict:
        """Prune a specific namespace"""

        # Get all memories in the namespace
        all_memories = await self.memory.search_memories(
            MemoryQuery(
                namespace=namespace_id,
                semantic_query="",  # Empty query to get all
                limit=50000  # Large limit to get everything
            )
        )

        initial_count = len(all_memories.memories)

        if initial_count == 0:
            return {"memories_removed": 0, "memories_consolidated": 0, "initial_count": 0}

        # Apply appropriate pruning strategy
        if strategy == PruningStrategy.AGE_BASED:
            to_remove = await self._identify_aged_memories(all_memories.memories, namespace_id)
            to_consolidate = []

        elif strategy == PruningStrategy.REDUNDANCY_BASED:
            to_remove, to_consolidate = await self._identify_redundant_memories(all_memories.memories)

        elif strategy == PruningStrategy.QUALITY_BASED:
            to_remove = await self._identify_low_quality_memories(all_memories.memories, namespace_id)
            to_consolidate = []

        elif strategy == PruningStrategy.HYBRID:
            # Combine all strategies
            aged_memories = await self._identify_aged_memories(all_memories.memories, namespace_id)
            redundant_memories, consolidation_groups = await self._identify_redundant_memories(all_memories.memories)
            low_quality_memories = await self._identify_low_quality_memories(all_memories.memories, namespace_id)

            # Union of all removal candidates, prioritizing preservation of valuable memories
            to_remove = self._merge_removal_candidates(aged_memories, redundant_memories, low_quality_memories)
            to_consolidate = consolidation_groups

        else:
            to_remove = []
            to_consolidate = []

        # Perform the actual removal and consolidation
        removed_count = await self._remove_memories(to_remove, namespace_id)
        consolidated_count = await self._consolidate_memories(to_consolidate, namespace_id)

        return {
            "memories_removed": removed_count,
            "memories_consolidated": consolidated_count,
            "initial_count": initial_count,
            "final_count": initial_count - removed_count + consolidated_count
        }

    async def _identify_aged_memories(self, memories: List, namespace_id: str) -> List[str]:
        """Identify memories that are too old to be useful"""

        # Protected namespaces have longer retention
        max_age = timedelta(days=self.config.max_age_days * 2) if namespace_id in self.protected_namespaces else timedelta(days=self.config.max_age_days)
        cutoff_date = datetime.now() - max_age

        aged_memories = []

        for memory in memories:
            try:
                # Parse creation date from metadata or use memory timestamp
                metadata = json.loads(memory.metadata or "{}")

                # Try different date fields
                date_str = (metadata.get("analysis_date") or
                           metadata.get("feedback_date") or
                           metadata.get("pattern_date") or
                           memory.timestamp)

                if isinstance(date_str, str):
                    memory_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    memory_date = date_str

                # Consider confidence when determining age threshold
                confidence = metadata.get("confidence", 0.5)

                # High confidence memories get extended retention
                if confidence > 0.8:
                    effective_cutoff = cutoff_date - timedelta(days=180)  # Extra 6 months
                elif confidence > 0.6:
                    effective_cutoff = cutoff_date - timedelta(days=90)   # Extra 3 months
                else:
                    effective_cutoff = cutoff_date

                if memory_date < effective_cutoff:
                    aged_memories.append(memory.id)

            except Exception as e:
                logger.warning(f"Error parsing date for memory {memory.id}: {e}")

        logger.debug(f"Identified {len(aged_memories)} aged memories in {namespace_id}")
        return aged_memories

    async def _identify_redundant_memories(self, memories: List) -> Tuple[List[str], List[List]]:
        """Identify redundant memories using semantic similarity and effectiveness metrics"""

        if len(memories) < 2:
            return [], []

        # Enhanced grouping with effectiveness consideration
        similarity_groups = []
        processed_ids = set()

        # First, analyze pattern effectiveness to inform pruning decisions
        pattern_effectiveness = await self._analyze_pattern_effectiveness(memories)

        for i, memory_a in enumerate(memories):
            if memory_a.id in processed_ids:
                continue

            similar_group = [memory_a]
            processed_ids.add(memory_a.id)

            for j, memory_b in enumerate(memories[i+1:], i+1):
                if memory_b.id in processed_ids:
                    continue

                # Enhanced similarity calculation considering pattern type
                similarity = await self._calculate_enhanced_similarity(memory_a, memory_b, pattern_effectiveness)

                if similarity > self.config.similarity_threshold:
                    similar_group.append(memory_b)
                    processed_ids.add(memory_b.id)

            if len(similar_group) > 1:
                similarity_groups.append(similar_group)

        # Enhanced removal and consolidation logic
        to_remove = []
        to_consolidate = []

        for group in similarity_groups:
            pattern_saturation = await self._analyze_group_saturation(group, pattern_effectiveness)

            if pattern_saturation["is_over_represented"]:
                # Aggressive pruning for over-represented patterns we're catching well
                pruning_strategy = self._determine_aggressive_pruning_strategy(group, pattern_saturation)
                to_remove.extend(pruning_strategy["to_remove"])
                to_consolidate.extend(pruning_strategy["to_consolidate"])

            elif len(group) >= self.config.consolidation_threshold:
                # Standard consolidation for large groups
                to_consolidate.append(group)
            elif len(group) > 1:
                # Conservative pruning - keep the highest quality ones
                sorted_group = sorted(group, key=lambda m: self._calculate_quality_score_with_effectiveness(m, pattern_effectiveness), reverse=True)
                # Only remove lowest quality if confidence is high
                if self._should_remove_duplicates(sorted_group, pattern_effectiveness):
                    to_remove.extend([memory.id for memory in sorted_group[1:]])

        logger.debug(f"Identified {len(to_remove)} redundant memories and {len(to_consolidate)} consolidation groups using effectiveness metrics")
        return to_remove, to_consolidate

    async def _identify_low_quality_memories(self, memories: List, namespace_id: str) -> List[str]:
        """Identify low-quality memories based on various metrics"""

        low_quality = []

        for memory in memories:
            quality_score = self._calculate_quality_score(memory)

            # Apply namespace-specific quality thresholds
            if namespace_id in self.protected_namespaces:
                threshold = self.config.quality_score_threshold * 0.7  # Lower threshold for protected
            else:
                threshold = self.config.quality_score_threshold

            if quality_score < threshold:
                low_quality.append(memory.id)

        logger.debug(f"Identified {len(low_quality)} low-quality memories in {namespace_id}")
        return low_quality

    def _calculate_quality_score(self, memory) -> float:
        """Calculate quality score for a memory based on various factors"""

        try:
            metadata = json.loads(memory.metadata or "{}")
            memory_type = metadata.get("memory_type", "unknown")

            # Base score from confidence
            confidence = metadata.get("confidence", 0.5)
            quality_score = confidence

            # Add type-specific quality indicators
            indicators = self.quality_indicators.get(memory_type, [])

            for indicator in indicators:
                if indicator in metadata:
                    value = metadata[indicator]
                    if isinstance(value, (int, float)):
                        quality_score += value * 0.1  # Weight indicator values
                    elif isinstance(value, bool) and value:
                        quality_score += 0.2

            # Boost for user validation
            if metadata.get("user_validated", False):
                quality_score += 0.3

            # Boost for cross-project validation
            if metadata.get("cross_project_validation", False):
                quality_score += 0.2

            # Penalty for low usage
            usage_count = metadata.get("usage_count", 1)
            if usage_count == 0:
                quality_score -= 0.3

            return min(1.0, max(0.0, quality_score))

        except Exception as e:
            logger.warning(f"Error calculating quality score for memory {memory.id}: {e}")
            return 0.5  # Default middle score

    async def _analyze_pattern_effectiveness(self, memories: List) -> Dict:
        """Analyze pattern effectiveness across the memory set"""

        pattern_stats = {}
        total_patterns = len(memories)

        for memory in memories:
            try:
                metadata = json.loads(memory.metadata or "{}")
                pattern_type = metadata.get("memory_type", "unknown")
                issue_type = metadata.get("issue_type", pattern_type)

                if issue_type not in pattern_stats:
                    pattern_stats[issue_type] = {
                        "count": 0,
                        "total_confidence": 0.0,
                        "false_positive_count": 0,
                        "user_validated_count": 0,
                        "recent_count": 0
                    }

                stats = pattern_stats[issue_type]
                stats["count"] += 1
                stats["total_confidence"] += metadata.get("confidence", 0.5)

                if metadata.get("is_false_positive", False):
                    stats["false_positive_count"] += 1

                if metadata.get("user_validated", False):
                    stats["user_validated_count"] += 1

                date_str = metadata.get("analysis_date") or metadata.get("pattern_date")
                if date_str:
                    try:
                        memory_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        if memory_date > datetime.now() - timedelta(days=30):
                            stats["recent_count"] += 1
                    except Exception as e:
                        pass

            except Exception as e:
                logger.warning(f"Error analyzing pattern effectiveness for memory {memory.id}: {e}")

        # Calculate effectiveness metrics
        for pattern_type, stats in pattern_stats.items():
            if stats["count"] > 0:
                stats["avg_confidence"] = stats["total_confidence"] / stats["count"]
                stats["false_positive_rate"] = stats["false_positive_count"] / stats["count"]
                stats["user_validation_rate"] = stats["user_validated_count"] / stats["count"]
                stats["recent_activity_rate"] = stats["recent_count"] / stats["count"]

                # Calculate overall effectiveness score
                effectiveness = (
                    stats["avg_confidence"] * 0.3 +
                    (1.0 - stats["false_positive_rate"]) * 0.4 +
                    stats["user_validation_rate"] * 0.2 +
                    min(1.0, stats["recent_activity_rate"] * 2) * 0.1
                )
                stats["effectiveness_score"] = effectiveness

                # Determine if pattern is over-represented
                representation_ratio = stats["count"] / total_patterns
                stats["is_over_represented"] = (
                    representation_ratio > 0.2 and  # >20% of all patterns
                    stats["count"] > 10 and         # Absolute threshold
                    effectiveness > 0.7             # High effectiveness (we're catching these well)
                )

        return pattern_stats

    async def _calculate_enhanced_similarity(self, memory_a, memory_b, pattern_effectiveness: Dict) -> float:
        """Enhanced similarity calculation that considers pattern effectiveness"""

        # Base semantic similarity
        base_similarity = await self._calculate_similarity(memory_a, memory_b)

        try:
            # Get pattern types
            metadata_a = json.loads(memory_a.metadata or "{}")
            metadata_b = json.loads(memory_b.metadata or "{}")

            pattern_a = metadata_a.get("issue_type", "unknown")
            pattern_b = metadata_b.get("issue_type", "unknown")

            # If different pattern types, reduce similarity
            if pattern_a != pattern_b:
                base_similarity *= 0.7

            # If pattern is over-represented, increase similarity threshold for aggressive pruning
            pattern_stats = pattern_effectiveness.get(pattern_a, {})
            if pattern_stats.get("is_over_represented", False):
                # Make it easier to group over-represented patterns for pruning
                base_similarity *= 1.2

            return min(1.0, base_similarity)

        except Exception as e:
            logger.warning(f"Error in enhanced similarity calculation: {e}")
            return base_similarity

    async def _analyze_group_saturation(self, group: List, pattern_effectiveness: Dict) -> Dict:
        """Analyze if a group represents pattern saturation"""

        if not group:
            return {"is_over_represented": False}

        # Get the pattern type from the first memory
        try:
            first_metadata = json.loads(group[0].metadata or "{}")
            pattern_type = first_metadata.get("issue_type", "unknown")

            pattern_stats = pattern_effectiveness.get(pattern_type, {})

            # Calculate saturation metrics
            group_size = len(group)
            effectiveness_score = pattern_stats.get("effectiveness_score", 0.5)
            is_over_represented = pattern_stats.get("is_over_represented", False)
            false_positive_rate = pattern_stats.get("false_positive_rate", 0.5)

            # Determine saturation level
            saturation_level = "high" if group_size > 20 else ("medium" if group_size > 10 else "low")

            return {
                "pattern_type": pattern_type,
                "group_size": group_size,
                "effectiveness_score": effectiveness_score,
                "is_over_represented": is_over_represented,
                "false_positive_rate": false_positive_rate,
                "saturation_level": saturation_level,
                "can_aggressive_prune": is_over_represented and effectiveness_score > 0.7
            }

        except Exception as e:
            logger.warning(f"Error analyzing group saturation: {e}")
            return {"is_over_represented": False}

    def _determine_aggressive_pruning_strategy(self, group: List, saturation_analysis: Dict) -> Dict:
        """Determine aggressive pruning strategy for over-represented patterns"""

        group_size = len(group)
        effectiveness_score = saturation_analysis.get("effectiveness_score", 0.5)

        # Sort by quality
        sorted_group = sorted(group, key=lambda m: self._calculate_quality_score(m), reverse=True)

        if effectiveness_score > 0.8 and group_size > 20:
            # Very effective pattern with high duplication - aggressive pruning
            keep_count = max(3, group_size // 8)  # Keep only 12.5% (min 3)
            to_remove = [memory.id for memory in sorted_group[keep_count:]]
            to_consolidate = []

        elif effectiveness_score > 0.7 and group_size > 10:
            # Effective pattern with medium duplication - moderate pruning + consolidation
            keep_count = max(2, group_size // 4)  # Keep 25% (min 2)
            consolidate_count = min(8, group_size - keep_count)  # Consolidate up to 8

            to_remove = [memory.id for memory in sorted_group[keep_count + consolidate_count:]]
            to_consolidate = [sorted_group[keep_count:keep_count + consolidate_count]] if consolidate_count > 0 else []

        else:
            # Standard pruning for moderately effective patterns
            keep_count = max(5, group_size // 2)  # Keep 50% (min 5)
            to_remove = [memory.id for memory in sorted_group[keep_count:]]
            to_consolidate = []

        logger.info(f"Aggressive pruning for {saturation_analysis.get('pattern_type', 'unknown')}: "
                   f"keeping {group_size - len(to_remove)} out of {group_size}")

        return {
            "to_remove": to_remove,
            "to_consolidate": to_consolidate,
            "pruning_reason": f"Over-represented pattern with {effectiveness_score:.2f} effectiveness"
        }

    def _calculate_quality_score_with_effectiveness(self, memory, pattern_effectiveness: Dict) -> float:
        """Enhanced quality score that considers pattern effectiveness"""

        base_score = self._calculate_quality_score(memory)

        try:
            metadata = json.loads(memory.metadata or "{}")
            pattern_type = metadata.get("issue_type", "unknown")

            pattern_stats = pattern_effectiveness.get(pattern_type, {})

            # Boost score for effective patterns
            effectiveness_boost = pattern_stats.get("effectiveness_score", 0.5) * 0.1

            if pattern_stats.get("is_over_represented", False):
                over_representation_penalty = -0.05
            else:
                over_representation_penalty = 0.0

            enhanced_score = base_score + effectiveness_boost + over_representation_penalty
            return min(1.0, max(0.0, enhanced_score))

        except Exception as e:
            logger.warning(f"Error calculating enhanced quality score: {e}")
            return base_score

    def _should_remove_duplicates(self, sorted_group: List, pattern_effectiveness: Dict) -> bool:
        """Determine if duplicates should be removed based on pattern effectiveness"""

        if len(sorted_group) < 2:
            return False

        try:
            # Get pattern type from the highest quality memory
            metadata = json.loads(sorted_group[0].metadata or "{}")
            pattern_type = metadata.get("issue_type", "unknown")

            pattern_stats = pattern_effectiveness.get(pattern_type, {})

            # More aggressive removal for effective patterns
            effectiveness_score = pattern_stats.get("effectiveness_score", 0.5)
            false_positive_rate = pattern_stats.get("false_positive_rate", 0.5)

            # 2. We have sufficient examples
            # 3. Quality difference between memories is significant

            quality_diff = self._calculate_quality_score(sorted_group[0]) - self._calculate_quality_score(sorted_group[-1])

            should_remove = (
                effectiveness_score > 0.6 and
                false_positive_rate < 0.4 and
                quality_diff > 0.2 and
                len(sorted_group) > 3
            )

            return should_remove

        except Exception as e:
            logger.warning(f"Error determining duplicate removal: {e}")
            return False

    async def _calculate_similarity(self, memory_a, memory_b) -> float:
        """Calculate semantic similarity between two memories"""

        try:
            # Use the memory engine's semantic search if available
            if hasattr(self.memory, '_calculate_similarity'):
                return await self.memory._calculate_similarity(memory_a.content, memory_b.content)

            # Fallback to simple text similarity
            words_a = set(memory_a.content.lower().split())
            words_b = set(memory_b.content.lower().split())

            intersection = len(words_a.intersection(words_b))
            union = len(words_a.union(words_b))

            return intersection / union if union > 0 else 0.0

        except Exception as e:
            logger.warning(f"Error calculating similarity: {e}")
            return 0.0

    def _merge_removal_candidates(self, aged: List[str], redundant: List[str], low_quality: List[str]) -> List[str]:
        """Merge removal candidates from different strategies, avoiding over-aggressive pruning"""

        candidates = set(aged)

        # Add redundant memories
        candidates.update(redundant)

        # Add low quality memories, but limit to prevent over-pruning
        max_low_quality = len(low_quality) // 2  # Only remove half of low quality memories
        candidates.update(low_quality[:max_low_quality])

        return list(candidates)

    async def _remove_memories(self, memory_ids: List[str], namespace_id: str) -> int:
        """Remove specified memories"""

        removed_count = 0

        for memory_id in memory_ids:
            try:
                await self.memory.delete_memory(memory_id)
                removed_count += 1
            except Exception as e:
                logger.warning(f"Error removing memory {memory_id}: {e}")

        logger.info(f"Removed {removed_count} memories from {namespace_id}")
        return removed_count

    async def _consolidate_memories(self, consolidation_groups: List[List], namespace_id: str) -> int:
        """Consolidate similar memories into summary memories"""

        consolidated_count = 0

        for group in consolidation_groups:
            try:
                # Create consolidated memory
                consolidated_memory = self._create_consolidated_memory(group, namespace_id)

                # Store the consolidated memory
                await self.memory.store_memory(consolidated_memory)

                # Remove original memories
                for memory in group:
                    await self.memory.delete_memory(memory.id)

                consolidated_count += 1
                logger.debug(f"Consolidated {len(group)} memories into 1 summary")

            except Exception as e:
                logger.warning(f"Error consolidating memory group: {e}")

        logger.info(f"Consolidated {consolidated_count} memory groups in {namespace_id}")
        return consolidated_count

    def _create_consolidated_memory(self, memory_group: List, namespace_id: str) -> MemoryEntry:
        """Create a consolidated memory from a group of similar memories"""

        # Aggregate content
        all_content = [memory.content for memory in memory_group]
        consolidated_content = f"Consolidated pattern from {len(memory_group)} similar memories: " + "; ".join(all_content[:3])

        # Aggregate metadata
        all_metadata = []
        total_confidence = 0
        user_validated_count = 0

        for memory in memory_group:
            try:
                metadata = json.loads(memory.metadata or "{}")
                all_metadata.append(metadata)
                total_confidence += metadata.get("confidence", 0.5)
                if metadata.get("user_validated", False):
                    user_validated_count += 1
            except Exception as e:
                pass

        # Create consolidated metadata
        consolidated_metadata = {
            "memory_type": "consolidated_pattern",
            "original_count": len(memory_group),
            "consolidated_date": datetime.now().isoformat(),
            "confidence": total_confidence / len(memory_group),
            "user_validated": user_validated_count > len(memory_group) // 2,
            "consolidation_source": "memory_pruning_system",
            "original_memory_ids": [memory.id for memory in memory_group]
        }

        # Aggregate common fields
        if all_metadata:
            common_fields = ["issue_type", "file_context", "pattern_type"]
            for field in common_fields:
                values = [m.get(field) for m in all_metadata if m.get(field)]
                if values:
                    # Use most common value
                    consolidated_metadata[field] = max(set(values), key=values.count)

        # Aggregate tags
        all_tags = []
        for memory in memory_group:
            all_tags.extend(memory.tags or [])
        unique_tags = list(set(all_tags))
        unique_tags.append("consolidated")

        return MemoryEntry(
            namespace=namespace_id,
            content=consolidated_content,
            memory_type="consolidated_pattern",
            metadata=json.dumps(consolidated_metadata),
            tags=unique_tags
        )

    async def _get_memory_statistics(self) -> Dict:
        """Get overall memory statistics"""

        try:
            namespaces = await self.memory.list_namespaces()
            total_memories = 0

            for namespace in namespaces:
                memories = await self.memory.search_memories(
                    MemoryQuery(namespace=namespace.namespace_id, semantic_query="", limit=50000)
                )
                total_memories += len(memories.memories)

            return {"total_memories": total_memories}

        except Exception as e:
            logger.error(f"Error getting memory statistics: {e}")
            return {"total_memories": 0}

    def _estimate_space_saved(self, removed_count: int, consolidated_count: int) -> float:
        """Estimate space saved in MB"""

        # Rough estimates based on typical memory entry sizes
        avg_memory_size_kb = 2.0  # Average size per memory entry in KB

        # Consolidation saves space by reducing redundancy
        consolidation_savings = consolidated_count * 3 * avg_memory_size_kb  # Assume 4:1 consolidation ratio
        removal_savings = removed_count * avg_memory_size_kb

        total_savings_kb = consolidation_savings + removal_savings
        return total_savings_kb / 1024  # Convert to MB

    async def schedule_automatic_pruning(self, interval_hours: int = 24):
        """Schedule automatic pruning to run periodically"""

        logger.info(f"Scheduling automatic pruning every {interval_hours} hours")

        while True:
            try:
                await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds

                logger.info("Starting scheduled memory pruning")
                result = await self.prune_all_namespaces(PruningStrategy.HYBRID)

                logger.info(f"Scheduled pruning completed: {result.memories_removed} removed, "
                           f"{result.memories_consolidated} consolidated, "
                           f"{result.space_saved_mb:.2f}MB saved")

            except Exception as e:
                logger.error(f"Error in scheduled pruning: {e}")
                # Continue the loop even if one iteration fails

    async def prune_namespace_by_size(self, namespace_id: str, target_size: int) -> Dict:
        """Prune a namespace to a target size"""

        # Get all memories in namespace
        all_memories = await self.memory.search_memories(
            MemoryQuery(namespace=namespace_id, semantic_query="", limit=50000)
        )

        current_size = len(all_memories.memories)

        if current_size <= target_size:
            return {"message": f"Namespace {namespace_id} already under target size"}

        # Sort by quality score and remove lowest quality memories
        sorted_memories = sorted(
            all_memories.memories,
            key=lambda m: self._calculate_quality_score(m),
            reverse=True
        )

        # Keep the top target_size memories
        to_remove = sorted_memories[target_size:]

        # Remove excess memories
        removed_count = await self._remove_memories([m.id for m in to_remove], namespace_id)

        return {
            "namespace": namespace_id,
            "original_size": current_size,
            "target_size": target_size,
            "new_size": current_size - removed_count,
            "memories_removed": removed_count
        }