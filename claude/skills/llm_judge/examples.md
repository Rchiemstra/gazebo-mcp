# LLM-as-Judge Skill Examples

Practical usage examples for the llm-judge skill.

---

## Example 1: Evaluate Agent Response Quality

```python
from skills.llm_judge import evaluate_teaching

# Student asks: "How do I implement binary search?"

# Good teaching response (guidance)
good_response = """
Let's break down binary search step by step:

1. Core Idea: Cut the search space in half each time
2. Key Requirements:
   - Array must be sorted
   - Compare middle element with target
   - Narrow search range based on comparison

Questions to consider:
- What data structure represents the search range?
- How do you calculate the middle index?
- What's the base case for your recursion/loop?

Try implementing the core loop first. Start with:
```python
left, right = 0, len(arr) - 1
while left <= right:
    # Your code here
```

What would you check next?
"""

# Evaluate it
result = evaluate_teaching(good_response)

if result.success:
    print(f"Teaching-focused: {result.data['is_teaching_focused']}")  # True
    print(f"Quality score: {result.data['quality_score']:.1%}")  # ~80-90%
    print(f"Strengths: {result.data.get('top_strengths', [])}")
    # ["Uses 4 teaching patterns", "Asks 2 guiding questions", "Uses small examples"]
```

---

## Example 2: Detect Solution-Giving Anti-Pattern

```python
from skills.llm_judge import evaluate_teaching

# Bad teaching response (complete solution)
bad_response = """
Here's the complete binary search implementation:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

Copy and paste this code into your project.
"""

# Evaluate it
result = evaluate_teaching(bad_response, response_format="detailed")

if result.success:
    print(f"Teaching-focused: {result.data['is_teaching_focused']}")  # False
    print(f"Quality score: {result.data['quality_score']:.1%}")  # ~20-30%

    print("\\nIssues found:")
    for issue in result.data['issues']:
        print(f"  {issue['severity'].upper()}: {issue['message']}")
        print(f"    Suggestion: {issue['suggestion']}")

    # Output:
    # ERROR: Response contains 1 complete solution(s)
    #   Suggestion: Provide guidance and small examples instead of complete implementations
    # WARNING: Contains 1 large code block(s) (>200 chars)
    #   Suggestion: Use small, focused examples (2-5 lines) instead of large code blocks
```

---

## Example 3: Check Student Understanding (Beginner)

```python
from skills.llm_judge import check_understanding

# Beginner student's code
student_code = '''
def calculate_total(prices):
    total = 0
    for price in prices:
        total = total + price
    return total

items = [10, 20, 30]
print(calculate_total(items))
'''

# Check understanding
result = check_understanding(
    student_code,
    expected_concepts=["functions", "loops", "variables"],
    learning_context={"level": "beginner"}
)

if result.success:
    print(f"Understands: {result.data['demonstrates_understanding']}")  # True
    print(f"Confidence: {result.data['confidence_level']:.1%}")  # ~70%
    print(f"Demonstrated: {result.data.get('top_demonstrated', [])}")
    # ["functions", "loops", "conditionals"]

    if result.data['next_steps']:
        print("\\nNext learning steps:")
        for step in result.data['next_steps']:
            print(f"  - {step}")
    # - Continue practicing current concepts to build fluency
```

---

## Example 4: Identify Knowledge Gaps

```python
from skills.llm_judge import check_understanding

# Student code with issues
student_code = '''
prices = [10, 20, 30]
total = 0
for p in prices:
    total = total + p
print(total)
'''

# Expected to use functions
result = check_understanding(
    student_code,
    expected_concepts=["functions", "loops"],
    learning_context={"level": "beginner"},
    response_format="detailed"
)

if result.success:
    print(f"Confidence: {result.data['confidence_level']:.1%}")  # ~40-50%

    print("\\nKnowledge gaps:")
    for gap in result.data['knowledge_gaps']:
        if gap['severity'] in ['critical', 'moderate']:
            print(f"  {gap['severity'].upper()} - {gap['concept']}")
            print(f"    Evidence: {gap['evidence']}")
            print(f"    Suggestion: {gap['suggestion']}")

    # Output:
    # CRITICAL - functions
    #   Evidence: Expected to see 'functions' but not found in code
    #   Suggestion: Break your code into reusable functions
```

---

## Example 5: Assess Intermediate Student

