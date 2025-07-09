#!/usr/bin/env python3
"""
Memory-Enhanced False Positive Detector

This module leverages PRI's sophisticated memory system to provide context-aware
false positive detection that learns and improves over time.

Key Features:
- Semantic pattern matching using FAISS vector search
- Cross-project pattern validation and transfer
- User feedback integration for continuous learning
- Context-aware rule application with memory persistence
- Namespace isolation for project-specific patterns
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

from .context_analyzer import FileContext, ContextAnalyzer
from ..memory.memory.engine import MemoryEngine
from ..memory.models import MemoryEntry, MemoryQuery, MemoryNamespace

logger = logging.getLogger(__name__)


class FalsePositiveConfidence(Enum):
    """Confidence levels for false positive detection"""


@dataclass
class FalsePositiveResult:
    """Result of false positive analysis"""
    is_false_positive: bool
    confidence: float
    reasoning: List[str]
    similar_cases: List[Dict]
    context_score: float
    cross_project_validation: Dict
    memory_based_adjustment: Optional[str] = None
    suggested_severity: Optional[str] = None


@dataclass
class ValidationMemory:
    """Structure for storing validation patterns in memory"""
    issue_type: str
    pattern_signature: str
    file_context: str
    project_type: str
    is_false_positive: bool
    confidence: float
    reasoning: str
    user_validated: bool
    validation_date: str
    pattern_features: Dict


class MemoryEnhancedFalsePositiveDetector:
    """
    Memory-enhanced false positive detector that learns from patterns and user feedback.

    This system uses PRI's memory engine to:
    1. Store and retrieve false positive patterns
    2. Learn from user corrections and feedback
    3. Apply context-aware rules based on historical data
    4. Validate issues against cross-project patterns
    5. Continuously improve detection accuracy
    """

    def __init__(self, memory_engine: MemoryEngine, context_analyzer: ContextAnalyzer):
        self.memory = memory_engine
        self.context_analyzer = context_analyzer
        self.false_positive_namespace = "false_positive_patterns"
        self.validation_namespace = "issue_validations"
        self.context_rules_namespace = "context_rules"

        # Pattern matching thresholds
        self.semantic_similarity_threshold = 0.75
        self.cross_project_agreement_threshold = 0.6
        self.context_confidence_threshold = 0.7

        # Initialize memory namespaces asynchronously when first used
        self._namespaces_initialized = False

    async def _ensure_namespaces_initialized(self):
        """Ensure memory namespaces are initialized for false positive detection"""
        if self._namespaces_initialized:
            return

        namespaces = [
            (self.false_positive_namespace, "Storage for confirmed false positive patterns"),
            (self.validation_namespace, "User validation results and feedback"),
            (self.context_rules_namespace, "Context-specific detection rules")
        ]

        for namespace_id, description in namespaces:
            try:
                await self.memory.create_namespace(MemoryNamespace(
                    namespace_id=namespace_id,
                    name=namespace_id.replace("_", " ").title(),
                    description=description
                ))
                logger.debug(f"Created namespace: {namespace_id}")
            except Exception as e:
                logger.debug(f"Namespace {namespace_id} may already exist: {e}")

        self._namespaces_initialized = True

    async def analyze_issue_for_false_positive(
        self,
        issue: Dict,
        file_path: str,
        project_context: Dict
    ) -> FalsePositiveResult:
        """
        Comprehensive false positive analysis using memory patterns.

        Args:
            issue: The detected issue to analyze
            file_path: Path to the file containing the issue
            project_context: Context about the current project

        Returns:
            FalsePositiveResult with detailed analysis
        """
        # Ensure namespaces are initialized
        await self._ensure_namespaces_initialized()

        logger.info(f"Analyzing issue for false positive: {issue['type']} in {file_path}")

        # Get file context
        file_context = self.context_analyzer.get_file_context(file_path)

        # 1. Semantic similarity to known false positives
        similar_fps = await self._find_similar_false_positives(issue, file_context)

        # 2. Context-based scoring
        context_score = await self._calculate_context_score(issue, file_context, project_context)

        # 3. Cross-project validation
        cross_project_validation = await self._validate_across_projects(issue, file_context)

        # 4. User feedback patterns
        user_feedback_patterns = await self._get_user_feedback_patterns(issue, file_context)

        # 5. Calculate final decision
        is_false_positive, confidence, reasoning = self._calculate_final_decision(
            similar_fps, context_score, cross_project_validation, user_feedback_patterns
        )

        # 6. Generate suggested severity adjustment
        suggested_severity = self._suggest_severity_adjustment(
            issue, file_context, is_false_positive, confidence
        )

        result = FalsePositiveResult(
            is_false_positive=is_false_positive,
            confidence=confidence,
            reasoning=reasoning,
            similar_cases=similar_fps,
            context_score=context_score,
            cross_project_validation=cross_project_validation,
            suggested_severity=suggested_severity
        )

        # Store analysis for future learning
        await self._store_analysis_result(issue, file_path, file_context, result)

        return result

    async def _find_similar_false_positives(self, issue: Dict, file_context: FileContext) -> List[Dict]:
        """Find similar false positive patterns using semantic search"""

        # Create semantic query for the issue
        query_text = f"false positive {issue['type']} {issue.get('description', '')} {file_context.value}"

        try:
            search_result = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=query_text,
                    namespace=self.false_positive_namespace,
                    similarity_threshold=self.semantic_similarity_threshold,
                    limit=10,
                    filters={"issue_type": issue["type"]}
                )
            )

            similar_cases = []
            for memory in search_result.memories:
                metadata = json.loads(memory.metadata or "{}")
                similar_cases.append({
                    "similarity": memory.similarity_score,
                    "issue_type": metadata.get("issue_type"),
                    "file_context": metadata.get("file_context"),
                    "reasoning": metadata.get("reasoning"),
                    "confidence": metadata.get("confidence", 0.0)
                })

            logger.info(f"Found {len(similar_cases)} similar false positive patterns")
            return similar_cases

        except Exception as e:
            logger.warning(f"Error searching for similar false positives: {e}")
            return []

    async def _calculate_context_score(
        self,
        issue: Dict,
        file_context: FileContext,
        project_context: Dict
    ) -> float:
        """Calculate context-based false positive score"""

        # Get stored context rules
        context_query = f"context rule {issue['type']} {file_context.value}"

        try:
            context_rules = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=context_query,
                    namespace=self.context_rules_namespace,
                    limit=5,
                    filters={"file_context": file_context.value}
                )
            )

            # Calculate base context score
            base_score = self._get_base_context_score(issue, file_context)

            # Adjust based on stored rules
            memory_adjustment = 0.0
            for rule_memory in context_rules.memories:
                rule_data = json.loads(rule_memory.metadata or "{}")
                if rule_data.get("issue_type") == issue["type"]:
                    memory_adjustment += rule_data.get("adjustment", 0.0) * rule_memory.similarity_score

            # Combine scores
            final_score = min(1.0, base_score + (memory_adjustment / max(len(context_rules.memories), 1)))

            logger.debug(f"Context score: base={base_score}, memory_adj={memory_adjustment}, final={final_score}")
            return final_score

        except Exception as e:
            logger.warning(f"Error calculating context score: {e}")
            return self._get_base_context_score(issue, file_context)

    def _get_base_context_score(self, issue: Dict, file_context: FileContext) -> float:
        """Get base context score without memory enhancement"""

        # Define context-specific false positive likelihoods
        context_fp_rates = {
            FileContext.TEST: {
                "print_statements": 0.8,
                "debug_code": 0.7,
                "hardcoded_credentials": 0.6,
                "bare_except": 0.3
            },
            FileContext.DEMO: {
                "print_statements": 0.9,
                "debug_code": 0.8,
                "hardcoded_credentials": 0.7,
                "hardcoded_paths": 0.8
            },
            FileContext.SCRIPT: {
                "print_statements": 0.6,
                "debug_code": 0.5,
                "hardcoded_paths": 0.4
            },
            FileContext.PRODUCTION: {
                "print_statements": 0.1,
                "debug_code": 0.0,
                "hardcoded_credentials": 0.0
            }
        }

        issue_type = issue.get("type", "unknown")
        return context_fp_rates.get(file_context, {}).get(issue_type, 0.3)

    async def _validate_across_projects(self, issue: Dict, file_context: FileContext) -> Dict:
        """Validate issue against patterns from other projects"""

        try:
            # Search across all validation namespaces
            all_namespaces = await self.memory.list_namespaces()
            validation_results = []

            for namespace in all_namespaces:
                if namespace.namespace_id in [self.false_positive_namespace, self.validation_namespace]:
                    continue

                # Search for similar validated issues
                similar_validations = await self.memory.search_memories(
                    MemoryQuery(
                        namespace=namespace.namespace_id,
                        semantic_query=f"{issue['type']} {issue.get('description', '')}",
                        filters={"memory_type": "validated_issue"},
                        similarity_threshold=0.7,
                        limit=3
                    )
                )

                for memory in similar_validations.memories:
                    validation_data = json.loads(memory.metadata or "{}")
                    validation_results.append({
                        "project": namespace.name,
                        "is_false_positive": validation_data.get("is_false_positive", False),
                        "confidence": validation_data.get("confidence", 0.0),
                        "similarity": memory.similarity_score,
                        "context": validation_data.get("file_context", "unknown")
                    })

            # Aggregate results
            if not validation_results:
                return {"cross_project_fp_rate": 0.0, "supporting_projects": [], "total_cases": 0}

            false_positive_votes = sum(
                v["confidence"] for v in validation_results
                if v["is_false_positive"] and v["context"] == file_context.value
            )
            total_confidence = sum(v["confidence"] for v in validation_results)

            fp_rate = false_positive_votes / max(total_confidence, 0.1)

            return {
                "cross_project_fp_rate": fp_rate,
                "supporting_projects": [v["project"] for v in validation_results if v["is_false_positive"]],
                "total_cases": len(validation_results),
                "average_confidence": total_confidence / len(validation_results)
            }

        except Exception as e:
            logger.warning(f"Error in cross-project validation: {e}")
            return {"cross_project_fp_rate": 0.0, "supporting_projects": [], "total_cases": 0}

    async def _get_user_feedback_patterns(self, issue: Dict, file_context: FileContext) -> List[Dict]:
        """Get user feedback patterns for similar issues"""

        try:
            feedback_query = f"user feedback {issue['type']} {file_context.value}"

            feedback_results = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=feedback_query,
                    namespace=self.validation_namespace,
                    filters={"memory_type": "user_feedback", "issue_type": issue["type"]},
                    limit=10
                )
            )

            patterns = []
            for memory in feedback_results.memories:
                feedback_data = json.loads(memory.metadata or "{}")
                patterns.append({
                    "is_false_positive": feedback_data.get("is_false_positive", False),
                    "user_reasoning": feedback_data.get("reasoning", ""),
                    "confidence": feedback_data.get("confidence", 0.0),
                    "similarity": memory.similarity_score
                })

            return patterns

        except Exception as e:
            logger.warning(f"Error getting user feedback patterns: {e}")
            return []

    def _calculate_final_decision(
        self,
        similar_fps: List[Dict],
        context_score: float,
        cross_project_validation: Dict,
        user_feedback: List[Dict]
    ) -> Tuple[bool, float, List[str]]:
        """Calculate final false positive decision with confidence and reasoning"""

        reasoning = []
        confidence_factors = []

        # Factor 1: Semantic similarity to known false positives
        if similar_fps:
            avg_similarity = sum(fp["similarity"] for fp in similar_fps) / len(similar_fps)
            fp_confidence = sum(fp["confidence"] for fp in similar_fps) / len(similar_fps)
            semantic_score = avg_similarity * fp_confidence
            confidence_factors.append(semantic_score)
            reasoning.append(f"Found {len(similar_fps)} similar false positive patterns (avg similarity: {avg_similarity:.2f})")

        # Factor 2: Context-based scoring
        confidence_factors.append(context_score)
        if context_score > self.context_confidence_threshold:
            reasoning.append(f"High context-based false positive likelihood ({context_score:.2f})")

        # Factor 3: Cross-project validation
        cross_project_score = cross_project_validation.get("cross_project_fp_rate", 0.0)
        if cross_project_validation.get("total_cases", 0) > 0:
            confidence_factors.append(cross_project_score)
            reasoning.append(f"Cross-project validation: {cross_project_score:.2f} FP rate across {cross_project_validation['total_cases']} cases")

        # Factor 4: User feedback patterns
        if user_feedback:
            user_fp_rate = sum(1 for fb in user_feedback if fb["is_false_positive"]) / len(user_feedback)
            confidence_factors.append(user_fp_rate)
            reasoning.append(f"User feedback indicates {user_fp_rate:.2f} false positive rate")

        # Calculate final confidence
        if confidence_factors:
            final_confidence = sum(confidence_factors) / len(confidence_factors)
        else:
            final_confidence = 0.3  # Default low confidence

        # Make final decision
        is_false_positive = final_confidence > 0.5

        # Add decision reasoning
        if is_false_positive:
            reasoning.append(f"CONCLUSION: Likely false positive (confidence: {final_confidence:.2f})")
        else:
            reasoning.append(f"CONCLUSION: Likely valid issue (confidence: {1-final_confidence:.2f})")

        return is_false_positive, final_confidence, reasoning

    def _suggest_severity_adjustment(
        self,
        issue: Dict,
        file_context: FileContext,
        is_false_positive: bool,
        confidence: float
    ) -> Optional[str]:
        """Suggest severity adjustment based on false positive analysis"""

        original_severity = issue.get("severity", "medium")

        if is_false_positive and confidence > 0.8:
            return "info"  # Downgrade to informational
        elif is_false_positive and confidence > 0.6:
            return "low"   # Downgrade to low
        elif not is_false_positive and confidence > 0.8:
            return original_severity  # Keep original severity
        else:
            # Moderate confidence - slight adjustment based on context
            context_adjustments = {
                FileContext.TEST: {"high": "medium", "critical": "high"},
                FileContext.DEMO: {"high": "medium", "medium": "low"},
                FileContext.SCRIPT: {"critical": "high", "high": "medium"}
            }

            return context_adjustments.get(file_context, {}).get(original_severity, original_severity)

    async def _store_analysis_result(
        self,
        issue: Dict,
        file_path: str,
        file_context: FileContext,
        result: FalsePositiveResult
    ):
        """Store analysis result for future learning"""

        try:
            analysis_memory = MemoryEntry(
                namespace=self.validation_namespace,
                content=f"False positive analysis: {issue['type']} issue in {file_context.value} file",
                memory_type="fp_analysis",
                metadata=json.dumps({
                    "issue_type": issue["type"],
                    "file_context": file_context.value,
                    "file_path": file_path,
                    "is_false_positive": result.is_false_positive,
                    "confidence": result.confidence,
                    "reasoning": result.reasoning,
                    "analysis_date": datetime.now().isoformat(),
                    "original_severity": issue.get("severity"),
                    "suggested_severity": result.suggested_severity
                }),
                tags=["false_positive_analysis", issue["type"], file_context.value]
            )

            await self.memory.store_memory(analysis_memory)
            logger.debug(f"Stored false positive analysis for {issue['type']} in {file_path}")

        except Exception as e:
            logger.warning(f"Error storing analysis result: {e}")

    async def learn_from_user_feedback(
        self,
        issue: Dict,
        file_path: str,
        is_false_positive: bool,
        user_reasoning: str,
        confidence: float = 1.0
    ):
        """Learn from user feedback to improve future detection"""

        # Ensure namespaces are initialized
        await self._ensure_namespaces_initialized()

        file_context = self.context_analyzer.get_file_context(file_path)

        try:
            # Store user feedback
            feedback_memory = MemoryEntry(
                namespace=self.validation_namespace,
                content=f"User validation: {issue['type']} marked as {'false positive' if is_false_positive else 'valid issue'}",
                memory_type="user_feedback",
                metadata=json.dumps({
                    "issue_type": issue["type"],
                    "file_context": file_context.value,
                    "file_path": file_path,
                    "is_false_positive": is_false_positive,
                    "user_reasoning": user_reasoning,
                    "confidence": confidence,
                    "feedback_date": datetime.now().isoformat(),
                    "issue_description": issue.get("description", ""),
                    "original_severity": issue.get("severity")
                }),
                tags=["user_feedback", "validation", issue["type"], file_context.value]
            )

            await self.memory.store_memory(feedback_memory)

            # If it's a confirmed false positive, store as a pattern
            if is_false_positive:
                await self._store_false_positive_pattern(issue, file_context, user_reasoning, confidence)

            logger.info(f"Learned from user feedback: {issue['type']} is {'false positive' if is_false_positive else 'valid'}")

        except Exception as e:
            logger.error(f"Error learning from user feedback: {e}")

    async def _store_false_positive_pattern(
        self,
        issue: Dict,
        file_context: FileContext,
        reasoning: str,
        confidence: float
    ):
        """Store confirmed false positive as a reusable pattern"""

        try:
            pattern_memory = MemoryEntry(
                namespace=self.false_positive_namespace,
                content=f"False positive pattern: {issue['type']} in {file_context.value} context - {reasoning}",
                memory_type="false_positive_pattern",
                metadata=json.dumps({
                    "issue_type": issue["type"],
                    "file_context": file_context.value,
                    "pattern_description": issue.get("description", ""),
                    "reasoning": reasoning,
                    "confidence": confidence,
                    "pattern_date": datetime.now().isoformat(),
                    "user_validated": True
                }),
                tags=["false_positive", "pattern", issue["type"], file_context.value]
            )

            await self.memory.store_memory(pattern_memory)
            logger.debug(f"Stored false positive pattern for {issue['type']} in {file_context.value}")

        except Exception as e:
            logger.warning(f"Error storing false positive pattern: {e}")

    async def get_false_positive_statistics(self) -> Dict:
        """Get statistics about false positive detection performance"""

        try:
            # Get all validation memories
            validation_results = await self.memory.search_memories(
                MemoryQuery(
                    namespace=self.validation_namespace,
                    semantic_query="false positive analysis validation",
                    limit=1000
                )
            )

            total_analyses = len(validation_results.memories)
            if total_analyses == 0:
                return {"message": "No validation data available yet"}

            # Calculate statistics
            false_positives = 0
            user_feedbacks = 0
            issue_type_stats = {}
            context_stats = {}

            for memory in validation_results.memories:
                metadata = json.loads(memory.metadata or "{}")
                issue_type = metadata.get("issue_type", "unknown")
                file_context = metadata.get("file_context", "unknown")

                if metadata.get("is_false_positive", False):
                    false_positives += 1

                if metadata.get("memory_type") == "user_feedback":
                    user_feedbacks += 1

                # Issue type statistics
                if issue_type not in issue_type_stats:
                    issue_type_stats[issue_type] = {"total": 0, "false_positives": 0}
                issue_type_stats[issue_type]["total"] += 1
                if metadata.get("is_false_positive", False):
                    issue_type_stats[issue_type]["false_positives"] += 1

                # Context statistics
                if file_context not in context_stats:
                    context_stats[file_context] = {"total": 0, "false_positives": 0}
                context_stats[file_context]["total"] += 1
                if metadata.get("is_false_positive", False):
                    context_stats[file_context]["false_positives"] += 1

            # Calculate rates
            overall_fp_rate = false_positives / total_analyses

            for stats in issue_type_stats.values():
                stats["fp_rate"] = stats["false_positives"] / stats["total"]

            for stats in context_stats.values():
                stats["fp_rate"] = stats["false_positives"] / stats["total"]

            return {
                "total_analyses": total_analyses,
                "total_false_positives": false_positives,
                "overall_fp_rate": overall_fp_rate,
                "user_feedbacks": user_feedbacks,
                "issue_type_statistics": issue_type_stats,
                "context_statistics": context_stats,
                "learning_effectiveness": user_feedbacks / max(total_analyses, 1)
            }

        except Exception as e:
            logger.error(f"Error getting false positive statistics: {e}")
            return {"error": str(e)}