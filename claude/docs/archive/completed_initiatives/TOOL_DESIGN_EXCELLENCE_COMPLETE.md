# Tool Design Excellence Guide

**Last Updated:** 2025-11-10
**Status:** Complete reference for designing skills and agents
**Based on:** Anthropic's "Writing Tools for Agents" best practices

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Skill Structure Template](#skill-structure-template)
3. [Agent Structure Template](#agent-structure-template)
4. [Naming Conventions](#naming-conventions)
5. [Parameter Handling](#parameter-handling)
6. [Progressive Disclosure](#progressive-disclosure)
7. [Error Messages](#error-messages)
8. [Common Patterns](#common-patterns)
9. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
10. [Validation Checklist](#validation-checklist)

---

## Core Principles

### 1. Clear, Non-Overlapping Functionality

**Each skill should have ONE clear purpose**

✅ **Good:**
- `/verify-build` - Compiles code and checks for errors
- `/verify-tests` - Runs test suites
- `/verify-lint` - Checks code quality

❌ **Bad:**
- `/verify-all` - Does build, tests, lint, and integration checks (too broad)
- `/check-code` - Ambiguous - what exactly does it check?

**Rule:** If humans can't definitively choose between two tools, neither can AI agents.

### 2. Self-Contained Descriptions

**The description field must fully explain what the tool does**

```yaml
# ❌ Too vague
---
description: Validates ROS2 node implementation
---

# ✅ Clear and specific
---
description: Validates ROS2 node implementation against best practices including parameter declaration, proper initialization, QoS configuration, and logging patterns
---
```

**What to include:**
- **What** it does
- **What** it checks/validates/generates
- **What** output it produces
- **When** to use it

### 3. Meaningful Return Values

**Return human-readable information, not just technical IDs**

❌ **Bad:**
```
Build completed
Exit code: 0
Build ID: 8a3d-9f2e-11eb
```

✅ **Good:**
```
Build Verification: my_package

Status: ✅ SUCCESS
Build Time: 45.2 seconds
Warnings: 0
Files Compiled: 12

Artifacts Created:
  - lib/my_package/my_node
  - lib/libmy_package.so

Next Steps:
1. Run tests: /verify-tests my_package
2. Run node: ros2 run my_package my_node
```

**Return format principles:**
- Use clear status indicators (✅ ❌ ⚠️)
- Include actionable next steps
- Provide context, not just data
- Format for human readability

### 4. Token Efficiency

**Provide options for response detail level**

```yaml
# In skill parameters
response_format: ${2:-concise}  # or "detailed"
```

**Concise** (default):
```
✅ ROS Node Verification: PASSED
Checked: 12 items | Warnings: 2 | Time: 1.2s
```

**Detailed** (when requested):
```
ROS Node Verification: sensor_node.py

✅ PASSED (10/12 checks)

✅ Structure: Node class inherits from rclcpp::Node
✅ Parameters: All declared with declare_parameter()
⚠️  QoS: Using default QoS (consider explicit)
✅ Logging: Uses ROS logger correctly
...
```

**For Python skills:** Implement `response_format` parameter in operations
```python
def operation(params, response_format="summary"):
    if response_format == "summary":
        return {"status": "success", "count": 10}
    else:
        return {"status": "success", "items": [...], "details": [...]}
```

### 5. Actionable Error Messages

**Replace opaque errors with specific guidance**

❌ **Bad:**
```
Error: ParameterNotDeclaredException
Traceback (most recent call last):
  File "node.py", line 42, in __init__
    rate = self.get_parameter('rate').value
rclcpp._rclpy_pybind11.ParameterNotDeclaredException
```

✅ **Good:**
```
❌ ERROR: Parameter Not Declared

File: src/sensor_node.py
Line: 42
Issue: Attempting to get parameter 'rate' without declaring it first

In ROS2, parameters MUST be declared before use.

Fix:
  # Add this BEFORE getting the parameter:
  self.declare_parameter('rate', 10.0)  # name, default
  rate = self.get_parameter('rate').value

Reference: .claude/ros-patterns.md (Parameter Management section)
```

**Error message format:**
```
❌ ERROR: [Clear Error Title]

Location: [file:line]
Issue: [What went wrong]
Cause: [Why it happened]

Fix:
[Specific code or steps to resolve]

Reference: [Where to learn more]
```

---

## Skill Structure Template

```markdown
---
description: [Clear, specific description of what this skill does]
argument-hint: [arg1] [arg2] [optional-arg]
model: claude-haiku-4-5-20251001  # or sonnet for complex reasoning
category: [verification|workflow|ros|modbus|git|analysis]
complexity: [low|medium|high]
requires: [comma-separated list of dependencies]
---

You are the [Skill Name] skill. Your job is to [clear, one-sentence purpose].

## Task

[What needs to be done]: ${1:-<ask user if not provided>}

## Purpose

[2-3 sentences explaining WHY this skill exists and WHEN to use it]

## Process

### 1. [First Step]
[Clear instructions for first action]

### 2. [Second Step]
[Clear instructions for second action]

### 3. [Validation]
[How to verify the action succeeded]

## Output Format

```
[Skill Name]: [target]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SECTION HEADER]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: [✅ SUCCESS | ⚠️ WARNINGS | ❌ FAILED]

[Key metrics or information]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DETAILS SECTION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Detailed information]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[RECOMMENDATIONS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Actionable next steps based on results]
```

## Common Issues

### Issue: [Problem Description]

**Symptoms**: [How to recognize it]

**Cause**: [Why it happens]

**Solution**:
```
[Code or commands to fix]
```

## Exit Codes

- **0**: [Success condition]
- **1**: [Warning condition]
- **2**: [Failure condition]
- **3**: [Cannot execute condition]

Now [perform the skill's action]!
```

---

## Agent Structure Template

```markdown
---
description: [Clear description of what this agent orchestrates]
argument-hint: [task-description]
category: [workflow|ros|modbus|cpp|python|testing|quality]
complexity: [medium|high]
requires: [comma-separated list of skills this agent uses]
---

You are the [Agent Name] agent. Your job is to [clear purpose statement].

## Your Mission

[2-3 sentences explaining the agent's role and what it coordinates]

## Task Description

$ARGUMENTS

## Required Skills

This agent uses the following skills:
- `skill_name` (required) - Purpose description
- `skill_name` (optional) - Purpose description

## Setup Verification

Before proceeding, verify required skills are available:
```python
# Check required skills
try:
    from skills.required_skill import operation
except ImportError:
    raise MissingSkillError("Required skill not found")
```

## Workflow

### Phase 1: [Initial Phase Name]

**Goal**: [What this phase accomplishes]

**Actions**:
- [Specific action 1]
- [Specific action 2]
- Use `/skill-name` for [specific purpose]

**Expected Output**:
- [What gets produced]
- [What gets verified]

**Decision Point**: [When to pause and ask user]

### Phase 2: [Second Phase Name]

**Goal**: [What this phase accomplishes]

**Actions**:
[Similar structure]

**Expected Output**:
[Similar structure]

**Decision Point**: [When to pause and ask user]

### Phase 3: [Final Phase Name]

**Goal**: [What this phase accomplishes]

**Actions**:
[Similar structure]

**Expected Output**:
[Similar structure]

## Orchestration Pattern

```
User Request
  ↓
Phase 1: [Name]
  → Use /skill1
  → Use /skill2
  → Verify results
  ↓
[Decision point / user confirmation]
  ↓
Phase 2: [Name]
  → Use /skill3
  → Verify results
  ↓
Final Output
```

## Error Handling

**If Phase 1 fails:**
- [Specific recovery action]
- [When to ask user]

**If Phase 2 fails:**
- [Specific recovery action]

## Skill Usage Pattern

```python
# Example of calling a skill
from skills.skill_name import operation

try:
    result = operation(param1, param2, response_format="summary")
    if result.success:
        # Handle success
        pass
    else:
        # Handle error
        pass
except SkillError as e:
    # Handle skill-specific errors
    logger.error(f"Skill error: {e}")
```

## Graceful Degradation

If optional skills are unavailable:
1. Log a warning about missing functionality
2. Continue with available skills
3. Suggest installing missing skills

## Best Practices

1. [Practice 1]
2. [Practice 2]
3. Always verify after each action
4. Stop on failure, report clearly

## Output Format

[Clear structured output template]

Now begin [the agent's work]!
```

---

## Naming Conventions

### Skill Names

**Pattern:** `verb-noun` or `verb-noun-qualifier`

✅ **Good:**
- `/verify-build`
- `/verify-ros-node`
- `/gather-context`
- `/git-commit`
- `/modbus-handler`

❌ **Bad:**
- `/verification` (noun, not action)
- `/check` (too vague)
- `/do-ros-stuff` (unprofessional)

### Agent Names

**Pattern:** `noun-verb` or `action-context`

✅ **Good:**
- `/dev` (complete development workflow)
- `/create-ros-node`
- `/modbus-bridge`
- `/ros-debug`

❌ **Bad:**
- `/ros` (too vague)
- `/helper` (meaningless)
- `/do-everything` (not focused)

### Directory Organization

```
.claude/commands/
├── skills/           # Foundation tools
│   ├── meta/        # Skill/agent creators
│   ├── workflow/    # Context, planning
│   ├── git/         # Version control
│   ├── ros/         # ROS fundamentals
│   ├── modbus/      # Modbus protocol
│   ├── verification/# Quality checks
│   ├── analysis/    # Debugging, analysis
│   └── robot/       # Robot modeling
└── agents/          # High-level orchestrators
    ├── workflow/    # Development workflows
    ├── ros/         # ROS development
    ├── modbus/      # Modbus integration
    ├── cpp/         # C++ development
    ├── python/      # Python development
    ├── testing/     # Testing & validation
    ├── quality/     # Code quality
    └── [domain]/    # Domain-specific
```

---

## Parameter Handling

### Required Parameters

```yaml
---
argument-hint: [package-name]
---

Package to build: ${1:-<ask user>}
```

If not provided, skill MUST ask user clearly:
```
No package specified.

Usage: /verify-build <package-name>

Available packages:
  - my_robot_pkg
  - sensor_drivers
  - control_system

Which package should I build?
```

### Optional Parameters

```yaml
---
argument-hint: [package-name] [optional-flags]
---

Package: ${1:-<ask user>}
Build flags: ${2:-""}  # Empty string if not provided
```

### Named Parameters

For complex skills:
```yaml
---
argument-hint: [target] --format=[format] --output=[path]
---

Target: ${1:-<ask user>}
Format: [extract from arguments, default to "markdown"]
Output: [extract from arguments, default to "stdout"]
```

---

## Progressive Disclosure

**Load information in tiers:**

**Tier 1:** YAML frontmatter (always loaded)
```yaml
---
description: Short description
category: verification
complexity: low
---
```

**Tier 2:** Main skill content (loaded when skill invoked)
```markdown
Core instructions and workflow
```

**Tier 3:** Reference files (loaded on-demand)
```markdown
See detailed examples in: verify-ros-node-examples.md
See common issues in: ros-troubleshooting.md
```

**Benefits:**
- Reduces initial token load
- Enables targeted detail retrieval
- Maintains documentation completeness
- Scales to large knowledge bases

---

## Error Messages

### Error Message Structure

```python
class SkillError(Exception):
    """Base error with agent-friendly format"""

    def __init__(self, message, suggestions=None, example_fix=None):
        self.message = message
        self.suggestions = suggestions or []
        self.example_fix = example_fix
        super().__init__(self.format_error())

    def format_error(self):
        error_msg = f"❌ ERROR: {self.message}\n"

        if self.suggestions:
            error_msg += "\nSuggestions:\n"
            for i, suggestion in enumerate(self.suggestions, 1):
                error_msg += f"{i}. {suggestion}\n"

        if self.example_fix:
            error_msg += f"\nExample fix:\n{self.example_fix}\n"

        return error_msg
```

### Error Message Examples

**File Not Found:**
```python
raise SkillError(
    "File not found: src/node.py",
    suggestions=[
        "Check if the file path is correct",
        "Verify you're in the right directory",
        "Check if the file was moved or deleted"
    ],
    example_fix="ls -la src/  # List files to verify path"
)
```

**Invalid Configuration:**
```python
raise SkillError(
    "Invalid parameter 'rate': must be > 0",
    suggestions=[
        "Update YAML config with valid rate value",
        "Check parameter declaration in code",
        "Review parameter constraints"
    ],
    example_fix="""
# config.yaml
parameters:
  rate: 10.0  # Must be positive
"""
)
```

---

## Common Patterns

### Verification Pattern

Used in: `/verify-*` skills

```markdown
1. Check prerequisites
2. Run verification checks
3. Collect results
4. Categorize: PASS / WARN / FAIL
5. Report with specific issues
6. Provide fixes for failures
7. Return appropriate exit code
```

### Generation Pattern

Used in: `/create-*`, `/*-gen` skills

```markdown
1. Validate inputs
2. Load template/pattern
3. Customize for use case
4. Generate files/code
5. Validate generated output
6. Report what was created
7. Show usage examples
```

### Analysis Pattern

Used in: `/analyze`, `/debug`, `/pattern-detect` skills

```markdown
1. Scan target (files/system)
2. Identify patterns/issues
3. Categorize findings
4. Rank by severity/importance
5. Report with examples
6. Suggest improvements
7. Provide references
```

### Orchestration Pattern

Used in: agents like `/dev`, `/execute`

```markdown
1. Parse user request
2. Break into phases
3. For each phase:
   a. Execute actions
   b. Verify results
   c. Report progress
   d. Stop on failure
4. Final summary
5. Next steps
```

---

## Anti-Patterns to Avoid

### ❌ Vague Descriptions

```yaml
description: Helps with ROS stuff  # What stuff exactly?
```

### ❌ Tool Overlap

```
/verify-code     # What does it verify?
/check-code      # Same as above?
/validate-code   # Still unclear!
```

### ❌ Technical Jargon in Errors

```
Error: RCLCPP_PARAMETER_NOT_DECLARED_EXCEPTION_0x4a3f
# User has no idea what this means
```

### ❌ No Next Steps

```
Build failed.
# OK, but what should I do now?
```

### ❌ Overly Broad Tools

```
/do-everything   # Does way too much
/ros-helper      # Too vague
/fixer           # Fixes what?
```

### ❌ Duplicated Documentation

```markdown
# skill1.md
## Best Practices
[500 lines of content]

# skill2.md
## Best Practices
[Same 500 lines of content]
```

**Fix:** Reference shared documentation:
```markdown
## Best Practices
See: `.claude/best-practices.md`
```

---

## Validation Checklist

Before finalizing a skill/agent, verify:

### Description
- [ ] Clearly states what the tool does
- [ ] Specific enough to distinguish from similar tools
- [ ] Includes key actions/checks performed
- [ ] Under 100 characters for frontmatter

### Functionality
- [ ] Single, clear purpose
- [ ] No overlap with existing tools
- [ ] Self-contained (doesn't require other skills to work)
- [ ] Handles errors gracefully

### Parameters
- [ ] Required parameters clearly indicated
- [ ] Defaults provided where sensible
- [ ] Argument hints show usage
- [ ] Validates input before processing

### Output
- [ ] Human-readable format
- [ ] Clear status indicators
- [ ] Actionable next steps
- [ ] Appropriate detail level

### Error Handling
- [ ] Specific error messages
- [ ] Clear cause explanation
- [ ] Concrete fix suggestions
- [ ] References to documentation

### Documentation
- [ ] Purpose clearly explained
- [ ] Process steps detailed
- [ ] Common issues documented
- [ ] Exit codes defined

### Testing
- [ ] Tested with valid inputs
- [ ] Tested with invalid inputs
- [ ] Tested with edge cases
- [ ] Error messages verified

### Token Efficiency
- [ ] Uses appropriate model (Haiku vs Sonnet)
- [ ] Implements response_format parameter (if applicable)
- [ ] References external docs instead of duplicating
- [ ] Concise, structured content

---

## Best Practices Summary

**Great tools are:**
1. **Focused**: One clear purpose
2. **Clear**: Obvious what they do from description
3. **Helpful**: Return actionable information
4. **Efficient**: Don't waste tokens
5. **Resilient**: Handle errors gracefully
6. **Consistent**: Follow established patterns

**Before creating a new tool, ask:**
- Is this truly needed or does an existing tool cover it?
- Can the purpose be explained in one sentence?
- Will users know when to use this vs similar tools?
- Are error messages helpful and actionable?
- Does the output help users make decisions?

**Remember:** The best tool is one that's so clear, users know exactly when to use it and what to expect.

---

## Available Command Systems

This workspace provides three complementary command systems, each following the design principles outlined in this guide:

### 1. ROS/Robotics Commands (67 commands)
**Location:** `~/.claude/commands/`
**Reference:** `~/.claude/CLAUDE.md`
**Purpose:** Fast, specialized ROS2/robotics development tasks

**Examples following design excellence:**
- `/verify-build` - Clear single purpose (compile and check errors)
- `/create-ros-node` - Self-contained description with all required parameters
- `/dev` - Complete workflow orchestrator with phased approach

**Design patterns used:**
- Verification pattern (verify-build, verify-tests, verify-lint)
- Generation pattern (cmake-gen, package-xml-gen, launch-gen)
- Orchestration pattern (dev, dev-tdd, dev-visual)
- Analysis pattern (ros-graph-analyze, bag-analyze)

### 2. Python Skills (20+ skills)
**Location:** `skills/`
**Reference:** Individual `skills/*/SKILL.md` files
**Purpose:** Complex data operations, code analysis, programmatic integration

**Examples following design excellence:**
- `code_analysis.analyze_file()` - Progressive disclosure via response_format
- `refactor_assistant` - Meaningful return values with OperationResult
- `context_manager` - Token-efficient context operations

### 3. Teaching Agents (17+ agents)
**Location:** `agents/`
**Reference:** `COMMANDS_README.md`
**Purpose:** Learning, mentoring, guided workflows

**Examples following design excellence:**
- `learning-coordinator` - Clear orchestration of learning journey
- `ros2-learning-mentor` - Self-contained ROS2 teaching
- `plan-generation-mentor` - Focused on learning plan creation

**See `docs/COMMANDS_REFERENCE.md` for complete system overview.**

---

## Related Documentation

- `docs/TOKEN_EFFICIENCY_COMPLETE.md` - Token optimization guide
- `docs/COMMANDS_REFERENCE.md` - All command systems overview
- `~/.claude/CLAUDE.md` - ROS/robotics commands reference (67 commands)
- `~/.claude/ros-patterns.md` - ROS2 architectural patterns
- `templates/skill-template/` - Skill scaffolding
- `templates/agent-template/` - Agent scaffolding (if available)
- `skills/CLAUDE.md` - Skills usage guide (if exists)

---

## Maintenance

This guide should be updated when:
- New design patterns emerge
- Anthropic releases new best practices
- Project structure evolves
- Common anti-patterns are discovered

**Last updated:** 2025-11-10
**Next review:** When creating meta tools (Phase 2)

---

**Status:** Complete design reference
**Based on:** Anthropic "Writing Tools for Agents" + workspace experience
**Applies to:** All skills, agents, and commands
