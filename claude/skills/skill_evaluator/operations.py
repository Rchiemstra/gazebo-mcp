"""
Skill Evaluator Operations

Public interface for the skill evaluator.
"""

import time
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path

from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker
from skills.skill_evaluator.core.monitor import ExecutionMonitor
from skills.skill_evaluator.core.quality_evaluator import QualityEvaluator
from skills.skill_evaluator.core.performance_analyzer import PerformanceAnalyzer
from skills.skill_evaluator.core.trend_analyzer import TrendAnalyzer
from skills.skill_evaluator.core.improvement_engine import ImprovementEngine
from skills.skill_evaluator.core.improvement_applicator import ImprovementApplicator
from skills.skill_evaluator.core.report_generator import ReportGenerator
from skills.skill_evaluator.core.cross_skill_analyzer import CrossSkillAnalyzer
from skills.skill_evaluator.core.benchmarking_system import BenchmarkingSystem
from skills.skill_evaluator.core.models import EvaluatorError, ImprovementSuggestion


# Initialize singleton instances
_history_tracker = None
_monitor = None
_quality_evaluator = None
_performance_analyzer = None
_trend_analyzer = None
_improvement_engine = None
_improvement_applicator = None
_report_generator = None
_cross_skill_analyzer = None
_benchmarking_system = None


def _get_instances():
    """Get or create singleton instances."""
    global _history_tracker, _monitor, _quality_evaluator, _performance_analyzer, _trend_analyzer, _improvement_engine, _improvement_applicator, _report_generator, _cross_skill_analyzer, _benchmarking_system

    if _history_tracker is None:
        _history_tracker = ExecutionHistoryTracker()
        _monitor = ExecutionMonitor(_history_tracker)
        _quality_evaluator = QualityEvaluator(_history_tracker)
        _performance_analyzer = PerformanceAnalyzer(_history_tracker)
        _trend_analyzer = TrendAnalyzer(_history_tracker)
        _improvement_engine = ImprovementEngine(_history_tracker)
        _improvement_applicator = ImprovementApplicator()
        _report_generator = ReportGenerator(_history_tracker)
        _cross_skill_analyzer = CrossSkillAnalyzer(_history_tracker)
        _benchmarking_system = BenchmarkingSystem(_history_tracker, _quality_evaluator)

    return _history_tracker, _monitor, _quality_evaluator, _performance_analyzer, _trend_analyzer, _improvement_engine, _improvement_applicator, _report_generator, _cross_skill_analyzer, _benchmarking_system


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def monitor_execution(
    skill_name: str,
    operation: str,
    parameters: Dict[str, Any],
    collect_metrics: bool = True,
    profile_performance: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Monitor a skill execution in real-time.

    This operation tracks execution metrics, detects anomalies, and provides
    recommendations for optimization.

    Args:
        skill_name: Name of the skill to monitor
        operation: Operation being executed
        parameters: Operation parameters
        collect_metrics: Whether to collect detailed metrics
        profile_performance: Whether to profile CPU/memory usage

    Returns:
        OperationResult containing execution metrics and recommendations
    """
    start_time = time.time()

    try:
        _, monitor, _, _, _, _, _, _, _, _ = _get_instances()

        # Pre-execution check
        context = monitor.pre_execution_check(skill_name, operation, parameters)

        # Note: In a real integration, this would wrap the actual skill execution
        # For now, we simulate by just recording the attempt

        # Post-execution analysis (simulated success)
        analysis = monitor.post_execution_analysis(
            execution_id=context.execution_id,
            success=True,
            result_data={'monitored': True},
            error=None,
            error_code=None
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data={
                'execution_id': context.execution_id,
                'skill_name': skill_name,
                'operation': operation,
                'basic_metrics': {
                    'duration': analysis['performance_profile']['duration'],
                    'cpu_usage_percent': analysis['performance_profile'].get('cpu_usage_percent', 0),
                    'memory_delta_mb': analysis['performance_profile'].get('memory_delta_mb', 0)
                },
                'performance_profile': analysis['performance_profile'] if profile_performance else None,
                'warnings': analysis['warnings'],
                'recommendations': analysis['recommendations'],
                'baseline_comparison': analysis.get('baseline_comparison')
            },
            duration=duration,
            metadata={'context': context.to_dict()}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to monitor execution: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure skill_name exists in the system",
                    "Verify operation name is valid for the skill",
                    "Check that parameters dict is properly formatted",
                    "Try with simpler parameters first to verify monitoring works"
                ],
                "example_fix": "monitor_execution('test_orchestrator', 'generate_tests', {'file': 'test.py'})"
            }
        )


def evaluate_quality(
    skill_name: str,
    execution_samples: int = 100,
    include_code_analysis: bool = True,
    validate_outputs: bool = True,
    time_period_days: Optional[int] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Perform comprehensive quality evaluation of a skill.

    Analyzes execution history, performance, reliability, and code quality
    to generate a detailed health assessment with improvement suggestions.

    Args:
        skill_name: Name of the skill to evaluate
        execution_samples: Number of recent executions to analyze
        include_code_analysis: Whether to analyze code quality
        validate_outputs: Whether to validate output correctness
        time_period_days: Limit analysis to recent days (None for all time)
        response_format: "summary" (health score only) or "detailed" (full metrics)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing comprehensive quality metrics

    Token Efficiency:
        - Use response_format="summary" for health score and key issues
        - Use response_format="detailed" for complete metrics and analysis
        - Summary mode saves 85-95% tokens
    """
    start_time = time.time()

    try:
        history_tracker, _, quality_evaluator, _, _, _, _, _, _, _ = _get_instances()

        # Check if we have data for this skill
        stats = history_tracker.get_execution_stats(
            skill_name,
            time_period_days=time_period_days
        )

        if stats['total_executions'] == 0:
            return OperationResult(
                success=False,
                error=f"No execution data available for skill: {skill_name}",
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        # Perform evaluation
        metrics = quality_evaluator.evaluate(
            skill_name=skill_name,
            execution_samples=execution_samples,
            include_code_analysis=include_code_analysis,
            time_period_days=time_period_days
        )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'health_score': metrics.overall_health_score,
                'health_grade': metrics.get_health_grade(),
                'trend': metrics.health_trend,
                'critical_issues': len(metrics.priority_fixes),
                'strengths_count': len(metrics.strengths),
                'weaknesses_count': len(metrics.weaknesses),
                'summary': metrics.summary(),
                'efficiency_tip': 'Use response_format="detailed" for complete metrics'
            }
        else:
            data = {
                'skill_name': skill_name,
                'quality_metrics': metrics.to_dict(),
                'health_score': metrics.overall_health_score,
                'health_grade': metrics.get_health_grade(),
                'trend': metrics.health_trend,
                'strengths': metrics.strengths,
                'weaknesses': metrics.weaknesses,
                'improvement_opportunities': [
                    s.to_dict() for s in metrics.improvement_opportunities
                ],
                'priority_fixes': metrics.priority_fixes,
                'summary': metrics.summary(),
                'execution_samples_analyzed': metrics.execution_samples_analyzed
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'evaluation_id': metrics.evaluation_id,
                'timestamp': metrics.timestamp
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to evaluate quality: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has execution history",
                    "Try with a skill that has been used recently",
                    "Check if the skill name is correct",
                    "Use monitor_execution first to ensure data exists"
                ],
                "example_fix": "evaluate_quality('test_orchestrator', execution_samples=50)"
            }
        )


