# Anthropic Best Practices for Skills and Agents
## Comprehensive Guide Based on Anthropic Engineering Research

**Last Updated:** 2025-11-10
**Sources:** Anthropic Engineering Blog Posts
**Purpose:** Guide creation of high-quality skills and agents

---

## Table of Contents
1. [Context Engineering Fundamentals](#context-engineering-fundamentals)
2. [Agent Skills Design](#agent-skills-design)
3. [Tool Architecture](#tool-architecture)
4. [Agent Architecture Patterns](#agent-architecture-patterns)
5. [Security and Sandboxing](#security-and-sandboxing)
6. [Code Execution with MCP](#code-execution-with-mcp)
7. [Development Workflow](#development-workflow)
8. [Testing and Verification](#testing-and-verification)

---

## Context Engineering Fundamentals

### The Core Principle
> **Context is a finite resource with diminishing returns.**

**Goal:** Find "the smallest set of high-signal tokens that maximize the likelihood of desired outcome."

### Context Rot Problem
- LLMs exhibit **context rot** — as context windows grow, recall accuracy decreases
- Due to architectural constraints in transformer-based attention mechanisms
- **Implication:** More context ≠ better performance

### The Altitude Problem
Balance between two failure modes:
- ❌ **Overly brittle**: Hardcoded complex logic that creates maintenance burden
- ❌ **Overly vague**: Insufficient guidance that assumes false shared understanding
- ✅ **Sweet spot**: Structured sections with clear organization

### Recommended Prompt Structure
```markdown
# Background Information
[Context about the domain]

# Instructions
[Clear step-by-step guidance]

# Tool Guidance
[How to use available tools]

# Output Descriptions
[Expected output format]
```

Use XML tagging or Markdown headers for organization.

---

## Agent Skills Design

### What Are Skills?
**Agent Skills** = Organized folders containing instructions, scripts, and resources that enable AI agents to perform specialized tasks.

### Three-Level Information Hierarchy (Progressive Disclosure)

1. **Metadata Level** ⚡️ (Always Loaded)
   - `SKILL.md` with `name` and `description` fields
   - Pre-loaded into system prompt
   - Used for skill discovery

2. **Core Content** 📖 (Loaded When Relevant)
   - Full `SKILL.md` details
   - Claude determines relevance
   - Contains main instructions

3. **Supplementary Files** 📚 (Dynamically Loaded)
   - Reference docs, forms, additional guidance
   - Loaded only when needed
   - Keeps context lean

**Key Insight:** "This design keeps context lean while allowing unbounded complexity through deferred loading."

### File Organization Best Practices

```
skill-name/
├── skill.md              # ✅ Core guidance with metadata
├── operations.py         # ✅ Executable operations
├── core/                 # ✅ Implementation modules
│   ├── module1.py
│   └── module2.py
├── reference.md          # 📖 Supplementary documentation
├── forms.md              # 📖 Templates and forms
└── scripts/              # 📖 Pre-written utilities
    └── helper.py
```

**Principles:**
- ✅ Central `SKILL.md` contains core guidance
- ✅ Referenced files compartmentalize specialized contexts
- ✅ Code scripts are both executable tools and documentation
- ✅ Context remains modular and token-efficient

### Development Guidelines

#### 1. Evaluation-First Approach
> "Identify capability gaps by running agents on representative tasks, then incrementally build skills addressing specific shortcomings."

**Process:**
1. Run agents on real tasks
2. Identify failure patterns
3. Build targeted skills
4. Iterate based on results

#### 2. Thoughtful Naming
> "Craft precise `name` and `description` fields—Claude uses these to determine skill relevance."

**Impact on Triggering:**
- Clear names → Better discovery
- Specific descriptions → More accurate activation
- Vague names → Missed opportunities

**Examples:**
```yaml
# ❌ Bad
name: helper
description: Does stuff with code

# ✅ Good
name: code-search
description: Intelligent code search with AST-based indexing
```

#### 3. Iterative Refinement
> "Collaborate with Claude to document successful patterns and failures within reusable skill components."

- Discover actual contextual needs (don't anticipate)
- Document what works and what doesn't
- Refine based on real usage patterns

#### 4. Security Considerations
⚠️ **CRITICAL SECURITY RULES:**
- Install skills only from trusted sources
- Thoroughly audit bundled files
- Review code dependencies
- Check external network connections
- Validate before deployment

---

## Tool Architecture

### Core Tool Design Principles

#### 1. Choose High-Impact Tools Strategically
> "More tools don't always lead to better outcomes."

**Focus on:**
- ✅ Tools matching agent evaluation tasks
- ✅ Consolidate multi-step operations
- ✅ Purposeful, not comprehensive

**Example:**
```python
# ❌ Bad: Separate low-level tools
list_users(calendar_id)
check_availability(user_id, time)
create_event(calendar_id, time, attendees)

# ✅ Good: Consolidated high-level tool
schedule_event(attendees, duration, preferences)
# Handles availability checking internally
```

#### 2. Self-Contained with Minimal Overlap
- Each tool has clear, distinct purpose
- No ambiguity about which tool to use
- **Test:** "If humans can't say which tool to use, neither can agents"

#### 3. Clear About Intended Use

**Descriptive Parameters:**
```python
# ❌ Bad: Ambiguous
def search(user, query):
    ...

# ✅ Good: Unambiguous
def search(user_id: str, query: str):
    ...
```

#### 4. Token-Efficient Outputs
- Return high-signal information
- Avoid low-level identifiers (UUIDs)
- Use semantically meaningful fields

```python
# ❌ Bad: Low signal
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "ref": "usr_abc123"
}

# ✅ Good: High signal
{
    "name": "config.py",
    "file_type": "python",
    "last_modified": "2025-11-10"
}
```

### Parameter Handling Best Practices

#### 1. Unambiguous Parameter Names
```python
# ❌ Bad
def get_item(user, item):
    ...

# ✅ Good
def get_item(user_id: str, item_name: str):
    ...
```

#### 2. Enable Response Format Control
```python
def search_code(
    query: str,
    response_format: Literal["concise", "detailed"] = "concise"
) -> OperationResult:
    """
    Control verbosity based on agent needs.
    - concise: For quick checks
    - detailed: For downstream tool calls
    """
    ...
```

#### 3. Implement Smart Defaults
> "Implement some combination of pagination, range selection, filtering, and/or truncation with sensible default parameter values."

```python
def list_files(
    directory: str,
    limit: int = 100,        # ✅ Sensible default
    offset: int = 0,         # ✅ Enable pagination
    file_types: List[str] = None,  # ✅ Optional filtering
) -> OperationResult:
    ...
```

### Error Handling & Feedback

#### 1. Provide Actionable Error Messages
> "Prompt-engineer your error responses to clearly communicate specific and actionable improvements."

```python
# ❌ Bad
return OperationResult(
    success=False,
    error="Invalid input",
    error_code="ERROR_400"
)

# ✅ Good
return OperationResult(
    success=False,
    error="Parameter 'user_id' must be a valid UUID. Received: 'abc123'. Use search_users() to find valid user IDs.",
    error_code="VALIDATION_ERROR"
)
```

#### 2. Return Meaningful Context
Prioritize information that directly informs agent decisions:
- ✅ Names, types, descriptions
- ✅ Relationships and hierarchies
- ✅ Actionable metadata
- ❌ Internal IDs, raw UUIDs
- ❌ System-level details

### Thoughtful Namespacing

> "Namespacing (grouping related tools under common prefixes) helps agents select correct tools."

**Service-Level Namespacing:**
```python
asana_search_tasks()
asana_create_task()
jira_search_issues()
jira_create_issue()
```

**Resource-Level Namespacing:**
```python
asana_projects_search()
asana_projects_create()
asana_users_search()
asana_users_list()
```

---

## Agent Architecture Patterns

### Core Feedback Loop
> **"gather context → take action → verify work → repeat"**

This iterative approach enables agents to self-correct and improve continuously.

### Context Gathering Strategies

#### 1. Agentic Search & File System
**Use folder structures as context engineering.**

When encountering large files:
```bash
# ✅ Agents use bash utilities for selective loading
grep "pattern" large_file.txt
tail -n 100 log.txt
find . -name "*.py" -type f
```

**Advantages:**
- More accurate than semantic search
- Leverages file system organization
- Easy to maintain

**When to use:** Start here by default

#### 2. Semantic Search
**Generally faster but less accurate.**

**When to use:** Add only if performance improvements justify the tradeoff

**Implementation:** Requires vector embeddings, index maintenance

#### 3. Subagents
**Enable parallelization and context isolation.**

**Pattern:**
```python
# Main agent spawns subagents
subagent_results = await asyncio.gather(
    analyze_module_1(),
    analyze_module_2(),
    analyze_module_3()
)

# Subagents return condensed summaries (1,000-2,000 tokens)
summary = synthesize_results(subagent_results)
```

**Benefits:**
- ✅ Isolated context windows
- ✅ Parallel processing
- ✅ Return only relevant information
- ✅ Ideal for large datasets

#### 4. Context Compaction
**Automatic conversation summarization.**

**When:** Approaching context limits

**What:** Preserve architectural decisions, discard redundant outputs

**How:** SDK handles automatically

#### 5. Structured Note-Taking
**Persistent memory files outside context windows.**

**Pattern:**
```python
# Agent maintains notes file
with open(".agent_notes.md", "a") as f:
    f.write(f"## Decision: {decision}\n")
    f.write(f"Rationale: {rationale}\n\n")

# Load summary when needed (not entire history)
```

**Benefits:**
- ✅ Multi-hour task coherence
- ✅ Don't load everything simultaneously
- ✅ Persistent across sessions

### Action Execution Methods

#### 1. Tools (Primary Actions)
> "Design them as primary, frequent actions."

**Characteristics:**
- Appear prominently in Claude's context
- Guide decision-making
- Prioritize clarity and specificity

**When to use:** Repeated, structured operations

#### 2. Bash & Scripts
**Flexible computer access for varied tasks.**

**Examples:**
- PDF processing
- Data transformation
- File operations
- System commands

**When to use:** Exploratory or one-off operations

#### 3. Code Generation
> "Agents excel here; code is precise, composable, and reusable."

**Ideal for:**
- Complex operations requiring reliability
- Reusable logic
- Precise specifications

#### 4. Model Context Protocol (MCP)
**Standardized integrations with authentication.**

**Benefits:**
- Handles API calls automatically
- Seamless service connections
- No custom integration code needed

**Supported:** Slack, GitHub, Asana, etc.

---

## Long-Horizon Task Strategies

### Progressive Disclosure
> "Let agents incrementally discover context through exploration."

**Use as signals:**
- File metadata
- Naming conventions
- Timestamps
- Directory structure

### Just-in-Time Strategy
> "Maintain lightweight identifiers and dynamically load data via tools."

```python
# ❌ Bad: Pre-load everything
all_files = load_entire_project()

# ✅ Good: Load on demand
file_list = get_file_paths()  # Lightweight
for file_path in relevant_files:
    content = read_file(file_path)  # JIT loading
```

### Hybrid Model
**Balance speed with autonomy.**

- ✅ Retrieve some data upfront for speed
- ✅ Preserve autonomy for runtime exploration
- ✅ Let agents decide what to load

---

## Security and Sandboxing

### Core Sandboxing Boundaries

#### 1. Filesystem Isolation
> "Claude can only access or modify specific directories."

**Prevents:**
- Modifying sensitive system files
- Accessing user home directories
- Escaping project boundaries

#### 2. Network Isolation
> "Claude can only connect to approved servers."

**Prevents:**
- Data exfiltration
- Malware downloads
- Unauthorized connections

⚠️ **CRITICAL:** Both mechanisms are essential—filesystem isolation alone allows escape vectors

### Safety Impact
> Internal testing showed sandboxing "safely reduces permission prompts by 84%."

**Benefits:**
- Reduces approval fatigue
- Maintains protective boundaries
- Improves security paradoxically by reducing decision burden

### Implementation
- **Linux:** bubblewrap
- **macOS:** seatbelt
- **Enforcement:** OS-level kernel primitives

### Credential Protection Strategy

**For Claude Code on the web:**
- Credentials remain outside sandbox
- Custom proxy handles git interactions
- Validates tokens, branches, repository destinations
- Transparently forwards to GitHub

### Key Security Principle
> "Even successful prompt injection remains isolated."

**Cannot:**
- Steal SSH keys
- Establish unauthorized command channels
- Access credentials
- Break out of sandbox

---

## Code Execution with MCP

### Traditional Tool Integration Problems

#### 1. Token Consumption Overhead
> "Loading all tool definitions upfront means agents must process hundreds of thousands of tokens before reading a request."

**Problem:** With thousands of tools, context is exhausted before work begins

#### 2. Intermediate Result Bloat
> "Data flows through the model multiple times."

**Example:** 2-hour meeting transcript consumes 50,000+ tokens when passed between tool calls

### Code Execution Solution

**Present MCP servers as code APIs.**

**Benefits:**

#### 1. On-Demand Loading
```python
# Agent discovers and loads tools only when needed
from mcp_server import search_meetings

# Definition loaded just-in-time
results = search_meetings(query="budget discussion")
```

#### 2. Local Data Processing
```python
# Filter, transform, aggregate in execution environment
meetings = search_meetings(last_n_days=30)
budget_meetings = [m for m in meetings if "budget" in m.topic]
summary = summarize_locally(budget_meetings)

# Return only summary (not raw data)
return summary
```

#### 3. Dramatic Efficiency Gains
**Case Study:** Reduced token usage from 150,000 to 2,000 (98.7% reduction)

### Additional Benefits

#### Privacy & Security
> "Intermediate results stay in the execution environment by default."

- Prevents sensitive data from entering context
- Tokenization can mask PII automatically
- Compliance-friendly

#### State Persistence
```python
# Save progress to files
with open("analysis_state.json", "w") as f:
    json.dump(progress, f)

# Resume later
if os.path.exists("analysis_state.json"):
    progress = json.load(open("analysis_state.json"))
```

**Enables:**
- Resumable workflows
- Reusable skills
- Long-running tasks

#### Control Flow Efficiency
**Execute locally:**
- Loops
- Conditionals
- Error handling
- Complex logic

**No repeated model iterations needed.**

### Implementation Considerations

⚠️ **Complexity trade-offs:**
- Requires secure sandboxing
- Resource limits needed
- Monitoring infrastructure required

**Decision:** Weigh benefits against operational costs

---

## Development Workflow

### Setup & Customization

#### CLAUDE.md Files
> "There's no required format for CLAUDE.md files. We recommend keeping them concise and human-readable."

**Locations:**
- Repo root: `./CLAUDE.md`
- Parent directories: `../CLAUDE.md`
- Home folder: `~/.claude/CLAUDE.md`

**Usage:**
```markdown
# Project Context

This is a Python project using FastAPI.

## Important Commands

- Run tests: `pytest`
- Start server: `python -m app.main`

## Code Style

IMPORTANT: Always use type hints.
YOU MUST run Black before committing.
```

#### Tuning Instructions
> "Add emphasis with 'IMPORTANT' or 'YOU MUST' to improve adherence."

**Treat as living documentation:**
- Regularly refine instructions
- Add learnings from mistakes
- Document project patterns

#### Permission Management
```bash
# View current permissions
/permissions

# Customize allowed tools
claude --allowedTools Read,Write,Bash
```

### Effective Workflows

#### 1. Explore-Plan-Code-Commit
```bash
# 1. Explore: Read files first
"Show me the current authentication system"

# 2. Plan: Create detailed plan
"Create a plan to add OAuth support"

# 3. Code: Implement
"Implement the OAuth flow we planned"

# 4. Commit: Context-aware messages
"Commit these changes with an appropriate message"
```

#### 2. Test-Driven Development
> "Write tests first, confirm failures, then iterate code until all tests pass."

**Process:**
1. Write failing test
2. Confirm it fails
3. Implement feature
4. Iterate until green
5. Refactor

**Benefits:**
- Clear targets for iteration
- Prevents regressions
- Documents expected behavior

#### 3. Visual Development
> "Like humans, Claude's outputs tend to improve significantly with iteration."

**Provide:**
- Screenshots (cmd+ctrl+shift+4 on macOS)
- Design mocks
- Reference images
- Visual feedback

**Verify with screenshots:**
```python
# Generate UI
create_dashboard()

# Take screenshot
screenshot = capture_screen()

# Claude evaluates
"Does this match the design? Check layout, styling, and responsiveness."
```

#### 4. Codebase Learning
> "Ask Claude questions like you would a colleague."

**Examples:**
- "How does logging work in this project?"
- "Where are the API patterns defined?"
- "Show me examples of database queries"

**Claude will search proactively.**

### Optimization Techniques

#### 1. Be Specific
> "Detailed instructions significantly improve first-attempt success."

**Specify:**
- ✅ Exact filenames
- ✅ Edge cases
- ✅ Patterns to follow
- ✅ Expected output format

#### 2. Provide Context Visually
- Paste screenshots
- Drag images into prompts
- Reference file paths for visual assets

#### 3. File References
- Use tab-completion
- Mention specific files and folders
- Provide URLs when relevant

#### 4. Early Course Correction
> "Ask Claude to plan before coding. Use Escape to interrupt."

**Process:**
1. Request plan first
2. Review plan
3. Correct if needed
4. Then implement

#### 5. Context Management
```bash
# Reset context between tasks
/clear
```

**Benefits:**
- Maintain performance
- Prevent context pollution
- Start fresh

#### 6. Checklists for Complex Work
> "Have Claude create markdown checklists for large migrations or numerous fixes."

**Example:**
```markdown
## Migration Checklist

- [ ] Update database schema
- [ ] Migrate user data
- [ ] Update API endpoints
- [ ] Update frontend components
- [ ] Run integration tests
- [ ] Deploy to staging
```

### Multi-Claude Workflows

#### 1. Parallel Verification
**Have separate Claude instances:**
- One writes code
- Another reviews independently

**Benefits:** Catch more issues

#### 2. Git Worktrees
```bash
# Create worktrees for parallel work
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b

# Run Claude instance in each
cd ../project-feature-a && claude
cd ../project-feature-b && claude
```

#### 3. Headless Mode Automation
```bash
# CI integration
claude -p "Run all tests and report failures" --output-format stream-json

# Issue triage
claude -p "Analyze new issues and label them" --output-format stream-json

# Automated linting
claude -p "Fix all linting errors" --output-format stream-json
```

---

## Testing and Verification

### Work Verification Approaches

#### 1. Rules-Based Feedback
> "Provide clearly defined output rules and explain which ones failed."

**Example: Code Linting**
```python
# TypeScript with linting provides more feedback layers
# than raw JavaScript
rules = {
    "no-unused-vars": "error",
    "prefer-const": "error",
    "no-console": "warn"
}

# Explain failures
"Failed rules:
- no-unused-vars: Variable 'x' is declared but never used (line 42)
- prefer-const: Variable 'y' is never reassigned, use const (line 50)"
```

#### 2. Visual Feedback
**For UI tasks, screenshot generated outputs.**

**Assess:**
- Layout correctness
- Styling accuracy
- Content hierarchy
- Responsiveness
- Accessibility

**Pattern:**
```python
# 1. Generate output
render_component()

# 2. Capture screenshot
screenshot = take_screenshot()

# 3. Return for model evaluation
"Evaluate this screenshot against the design requirements"
```

#### 3. LLM-as-Judge
**Have another LLM evaluate outputs.**

**When to use:**
- Fuzzy criteria (style, tone, creativity)
- When any performance boost justifies cost

**Trade-offs:**
- ❌ Less robust
- ❌ Higher latency
- ❌ Additional cost
- ✅ Handles subjective criteria

### Evaluation Best Practices

#### Run Systematic Evaluations
> "Building an evaluation allows you to systematically measure the performance of your tools."

**Process:**
1. Create realistic, multi-step tasks
2. Ground in actual workflows
3. Run systematically
4. Measure performance

#### Examine Failures Carefully

**Critical questions:**
- Is missing context causing misunderstandings?
  → Restructure search APIs
- Can formal rules catch repeated failures?
  → Add validation
- Would additional tools enable different approaches?
  → Add targeted tools
- Does performance vary with new features?
  → Build representative test sets

#### Iterate With Agent Collaboration
> "Use Claude Code to analyze evaluation transcripts and refactor tools."

**Process:**
1. Run evaluations
2. Analyze transcripts with Claude
3. Refactor for consistency
4. Ensure descriptions match implementations
5. Repeat

---

## Key Principles Summary

### Context Management
✅ **DO:**
- Find smallest set of high-signal tokens
- Use progressive disclosure
- Load data just-in-time
- Leverage file system structure
- Use subagents for isolation

❌ **DON'T:**
- Pre-load everything
- Assume more context = better
- Keep all data in context
- Ignore context rot

### Tool Design
✅ **DO:**
- Choose high-impact tools strategically
- Consolidate multi-step operations
- Use unambiguous parameter names
- Provide actionable error messages
- Return semantically meaningful data
- Implement smart defaults

❌ **DON'T:**
- Create tools for every API endpoint
- Use ambiguous parameters
- Return low-level identifiers
- Give opaque error codes
- Assume more tools = better

### Agent Architecture
✅ **DO:**
- Follow gather→act→verify→repeat loop
- Start with agentic search
- Use subagents for parallelization
- Enable code execution for efficiency
- Provide visual feedback
- Test systematically

❌ **DON'T:**
- Skip verification steps
- Prematurely optimize with semantic search
- Keep everything in main agent context
- Rely solely on tool calls
- Skip visual validation
- Trust without testing

### Security
✅ **DO:**
- Implement filesystem isolation
- Implement network isolation
- Keep credentials outside sandbox
- Audit skills before installation
- Use OS-level enforcement
- Test injection scenarios

❌ **DON'T:**
- Rely on only one isolation method
- Store credentials in sandbox
- Trust unauthenticated skills
- Skip security audits
- Use application-level restrictions only
- Assume prompts prevent attacks

### Development Workflow
✅ **DO:**
- Be specific in instructions
- Provide visual context
- Use checklists for complex work
- Clear context between tasks
- Write tests first
- Iterate based on feedback
- Document in CLAUDE.md

❌ **DON'T:**
- Give vague instructions
- Skip visual feedback
- Let context accumulate
- Write code before tests
- Ignore evaluation results
- Leave patterns undocumented

---

## Applying These Principles to Skills and Agents

### For Skills

**Structure:**
```yaml
# skill.md frontmatter
---
name: descriptive-kebab-case              # ✅ Precise naming
description: Specific one-line purpose    # ✅ Clear description
operations:
  high_level_operation: "Consolidated purpose"  # ✅ High-impact
---
```

**Operations:**
```python
def operation(
    user_id: str,                    # ✅ Unambiguous parameters
    response_format: str = "concise",    # ✅ Smart defaults
    limit: int = 100                 # ✅ Pagination support
) -> OperationResult:
    """Clear description."""         # ✅ Documentation

    try:
        result = process()
        return OperationResult(
            success=True,
            data={"name": "file.py"},    # ✅ Semantic data
            duration=time.time() - start
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error="Specific actionable message",  # ✅ Actionable errors
            error_code="VALIDATION_ERROR"
        )
```

### For Agents

**Metadata:**
```yaml
---
name: specific-purpose-agent              # ✅ Clear naming
description: Precise role and approach    # ✅ 20-300 chars
tools:                                    # ✅ Minimal necessary
  - Read
  - Write
activation: manual                        # ✅ Appropriate mode
---
```

**Instructions:**
```markdown
## Teaching Approach

❌ NEVER:
- Write complete solutions              # ✅ Clear boundaries
- Skip explanation                      # ✅ Explicit rules

✅ ALWAYS:
- Follow gather→act→verify loop        # ✅ Methodology
- Provide visual feedback               # ✅ Best practices
- Use checklists for complex tasks      # ✅ Techniques

## Verification

- Screenshot outputs for visual tasks   # ✅ Verification
- Run tests to confirm behavior         # ✅ Testing
- Iterate based on feedback             # ✅ Improvement
```

---

## References

1. [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
2. [Equipping Agents for the Real World with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
3. [Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
4. [Building Agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
5. [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
6. [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
7. [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

---

**Version:** 1.0.0
**Maintained by:** Claude Code Team
**Usage:** Reference this document when creating new skills and agents