```python
from skills.llm_judge import check_understanding

# Intermediate student implementing a class
student_code = '''
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False
'''

# Check intermediate concepts
result = check_understanding(
    student_code,
    expected_concepts=["classes", "conditionals", "error_handling"],
    learning_context={"level": "intermediate"}
)

if result.success:
    print(f"Understanding: {result.data['demonstrates_understanding']}")
    print(f"Confidence: {result.data['confidence_level']:.1%}")  # ~60-70%

    # Show what's missing
    if 'critical_gaps' in result.data:
        print("\\nMissing:")
        for gap in result.data['critical_gaps']:
            print(f"  - {gap}")
    # - error_handling: Expected to see 'error_handling' but not found

    print("\\nRecommendations:")
    for step in result.data.get('next_steps', []):
        print(f"  - {step}")
    # - Review: error_handling
    # - Add try/except blocks to handle potential errors
```

---

## Example 6: Detect Security Issues

```python
from skills.llm_judge import check_understanding

# Student code with security issue
student_code = '''
def calculate(expression):
    result = eval(expression)
    return result

user_input = input("Enter calculation: ")
print(calculate(user_input))
'''

# Check understanding
result = check_understanding(
    student_code,
    expected_concepts=["functions"],
    response_format="detailed"
)

if result.success:
    # Find security gaps
    security_gaps = [
        gap for gap in result.data['knowledge_gaps']
        if gap['concept'] == 'security'
    ]

    if security_gaps:
        print("⚠️  Security issues detected:")
        for gap in security_gaps:
            print(f"  {gap['evidence']}")
            print(f"  Fix: {gap['suggestion']}")

    # Output:
    # ⚠️  Security issues detected:
    #   Using eval() function
    #   Fix: Avoid eval() - it's a security risk. Use safer alternatives...
```

---

## Example 7: Automated Teaching Workflow

```python
from skills.llm_judge import evaluate_teaching, check_understanding

def teaching_loop(student_question, agent_response, student_code):
    """Complete teaching quality assurance workflow."""

    print("🔍 Evaluating teaching quality...")

    # 1. Evaluate agent's response
    teaching_eval = evaluate_teaching(
        agent_response,
        student_question=student_question
    )

    if not teaching_eval.data['is_teaching_focused']:
        print("⚠️  Agent response is not teaching-focused")
        print(f"Quality score: {teaching_eval.data['quality_score']:.1%}")

        # Get detailed issues
        detailed = evaluate_teaching(agent_response, response_format="detailed")
        print("\\nImprovements needed:")
        for improvement in detailed.data.get('improvements', []):
            print(f"  - {improvement}")

        return False

    print(f"✅ Teaching quality: {teaching_eval.data['quality_score']:.1%}")

    # 2. Check student's understanding
    understanding = check_understanding(student_code)

    print(f"\\n📊 Student confidence: {understanding.data['confidence_level']:.1%}")

    if not understanding.data['demonstrates_understanding']:
        print("\\nNext steps for student:")
        for step in understanding.data.get('next_steps', []):
            print(f"  - {step}")
    else:
        print("✅ Student demonstrates understanding!")

    return True

# Use it
success = teaching_loop(
    student_question="How do I handle errors?",
    agent_response="Let's explore error handling...",
    student_code="def process():\\n    try:\\n        pass\\n    except ValueError:\\n        pass"
)
```

---

## Example 8: Track Teaching Quality Over Time

```python
from skills.llm_judge import evaluate_teaching

def track_teaching_quality(agent_responses):
    """Track teaching quality across multiple responses."""

    results = []

    for i, response in enumerate(agent_responses):
        result = evaluate_teaching(response)

        if result.success:
            results.append({
                "response_num": i + 1,
                "is_teaching": result.data['is_teaching_focused'],
                "score": result.data['quality_score'],
                "issue_count": result.data['issue_count']
            })

    # Calculate statistics
    avg_score = sum(r['score'] for r in results) / len(results)
    teaching_rate = sum(r['is_teaching'] for r in results) / len(results)

    print(f"Average teaching quality: {avg_score:.1%}")
    print(f"Teaching-focused rate: {teaching_rate:.1%}")

    # Find responses that need improvement
    low_quality = [r for r in results if r['score'] < 0.6]
    if low_quality:
        print(f"\\n{len(low_quality)} responses need improvement:")
        for r in low_quality:
            print(f"  Response #{r['response_num']}: {r['score']:.1%}")

# Example usage
responses = [
    "Let's explore this concept...",  # Good
    "Here's the complete code...",    # Bad - solution
    "What do you think would happen if...?",  # Good
    "Use this implementation:",       # Bad - solution
]

track_teaching_quality(responses)
```

