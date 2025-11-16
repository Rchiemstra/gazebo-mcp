# Mutation Testing

## Overview

Mutation testing is a powerful technique for validating test quality by introducing small code changes (mutations) and verifying that tests detect them. The test-orchestrator skill now includes comprehensive mutation testing support.

## What is Mutation Testing?

Mutation testing works by:
1. Creating small changes (mutations) in source code
2. Running the test suite against each mutated version
3. Checking if tests fail (mutation "killed") or pass (mutation "survived")

**Mutation Score** = (Killed Mutants / Total Mutants) × 100%

A high mutation score (>80%) indicates that tests effectively catch code changes and potential bugs.

## Features

### Mutation Operators

The mutation testing system includes six types of mutation operators:

#### 1. Comparison Operator Mutator
Changes comparison operators to test boundary conditions:
- `>` → `>=`, `<`, `==`
- `>=` → `>`, `<`
- `<` → `<=`, `>`, `==`
- `==` → `!=`, `<`, `>`
- `!=` → `==`

**Example:**
```python
# Original
if amount > 0:
    return True

# Mutated
if amount >= 0:  # Tests should catch this!
    return True
```

#### 2. Arithmetic Operator Mutator
Changes arithmetic operators:
- `+` → `-`, `*`
- `-` → `+`, `*`
- `*` → `/`, `+`
- `/` → `*`, `//`
- `%` → `*`, `//`

**Example:**
```python
# Original
fee = amount * 0.03

# Mutated
fee = amount / 0.03  # Tests should catch this!
```

#### 3. Boolean Operator Mutator
Changes boolean logic operators:
- `and` → `or`
- `or` → `and`

**Example:**
```python
# Original
if amount > 0 and gateway is not None:
    process()

# Mutated
if amount > 0 or gateway is not None:  # Tests should catch this!
    process()
```

#### 4. Constant Mutator
Changes constant values:
- Numbers: `0` → `1`, `-1`; `1` → `0`, `2`, `-1`
- Booleans: `True` → `False`; `False` → `True`
- Strings: `"text"` → `""`, `"textx"`, `"tex"`

**Example:**
```python
# Original
if amount == 0:
    raise ValueError()

# Mutated
if amount == 1:  # Tests should catch this!
    raise ValueError()
```

#### 5. Unary Operator Mutator
Changes unary operators:
- `-x` → `+x`
- `+x` → `-x`

**Example:**
```python
# Original
return -amount

# Mutated
return +amount  # Tests should catch this!
```

#### 6. Return Value Mutator
Changes return values:
- Any return → `return None`
- `return True` → `return False`
- `return False` → `return True`

**Example:**
```python
# Original
def validate():
    return True

# Mutated
def validate():
    return None  # Tests should catch this!
```

## Usage

### Basic Usage

```python
from core.mutation_tester import MutationGenerator, MutationRunner

# Generate mutations
generator = MutationGenerator()
with open('source_file.py', 'r') as f:
    source_code = f.read()

mutations = generator.generate_mutations(source_code)
print(f"Generated {len(mutations)} mutations")

# Run mutation tests
runner = MutationRunner()
result = runner.run_mutation_tests(
    source_file=Path('source_file.py'),
    test_file=Path('test_source_file.py'),
    mutations=mutations,
    max_mutations=50  # Limit for performance
)

print(f"Mutation Score: {result.mutation_score:.1f}%")
print(f"Killed: {result.killed_mutants}/{result.total_mutants}")
```

### Integration with Quality Scoring

Mutation score is automatically integrated with the quality scorer:

```python
from core.quality_scorer import TestQualityScorer

scorer = TestQualityScorer()
metrics = scorer.score_test_suite(
    test_code=test_content,
    num_tests=17,
    completeness_scores=completeness_scores,
    test_types=test_types,
    mutation_score=72.0  # Include mutation score
)

# Overall score now includes mutation testing (25% weight)
print(f"Overall Score: {metrics.overall_score:.1f}/100")
print(f"Mutation Score: {metrics.mutation_score:.1f}%")
```

### Demo Example

Run the enhanced demo to see mutation testing in action:

```bash
python demo_enhanced.py
```

The demo will:
1. Generate tests for sample code
2. Create mutations of the source code
3. Show estimated mutation score
4. Display updated quality metrics

## Interpreting Results

### Mutation Score Interpretation

| Score | Quality | Interpretation |
|-------|---------|----------------|
| 90-100% | Excellent | Tests catch almost all code changes |
| 80-89% | Good | Tests are effective but have minor gaps |
| 70-79% | Fair | Tests miss some important changes |
| 60-69% | Poor | Significant gaps in test coverage |
| <60% | Critical | Tests are inadequate |

### Analyzing Survived Mutations