def analyze_performance(
    skill_name: str,
    baseline_period: str = "7d",
    regression_threshold: float = 0.3,
    operation: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze performance and detect regressions (Phase 2 - Full Implementation).

    Performs comprehensive performance analysis including regression detection,
    bottleneck identification, and optimization recommendations.

    Args:
        skill_name: Name of the skill to analyze
        baseline_period: Period for baseline comparison (e.g., "7d", "30d")
        regression_threshold: Threshold for regression detection (0-1)
        operation: Specific operation to analyze (None for all)
        response_format: "summary" (key metrics) or "detailed" (full analysis)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing comprehensive performance analysis

    Token Efficiency:
        - Use response_format="summary" for performance score and regressions
        - Use response_format="detailed" for bottlenecks and full distribution
        - Summary mode saves 80-90% tokens
    """
    start_time = time.time()

    try:
        _, _, _, performance_analyzer, _, _, _, _, _, _ = _get_instances()

        # Parse baseline period
        days = int(baseline_period.replace('d', ''))

        # Perform comprehensive analysis
        analysis = performance_analyzer.analyze(
            skill_name=skill_name,
            baseline_period_days=days,
            regression_threshold=regression_threshold,
            operation=operation
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('error', 'Insufficient data'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time,
                metadata={'recommendation': analysis.get('recommendation')}
            )

        duration = time.time() - start_time

        # Format regression analysis for output
        regression = analysis['regression_analysis']
        bottlenecks = analysis['bottlenecks']
        suggestions = analysis['optimization_suggestions']

        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'operation': operation,
                'performance_score': analysis['performance_score'],
                'has_regression': regression['has_regression'],
                'regression_severity': regression.get('severity'),
                'avg_degradation_percent': regression['avg_degradation_percent'],
                'bottleneck_count': len(bottlenecks),
                'top_suggestions': suggestions[:3] if len(suggestions) > 0 else [],
                'trend': analysis['trend'],
                'efficiency_tip': 'Use response_format="detailed" for complete bottleneck analysis'
            }
        else:
            data = {
                'skill_name': skill_name,
                'operation': operation,
                'performance_score': analysis['performance_score'],
                'baseline_period_days': days,
                'regression_threshold': regression_threshold,

                # Regression analysis
                'has_regression': regression['has_regression'],
                'regression_confidence': regression.get('confidence', 0),
                'regression_severity': regression.get('severity'),
                'comparison': {
                    'baseline_avg': regression['baseline_avg'],
                    'current_avg': regression['current_avg'],
                    'baseline_median': regression['baseline_median'],
                    'current_median': regression['current_median'],
                    'avg_degradation_percent': regression['avg_degradation_percent'],
                    'median_degradation_percent': regression['median_degradation_percent']
                },

                # Bottlenecks
                'bottlenecks': bottlenecks,
                'bottleneck_count': len(bottlenecks),

                # Distribution analysis
                'distribution': analysis['distribution'],

                # Optimization suggestions
                'optimization_suggestions': suggestions,
                'suggestion_count': len(suggestions),

                # Trend
                'trend': analysis['trend'],

                # Baseline metrics
                'baseline_metrics': analysis['baseline_metrics'],
                'current_metrics': analysis['current_metrics']
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'analysis_method': 'statistical_regression_detection',
                'sample_size': regression.get('sample_size', 0)
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to analyze performance: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has sufficient execution history",
                    "Verify baseline_period format (e.g., '7d', '30d')",
                    "Check regression_threshold is between 0 and 1",
                    "Try with a longer baseline_period for more stable baselines"
                ],
                "example_fix": "analyze_performance('test_orchestrator', baseline_period='7d', regression_threshold=0.3)"
            }
        )


def suggest_improvements(
    skill_name: str,
    focus_areas: list = None,
    priority_threshold: str = "medium",
    include_examples: bool = True,
    use_ai_agents: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate AI-powered improvement suggestions (Phase 3 - Full Implementation).

    Uses ImprovementEngine with code analysis and intelligent suggestion generation.

    Args:
        skill_name: Name of the skill to improve
        focus_areas: Areas to focus on (default: ['all'])
        priority_threshold: Minimum priority level
        include_examples: Include code examples
        use_ai_agents: Whether to use AI agents for analysis
        response_format: "summary" (counts & top items) or "detailed" (all suggestions)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing comprehensive improvement suggestions

    Token Efficiency:
        - Use response_format="summary" for suggestion counts and action plan
        - Use response_format="detailed" for all suggestions with details
        - Summary mode saves 80-90% tokens
    """
    start_time = time.time()

    try:
        _, _, quality_evaluator, _, _, improvement_engine, _, _, _, _ = _get_instances()

        # First, evaluate quality to get current metrics
        metrics = quality_evaluator.evaluate(skill_name, execution_samples=100)

        # Generate comprehensive suggestions using ImprovementEngine
        suggestions = improvement_engine.generate_suggestions(
            skill_name=skill_name,
            metrics=metrics,
            focus_areas=focus_areas,
            use_ai_agents=use_ai_agents
        )

        if not suggestions:
            return OperationResult(
                success=True,
                data={
                    'skill_name': skill_name,
                    'suggestions': [],
                    'estimated_impact': {},
                    'implementation_complexity': 'none',
                    'auto_applicable': [],
                    'action_plan': {'has_plan': False},
                    'message': 'No improvements needed - skill is performing well'
                },
                duration=time.time() - start_time
            )

        # Filter by priority threshold
        priority_order = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        threshold_value = priority_order.get(priority_threshold.lower(), 2)

        filtered_suggestions = [
            s for s in suggestions
            if priority_order.get(s.severity, 0) >= threshold_value
        ]

        # Calculate estimated impact by category
        impact_by_category = {}
        for suggestion in filtered_suggestions:
            category = suggestion.category
            if category not in impact_by_category:
                impact_by_category[category] = 0
            impact_by_category[category] += suggestion.confidence * 10

        # Generate action plan
        action_plan = improvement_engine.generate_action_plan(
            filtered_suggestions,
            max_items=10
        )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'total_suggestions': len(suggestions),
                'filtered_suggestions': len(filtered_suggestions),
                'auto_applicable_count': len([s for s in filtered_suggestions if s.can_auto_apply]),
                'estimated_impact': impact_by_category,
                'implementation_complexity': action_plan.get('estimated_total_effort', 'medium'),
                'action_plan_summary': {
                    'priority_items': action_plan.get('priority_items', [])[:5],
                    'estimated_effort': action_plan.get('estimated_total_effort')
                },
                'priority_threshold': priority_threshold,
                'efficiency_tip': 'Use response_format="detailed" for all suggestions with details'
            }
        else:
            data = {
                'skill_name': skill_name,
                'suggestions': [s.to_dict() for s in filtered_suggestions],
                'total_suggestions': len(suggestions),
                'filtered_suggestions': len(filtered_suggestions),
                'estimated_impact': impact_by_category,
                'implementation_complexity': action_plan.get('estimated_total_effort', 'medium'),
                'auto_applicable': [s.to_dict() for s in filtered_suggestions if s.can_auto_apply],
                'action_plan': action_plan,
                'priority_threshold': priority_threshold,
                'used_ai_agents': use_ai_agents
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'evaluation_id': metrics.evaluation_id,
                'health_score': metrics.overall_health_score
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to suggest improvements: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has execution data",
                    "Try evaluate_quality first to verify skill health",
                    "Check priority_threshold is valid (critical, high, medium, low)",
                    "Verify skill_name is correct"
                ],
                "example_fix": "suggest_improvements('test_orchestrator', priority_threshold='medium')"
            }
        )


