# Skill Evaluation Framework

Comprehensive framework for continuous skill quality monitoring and improvement.

---

## Overview

The skill evaluation framework provides automated monitoring, quality assessment, and improvement recommendations for all skills in the system. It uses the `skill_evaluator` skill to track performance, detect regressions, and ensure skill effectiveness.

---

## Core Concepts

### What Gets Evaluated

**Skill Performance:**
- Execution time and token usage
- Success/failure rates
- Error patterns and frequencies
- Response quality and accuracy

**Skill Quality:**
- Code quality and maintainability
- Documentation completeness
- Error message clarity
- Token efficiency implementation

**Skill Usage:**
- Invocation patterns and frequency
- Parameter usage distributions
- Integration with other skills
- Common workflows and use cases

### Evaluation Dimensions

1. **Performance**: Speed, efficiency, resource usage
2. **Reliability**: Success rates, error handling, stability
3. **Quality**: Code standards, documentation, UX
4. **Impact**: Usage patterns, value delivered, user satisfaction
5. **Security**: Safe operations, sandboxing compliance

---

## Using the Skill Evaluator

### Basic Monitoring

```python
from skills.skill_evaluator import monitor_execution

# Monitor a skill operation
result = monitor_execution(
    skill_name="test_orchestrator",
    operation_name="generate_tests",
    execution_data={
        "duration": 2.5,
        "tokens_used": 1500,
        "success": True,
        "parameters": {"source_file": "payment.py"}
    }
)

if result.success:
    print(f"Execution monitored: {result.data['execution_id']}")
```

### Quality Evaluation

```python
from skills.skill_evaluator import evaluate_quality

# Evaluate skill quality
result = evaluate_quality(
    skill_name="code_analysis",
    quality_metrics={
        "has_response_format": True,
        "has_error_messages": True,
        "has_progressive_disclosure": True,
        "token_efficiency": 0.85,  # 85% savings
        "documentation_score": 0.90
    }
)

if result.success:
    print(f"Quality score: {result.data['quality_score']:.1%}")
    print(f"Grade: {result.data['grade']}")  # A, B, C, D, F
```

### Performance Analysis

```python
from skills.skill_evaluator import analyze_performance

# Analyze performance trends
result = analyze_performance(
    skill_name="verification",
    time_range="last_7_days",
    response_format="summary"
)

if result.success:
    print(f"Avg duration: {result.data['avg_duration']:.2f}s")
    print(f"Success rate: {result.data['success_rate']:.1%}")
    print(f"Token efficiency: {result.data['avg_token_efficiency']:.1%}")
```

### Generate Reports

```python
from skills.skill_evaluator import generate_report

# Generate comprehensive skill report
result = generate_report(
    skill_names=["verification", "llm_judge", "test_orchestrator"],
    report_type="comprehensive",
    output_format="markdown"
)

if result.success:
    print(result.data['report'])
    # Save to file
    with open("skill_quality_report.md", "w") as f:
        f.write(result.data['report'])
```

---

## Automated Evaluation Workflows

### Daily Quality Check

```python
#!/usr/bin/env python3
"""Daily skill quality check workflow."""

from skills.skill_evaluator import (
    evaluate_quality,
    analyze_performance,
    detect_patterns,
    generate_report
)

def daily_quality_check():
    """Run daily quality checks on all skills."""

    skills = [
        "test_orchestrator", "code_analysis", "learning_plan_manager",
        "context_manager", "refactor_assistant", "dependency_guardian",
        "pr_review_assistant", "git_workflow_assistant", "doc_generator",
        "code_search", "spec_to_implementation", "skill_evaluator",
        "verification", "llm_judge"
    ]

    issues = []

    for skill in skills:
        # Check performance
        perf = analyze_performance(skill, time_range="last_24_hours")

        if perf.success:
            if perf.data['success_rate'] < 0.95:
                issues.append(f"⚠️  {skill}: Low success rate ({perf.data['success_rate']:.1%})")

            if perf.data['avg_duration'] > 5.0:
                issues.append(f"⚠️  {skill}: Slow execution ({perf.data['avg_duration']:.2f}s)")

    # Generate report
    report = generate_report(
        skill_names=skills,
        report_type="summary",
        output_format="markdown"
    )

    if issues:
        print("## Issues Detected\n")
        for issue in issues:
            print(issue)
        print()

    if report.success:
        print(report.data['report'])

    return len(issues) == 0

if __name__ == "__main__":
    success = daily_quality_check()
    exit(0 if success else 1)
```

### Regression Detection

