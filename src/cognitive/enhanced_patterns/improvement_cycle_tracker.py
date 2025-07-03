#!/usr/bin/env python3
"""
Improvement Cycle Tracker for PRI

This module tracks the complete improvement cycle using metrics:
Error Detection → Pattern Recognition → Fix Application → Validation → Learning

Key Features:
- Full cycle tracking from detection to resolution
- Metrics-driven pattern effectiveness measurement
- Learning pathway optimization
- Fix success rate analysis
- Pattern evolution tracking
- Automated improvement suggestions
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

from ..memory.memory.engine import MemoryEngine
from ..memory.models import MemoryEntry, MemoryQuery
# Try to import metrics models, make optional for testing
try:
    from ...metrics.models import AnalysisMetrics, IntelligenceMetrics, PerformanceMetrics
except ImportError:
    # Fallback for testing - create dummy classes
    from typing import NamedTuple
    class AnalysisMetrics(NamedTuple):
        files_analyzed: int = 0
        issues_found: int = 0
        complexity_score: float = 0.0
        test_coverage_pct: float = 0.0

    class IntelligenceMetrics(NamedTuple):
        memory_entries: int = 0
        recursive_cycles: int = 0
        improvement_suggestions: int = 0

    class PerformanceMetrics(NamedTuple):
        response_time_ms: float = 0.0
        throughput_rps: float = 0.0
        error_rate: float = 0.0
        uptime_pct: float = 0.0
from .context_analyzer import FileContext

logger = logging.getLogger(__name__)


class ImprovementStage(Enum):
    """Stages in the improvement cycle"""


class CycleStatus(Enum):
    """Status of improvement cycle"""


@dataclass
class ImprovementCycle:
    """Represents a complete improvement cycle"""
    cycle_id: str
    issue_type: str
    file_path: str
    file_context: str
    detection_date: str
    current_stage: ImprovementStage
    status: CycleStatus

    # Stage timestamps
    detection_timestamp: Optional[str] = None
    pattern_recognition_timestamp: Optional[str] = None
    fix_suggestion_timestamp: Optional[str] = None
    fix_application_timestamp: Optional[str] = None
    validation_timestamp: Optional[str] = None
    learning_timestamp: Optional[str] = None

    # Stage results
    detection_confidence: float = 0.0
    pattern_match_score: float = 0.0
    fix_quality_score: float = 0.0
    validation_success: bool = False
    learning_insights: List[str] = None

    # Metrics
    total_cycle_time_hours: float = 0.0
    user_interaction_count: int = 0
    false_positive_flag: bool = False
    improvement_effectiveness: float = 0.0


@dataclass
class CycleMetrics:
    """Aggregated metrics across improvement cycles"""
    total_cycles: int
    completed_cycles: int
    success_rate: float
    average_cycle_time_hours: float
    common_failure_points: Dict[str, int]
    pattern_effectiveness_by_type: Dict[str, float]
    learning_velocity: float
    fix_application_rate: float


class ImprovementCycleTracker:
    """
    Tracks the complete improvement cycle using metrics to identify
    patterns in how errors are detected, fixed, and learned from.

    This enables:
    1. Optimization of detection patterns based on fix success rates
    2. Identification of common failure points in the improvement process
    3. Pattern evolution based on real-world effectiveness
    4. Automated suggestion of new improvement strategies
    """

    def __init__(self, memory_engine: MemoryEngine, metrics_collector=None):
        self.memory = memory_engine
        self.metrics_collector = metrics_collector
        self.cycle_namespace = "improvement_cycles"
        self.learning_namespace = "cycle_learning"

        # Initialize namespaces
        self._initialize_namespaces()

        # Tracking configuration
        self.min_cycle_time_minutes = 1  # Minimum time to consider a valid cycle
        self.max_cycle_time_days = 30    # Maximum time before marking cycle as abandoned

    def _initialize_namespaces(self):
        """Initialize memory namespaces for cycle tracking"""
        try:
            # These would be created by the memory system
            pass
        except Exception as e:
            logger.debug(f"Namespace initialization: {e}")

    async def start_improvement_cycle(
        self,
        issue: Dict,
        file_path: str,
        detection_context: Dict
    ) -> str:
        """Start tracking a new improvement cycle"""

        cycle_id = f"cycle_{datetime.now().strftime('%Y%m%d_%H%M%S")}_{hash(file_path)}_{issue['type']}"

        file_context = detection_context.get("file_context", "unknown")

        cycle = ImprovementCycle(
            cycle_id=cycle_id,
            issue_type=issue["type"],
            file_path=file_path,
            file_context=file_context,
            detection_date=datetime.now().isoformat(),
            current_stage=ImprovementStage.DETECTION,
            status=CycleStatus.IN_PROGRESS,
            detection_timestamp=datetime.now().isoformat(),
            detection_confidence=issue.get("confidence", 0.5)
        )

        # Store cycle in memory
        await self._store_cycle(cycle)

        logger.info(f"Started improvement cycle {cycle_id} for {issue['type']} in {file_path}")
        return cycle_id

    async def advance_cycle_stage(
        self,
        cycle_id: str,
        new_stage: ImprovementStage,
        stage_data: Dict
    ) -> bool:
        """Advance a cycle to the next stage with stage-specific data"""

        try:
            # Get current cycle
            cycle = await self._get_cycle(cycle_id)
            if not cycle:
                logger.warning(f"Cycle {cycle_id} not found")
                return False

            # Update stage and timestamp
            cycle.current_stage = new_stage
            current_time = datetime.now().isoformat()

            # Update stage-specific data
            if new_stage == ImprovementStage.PATTERN_RECOGNITION:
                cycle.pattern_recognition_timestamp = current_time
                cycle.pattern_match_score = stage_data.get("pattern_match_score", 0.0)

            elif new_stage == ImprovementStage.FIX_SUGGESTION:
                cycle.fix_suggestion_timestamp = current_time
                cycle.fix_quality_score = stage_data.get("fix_quality_score", 0.0)

            elif new_stage == ImprovementStage.FIX_APPLICATION:
                cycle.fix_application_timestamp = current_time
                cycle.user_interaction_count += stage_data.get("user_interactions", 0)

            elif new_stage == ImprovementStage.VALIDATION:
                cycle.validation_timestamp = current_time
                cycle.validation_success = stage_data.get("validation_success", False)
                cycle.false_positive_flag = stage_data.get("is_false_positive", False)

            elif new_stage == ImprovementStage.LEARNING:
                cycle.learning_timestamp = current_time
                cycle.learning_insights = stage_data.get("learning_insights", [])

                # Calculate cycle completion metrics
                if cycle.detection_timestamp:
                    start_time = datetime.fromisoformat(cycle.detection_timestamp.replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(current_time.replace('Z', '+00:00'))
                    cycle.total_cycle_time_hours = (end_time - start_time).total_seconds() / 3600

                # Calculate improvement effectiveness
                cycle.improvement_effectiveness = self._calculate_improvement_effectiveness(cycle, stage_data)

                # Mark cycle as completed
                cycle.status = CycleStatus.COMPLETED

            # Store updated cycle
            await self._store_cycle(cycle)

            # Update metrics if available
            if self.metrics_collector:
                await self._update_cycle_metrics(cycle, new_stage, stage_data)

            logger.info(f"Advanced cycle {cycle_id} to stage {new_stage.value}")
            return True

        except Exception as e:
            logger.error(f"Error advancing cycle {cycle_id} to {new_stage}: {e}")
            return False

    def _calculate_improvement_effectiveness(self, cycle: ImprovementCycle, stage_data: Dict) -> float:
        """Calculate overall improvement effectiveness for the cycle"""

        factors = []

        # Detection quality
        if cycle.detection_confidence > 0:
            factors.append(cycle.detection_confidence)

        # Pattern recognition quality
        if cycle.pattern_match_score > 0:
            factors.append(cycle.pattern_match_score)

        # Fix quality
        if cycle.fix_quality_score > 0:
            factors.append(cycle.fix_quality_score)

        # Validation success
        if cycle.validation_success and not cycle.false_positive_flag:
            factors.append(1.0)
        elif cycle.false_positive_flag:
            factors.append(0.0)  # False positive significantly reduces effectiveness
        else:
            factors.append(0.5)

        if cycle.total_cycle_time_hours > 0:
            time_efficiency = max(0.1, 1.0 - (cycle.total_cycle_time_hours / 24.0))  # Penalize cycles >24h
            factors.append(time_efficiency)

        if cycle.user_interaction_count == 0:
            factors.append(1.0)  # Fully automated
        elif cycle.user_interaction_count <= 2:
            factors.append(0.8)  # Minimal interaction
        else:
            factors.append(max(0.3, 1.0 - (cycle.user_interaction_count * 0.1)))

        return statistics.mean(factors) if factors else 0.0

    async def _store_cycle(self, cycle: ImprovementCycle):
        """Store cycle data in memory"""

        try:
            # Convert cycle to dict and handle enum serialization
            cycle_dict = asdict(cycle)
            cycle_dict['current_stage'] = cycle.current_stage.value
            cycle_dict['status'] = cycle.status.value

            cycle_memory = MemoryEntry(
                namespace=self.cycle_namespace,
                content=f"Improvement cycle: {cycle.issue_type} in {cycle.file_context} - Stage: {cycle.current_stage.value}",
                memory_type="improvement_cycle",
                metadata=json.dumps(cycle_dict),
                tags=["improvement_cycle", cycle.issue_type, cycle.file_context, cycle.current_stage.value]
            )

            await self.memory.store_memory(cycle_memory)

        except Exception as e:
            logger.error(f"Error storing cycle {cycle.cycle_id}: {e}")

    async def _get_cycle(self, cycle_id: str) -> Optional[ImprovementCycle]:
        """Retrieve cycle data from memory"""

        try:
            cycles = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query=f"improvement cycle {cycle_id}",
                    namespace=self.cycle_namespace,
                    filters={"memory_type": "improvement_cycle"},
                    limit=1
                )
            )

            if cycles.memories:
                metadata = json.loads(cycles.memories[0].metadata or "{}")
                # Convert string enum values back to enums
                if 'current_stage' in metadata:
                    metadata['current_stage'] = ImprovementStage(metadata['current_stage'])
                if 'status' in metadata:
                    metadata['status'] = CycleStatus(metadata['status'])
                return ImprovementCycle(**metadata)

            return None

        except Exception as e:
            logger.error(f"Error retrieving cycle {cycle_id}: {e}")
            return None

    async def _update_cycle_metrics(self, cycle: ImprovementCycle, stage: ImprovementStage, stage_data: Dict):
        """Update metrics based on cycle progression"""

        if not self.metrics_collector:
            return

        try:
            # Update intelligence metrics
            if stage == ImprovementStage.LEARNING:
                # Increment learning cycles
                self.metrics_collector.analysis_metrics['recursive_cycles'] += 1

                # Track improvement effectiveness
                if cycle.improvement_effectiveness > 0.7:
                    self.metrics_collector.analysis_metrics['high_quality_improvements'] = \
                        self.metrics_collector.analysis_metrics.get('high_quality_improvements', 0) + 1

            # Update performance metrics
            if stage == ImprovementStage.FIX_APPLICATION:
                if stage_data.get("validation_success", False):
                    self.metrics_collector.analysis_metrics['fixes_applied'] += 1

            # Update analysis metrics
            if stage == ImprovementStage.VALIDATION:
                if cycle.false_positive_flag:
                    self.metrics_collector.analysis_metrics['false_positives_detected'] = \
                        self.metrics_collector.analysis_metrics.get('false_positives_detected', 0) + 1

        except Exception as e:
            logger.warning(f"Error updating cycle metrics: {e}")

    async def analyze_cycle_patterns(self, days_back: int = 30) -> CycleMetrics:
        """Analyze patterns across improvement cycles"""

        try:
            # Get cycles from the specified period
            cutoff_date = datetime.now() - timedelta(days=days_back)

            cycles_data = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query="improvement cycle",
                    namespace=self.cycle_namespace,
                    filters={
                        "memory_type": "improvement_cycle",
                        "detection_date_after": cutoff_date.isoformat()
                    },
                    limit=1000
                )
            )

            if not cycles_data.memories:
                return CycleMetrics(
                    total_cycles=0,
                    completed_cycles=0,
                    success_rate=0.0,
                    average_cycle_time_hours=0.0,
                    common_failure_points={},
                    pattern_effectiveness_by_type={},
                    learning_velocity=0.0,
                    fix_application_rate=0.0
                )

            # Parse cycles
            cycles = []
            for memory in cycles_data.memories:
                try:
                    metadata = json.loads(memory.metadata or "{}")
                    cycles.append(ImprovementCycle(**metadata))
                except Exception as e:
                    logger.warning(f"Error parsing cycle data: {e}")

            # Analyze patterns
            total_cycles = len(cycles)
            completed_cycles = len([c for c in cycles if c.status == CycleStatus.COMPLETED])
            successful_cycles = len([c for c in cycles if c.validation_success and not c.false_positive_flag])

            success_rate = successful_cycles / max(total_cycles, 1)

            # Calculate average cycle time
            completed_with_time = [c for c in cycles if c.status == CycleStatus.COMPLETED and c.total_cycle_time_hours > 0]
            average_cycle_time = statistics.mean([c.total_cycle_time_hours for c in completed_with_time]) if completed_with_time else 0.0

            # Identify common failure points
            failure_points = {}
            for cycle in cycles:
                if cycle.status == CycleStatus.FAILED:
                    failure_stage = cycle.current_stage.value
                    failure_points[failure_stage] = failure_points.get(failure_stage, 0) + 1

            # Calculate pattern effectiveness by type
            pattern_effectiveness = {}
            issue_types = set(c.issue_type for c in cycles)

            for issue_type in issue_types:
                type_cycles = [c for c in cycles if c.issue_type == issue_type]
                type_successful = len([c for c in type_cycles if c.validation_success and not c.false_positive_flag])
                effectiveness = type_successful / max(len(type_cycles), 1)
                pattern_effectiveness[issue_type] = effectiveness

            learning_velocity = completed_cycles / max(days_back, 1)

            # Calculate fix application rate
            fix_applied_cycles = len([c for c in cycles if c.fix_application_timestamp])
            fix_application_rate = fix_applied_cycles / max(total_cycles, 1)

            return CycleMetrics(
                total_cycles=total_cycles,
                completed_cycles=completed_cycles,
                success_rate=success_rate,
                average_cycle_time_hours=average_cycle_time,
                common_failure_points=failure_points,
                pattern_effectiveness_by_type=pattern_effectiveness,
                learning_velocity=learning_velocity,
                fix_application_rate=fix_application_rate
            )

        except Exception as e:
            logger.error(f"Error analyzing cycle patterns: {e}")
            return CycleMetrics(
                total_cycles=0,
                completed_cycles=0,
                success_rate=0.0,
                average_cycle_time_hours=0.0,
                common_failure_points={},
                pattern_effectiveness_by_type={},
                learning_velocity=0.0,
                fix_application_rate=0.0
            )

    async def identify_improvement_opportunities(self) -> List[Dict]:
        """Identify opportunities to improve the improvement cycle based on metrics"""

        cycle_metrics = await self.analyze_cycle_patterns()
        opportunities = []

        # Low success rate opportunities
        if cycle_metrics.success_rate < 0.7:
            opportunities.append({
                "type": "success_rate_improvement",
                "priority": "high",
                "description": f"Success rate is {cycle_metrics.success_rate:.1%} - below target of 70%",
                "suggestions": [
                    "Review pattern recognition accuracy",
                    "Improve fix quality scoring",
                    "Enhance validation processes"
                ]
            })

        # Slow cycle time opportunities
        if cycle_metrics.average_cycle_time_hours > 8:
            opportunities.append({
                "type": "cycle_time_optimization",
                "priority": "medium",
                "description": f"Average cycle time is {cycle_metrics.average_cycle_time_hours:.1f} hours - above target",
                "suggestions": [
                    "Automate more stages of the improvement process",
                    "Optimize pattern matching algorithms",
                    "Streamline user interaction workflows"
                ]
            })

        # Common failure point opportunities
        if cycle_metrics.common_failure_points:
            most_common_failure = max(cycle_metrics.common_failure_points.items(), key=lambda x: x[1])
            opportunities.append({
                "type": "failure_point_reduction",
                "priority": "high",
                "description": f"Most cycles fail at {most_common_failure[0]} stage ({most_common_failure[1]} failures)",
                "suggestions": [
                    f"Investigate and improve {most_common_failure[0]} stage reliability",
                    "Add additional validation at this stage",
                    "Provide better error recovery mechanisms"
                ]
            })

        # Low effectiveness patterns
        if cycle_metrics.pattern_effectiveness_by_type:
            low_effectiveness_patterns = {
                pattern: eff for pattern, eff in cycle_metrics.pattern_effectiveness_by_type.items()
                if eff < 0.5
            }

            if low_effectiveness_patterns:
                opportunities.append({
                    "type": "pattern_effectiveness_improvement",
                    "priority": "medium",
                    "description": f"Patterns with low effectiveness: {list(low_effectiveness_patterns.keys())}",
                    "suggestions": [
                        "Retrain detection algorithms for low-performing patterns",
                        "Gather more training data for these pattern types",
                        "Consider removing or consolidating ineffective patterns"
                    ]
                })

        # Learning velocity opportunities
        if cycle_metrics.learning_velocity < 1.0:  # Less than 1 completed cycle per day
            opportunities.append({
                "type": "learning_velocity_improvement",
                "priority": "low",
                "description": f"Learning velocity is {cycle_metrics.learning_velocity:.2f} cycles/day - below optimal",
                "suggestions": [
                    "Increase automated cycle completion",
                    "Reduce manual intervention requirements",
                    "Optimize memory storage and retrieval"
                ]
            })

        return opportunities

    async def detect_manual_fixes_in_scan(self, current_scan_issues: List[Dict], project_path: str) -> List[Dict]:
        """Detect manual fixes by comparing current scan with previous improvement cycles"""

        manual_fixes_detected = []

        try:
            # Get all incomplete cycles from the last 30 days
            cutoff_date = datetime.now() - timedelta(days=30)

            incomplete_cycles = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query="improvement cycle in_progress",
                    namespace=self.cycle_namespace,
                    filters={
                        "memory_type": "improvement_cycle",
                        "detection_date_after": cutoff_date.isoformat()
                    },
                    limit=1000
                )
            )

            if not incomplete_cycles.memories:
                return manual_fixes_detected

            # Parse cycle data
            active_cycles = []
            for memory in incomplete_cycles.memories:
                try:
                    metadata = json.loads(memory.metadata or "{}")
                    cycle = ImprovementCycle(**metadata)
                    if cycle.status == CycleStatus.IN_PROGRESS:
                        active_cycles.append(cycle)
                except Exception as e:
                    logger.warning(f"Error parsing cycle data: {e}")

            # Create issue signature from current scan for comparison
            current_issue_signatures = set()
            for issue in current_scan_issues:
                signature = self._create_issue_signature(issue, project_path)
                current_issue_signatures.add(signature)

            # Check each active cycle to see if the issue still exists
            for cycle in active_cycles:
                cycle_signature = self._create_cycle_signature(cycle, project_path)

                if cycle_signature not in current_issue_signatures:
                    # Issue is no longer present - likely manually fixed
                    manual_fix = await self._process_manual_fix_detection(cycle, project_path)
                    if manual_fix:
                        manual_fixes_detected.append(manual_fix)

            logger.info(f"Detected {len(manual_fixes_detected)} manual fixes in current scan")
            return manual_fixes_detected

        except Exception as e:
            logger.error(f"Error detecting manual fixes: {e}")
            return []

    def _create_issue_signature(self, issue: Dict, project_path: str) -> str:
        """Create a signature for an issue to enable comparison across scans"""

        # Normalize file path relative to project
        file_path = issue.get('file_path', issue.get('file', ''))
        if file_path.startswith(project_path):
            file_path = file_path[len(project_path):].lstrip('/')

        # Create signature from key identifying features
        signature_parts = [
            issue.get('type', 'unknown'),
            file_path,
            str(issue.get('line', 0)),
            issue.get('description', '')[:100]  # First 100 chars of description
        ]

        return '|'.join(signature_parts)

    def _create_cycle_signature(self, cycle: ImprovementCycle, project_path: str) -> str:
        """Create a signature for a cycle to match against current issues"""

        # Normalize file path
        file_path = cycle.file_path
        if file_path.startswith(project_path):
            file_path = file_path[len(project_path):].lstrip('/')

        # Create signature similar to issue signature
        signature_parts = [
            cycle.issue_type,
            file_path,
            str(0),  # Line number not stored in cycle
            ''  # Description not easily available
        ]

        return '|'.join(signature_parts)

    async def _process_manual_fix_detection(self, cycle: ImprovementCycle, project_path: str) -> Optional[Dict]:
        """Process detection of a manual fix and update the cycle"""

        try:
            # Update cycle to mark manual fix completion
            await self.advance_cycle_stage(
                cycle.cycle_id,
                ImprovementStage.VALIDATION,
                {
                    "validation_success": True,
                    "is_false_positive": False,
                    "manual_fix_detected": True,
                    "fix_type": "manual_intervention"
                }
            )

            # Complete the learning stage
            learning_insights = [
                f"Manual fix detected for {cycle.issue_type}",
                f"Issue resolved outside of automated cycle",
                f"Manual intervention was effective for {cycle.file_context} context"
            ]

            await self.advance_cycle_stage(
                cycle.cycle_id,
                ImprovementStage.LEARNING,
                {
                    "learning_insights": learning_insights,
                    "manual_fix_confirmed": True,
                    "improvement_method": "manual_intervention"
                }
            )

            # Return manual fix detection info
            return {
                "cycle_id": cycle.cycle_id,
                "issue_type": cycle.issue_type,
                "file_path": cycle.file_path,
                "file_context": cycle.file_context,
                "detection_date": cycle.detection_date,
                "manual_fix_detected_date": datetime.now().isoformat(),
                "fix_type": "manual_intervention",
                "effectiveness_estimated": 1.0,  # Assume manual fixes are effective
                "learning_insights": learning_insights
            }

        except Exception as e:
            logger.error(f"Error processing manual fix detection for cycle {cycle.cycle_id}: {e}")
            return None

    async def track_scan_comparison_metrics(self, previous_issues: List[Dict], current_issues: List[Dict], project_path: str) -> Dict:
        """Track metrics comparing scans to identify patterns in manual vs automated fixes"""

        try:
            # Detect manual fixes
            manual_fixes = await self.detect_manual_fixes_in_scan(current_issues, project_path)

            # Calculate metrics
            previous_count = len(previous_issues)
            current_count = len(current_issues)
            resolved_count = max(0, previous_count - current_count)
            manual_fix_count = len(manual_fixes)
            automated_fix_count = max(0, resolved_count - manual_fix_count)

            # Calculate rates
            manual_fix_rate = manual_fix_count / max(resolved_count, 1)
            automated_fix_rate = automated_fix_count / max(resolved_count, 1)

            # Analyze issue types being manually fixed
            manual_fix_types = {}
            for fix in manual_fixes:
                issue_type = fix.get('issue_type', 'unknown')
                manual_fix_types[issue_type] = manual_fix_types.get(issue_type, 0) + 1

            scan_metrics = {
                "previous_issues_count": previous_count,
                "current_issues_count": current_count,
                "total_resolved": resolved_count,
                "manual_fixes_detected": manual_fix_count,
                "automated_fixes_estimated": automated_fix_count,
                "manual_fix_rate": manual_fix_rate,
                "automated_fix_rate": automated_fix_rate,
                "manual_fix_types_breakdown": manual_fix_types,
                "scan_comparison_date": datetime.now().isoformat()
            }

            # Store scan comparison metrics in memory
            scan_memory = MemoryEntry(
                namespace=self.cycle_namespace,
                content=f"Scan comparison: {manual_fix_count} manual fixes detected, {automated_fix_count} automated fixes",
                memory_type="scan_comparison_metrics",
                metadata=json.dumps(scan_metrics),
                tags=["scan_comparison", "manual_fixes", "metrics"]
            )

            await self.memory.store_memory(scan_memory)

            logger.info(f"Scan comparison metrics: {manual_fix_count} manual, {automated_fix_count} automated fixes")
            return scan_metrics

        except Exception as e:
            logger.error(f"Error tracking scan comparison metrics: {e}")
            return {}

    async def get_manual_fix_patterns(self, days_back: int = 30) -> Dict:
        """Analyze patterns in manual fixes to identify automation opportunities"""

        try:
            # Get manual fix records
            cutoff_date = datetime.now() - timedelta(days=days_back)

            manual_fix_cycles = await self.memory.search_memories(
                MemoryQuery(
                    semantic_query="manual fix detected improvement cycle",
                    namespace=self.cycle_namespace,
                    filters={
                        "memory_type": "improvement_cycle",
                        "detection_date_after": cutoff_date.isoformat()
                    },
                    limit=1000
                )
            )

            manual_fixes = []
            for memory in manual_fix_cycles.memories:
                try:
                    metadata = json.loads(memory.metadata or "{}")
                    cycle = ImprovementCycle(**metadata)

                    # Check if this was a manual fix
                    if (cycle.status == CycleStatus.COMPLETED and
                        hasattr(cycle, 'learning_insights') and
                        cycle.learning_insights and
                        any("manual fix" in insight.lower() for insight in cycle.learning_insights)):
                        manual_fixes.append(cycle)

                except Exception as e:
                    logger.warning(f"Error parsing manual fix cycle: {e}")

            if not manual_fixes:
                return {"message": "No manual fixes detected in the specified period"}

            # Analyze patterns
            patterns = {
                "total_manual_fixes": len(manual_fixes),
                "issue_types": {},
                "file_contexts": {},
                "common_fix_times": [],
                "automation_opportunities": []
            }

            # Group by issue type and context
            for fix in manual_fixes:
                # Issue type analysis
                issue_type = fix.issue_type
                if issue_type not in patterns["issue_types"]:
                    patterns["issue_types"][issue_type] = {"count": 0, "contexts": set()}
                patterns["issue_types"][issue_type]["count"] += 1
                patterns["issue_types"][issue_type]["contexts"].add(fix.file_context)

                # File context analysis
                context = fix.file_context
                patterns["file_contexts"][context] = patterns["file_contexts"].get(context, 0) + 1

                # Fix timing
                if fix.total_cycle_time_hours > 0:
                    patterns["common_fix_times"].append(fix.total_cycle_time_hours)

            # Convert sets to lists for JSON serialization
            for issue_type_data in patterns["issue_types"].values():
                issue_type_data["contexts"] = list(issue_type_data["contexts"])

            # Identify automation opportunities
            for issue_type, data in patterns["issue_types"].items():
                if data["count"] >= 3:  # 3+ manual fixes of same type
                    patterns["automation_opportunities"].append({
                        "issue_type": issue_type,
                        "frequency": data["count"],
                        "contexts": data["contexts"],
                        "automation_potential": "high" if data["count"] >= 5 else "medium",
                        "recommendation": f"Consider automating {issue_type} detection and fixing"
                    })

            # Calculate average manual fix time
            if patterns["common_fix_times"]:
                patterns["average_manual_fix_time_hours"] = statistics.mean(patterns["common_fix_times"])
                patterns["median_manual_fix_time_hours"] = statistics.median(patterns["common_fix_times"])

            return patterns

        except Exception as e:
            logger.error(f"Error analyzing manual fix patterns: {e}")
            return {"error": str(e)}

    async def generate_cycle_learning_insights(self, cycle_id: str) -> List[str]:
        """Generate learning insights from a completed cycle"""

        cycle = await self._get_cycle(cycle_id)
        if not cycle or cycle.status != CycleStatus.COMPLETED:
            return []

        insights = []

        # Effectiveness insights
        if cycle.improvement_effectiveness > 0.8:
            insights.append(f"High-effectiveness cycle: {cycle.issue_type} pattern works well in {cycle.file_context} context")
        elif cycle.improvement_effectiveness < 0.3:
            insights.append(f"Low-effectiveness cycle: {cycle.issue_type} pattern needs improvement for {cycle.file_context} context")

        # Time efficiency insights
        if cycle.total_cycle_time_hours < 1:
            insights.append(f"Fast resolution: {cycle.issue_type} can be resolved quickly - consider automation")
        elif cycle.total_cycle_time_hours > 24:
            insights.append(f"Slow resolution: {cycle.issue_type} requires extended time - investigate bottlenecks")

        # User interaction insights
        if cycle.user_interaction_count == 0:
            insights.append(f"Fully automated: {cycle.issue_type} successfully resolved without user intervention")
        elif cycle.user_interaction_count > 5:
            insights.append(f"High user interaction: {cycle.issue_type} requires significant manual intervention - consider automation")

        # False positive insights
        if cycle.false_positive_flag:
            insights.append(f"False positive: {cycle.issue_type} pattern incorrectly triggered in {cycle.file_context} - adjust detection")

        # Pattern matching insights
        if cycle.pattern_match_score > 0.9:
            insights.append(f"Excellent pattern match: {cycle.issue_type} detection is highly accurate")
        elif cycle.pattern_match_score < 0.5:
            insights.append(f"Poor pattern match: {cycle.issue_type} detection needs refinement")

        return insights