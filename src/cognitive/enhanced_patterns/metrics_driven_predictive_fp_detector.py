#!/usr/bin/env python3
"""
Metrics-Driven Predictive False Positive Detector

This module leverages PRI's metrics system to predict false positives before they occur,
using historical data patterns, detection effectiveness metrics, and trend analysis.

Key Features:
- Predictive modeling based on historical metrics
- Pattern trend analysis for early false positive detection
- Context-specific prediction models
- Real-time adjustment of detection thresholds
- Metrics-informed confidence scoring
- Performance-based model adaptation
"""

import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio

from ..memory.memory.engine import MemoryEngine
from ..memory.models import MemoryEntry, MemoryQuery
from ..metrics.models import AnalysisMetrics, IntelligenceMetrics, PerformanceMetrics
from .context_analyzer import FileContext, ContextAnalyzer
from .memory_enhanced_false_positive_detector import MemoryEnhancedFalsePositiveDetector

logger = logging.getLogger(__name__)


class PredictionConfidence(Enum):
    """Confidence levels for false positive predictions"""


@dataclass
class FalsePositivePrediction:
    """Prediction result for false positive likelihood"""
    issue_type: str
    predicted_fp_probability: float
    confidence: float
    prediction_basis: List[str]
    historical_fp_rate: float
    trend_analysis: Dict
    context_influence: float
    metrics_factors: Dict
    recommended_action: str
    threshold_adjustment: Optional[float] = None


@dataclass
class PatternTrend:
    """Trend analysis for a specific pattern"""
    pattern_type: str
    recent_fp_rate: float
    historical_fp_rate: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    sample_size: int
    confidence_interval: Tuple[float, float]
    prediction_accuracy: float


