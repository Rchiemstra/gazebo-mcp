# Best Practices Checklist
## For Skills and Agents Creation

**Purpose:** Use this checklist when creating or reviewing skills and agents to ensure adherence to best practices.

**References:**
- `docs/ANTHROPIC_BEST_PRACTICES.md` - Comprehensive best practices guide
- `docs/BEST_PRACTICES_ENFORCEMENT_PLAN.md` - Enforcement strategy

---

## Table of Contents
1. [Skill Creation Checklist](#skill-creation-checklist)
2. [Agent Creation Checklist](#agent-creation-checklist)
3. [Code Review Checklist](#code-review-checklist)
4. [Testing Checklist](#testing-checklist)
5. [Documentation Checklist](#documentation-checklist)

---

## Skill Creation Checklist

### Setup and Scaffolding

- [ ] Used `python scripts/create-skill.py` to scaffold the skill
- [ ] Skill name follows kebab-case format (e.g., `my-skill-name`)
- [ ] Skill directory created in `skills/`
- [ ] All template files generated successfully

### File Structure

**Required Files:**
- [ ] `skill.md` exists and contains valid YAML frontmatter
- [ ] `operations.py` exists with standardized interface
- [ ] `__init__.py` exists with proper exports

**Recommended Files:**
- [ ] `README.md` exists with user documentation
- [ ] `demo.py` exists demonstrating all operations
- [ ] `core/` directory exists for implementation
- [ ] `tests/` directory exists with test files

### skill.md Configuration

- [ ] YAML frontmatter properly formatted (`---` delimiters)
- [ ] **Required fields present:**
  - [ ] `name` - matches directory name, kebab-case
  - [ ] `version` - follows semantic versioning (X.Y.Z)
  - [ ] `description` - clear, one-line description
  - [ ] `operations` - dict of operation_name: description
- [ ] **Recommended fields present:**
  - [ ] `category` - appropriate category selected
  - [ ] `author` - author name specified
  - [ ] `created` - creation date (YYYY-MM-DD)
- [ ] Operations dictionary is complete and accurate
- [ ] Each operation has clear description
- [ ] Documentation body provides detailed information

### operations.py Implementation

**Data Structures:**
- [ ] `OperationResult` dataclass defined or imported
- [ ] `ErrorCodes` class defined with standard codes
- [ ] All operations return `OperationResult`

**Operation Functions:**
- [ ] All operations have type hints for parameters
- [ ] All operations have comprehensive docstrings
- [ ] All operations include usage examples in docstrings
- [ ] All operations list possible error codes

**Error Handling:**
- [ ] All operations wrapped in try-except blocks
- [ ] Specific exceptions caught (ValueError, FileNotFoundError, etc.)
- [ ] Generic Exception as final catch-all
- [ ] Error messages are actionable and specific
- [ ] Standard error codes used (from ErrorCodes class)

**Performance Tracking:**
- [ ] `import time` at module level
- [ ] `start_time = time.time()` at beginning of each operation
- [ ] Duration calculated: `time.time() - start_time`
- [ ] Duration included in all OperationResult returns

**Metadata:**
- [ ] Metadata dictionary includes skill name
- [ ] Metadata dictionary includes version
- [ ] Metadata dictionary includes operation name
- [ ] Metadata includes operation-specific context

**Best Practices from Anthropic:**
- [ ] Operations consolidate multi-step actions (high-level, not low-level)
- [ ] Parameter names are unambiguous (e.g., `user_id` not `user`)
- [ ] Return data is semantically meaningful (names, types, not UUIDs)
- [ ] Smart defaults implemented for pagination/filtering
- [ ] Operations target < 200ms execution time

### __init__.py Configuration

- [ ] Imports all operations from operations.py
- [ ] Imports OperationResult
- [ ] Imports ErrorCodes
- [ ] `__version__` defined matching skill.md
- [ ] `__all__` list contains all exports
- [ ] Module docstring present

### Implementation (core/)

- [ ] Core implementation separated from operations interface
- [ ] Implementation modules in `core/` directory
- [ ] Clear separation of concerns
- [ ] No direct coupling to operations.py
- [ ] Reusable, testable functions

### Demo (demo.py)

- [ ] Demonstrates all operations
- [ ] Shows successful operation execution
- [ ] Shows error handling
- [ ] Shows agent usage example
- [ ] Pretty-prints results
- [ ] Runnable without errors

### Testing (tests/)

- [ ] Test file exists: `tests/test_operations.py`
- [ ] Tests for each operation
- [ ] Tests for successful execution
- [ ] Tests for error cases
- [ ] Tests for edge cases
- [ ] Tests verify OperationResult structure
- [ ] Tests verify duration tracking
- [ ] Tests verify metadata presence
- [ ] Tests runnable with pytest

### Documentation (README.md)

- [ ] Clear description of skill purpose
- [ ] Installation/setup instructions (if needed)
- [ ] Usage examples for each operation
- [ ] Python API examples
- [ ] Agent invocation examples
- [ ] Error handling examples
- [ ] Performance characteristics documented
- [ ] Testing instructions
- [ ] Contributing guidelines

### Validation

- [ ] Ran `python scripts/validate-all.py`
- [ ] No validation errors
- [ ] Addressed all warnings (or documented why ignored)
- [ ] Tested skill with actual agent invocation
- [ ] All operations tested manually
- [ ] Demo runs successfully

### Security

- [ ] No hardcoded credentials or secrets
- [ ] No unsafe file operations
- [ ] No SQL injection vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] Input validation implemented
- [ ] Sanitization of user inputs

---

## Agent Creation Checklist

### Setup and Scaffolding

- [ ] Used `python scripts/create-agent.py` to scaffold the agent
- [ ] Agent name follows kebab-case format (e.g., `my-agent-name`)
- [ ] Agent file created in `agents/` directory
- [ ] Template selected matches agent purpose

### YAML Frontmatter

**Required Fields:**
- [ ] `name` - kebab-case, matches filename
- [ ] `description` - between 20-300 characters
- [ ] `tools` - list of minimal necessary tools
- [ ] `model` - one of: sonnet, opus, haiku

**Validation:**
- [ ] Name format correct (lowercase, hyphens only)
- [ ] Description length appropriate (20-300 chars)
- [ ] Description describes role AND approach
- [ ] Tools are from valid list
- [ ] Tools are minimal for the role
- [ ] Model selection appropriate for task complexity

**Optional but Recommended:**
- [ ] `activation` specified (proactive/manual/always)
- [ ] Activation mode appropriate for agent type

### Tool Selection

- [ ] Tools list justified (not excessive)
- [ ] Read included if agent needs to read files
- [ ] Write included if agent needs to create files
- [ ] Edit included if agent needs to modify files
- [ ] Bash included if agent needs shell commands
- [ ] Task included if agent coordinates subagents
- [ ] No redundant tools included

**Best Practices:**
- [ ] Uses minimal tools necessary
- [ ] Teaching agents typically use: Read, Write
- [ ] Coordinators typically use: Read, Write, Task
- [ ] Specialists typically use: Read, Write, Bash
- [ ] Total tools < 6 (ideally 2-4)

### Model Selection

- [ ] Sonnet selected for general-purpose agents ✅ (recommended)
- [ ] Opus selected only if complex reasoning required
- [ ] Haiku selected only for simple, fast operations
- [ ] Model choice justified for the task

### Activation Mode

- [ ] `manual` for: Teaching agents, specialists, heavy operations ✅ (most common)
- [ ] `proactive` for: Coordinators, mentors, high-value automation
- [ ] `always` used sparingly (only critical monitoring)
- [ ] Activation mode appropriate for agent frequency
- [ ] Proactive agents won't cause alert fatigue

### Agent Instructions

**Structure:**
- [ ] Clear sections with headings
- [ ] Logical organization (approach, methodology, examples)
- [ ] Uses Markdown formatting for readability

**Teaching Approach (for teaching/guide agents):**
- [ ] `❌ NEVER` section clearly defined
- [ ] `✅ ALWAYS` section clearly defined
- [ ] Emphasizes guidance over complete solutions
- [ ] Promotes learning and understanding
- [ ] Includes small pattern examples (2-3 lines max)

**Methodology:**
- [ ] Clear step-by-step process defined
- [ ] Follows gather→act→verify loop (from Anthropic best practices)
- [ ] Context gathering strategy specified
- [ ] Action execution approach defined
- [ ] Verification/feedback mechanism included

**Response Format:**
- [ ] Expected response structure documented
- [ ] Examples of good responses provided
- [ ] Tone and style guidelines included

**Integration (if applicable):**
- [ ] Skill invocation patterns documented
- [ ] Subagent delegation patterns documented
- [ ] Coordination protocols defined

**Examples:**
- [ ] At least one example interaction provided
- [ ] Examples demonstrate best practices
- [ ] Examples show expected behavior

### Content Quality

- [ ] Instructions are specific, not vague
- [ ] Avoids "altitude problem" (not too brittle, not too vague)
- [ ] Clear domain boundaries
- [ ] No ambiguity about responsibilities
- [ ] Sufficient context without being excessive

**Anthropic Best Practices:**
- [ ] Follows progressive disclosure (loads context as needed)
- [ ] Encourages just-in-time data loading
- [ ] Promotes agentic search over pre-loading
- [ ] Uses subagents for parallelization (if coordinator)
- [ ] Implements structured note-taking (if long-running)

### Security Considerations

- [ ] Agent instructions don't expose secrets
- [ ] No instructions to bypass security measures
- [ ] Sandboxing principles respected
- [ ] Appropriate file system access patterns
- [ ] Network access patterns appropriate

### Validation

- [ ] Ran `python scripts/validate-all.py`
- [ ] No validation errors
- [ ] Addressed all warnings
- [ ] Tested agent activation in Claude Code
- [ ] Agent activates appropriately
- [ ] Agent follows instructions correctly

### Documentation

- [ ] Purpose is clear from description
- [ ] Instructions are self-contained
- [ ] No external dependencies undocumented
- [ ] Usage examples provided
- [ ] Integration patterns documented

---

## Code Review Checklist

Use this checklist when reviewing skill or agent pull requests.

### General

- [ ] Code follows project style guidelines
- [ ] No debugging code or console.logs
- [ ] No commented-out code blocks
- [ ] No TODO comments without tracking issues
- [ ] Proper error handling implemented

### Skills

- [ ] All skill creation checklist items verified
- [ ] Operations are high-level and consolidated
- [ ] Error messages are actionable
- [ ] Performance targets met (< 200ms typical)
- [ ] Tests cover success and error cases
- [ ] Documentation is complete and accurate

### Agents

- [ ] All agent creation checklist items verified
- [ ] Tool selection is minimal and justified
- [ ] Activation mode is appropriate
- [ ] Teaching approach clearly defined
- [ ] No complete solution provision (for teaching agents)
- [ ] Clear methodology and examples

### Security

- [ ] No hardcoded secrets or credentials
- [ ] Input validation present
- [ ] No unsafe operations
- [ ] Follows principle of least privilege
- [ ] Sandboxing boundaries respected

### Documentation

- [ ] README is complete and accurate
- [ ] Code is well-commented
- [ ] Examples are runnable
- [ ] Best practices followed
- [ ] References to relevant docs

### Testing

- [ ] Tests exist and pass
- [ ] Edge cases covered
- [ ] Error paths tested
- [ ] Performance acceptable
- [ ] Manual testing completed

---

## Testing Checklist

### Unit Tests

- [ ] Test file exists in `tests/` directory
- [ ] Tests for all operations/functions
- [ ] Tests for successful execution paths
- [ ] Tests for error conditions
- [ ] Tests for edge cases:
  - [ ] Empty inputs
  - [ ] None/null inputs
  - [ ] Very long inputs
  - [ ] Special characters
  - [ ] Boundary conditions

### Integration Tests

- [ ] End-to-end workflow tested
- [ ] Multiple operations in sequence
- [ ] Data flows correctly between operations
- [ ] Error handling in workflows

### Performance Tests

- [ ] Operations meet performance targets:
  - [ ] Target: < 200ms
  - [ ] Maximum: < 2000ms
- [ ] Large input performance acceptable
- [ ] No memory leaks
- [ ] Duration tracking verified

### Agent Testing

- [ ] Agent activates correctly
- [ ] Agent follows instructions
- [ ] Agent uses tools appropriately
- [ ] Agent provides appropriate responses
- [ ] Agent handles errors gracefully

### Validation Testing

- [ ] `python scripts/validate-all.py` passes
- [ ] No validation errors
- [ ] Warnings addressed or documented

---

## Documentation Checklist

### README.md

- [ ] **Title and description** clear and accurate
- [ ] **Features list** comprehensive
- [ ] **Installation instructions** (if applicable)
- [ ] **Usage examples** for all operations
- [ ] **Python API examples** with code blocks
- [ ] **Agent invocation examples**
- [ ] **Error handling examples**
- [ ] **Performance characteristics** documented
- [ ] **Testing instructions** clear
- [ ] **Development guidelines** present
- [ ] **Contributing guidelines** present
- [ ] **License information** (if applicable)
- [ ] **Support/contact information**

### skill.md / Agent File

- [ ] **Metadata complete** and accurate
- [ ] **Operations documented** with descriptions
- [ ] **Dependencies listed** (if any)
- [ ] **Integration examples** provided
- [ ] **Error codes documented**
- [ ] **Changelog maintained**

### Code Comments

- [ ] **Module docstrings** present
- [ ] **Function docstrings** complete:
  - [ ] Description
  - [ ] Args with types
  - [ ] Returns with type
  - [ ] Raises (errors)
  - [ ] Examples
- [ ] **Complex logic** explained with comments
- [ ] **No misleading comments** (updated when code changes)

### Examples

- [ ] **All examples runnable**
- [ ] **Examples demonstrate best practices**
- [ ] **Examples cover common use cases**
- [ ] **Examples include error handling**

---

## Quick Reference

### Skill Creation Flow
```bash
1. python scripts/create-skill.py
2. Implement core logic in core/
3. Update operations.py
4. Write demo.py
5. Write tests
6. python scripts/validate-all.py
7. Test with agent
8. Commit
```

### Agent Creation Flow
```bash
1. python scripts/create-agent.py
2. Edit agent markdown file
3. Fill in placeholders
4. Add teaching approach
5. python scripts/validate-all.py
6. Test activation
7. Commit
```

### Validation Command
```bash
# Validate everything
python scripts/validate-all.py

# Verbose output
python scripts/validate-all.py --verbose

# Skills only
python scripts/validate-all.py --skills-only

# Agents only
python scripts/validate-all.py --agents-only

# JSON output for CI
python scripts/validate-all.py --json
```

---

## Common Mistakes to Avoid

### Skills

❌ **Don't:**
- Return low-level identifiers (UUIDs) instead of meaningful names
- Create separate tools for every API endpoint
- Skip error handling or use generic error messages
- Forget to track operation duration
- Pre-load all data instead of loading just-in-time
- Create brittle, hardcoded logic

✅ **Do:**
- Return semantically meaningful data
- Consolidate multi-step operations
- Provide actionable error messages with specific codes
- Always track and return duration
- Load data progressively as needed
- Keep operations flexible and reusable

### Agents

❌ **Don't:**
- Provide complete solutions (for teaching agents)
- Include excessive tools "just in case"
- Use vague, high-level instructions
- Skip teaching approach definition
- Use 'always' activation mode casually
- Forget to define clear domain boundaries

✅ **Do:**
- Guide and teach, don't solve
- Use minimal necessary tools
- Provide specific, structured instructions
- Define ❌ NEVER and ✅ ALWAYS rules
- Use 'manual' or 'proactive' activation appropriately
- Clearly define what agent does and doesn't do

---

## Resources

- **Best Practices Guide:** `docs/ANTHROPIC_BEST_PRACTICES.md`
- **Enforcement Plan:** `docs/BEST_PRACTICES_ENFORCEMENT_PLAN.md`
- **Skills System Overview:** `docs/SKILLS_SYSTEM_OVERVIEW.md`
- **Agent Skills Integration:** `docs/AGENT_SKILLS_INTEGRATION_GUIDE.md`
- **Scaffolding Tools:**
  - Create Skill: `python scripts/create-skill.py`
  - Create Agent: `python scripts/create-agent.py`
- **Validation:** `python scripts/validate-all.py`
- **Templates:**
  - Skill Template: `templates/skill-template/`
  - Agent Templates: Built into `scripts/create-agent.py`

---

**Version:** 1.0.0
**Last Updated:** 2025-11-10
**Maintained by:** Claude Code Team
