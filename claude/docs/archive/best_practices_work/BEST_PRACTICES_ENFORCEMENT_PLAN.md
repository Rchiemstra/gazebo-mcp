# Best Practices Enforcement Plan for Skills and Agents

## Executive Summary

This document outlines a comprehensive system to ensure all new skills and agents in Claude Code follow established best practices. The system includes automated scaffolding, validation, templates, and CI/CD integration to maintain high quality standards with minimal manual oversight.

## Current State Analysis

### ✅ What Exists

**Skills:**
- 8 operational skills with consistent structure
- Skill registry with validation (`skills/integration/skill_registry.py`)
- Integration tests for Phase 1 and Phase 2 skills
- Comprehensive documentation

**Agents:**
- 14+ agents with standardized format
- Agent validation script (`scripts/validate-agents.py`)
- Clear teaching methodologies in agent prompts

**Documentation:**
- Skills system overview
- Integration architecture guide
- Agent-skills integration patterns

### ❌ Gaps Identified

1. **No templates** - No reusable skill template (agents have implicit template from examples)
2. **No scaffolding tools** - Manual creation prone to errors
3. **No pre-commit hooks** - No automated validation before commits
4. **No CI/CD integration** - No automated checks in pull requests
5. **No unified validation** - Separate scripts for skills vs agents
6. **No creation workflow** - No guided process for developers
7. **No code quality enforcement** - No linting/formatting checks

## Solution Architecture

### Phase 1: Templates and Scaffolding (Week 1)

#### 1.1 Skill Template
**Location:** `templates/skill-template/`

Complete directory structure with placeholders:
```
skill-template/
├── skill.md              # YAML frontmatter template
├── operations.py         # Standardized operations with OperationResult
├── __init__.py           # Package exports
├── README.md             # Documentation template
├── demo.py               # Usage demonstration template
├── core/                 # Core implementation directory
│   └── __init__.py
└── tests/                # Test directory
    └── __init__.py
```

**Placeholders:**
- `{{SKILL_NAME}}` - Kebab-case skill name
- `{{SKILL_DESCRIPTION}}` - One-line description
- `{{SKILL_CATEGORY}}` - Category (e.g., developer-productivity)
- `{{OPERATION_NAME}}` - Operation function names
- `{{OPERATION_DESCRIPTION}}` - Operation descriptions
- `{{AUTHOR_NAME}}` - Author name
- `{{CREATED_DATE}}` - ISO date

#### 1.2 CLI Scaffolding Tool for Skills
**Location:** `scripts/create-skill.py`

**Features:**
- Interactive prompts for all required fields
- Name validation (kebab-case)
- Description validation (length, clarity)
- Category selection from predefined list
- Multiple operations support
- Generates complete skill from template
- Runs validation after creation
- Provides next steps checklist

**Usage:**
```bash
python scripts/create-skill.py

# Interactive prompts:
# - Skill name (kebab-case): my-awesome-skill
# - Description: Brief description of functionality
# - Category: [1] developer-productivity [2] security-and-quality ...
# - Operation 1 name: analyze_code
# - Operation 1 description: Analyzes code for patterns
# - Add another operation? (y/n)
# - Author name: Your Name
#
# ✅ Skill created at: skills/my-awesome-skill/
# ✅ Validation passed
#
# Next steps:
# 1. Implement core logic in skills/my-awesome-skill/core/
# 2. Update operations.py with your implementation
# 3. Create demo.py to demonstrate usage
# 4. Run: python skills/my-awesome-skill/demo.py
```

#### 1.3 CLI Scaffolding Tool for Agents
**Location:** `scripts/create-agent.py`

**Features:**
- Interactive prompts for all required fields
- Name validation (kebab-case)
- Description validation (20-300 chars)
- Tool selection from valid tools list
- Model selection (sonnet, opus, haiku)
- Activation mode selection with guidance
- Generates agent markdown file
- Runs validation after creation

**Usage:**
```bash
python scripts/create-agent.py

# Interactive prompts:
# - Agent name (kebab-case): code-reviewer-assistant
# - Description: Reviews code and teaches best practices
# - Tools (space-separated): Read Write Bash
# - Model [sonnet/opus/haiku]: sonnet
# - Activation [proactive/manual/always]: manual
# - Agent type: [1] Teaching [2] Coordinator [3] Specialist
#
# ✅ Agent created at: agents/code-reviewer-assistant.md
# ✅ Validation passed
#
# Next steps:
# 1. Edit agents/code-reviewer-assistant.md
# 2. Add teaching approach (❌ NEVER and ✅ ALWAYS rules)
# 3. Add detailed agent instructions
# 4. Test activation in Claude Code
```

### Phase 2: Unified Validation (Week 1-2)

