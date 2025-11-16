"""
Benchmarking System

Compares skill performance and provides rankings, leaderboards,
and comparative analysis across skills.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics


@dataclass
class BenchmarkMetrics:
    """Metrics for a skill benchmark."""
    skill_name: str

    # Performance metrics
    avg_duration: float = 0.0
    median_duration: float = 0.0
    p95_duration: float = 0.0
    min_duration: float = 0.0
    max_duration: float = 0.0

    # Reliability metrics
    success_rate: float = 0.0
    error_rate: float = 0.0
    total_executions: int = 0

    # Quality metrics
    health_score: float = 0.0
    quality_score: float = 0.0
    performance_score: float = 0.0
    reliability_score: float = 0.0

    # Comparative metrics
    percentile_rank: float = 0.0  # 0-100, higher is better
    category_rank: Optional[int] = None
    overall_rank: Optional[int] = None

    # Metadata
    time_period_days: int = 0
    last_updated: float = field(default_factory=lambda: datetime.now().timestamp())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'skill_name': self.skill_name,
            'performance': {
                'avg_duration': self.avg_duration,
                'median_duration': self.median_duration,
                'p95_duration': self.p95_duration,
                'min_duration': self.min_duration,
                'max_duration': self.max_duration
            },
            'reliability': {
                'success_rate': self.success_rate,
                'error_rate': self.error_rate,
                'total_executions': self.total_executions
            },
            'quality': {
                'health_score': self.health_score,
                'quality_score': self.quality_score,
                'performance_score': self.performance_score,
                'reliability_score': self.reliability_score
            },
            'rankings': {
                'percentile_rank': self.percentile_rank,
                'category_rank': self.category_rank,
                'overall_rank': self.overall_rank
            },
            'metadata': {
                'time_period_days': self.time_period_days,
                'last_updated': self.last_updated
            }
        }


class BenchmarkingSystem:
    """
    Benchmarking system for comparing skill performance.

    Provides:
    - Performance rankings
    - Comparative analysis
    - Leaderboards
    - Percentile calculations
    - Category-based comparisons
    """

    def __init__(self, history_tracker, quality_evaluator):
        """
        Initialize the benchmarking system.

        Args:
            history_tracker: ExecutionHistoryTracker instance
            quality_evaluator: QualityEvaluator instance
        """
        self.history_tracker = history_tracker
        self.quality_evaluator = quality_evaluator

    def benchmark_skills(
        self,
        skill_names: Optional[List[str]] = None,
        time_period_days: int = 30,
        min_executions: int = 10
    ) -> Dict[str, Any]:
        """
        Benchmark multiple skills and generate comparative metrics.

        Args:
            skill_names: List of skills to benchmark (None for all)
            time_period_days: Time period for metrics
            min_executions: Minimum executions required for benchmarking

        Returns:
            Dictionary containing benchmark results
        """
        # Get skills to benchmark
        if skill_names is None:
            skill_names = self.history_tracker.get_all_tracked_skills()

        if not skill_names:
            return {
                'has_data': False,
                'message': 'No skills available for benchmarking'
            }

        # Collect metrics for each skill
        benchmarks = []

        for skill_name in skill_names:
            stats = self.history_tracker.get_execution_stats(
                skill_name=skill_name,
                time_period_days=time_period_days
            )

            # Skip skills with insufficient data
            if stats['total_executions'] < min_executions:
                continue

            # Get quality evaluation
            try:
                evaluation = self.quality_evaluator.evaluate(
                    skill_name=skill_name,
                    execution_samples=100,
                    time_period_days=time_period_days
                )

                health_score = evaluation.overall_health_score
                quality_score = evaluation.quality_scores.overall_score()
                performance_score = evaluation.performance_scores.overall_score()
                reliability_score = evaluation.reliability_scores.overall_score()
            except Exception:
                # Use default scores if evaluation fails
                health_score = 0.0
                quality_score = 0.0
                performance_score = 0.0
                reliability_score = 0.0

            # Get performance baseline for more detailed metrics
            baseline = self.history_tracker.get_performance_baseline(
                skill_name=skill_name,
                days=time_period_days
            )

            if baseline:
                avg_duration = baseline['avg_duration']
                median_duration = baseline['median_duration']
                p95_duration = baseline['p95_duration']
                min_duration = baseline['min_duration']
                max_duration = baseline['max_duration']
            else:
                avg_duration = stats['avg_duration']
                median_duration = avg_duration
                p95_duration = avg_duration * 1.5
                min_duration = stats['min_duration']
                max_duration = stats['max_duration']

            benchmark = BenchmarkMetrics(
                skill_name=skill_name,
                avg_duration=avg_duration,
                median_duration=median_duration,
                p95_duration=p95_duration,
                min_duration=min_duration,
                max_duration=max_duration,
                success_rate=stats['success_rate'],
                error_rate=stats['error_rate'],
                total_executions=stats['total_executions'],
                health_score=health_score,
                quality_score=quality_score,
                performance_score=performance_score,
                reliability_score=reliability_score,
                time_period_days=time_period_days
            )

            benchmarks.append(benchmark)

        if not benchmarks:
            return {
                'has_data': False,
                'message': f'No skills meet minimum execution requirement ({min_executions})'
            }

        # Calculate percentile ranks
        benchmarks = self._calculate_percentile_ranks(benchmarks)

        # Calculate overall ranks
        benchmarks = self._calculate_overall_ranks(benchmarks)

        # Generate leaderboard
        leaderboard = self._generate_leaderboard(benchmarks)

        # Generate comparative statistics
        comparative_stats = self._generate_comparative_stats(benchmarks)

        # Identify top performers and underperformers
        top_performers = [b for b in benchmarks if b.percentile_rank >= 75]
        underperformers = [b for b in benchmarks if b.percentile_rank < 25]

        return {
            'has_data': True,
            'total_benchmarked': len(benchmarks),
            'benchmarks': [b.to_dict() for b in benchmarks],
            'leaderboard': leaderboard,
            'comparative_stats': comparative_stats,
            'top_performers': [b.skill_name for b in top_performers],
            'underperformers': [b.skill_name for b in underperformers],
            'time_period_days': time_period_days,
            'min_executions_required': min_executions
        }

    def compare_skills(
        self,
        skill1: str,
        skill2: str,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Compare two skills head-to-head.

        Args:
            skill1: First skill name
            skill2: Second skill name
            time_period_days: Time period for comparison

        Returns:
            Dictionary containing comparison results
        """
        # Benchmark both skills
        benchmark_result = self.benchmark_skills(
            skill_names=[skill1, skill2],
            time_period_days=time_period_days,
            min_executions=1  # Allow comparison even with few executions
        )

        if not benchmark_result.get('has_data'):
            return {
                'has_data': False,
                'message': 'Unable to benchmark skills for comparison'
            }

        benchmarks = {
            b['skill_name']: b
            for b in benchmark_result['benchmarks']
        }

        if skill1 not in benchmarks or skill2 not in benchmarks:
            return {
                'has_data': False,
                'message': 'One or both skills not found in benchmark data'
            }

        b1 = benchmarks[skill1]
        b2 = benchmarks[skill2]

        # Calculate differences and determine winner for each metric
        comparison = {
            'skill1': skill1,
            'skill2': skill2,
            'metrics': {
                'performance': {
                    'skill1_avg_duration': b1['performance']['avg_duration'],
                    'skill2_avg_duration': b2['performance']['avg_duration'],
                    'difference_seconds': b1['performance']['avg_duration'] - b2['performance']['avg_duration'],
                    'winner': skill1 if b1['performance']['avg_duration'] < b2['performance']['avg_duration'] else skill2
                },
                'reliability': {
                    'skill1_success_rate': b1['reliability']['success_rate'],
                    'skill2_success_rate': b2['reliability']['success_rate'],
                    'difference_percent': b1['reliability']['success_rate'] - b2['reliability']['success_rate'],
                    'winner': skill1 if b1['reliability']['success_rate'] > b2['reliability']['success_rate'] else skill2
                },
                'health': {
                    'skill1_health_score': b1['quality']['health_score'],
                    'skill2_health_score': b2['quality']['health_score'],
                    'difference_points': b1['quality']['health_score'] - b2['quality']['health_score'],
                    'winner': skill1 if b1['quality']['health_score'] > b2['quality']['health_score'] else skill2
                },
                'executions': {
                    'skill1_total': b1['reliability']['total_executions'],
                    'skill2_total': b2['reliability']['total_executions'],
                    'difference': b1['reliability']['total_executions'] - b2['reliability']['total_executions']
                }
            },
            'overall_winner': self._determine_overall_winner(b1, b2, skill1, skill2),
            'time_period_days': time_period_days
        }

        return {
            'has_data': True,
            'comparison': comparison,
            'recommendations': self._generate_comparison_recommendations(comparison)
        }

    def generate_leaderboard(
        self,
        category: str = 'overall',
        time_period_days: int = 30,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Generate a leaderboard for skills.

        Args:
            category: Category to rank by ('overall', 'performance', 'reliability', 'quality')
            time_period_days: Time period for rankings
            top_n: Number of top skills to include

        Returns:
            Dictionary containing leaderboard
        """
        benchmark_result = self.benchmark_skills(
            time_period_days=time_period_days,
            min_executions=5
        )

        if not benchmark_result.get('has_data'):
            return {
                'has_data': False,
                'message': 'Insufficient data for leaderboard'
            }

        benchmarks = benchmark_result['benchmarks']

        # Sort by category
        if category == 'performance':
            # Lower duration is better, so invert
            sorted_benchmarks = sorted(
                benchmarks,
                key=lambda b: -b['quality']['performance_score']
            )
        elif category == 'reliability':
            sorted_benchmarks = sorted(
                benchmarks,
                key=lambda b: -b['quality']['reliability_score']
            )
        elif category == 'quality':
            sorted_benchmarks = sorted(
                benchmarks,
                key=lambda b: -b['quality']['quality_score']
            )
        else:  # overall
            sorted_benchmarks = sorted(
                benchmarks,
                key=lambda b: -b['quality']['health_score']
            )

        # Generate leaderboard entries
        leaderboard = []
        for rank, benchmark in enumerate(sorted_benchmarks[:top_n], 1):
            entry = {
                'rank': rank,
                'skill_name': benchmark['skill_name'],
                'score': self._get_category_score(benchmark, category),
                'metrics': benchmark
            }
            leaderboard.append(entry)

        return {
            'has_data': True,
            'category': category,
            'leaderboard': leaderboard,
            'total_skills': len(benchmarks),
            'time_period_days': time_period_days
        }

    # Helper methods

    def _calculate_percentile_ranks(
        self,
        benchmarks: List[BenchmarkMetrics]
    ) -> List[BenchmarkMetrics]:
        """Calculate percentile ranks for benchmarks."""
        if not benchmarks:
            return benchmarks

        # Collect scores for percentile calculation
        scores = []
        for b in benchmarks:
            # Composite score based on multiple factors
            score = (
                b.health_score * 0.4 +
                b.performance_score * 0.2 +
                b.reliability_score * 0.2 +
                b.quality_score * 0.2
            )
            scores.append((b, score))

        # Sort by score
        scores.sort(key=lambda x: x[1])

        # Calculate percentile ranks
        for i, (benchmark, score) in enumerate(scores):
            percentile = (i / (len(scores) - 1)) * 100 if len(scores) > 1 else 50
            benchmark.percentile_rank = percentile

        return benchmarks

    def _calculate_overall_ranks(
        self,
        benchmarks: List[BenchmarkMetrics]
    ) -> List[BenchmarkMetrics]:
        """Calculate overall ranks based on composite scores."""
        # Sort by percentile rank (descending)
        sorted_benchmarks = sorted(
            benchmarks,
            key=lambda b: b.percentile_rank,
            reverse=True
        )

        # Assign ranks
        for rank, benchmark in enumerate(sorted_benchmarks, 1):
            benchmark.overall_rank = rank

        return benchmarks

    def _generate_leaderboard(
        self,
        benchmarks: List[BenchmarkMetrics]
    ) -> List[Dict[str, Any]]:
        """Generate leaderboard from benchmarks."""
        sorted_benchmarks = sorted(
            benchmarks,
            key=lambda b: b.percentile_rank,
            reverse=True
        )

        leaderboard = []
        for rank, benchmark in enumerate(sorted_benchmarks[:10], 1):
            leaderboard.append({
                'rank': rank,
                'skill_name': benchmark.skill_name,
                'health_score': benchmark.health_score,
                'percentile_rank': benchmark.percentile_rank,
                'success_rate': benchmark.success_rate,
                'avg_duration': benchmark.avg_duration
            })

        return leaderboard

    def _generate_comparative_stats(
        self,
        benchmarks: List[BenchmarkMetrics]
    ) -> Dict[str, Any]:
        """Generate comparative statistics across all benchmarks."""
        if not benchmarks:
            return {}

        durations = [b.avg_duration for b in benchmarks]
        success_rates = [b.success_rate for b in benchmarks]
        health_scores = [b.health_score for b in benchmarks]

        return {
            'duration': {
                'mean': statistics.mean(durations),
                'median': statistics.median(durations),
                'stdev': statistics.stdev(durations) if len(durations) > 1 else 0,
                'min': min(durations),
                'max': max(durations)
            },
            'success_rate': {
                'mean': statistics.mean(success_rates),
                'median': statistics.median(success_rates),
                'stdev': statistics.stdev(success_rates) if len(success_rates) > 1 else 0,
                'min': min(success_rates),
                'max': max(success_rates)
            },
            'health_score': {
                'mean': statistics.mean(health_scores),
                'median': statistics.median(health_scores),
                'stdev': statistics.stdev(health_scores) if len(health_scores) > 1 else 0,
                'min': min(health_scores),
                'max': max(health_scores)
            },
            'total_executions': sum(b.total_executions for b in benchmarks)
        }

    def _determine_overall_winner(
        self,
        b1: Dict[str, Any],
        b2: Dict[str, Any],
        skill1: str,
        skill2: str
    ) -> Dict[str, str]:
        """Determine overall winner based on multiple factors."""
        # Count wins in each category
        skill1_wins = 0
        skill2_wins = 0

        # Performance (lower duration wins)
        if b1['performance']['avg_duration'] < b2['performance']['avg_duration']:
            skill1_wins += 1
        else:
            skill2_wins += 1

        # Reliability (higher success rate wins)
        if b1['reliability']['success_rate'] > b2['reliability']['success_rate']:
            skill1_wins += 1
        else:
            skill2_wins += 1

        # Health (higher score wins)
        if b1['quality']['health_score'] > b2['quality']['health_score']:
            skill1_wins += 1
        else:
            skill2_wins += 1

        if skill1_wins > skill2_wins:
            return {
                'winner': skill1,
                'score': f"{skill1_wins}-{skill2_wins}",
                'margin': 'decisive' if skill1_wins - skill2_wins >= 2 else 'narrow'
            }
        elif skill2_wins > skill1_wins:
            return {
                'winner': skill2,
                'score': f"{skill2_wins}-{skill1_wins}",
                'margin': 'decisive' if skill2_wins - skill1_wins >= 2 else 'narrow'
            }
        else:
            return {
                'winner': 'tie',
                'score': f"{skill1_wins}-{skill2_wins}",
                'margin': 'even'
            }

    def _generate_comparison_recommendations(
        self,
        comparison: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on comparison."""
        recommendations = []

        metrics = comparison['metrics']
        skill1 = comparison['skill1']
        skill2 = comparison['skill2']

        # Performance recommendation
        perf_diff = abs(metrics['performance']['difference_seconds'])
        if perf_diff > 1.0:
            slower_skill = skill1 if metrics['performance']['winner'] == skill2 else skill2
            recommendations.append(
                f"Optimize {slower_skill} performance - it's {perf_diff:.2f}s slower on average"
            )

        # Reliability recommendation
        rel_diff = abs(metrics['reliability']['difference_percent'])
        if rel_diff > 10:
            less_reliable = skill1 if metrics['reliability']['winner'] == skill2 else skill2
            recommendations.append(
                f"Improve {less_reliable} reliability - success rate is {rel_diff:.1f}% lower"
            )

        # Health recommendation
        health_diff = abs(metrics['health']['difference_points'])
        if health_diff > 20:
            lower_health = skill1 if metrics['health']['winner'] == skill2 else skill2
            recommendations.append(
                f"Address quality issues in {lower_health} - health score is {health_diff:.1f} points lower"
            )

        if not recommendations:
            recommendations.append("Both skills are performing comparably well")

        return recommendations

    def _get_category_score(self, benchmark: Dict[str, Any], category: str) -> float:
        """Get score for a specific category."""
        if category == 'performance':
            return benchmark['quality']['performance_score']
        elif category == 'reliability':
            return benchmark['quality']['reliability_score']
        elif category == 'quality':
            return benchmark['quality']['quality_score']
        else:  # overall
            return benchmark['quality']['health_score']
