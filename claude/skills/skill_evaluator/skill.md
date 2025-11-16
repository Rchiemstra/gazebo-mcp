---
name: skill-evaluator
version: 0.6.0
description: Meta-skill that monitors, evaluates, and improves other skills through real-time analysis, AI-powered suggestions, safe automated application, comprehensive reporting, cross-skill analysis, and benchmarking
author: Claude Code Team
category: meta-analysis
tags:
  - monitoring
  - evaluation
  - self-improvement
  - meta-analysis
  - quality-assurance
  - benchmarking
  - workflow-optimization
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
activation_mode: manual
dependencies:
  - test-orchestrator
  - doc-generator
  - git-workflow-assistant
operations:
  monitor_execution: "Real-time monitoring of skill execution with metrics collection"
  evaluate_quality: "Comprehensive quality assessment of skill performance and code"
  analyze_performance: "Performance regression detection and bottleneck identification"
  suggest_improvements: "AI-powered improvement suggestions using specialized agents"
  apply_improvements: "Safe application of improvements with validation and rollback"
  generate_report: "Comprehensive evaluation reports with trends and recommendations"
  analyze_skill_interactions: "Analyze interaction patterns between different skills"
  detect_dependency_chains: "Detect and visualize skill dependency chains"
  analyze_workflow_patterns: "Identify common workflow patterns and sequences"
  identify_bottlenecks: "Find skills that slow down workflow execution"
  suggest_workflow_optimizations: "Suggest optimizations for skill workflows"
  benchmark_skills: "Compare skill performance across time periods"
  compare_skills: "Head-to-head comparison of multiple skills"
  generate_leaderboard: "Generate ranked leaderboard of skill performance"
---

# Skill Evaluator

A meta-skill that monitors skill executions in real-time, evaluates their quality and performance, and automatically suggests or applies improvements to skill implementations.

## Overview

The Skill Evaluator acts as a continuous improvement system for the entire skills ecosystem. It:

- **Monitors** all skill executions in real-time
- **Evaluates** quality, performance, reliability, and code quality
- **Detects** regressions and performance issues automatically
- **Suggests** improvements using specialized AI agents
- **Applies** safe improvements with approval gates
- **Reports** on skill health and trends over time

## Key Features

### 1. Real-Time Monitoring
- Intercepts all skill invocations
- Collects detailed metrics (duration, success rate, errors)
- Tracks resource usage (CPU, memory, I/O)
- Maintains execution history with persistence

### 2. Multi-Dimensional Evaluation
- **Quality**: Output quality, correctness, consistency
- **Performance**: Speed, efficiency, regression detection
- **Reliability**: Error handling, recovery capability
- **Code Quality**: Maintainability, complexity, test coverage

### 3. Self-Improvement Loop
Uses existing agents to analyze and improve skills:
- **Explore agent**: Understands skill implementations
- **debugging-detective**: Analyzes failure patterns
- **code-architecture-mentor**: Suggests architectural improvements
- **python-best-practices**: Language-specific optimizations

### 4. Safety-First Automation
- Risk assessment before changes
- Explicit approval for high-impact changes
- Validation using test-orchestrator
- Rollback mechanism for failed improvements
- Git integration via git-workflow-assistant

## Operations

### monitor_execution
Real-time monitoring of a skill execution.

**Parameters:**
- `skill_name` (str): Name of the skill to monitor
- `operation` (str): Operation being executed
- `parameters` (dict): Operation parameters
- `collect_metrics` (bool, optional): Whether to collect detailed metrics (default: True)
- `profile_performance` (bool, optional): Whether to profile performance (default: False)

**Returns:**
- `execution_id`: Unique execution identifier
- `basic_metrics`: Collected metrics (duration, status, etc.)
- `performance_profile`: Optional performance profiling data
- `warnings`: List of warnings detected
- `recommendations`: List of immediate recommendations

### evaluate_quality
Comprehensive quality assessment of a skill.