#### 2.1 Unified Validation Runner
**Location:** `scripts/validate-all.py`

**Features:**
- Validates all skills using SkillRegistry
- Validates all agents using agent validator
- Validates command files
- Generates comprehensive report
- Exit codes: 0 (success), 1 (errors), 2 (warnings)
- JSON output option for CI/CD
- Verbose mode for debugging

**Usage:**
```bash
# Validate everything
python scripts/validate-all.py

# Validate specific category
python scripts/validate-all.py --skills-only
python scripts/validate-all.py --agents-only

# JSON output for CI
python scripts/validate-all.py --json > validation-report.json

# Verbose mode
python scripts/validate-all.py --verbose
```

**Output:**
```
🔍 Validating Skills...
✅ code-search (4 operations)
✅ dependency-guardian (3 operations)
⚠️  new-skill: Missing README.md (warning)

🔍 Validating Agents...
✅ python-best-practices
✅ git-workflow-expert
❌ broken-agent: Description too short (error)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
✅ 8 skills validated
❌ 1 agent validation error
⚠️  1 warning

Exit code: 1 (validation errors found)
```

#### 2.2 Enhanced Skill Validation
**Updates to:** `skills/integration/skill_registry.py`

**New Checks:**
- ✅ Required files exist (skill.md, operations.py, __init__.py)
- ✅ Recommended files exist (README.md, demo.py)
- ✅ Operations match between skill.md and operations.py
- ✅ All operations use OperationResult return type
- ✅ All operations track duration
- ✅ All operations have error handling
- ✅ Error codes from standard list
- ✅ Docstrings present for all operations
- ✅ Exports in __init__.py match operations

#### 2.3 Enhanced Agent Validation
**Updates to:** `scripts/validate-agents.py`

**New Checks:**
- ✅ Activation mode appropriate for agent type
- ✅ Tool selection justified (not excessive)
- ✅ Teaching approach defined (for teaching agents)
- ✅ Response examples provided
- ✅ Integration patterns documented (if uses skills)
- ✅ Coordination protocols defined (for coordinators)

### Phase 3: Automation and CI/CD (Week 2)

#### 3.1 Pre-commit Hooks
**Location:** `.pre-commit-config.yaml`

**Hooks:**
```yaml
repos:
  - repo: local
    hooks:
      # Validate skills and agents
      - id: validate-skills-agents
        name: Validate Skills and Agents
        entry: python scripts/validate-all.py
        language: system
        pass_filenames: false
        always_run: false
        files: ^(skills/|agents/|scripts/validate)

      # Python code formatting
      - id: black
        name: Black Code Formatter
        entry: black
        language: system
        types: [python]
        files: ^skills/

      # Python linting
      - id: flake8
        name: Flake8 Linter
        entry: flake8
        language: system
        types: [python]
        files: ^skills/

      # Markdown formatting
      - id: markdownlint
        name: Markdown Lint
        entry: markdownlint-cli2
        language: system
        types: [markdown]
        files: ^(skills/|agents/|docs/)
```

**Installation:**
```bash
pip install pre-commit black flake8
pre-commit install
```

#### 3.2 GitHub Actions Workflow
**Location:** `.github/workflows/validate-skills-agents.yml`

```yaml
name: Validate Skills and Agents

on:
  pull_request:
    paths:
      - 'skills/**'
      - 'agents/**'
      - 'scripts/validate-*.py'
  push:
    branches:
      - main
      - develop

jobs:
  validate:
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

      - name: Run unified validation
        id: validate
        run: |
          python scripts/validate-all.py --json > validation-report.json
          python scripts/validate-all.py --verbose

      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: validation-report.json

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('validation-report.json', 'utf8'));
            const comment = `## Validation Report\n\n${report.summary}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });

  test-skills:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v3

      - name: Run skill integration tests
        run: |
          python test_all_phase1_skills.py
          python test_all_phase2_skills.py