```python
#!/usr/bin/env python3
"""Detect performance regressions in skills."""

from skills.skill_evaluator import analyze_trends, detect_patterns

def detect_regressions():
    """Detect performance regressions."""

    skills = ["verification", "llm_judge", "test_orchestrator"]
    regressions = []

    for skill in skills:
        # Analyze trends
        trends = analyze_trends(
            skill_name=skill,
            metrics=["duration", "token_usage", "success_rate"],
            time_range="last_30_days"
        )

        if trends.success:
            for metric, trend in trends.data['trends'].items():
                if trend['direction'] == 'increasing' and metric in ['duration', 'token_usage']:
                    regressions.append({
                        'skill': skill,
                        'metric': metric,
                        'change': trend['change_percent']
                    })
                elif trend['direction'] == 'decreasing' and metric == 'success_rate':
                    regressions.append({
                        'skill': skill,
                        'metric': metric,
                        'change': trend['change_percent']
                    })

    if regressions:
        print("## Regressions Detected\n")
        for reg in regressions:
            print(f"⚠️  {reg['skill']}: {reg['metric']} changed by {reg['change']:+.1f}%")
        return False
    else:
        print("✅ No regressions detected")
        return True

if __name__ == "__main__":
    success = detect_regressions()
    exit(0 if success else 1)
```

### Continuous Improvement

```python
#!/usr/bin/env python3
"""Continuous skill improvement workflow."""

from skills.skill_evaluator import (
    suggest_improvements,
    apply_improvements,
    evaluate_quality
)

def continuous_improvement(skill_name):
    """Suggest and apply improvements to a skill."""

    # Get improvement suggestions
    suggestions = suggest_improvements(
        skill_name=skill_name,
        focus_areas=["performance", "token_efficiency", "error_messages"]
    )

    if not suggestions.success:
        print(f"❌ Failed to get suggestions: {suggestions.error}")
        return False

    print(f"## Improvement Suggestions for {skill_name}\n")

    for suggestion in suggestions.data['suggestions']:
        print(f"**{suggestion['category']}** (Priority: {suggestion['priority']})")
        print(f"  Issue: {suggestion['issue']}")
        print(f"  Suggestion: {suggestion['recommendation']}")
        print(f"  Impact: {suggestion['expected_impact']}")
        print()

    # Apply high-priority improvements automatically
    high_priority = [s for s in suggestions.data['suggestions']
                     if s['priority'] == 'high']

    if high_priority:
        print(f"Applying {len(high_priority)} high-priority improvements...")

        for suggestion in high_priority:
            result = apply_improvements(
                skill_name=skill_name,
                improvements=[suggestion],
                auto_approve=True
            )

            if result.success:
                print(f"✅ Applied: {suggestion['category']}")
            else:
                print(f"❌ Failed: {suggestion['category']}")

    return True

if __name__ == "__main__":
    import sys
    skill = sys.argv[1] if len(sys.argv) > 1 else "verification"
    continuous_improvement(skill)
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/skill_evaluation.yml
name: Skill Quality Evaluation

on:
  push:
    branches: [ main, feat/* ]
  pull_request:
    branches: [ main ]
  schedule:
    # Run daily at 2 AM UTC
    - cron: '0 2 * * *'

jobs:
  evaluate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run daily quality check
      run: |
        python scripts/daily_quality_check.py

    - name: Detect regressions
      run: |
        python scripts/detect_regressions.py

    - name: Generate skill quality report
      run: |
        python scripts/generate_skill_report.py

    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: skill-quality-report
        path: skill_quality_report.md

    - name: Comment on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('skill_quality_report.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '## Skill Quality Report\n\n' + report
          });
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Evaluate skill quality before commit

echo "Running skill quality checks..."

# Run quality check on modified skills
python scripts/check_modified_skills.py

if [ $? -ne 0 ]; then
    echo "❌ Skill quality checks failed"
    echo "Fix issues or use 'git commit --no-verify' to skip"
    exit 1
fi

echo "✅ Skill quality checks passed"
exit 0
```

---

## Monitoring Dashboards

### CLI Dashboard