**Parameters:**
- `skill_name` (str): Name of the skill to evaluate
- `execution_samples` (int, optional): Number of recent executions to analyze (default: 100)
- `include_code_analysis` (bool, optional): Whether to analyze code (default: True)
- `validate_outputs` (bool, optional): Whether to validate outputs (default: True)

**Returns:**
- `quality_metrics`: Comprehensive metrics including health score
- `strengths`: List of identified strengths
- `weaknesses`: List of identified weaknesses
- `improvement_opportunities`: Prioritized improvement suggestions
- `health_score`: Overall health score (0-100)
- `trend`: Health trend (improving/stable/declining)

### analyze_performance
Performance regression detection and analysis.

**Parameters:**
- `skill_name` (str): Name of the skill to analyze
- `baseline_period` (str, optional): Period for baseline comparison (default: "7d")
- `regression_threshold` (float, optional): Degradation threshold to flag (default: 0.3)

**Returns:**
- `has_regression`: Boolean indicating if regression detected
- `performance_score`: Current performance score (0-100)
- `comparison`: Baseline vs current metrics
- `bottlenecks`: Identified bottlenecks
- `optimization_suggestions`: Specific optimization recommendations

### suggest_improvements
Generate AI-powered improvement suggestions.

**Parameters:**
- `skill_name` (str): Name of the skill to improve
- `focus_areas` (list, optional): Areas to focus on (default: ['all'])
- `priority_threshold` (str, optional): Minimum priority to return (default: "medium")
- `include_examples` (bool, optional): Include code examples (default: True)

**Returns:**
- `suggestions`: List of improvement suggestions with code examples
- `estimated_impact`: Expected impact by category
- `implementation_complexity`: Overall complexity assessment
- `auto_applicable`: Suggestions safe for automatic application

### apply_improvements
Apply improvements with validation and safety gates.

**Parameters:**
- `skill_name` (str): Name of the skill to improve
- `improvements` (list): List of improvements to apply
- `create_branch` (bool, optional): Create git branch (default: True)
- `run_tests` (bool, optional): Run validation tests (default: True)
- `require_approval` (bool, optional): Require explicit approval (default: True)

**Returns:**
- `applied`: List of successfully applied improvements
- `failed`: List of failed improvements with reasons
- `validation_results`: Test validation results
- `branch_name`: Created git branch name
- `rollback_available`: Whether rollback is possible

### generate_report
Generate comprehensive evaluation reports.

**Parameters:**
- `skill_name` (str): Name of the skill to report on
- `report_type` (str, optional): Type of report (default: "full")
- `time_period` (str, optional): Time period to cover (default: "30d")
- `include_recommendations` (bool, optional): Include recommendations (default: True)
- `format` (str, optional): Output format (default: "markdown")

**Returns:**
- `report`: Formatted report content
- `summary`: Executive summary with key metrics
- `recommendations`: Prioritized recommendations

### analyze_skill_interactions
Analyze interaction patterns between different skills.

**Parameters:**
- `time_period_days` (int, optional): Number of days to analyze (default: 30)
- `min_interactions` (int, optional): Minimum interactions to report (default: 2)

**Returns:**
- `interaction_pairs`: Skills that frequently execute together
- `interaction_strength`: Strength metrics for each pair
- `common_patterns`: Common interaction sequences
- `circular_dependencies`: Any circular dependency patterns detected

### detect_dependency_chains
Detect and visualize skill dependency chains.

**Parameters:**
- `time_period_days` (int, optional): Number of days to analyze (default: 30)

**Returns:**
- `dependency_chains`: Identified dependency chains
- `chain_depth`: Depth of each chain
- `circular_references`: Any circular dependencies
- `critical_skills`: Skills that many others depend on

### analyze_workflow_patterns
Identify common workflow patterns and skill execution sequences.

**Parameters:**
- `time_period_days` (int, optional): Number of days to analyze (default: 30)
- `min_pattern_length` (int, optional): Minimum pattern length (default: 2)
- `max_pattern_length` (int, optional): Maximum pattern length (default: 5)

