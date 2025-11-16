---
name: llm-judge
description: Evaluates teaching quality and student understanding for learning-first workflows
version: 1.0.0
category: quality
tags:
  - teaching
  - evaluation
  - learning-assessment
  - quality-assurance
activation: manual
tools:
  - Read
dependencies: []
---

# LLM-as-Judge Skill

## When to Use This Skill

Use the llm-judge skill when you need to:
- **Evaluate teaching quality** in agent responses
- **Check if responses give guidance vs complete solutions**
- **Assess student understanding** through code analysis
- **Identify knowledge gaps** in student work
- **Ensure teaching-first approach** in agent interactions
- **Provide automated feedback** on learning progress

## Quick Start

```python
from skills.llm_judge import evaluate_teaching, check_understanding

# Evaluate an agent's response
result = evaluate_teaching(agent_response)
if result.success:
    print(f"Teaching-focused: {result.data['is_teaching_focused']}")
    print(f"Quality score: {result.data['quality_score']:.1%}")

# Check student understanding
result = check_understanding(
    student_code,
    expected_concepts=["functions", "loops", "error_handling"]
)
print(f"Understanding: {result.data['demonstrates_understanding']}")
print(f"Confidence: {result.data['confidence_level']:.1%}")
```

## Operations

**Teaching Evaluation:**
- `evaluate_teaching` - Evaluate agent responses for teaching quality

**Understanding Assessment:**
- `check_understanding` - Assess student understanding through code analysis

## Token Efficiency

All operations support `response_format` parameter:
- **"summary"**: Overview only (75-90% token savings)
- **"detailed"**: Full analysis with all issues and suggestions

## Documentation

- See [reference.md](./reference.md) for complete API documentation
- See [examples.md](./examples.md) for usage examples

## Example Use Cases

1. **Teaching Quality Assurance**
   - Agent responds to student question
   - Evaluate response for teaching quality
   - Ensure guidance-focused, not solution-giving

2. **Learning Progress Assessment**
   - Student submits code
   - Check understanding of expected concepts
   - Identify knowledge gaps and next steps

3. **Adaptive Learning**
   - Track student understanding over time
   - Adjust teaching approach based on gaps
   - Recommend personalized learning paths

## Related Skills

- **verification** - Validate code, output, and tests
- **test_orchestrator** - Generate and run tests
- **learning_plan_manager** - Manage learning plans
- **learning_analytics** - Track learning progress