```

### Phase 4: Documentation (Week 2-3)

#### 4.1 Best Practices Checklist
**Location:** `docs/BEST_PRACTICES_CHECKLIST.md`

**Skill Creation Checklist:**
- [ ] Used `create-skill.py` scaffolding tool
- [ ] Implemented all operations in `operations.py`
- [ ] All operations return `OperationResult`
- [ ] All operations track duration
- [ ] Error handling with standard error codes
- [ ] Docstrings for all operations
- [ ] Created `demo.py` demonstrating usage
- [ ] Created comprehensive `README.md`
- [ ] Added tests in `tests/` directory
- [ ] Ran `python scripts/validate-all.py` successfully
- [ ] Tested with actual agent invocation

**Agent Creation Checklist:**
- [ ] Used `create-agent.py` scaffolding tool
- [ ] Description between 20-300 characters
- [ ] Minimal necessary tools selected
- [ ] Appropriate activation mode chosen
- [ ] Teaching approach defined (❌ NEVER / ✅ ALWAYS)
- [ ] Response examples provided
- [ ] Integration with skills documented (if applicable)
- [ ] Ran `python scripts/validate-all.py` successfully
- [ ] Tested agent activation in Claude Code

**Code Review Checklist:**
- [ ] All validation checks pass
- [ ] Code follows Python style guide (Black, Flake8)
- [ ] Documentation is clear and complete
- [ ] Examples are provided and working
- [ ] No security vulnerabilities introduced
- [ ] Performance requirements met (<200ms for operations)

#### 4.2 Quick Start Guide
**Location:** `docs/QUICK_START_GUIDE.md`

**Contents:**
1. Creating Your First Skill (5 min)
2. Creating Your First Agent (3 min)
3. Testing Your Skill/Agent
4. Submitting for Review
5. Common Pitfalls and Solutions
6. FAQ

### Phase 5: Quality Tools (Week 3)

#### 5.1 Code Quality Configuration

**pyproject.toml:**
```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

**.flake8:**
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, E266, E501, W503
exclude = .git,__pycache__,build,dist,.venv
per-file-ignores =
    __init__.py:F401
```

#### 5.2 Documentation Checker
**Location:** `scripts/check-documentation.py`

**Checks:**
- README.md completeness
- Broken links in documentation
- Code examples validity
- Consistent formatting
- Required sections present

## Standard Error Codes

All skills must use these standardized error codes:

| Code | Usage | Resolution Guidance |
|------|-------|---------------------|
| `VALIDATION_ERROR` | Invalid input parameters | Review parameter requirements and types |
| `FILE_NOT_FOUND` | Required file/directory missing | Verify file paths and existence |
| `OPERATION_ERROR` | General operation failure | Check logs for detailed error information |
| `SEARCH_ERROR` | Search operation failed | Verify search parameters and index |
| `ANALYSIS_ERROR` | Code analysis failed | Ensure code is parseable and valid |
| `TIMEOUT` | Operation exceeded time limit | Reduce scope or increase timeout |
| `DEPENDENCY_ERROR` | Missing required dependency | Install required dependencies |
| `PARSE_ERROR` | Code parsing failed | Check syntax and language support |
| `GENERATION_ERROR` | Code/doc generation failed | Review generation parameters |
| `PERMISSION_DENIED` | Insufficient permissions | Check file/directory permissions |
| `NETWORK_ERROR` | Network request failed | Check connectivity and endpoints |

## Best Practices Reference

### Skills Best Practices

**1. Structure:**
```
skill-name/
├── skill.md              # ✅ REQUIRED
├── operations.py         # ✅ REQUIRED
├── __init__.py           # ✅ REQUIRED
├── README.md             # ⭐ RECOMMENDED
├── demo.py               # ⭐ RECOMMENDED
├── core/                 # Implementation modules
└── tests/                # ⭐ RECOMMENDED
```

**2. skill.md Format:**
```yaml
---
name: kebab-case-name              # ✅ REQUIRED
version: 0.1.0                     # ✅ REQUIRED (semver)
description: Brief one-liner       # ✅ REQUIRED
category: category-name            # ⭐ RECOMMENDED
operations:                        # ✅ REQUIRED
  operation_name: "Description"
dependencies: []                   # Optional
tags: [tag1, tag2]                # Optional
---
```

**3. operations.py Pattern:**
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time

@dataclass
class OperationResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None

def operation_name(param: str, **kwargs) -> OperationResult:
    """Operation description."""
    start_time = time.time()

    try:
        # Implementation
        return OperationResult(
            success=True,
            data={'result': result},
            duration=time.time() - start_time,
            metadata={'skill': 'skill-name', 'version': '0.1.0'}
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=str(e),
            error_code='OPERATION_ERROR',
            duration=time.time() - start_time
        )
```

**4. Performance Targets:**
- Target: < 200ms per operation
- Maximum: < 2000ms per operation
- Always track duration in OperationResult

### Agents Best Practices

**1. YAML Frontmatter:**
```yaml
---
name: agent-name                   # ✅ Kebab-case
description: 20-300 char desc      # ✅ Clear and specific
tools:                             # ✅ Minimal necessary
  - Read
  - Write
model: sonnet                      # ✅ sonnet/opus/haiku
activation: manual                 # ✅ proactive/manual/always
---
```

**2. Activation Modes:**
- **proactive**: Coordinators, mentors, high-value automation
- **manual**: Specialized tasks, heavy operations, teaching
- **always**: ⚠️ Use sparingly for critical monitoring only