**Returns:**
- `common_patterns`: Most frequent skill sequences
- `pattern_frequency`: How often each pattern occurs
- `workflow_templates`: Suggested workflow templates
- `optimization_opportunities`: Patterns that could be optimized

### identify_bottlenecks
Find skills that slow down or block workflow execution.

**Parameters:**
- `time_period_days` (int, optional): Number of days to analyze (default: 30)

**Returns:**
- `bottleneck_skills`: Skills identified as bottlenecks
- `bottleneck_score`: Severity score for each bottleneck
- `impact_analysis`: Impact on overall workflow
- `mitigation_suggestions`: Suggestions to reduce bottlenecks

### suggest_workflow_optimizations
Generate suggestions for optimizing skill workflows and sequences.

**Parameters:**
- `time_period_days` (int, optional): Number of days to analyze (default: 30)

**Returns:**
- `optimization_suggestions`: Detailed optimization recommendations
- `parallelization_opportunities`: Skills that could run in parallel
- `caching_opportunities`: Data that could be cached between skills
- `estimated_time_savings`: Expected performance improvements

### benchmark_skills
Compare skill performance metrics across time periods.

**Parameters:**
- `time_period_days` (int, optional): Number of days to benchmark (default: 30)
- `min_executions` (int, optional): Minimum executions required (default: 5)

**Returns:**
- `benchmark_results`: Performance metrics for each skill
- `performance_rankings`: Skills ranked by performance
- `trends`: Performance trends over time
- `outliers`: Skills with unusual performance patterns

### compare_skills
Head-to-head comparison of multiple skills' performance.

**Parameters:**
- `skill_names` (list): List of skill names to compare
- `time_period_days` (int, optional): Number of days to compare (default: 30)
- `metrics` (list, optional): Metrics to compare (default: all)

**Returns:**
- `comparison_matrix`: Side-by-side metric comparison
- `strengths_by_skill`: Each skill's relative strengths
- `weaknesses_by_skill`: Each skill's relative weaknesses
- `recommendations`: Which skill to use in different scenarios

### generate_leaderboard
Generate a ranked leaderboard of skill performance.

**Parameters:**
- `time_period_days` (int, optional): Number of days to include (default: 30)
- `ranking_criteria` (str, optional): Primary ranking metric (default: "health_score")
- `min_executions` (int, optional): Minimum executions required (default: 5)

**Returns:**
- `leaderboard`: Ranked list of skills
- `top_performers`: Top performing skills
- `needs_improvement`: Skills requiring attention
- `category_leaders`: Best skill in each category

## Architecture

### Non-Invasive Integration
- Wraps SkillInvoker without replacing it
- Optional monitoring (can be disabled per skill)
- No changes required to existing skills
- Graceful degradation if evaluator unavailable

### Quality Gates
Automatic intervention when:
- Error rate exceeds 20%
- Performance degrades by more than 30%
- Correctness score drops below 70%
- Code complexity spikes significantly
- Resource usage anomalies detected

## Usage Examples

### Basic Monitoring
```python
from skills.integration.skill_invoker import SkillInvoker
from skills.skill_evaluator import operations as evaluator_ops

invoker = SkillInvoker()

# Monitor an execution
result = evaluator_ops.monitor_execution(
    skill_name='test-orchestrator',
    operation='generate_tests',
    parameters={'source_file': 'src/example.py'},
    collect_metrics=True
)

print(f"Execution ID: {result.data['execution_id']}")
print(f"Duration: {result.data['basic_metrics']['duration']}s")
print(f"Warnings: {result.data['warnings']}")
```

### Quality Evaluation
```python
# Evaluate a skill's quality
result = evaluator_ops.evaluate_quality(
    skill_name='refactor-assistant',
    execution_samples=100,
    include_code_analysis=True
)

print(f"Health Score: {result.data['health_score']}/100")
print(f"Trend: {result.data['trend']}")
print(f"Top Weaknesses: {result.data['weaknesses'][:3]}")
```