When a mutation survives (tests don't fail), it indicates:
- Missing test case for that scenario
- Weak assertion that doesn't catch the change
- Redundant code that doesn't affect behavior

**Example:**
```python
# If this mutation survives:
# Original: if amount > 0
# Mutated:  if amount >= 0

# Action: Add test for amount=0 edge case
def test_validate_amount_zero():
    with pytest.raises(InvalidAmountError):
        validate_amount(0)  # This will kill the mutation!
```

## Performance Considerations

Mutation testing can be slow because it:
1. Creates N mutated versions (N = number of mutations)
2. Runs full test suite for each mutation
3. May execute hundreds of test runs

### Optimization Tips

1. **Limit mutations for development:**
```python
result = runner.run_mutation_tests(
    source_file, test_file, mutations,
    max_mutations=50  # Test first 50 only
)
```

2. **Target specific files:**
```python
# Only mutate critical files
mutations = generator.generate_mutations(critical_module_code)
```

3. **Use faster tests:**
- Unit tests run faster than integration tests
- Mock external dependencies to avoid I/O

4. **Parallel execution:**
```python
# Future enhancement - run mutations in parallel
# This can speed up testing significantly
```

## Quality Score Impact

When mutation score is included, the overall quality score calculation changes:

**Without mutation testing:**
- Completeness: 35%
- Coverage: 25%
- Assertions: 25%
- Variety: 15%

**With mutation testing:**
- Completeness: 25%
- Coverage: 20%
- Assertions: 20%
- Variety: 10%
- **Mutation Score: 25%** ← New!

This gives mutation testing significant weight because it's the most reliable indicator of test effectiveness.

## Best Practices

### 1. Start with Small Codebases
Begin with individual modules before testing entire systems.

### 2. Fix Survived Mutations
Review survived mutations to identify gaps:
```python
# Get mutations that survived
survived = mutation_result.get_survived_mutations()
for mut in survived:
    print(f"Line {mut.line_number}: {mut.description}")
    # Add test to kill this mutation
```

### 3. Combine with Coverage
Use both code coverage and mutation score:
- **Code coverage** = Are all lines executed?
- **Mutation score** = Are all lines properly tested?

You can have 100% code coverage but low mutation score if assertions are weak.

### 4. Set Quality Gates
Require minimum mutation score for production code:
```python
if mutation_result.mutation_score < 70:
    print("⚠️  Mutation score too low - strengthen tests")
    sys.exit(1)
```

### 5. Regular Testing
Run mutation tests:
- Before major releases
- For critical code paths
- After test improvements

## Tools Integration

### Using mutmut (External Tool)

For production mutation testing, consider using `mutmut`:

```bash
# Install
pip install mutmut

# Run mutation testing
mutmut run --paths-to-mutate=src/

# View results
mutmut show

# Apply survived mutation to see what tests missed
mutmut apply 42
```

### Integration with CI/CD

Add mutation testing to your pipeline:

```yaml
# .github/workflows/tests.yml
- name: Run mutation tests
  run: |
    python -m pytest
    mutmut run --paths-to-mutate=src/critical/
    mutmut junitxml > mutation-results.xml
```

## Limitations

1. **Not all mutations are meaningful**
   - Some mutations may be equivalent to original code
   - Framework-specific code may be hard to mutate

2. **Performance overhead**
   - Can take 10-100x longer than regular tests
   - Not practical for every test run

3. **False positives**
   - Some survived mutations may be acceptable
   - Requires manual review

## Examples

### Example 1: High Mutation Score

```python
# Source code
def is_positive(n):
    if n > 0:
        return True
    return False

# Good tests (will kill mutations)
def test_is_positive_with_positive():
    assert is_positive(1) == True

def test_is_positive_with_zero():
    assert is_positive(0) == False  # Kills ">= mutation"

def test_is_positive_with_negative():
    assert is_positive(-1) == False

# Result: 100% mutation score
```

### Example 2: Low Mutation Score

```python
# Source code
def calculate_discount(price, rate):
    return price * rate

# Weak test (won't kill many mutations)
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result is not None  # Too generic!

# Better test (kills mutations)
def test_calculate_discount():
    assert calculate_discount(100, 0.1) == 10.0  # Specific!
    assert calculate_discount(0, 0.5) == 0.0     # Edge case!
```

## Advanced Topics

### Custom Mutation Operators

Extend the system with custom operators:

```python
class CustomMutator(MutationOperator):
    def mutate(self, node: ast.AST) -> List[ast.AST]:
        # Your custom mutation logic
        mutations = []
        # ... generate mutations
        return mutations

# Add to generator
generator = MutationGenerator()
generator.operators.append(CustomMutator())
```

### Mutation Testing Metrics

Track mutation testing trends:
```python
metrics = {
    'timestamp': datetime.now(),
    'mutation_score': result.mutation_score,
    'total_mutants': result.total_mutants,
    'killed': result.killed_mutants,
    'survived': result.survived_mutants
}

# Store in database or file for trending
```

## Summary

Mutation testing is the gold standard for validating test quality. The test-orchestrator skill now provides:

✅ **6 mutation operators** covering common code patterns
✅ **Automatic mutation generation** from source code
✅ **Integrated quality scoring** with 25% weight
✅ **Performance optimization** with configurable limits
✅ **Actionable insights** from survived mutations

Use mutation testing to ensure your generated tests truly protect against bugs!

## References

- [Mutation Testing Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing)
- [mutmut Documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing Best Practices](https://pitest.org/quickstart/mutators/)