```python
#!/usr/bin/env python3
"""Real-time skill monitoring dashboard."""

import time
from skills.skill_evaluator import analyze_performance, generate_report

def dashboard():
    """Display real-time skill monitoring dashboard."""

    while True:
        # Clear screen
        print("\033[2J\033[H")

        print("=" * 80)
        print("SKILL MONITORING DASHBOARD")
        print("=" * 80)
        print()

        # Get performance data
        skills = ["verification", "llm_judge", "test_orchestrator"]

        print(f"{'Skill':<25} {'Success Rate':<15} {'Avg Duration':<15} {'Tokens':<15}")
        print("-" * 80)

        for skill in skills:
            perf = analyze_performance(
                skill_name=skill,
                time_range="last_1_hour",
                response_format="summary"
            )

            if perf.success:
                success_rate = perf.data['success_rate']
                avg_duration = perf.data['avg_duration']
                avg_tokens = perf.data.get('avg_token_usage', 0)

                # Color code success rate
                if success_rate >= 0.95:
                    status = "✅"
                elif success_rate >= 0.85:
                    status = "⚠️ "
                else:
                    status = "❌"

                print(f"{skill:<25} {status} {success_rate:>6.1%}     "
                      f"{avg_duration:>6.2f}s        {avg_tokens:>6.0f}")

        print()
        print("Refreshing in 60 seconds... (Ctrl+C to exit)")
        time.sleep(60)

if __name__ == "__main__":
    try:
        dashboard()
    except KeyboardInterrupt:
        print("\nDashboard stopped")
```

### Web Dashboard (Flask Example)

```python
#!/usr/bin/env python3
"""Web-based skill monitoring dashboard."""

from flask import Flask, render_template, jsonify
from skills.skill_evaluator import analyze_performance, generate_report

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/skills')
def get_skills():
    """Get all skill performance data."""
    skills = [
        "test_orchestrator", "code_analysis", "verification", "llm_judge"
    ]

    data = []
    for skill in skills:
        perf = analyze_performance(
            skill_name=skill,
            time_range="last_24_hours",
            response_format="summary"
        )

        if perf.success:
            data.append({
                'name': skill,
                'success_rate': perf.data['success_rate'],
                'avg_duration': perf.data['avg_duration'],
                'avg_tokens': perf.data.get('avg_token_usage', 0),
                'invocation_count': perf.data.get('invocation_count', 0)
            })

    return jsonify(data)

@app.route('/api/report')
def get_report():
    """Get comprehensive skill report."""
    report = generate_report(
        skill_names=["all"],
        report_type="comprehensive",
        output_format="json"
    )

    if report.success:
        return jsonify(report.data)
    else:
        return jsonify({'error': report.error}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## Quality Metrics

### Skill Quality Score

Quality score calculated from multiple dimensions:

```python
def calculate_quality_score(skill_name):
    """
    Calculate comprehensive quality score (0.0 to 1.0).

    Components:
    - Code quality: 20%
    - Documentation: 20%
    - Token efficiency: 20%
    - Error messages: 15%
    - Performance: 15%
    - Security: 10%
    """

    weights = {
        'code_quality': 0.20,
        'documentation': 0.20,
        'token_efficiency': 0.20,
        'error_messages': 0.15,
        'performance': 0.15,
        'security': 0.10
    }

    scores = {
        'code_quality': check_code_quality(skill_name),
        'documentation': check_documentation(skill_name),
        'token_efficiency': check_token_efficiency(skill_name),
        'error_messages': check_error_messages(skill_name),
        'performance': check_performance(skill_name),
        'security': check_security(skill_name)
    }

    total_score = sum(score * weights[metric]
                      for metric, score in scores.items())

    return total_score, scores
```

### Grading Scale

- **A (90-100%)**: Excellent - Best practices followed, high quality
- **B (80-89%)**: Good - Minor improvements needed
- **C (70-79%)**: Acceptable - Several improvements recommended
- **D (60-69%)**: Needs Improvement - Significant issues present
- **F (<60%)**: Failing - Major issues, immediate attention required

---

## Best Practices

### Continuous Monitoring

1. **Run daily quality checks** on all skills
2. **Monitor performance trends** weekly
3. **Detect regressions** immediately
4. **Review quality reports** monthly

### Quality Gates

Set quality gates for skill acceptance:

```python
QUALITY_GATES = {
    'min_quality_score': 0.80,  # B grade minimum
    'min_success_rate': 0.95,   # 95% operations succeed
    'max_avg_duration': 5.0,    # < 5 seconds average
    'min_token_efficiency': 0.70,  # 70% token savings
    'max_error_rate': 0.05,     # < 5% error rate
}

def passes_quality_gates(skill_name):
    """Check if skill passes all quality gates."""

    # Get metrics
    quality = evaluate_quality(skill_name)
    performance = analyze_performance(skill_name, time_range="last_7_days")

    if not (quality.success and performance.success):
        return False, "Failed to evaluate skill"

    checks = {
        'Quality score': quality.data['quality_score'] >= QUALITY_GATES['min_quality_score'],
        'Success rate': performance.data['success_rate'] >= QUALITY_GATES['min_success_rate'],
        'Avg duration': performance.data['avg_duration'] <= QUALITY_GATES['max_avg_duration'],
        'Token efficiency': quality.data.get('token_efficiency', 0) >= QUALITY_GATES['min_token_efficiency'],
        'Error rate': performance.data['error_rate'] <= QUALITY_GATES['max_error_rate'],
    }

    failed = [name for name, passed in checks.items() if not passed]

    if failed:
        return False, f"Failed gates: {', '.join(failed)}"

    return True, "All quality gates passed"
