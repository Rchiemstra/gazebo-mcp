# Skill Evaluator & Self-Improvement Agent - Design Plan

## Overview
A meta-skill that monitors skill executions in real-time, evaluates their quality/performance, and automatically suggests or applies improvements to skill implementations.

## Architecture

### Integration with Existing Infrastructure

**Build on top of:**
- `SkillInvoker` - Wrap/extend to intercept all skill executions
- `SkillMetrics` - Extend with quality and correctness metrics
- `OperationResult` - Add evaluation metadata
- `QualityMetrics` pattern from test-orchestrator

**Use existing agents:**
- **Task tool with general-purpose agent** - For code analysis and improvement suggestions
- **Explore agent** - To understand skill implementations before suggesting improvements
- **debugging-detective agent** - To analyze failure patterns
- **code-architecture-mentor** - For architectural improvement suggestions

**Skill name:** `skill-evaluator`

**Operations:**
1. `monitor_execution` - Real-time monitoring of skill runs
2. `evaluate_quality` - Assess output quality and correctness
3. `analyze_performance` - Performance regression detection
4. `suggest_improvements` - Generate improvement recommendations
5. `apply_improvements` - Auto-apply safe improvements (with approval)
6. `generate_report` - Comprehensive evaluation reports

---

## Evaluation Dimensions

```python
@dataclass
class SkillEvaluationMetrics:
    # Existing metrics (from SkillInvoker)
    basic_metrics: SkillMetrics

    # Quality metrics
    output_quality_score: float  # 0-100
    correctness_score: float     # 0-100 (validated against expected outcomes)
    consistency_score: float     # 0-100 (consistent results for same input)

    # Performance metrics
    performance_score: float     # 0-100
    resource_efficiency: float   # 0-100 (CPU, memory, I/O)
    has_regression: bool
    regression_details: Optional[Dict]

    # Reliability metrics
    reliability_score: float     # 0-100
    error_handling_quality: float
    recovery_capability: float

    # Code quality metrics
    code_quality_score: float    # 0-100
    maintainability_index: float
    complexity_score: float
    test_coverage: float

    # Improvement potential
    improvement_opportunities: List[ImprovementSuggestion]
    priority_fixes: List[str]

    # Overall
    overall_health_score: float  # 0-100
    health_trend: str  # 'improving', 'stable', 'declining'
```

```python
@dataclass
class ImprovementSuggestion:
    category: str  # 'performance', 'quality', 'reliability', 'maintainability'
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    location: str  # file:line_number
    current_code: str
    suggested_code: str
    expected_impact: str
    confidence: float  # 0-1
    can_auto_apply: bool
```

---

## Real-Time Monitoring & Intervention

### Execution Monitoring Hook

Extend `SkillInvoker` with monitoring wrapper:

```python
class MonitoredSkillInvoker(SkillInvoker):
    def __init__(self, evaluator_skill):
        super().__init__()
        self.evaluator = evaluator_skill
        self.execution_history = []

    def invoke(self, skill_name, operation, parameters):
        # Pre-execution
        context = self.evaluator.pre_execution_check(
            skill_name, operation, parameters
        )

        # Execute with monitoring
        start_time = time.time()
        result = super().invoke(skill_name, operation, parameters)
        duration = time.time() - start_time

        # Post-execution evaluation
        evaluation = self.evaluator.evaluate_execution(
            skill_name, operation, parameters,
            result, duration, context
        )

        # Intervention if needed
        if evaluation.needs_intervention:
            self.evaluator.intervene(evaluation)

        return result, evaluation
```

### Quality Gates

Automatic intervention triggers:
- **Error rate > 20%** → Analyze common failure patterns
- **Performance degradation > 30%** → Profile and optimize
- **Correctness score < 70%** → Validate logic and outputs
- **Code complexity spike** → Suggest refactoring
- **Resource usage spike** → Investigate memory leaks

---

## Self-Improvement Feedback Loop

### Workflow:

```
1. MONITOR → 2. ANALYZE → 3. EVALUATE → 4. IMPROVE → 5. VALIDATE → 6. APPLY
     ↑                                                                    ↓
     └─────────────────────── CONTINUOUS LOOP ─────────────────────────┘
```

### Implementation using existing agents:

```python
async def self_improvement_cycle(skill_name: str):
    """
    Uses Task tool with various agents to analyze and improve a skill
    """

    # 1. MONITOR - Collect execution data
    metrics = invoker.get_metrics(skill_name)
    recent_executions = get_recent_executions(skill_name, limit=100)

    # 2. ANALYZE - Use Explore agent to understand skill code
    analysis = await run_task(
        subagent_type='Explore',
        prompt=f'''Analyze the {skill_name} skill implementation.
        Focus on:
        - Code structure and patterns
        - Error handling approach
        - Performance bottlenecks
        - Code complexity

        Execution metrics show:
        - Error rate: {metrics.error_rate}%
        - Avg duration: {metrics.avg_duration}s
        - Common errors: {metrics.errors_by_code}
        '''
    )

    # 3. EVALUATE - Use debugging-detective for failure analysis
    if metrics.error_rate > 10:
        failure_analysis = await run_task(
            subagent_type='debugging-detective',
            prompt=f'''Analyze failure patterns for {skill_name}.
            Recent failures: {get_failed_executions(skill_name)}
            Identify root causes and suggest fixes.'''
        )

    # 4. IMPROVE - Use code-architecture-mentor for design improvements
    improvements = await run_task(
        subagent_type='code-architecture-mentor',
        prompt=f'''Based on this analysis:
        {analysis}
        {failure_analysis if exists else ""}

        Suggest architectural and code improvements for {skill_name}.
        Focus on reliability, performance, and maintainability.'''
    )

    # 5. VALIDATE - Use test-orchestrator to generate validation tests
    validation_tests = await invoke_skill(
        'test-orchestrator',
        'generate_tests',
        {'source_file': f'skills/{skill_name}/operations.py'}
    )

    # 6. APPLY - Apply improvements with user approval
    return await apply_improvements_with_approval(
        skill_name, improvements, validation_tests
    )
```

---

## Operations Specification

### Operation 1: monitor_execution

**Purpose:** Real-time monitoring of skill execution

**Parameters:**
```python
{
    'skill_name': str,
    'operation': str,
    'parameters': dict,
    'collect_metrics': bool = True,
    'profile_performance': bool = False
}
```

**Returns:**
```python
{
    'execution_id': str,
    'basic_metrics': SkillMetrics,
    'performance_profile': Optional[dict],  # CPU, memory, I/O
    'warnings': List[str],
    'recommendations': List[str]
}
```

---

### Operation 2: evaluate_quality

**Purpose:** Comprehensive quality assessment

**Uses:**
- **test-orchestrator** for testing quality
- **General-purpose agent** for code analysis
- **Existing QualityMetrics pattern**

**Parameters:**
```python
{
    'skill_name': str,
    'execution_samples': int = 100,  # Recent executions to analyze
    'include_code_analysis': bool = True,
    'validate_outputs': bool = True
}
```

**Returns:**
```python
{
    'quality_metrics': SkillEvaluationMetrics,
    'strengths': List[str],
    'weaknesses': List[str],
    'improvement_opportunities': List[ImprovementSuggestion],
    'health_score': float,
    'trend': str
}
```

---

### Operation 3: analyze_performance

**Purpose:** Performance regression detection

**Parameters:**
```python
{
    'skill_name': str,
    'baseline_period': str = '7d',  # Compare against last 7 days
    'regression_threshold': float = 0.3  # 30% degradation
}
```

**Returns:**
```python
{
    'has_regression': bool,
    'performance_score': float,
    'comparison': {
        'baseline_avg': float,
        'current_avg': float,
        'change_percent': float
    },
    'bottlenecks': List[str],
    'optimization_suggestions': List[ImprovementSuggestion]
}
```

---

### Operation 4: suggest_improvements

**Purpose:** Generate actionable improvement suggestions

**Uses:**
- **Explore agent** to understand code
- **code-architecture-mentor** for design advice
- **debugging-detective** for error analysis
- **python-best-practices** for language-specific improvements

**Parameters:**
```python
{
    'skill_name': str,
    'focus_areas': List[str] = ['all'],  # 'performance', 'quality', 'reliability'
    'priority_threshold': str = 'medium',  # Only return medium+ priority
    'include_examples': bool = True
}
```

**Returns:**
```python
{
    'suggestions': List[ImprovementSuggestion],
    'estimated_impact': Dict[str, float],  # category → impact score
    'implementation_complexity': str,  # 'easy', 'medium', 'complex'
    'auto_applicable': List[ImprovementSuggestion]
}
```

---

### Operation 5: apply_improvements

**Purpose:** Apply improvements (with approval)

