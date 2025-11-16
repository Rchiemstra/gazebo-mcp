# Workflow Guide

Best practices for common development workflows using Claude Code.

---

## 📋 Overview

This guide covers recommended workflows for:
- Learning and skill development
- Feature implementation
- Code review and refactoring
- Testing and debugging
- Documentation

Each workflow includes security considerations and efficiency patterns.

---

## 🎓 Learning Workflow

### Pattern: Guided Learning Journey

**Use When:** Learning new concepts or technologies

**Steps:**

1. **Start Learning Plan**
   ```bash
   /start-learning "autonomous navigation"
   ```

2. **Review Plan Overview**
   - Check phases and prerequisites
   - Understand specialist involvement
   - Note checkpoints and milestones

3. **Execute Phase by Phase**
   ```bash
   /continue-plan  # Start current phase
   ```

   **During Each Phase:**
   - Read suggested resources
   - Experiment with concepts
   - Ask specialists for guidance
   ```bash
   /ask-specialist How do ROS2 transforms work?
   ```

4. **Verify Understanding**
   ```bash
   /check-understanding "transform trees"
   ```

5. **Track Progress**
   ```bash
   /update-plan
   # Journal: What worked? What was challenging?
   ```

6. **Repeat** until plan complete

**Token Efficiency:**
- Plans are ~5,000-15,000 tokens (loaded once)
- Phase guidance ~500-1,000 tokens each
- Specialist help ~300-500 tokens per interaction

**Security:**
- Learning mode: Read-only tools recommended
- Progress to Write/Edit as skills develop
- Code examples reviewed before execution

---

## 💻 Feature Implementation Workflow

### Pattern: Explore → Plan → Code → Commit

**Use When:** Implementing new features

**Steps:**

1. **Explore Existing Code**
   ```python
   # Use Task agent for exploration
   "Explore the authentication system - how does it work?"
   ```

   **Efficient Pattern:**
   - Let agent use Glob/Grep
   - Gets context without loading all files
   - Returns summary (~500 tokens)

2. **Create Implementation Plan**
   ```bash
   /create-project-plan
   ```

   **Plan Structure:**
   - Phase 1: Research and design
   - Phase 2: Core implementation
   - Phase 3: Testing
   - Phase 4: Documentation
   - Phase 5: Integration

3. **Start Feature Branch**
   ```bash
   /git-start-feature "add-2fa"
   ```

4. **Implement Phase 1**
   - Research existing patterns
   - Design your approach
   - Create scaffolding
   - Review with specialist
   ```bash
   /ask-specialist "Is this authentication design secure?"
   ```

5. **Commit Phase Progress**
   ```bash
   /git-stage-commit
   # Automatic message generation
   ```

6. **Implement Remaining Phases**
   - Phase 2: Core logic
   - Phase 3: Tests
   - Phase 4: Docs
   - Phase 5: Integration

   **Commit after each phase:**
   ```bash
   /git-stage-commit
   ```

7. **Create Pull Request**
   ```bash
   /create-pr
   ```

**Token Efficiency:**
- Exploration: ~500-1,000 tokens (summary)
- Plan creation: ~5,000 tokens (loaded once)
- Phase guidance: ~500 tokens each
- **Total: ~7,000 tokens** (vs 50,000+ without workflow)

**Security:**
- Review plan before coding
- Incremental commits (reversible)
- Specialist review at checkpoints
- PR review before merge

---

## 🔍 Code Review Workflow

### Pattern: Analyze → Review → Refactor → Test

**Use When:** Reviewing or improving existing code

**Steps:**

1. **Analyze Code Quality**
   ```python
   from skills.code_analysis.operations import analyze_file

   result = analyze_file(
       "payment.py",
       response_format="summary"  # Get overview first
   )

   print(f"Complexity: {result.data['avg_complexity']}")
   print(f"Issues: {result.data['issue_count']}")
   ```

2. **Deep Dive on Issues**
   ```python
   # Get details for specific file
   detailed = analyze_file(
       "payment.py",
       response_format="detailed"
   )

   # Review specific issues
   for issue in detailed.data['issues']:
       print(f"{issue['type']}: {issue['message']}")
   ```

3. **Get Refactoring Suggestions**
   ```python
   from skills.refactor_assistant.operations import suggest_refactorings

   suggestions = suggest_refactorings(
       "payment.py",
       max_suggestions=5
   )

   for suggestion in suggestions.data['suggestions']:
       print(f"- {suggestion['description']}")
   ```

4. **Apply Refactorings**
   ```python
   from skills.refactor_assistant.operations import apply_refactoring

   # Apply one refactoring at a time
   result = apply_refactoring(
       file_path="payment.py",
       refactoring_type="extract_method",
       location={"start_line": 45, "end_line": 67},
       parameters={"new_method_name": "validate_payment"},
       run_tests=True  # Verify after refactoring
   )
   ```