**3. Teaching Agent Pattern:**
```markdown
## TEACHING APPROACH (NO COMPLETE SOLUTIONS)

❌ NEVER:
- Write complete functions or implementations
- Just give answers without explaining why
- Do the work for the student

✅ ALWAYS:
- Guide through understanding
- Explain the thinking process
- Provide small pattern examples (2-3 lines max)
- Ask guiding questions
```

**4. Tool Selection:**
- Use minimal tools necessary for the role
- Always Read before Write/Edit
- Prefer specialized tools over Bash
- Document why each tool is needed

## Implementation Timeline

### Week 1: Foundation
- ✅ Day 1-2: Create skill template structure
- ✅ Day 2-3: Create CLI scaffolding tools (skills + agents)
- ✅ Day 3-4: Create unified validation runner
- ✅ Day 4-5: Enhance existing validation scripts

### Week 2: Automation
- ✅ Day 1-2: Set up pre-commit hooks configuration
- ✅ Day 2-3: Create GitHub Actions workflow
- ✅ Day 3-4: Create best practices checklist
- ✅ Day 4-5: Create quick start guide

### Week 3: Quality and Testing
- ✅ Day 1-2: Add code quality tools (Black, Flake8)
- ✅ Day 2-3: Create documentation checker
- ✅ Day 3-4: End-to-end testing of entire workflow
- ✅ Day 4-5: Documentation and tutorial video

## Success Metrics

- ✅ 100% of new skills use scaffolding tool
- ✅ 100% validation pass rate on main branch
- ✅ < 5 minutes to create new skill/agent from scratch
- ✅ Zero manual review for automated checks
- ✅ All PRs automatically validated
- ✅ 100% of skills/agents have complete documentation
- ✅ < 10% of PRs require validation fixes

## Rollout Strategy

### Phase 1: Pilot (Week 1-2)
- Deploy to development branch
- Test with 2-3 new skills/agents created by team
- Gather feedback and iterate
- Document common issues

### Phase 2: Soft Launch (Week 3-4)
- Enable pre-commit hooks (warnings only)
- Run CI/CD validation (non-blocking)
- Provide support and documentation
- Monitor adoption metrics

### Phase 3: Full Enforcement (Week 5+)
- Make pre-commit hooks required
- Make CI/CD validation blocking on PRs
- Deprecate manual creation process
- Regular review and improvement meetings

## Maintenance and Improvement

### Monthly Reviews
- Review validation failure patterns
- Update error codes and checks as needed
- Improve documentation based on feedback
- Add new templates for emerging patterns

### Quarterly Reviews
- Analyze adoption metrics
- Survey developer satisfaction
- Review and update best practices
- Plan new automation features

## Tool Reference

### Creation Tools
- `scripts/create-skill.py` - Scaffold new skill
- `scripts/create-agent.py` - Scaffold new agent

### Validation Tools
- `scripts/validate-all.py` - Unified validation
- `scripts/validate-agents.py` - Agent validation
- `skills/integration/skill_registry.py` - Skill validation

### Quality Tools
- `black` - Python code formatter
- `flake8` - Python linter
- `isort` - Import sorter
- `markdownlint` - Markdown linter

### Testing Tools
- `test_all_phase1_skills.py` - Phase 1 skill tests
- `test_all_phase2_skills.py` - Phase 2 skill tests
- `pytest` - Unit testing framework

## Support and Resources

### Documentation
- `docs/QUICK_START_GUIDE.md` - Getting started
- `docs/BEST_PRACTICES_CHECKLIST.md` - Creation checklist
- `docs/SKILLS_SYSTEM_OVERVIEW.md` - Skills architecture
- `skills/INTEGRATION_ARCHITECTURE.md` - Integration patterns

### Getting Help
- GitHub Issues for bugs
- GitHub Discussions for questions
- Code review for complex cases

## Appendix: Example Workflows

### Creating a New Skill
```bash
# 1. Run scaffolding tool
python scripts/create-skill.py

# 2. Implement core logic
cd skills/my-skill/core
# ... implement your logic ...

# 3. Update operations.py
# ... connect operations to core logic ...

# 4. Create demo
python skills/my-skill/demo.py

# 5. Validate
python scripts/validate-all.py

# 6. Commit
git add skills/my-skill/
git commit -m "Add my-skill: Description"
# Pre-commit hooks run automatically
```

### Creating a New Agent
```bash
# 1. Run scaffolding tool
python scripts/create-agent.py

# 2. Edit agent file
vim agents/my-agent.md
# ... add teaching approach and instructions ...

# 3. Validate
python scripts/validate-all.py

# 4. Test
# Test agent activation in Claude Code

# 5. Commit
git add agents/my-agent.md
git commit -m "Add my-agent: Description"
# Pre-commit hooks run automatically
```

---

**Version:** 1.0.0
**Last Updated:** 2025-11-10
**Author:** Claude Code Team