**Uses:**
- **Edit tool** to apply code changes
- **test-orchestrator** to validate changes
- **Git workflow** to create branches/commits

**Parameters:**
```python
{
    'skill_name': str,
    'improvements': List[ImprovementSuggestion],
    'create_branch': bool = True,
    'run_tests': bool = True,
    'require_approval': bool = True
}
```

**Returns:**
```python
{
    'applied': List[str],  # Applied improvement IDs
    'failed': List[Dict],  # Failed improvements with reasons
    'validation_results': dict,
    'branch_name': Optional[str],
    'rollback_available': bool
}
```

---

### Operation 6: generate_report

**Purpose:** Comprehensive evaluation report

**Uses:**
- **doc-generator** for formatted reports
- All other evaluation operations

**Parameters:**
```python
{
    'skill_name': str,
    'report_type': str = 'full',  # 'full', 'summary', 'trends'
    'time_period': str = '30d',
    'include_recommendations': bool = True,
    'format': str = 'markdown'  # 'markdown', 'json', 'html'
}
```

**Returns:**
```python
{
    'report': str,  # Formatted report
    'summary': {
        'overall_health': float,
        'trend': str,
        'critical_issues': int,
        'recent_improvements': List[str]
    },
    'recommendations': List[ImprovementSuggestion]
}
```

---

## Implementation Phases & TODO List

### Phase 1: Foundation (Core Evaluation)
**Goal:** Basic monitoring and quality evaluation

- [ ] Create skill-evaluator directory structure
  - [ ] Create `/skills/skill_evaluator/` directory
  - [ ] Create skill.md with metadata and operations
  - [ ] Create __init__.py for package exports
  - [ ] Create README.md with documentation

- [ ] Create core data models
  - [ ] Create `/skills/skill_evaluator/core/models.py`
  - [ ] Implement SkillEvaluationMetrics dataclass
  - [ ] Implement ImprovementSuggestion dataclass
  - [ ] Implement ExecutionContext dataclass

- [ ] Implement execution history tracking
  - [ ] Create `/skills/skill_evaluator/core/history_tracker.py`
  - [ ] Implement ExecutionHistoryTracker class
  - [ ] Add methods: record_execution, get_recent_executions, get_execution_stats
  - [ ] Add persistence (JSON file storage)

- [ ] Implement basic monitoring
  - [ ] Create `/skills/skill_evaluator/core/monitor.py`
  - [ ] Implement ExecutionMonitor class
  - [ ] Add pre_execution_check method
  - [ ] Add post_execution_analysis method
  - [ ] Add basic metrics collection

- [ ] Implement quality evaluator
  - [ ] Create `/skills/skill_evaluator/core/quality_evaluator.py`
  - [ ] Implement QualityEvaluator class
  - [ ] Add output quality scoring
  - [ ] Add consistency analysis
  - [ ] Add strengths/weaknesses identification

- [ ] Implement operations interface
  - [ ] Create `/skills/skill_evaluator/operations.py`
  - [ ] Implement monitor_execution operation
  - [ ] Implement evaluate_quality operation (basic version)
  - [ ] Add proper error handling and OperationResult returns

- [ ] Create demo script
  - [ ] Create `/skills/skill_evaluator/demo.py`
  - [ ] Add example: monitoring a skill execution
  - [ ] Add example: evaluating skill quality

- [ ] Write tests
  - [ ] Create test file for models
  - [ ] Create test file for history tracker
  - [ ] Create test file for monitor
  - [ ] Create test file for quality evaluator

---

### Phase 2: Analysis & Insights
**Goal:** Performance analysis and regression detection

- [ ] Implement performance analyzer
  - [ ] Create `/skills/skill_evaluator/core/performance_analyzer.py`
  - [ ] Implement PerformanceAnalyzer class
  - [ ] Add baseline comparison logic
  - [ ] Add regression detection
  - [ ] Add bottleneck identification

- [ ] Implement resource monitoring
  - [ ] Add CPU usage tracking
  - [ ] Add memory usage tracking
  - [ ] Add I/O metrics tracking
  - [ ] Integrate with ExecutionMonitor

- [ ] Implement trending analysis
  - [ ] Create `/skills/skill_evaluator/core/trend_analyzer.py`
  - [ ] Implement TrendAnalyzer class
  - [ ] Add time-series analysis
  - [ ] Add trend classification (improving/stable/declining)

