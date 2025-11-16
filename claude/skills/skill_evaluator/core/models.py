"""
Core data models for skill evaluator.

This module defines the data structures used throughout the skill evaluator system.
"""

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, List
from enum import Enum


class ImprovementCategory(str, Enum):
    """Categories for improvement suggestions."""
    PERFORMANCE = "performance"
    QUALITY = "quality"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    SECURITY = "security"
    DOCUMENTATION = "documentation"


class ImprovementSeverity(str, Enum):
    """Severity levels for improvements."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class HealthTrend(str, Enum):
    """Health trend indicators."""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    UNKNOWN = "unknown"


@dataclass
class ImprovementSuggestion:
    """A suggestion for improving a skill."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: str = ImprovementCategory.QUALITY.value
    severity: str = ImprovementSeverity.MEDIUM.value
    description: str = ""
    location: str = ""  # file:line_number
    current_code: Optional[str] = None
    suggested_code: Optional[str] = None
    expected_impact: str = ""
    confidence: float = 0.5  # 0-1
    can_auto_apply: bool = False
    created_at: float = field(default_factory=time.time)
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ExecutionContext:
    """Context information for a skill execution."""

    skill_name: str
    operation: str
    parameters: Dict[str, Any]
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    environment: Optional[Dict[str, Any]] = None
    parent_execution_id: Optional[str] = None  # For chained operations

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ExecutionRecord:
    """Record of a single skill execution."""

    execution_id: str
    skill_name: str
    operation: str
    parameters: Dict[str, Any]
    success: bool
    duration: float
    timestamp: float
    error: Optional[str] = None
    error_code: Optional[str] = None
    result_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExecutionRecord':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class QualityScores:
    """Quality-related scores."""

    output_quality_score: float = 0.0  # 0-100
    correctness_score: float = 0.0  # 0-100
    consistency_score: float = 0.0  # 0-100
    completeness_score: float = 0.0  # 0-100

    def overall_score(self) -> float:
        """Calculate overall quality score."""
        scores = [
            self.output_quality_score,
            self.correctness_score,
            self.consistency_score,
            self.completeness_score
        ]
        return sum(scores) / len(scores) if scores else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['overall_score'] = self.overall_score()
        return result


@dataclass
class PerformanceScores:
    """Performance-related scores."""

    performance_score: float = 0.0  # 0-100
    resource_efficiency: float = 0.0  # 0-100
    has_regression: bool = False
    regression_details: Optional[Dict[str, Any]] = None
    avg_duration: float = 0.0
    duration_trend: str = HealthTrend.UNKNOWN.value

    def overall_score(self) -> float:
        """Calculate overall performance score."""
        # Penalize if regression detected
        base_score = (self.performance_score + self.resource_efficiency) / 2
        return base_score * 0.5 if self.has_regression else base_score

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['overall_score'] = self.overall_score()
        return result


@dataclass
class ReliabilityScores:
    """Reliability-related scores."""

    reliability_score: float = 0.0  # 0-100
    error_handling_quality: float = 0.0  # 0-100
    recovery_capability: float = 0.0  # 0-100
    success_rate: float = 0.0  # 0-100
    error_rate: float = 0.0  # 0-100

    def overall_score(self) -> float:
        """Calculate overall reliability score."""
        scores = [
            self.reliability_score,
            self.error_handling_quality,
            self.recovery_capability,
            self.success_rate
        ]
        return sum(scores) / len(scores) if scores else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['overall_score'] = self.overall_score()
        return result


@dataclass
class CodeQualityScores:
    """Code quality-related scores."""

    code_quality_score: float = 0.0  # 0-100
    maintainability_index: float = 0.0  # 0-100
    complexity_score: float = 0.0  # 0-100
    test_coverage: float = 0.0  # 0-100
    documentation_score: float = 0.0  # 0-100

    def overall_score(self) -> float:
        """Calculate overall code quality score."""
        scores = [
            self.code_quality_score,
            self.maintainability_index,
            100 - self.complexity_score,  # Lower complexity is better
            self.test_coverage,
            self.documentation_score
        ]
        return sum(scores) / len(scores) if scores else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['overall_score'] = self.overall_score()
        return result