```

### Improvement Prioritization

Prioritize improvements based on impact:

1. **Critical**: Security issues, high error rates, failures
2. **High**: Performance regressions, token inefficiency
3. **Medium**: Documentation gaps, minor bugs
4. **Low**: Code style, minor optimizations

---

## Integration with Other Skills

### With Learning Analytics

```python
from skills.learning_analytics import track_skill_usage
from skills.skill_evaluator import monitor_execution

# Track skill usage in learning context
def track_learning_skill_usage(skill_name, student_id, operation, result):
    """Track skill usage for learning analytics."""

    # Monitor execution
    monitor_execution(
        skill_name=skill_name,
        operation_name=operation,
        execution_data={
            'duration': result.duration,
            'success': result.success,
            'student_id': student_id
        }
    )

    # Track for analytics
    track_skill_usage(
        student_id=student_id,
        skill_name=skill_name,
        operation=operation,
        outcome=result.success
    )
```

### With Verification Skill

```python
from skills.verification import validate_code
from skills.skill_evaluator import evaluate_quality

# Validate skill code quality
def validate_skill_code(skill_path):
    """Validate skill implementation code."""

    operations_file = f"{skill_path}/operations.py"

    with open(operations_file) as f:
        code = f.read()

    # Validate code
    code_result = validate_code(
        code,
        check_style=True,
        check_security=True
    )

    # Evaluate overall quality
    skill_name = skill_path.split('/')[-1]
    quality_result = evaluate_quality(skill_name)

    return code_result, quality_result
```

---

## Troubleshooting

### Low Success Rate

**Symptoms**: Success rate < 95%

**Diagnosis:**
1. Check error logs for patterns
2. Analyze failing operations
3. Review parameter validation

**Solutions:**
- Improve error handling
- Add parameter validation
- Fix identified bugs

### High Token Usage

**Symptoms**: Token efficiency < 70%

**Diagnosis:**
1. Check if response_format is implemented
2. Analyze default response size
3. Review summary mode implementation

**Solutions:**
- Implement response_format parameter
- Reduce default response verbosity
- Add token efficiency tips

### Slow Performance

**Symptoms**: Avg duration > 5 seconds

**Diagnosis:**
1. Profile code execution
2. Check for expensive operations
3. Review algorithm complexity

**Solutions:**
- Optimize expensive operations
- Add caching where appropriate
- Improve algorithm efficiency

---

## Example Reports

### Daily Quality Report

```markdown
# Skill Quality Report - 2025-11-09

## Summary

- **Total Skills**: 14
- **Average Quality Score**: 87.3% (B+)
- **Skills at A grade**: 8
- **Skills needing improvement**: 2

## Top Performers

1. **verification** - 94.2% (A)
   - Excellent token efficiency (85%)
   - Complete documentation
   - Strong performance (1.2s avg)

2. **llm_judge** - 91.8% (A-)
   - Good teaching evaluation accuracy
   - Well-documented operations
   - Efficient execution

3. **test_orchestrator** - 90.5% (A-)
   - High success rate (98.7%)
   - Good token efficiency (82%)
   - Clear error messages

## Needs Attention

1. **code_search** - 72.1% (C+)
   - Missing token efficiency docs in 3 operations
   - Performance could be improved
   - **Action**: Add efficiency documentation

2. **context_manager** - 68.9% (D+)
   - Token efficiency below target (65%)
   - Some error messages lack examples
   - **Action**: Improve summary mode, enhance errors

## Trends (Last 7 Days)

- **Success rates**: Stable at 96.2%
- **Performance**: Slight improvement (-8% avg duration)
- **Token efficiency**: Improved from 80% to 83%

## Recommendations

1. Update code_search documentation (HIGH priority)
2. Improve context_manager token efficiency (MEDIUM)
3. Continue monitoring verification and llm_judge (LOW)
```

---

## Summary

The skill evaluation framework provides:
- ✅ Continuous quality monitoring
- ✅ Performance tracking and regression detection
- ✅ Automated improvement suggestions
- ✅ CI/CD integration
- ✅ Quality gates for skill acceptance
- ✅ Comprehensive reporting

Use this framework to maintain high skill quality and continuously improve the learning system.

---

*Last Updated: 2025-11-09*
