"""
Agent Evaluation Framework for Quality Tracking.

Implements systematic evaluation of agents and skills using:
- Test queries per agent (20+ queries)
- Performance metrics tracking
- Quality trends over time
- Improvement visualization

Part of Phase 3: Polish & Optimization
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum


class AgentType(Enum):
    """Types of agents to evaluate."""
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    MENTOR = "mentor"
    SPECIALIST = "specialist"
    GENERAL = "general"


class QueryDifficulty(Enum):
    """Difficulty level of test queries."""
    SIMPLE = "simple"  # Straightforward, single-step
    MODERATE = "moderate"  # Multi-step, some complexity
    COMPLEX = "complex"  # Multi-agent, long chains, high complexity


@dataclass
class TestQuery:
    """A test query for evaluating an agent."""
    id: str
    query: str
    agent_type: str  # Which agent to test
    difficulty: QueryDifficulty
    expected_capabilities: List[str]  # What should the agent demonstrate?
    success_criteria: List[str]  # How to determine success?
    category: str  # code_review, architecture_analysis, learning, etc.


@dataclass
class EvaluationResult:
    """Result from evaluating an agent on a query."""
    query_id: str
    agent_type: str
    timestamp: datetime
    success: bool
    score: float  # 0.0 - 1.0
    response_time: float  # seconds
    token_usage: Optional[int] = None
    capabilities_demonstrated: List[str] = field(default_factory=list)
    issues_found: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for an agent."""
    agent_type: str
    total_queries: int
    successful_queries: int
    average_score: float
    average_response_time: float
    total_tokens_used: int
    success_rate: float
    queries_by_difficulty: Dict[str, Dict[str, int]]  # difficulty -> {total, success}
    trend_data: List[Dict[str, Any]]  # Historical performance