5. **Verify with Tests**
   ```python
   from skills.test_orchestrator.operations import run_tests

   test_results = run_tests(
       "tests/test_payment.py",
       response_format="summary"
   )

   assert test_results.data['all_passed']
   ```

6. **Commit Improvements**
   ```bash
   git add payment.py
   git commit -m "refactor: extract payment validation logic

   - Extracted validate_payment method
   - Reduced complexity from 15 to 8
   - All tests passing

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

**Token Efficiency:**
- Analysis summary: ~500 tokens
- Detailed analysis: ~2,000 tokens (only when needed)
- Refactoring suggestions: ~1,000 tokens
- **Savings: ~95%** vs analyzing everything

**Security:**
- Automated tests verify refactorings
- Incremental commits (easy rollback)
- Code review before merge

---

## 🧪 Test-Driven Development Workflow

### Pattern: Test → Code → Refactor

**Use When:** Implementing new features with TDD

**Steps:**

1. **Write Failing Test**
   ```python
   def test_process_payment_validates_amount():
       """Test that payment validation works."""
       payment = Payment(amount=-100)

       result = process_payment(payment)

       assert not result.success
       assert "invalid amount" in result.error.lower()
   ```

2. **Run Tests (Should Fail)**
   ```bash
   pytest tests/test_payment.py::test_process_payment_validates_amount -v
   ```

3. **Implement Minimum Code**
   ```python
   def process_payment(payment):
       """Process a payment."""
       if payment.amount <= 0:
           return Result(
               success=False,
               error="Invalid amount"
           )

       # Actual payment processing...
       return Result(success=True)
   ```

4. **Run Tests (Should Pass)**
   ```bash
   pytest tests/test_payment.py -v
   ```

5. **Refactor**
   ```python
   # Extract validation
   def validate_payment_amount(amount):
       """Validate payment amount."""
       if amount <= 0:
           raise ValueError("Invalid amount")

   def process_payment(payment):
       """Process a payment."""
       try:
           validate_payment_amount(payment.amount)
       except ValueError as e:
           return Result(success=False, error=str(e))

       # Process payment...
       return Result(success=True)
   ```

6. **Run Tests Again**
   ```bash
   pytest tests/test_payment.py -v
   ```

7. **Commit Red-Green-Refactor Cycle**
   ```bash
   git add tests/test_payment.py payment.py
   git commit -m "feat: add payment amount validation

   - Added validation for negative amounts
   - Extracted validate_payment_amount
   - All tests passing

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

**Token Efficiency:**
- Using test_orchestrator for generation: ~1,000 tokens
- Manual TDD: Minimal tokens (direct coding)

**Security:**
- Tests verify security requirements
- Validation logic tested first
- Regression prevention

---

## 🐛 Debugging Workflow

### Pattern: Reproduce → Isolate → Fix → Verify

**Use When:** Investigating and fixing bugs

**Steps:**

1. **Reproduce the Bug**
   ```python
   # Create minimal reproduction
   def test_reproduces_bug():
       """Reproduce the authentication bug."""
       user = User(email="test@example.com")
       token = generate_token(user)

       # Bug: Token expires immediately
       is_valid = validate_token(token)

       # This should pass but fails
       assert is_valid
   ```

2. **Add Debugging Output**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)

   def generate_token(user):
       """Generate auth token."""
       expiry = datetime.now() + timedelta(hours=24)
       logging.debug(f"Token expiry: {expiry}")

       token = create_jwt(user.id, expiry)
       logging.debug(f"Created token: {token[:20]}...")

       return token
   ```

3. **Isolate the Problem**
   ```bash
   # Run with debugging
   pytest tests/test_auth.py::test_reproduces_bug -v -s

   # Output shows issue:
   # Token expiry: 2024-11-08 10:00:00
   # Validation time: 2024-11-09 10:00:00
   # Bug: Clock skew issue!
   ```

4. **Fix the Issue**
   ```python
   def validate_token(token):
       """Validate auth token."""
       try:
           payload = decode_jwt(token)

           # Fix: Add grace period for clock skew
           grace_period = timedelta(minutes=5)
           expiry = datetime.fromisoformat(payload['exp'])

           if datetime.now() > expiry + grace_period:
               return False

           return True
       except Exception:
           return False
   ```

5. **Verify Fix**
   ```bash
   # Original test should pass
   pytest tests/test_auth.py::test_reproduces_bug -v

   # Run full suite
   pytest tests/test_auth.py -v
   ```

6. **Add Regression Test**
   ```python
   @pytest.mark.regression
   def test_token_validation_handles_clock_skew():
       """Test token validation with clock skew (bug #123)."""
       user = User(email="test@example.com")

       # Create token
       token = generate_token(user)

       # Simulate small clock skew (< 5 min)
       with freeze_time("2024-11-08 10:04:00"):
           assert validate_token(token)

       # Simulate large clock skew (> 5 min)
       with freeze_time("2024-11-08 10:10:00"):
           assert not validate_token(token)
   ```

7. **Commit Fix**
   ```bash
   git add auth.py tests/test_auth.py
   git commit -m "fix: handle clock skew in token validation

   Fixes #123

   - Added 5-minute grace period for clock skew
   - Updated token validation logic
   - Added regression test

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