def apply_improvements(
    skill_name: str,
    improvements: list,
    create_branch: bool = True,
    run_tests: bool = True,
    require_approval: bool = True,
    dry_run: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Apply improvements with validation (Phase 4 - Full Implementation).

    Safely applies code improvements with risk assessment, backup creation,
    git integration, test validation, and rollback capabilities.

    Args:
        skill_name: Name of the skill to improve
        improvements: List of improvements to apply (dicts or ImprovementSuggestion objects)
        create_branch: Create git branch for changes
        run_tests: Run validation tests after applying
        require_approval: Require approval for high-risk changes
        dry_run: If True, simulate changes without applying them
        response_format: "summary" (counts only) or "detailed" (all results)
        **kwargs: Additional parameters

    Returns:
        OperationResult with application results including:
        - applied: List of successfully applied improvements
        - failed: List of failed improvements
        - skipped: List of skipped improvements
        - requires_approval: List of improvements requiring manual approval
        - backup_id: ID for rollback
        - branch_name: Created git branch (if create_branch=True)

    Token Efficiency:
        - Use response_format="summary" for counts and status
        - Use response_format="detailed" for all applied/failed/skipped items
        - Summary mode saves 85-95% tokens
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, applicator, _, _, _ = _get_instances()

        if not improvements:
            return OperationResult(
                success=True,
                data={
                    'skill_name': skill_name,
                    'applied': [],
                    'failed': [],
                    'skipped': [],
                    'requires_approval': [],
                    'message': 'No improvements to apply'
                },
                duration=time.time() - start_time
            )

        # Convert improvement dicts to ImprovementSuggestion objects if needed
        suggestions = []
        for imp in improvements:
            if isinstance(imp, ImprovementSuggestion):
                suggestions.append(imp)
            elif isinstance(imp, dict):
                # Convert dict to ImprovementSuggestion
                suggestions.append(ImprovementSuggestion(
                    category=imp.get('category', 'quality'),
                    severity=imp.get('severity', 'medium'),
                    description=imp.get('description', 'Improvement'),
                    expected_impact=imp.get('expected_impact', 'Improvement'),
                    confidence=imp.get('confidence', 0.7),
                    can_auto_apply=imp.get('can_auto_apply', False),
                    location=imp.get('location'),
                    suggested_code=imp.get('suggested_code'),
                    metadata=imp.get('metadata')
                ))
            else:
                return OperationResult(
                    success=False,
                    error=f"Invalid improvement format: {type(imp)}",
                    error_code=EvaluatorError.INVALID_PARAMETERS,
                    duration=time.time() - start_time
                )

        # Apply improvements using ImprovementApplicator
        result = applicator.apply_improvements(
            skill_name=skill_name,
            suggestions=suggestions,
            create_branch=create_branch,
            run_tests=run_tests,
            require_approval=require_approval,
            dry_run=dry_run
        )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'skill_name': result['skill_name'],
                'dry_run': result['dry_run'],
                'total_suggestions': result['total_suggestions'],
                'attempted': result['attempted'],
                'applied_count': len(result['applied']),
                'failed_count': len(result['failed']),
                'skipped_count': len(result['skipped']),
                'requires_approval_count': len(result['requires_approval']),
                'branch_name': result.get('branch_name'),
                'backup_id': result.get('backup_id'),
                'rollback_available': result.get('rollback_available', False),
                'message': result.get('message', 'Improvements processed'),
                'efficiency_tip': 'Use response_format="detailed" for all applied/failed/skipped items'
            }
        else:
            data = {
                'skill_name': result['skill_name'],
                'dry_run': result['dry_run'],
                'total_suggestions': result['total_suggestions'],
                'attempted': result['attempted'],
                'applied': result['applied'],
                'failed': result['failed'],
                'skipped': result['skipped'],
                'requires_approval': result['requires_approval'],
                'branch_name': result.get('branch_name'),
                'backup_id': result.get('backup_id'),
                'rollback_available': result.get('rollback_available', False),
                'validation': result.get('validation'),
                'message': result.get('message', 'Improvements processed')
            }

        return OperationResult(
            success=result['success'],
            data=data,
            duration=duration,
            metadata={
                'create_branch': create_branch,
                'run_tests': run_tests,
                'require_approval': require_approval
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to apply improvements: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure suggestions list is from suggest_improvements operation",
                    "Check that skill files exist and are writable",
                    "Try with create_branch=True for safer testing",
                    "Verify git is configured if create_branch=True"
                ],
                "example_fix": "apply_improvements('skill', suggestions, create_branch=True, run_tests=False)"
            }
        )