class AgentEvaluator:
    """
    Evaluates agents and tracks quality over time.

    Features:
    - Test query library (20+ per agent type)
    - Automated evaluation tracking
    - Performance metrics calculation
    - Trend analysis
    - Quality dashboard data

    Example:
        evaluator = AgentEvaluator()

        # Add test queries
        evaluator.add_test_query(TestQuery(
            id="code_review_1",
            query="Review this authentication module for security issues",
            agent_type="code-review-orchestrator",
            difficulty=QueryDifficulty.COMPLEX,
            expected_capabilities=["security_analysis", "parallel_workers"],
            success_criteria=["Identified security issues", "Clear recommendations"]
        ))

        # Evaluate agent
        result = evaluator.evaluate_agent_manually(
            query_id="code_review_1",
            success=True,
            score=0.9,
            response_time=120.5
        )

        # Get metrics
        metrics = evaluator.get_agent_metrics("code-review-orchestrator")
        print(f"Success rate: {metrics.success_rate:.1%}")
    """

    def __init__(self, data_dir: str = "evaluation_data"):
        """
        Initialize evaluator.

        Args:
            data_dir: Directory to store evaluation data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.test_queries: Dict[str, TestQuery] = {}
        self.evaluation_results: List[EvaluationResult] = []

        self._load_data()

    def add_test_query(self, query: TestQuery):
        """Add a test query to the library."""
        self.test_queries[query.id] = query
        self._save_test_queries()

    def add_test_queries_bulk(self, queries: List[TestQuery]):
        """Add multiple test queries at once."""
        for query in queries:
            self.test_queries[query.id] = query
        self._save_test_queries()

    def evaluate_agent_manually(
        self,
        query_id: str,
        success: bool,
        score: float,
        response_time: float,
        token_usage: Optional[int] = None,
        capabilities_demonstrated: Optional[List[str]] = None,
        issues_found: Optional[List[str]] = None,
        notes: str = ""
    ) -> EvaluationResult:
        """
        Manually record evaluation result.

        Args:
            query_id: ID of test query
            success: Whether agent succeeded
            score: Quality score (0.0 - 1.0)
            response_time: Response time in seconds
            token_usage: Tokens used (optional)
            capabilities_demonstrated: Capabilities shown
            issues_found: Issues identified
            notes: Additional notes

        Returns:
            EvaluationResult
        """
        if query_id not in self.test_queries:
            raise ValueError(f"Query {query_id} not found")

        query = self.test_queries[query_id]

        result = EvaluationResult(
            query_id=query_id,
            agent_type=query.agent_type,
            timestamp=datetime.now(),
            success=success,
            score=score,
            response_time=response_time,
            token_usage=token_usage,
            capabilities_demonstrated=capabilities_demonstrated or [],
            issues_found=issues_found or [],
            notes=notes
        )

        self.evaluation_results.append(result)
        self._save_evaluation_results()

        return result

    def get_agent_metrics(self, agent_type: str) -> AgentPerformanceMetrics:
        """
        Get performance metrics for an agent.

        Args:
            agent_type: Type of agent

        Returns:
            AgentPerformanceMetrics
        """
        # Filter results for this agent
        results = [r for r in self.evaluation_results if r.agent_type == agent_type]

        if not results:
            return AgentPerformanceMetrics(
                agent_type=agent_type,
                total_queries=0,
                successful_queries=0,
                average_score=0.0,
                average_response_time=0.0,
                total_tokens_used=0,
                success_rate=0.0,
                queries_by_difficulty={},
                trend_data=[]
            )

        # Calculate metrics
        total = len(results)
        successful = sum(1 for r in results if r.success)
        avg_score = sum(r.score for r in results) / total
        avg_time = sum(r.response_time for r in results) / total
        total_tokens = sum(r.token_usage for r in results if r.token_usage)
        success_rate = successful / total if total > 0 else 0.0

        # By difficulty
        by_difficulty = {}
        for result in results:
            query = self.test_queries.get(result.query_id)
            if query:
                diff = query.difficulty.value
                if diff not in by_difficulty:
                    by_difficulty[diff] = {"total": 0, "success": 0}
                by_difficulty[diff]["total"] += 1
                if result.success:
                    by_difficulty[diff]["success"] += 1

        # Trend data (last 30 days)
        trend_data = self._calculate_trend_data(agent_type, days=30)

        return AgentPerformanceMetrics(
            agent_type=agent_type,
            total_queries=total,
            successful_queries=successful,
            average_score=avg_score,
            average_response_time=avg_time,
            total_tokens_used=total_tokens,
            success_rate=success_rate,
            queries_by_difficulty=by_difficulty,
            trend_data=trend_data
        )

    def _calculate_trend_data(self, agent_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Calculate performance trend over time."""
        from datetime import timedelta

        results = [r for r in self.evaluation_results if r.agent_type == agent_type]
        results.sort(key=lambda r: r.timestamp)

        if not results:
            return []

        # Group by week
        trend = []
        current_week = None
        week_results = []

        for result in results:
            week = result.timestamp.isocalendar()[1]  # Week number

            if current_week is None:
                current_week = week

            if week != current_week:
                # Summarize previous week
                if week_results:
                    trend.append(self._summarize_week(week_results))
                week_results = []
                current_week = week

            week_results.append(result)

        # Last week
        if week_results:
            trend.append(self._summarize_week(week_results))

        return trend[-12:]  # Last 12 weeks

    def _summarize_week(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Summarize results for a week."""
        if not results:
            return {}

        return {
            "week": results[0].timestamp.strftime("%Y-W%W"),
            "total": len(results),
            "success": sum(1 for r in results if r.success),
            "average_score": sum(r.score for r in results) / len(results),
            "success_rate": sum(1 for r in results if r.success) / len(results)
        }

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """
        Generate data for performance dashboard.

        Returns:
            Dashboard data with metrics for all agents
        """
        # Get all unique agent types
        agent_types = set(q.agent_type for q in self.test_queries.values())

        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "agents": {},
            "overall": {
                "total_queries": len(self.test_queries),
                "total_evaluations": len(self.evaluation_results),
                "agent_types": len(agent_types)
            }
        }

        for agent_type in agent_types:
            metrics = self.get_agent_metrics(agent_type)
            dashboard["agents"][agent_type] = {
                "total_queries": metrics.total_queries,
                "success_rate": metrics.success_rate,
                "average_score": metrics.average_score,
                "average_response_time": metrics.average_response_time,
                "by_difficulty": metrics.queries_by_difficulty,
                "trend": metrics.trend_data
            }

        return dashboard

    def _save_test_queries(self):
        """Save test queries to disk."""
        path = self.data_dir / "test_queries.json"
        data = {
            query_id: {
                "id": query.id,
                "query": query.query,
                "agent_type": query.agent_type,
                "difficulty": query.difficulty.value,
                "expected_capabilities": query.expected_capabilities,
                "success_criteria": query.success_criteria,
                "category": query.category
            }
            for query_id, query in self.test_queries.items()
        }

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def _save_evaluation_results(self):
        """Save evaluation results to disk."""
        path = self.data_dir / "evaluation_results.json"
        data = [
            {
                "query_id": r.query_id,
                "agent_type": r.agent_type,
                "timestamp": r.timestamp.isoformat(),
                "success": r.success,
                "score": r.score,
                "response_time": r.response_time,
                "token_usage": r.token_usage,
                "capabilities_demonstrated": r.capabilities_demonstrated,
                "issues_found": r.issues_found,
                "notes": r.notes
            }
            for r in self.evaluation_results
        ]

        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_data(self):
        """Load test queries and results from disk."""
        # Load test queries
        queries_path = self.data_dir / "test_queries.json"
        if queries_path.exists():
            with open(queries_path) as f:
                data = json.load(f)
                for query_id, query_data in data.items():
                    self.test_queries[query_id] = TestQuery(
                        id=query_data["id"],
                        query=query_data["query"],
                        agent_type=query_data["agent_type"],
                        difficulty=QueryDifficulty(query_data["difficulty"]),
                        expected_capabilities=query_data["expected_capabilities"],
                        success_criteria=query_data["success_criteria"],
                        category=query_data["category"]
                    )

        # Load evaluation results
        results_path = self.data_dir / "evaluation_results.json"
        if results_path.exists():
            with open(results_path) as f:
                data = json.load(f)
                for result_data in data:
                    self.evaluation_results.append(EvaluationResult(
                        query_id=result_data["query_id"],
                        agent_type=result_data["agent_type"],
                        timestamp=datetime.fromisoformat(result_data["timestamp"]),
                        success=result_data["success"],
                        score=result_data["score"],
                        response_time=result_data["response_time"],
                        token_usage=result_data.get("token_usage"),
                        capabilities_demonstrated=result_data.get("capabilities_demonstrated", []),
                        issues_found=result_data.get("issues_found", []),
                        notes=result_data.get("notes", "")
                    ))


def create_default_test_queries() -> List[TestQuery]:
    """
    Create default test queries for all agent types.

    Returns 20+ queries per major agent type.
    """
    queries = []

    # Code Review Orchestrator (20 queries)
    for i in range(20):
        queries.append(TestQuery(
            id=f"code_review_{i+1}",
            query=f"Review authentication module PR #{i+1}",
            agent_type="code-review-orchestrator",
            difficulty=QueryDifficulty.COMPLEX if i < 5 else QueryDifficulty.MODERATE,
            expected_capabilities=["security_analysis", "test_coverage", "parallel_workers"],
            success_criteria=["Identified issues", "Clear recommendations", "Go/no-go decision"],
            category="code_review"
        ))

    # Architecture Mentor (20 queries)
    for i in range(20):
        queries.append(TestQuery(
            id=f"architecture_{i+1}",
            query=f"Explain design pattern for {['authentication', 'caching', 'logging'][i%3]} system",
            agent_type="code-architecture-mentor",
            difficulty=QueryDifficulty.MODERATE if i < 10 else QueryDifficulty.SIMPLE,
            expected_capabilities=["design_thinking", "teaching", "think_tool"],
            success_criteria=["Guided learning", "No complete solutions", "Clear examples"],
            category="architecture_teaching"
        ))

    # Think Tool Usage (20 queries)
    for i in range(20):
        queries.append(TestQuery(
            id=f"think_tool_{i+1}",
            query=f"Analyze trade-offs for {['microservices', 'monolith', 'serverless'][i%3]} architecture",
            agent_type="general",
            difficulty=QueryDifficulty.COMPLEX if i < 5 else QueryDifficulty.MODERATE,
            expected_capabilities=["think_tool", "structured_reasoning", "decision_making"],
            success_criteria=["Used think tool", "Clear reasoning", "Confident decision"],
            category="complex_reasoning"
        ))

    # Contextual Retrieval (20 queries)
    for i in range(20):
        queries.append(TestQuery(
            id=f"retrieval_{i+1}",
            query=f"Find tutorials for {['SLAM', 'navigation', 'sensor fusion'][i%3]}",
            agent_type="general",
            difficulty=QueryDifficulty.MODERATE,
            expected_capabilities=["contextual_retrieval", "content_recommendation"],
            success_criteria=["Relevant results", "High accuracy", "Contextual matches"],
            category="knowledge_retrieval"
        ))

    return queries


def create_evaluator_with_default_queries() -> AgentEvaluator:
    """
    Create evaluator pre-loaded with default test queries.

    Returns:
        AgentEvaluator with 80+ test queries
    """
    evaluator = AgentEvaluator()
    queries = create_default_test_queries()
    evaluator.add_test_queries_bulk(queries)
    return evaluator