class MetricsDrivenPredictiveFPDetector:
    """
    Advanced false positive detector that uses metrics to predict issues before they occur.

    This system analyzes:
    1. Historical false positive rates by pattern type and context
    2. Detection effectiveness trends over time
    3. Pattern saturation and duplication levels
    4. Performance impact of different detection strategies
    5. Cross-project pattern transfer success rates
    """

    def __init__(self,
                 memory_engine: MemoryEngine,
                 context_analyzer: ContextAnalyzer,
                 base_fp_detector: MemoryEnhancedFalsePositiveDetector,
                 metrics_collector = None):
        self.memory = memory_engine
        self.context_analyzer = context_analyzer
        self.base_fp_detector = base_fp_detector
        self.metrics_collector = metrics_collector

        # Prediction model parameters
        self.trend_analysis_window_days = 30
        self.min_samples_for_prediction = 5
        self.pattern_saturation_threshold = 0.8

        # Adaptive thresholds based on metrics
        self.adaptive_thresholds = {}

        # Pattern effectiveness cache
        self.pattern_effectiveness_cache = {}
        self.cache_expiry = datetime.now()
        self.cache_duration_hours = 6

    async def predict_false_positive_likelihood(
        self,
        issue: Dict,
        file_path: str,
        project_context: Dict
    ) -> FalsePositivePrediction:
        """
        Predict the likelihood of an issue being a false positive using metrics analysis.

        Args:
            issue: The detected issue to analyze
            file_path: Path to the file containing the issue
            project_context: Context about the current project

        Returns:
            FalsePositivePrediction with detailed analysis and confidence
        """
        logger.info(f"Predicting false positive likelihood for {issue['type']} in {file_path}")

        # Get file context
        file_context = self.context_analyzer.get_file_context(file_path)

        # 1. Historical false positive rate analysis
        historical_fp_rate = await self._get_historical_fp_rate(issue['type'], file_context)

        # 2. Pattern trend analysis
        trend_analysis = await self._analyze_pattern_trends(issue['type'], file_context)

        # 3. Context-specific influence analysis
        context_influence = await self._analyze_context_influence(issue, file_context, project_context)

        # 4. Metrics-based factors
        metrics_factors = await self._analyze_metrics_factors(issue, file_context)

        # 5. Pattern saturation analysis
        saturation_analysis = await self._analyze_pattern_saturation(issue['type'])

        # 6. Calculate prediction
        prediction_result = self._calculate_prediction(
            issue, historical_fp_rate, trend_analysis, context_influence,
            metrics_factors, saturation_analysis
        )

        # 7. Generate recommended action

        # 8. Store prediction for learning
        await self._store_prediction(issue, file_path, prediction_result)

        return prediction_result

    async def _get_historical_fp_rate(self, issue_type: str, file_context: FileContext) -> float:
        """Get historical false positive rate for this issue type and context"""

        try:
            # Query validation memories for historical data
            historical_query = f"false positive {issue_type} {file_context.value}"

            historical_data = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=historical_query,
                    namespace="issue_validations",
                    filters={"issue_type": issue_type, "file_context": file_context.value},
                    limit=100
                )
            )

            if len(historical_data.memories) < self.min_samples_for_prediction:
                # Fall back to general stats if insufficient context-specific data
                general_stats = await self.base_fp_detector.get_false_positive_statistics()
                type_stats = general_stats.get("issue_type_statistics", {}).get(issue_type, {})
                return type_stats.get("fp_rate", 0.5)

            # Calculate historical FP rate
            false_positives = 0
            total_samples = 0

            for memory in historical_data.memories:
                metadata = json.loads(memory.metadata or "{}")
                if metadata.get("is_false_positive", False):
                    false_positives += 1
                total_samples += 1

            historical_rate = false_positives / max(total_samples, 1)
            logger.debug(f"Historical FP rate for {issue_type} in {file_context.value}: {historical_rate:.2f}")

            return historical_rate

        except Exception as e:
            logger.warning(f"Error getting historical FP rate: {e}")
            return 0.5  # Default neutral rate

    async def _analyze_pattern_trends(self, issue_type: str, file_context: FileContext) -> PatternTrend:
        """Analyze trends in false positive rates for this pattern"""

        try:
            recent_cutoff = datetime.now() - timedelta(days=self.trend_analysis_window_days)

            recent_data = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"validation {issue_type} {file_context.value}",
                    namespace="issue_validations",
                    filters={
                        "issue_type": issue_type,
                        "validation_date_after": recent_cutoff.isoformat()
                    },
                    limit=50
                )
            )

            # Get older data for comparison
            older_cutoff = recent_cutoff - timedelta(days=self.trend_analysis_window_days)

            older_data = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"validation {issue_type} {file_context.value}",
                    namespace="issue_validations",
                    filters={
                        "issue_type": issue_type,
                        "validation_date_before": recent_cutoff.isoformat(),
                        "validation_date_after": older_cutoff.isoformat()
                    },
                    limit=50
                )
            )

            # Calculate rates
            recent_fp_rate = self._calculate_fp_rate_from_memories(recent_data.memories)
            historical_fp_rate = self._calculate_fp_rate_from_memories(older_data.memories)

            # Determine trend direction
            if recent_fp_rate > historical_fp_rate + 0.1:
                trend_direction = "increasing"
            elif recent_fp_rate < historical_fp_rate - 0.1:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"

            # Calculate confidence interval
            recent_samples = len(recent_data.memories)
            confidence_interval = self._calculate_confidence_interval(recent_fp_rate, recent_samples)

            # Estimate prediction accuracy based on trend stability
            prediction_accuracy = self._estimate_prediction_accuracy(
                recent_fp_rate, historical_fp_rate, recent_samples
            )

            return PatternTrend(
                pattern_type=issue_type,
                recent_fp_rate=recent_fp_rate,
                historical_fp_rate=historical_fp_rate,
                trend_direction=trend_direction,
                sample_size=recent_samples,
                confidence_interval=confidence_interval,
                prediction_accuracy=prediction_accuracy
            )

        except Exception as e:
            logger.warning(f"Error analyzing pattern trends: {e}")
            return PatternTrend(
                pattern_type=issue_type,
                recent_fp_rate=0.5,
                historical_fp_rate=0.5,
                trend_direction="stable",
                sample_size=0,
                confidence_interval=(0.3, 0.7),
                prediction_accuracy=0.5
            )

    def _calculate_fp_rate_from_memories(self, memories: List) -> float:
        """Calculate false positive rate from memory entries"""

        if not memories:
            return 0.5

        false_positives = 0
        for memory in memories:
            try:
                metadata = json.loads(memory.metadata or "{}")
                if metadata.get("is_false_positive", False):
                    false_positives += 1
            except Exception as e:
                continue

        return false_positives / len(memories)

    def _calculate_confidence_interval(self, rate: float, sample_size: int) -> Tuple[float, float]:
        """Calculate 95% confidence interval for false positive rate"""

        if sample_size < 5:
            return (max(0, rate - 0.3), min(1, rate + 0.3))

        # Simple confidence interval calculation
        margin_of_error = 1.96 * (rate * (1 - rate) / sample_size) ** 0.5

        return (
            max(0, rate - margin_of_error),
            min(1, rate + margin_of_error)
        )

    def _estimate_prediction_accuracy(self, recent_rate: float, historical_rate: float, sample_size: int) -> float:
        """Estimate how accurate our prediction is likely to be"""

        # 1. Larger sample size
        # 2. Stable trends
        # 3. Historical consistency

        sample_factor = min(1.0, sample_size / 20.0)  # Improves with more samples
        stability_factor = 1.0 - abs(recent_rate - historical_rate)  # Improves with stability

        base_accuracy = 0.5
        return min(0.95, base_accuracy + (sample_factor * 0.2) + (stability_factor * 0.3))

    async def _analyze_context_influence(
        self,
        issue: Dict,
        file_context: FileContext,
        project_context: Dict
    ) -> float:
        """Analyze how context influences false positive likelihood"""

        try:
            # Get context-specific patterns
            context_patterns = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"context influence {file_context.value} {issue['type']}",
                    namespace="context_rules",
                    limit=20
                )
            )

            context_influence = 0.0
            total_weight = 0.0

            for pattern in context_patterns.memories:
                metadata = json.loads(pattern.metadata or "{}")

                # Weight by pattern confidence and similarity
                weight = metadata.get("confidence", 0.5) * pattern.similarity_score
                influence = metadata.get("context_fp_influence", 0.0)

                context_influence += influence * weight
                total_weight += weight

            if total_weight > 0:
                context_influence /= total_weight

            # Add project-specific influences
            project_type = project_context.get("project_type", "unknown")
            project_influences = {
                "test_project": 0.3,    # Test projects have higher FP tolerance
                "demo_project": 0.4,    # Demo projects often have intentional issues
                "production": -0.2,     # Production code should have fewer FPs
                "library": -0.1,        # Libraries should be clean
                "script": 0.2           # Scripts can be more lenient
            }

            project_influence = project_influences.get(project_type, 0.0)

            return min(1.0, max(-1.0, context_influence + project_influence))

        except Exception as e:
            logger.warning(f"Error analyzing context influence: {e}")
            return 0.0

    async def _analyze_metrics_factors(self, issue: Dict, file_context: FileContext) -> Dict:
        """Analyze metrics-based factors that influence false positive prediction"""

        try:
            metrics_factors = {}

            # 1. Pattern detection effectiveness from metrics
            if self.metrics_collector:
                recent_metrics = self.metrics_collector.get_metrics_summary()

                # Extract relevant metrics
                metrics_factors["detection_accuracy"] = recent_metrics.get("pattern_recognition_accuracy", 0.6)
                metrics_factors["false_positive_rate"] = recent_metrics.get("false_positive_rate", 0.3)
                metrics_factors["analysis_confidence"] = recent_metrics.get("analysis_confidence", 0.7)

            # 2. Pattern frequency analysis
            pattern_frequency = await self._get_pattern_frequency(issue['type'])
            metrics_factors["pattern_frequency"] = pattern_frequency

            # 3. Cross-project validation strength
            cross_project_strength = await self._get_cross_project_validation_strength(issue['type'])
            metrics_factors["cross_project_validation"] = cross_project_strength

            # 4. Recent error rates
            recent_error_rate = await self._get_recent_error_rate(issue['type'])
            metrics_factors["recent_error_rate"] = recent_error_rate

            memory_performance = await self._get_memory_performance_metrics()
            metrics_factors["memory_performance"] = memory_performance

            return metrics_factors

        except Exception as e:
            logger.warning(f"Error analyzing metrics factors: {e}")
            return {"error": str(e)}

    async def _get_pattern_frequency(self, issue_type: str) -> float:
        """Get how frequently this pattern appears (high frequency may indicate over-detection)"""

        try:
            # Count recent detections of this pattern
            recent_detections = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"pattern detection {issue_type}",
                    namespace="",  # Search all namespaces
                    filters={"issue_type": issue_type},
                    limit=1000
                )
            )

            frequency = len(recent_detections.memories)

            # High frequency (>100 detections) suggests possible over-detection
            if frequency > 100:
                return 1.0  # Very high frequency
            elif frequency > 50:
                return 0.7  # High frequency
            elif frequency > 20:
                return 0.4  # Medium frequency
            else:
                return 0.1  # Low frequency

        except Exception as e:
            logger.warning(f"Error getting pattern frequency: {e}")
            return 0.3

    async def _get_cross_project_validation_strength(self, issue_type: str) -> float:
        """Get strength of cross-project validation for this pattern"""

        try:
            # Get validation data from multiple projects
            all_namespaces = await self.memory.list_namespaces()

            validation_scores = []

            for namespace in all_namespaces:
                if namespace.namespace_id == "issue_validations":
                    continue

                validations = await self.memory.search_memories(
                    MemoryQuery(
                        namespace=namespace.namespace_id,
                        semantic_query=f"validation {issue_type}",
                        filters={"issue_type": issue_type},
                        limit=10
                    )
                )

                if validations.memories:
                    # Calculate validation strength for this namespace
                    namespace_strength = len(validations.memories) / 10.0  # Normalize
                    validation_scores.append(min(1.0, namespace_strength))

            if validation_scores:
                return statistics.mean(validation_scores)
            else:
                return 0.0

        except Exception as e:
            logger.warning(f"Error getting cross-project validation strength: {e}")
            return 0.0

    async def _get_recent_error_rate(self, issue_type: str) -> float:
        """Get recent error rate for this pattern type"""

        try:
            # Look for error indicators in recent memories
            recent_errors = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"error validation mistake {issue_type}",
                    namespace="issue_validations",
                    filters={"issue_type": issue_type},
                    limit=50
                )
            )

            total_recent = len(recent_errors.memories)
            error_count = 0

            for memory in recent_errors.memories:
                metadata = json.loads(memory.metadata or "{}")
                if metadata.get("was_error", False) or metadata.get("corrected", False):
                    error_count += 1

            return error_count / max(total_recent, 1)

        except Exception as e:
            logger.warning(f"Error getting recent error rate: {e}")
            return 0.0

    async def _get_memory_performance_metrics(self) -> Dict:
        """Get memory system performance metrics that affect confidence"""

        try:
            # Simulate memory performance metrics
            # In real implementation, this would query actual performance data
            return {
                "query_response_time": 0.05,  # seconds
                "index_accuracy": 0.85,       # semantic search accuracy
                "storage_efficiency": 0.90,   # storage utilization
                "cache_hit_rate": 0.75        # cache effectiveness
            }

        except Exception as e:
            logger.warning(f"Error getting memory performance metrics: {e}")
            return {"error": str(e)}

    async def _analyze_pattern_saturation(self, issue_type: str) -> Dict:
        """Analyze if we have enough examples of this pattern (saturation analysis)"""

        try:
            # Get all memories for this pattern type
            pattern_memories = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"{issue_type} pattern",
                    namespace="",
                    filters={"issue_type": issue_type},
                    limit=1000
                )
            )

            total_patterns = len(pattern_memories.memories)

            # Analyze distribution across contexts
            context_distribution = {}
            confidence_distribution = []

            for memory in pattern_memories.memories:
                metadata = json.loads(memory.metadata or "{}")
                context = metadata.get("file_context", "unknown")
                confidence = metadata.get("confidence", 0.5)

                context_distribution[context] = context_distribution.get(context, 0) + 1
                confidence_distribution.append(confidence)

            # Calculate saturation metrics
            saturation_score = min(1.0, total_patterns / 100.0)  # Saturated at 100+ examples
            context_coverage = len(context_distribution) / 6.0    # 6 main contexts
            avg_confidence = statistics.mean(confidence_distribution) if confidence_distribution else 0.5

            return {
                "saturation_score": saturation_score,
                "total_examples": total_patterns,
                "context_coverage": context_coverage,
                "average_confidence": avg_confidence,
                "context_distribution": context_distribution,
                "is_saturated": saturation_score > self.pattern_saturation_threshold
            }

        except Exception as e:
            logger.warning(f"Error analyzing pattern saturation: {e}")
            return {"error": str(e)}

    def _calculate_prediction(
        self,
        issue: Dict,
        historical_fp_rate: float,
        trend_analysis: PatternTrend,
        context_influence: float,
        metrics_factors: Dict,
        saturation_analysis: Dict
    ) -> FalsePositivePrediction:
        """Calculate the final false positive prediction"""

        # Base prediction from historical rate
        base_prediction = historical_fp_rate

        # Adjust based on trend
        trend_adjustment = 0.0
        if trend_analysis.trend_direction == "increasing":
            trend_adjustment = 0.1  # Higher FP likelihood
        elif trend_analysis.trend_direction == "decreasing":
            trend_adjustment = -0.1  # Lower FP likelihood

        # Apply context influence
        context_adjustment = context_influence * 0.2

        # Apply metrics factors
        metrics_adjustment = 0.0
        if metrics_factors.get("pattern_frequency", 0.3) > 0.7:
            metrics_adjustment += 0.15  # High frequency suggests over-detection

        if metrics_factors.get("cross_project_validation", 0.0) > 0.5:
            metrics_adjustment -= 0.1   # Strong validation reduces FP likelihood

        if metrics_factors.get("recent_error_rate", 0.0) > 0.3:
            metrics_adjustment += 0.1   # High error rate increases FP likelihood

        # Apply saturation analysis
        saturation_adjustment = 0.0
        if saturation_analysis.get("is_saturated", False):
            saturation_adjustment = 0.1  # Saturated patterns more likely to be over-detected

        # Calculate final prediction
        predicted_fp_probability = base_prediction + trend_adjustment + context_adjustment + metrics_adjustment + saturation_adjustment
        predicted_fp_probability = max(0.0, min(1.0, predicted_fp_probability))

        # Calculate confidence based on data quality
        confidence_factors = [
            trend_analysis.prediction_accuracy,
            min(1.0, trend_analysis.sample_size / 20.0),
            1.0 - abs(context_influence),  # More extreme context = less confidence
            metrics_factors.get("analysis_confidence", 0.7)
        ]

        confidence = statistics.mean(confidence_factors)

        # Generate prediction basis
        prediction_basis = [
            f"Historical FP rate: {historical_fp_rate:.2f}",
            f"Trend: {trend_analysis.trend_direction} (recent: {trend_analysis.recent_fp_rate:.2f})",
            f"Context influence: {context_influence:+.2f}",
            f"Pattern frequency: {metrics_factors.get('pattern_frequency', 0.3):.2f}",
            f"Saturation: {'Yes' if saturation_analysis.get('is_saturated', False) else 'No'}"
        ]

        return FalsePositivePrediction(
            issue_type=issue['type'],
            predicted_fp_probability=predicted_fp_probability,
            confidence=confidence,
            prediction_basis=prediction_basis,
            historical_fp_rate=historical_fp_rate,
            trend_analysis=asdict(trend_analysis),
            context_influence=context_influence,
            metrics_factors=metrics_factors,
            recommended_action="",  # Will be filled by _generate_recommendation
            threshold_adjustment=self._calculate_threshold_adjustment(predicted_fp_probability, confidence)
        )

    def _calculate_threshold_adjustment(self, fp_probability: float, confidence: float) -> Optional[float]:
        """Calculate recommended threshold adjustment based on prediction"""

        if confidence < 0.5:
            return None  # Don't adjust if not confident

        if fp_probability > 0.8 and confidence > 0.7:
            return 0.2   # Raise threshold to catch fewer false positives
        elif fp_probability < 0.2 and confidence > 0.7:
            return -0.1  # Lower threshold to catch more issues
        else:
            return None

    def _generate_recommendation(self, prediction: FalsePositivePrediction, metrics_factors: Dict) -> str:
        """Generate recommended action based on prediction"""

        fp_prob = prediction.predicted_fp_probability
        confidence = prediction.confidence

        if fp_prob > 0.8 and confidence > 0.7:
            recommendation = "HIGH FP RISK: Consider auto-flagging as false positive or increasing detection threshold"
        elif fp_prob > 0.6 and confidence > 0.6:
            recommendation = "MEDIUM FP RISK: Recommend manual review with FP warning"
        elif fp_prob < 0.3 and confidence > 0.6:
            recommendation = "LOW FP RISK: High confidence in validity, proceed with normal processing"
        elif confidence < 0.5:
            recommendation = "UNCERTAIN: Insufficient data for confident prediction, use default processing"
        else:
            recommendation = "MODERATE RISK: Standard processing with normal false positive checks"

        # Add metrics-specific recommendations
        if metrics_factors.get("pattern_frequency", 0.3) > 0.8:
            recommendation += " | Consider pattern consolidation due to high frequency"

        if metrics_factors.get("recent_error_rate", 0.0) > 0.4:
            recommendation += " | Review pattern definition due to high error rate"

        prediction.recommended_action = recommendation
        return recommendation

    async def _store_prediction(self, issue: Dict, file_path: str, prediction: FalsePositivePrediction):
        """Store prediction for future learning and validation"""

        try:
            prediction_memory = MemoryEntry(
                namespace="fp_predictions",
                content=f"False positive prediction: {issue['type']} - {prediction.predicted_fp_probability:.2f} probability",
                memory_type="fp_prediction",
                metadata=json.dumps({
                    "issue_type": issue["type"],
                    "file_path": file_path,
                    "predicted_fp_probability": prediction.predicted_fp_probability,
                    "confidence": prediction.confidence,
                    "historical_fp_rate": prediction.historical_fp_rate,
                    "context_influence": prediction.context_influence,
                    "metrics_factors": prediction.metrics_factors,
                    "prediction_date": datetime.now().isoformat(),
                    "prediction_basis": prediction.prediction_basis,
                    "recommended_action": prediction.recommended_action
                }),
                tags=["fp_prediction", "metrics_driven", issue["type"]]
            )

            await self.memory.store_memory(prediction_memory)

        except Exception as e:
            logger.warning(f"Error storing prediction: {e}")

    async def validate_prediction_accuracy(self, days_back: int = 7) -> Dict:
        """Validate prediction accuracy against actual results"""

        try:
            # Get predictions from the specified time period
            cutoff_date = datetime.now() - timedelta(days=days_back)

            predictions = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query="false positive prediction",
                    namespace="fp_predictions",
                    filters={"prediction_date_after": cutoff_date.isoformat()},
                    limit=100
                )
            )

            # Get actual validations for the same period
            validations = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query="user validation feedback",
                    namespace="issue_validations",
                    filters={"validation_date_after": cutoff_date.isoformat()},
                    limit=100
                )
            )

            # Match predictions with actual outcomes
            accuracy_results = []

            for prediction_memory in predictions.memories:
                pred_metadata = json.loads(prediction_memory.metadata or "{}")
                pred_issue_type = pred_metadata.get("issue_type")
                pred_file_path = pred_metadata.get("file_path")
                predicted_prob = pred_metadata.get("predicted_fp_probability", 0.5)

                # Find matching validation
                for validation_memory in validations.memories:
                    val_metadata = json.loads(validation_memory.metadata or "{}")

                    if (val_metadata.get("issue_type") == pred_issue_type and
                        val_metadata.get("file_path") == pred_file_path):

                        actual_fp = val_metadata.get("is_false_positive", False)
                        predicted_fp = predicted_prob > 0.5

                        accuracy_results.append({
                            "predicted_probability": predicted_prob,
                            "predicted_fp": predicted_fp,
                            "actual_fp": actual_fp,
                            "correct": predicted_fp == actual_fp,
                            "error": abs(predicted_prob - (1.0 if actual_fp else 0.0))
                        })
                        break

            # Calculate accuracy metrics
            if accuracy_results:
                total_predictions = len(accuracy_results)
                correct_predictions = sum(1 for r in accuracy_results if r["correct"])
                accuracy = correct_predictions / total_predictions

                mean_error = statistics.mean(r["error"] for r in accuracy_results)

                return {
                    "total_predictions": total_predictions,
                    "correct_predictions": correct_predictions,
                    "accuracy": accuracy,
                    "mean_error": mean_error,
                    "days_analyzed": days_back,
                    "prediction_details": accuracy_results
                }
            else:
                return {"message": "No matching predictions and validations found"}

        except Exception as e:
            logger.error(f"Error validating prediction accuracy: {e}")
            return {"error": str(e)}