@dataclass
class SkillEvaluationMetrics:
    """Comprehensive evaluation metrics for a skill."""

    skill_name: str
    evaluation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    # Sub-scores
    quality_scores: QualityScores = field(default_factory=QualityScores)
    performance_scores: PerformanceScores = field(default_factory=PerformanceScores)
    reliability_scores: ReliabilityScores = field(default_factory=ReliabilityScores)
    code_quality_scores: CodeQualityScores = field(default_factory=CodeQualityScores)

    # Improvement tracking
    improvement_opportunities: List[ImprovementSuggestion] = field(default_factory=list)
    priority_fixes: List[str] = field(default_factory=list)

    # Overall assessment
    overall_health_score: float = 0.0  # 0-100
    health_trend: str = HealthTrend.UNKNOWN.value

    # Analysis metadata
    execution_samples_analyzed: int = 0
    time_period_days: int = 0
    last_evaluation: Optional[float] = None

    # Strengths and weaknesses
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)

    def calculate_overall_health(self) -> float:
        """
        Calculate overall health score from sub-scores.

        Weights:
        - Quality: 30%
        - Performance: 25%
        - Reliability: 30%
        - Code Quality: 15%
        """
        weights = {
            'quality': 0.30,
            'performance': 0.25,
            'reliability': 0.30,
            'code_quality': 0.15
        }

        overall = (
            self.quality_scores.overall_score() * weights['quality'] +
            self.performance_scores.overall_score() * weights['performance'] +
            self.reliability_scores.overall_score() * weights['reliability'] +
            self.code_quality_scores.overall_score() * weights['code_quality']
        )

        self.overall_health_score = round(overall, 2)
        return self.overall_health_score

    def get_health_grade(self) -> str:
        """Get letter grade for health score."""
        score = self.overall_health_score
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'skill_name': self.skill_name,
            'evaluation_id': self.evaluation_id,
            'timestamp': self.timestamp,
            'quality_scores': self.quality_scores.to_dict(),
            'performance_scores': self.performance_scores.to_dict(),
            'reliability_scores': self.reliability_scores.to_dict(),
            'code_quality_scores': self.code_quality_scores.to_dict(),
            'improvement_opportunities': [s.to_dict() for s in self.improvement_opportunities],
            'priority_fixes': self.priority_fixes,
            'overall_health_score': self.overall_health_score,
            'health_grade': self.get_health_grade(),
            'health_trend': self.health_trend,
            'execution_samples_analyzed': self.execution_samples_analyzed,
            'time_period_days': self.time_period_days,
            'last_evaluation': self.last_evaluation,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses
        }

    def summary(self) -> str:
        """Get a human-readable summary."""
        return f"""
Skill Evaluation Summary: {self.skill_name}
{'=' * 50}
Overall Health: {self.overall_health_score}/100 (Grade: {self.get_health_grade()})
Trend: {self.health_trend}

Sub-Scores:
  Quality:      {self.quality_scores.overall_score():.1f}/100
  Performance:  {self.performance_scores.overall_score():.1f}/100
  Reliability:  {self.reliability_scores.overall_score():.1f}/100
  Code Quality: {self.code_quality_scores.overall_score():.1f}/100

Strengths: {len(self.strengths)}
Weaknesses: {len(self.weaknesses)}
Improvement Opportunities: {len(self.improvement_opportunities)}
Priority Fixes: {len(self.priority_fixes)}

Samples Analyzed: {self.execution_samples_analyzed}
Time Period: {self.time_period_days} days
""".strip()


# Error codes for skill evaluator operations
class EvaluatorError:
    """Error codes for evaluator operations."""
    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    ANALYSIS_FAILED = "ANALYSIS_FAILED"
    IMPROVEMENT_FAILED = "IMPROVEMENT_FAILED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    OPERATION_TIMEOUT = "OPERATION_TIMEOUT"