---

## Example 9: Progressive Learning Assessment

```python
from skills.llm_judge import check_understanding

def assess_progression(code_submissions, concepts_by_level):
    """Assess student progression through multiple submissions."""

    progression = []

    for i, (code, expected) in enumerate(zip(code_submissions, concepts_by_level)):
        result = check_understanding(
            code,
            expected_concepts=expected,
            learning_context={"previous_attempts": i}
        )

        if result.success:
            progression.append({
                "attempt": i + 1,
                "confidence": result.data['confidence_level'],
                "gap_count": result.data['knowledge_gap_count'],
                "concepts_shown": result.data['concepts_demonstrated']
            })

    # Analyze progression
    if len(progression) >= 2:
        confidence_delta = progression[-1]['confidence'] - progression[0]['confidence']
        gap_delta = progression[0]['gap_count'] - progression[-1]['gap_count']

        print(f"Confidence improvement: {confidence_delta:+.1%}")
        print(f"Gaps reduced: {gap_delta}")

        if confidence_delta > 0.2:
            print("✅ Strong learning progress!")
        elif confidence_delta < 0:
            print("⚠️  Student may be struggling - provide support")

# Example: Track beginner → intermediate progression
submissions = [
    "x = 5\\nprint(x)",  # Basic
    "def add(a, b):\\n    return a + b",  # Functions
    "class Calculator:\\n    def add(self, a, b):\\n        return a + b",  # Classes
]

concepts = [
    ["variables"],
    ["functions", "variables"],
    ["classes", "functions"]
]

assess_progression(submissions, concepts)
```

---

## Integration with Other Skills

### With Verification Skill

```python
from skills.verification import validate_code
from skills.llm_judge import check_understanding

def complete_assessment(student_code, expected_concepts):
    """Combine code validation and understanding check."""

    # 1. Validate code quality
    validation = validate_code(student_code)

    # 2. Check understanding
    understanding = check_understanding(
        student_code,
        expected_concepts=expected_concepts
    )

    # 3. Provide combined feedback
    report = {
        "code_valid": validation.data['is_valid'],
        "demonstrates_understanding": understanding.data['demonstrates_understanding'],
        "overall_ready": (
            validation.data['is_valid'] and
            understanding.data['demonstrates_understanding']
        )
    }

    if not report['overall_ready']:
        print("Areas to improve:")

        # Code quality issues
        if not validation.data['is_valid']:
            print("\\n  Code Quality:")
            for issue in validation.data.get('top_issues', []):
                print(f"    - {issue}")

        # Knowledge gaps
        if not understanding.data['demonstrates_understanding']:
            print("\\n  Understanding:")
            for gap in understanding.data.get('critical_gaps', []):
                print(f"    - {gap}")

    return report

# Use it
report = complete_assessment(
    student_code,
    expected_concepts=["functions", "error_handling"]
)
```

---

## Common Patterns

### Pattern: Evaluate Then Guide

```python
result = evaluate_teaching(agent_response)
if result.success:
    if not result.data['is_teaching_focused']:
        # Get detailed feedback
        detailed = evaluate_teaching(agent_response, response_format="detailed")
        improve_response_based_on(detailed.data['improvements'])
```

### Pattern: Check Understanding Then Recommend

```python
result = check_understanding(student_code, expected_concepts)
if result.success:
    if not result.data['demonstrates_understanding']:
        # Get learning recommendations
        detailed = check_understanding(student_code, expected_concepts, response_format="detailed")
        provide_targeted_help(detailed.data['recommended_review'])
```

### Pattern: Adaptive Teaching

```python
# Adjust teaching based on understanding
understanding = check_understanding(student_code)
if understanding.data['confidence_level'] < 0.5:
    # Use more guidance, simpler examples
    criteria = {"require_questions": True, "require_examples": True}
else:
    # Can use more advanced patterns
    criteria = {"require_questions": False, "require_examples": False}

evaluate_teaching(response, teaching_criteria=criteria)
```

---

## Tips

1. **Start with summary format** - Get overview before details
2. **Set appropriate expectations** - Beginner vs advanced students
3. **Use context** - Provide learning level and known struggles
4. **Combine skills** - Use with verification and analytics
5. **Track over time** - Monitor teaching quality and student progress