### Automated Improvement
```python
# Get improvement suggestions
suggestions = evaluator_ops.suggest_improvements(
    skill_name='pr-review-assistant',
    focus_areas=['performance', 'reliability'],
    priority_threshold='high'
)

# Apply safe improvements
result = evaluator_ops.apply_improvements(
    skill_name='pr-review-assistant',
    improvements=[s for s in suggestions.data['suggestions'] if s['can_auto_apply']],
    create_branch=True,
    run_tests=True
)

print(f"Applied: {len(result.data['applied'])} improvements")
print(f"Branch: {result.data['branch_name']}")
```

## Development Status

**Current Phase:** Phase 6 - Advanced Features (Complete)
**Version:** 0.6.0

### Phase 1: Foundation ✅ Complete
- [x] Directory structure and metadata
- [x] Core data models
- [x] Execution history tracking
- [x] Basic monitoring
- [x] Quality evaluation
- [x] Operations interface
- [x] Demo script
- [x] Unit tests

### Phase 2: Performance Analysis ✅ Complete
- [x] Statistical regression detection
- [x] Bottleneck identification
- [x] Time-series trend analysis
- [x] Anomaly detection
- [x] Performance forecasting
- [x] Pattern detection

### Phase 3: AI-Powered Suggestions ✅ Complete
- [x] Improvement engine with AI coordination
- [x] AST-based code analysis
- [x] Failure pattern analyzer
- [x] Multi-source suggestion generation
- [x] Intelligent prioritization
- [x] Action plan generation

### Phase 4: Automated Improvements ✅ Complete
- [x] SafetyGate risk assessment
- [x] ImprovementApplicator engine
- [x] Backup and rollback system
- [x] Approval gates
- [x] Dry-run mode
- [x] Apply_improvements operation
- [x] Git integration points (simulated)
- [x] Test validation points (simulated)

### Phase 5: Comprehensive Reporting ✅ Complete
- [x] ReportGenerator class with multi-format support
- [x] Rich ASCII visualizations (progress bars, health badges, trend indicators)
- [x] Multiple report types (full, summary, trends, comparison)
- [x] Multiple output formats (Markdown, JSON, HTML)
- [x] Dashboard-ready data generation
- [x] Improvement history tracking
- [x] Impact measurement and effectiveness analysis
- [x] Enhanced generate_report operation

### Phase 6: Advanced Features ✅ Complete
- [x] CrossSkillAnalyzer for interaction pattern analysis
- [x] Time-proximity based interaction detection
- [x] Dependency chain detection and visualization
- [x] Workflow pattern identification
- [x] Bottleneck analysis across skills
- [x] Workflow optimization suggestions
- [x] BenchmarkingSystem for comparative analysis
- [x] Percentile-based ranking system
- [x] Multi-skill comparison capabilities
- [x] Performance leaderboard generation
- [x] 8 new cross-skill operations

### Future Enhancements
- Phase 7: Predictive analytics (failure prediction, proactive optimization)
- Phase 8: Parameter optimization (ML-based parameter tuning)
- Future: Real-time dashboard UI
- Future: Continuous monitoring daemon and alerting
- Future: Complete git-workflow-assistant integration
- Future: Complete test-orchestrator integration

## Dependencies

- **test-orchestrator**: Test generation and validation
- **doc-generator**: Report formatting
- **git-workflow-assistant**: Git operations (branching, commits, PRs)

## Technical Notes

- Uses Task tool to orchestrate specialized agents
- Leverages existing SkillMetrics infrastructure
- Follows OperationResult pattern for consistency
- Implements standardized error codes
- Thread-safe execution history tracking
- JSON-based persistence for metrics

## Contributing

When extending this skill:
1. Follow the established OperationResult pattern
2. Use existing agents via Task tool
3. Add proper error handling with standard error codes
4. Update tests for new functionality
5. Document new operations in skill.md
6. Maintain backward compatibility

## License

Part of the Claude Code skills ecosystem.