**Token Efficiency:**
- Debugging with specialists: ~500-1,000 tokens
- Code analysis for bug hunting: ~1,000 tokens

**Security:**
- Regression tests prevent reintroduction
- Security bugs get CVE references
- Document security implications

---

## 📖 Documentation Workflow

### Pattern: Generate → Review → Enhance

**Use When:** Creating or updating documentation

**Steps:**

1. **Generate Docstrings**
   ```python
   from skills.doc_generator.operations import generate_docstrings

   result = generate_docstrings(
       "payment.py",
       style="google",
       include_examples=True
   )

   print(f"Generated: {result.data['functions_documented']} docstrings")
   ```

2. **Generate README**
   ```python
   from skills.doc_generator.operations import generate_readme

   result = generate_readme(
       directory="skills/payment_processor/",
       include_api=True,
       include_examples=True
   )

   print(f"README saved to: {result.data['readme_path']}")
   ```

3. **Review Documentation**
   ```python
   from skills.doc_generator.operations import analyze_documentation

   analysis = analyze_documentation("skills/payment_processor/")

   print(f"Coverage: {analysis.data['coverage_percent']}%")
   print(f"Missing: {len(analysis.data['undocumented_items'])} items")
   ```

4. **Enhance Generated Docs**
   - Add usage examples
   - Include architecture diagrams
   - Document security considerations
   - Add troubleshooting sections

5. **Commit Documentation**
   ```bash
   git add skills/payment_processor/
   git commit -m "docs: add comprehensive payment processor documentation

   - Generated docstrings (Google style)
   - Added README with API reference
   - Included usage examples
   - Documented security considerations

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

**Token Efficiency:**
- Doc generation: ~1,000-2,000 tokens
- Analysis: ~500 tokens
- **vs manual writing:** ~10,000+ tokens

**Security:**
- Document security requirements
- Include safe usage examples
- Note permission requirements

---

## 🔄 Continuous Integration Workflow

### Pattern: Push → Build → Test → Deploy

**Use When:** Automated CI/CD pipeline

**Steps:**

1. **Pre-Push Checks**
   ```bash
   # Run tests
   pytest --cov=src --cov-fail-under=80

   # Check code quality
   pylint src/

   # Security scan
   safety check

   # Format check
   black --check src/
   ```

2. **Push to Remote**
   ```bash
   git push origin feature/add-2fa
   ```

3. **CI Pipeline Runs** (automated)
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on: [push, pull_request]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Run tests
           run: pytest --cov=src
         - name: Security scan
           run: safety check
   ```

4. **Review Results**
   - All tests passing?
   - Coverage acceptable?
   - No security issues?
   - Code quality good?

5. **Create PR** (if on feature branch)
   ```bash
   gh pr create --title "feat: Add 2FA support" --body "..."
   ```

6. **Merge After Approval**
   ```bash
   gh pr merge --squash
   ```

**Token Efficiency:**
- CI runs automatically (no tokens)
- PR review uses ~1,000-2,000 tokens

**Security:**
- Automated security scans
- Required checks before merge
- Code review required

---

## 🎯 Quick Reference

### Workflow Selection

| Task | Workflow | Estimated Time |
|------|----------|----------------|
| Learn new concept | Learning | 1-4 weeks |
| Add feature | Feature Implementation | 2-8 hours |
| Fix bug | Debugging | 30min-4 hours |
| Refactor code | Code Review | 1-3 hours |
| Write tests | TDD | Ongoing |
| Document code | Documentation | 30min-2 hours |

### Command Quick Reference

```bash
# Learning
/start-learning "<topic>"
/continue-plan
/ask-specialist <question>
/check-understanding "<concept>"
/update-plan

# Development
/create-project-plan
/git-start-feature "<name>"
/git-stage-commit
/create-pr

# Skills (Python)
from skills.<skill>.operations import <operation>
result = operation(response_format="summary")  # Always start with summary!
```

### Tool Configurations by Workflow

**Learning:**
```json
{"allowedTools": ["Read", "Glob", "Grep"]}
```

**Development:**
```json
{"allowedTools": ["Read", "Write", "Edit", "Glob", "Grep", "Bash(git:*)", "Bash(pytest:*)"]}
```

**Review:**
```json
{"allowedTools": ["Read", "Glob", "Grep"]}
```

---

## 📚 Related Documentation

- `TOOL_ALLOWLISTING_GUIDE.md` - Tool permissions per workflow
- `OPTIMIZATION_GUIDE.md` - Efficiency patterns
- `SANDBOXING_GUIDE.md` - Security configuration
- `../CLAUDE.md` - Navigation and patterns
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - System design

---

**Remember:** Good workflows are repeatable, efficient, and safe. Start with these patterns and adapt to your needs! 🚀

*Last Updated: 2025-11-08*
