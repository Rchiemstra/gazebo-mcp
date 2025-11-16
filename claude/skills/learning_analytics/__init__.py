"""
Learning Analytics Skill

Analyzes learning plan data to provide insights, detect struggles,
and generate recommendations for teaching optimization.

This skill builds on learning-plan-manager to provide:
- Learning velocity tracking and trends
- Struggle area detection
- Checkpoint performance analysis
- Learning pattern recognition
- Time estimation accuracy analysis
- Actionable recommendations for teaching optimization
- Contextual retrieval for learning content (67% better accuracy)
"""

from .models import (
    # Enums
    StruggleIndicator,
    PatternType,
    RecommendationPriority,
    RecommendationType,

    # Models
    VelocityMetrics,
    StruggleArea,
    CheckpointAnalysis,
    CheckpointPerformance,
    LearningPattern,
    TimeEstimationAnalysis,
    LearningRecommendation,
    LearningAnalytics,
)

from .analyzer import LearningAnalyzer

from .contextual_retrieval import (
    ContextualRetrieval,
    Document,
    Chunk,
    RetrievalResult,
    create_learning_content_retrieval,
)

from .content_indexer import (
    LearningContentIndexer,
    LearningContent,
    index_learning_content,
)

from .prerequisite_discovery import (
    PrerequisiteDiscovery,
    Prerequisite,
    PrerequisiteGraph,
    discover_prerequisites,
    build_learning_path,
)

__all__ = [
    # Enums
    "StruggleIndicator",
    "PatternType",
    "RecommendationPriority",
    "RecommendationType",

    # Models
    "VelocityMetrics",
    "StruggleArea",
    "CheckpointAnalysis",
    "CheckpointPerformance",
    "LearningPattern",
    "TimeEstimationAnalysis",
    "LearningRecommendation",
    "LearningAnalytics",

    # Analyzer
    "LearningAnalyzer",

    # Contextual Retrieval
    "ContextualRetrieval",
    "Document",
    "Chunk",
    "RetrievalResult",
    "create_learning_content_retrieval",

    # Content Indexing (Phase 4)
    "LearningContentIndexer",
    "LearningContent",
    "index_learning_content",

    # Prerequisite Discovery (Phase 4)
    "PrerequisiteDiscovery",
    "Prerequisite",
    "PrerequisiteGraph",
    "discover_prerequisites",
    "build_learning_path",
]

__version__ = "1.2.0"  # Added content indexing and prerequisite discovery (Phase 4)