def generate_report(
    skill_name: str,
    report_type: str = "full",
    time_period: str = "30d",
    include_recommendations: bool = True,
    format: str = "markdown",
    include_trends: bool = True,
    include_history: bool = True,
    include_improvements: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate comprehensive evaluation report (Phase 5 - Complete).

    Uses the ReportGenerator to create professional reports in multiple formats
    with visualizations, trends, and comprehensive analysis.

    Args:
        skill_name: Name of the skill to report on
        report_type: Type of report ('full', 'summary', 'trends', 'comparison')
        time_period: Time period to cover (e.g., '30d', '7d', '90d')
        include_recommendations: Include improvement recommendations
        format: Output format ('markdown', 'json', 'html')
        include_trends: Include trend analysis section
        include_history: Include execution history section
        include_improvements: Include improvement history
        response_format: "summary" (report metadata) or "detailed" (full report content)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing the comprehensive report

    Token Efficiency:
        - Use response_format="summary" for report summary and key metrics
        - Use response_format="detailed" for complete report content
        - Summary mode saves 90-95% tokens (report content can be large)
    """
    start_time = time.time()

    try:
        history_tracker, _, quality_evaluator, _, _, _, _, report_generator, _, _ = _get_instances()

        # Parse time period
        days = int(time_period.replace('d', ''))

        # Generate evaluation metrics
        metrics = quality_evaluator.evaluate(
            skill_name,
            execution_samples=200,
            time_period_days=days
        )

        # Generate report using ReportGenerator
        report_data = report_generator.generate_report(
            skill_name=skill_name,
            metrics=metrics,
            report_type=report_type,
            format=format,
            time_period_days=days,
            include_recommendations=include_recommendations,
            include_trends=include_trends,
            include_history=include_history
        )

        # Get improvement history if requested
        improvement_stats = None
        if include_improvements:
            improvement_stats = history_tracker.get_improvement_stats(
                skill_name=skill_name,
                time_period_days=days
            )

        # Generate dashboard data
        dashboard_data = report_generator.generate_dashboard_data(
            skill_name=skill_name,
            metrics=metrics,
            time_period_days=days
        )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'summary': {
                    'overall_health': metrics.overall_health_score,
                    'health_grade': metrics.get_health_grade(),
                    'trend': metrics.health_trend,
                    'critical_issues': len(metrics.priority_fixes),
                    'recent_improvements': improvement_stats['total_improvements'] if improvement_stats else 0
                },
                'report_metadata': {
                    'format': format,
                    'report_type': report_type,
                    'time_period_days': days,
                    'generated_at': report_data['generated_at'],
                    'sections': list(report_data.get('sections', {}).keys())
                },
                'top_recommendations': [s.to_dict() for s in metrics.improvement_opportunities[:3]],
                'efficiency_tip': 'Use response_format="detailed" for full report content'
            }
        else:
            data = {
                'report': report_data['content'],
                'report_data': report_data,
                'summary': {
                    'overall_health': metrics.overall_health_score,
                    'health_grade': metrics.get_health_grade(),
                    'trend': metrics.health_trend,
                    'critical_issues': len(metrics.priority_fixes),
                    'recent_improvements': improvement_stats['total_improvements'] if improvement_stats else 0
                },
                'recommendations': [s.to_dict() for s in metrics.improvement_opportunities[:10]],
                'improvement_stats': improvement_stats,
                'dashboard_data': dashboard_data,
                'format': format,
                'report_type': report_type,
                'time_period_days': days,
                'generated_at': report_data['generated_at']
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'evaluation_id': metrics.evaluation_id,
                'report_generator_version': '0.5.0'
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to generate report: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has execution history",
                    "Verify report_type is valid (summary, detailed, executive, technical)",
                    "Check time_period format (e.g., '7d', '30d')",
                    "Try with report_type='summary' for simpler report"
                ],
                "example_fix": "generate_report('test_orchestrator', report_type='summary', time_period='7d')"
            }
        )


def analyze_trends(
    skill_name: str,
    time_period_days: int = 30,
    bucket_size_hours: int = 24,
    operation: Optional[str] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze performance trends over time (Phase 2).

    Provides time-series analysis, forecasting, and anomaly detection.

    Args:
        skill_name: Name of the skill to analyze
        time_period_days: Days to analyze (default: 30)
        bucket_size_hours: Size of time buckets for aggregation (default: 24)
        operation: Specific operation to analyze (None for all)
        response_format: "summary" (trend direction) or "detailed" (full time-series)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing trend analysis

    Token Efficiency:
        - Use response_format="summary" for trend direction and key anomalies
        - Use response_format="detailed" for complete time-series data
        - Summary mode saves 85-95% tokens
    """
    start_time = time.time()

    try:
        _, _, _, _, trend_analyzer, _, _, _, _, _ = _get_instances()

        # Perform trend analysis
        analysis = trend_analyzer.analyze_trends(
            skill_name=skill_name,
            time_period_days=time_period_days,
            bucket_size_hours=bucket_size_hours,
            operation=operation
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('error', 'Insufficient data'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time,
                metadata={'recommendation': analysis.get('recommendation')}
            )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'operation': operation,
                'time_period_days': time_period_days,
                'trend': analysis.get('trend', 'unknown'),
                'trend_strength': analysis.get('trend_strength', 0),
                'anomaly_count': len(analysis.get('anomalies', [])),
                'forecast_available': analysis['forecast'].get('available', False),
                'forecast_direction': analysis['forecast'].get('direction') if analysis['forecast'].get('available') else None,
                'efficiency_tip': 'Use response_format="detailed" for complete time-series data'
            }
        else:
            data = analysis

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'analysis_type': 'time_series_trend',
                'forecast_available': analysis['forecast'].get('available', False)
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to analyze trends: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has sufficient execution history",
                    "Verify time_period_days is a positive integer",
                    "Try with a longer time period for better trend detection",
                    "Check if the skill has been used consistently over time"
                ],
                "example_fix": "analyze_trends('test_orchestrator', time_period_days=30)"
            }
        )