- [ ] Add analyze_performance operation
  - [ ] Implement in operations.py
  - [ ] Integrate PerformanceAnalyzer
  - [ ] Add comprehensive result formatting

- [ ] Update demo script
  - [ ] Add performance analysis examples
  - [ ] Add regression detection examples

- [ ] Write tests
  - [ ] Test performance analyzer
  - [ ] Test resource monitoring
  - [ ] Test trend analysis

---

### Phase 3: Self-Improvement Loop
**Goal:** AI-powered improvement suggestions

- [ ] Implement improvement suggestion engine
  - [ ] Create `/skills/skill_evaluator/core/improvement_engine.py`
  - [ ] Implement ImprovementEngine class
  - [ ] Add integration with Explore agent
  - [ ] Add integration with code-architecture-mentor agent
  - [ ] Add integration with debugging-detective agent

- [ ] Implement code analyzer
  - [ ] Create `/skills/skill_evaluator/core/code_analyzer.py`
  - [ ] Implement CodeAnalyzer class
  - [ ] Add code complexity analysis
  - [ ] Add maintainability scoring
  - [ ] Add code pattern detection

- [ ] Implement failure pattern analyzer
  - [ ] Create `/skills/skill_evaluator/core/failure_analyzer.py`
  - [ ] Implement FailurePatternAnalyzer class
  - [ ] Add error clustering
  - [ ] Add root cause identification

- [ ] Implement suggestion prioritization
  - [ ] Add confidence scoring
  - [ ] Add impact estimation
  - [ ] Add complexity assessment
  - [ ] Add auto-apply safety checks

- [ ] Add suggest_improvements operation
  - [ ] Implement in operations.py
  - [ ] Integrate ImprovementEngine
  - [ ] Add filtering by focus areas
  - [ ] Add priority thresholding

- [ ] Update demo script
  - [ ] Add improvement suggestion examples
  - [ ] Show agent integration

- [ ] Write tests
  - [ ] Test improvement engine
  - [ ] Test code analyzer
  - [ ] Test failure analyzer

---

### Phase 4: Automated Improvements
**Goal:** Safe automatic application of improvements

- [ ] Implement improvement applicator
  - [ ] Create `/skills/skill_evaluator/core/improvement_applicator.py`
  - [ ] Implement ImprovementApplicator class
  - [ ] Add code change application logic
  - [ ] Add validation logic
  - [ ] Add rollback mechanism

- [ ] Implement safety gates
  - [ ] Add risk assessment
  - [ ] Add approval workflow
  - [ ] Add dry-run mode
  - [ ] Add change verification

- [ ] Integrate with git-workflow-assistant
  - [ ] Add branch creation
  - [ ] Add commit creation
  - [ ] Add PR creation support

- [ ] Integrate with test-orchestrator
  - [ ] Add pre-change test generation
  - [ ] Add post-change validation
  - [ ] Add test coverage checks

- [ ] Add apply_improvements operation
  - [ ] Implement in operations.py
  - [ ] Add batch application support
  - [ ] Add progress reporting

- [ ] Implement A/B testing framework
  - [ ] Create `/skills/skill_evaluator/core/ab_tester.py`
  - [ ] Add before/after comparison
  - [ ] Add statistical significance testing

- [ ] Update demo script
  - [ ] Add improvement application examples
  - [ ] Show git integration
  - [ ] Show validation workflow

- [ ] Write tests
  - [ ] Test improvement applicator
  - [ ] Test safety gates
  - [ ] Test rollback mechanism

---

### Phase 5: Reporting & Continuous Monitoring
**Goal:** Comprehensive reporting and always-on monitoring

- [ ] Implement report generator
  - [ ] Create `/skills/skill_evaluator/core/report_generator.py`
  - [ ] Implement ReportGenerator class
  - [ ] Add markdown formatting
  - [ ] Add JSON formatting
  - [ ] Add HTML formatting (optional)

- [ ] Integrate with doc-generator
  - [ ] Use doc-generator for advanced formatting
  - [ ] Add charts/visualizations (if supported)

- [ ] Implement dashboard data
  - [ ] Create summary views
  - [ ] Add health score visualization
  - [ ] Add trend graphs data

- [ ] Add generate_report operation
  - [ ] Implement in operations.py
  - [ ] Support multiple report types
  - [ ] Add time period filtering

- [ ] Implement continuous monitoring daemon
  - [ ] Create `/skills/skill_evaluator/daemon.py`
  - [ ] Add background monitoring loop
  - [ ] Add configurable check intervals
  - [ ] Add automatic evaluation triggers

