"""
Data models for learning analytics skill.

Defines Pydantic models for:
- Velocity metrics
- Struggle detection
- Checkpoint performance
- Learning patterns
- Time estimation
- Recommendations
- Comprehensive analytics output
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# Enums
# ============================================================================

class StruggleIndicator(str, Enum):
    """Types of struggle indicators"""
    LONG_DURATION = "long_duration"
    MULTIPLE_ATTEMPTS = "multiple_attempts"
    CHECKPOINT_FAILED = "checkpoint_failed"
    STUCK = "stuck"
    DEPENDENCY_BLOCKED = "dependency_blocked"


class PatternType(str, Enum):
    """Types of learning patterns"""
    PRODUCTIVE_TIME = "productive_time"
    TASK_SEQUENCING = "task_sequencing"
    BREAK_PATTERN = "break_pattern"
    STRUGGLE_THEN_SUCCESS = "struggle_then_success"
    STEADY_PROGRESS = "steady_progress"
    BURST_PROGRESS = "burst_progress"


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationType(str, Enum):
    """Types of recommendations"""
    PACE_ADJUSTMENT = "pace_adjustment"
    SPECIALIST_CONSULTATION = "specialist_consultation"
    CONCEPT_REVIEW = "concept_review"
    BREAK_SUGGESTION = "break_suggestion"
    CELEBRATION = "celebration"
    TASK_REORDERING = "task_reordering"
    DIFFICULTY_ADJUSTMENT = "difficulty_adjustment"


# ============================================================================
# Velocity Metrics
# ============================================================================

class VelocityMetrics(BaseModel):
    """Learning velocity metrics"""

    tasks_per_week: float = Field(
        description="Average tasks completed per week"
    )
    tasks_completed_total: int = Field(
        description="Total tasks completed"
    )

    days_active: int = Field(
        description="Number of days with activity"
    )
    average_task_duration_hours: Optional[float] = Field(
        default=None,
        description="Average time to complete a task (if timestamps available)"
    )

    velocity_trend: str = Field(
        description="Trend direction: increasing, stable, decreasing"
    )
    recent_velocity: float = Field(
        description="Tasks per week in last 2 weeks"
    )
    overall_velocity: float = Field(
        description="Tasks per week over entire learning period"
    )

    estimated_completion_date: Optional[str] = Field(
        default=None,
        description="Predicted completion date based on current velocity"
    )
    on_track: bool = Field(
        description="Whether student is on track to meet estimated time"
    )


# ============================================================================
# Struggle Detection
# ============================================================================

class StruggleArea(BaseModel):
    """Represents an area where student is struggling"""

    task_id: str = Field(description="ID of the struggling task")
    task_title: str = Field(description="Title of the task")
    phase_number: int = Field(description="Which phase this task is in")

    indicators: List[StruggleIndicator] = Field(
        description="Types of struggle detected"
    )

    severity: str = Field(
        description="Severity level: minor, moderate, severe"
    )

    duration_days: Optional[int] = Field(
        default=None,
        description="How many days student has been on this task"
    )

    expected_duration_days: Optional[int] = Field(
        default=None,
        description="Expected duration for this task"
    )

    recommendation: str = Field(
        description="Suggested action to address struggle"
    )

    specialist_suggestion: Optional[str] = Field(
        default=None,
        description="Which specialist agent might help"
    )


# ============================================================================
# Checkpoint Performance
# ============================================================================

class CheckpointPerformance(BaseModel):
    """Performance on learning checkpoints"""

    checkpoint_id: str
    checkpoint_title: str
    phase_number: int

    status: str = Field(description="PASSED, FAILED, NOT_ATTEMPTED")

    attempt_count: int = Field(
        default=1,
        description="Number of attempts (if trackable)"
    )

    passed_on_first_try: bool = Field(
        description="Whether checkpoint passed on first attempt"
    )

    time_to_pass_days: Optional[int] = Field(
        default=None,
        description="Days from phase start to checkpoint pass"
    )

    related_struggle_areas: List[str] = Field(
        default_factory=list,
        description="Task IDs student struggled with before checkpoint"
    )


class CheckpointAnalysis(BaseModel):
    """Overall checkpoint performance analysis"""

    total_checkpoints: int
    passed_checkpoints: int
    failed_checkpoints: int
    not_attempted_checkpoints: int

    pass_rate: float = Field(
        description="Percentage of attempted checkpoints passed"
    )

    first_try_pass_rate: float = Field(
        description="Percentage passed on first attempt"
    )

    checkpoint_performances: List[CheckpointPerformance] = Field(
        default_factory=list,
        description="Individual checkpoint details"
    )

    patterns: List[str] = Field(
        default_factory=list,
        description="Detected patterns in checkpoint performance"
    )


# ============================================================================
# Learning Patterns
# ============================================================================

class LearningPattern(BaseModel):
    """Detected learning pattern"""

    pattern_type: PatternType

    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence in pattern detection (0-1)"
    )

    description: str = Field(
        description="Human-readable pattern description"
    )

    evidence: List[str] = Field(
        description="Evidence supporting this pattern"
    )

    recommendation: str = Field(
        description="How to leverage or improve this pattern"
    )

    impact: str = Field(
        description="Impact level: positive, neutral, negative"
    )


# ============================================================================
# Time Estimation
# ============================================================================

class TimeEstimationAnalysis(BaseModel):
    """Analysis of time estimation accuracy"""

    estimated_total_weeks: Optional[float] = Field(
        default=None,
        description="Original time estimate from plan"
    )

    actual_weeks_so_far: float = Field(
        description="Actual time elapsed in weeks"
    )

    projected_total_weeks: Optional[float] = Field(
        default=None,
        description="Projected total time based on current velocity"
    )

    estimation_accuracy: Optional[str] = Field(
        default=None,
        description="Accurate, optimistic, pessimistic"
    )

    variance_percentage: Optional[float] = Field(
        default=None,
        description="Percentage difference between estimated and projected"
    )

    task_estimate_accuracy: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-task estimation accuracy (task_id -> accuracy ratio)"
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving estimates"
    )


# ============================================================================
# Recommendations
# ============================================================================

class LearningRecommendation(BaseModel):
    """Actionable recommendation for teaching optimization"""

    priority: RecommendationPriority
    recommendation_type: RecommendationType

    title: str = Field(description="Short recommendation title")

    description: str = Field(
        description="Detailed recommendation description"
    )

    rationale: str = Field(
        description="Why this recommendation is being made"
    )

    suggested_action: str = Field(
        description="Specific action to take"
    )

    target_agent: Optional[str] = Field(
        default=None,
        description="Which agent should act on this (learning-coordinator, etc.)"
    )

    expected_impact: str = Field(
        description="Expected positive outcome"
    )

    evidence: List[str] = Field(
        default_factory=list,
        description="Data points supporting this recommendation"
    )


# ============================================================================
# Comprehensive Analytics
# ============================================================================

class LearningAnalytics(BaseModel):
    """Comprehensive learning analytics"""

    # Metadata
    plan_title: str
    student_name: Optional[str] = None
    analysis_date: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )

    # Core metrics
    velocity_metrics: VelocityMetrics
    struggle_areas: List[StruggleArea] = Field(default_factory=list)
    checkpoint_analysis: CheckpointAnalysis
    time_estimation: TimeEstimationAnalysis

    # Pattern analysis
    learning_patterns: List[LearningPattern] = Field(default_factory=list)

    # Recommendations
    recommendations: List[LearningRecommendation] = Field(
        default_factory=list,
        description="Sorted by priority"
    )

    # Summary
    overall_health: str = Field(
        description="Overall learning health: excellent, good, needs_attention, struggling"
    )

    key_insights: List[str] = Field(
        default_factory=list,
        description="Top 3-5 key insights from analysis"
    )

    strengths: List[str] = Field(
        default_factory=list,
        description="Student's demonstrated strengths"
    )

    growth_areas: List[str] = Field(
        default_factory=list,
        description="Areas for growth and improvement"
    )