def detect_patterns(
    skill_name: str,
    time_period_days: int = 30,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Detect recurring patterns in execution behavior (Phase 2).

    Identifies time-of-day patterns, day-of-week patterns, and error clustering.

    Args:
        skill_name: Name of the skill
        time_period_days: Days to analyze (default: 30)
        response_format: "summary" (pattern counts) or "detailed" (all patterns)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing detected patterns

    Token Efficiency:
        - Use response_format="summary" for pattern counts and top patterns
        - Use response_format="detailed" for all detected patterns
        - Summary mode saves 80-90% tokens
    """
    start_time = time.time()

    try:
        _, _, _, _, trend_analyzer, _, _, _, _, _ = _get_instances()

        # Detect patterns
        patterns = trend_analyzer.detect_patterns(
            skill_name=skill_name,
            time_period_days=time_period_days
        )

        if not patterns.get('has_data'):
            return OperationResult(
                success=False,
                error=patterns.get('error', 'Insufficient data'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'skill_name': skill_name,
                'time_period_days': time_period_days,
                'patterns_found': patterns.get('patterns_found', 0),
                'time_of_day_patterns': len(patterns.get('time_of_day_patterns', [])),
                'day_of_week_patterns': len(patterns.get('day_of_week_patterns', [])),
                'error_clusters': len(patterns.get('error_clusters', [])),
                'top_patterns': patterns.get('top_patterns', [])[:3],
                'efficiency_tip': 'Use response_format="detailed" for all detected patterns'
            }
        else:
            data = patterns

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                'patterns_found': patterns.get('patterns_found', 0)
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to detect patterns: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure the skill has sufficient execution history",
                    "Try with a longer time_period_days for better pattern detection",
                    "Verify the skill has varied execution times and parameters",
                    "Check min_sample_size is reasonable (default: 10)"
                ],
                "example_fix": "detect_patterns('test_orchestrator', time_period_days=30, min_sample_size=10)"
            }
        )


def analyze_skill_interactions(
    time_period_days: int = 30,
    min_interactions: int = 2,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze interactions between skills (Phase 6).

    Identifies patterns of skill usage, dependencies, and
    interaction frequencies to understand workflow patterns.

    Args:
        time_period_days: Time period to analyze (default: 30)
        min_interactions: Minimum interaction count to include (default: 2)
        response_format: "summary" (interaction counts) or "detailed" (all interactions)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing interaction analysis

    Token Efficiency:
        - Use response_format="summary" for interaction counts and top pairs
        - Use response_format="detailed" for all interaction patterns
        - Summary mode saves 85-90% tokens
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, cross_skill_analyzer, _ = _get_instances()

        # Analyze skill interactions
        analysis = cross_skill_analyzer.analyze_skill_interactions(
            time_period_days=time_period_days,
            min_interactions=min_interactions
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'time_period_days': time_period_days,
                'total_interactions': analysis.get('total_interactions', 0),
                'unique_skill_pairs': analysis.get('unique_skill_pairs', 0),
                'most_common_interactions': analysis.get('most_common_interactions', [])[:5],
                'interaction_network_size': len(analysis.get('interaction_network', [])),
                'efficiency_tip': 'Use response_format="detailed" for complete interaction patterns'
            }
        else:
            data = analysis

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={'time_period_days': time_period_days}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to analyze skill interactions: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure multiple skills have execution history",
                    "Try with a longer time_period_days to capture more interactions",
                    "Check min_interactions threshold (default: 2)",
                    "Verify skills have been used together in workflows"
                ],
                "example_fix": "analyze_skill_interactions(time_period_days=30, min_interactions=2)"
            }
        )


def detect_dependency_chains(
    time_period_days: int = 30,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Detect skill dependency chains and execution sequences (Phase 6).

    Identifies common patterns where one skill is followed by another,
    helping understand workflow dependencies.

    Args:
        time_period_days: Time period to analyze (default: 30)
        response_format: "summary" (chain counts) or "detailed" (all chains)
        **kwargs: Additional parameters

    Returns:
        OperationResult containing dependency chain analysis

    Token Efficiency:
        - Use response_format="summary" for chain counts and top sequences
        - Use response_format="detailed" for all dependency chains
        - Summary mode saves 85-95% tokens
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, cross_skill_analyzer, _ = _get_instances()

        # Detect dependency chains
        analysis = cross_skill_analyzer.detect_dependency_chains(
            time_period_days=time_period_days
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                'time_period_days': time_period_days,
                'total_chains': analysis.get('total_chains', 0),
                'unique_chains': analysis.get('unique_chains', 0),
                'most_common_chains': analysis.get('most_common_chains', [])[:5],
                'max_chain_length': analysis.get('max_chain_length', 0),
                'efficiency_tip': 'Use response_format="detailed" for all dependency chains'
            }
        else:
            data = analysis

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={'time_period_days': time_period_days}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to detect dependency chains: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration,
            metadata={
                "suggestions": [
                    "Ensure multiple skills have execution history",
                    "Try with a longer time_period_days to capture chains",
                    "Check min_chain_length is reasonable (default: 2)",
                    "Verify skills have dependency relationships in execution flow"
                ],
                "example_fix": "detect_dependency_chains(time_period_days=30, min_chain_length=2)"
            }
        )


def analyze_workflow_patterns(
    time_period_days: int = 30,
    min_pattern_length: int = 2,
    max_pattern_length: int = 5,
    **kwargs
) -> OperationResult:
    """
    Analyze common workflow patterns (Phase 6).

    Identifies frequently occurring sequences of skill executions
    to understand common usage patterns.

    Args:
        time_period_days: Time period to analyze (default: 30)
        min_pattern_length: Minimum pattern length (default: 2)
        max_pattern_length: Maximum pattern length (default: 5)

    Returns:
        OperationResult containing workflow pattern analysis
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, cross_skill_analyzer, _ = _get_instances()

        # Analyze workflow patterns
        analysis = cross_skill_analyzer.analyze_workflow_patterns(
            time_period_days=time_period_days,
            min_pattern_length=min_pattern_length,
            max_pattern_length=max_pattern_length
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=analysis,
            duration=duration,
            metadata={
                'time_period_days': time_period_days,
                'min_pattern_length': min_pattern_length,
                'max_pattern_length': max_pattern_length
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to analyze workflow patterns: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


def identify_bottlenecks(
    time_period_days: int = 30,
    **kwargs
) -> OperationResult:
    """
    Identify workflow bottlenecks (Phase 6).

    Detects skills that may be slowing down workflows based on
    frequency, duration, and failure rates.

    Args:
        time_period_days: Time period to analyze (default: 30)

    Returns:
        OperationResult containing bottleneck analysis
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, cross_skill_analyzer, _ = _get_instances()

        # Identify bottlenecks
        analysis = cross_skill_analyzer.identify_bottlenecks(
            time_period_days=time_period_days
        )

        if not analysis.get('has_data'):
            return OperationResult(
                success=False,
                error=analysis.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=analysis,
            duration=duration,
            metadata={'time_period_days': time_period_days}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to identify bottlenecks: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


def suggest_workflow_optimizations(
    time_period_days: int = 30,
    **kwargs
) -> OperationResult:
    """
    Suggest workflow optimizations (Phase 6).

    Analyzes cross-skill patterns and suggests optimizations
    for improved performance and reliability.

    Args:
        time_period_days: Time period to analyze (default: 30)

    Returns:
        OperationResult containing optimization suggestions
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, cross_skill_analyzer, _ = _get_instances()

        # Suggest optimizations
        analysis = cross_skill_analyzer.suggest_workflow_optimizations(
            time_period_days=time_period_days
        )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=analysis,
            duration=duration,
            metadata={'time_period_days': time_period_days}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to suggest optimizations: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


def benchmark_skills(
    skill_names: Optional[list] = None,
    time_period_days: int = 30,
    min_executions: int = 10,
    **kwargs
) -> OperationResult:
    """
    Benchmark multiple skills for comparison (Phase 6).

    Compares performance, reliability, and quality metrics
    across multiple skills.

    Args:
        skill_names: List of skills to benchmark (None for all)
        time_period_days: Time period for metrics (default: 30)
        min_executions: Minimum executions required (default: 10)

    Returns:
        OperationResult containing benchmark results
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, _, benchmarking_system = _get_instances()

        # Benchmark skills
        results = benchmarking_system.benchmark_skills(
            skill_names=skill_names,
            time_period_days=time_period_days,
            min_executions=min_executions
        )

        if not results.get('has_data'):
            return OperationResult(
                success=False,
                error=results.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=results,
            duration=duration,
            metadata={
                'time_period_days': time_period_days,
                'min_executions': min_executions
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to benchmark skills: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


def compare_skills(
    skill1: str,
    skill2: str,
    time_period_days: int = 30,
    **kwargs
) -> OperationResult:
    """
    Compare two skills head-to-head (Phase 6).

    Provides detailed comparison of performance, reliability,
    and quality between two skills.

    Args:
        skill1: First skill name
        skill2: Second skill name
        time_period_days: Time period for comparison (default: 30)

    Returns:
        OperationResult containing comparison results
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, _, benchmarking_system = _get_instances()

        # Compare skills
        results = benchmarking_system.compare_skills(
            skill1=skill1,
            skill2=skill2,
            time_period_days=time_period_days
        )

        if not results.get('has_data'):
            return OperationResult(
                success=False,
                error=results.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=results,
            duration=duration,
            metadata={'time_period_days': time_period_days}
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to compare skills: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


def generate_leaderboard(
    category: str = 'overall',
    time_period_days: int = 30,
    top_n: int = 10,
    **kwargs
) -> OperationResult:
    """
    Generate skills leaderboard (Phase 6).

    Creates a ranked list of skills based on specified category.

    Args:
        category: Category to rank by ('overall', 'performance', 'reliability', 'quality')
        time_period_days: Time period for rankings (default: 30)
        top_n: Number of top skills to include (default: 10)

    Returns:
        OperationResult containing leaderboard
    """
    start_time = time.time()

    try:
        _, _, _, _, _, _, _, _, _, benchmarking_system = _get_instances()

        # Generate leaderboard
        results = benchmarking_system.generate_leaderboard(
            category=category,
            time_period_days=time_period_days,
            top_n=top_n
        )

        if not results.get('has_data'):
            return OperationResult(
                success=False,
                error=results.get('message', 'No data available'),
                error_code=EvaluatorError.INSUFFICIENT_DATA,
                duration=time.time() - start_time
            )

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=results,
            duration=duration,
            metadata={
                'category': category,
                'time_period_days': time_period_days,
                'top_n': top_n
            }
        )

    except Exception as e:
        duration = time.time() - start_time
        return OperationResult(
            success=False,
            error=f"Failed to generate leaderboard: {str(e)}",
            error_code=EvaluatorError.ANALYSIS_FAILED,
            duration=duration
        )


# Utility functions for testing
def get_history_tracker():
    """Get the history tracker instance (for testing/debugging)."""
    tracker, _, _, _, _, _, _, _, _, _ = _get_instances()
    return tracker


def get_monitor():
    """Get the monitor instance (for testing/debugging)."""
    _, monitor, _, _, _, _, _, _, _, _ = _get_instances()
    return monitor


def get_quality_evaluator():
    """Get the quality evaluator instance (for testing/debugging)."""
    _, _, evaluator, _, _, _, _, _, _, _ = _get_instances()
    return evaluator


def get_performance_analyzer():
    """Get the performance analyzer instance (for testing/debugging)."""
    _, _, _, analyzer, _, _, _, _, _, _ = _get_instances()
    return analyzer


def get_trend_analyzer():
    """Get the trend analyzer instance (for testing/debugging)."""
    _, _, _, _, analyzer, _, _, _, _, _ = _get_instances()
    return analyzer


def get_cross_skill_analyzer():
    """Get the cross-skill analyzer instance (for testing/debugging)."""
    _, _, _, _, _, _, _, _, analyzer, _ = _get_instances()
    return analyzer


def get_benchmarking_system():
    """Get the benchmarking system instance (for testing/debugging)."""
    _, _, _, _, _, _, _, _, _, benchmarking = _get_instances()
    return benchmarking
