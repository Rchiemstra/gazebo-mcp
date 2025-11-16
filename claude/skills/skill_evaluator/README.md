# Skill Evaluator

A meta-skill that monitors, evaluates, and improves other skills through real-time analysis and AI-powered suggestions.

## Quick Start

```python
from skills.skill_evaluator import operations

# Evaluate a skill
result = operations.evaluate_quality(
    skill_name='test-orchestrator',
    execution_samples=50
)

print(f"Health Score: {result.data['health_score']}/100")
```

## Features

- **Real-time monitoring** of skill executions
- **Multi-dimensional evaluation** (quality, performance, reliability, code quality)
- **AI-powered improvement suggestions** using specialized agents
- **Safe automated improvements** with validation and rollback
- **Comprehensive reporting** with trends and insights

## Operations

### 1. monitor_execution
Monitor a skill execution in real-time.

```python
result = operations.monitor_execution(
    skill_name='refactor-assistant',
    operation='detect_code_smells',
    parameters={'file_path': 'src/example.py'}
)
```

### 2. evaluate_quality
Comprehensive quality assessment.

```python
result = operations.evaluate_quality(
    skill_name='pr-review-assistant',
    execution_samples=100,
    include_code_analysis=True
)
```

### 3. analyze_performance
Performance regression detection.

```python
result = operations.analyze_performance(
    skill_name='doc-generator',
    baseline_period='7d',
    regression_threshold=0.3
)
```

### 4. suggest_improvements
AI-powered improvement suggestions.

```python
result = operations.suggest_improvements(
    skill_name='test-orchestrator',
    focus_areas=['performance', 'quality']
)
```

### 5. apply_improvements
Apply improvements safely.

```python
result = operations.apply_improvements(
    skill_name='refactor-assistant',
    improvements=suggestions,
    create_branch=True,
    run_tests=True
)
```

### 6. generate_report
Generate evaluation reports.

```python
result = operations.generate_report(
    skill_name='all',
    report_type='summary',
    time_period='30d'
)
```

## Architecture

### Core Components

1. **ExecutionHistoryTracker** - Tracks and persists execution history
2. **ExecutionMonitor** - Monitors executions and collects metrics
3. **QualityEvaluator** - Evaluates skill quality across multiple dimensions
4. **PerformanceAnalyzer** - Detects regressions and bottlenecks
5. **ImprovementEngine** - Generates AI-powered suggestions
6. **ImprovementApplicator** - Applies changes safely with validation

### Integration with Existing Skills

The evaluator leverages existing skills:
- **test-orchestrator** for validation
- **doc-generator** for reports
- **git-workflow-assistant** for git operations

And uses specialized agents:
- **Explore agent** for code understanding
- **debugging-detective** for failure analysis
- **code-architecture-mentor** for design advice
- **python-best-practices** for optimizations

## Development Phases

### Phase 1: Foundation (Current)
- Core data models
- Execution history tracking
- Basic monitoring
- Quality evaluation

### Phase 2: Analysis & Insights
- Performance analysis
- Regression detection
- Trend analysis

### Phase 3: Self-Improvement
- AI-powered suggestions
- Code analysis
- Failure pattern detection

### Phase 4: Automation
- Safe auto-application
- Git integration
- Test validation

### Phase 5: Reporting
- Comprehensive reports
- Continuous monitoring
- Alerting system

### Phase 6: Advanced
- Cross-skill analysis
- Predictive detection
- Parameter optimization

## Safety & Approval

The evaluator prioritizes safety:
- **Risk assessment** before any changes
- **Explicit approval** for high-impact changes
- **Validation** using test-orchestrator
- **Rollback mechanism** for failed improvements
- **Quality gates** to prevent degradation

## Examples

See `demo.py` for comprehensive usage examples.

## Contributing

When extending this skill:
1. Follow OperationResult pattern
2. Use existing agents via Task tool
3. Add proper error handling
4. Update tests
5. Document changes

## Version

Current: 0.1.0 (Phase 1 - Foundation)

## License

Part of the Claude Code skills ecosystem.