- [ ] Implement alerting system
  - [ ] Create `/skills/skill_evaluator/core/alerting.py`
  - [ ] Add threshold-based alerts
  - [ ] Add alert formatting
  - [ ] Add notification hooks

- [ ] Implement improvement history tracking
  - [ ] Track all applied improvements
  - [ ] Track improvement outcomes
  - [ ] Add improvement effectiveness analysis

- [ ] Update demo script
  - [ ] Add report generation examples
  - [ ] Add continuous monitoring example

- [ ] Write comprehensive tests
  - [ ] Test report generator
  - [ ] Test all report formats
  - [ ] Test daemon functionality

---

### Phase 6: Advanced Features
**Goal:** Advanced capabilities and ecosystem integration

- [ ] Implement cross-skill evaluation
  - [ ] Analyze skill interactions
  - [ ] Detect integration issues
  - [ ] Suggest workflow optimizations

- [ ] Implement workflow optimization
  - [ ] Analyze multi-skill chains
  - [ ] Identify inefficient patterns
  - [ ] Suggest parallel execution opportunities

- [ ] Implement predictive failure detection
  - [ ] Add pattern learning
  - [ ] Add anomaly detection
  - [ ] Add early warning system

- [ ] Implement parameter auto-optimization
  - [ ] Add parameter sensitivity analysis
  - [ ] Add automatic tuning
  - [ ] Add optimal parameter suggestions

- [ ] Implement benchmarking system
  - [ ] Create skill performance benchmarks
  - [ ] Add comparative analysis
  - [ ] Add performance leaderboards

- [ ] Implement community feedback integration
  - [ ] Add user rating system
  - [ ] Add improvement voting
  - [ ] Add collaborative improvement

- [ ] Write advanced tests
  - [ ] Test cross-skill analysis
  - [ ] Test predictive capabilities
  - [ ] Test optimization algorithms

---

## Design Decisions

### Use Existing Infrastructure
✅ Build on SkillInvoker, not replace it
✅ Extend SkillMetrics, don't create parallel tracking
✅ Leverage existing agents via Task tool
✅ Use existing skills (test-orchestrator, doc-generator, git-workflow)
✅ Follow established patterns (OperationResult, error codes)

### Non-Invasive Integration
✅ Wrapper pattern for monitoring
✅ Optional evaluation (can disable)
✅ Explicit approval for improvements
✅ Gradual rollout per skill

### Safety First
✅ Never auto-apply high-risk changes
✅ Always validate before applying
✅ Provide rollback mechanism
✅ Require human approval for structural changes

---

## Example Usage

### Scenario 1: Continuous Monitoring
```python
# Enable monitoring for a skill
evaluator.start_monitoring('test-orchestrator', {
    'quality_gates': {
        'error_rate_threshold': 0.15,
        'performance_degradation_threshold': 0.30
    },
    'auto_evaluate_interval': '1h',
    'alert_on_regression': True
})
```

### Scenario 2: On-Demand Evaluation
```python
# Evaluate a skill's quality
evaluation = invoker.invoke('skill-evaluator', 'evaluate_quality', {
    'skill_name': 'refactor-assistant',
    'execution_samples': 100,
    'include_code_analysis': True
})

print(f"Health Score: {evaluation.data['health_score']}/100")
print(f"Trend: {evaluation.data['trend']}")
```

### Scenario 3: Automated Improvement
```python
# Get suggestions
suggestions = invoker.invoke('skill-evaluator', 'suggest_improvements', {
    'skill_name': 'pr-review-assistant',
    'focus_areas': ['performance', 'reliability']
})

# Apply safe improvements automatically
result = invoker.invoke('skill-evaluator', 'apply_improvements', {
    'skill_name': 'pr-review-assistant',
    'improvements': [s for s in suggestions.data['suggestions'] if s.can_auto_apply],
    'create_branch': True,
    'run_tests': True
})
```

---

## Current Progress

**Status:** Planning complete, ready for Phase 1 implementation

**Next Steps:**
1. Create directory structure
2. Implement core data models
3. Build execution history tracker
4. Implement basic monitoring

---

## Notes

- This design leverages the entire ecosystem of existing agents and skills
- The meta-evaluator coordinates specialized agents rather than doing analysis itself
- Safety and human approval are paramount
- Implementation is phased to allow incremental value delivery
- Each phase builds on the previous one
- All phases maintain backward compatibility
