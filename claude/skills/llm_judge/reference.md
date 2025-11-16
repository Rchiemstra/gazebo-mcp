# LLM-as-Judge Skill Reference

Complete API documentation for the llm-judge skill.

---

## evaluate_teaching

Evaluates agent responses for teaching quality.

### Signature

```python
def evaluate_teaching(
    agent_response: str,
    student_question: Optional[str] = None,
    teaching_criteria: Optional[Dict[str, bool]] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

### Parameters

- **agent_response** (`str`, required): The agent's response to evaluate
- **student_question** (`str`, optional): Student question for context
- **teaching_criteria** (`dict`, optional): Criteria to check
  - `require_questions` (bool, default=True): Must ask guiding questions
  - `forbid_solutions` (bool, default=True): Must not give complete solutions
  - `require_examples` (bool, default=False): Must include small examples
  - `require_explanations` (bool, default=True): Must explain concepts
- **response_format** (`str`, default="summary"):
  - `"summary"`: Overview with score and top issues
  - `"detailed"`: All issues, strengths, improvements, and metrics

### Returns

`OperationResult` with:

**Summary Format:**
```python
{
    "is_teaching_focused": bool,
    "quality_score": float,  # 0.0 to 1.0
    "issue_count": int,
    "strength_count": int,
    "top_issues": [str, ...],  # Top 3 issues
    "top_strengths": [str, ...],  # Top 3 strengths
    "top_improvements": [str, ...],  # Top 3 suggestions
    "efficiency_tip": str
}
```

**Detailed Format:**
```python
{
    "is_teaching_focused": bool,
    "quality_score": float,
    "issue_count": int,
    "strength_count": int,
    "issues": [
        {
            "severity": "error" | "warning" | "info",
            "category": "solution_given" | "no_guidance" | "unclear" | "missing_questions",
            "message": str,
            "suggestion": str | None
        },
        ...
    ],
    "strengths": [str, ...],
    "improvements": [str, ...],
    "metrics": {
        "response_length": int,
        "code_block_count": int,
        "question_count": int,
        "teaching_pattern_count": int,
        "solution_pattern_count": int,
        "explanation_count": int
    }
}
```

### Evaluation Criteria

**Anti-Patterns (detected):**
- Complete function/class definitions (>20 lines)
- Large code blocks (>200 chars)
- "Here's the complete code" language
- "Copy and paste this" instructions
- No guiding questions
- No explanations

**Teaching Patterns (encouraged):**
- Asking questions
- "Can you", "Could you", "Try to" prompts
- Step-by-step guidance
- Small examples (2-5 lines)
- Explanations of concepts
- "Let's break this down" approach

### Quality Score Calculation

Score starts at 0.5 (neutral):

**Positive factors:**
- Has questions: +0.15
- Multiple teaching patterns: +0.15
- Has explanations: +0.10
- Has examples (not solutions): +0.10

**Negative factors:**
- Error severity issue: -0.25 each
- Warning severity issue: -0.10 each

---

## check_understanding

Assesses student understanding through code analysis.

### Signature

```python
def check_understanding(
    student_code: str,
    expected_concepts: Optional[List[str]] = None,
    learning_context: Optional[Dict[str, Any]] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult
```

### Parameters

- **student_code** (`str`, required): Student's code to analyze
- **expected_concepts** (`list`, optional): Concepts student should demonstrate
  - Beginner: `"functions"`, `"loops"`, `"conditionals"`, `"variables"`
  - Intermediate: `"classes"`, `"error_handling"`, `"docstrings"`, `"typing"`
  - Advanced: `"list_comprehension"`, `"generators"`, `"decorators"`
- **learning_context** (`dict`, optional): Context about student
  - `level`: `"beginner"`, `"intermediate"`, `"advanced"`
  - `previous_attempts`: int
  - `known_struggles`: List[str]
- **response_format** (`str`, default="summary"):
  - `"summary"`: Understanding status and confidence
  - `"detailed"`: All knowledge gaps and learning recommendations

### Returns

`OperationResult` with:

**Summary Format:**
```python
{
    "demonstrates_understanding": bool,
    "confidence_level": float,  # 0.0 to 1.0
    "knowledge_gap_count": int,
    "concepts_demonstrated": int,
    "critical_gaps": [str, ...],  # Critical issues only
    "top_demonstrated": [str, ...],  # Top 5 concepts
    "next_steps": [str, ...],  # Top 2 next steps
    "efficiency_tip": str
}
```

**Detailed Format:**
```python
{
    "demonstrates_understanding": bool,
    "confidence_level": float,
    "knowledge_gap_count": int,
    "concepts_demonstrated": int,
    "knowledge_gaps": [
        {
            "concept": str,
            "severity": "critical" | "moderate" | "minor",
            "evidence": str,
            "suggestion": str
        },
        ...
    ],
    "demonstrated_concepts": [str, ...],
    "recommended_review": [str, ...],
    "next_learning_steps": [str, ...],
    "metrics": {
        "total_lines": int,
        "functions_defined": int,
        "classes_defined": int,
        "has_docstrings": bool,
        "has_type_hints": bool,
        "has_error_handling": bool,
        "complexity_indicators": [str, ...]
    }
}
```

### Understanding Checks

**Concept Detection:**
- Functions: AST analysis for FunctionDef nodes
- Classes: ClassDef nodes
- Loops: For/While nodes
- Conditionals: If nodes
- Error handling: Try/Except blocks
- Type hints: Function annotations
- Docstrings: Function/class docstrings
- List comprehensions: ListComp nodes
- Generators: GeneratorExp nodes

**Anti-Pattern Detection:**
- `eval()` / `exec()` usage (security)
- Bare except clauses (error handling)
- Global variables (code organization)
- Magic numbers (readability)

**Severity Levels:**
- **Critical**: Syntax errors, security issues, missing expected concepts (beginner level)
- **Moderate**: Anti-patterns, missing expected concepts (intermediate/advanced)
- **Minor**: Code readability issues

### Confidence Calculation

Score starts at 0.5 (neutral):

**Positive factors:**
- Functions defined: +0.10
- Classes defined: +0.10
- Has docstrings: +0.10
- Has type hints: +0.10
- Has error handling: +0.10
- Coverage of expected concepts: +0.30

**Negative factors:**
- Critical gap: -0.25 each
- Moderate gap: -0.10 each
- Minor gap: -0.05 each

---

## Error Codes

All operations return agent-friendly errors with these codes:

- `EVALUATION_ERROR`: Teaching evaluation failure
- `CHECK_ERROR`: Understanding check failure

Each error includes:
- Clear error message
- 3-4 actionable suggestions
- Example fix showing correct usage

---

## Token Efficiency Guide

### Summary Format (Recommended for Most Cases)

```python
# Use summary for quick evaluation
result = evaluate_teaching(response)  # ~300-600 tokens
```

**When to use:**
- Just need to know if teaching-focused
- Quality score is sufficient
- Large responses to evaluate

**Token savings:** 75-90%

### Detailed Format (Use When Needed)

```python
# Use detailed when you need specifics
result = evaluate_teaching(response, response_format="detailed")  # ~1500-3000 tokens
```

**When to use:**
- Need all issues and suggestions
- Providing detailed feedback
- Analyzing specific teaching patterns
- Building reports

---

## Best Practices

1. **Start with summary format**
   - Get overview first
   - Request details only if needed

2. **Set appropriate criteria**
   - Beginner students: Focus on basic concepts
   - Advanced students: Expect more sophisticated patterns

3. **Use context**
   - Provide learning_context for better assessment
   - Track previous attempts
   - Note known struggles

4. **Handle syntax errors gracefully**
   - Syntax errors in student code are normal
   - They're reported as critical gaps with suggestions

5. **Combine with other skills**
   - Use with verification skill for complete assessment
   - Integrate with learning_analytics for tracking
   - Combine with test_orchestrator for testing

---

## Integration Patterns

### With Verification Skill

```python
from skills.verification import validate_code
from skills.llm_judge import check_understanding

# 1. Validate code quality
code_result = validate_code(student_code)

# 2. Check understanding
understanding = check_understanding(
    student_code,
    expected_concepts=["functions", "error_handling"]
)

# 3. Provide combined feedback
if code_result.success and understanding.data["demonstrates_understanding"]:
    print("✅ Code is valid and demonstrates understanding")
else:
    # Provide targeted guidance
    pass
```

### With Learning Analytics

```python
from skills.learning_analytics import track_progress
from skills.llm_judge import check_understanding

# Check understanding over time
results = []
for submission in student_submissions:
    result = check_understanding(submission, expected_concepts=concepts)
    results.append({
        "timestamp": submission.timestamp,
        "confidence": result.data["confidence_level"],
        "gaps": result.data["knowledge_gap_count"]
    })

# Track improvement
track_progress(results)
```

---

## Version

**Current Version:** 1.0.0

**Dependencies:** None (uses Python stdlib only)

**Required Tools:** Read (for loading files)
