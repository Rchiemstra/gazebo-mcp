# Complete Guide to Claude Code Sub-Agents

A comprehensive guide to building, configuring, and orchestrating specialized AI agents in Claude Code.

---

## Table of Contents

1. [Introduction](#introduction)
2. [What Are Sub-Agents?](#what-are-sub-agents)
3. [Why Use Sub-Agents?](#why-use-sub-agents)
4. [Agent Philosophy & Design](#agent-philosophy--design)
5. [Configuration Deep Dive](#configuration-deep-dive)
6. [Building Effective Agents](#building-effective-agents)
7. [Agent Coordination Patterns](#agent-coordination-patterns)
8. [Commands & Workflows](#commands--workflows)
9. [Best Practices](#best-practices)
10. [Advanced Usage Patterns](#advanced-usage-patterns)
11. [Real-World Examples](#real-world-examples)
12. [Team Collaboration](#team-collaboration)
13. [Troubleshooting](#troubleshooting)
14. [Quick Reference](#quick-reference)

---

## Introduction

Claude Code supports a powerful **sub-agent system** that allows you to create specialized AI assistants for specific domains, tasks, or teaching roles. Unlike the main Claude Code assistant that handles general programming tasks, sub-agents are focused experts with:

- **Independent context**: Fresh context window for each invocation
- **Specialized knowledge**: Tailored expertise in specific domains
- **Custom tool access**: Controlled permissions for different capabilities
- **Persistent identity**: Consistent behavior across sessions

This guide covers both **teaching-focused agents** (guiding users to learn) and **implementation-focused agents** (producing code/solutions), showing you how to build effective agents for any purpose.

---

## What Are Sub-Agents?

### Definition

A **sub-agent** (or simply "agent") is a specialized instance of Claude configured with:

1. **Identity**: A role, expertise area, and mission
2. **Instructions**: Detailed behavioral guidelines
3. **Tool Access**: Specific permissions for reading, editing, executing
4. **Philosophy**: Teaching approach or implementation strategy

### How They Differ from Main Assistant

| Aspect | Main Assistant | Sub-Agent |
|--------|---------------|-----------|
| **Context** | Shared across conversation | Independent per invocation |
| **Scope** | General-purpose | Specialized domain |
| **Activation** | Always active | Invoked when needed |
| **Tool Access** | Full access | Restricted by configuration |
| **Memory** | Remembers conversation | Fresh start each time |

### When to Use Sub-Agents

✅ **Use sub-agents when:**
- Task requires specialized expertise
- Need focused approach without distraction
- Want consistent methodology across sessions
- Teaching/guiding requires domain-specific pedagogy
- Context management is important (isolate complex work)
- Multiple specialists should coordinate

❌ **Don't use sub-agents when:**
- Simple one-off tasks
- No specialized knowledge needed
- Quick file edits or reads
- General Q&A that doesn't require expertise

---

## Why Use Sub-Agents?

### 1. Context Preservation

**Problem**: Main assistant's context fills up with code, conversation, files
**Solution**: Sub-agents start fresh, focusing only on their specific task

**Example**:
```
Main Assistant: [10,000 tokens of prior conversation]
→ Invokes debugging-detective sub-agent
Debugging Detective: [Fresh context, focused only on the bug]
→ Returns findings to main assistant
```

### 2. Specialized Performance

**Problem**: Generalist approach may miss domain-specific patterns
**Solution**: Specialists apply deep expertise consistently

**Example Specializations**:
- **Teaching**: ros2-learning-mentor knows ROS2 pedagogy
- **Design**: code-architecture-mentor knows pattern trade-offs
- **Hardware**: jetank-hardware-specialist knows safety-first approaches
- **Testing**: testing-specialist knows TDD methodology

### 3. Consistency

**Problem**: General assistant may vary approach across sessions
**Solution**: Agents maintain consistent methodology

**Example**:
- `debugging-detective` always uses same systematic 5-step process
- `git-workflow-expert` always explains Git mental models first
- `code-architecture-mentor` always discusses trade-offs before patterns

### 4. Scalability

**Problem**: One assistant handling everything becomes inefficient
**Solution**: Coordinate multiple specialists working in parallel

**Example Workflow**:
```
User: "Help me build autonomous navigation"
→ Main coordinates:
  ├─ plan-generation-mentor (creates learning plan)
  ├─ ros2-learning-mentor (teaches ROS2 concepts)
  ├─ robotics-vision-navigator (teaches SLAM)
  └─ code-architecture-mentor (teaches system design)
```

### 5. Tool Access Control

**Problem**: Not all tasks should have full system access
**Solution**: Agents have restricted tool permissions

**Example**:
- **Learning agents**: Read-only access (teach, don't implement)
- **Review agents**: Read + analysis tools only
- **Implementation agents**: Full read/write/execute access

---

## Agent Philosophy & Design

### Teaching vs. Implementation Agents

#### Teaching-Focused Agents

**Purpose**: Guide users to learn and understand concepts

**Characteristics**:
- Ask questions instead of providing answers
- Explain concepts before code
- Verify understanding at checkpoints
- Provide patterns, not complete solutions
- Encourage exploration and experimentation

**Example Teaching Agent**: `ros2-learning-mentor`
```markdown
## TEACHING RULES (NEVER BREAK THESE)
- ❌ NEVER write complete working systems
- ❌ NEVER provide full implementations
- ❌ NEVER give copy-paste ready code
- ✅ ALWAYS explain concepts first
- ✅ ALWAYS guide through design thinking
- ✅ ALWAYS use small code snippets (2-5 lines) as examples only
- ✅ ALWAYS verify understanding before advancing
```

#### Implementation-Focused Agents

**Purpose**: Produce working code, systems, or solutions

**Characteristics**:
- Generate complete implementations
- Focus on best practices and quality
- Provide production-ready code
- Include tests and documentation
- Optimize for maintainability

**Example Implementation Agent**: `new-node` (ROS2 production)
```markdown
## Implementation Mission
Create production-ready ROS2 nodes with:
- Complete working code
- Proper package structure
- Unit tests included
- Documentation generated
- Best practices applied
```

### Hybrid Agents

Some agents blend both approaches:

**Example**: `code-architecture-mentor`
- **Teaching**: Discusses pattern trade-offs, asks design questions
- **Implementation**: Shows reference implementations after understanding verified
- **Balance**: Guides thinking, then provides tools to implement

### Agent Design Principles

#### 1. Single Responsibility

Each agent should have **one clear domain** of expertise.

**Good Examples**:
- ✅ `ros2-learning-mentor` - ROS2 concepts and architecture
- ✅ `python-best-practices` - Python code quality and patterns
- ✅ `debugging-detective` - Systematic bug investigation

**Bad Examples**:
- ❌ `general-coding-helper` - Too broad, overlaps with main assistant
- ❌ `ros2-and-python-expert` - Two domains, split into two agents
- ❌ `everything-robotics` - Unfocused, should be multiple specialists

#### 2. Clear Activation Conditions

Define **when** the agent should be invoked.

**Good Activation Triggers**:
```markdown
**Invoke me when:**
- User asks about ROS2 transform concepts
- User needs to design node architecture
- User is learning message passing patterns
```

**Bad Activation Triggers**:
```markdown
**Invoke me when:**
- User has any question (too broad)
- Sometimes when coding (vague)
```

#### 3. Well-Defined Scope

Specify what the agent **will** and **won't** do.

**Good Scope Definition**:
```markdown
**I will:**
- Explain computer vision algorithms conceptually
- Guide through SLAM design thinking
- Help choose appropriate CV libraries
- Show small example snippets (2-5 lines)

**I won't:**
- Write complete vision systems
- Provide full SLAM implementations
- Make all design decisions for you
```

#### 4. Consistent Methodology

Use the same approach every time.

**Example - debugging-detective**:
```markdown
## My 5-Step Process (Always Follow)
1. **Understand**: Reproduce the bug
2. **Isolate**: Narrow down the cause
3. **Investigate**: Use scientific method
4. **Fix**: Address root cause
5. **Verify**: Ensure fix works
```

#### 5. Clear Output Format

Define how results are returned to the main assistant or user.

**Example Formats**:
- **Teaching Session**: Discussion transcript + understanding assessment
- **Code Review**: Findings list + severity ratings + suggestions
- **Implementation**: Working code + tests + documentation
- **Planning**: Structured plan document with phases and tasks

---

## Configuration Deep Dive

### File Structure

Agents are defined in markdown files with YAML frontmatter:

```
claude_code/
├── agents/                      # Agent definitions
│   ├── my-agent.md             # Agent definition file
│   └── another-agent.md
├── commands/                    # Slash command definitions
│   └── my-command.md
└── plans/                       # Generated artifacts
    └── learning-plans.md
```

### Agent File Anatomy

**File**: `agents/my-specialist.md`

```markdown
---
name: my-specialist
description: Brief description of what this agent does
tools:
  - Read
  - Grep
activation: proactive
---

You are the **my-specialist** agent, an expert in [domain].

## Your Mission
[Clear statement of purpose]

## Your Expertise
- [Area 1]
- [Area 2]
- [Area 3]

## Teaching Philosophy / Implementation Approach
[How you operate]

## Process
[Step-by-step methodology]

## [Additional Sections]
[Specific guidelines, examples, etc.]
```

### YAML Frontmatter Options

#### `name` (required)
Unique identifier for the agent.

```yaml
name: ros2-learning-mentor
```

**Best Practices**:
- Use kebab-case
- Be descriptive but concise
- Avoid generic names like "helper" or "assistant"

#### `description` (required)
Brief summary of agent's purpose (1-2 sentences).

```yaml
description: Teaches ROS2 concepts, node architecture, and message passing patterns through guided discovery
```

**Best Practices**:
- Focus on *what* the agent does
- Include primary domain/specialty
- Mention teaching vs. implementation approach

#### `tools` (optional)
List of tools the agent can use.

**Available Tools**:
- `Read` - Read files
- `Write` - Create new files
- `Edit` - Modify existing files
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `Bash` - Execute shell commands
- `Task` - Invoke other agents

**Examples**:

Teaching agent (read-only):
```yaml
tools:
  - Read
  - Glob
  - Grep
```

Implementation agent (full access):
```yaml
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

Coordinator agent (can delegate):
```yaml
tools:
  - Read
  - Glob
  - Task
```

#### `activation` (optional)
When the agent should be invoked.

**Options**:
- `proactive` - Main assistant should invoke automatically when appropriate
- `manual` - Only invoke when explicitly requested
- `always` - Consider for every task (use sparingly!)

**Examples**:

Proactive teaching:
```yaml
activation: proactive
```

Manual invocation only:
```yaml
activation: manual
```

### Complete Configuration Example

**File**: `agents/code-architecture-mentor.md`

```markdown
---
name: code-architecture-mentor
description: Teaches software design patterns, SOLID principles, and architectural decision-making through Socratic questioning and trade-off analysis
tools:
  - Read
  - Glob
  - Grep
  - Edit
activation: proactive
---

You are the **code-architecture-mentor**, an expert software architect specializing in teaching design patterns and architectural thinking.

## Your Mission
Guide students to understand when and why to use specific design patterns, focusing on trade-offs and decision-making rather than just pattern mechanics.

## Teaching Philosophy
- ❌ NEVER provide complete pattern implementations upfront
- ❌ NEVER make architectural decisions for the student
- ✅ ALWAYS discuss trade-offs before suggesting patterns
- ✅ ALWAYS use Socratic questioning to develop thinking
- ✅ ALWAYS provide robotics-relevant examples

## Your Expertise
- 10 core design patterns (Factory, Strategy, Observer, etc.)
- SOLID principles application
- Architectural trade-off analysis
- Pattern selection for robotics systems
- Anti-pattern recognition

## Process
### 1. Understand the Problem
Ask about:
- What problem are you trying to solve?
- What are the requirements?
- What might change in the future?

### 2. Guide Pattern Selection
Discuss:
- What patterns might apply?
- What are the trade-offs of each?
- Why might one be better than another?

### 3. Teach the Pattern
- Explain core concept
- Show structure (not full implementation)
- Discuss when to use / when not to use
- Provide small example snippets

### 4. Verify Understanding
- Can you explain when you'd use this pattern?
- What are the downsides?
- How would you apply it to your project?

[Continue with detailed pattern teaching sections...]
```

---

## Building Effective Agents

### Step 1: Define the Domain

Start by clearly identifying the agent's area of expertise.

**Questions to Answer**:
- What specific knowledge does this agent have?
- What problems does it solve?
- What related domains should it NOT handle?

**Example - Robotics Vision Navigator**:
```markdown
## Domain: Computer Vision & Navigation

**I Handle**:
- Computer vision algorithms (detection, tracking, segmentation)
- SLAM concepts and approaches
- Path planning algorithms
- Sensor fusion for navigation

**I Don't Handle**:
- Hardware setup (→ jetank-hardware-specialist)
- ROS2 architecture (→ ros2-learning-mentor)
- General Python code quality (→ python-best-practices)
```

### Step 2: Choose Teaching vs. Implementation

Decide on the agent's primary approach.

**Teaching Agent Template**:
```markdown
## TEACHING RULES (NEVER BREAK THESE)
- ❌ NEVER write complete [systems/implementations]
- ❌ NEVER provide copy-paste ready code
- ❌ NEVER make design decisions for the student
- ✅ ALWAYS explain concepts first
- ✅ ALWAYS guide through design thinking
- ✅ ALWAYS verify understanding
- ✅ ALWAYS use small snippets (2-5 lines) as examples only

## Teaching Process
1. **Understand Current Knowledge**: Assess what they know
2. **Introduce Concept**: Explain fundamentals
3. **Guide Design**: Ask questions, don't provide answers
4. **Verify Understanding**: Check comprehension before proceeding
5. **Encourage Exploration**: Suggest experiments and learning tasks
```

**Implementation Agent Template**:
```markdown
## IMPLEMENTATION APPROACH
- ✅ Generate complete, working code
- ✅ Follow best practices and patterns
- ✅ Include error handling and edge cases
- ✅ Provide tests and documentation
- ✅ Optimize for maintainability

## Implementation Process
1. **Analyze Requirements**: Understand what needs to be built
2. **Design Solution**: Plan architecture and components
3. **Implement Code**: Write production-ready implementation
4. **Add Tests**: Ensure code is tested
5. **Document**: Provide clear documentation
```

### Step 3: Define the Process

Create a consistent methodology the agent always follows.

**Good Process Example - Debugging Detective**:
```markdown
## My 5-Step Debugging Process (Always Follow)

### Step 1: Understand & Reproduce
- What is the expected behavior?
- What is the actual behavior?
- Can we reproduce it consistently?
- What are the reproduction steps?

### Step 2: Isolate the Problem
- What component/module is involved?
- What was the last working state?
- What changed since then?
- Can we narrow down the scope?

### Step 3: Investigate Root Cause
- What does the code do at the failure point?
- What are the variable values?
- What does logging/debugging reveal?
- What are possible causes?

### Step 4: Develop Fix
- What is the root cause?
- What are potential solutions?
- What are the trade-offs?
- Which solution is best? Why?

### Step 5: Verify & Prevent
- Does the fix work?
- Are there other instances of this bug?
- How can we prevent this in the future?
- Should we add tests?
```

### Step 4: Add Examples and Templates

Provide concrete examples of interactions.

**Example - Teaching Interaction**:
```markdown
## Example Teaching Session

**Student**: "How do I create a ROS2 node?"

**ros2-learning-mentor**:
Great question! Before we create a node, let's make sure we understand what a node is.

🤔 **Questions for you**:
1. What do you think a "node" is in ROS2?
2. What would you want your node to do?
3. How do you think nodes communicate with each other?

Take a moment to think about these, then share your thoughts!

---

**Student**: "A node is like a program that does something, and nodes talk through topics?"

**ros2-learning-mentor**:
Excellent! You've got the core concepts! Let me build on that understanding...

[Continues teaching conversation...]
```

### Step 5: Define Coordination

Specify how the agent works with others.

**Coordination Examples**:
```markdown
## Coordination with Other Agents

**I work with**:
- **ros2-learning-mentor**: I teach vision algorithms; they teach ROS2 integration
- **code-architecture-mentor**: I explain CV algorithms; they help structure the code
- **python-best-practices**: I focus on algorithms; they ensure code quality

**Hand-off points**:
- When student understands vision concepts → ros2-learning-mentor for node creation
- When design patterns needed → code-architecture-mentor for architecture
- When implementation quality matters → python-best-practices for code review

**Example Coordination**:
Student learning object detection:
1. **Me**: Teach detection algorithms (YOLO, SSD concepts)
2. **ros2-learning-mentor**: Guide ROS2 node structure for detection
3. **code-architecture-mentor**: Help design multi-algorithm system
4. **python-best-practices**: Review final implementation quality
```

### Step 6: Test and Iterate

**Testing Checklist**:
- [ ] Can the agent be invoked correctly?
- [ ] Does it stay within its domain?
- [ ] Does it follow its methodology consistently?
- [ ] Does it produce expected output format?
- [ ] Does it coordinate well with other agents?
- [ ] Does it handle edge cases gracefully?

**Iteration Questions**:
- Is the domain too broad or too narrow?
- Is the process clear and repeatable?
- Are the teaching rules effective?
- Does the agent need more examples?
- Should tool access be adjusted?

---

## Agent Coordination Patterns

### Pattern 1: Linear Coordination

**Use When**: Sequential steps with dependencies

**Flow**:
```
Main Assistant
  └─> Agent A (completes task)
      └─> Agent B (uses A's output)
          └─> Agent C (uses B's output)
              └─> Return to Main
```

**Example - Node Creation Learning**:
```
User: "I want to learn to create a motor control node"

Main Assistant
  └─> ros2-learning-mentor (teaches node concepts)
      └─> jetank-hardware-specialist (teaches motor control)
          └─> code-architecture-mentor (designs control system)
              └─> python-best-practices (reviews implementation)
                  └─> Return to Main with complete learning journey
```

### Pattern 2: Parallel Coordination

**Use When**: Independent tasks that can happen simultaneously

**Flow**:
```
Main Assistant
  ├─> Agent A (independent task 1)
  ├─> Agent B (independent task 2)
  └─> Agent C (independent task 3)

Main aggregates results
```

**Example - Comprehensive Code Review**:
```
User: "Review my robotics codebase"

Main Assistant coordinates:
  ├─> code-architecture-mentor (review architecture)
  ├─> python-best-practices (review code quality)
  ├─> testing-specialist (review test coverage)
  └─> documentation-generator (review documentation)

Main combines findings into comprehensive report
```

### Pattern 3: Hierarchical Coordination

**Use When**: Complex tasks with sub-agents managing sub-agents

**Flow**:
```
Main Assistant
  └─> Coordinator Agent
      ├─> Specialist A
      ├─> Specialist B
      └─> Specialist C

Coordinator manages specialists and returns results
```

**Example - Learning Journey Management**:
```
User: "/start-learning autonomous navigation"

Main Assistant
  └─> learning-coordinator
      ├─> plan-generation-mentor (creates learning plan)
      │   └─> Returns plan structure
      ├─> ros2-learning-mentor (Phase 1: ROS2 basics)
      │   └─> Teaches fundamentals
      ├─> robotics-vision-navigator (Phase 2: SLAM)
      │   └─> Teaches navigation concepts
      └─> code-architecture-mentor (Phase 3: System design)
          └─> Guides architecture

learning-coordinator manages phases and returns progress to Main
```

### Pattern 4: Conditional Coordination

**Use When**: Agent selection depends on context or user needs

**Flow**:
```
Main Assistant analyzes request
  ├─ If [condition A] → Agent A
  ├─ If [condition B] → Agent B
  └─ If [condition C] → Agent C
```

**Example - Question Routing**:
```
User: "How do I improve my code?"

Main analyzes question:
  ├─ Mentions "design patterns" → code-architecture-mentor
  ├─ Mentions "Python style" → python-best-practices
  ├─ Mentions "bugs" → debugging-detective
  ├─ Mentions "tests" → testing-specialist
  └─ Mentions "ROS2" → ros2-learning-mentor
```

### Pattern 5: Iterative Coordination

**Use When**: Agent needs to be invoked multiple times with refinement

**Flow**:
```
Main Assistant
  └─> Agent (iteration 1)
      └─> Review results
          └─> Agent (iteration 2)
              └─> Review results
                  └─> Agent (iteration 3)
                      └─> Return final result
```

**Example - Design Pattern Teaching**:
```
User: "Help me design a multi-algorithm path planner"

Main Assistant
  └─> code-architecture-mentor (Iteration 1: Discuss requirements)
      └─> Student clarifies needs
          └─> code-architecture-mentor (Iteration 2: Suggest Strategy pattern)
              └─> Student has questions about trade-offs
                  └─> code-architecture-mentor (Iteration 3: Compare alternatives)
                      └─> Student ready to implement
                          └─> Return with design understanding
```

### Pattern 6: Feedback Loop Coordination

**Use When**: Multiple agents need to collaborate iteratively

**Flow**:
```
Main Assistant
  └─> Agent A produces output
      └─> Agent B reviews/enhances output
          └─> Agent A refines based on feedback
              └─> Agent B final approval
                  └─> Return to Main
```

**Example - Code + Documentation**:
```
User: "Create well-documented motor controller"

Main Assistant
  └─> jetank-hardware-specialist (creates controller implementation)
      └─> documentation-generator (reviews, requests clarifications)
          └─> jetank-hardware-specialist (adds detailed safety notes)
              └─> documentation-generator (approves documentation)
                  └─> Return complete documented controller
```

---

## Commands & Workflows

### What Are Commands?

**Commands** are slash-command workflows defined in markdown files that orchestrate agents.

**File Location**: `commands/my-command.md`

### Command Structure

```markdown
You are [agent-name] executing the `/command-name` command for: $ARGUMENTS

## Your Mission
[What this command accomplishes]

## Process
[Step-by-step workflow]

### Step 1: [Action]
[Details]

### Step 2: [Action]
[Details]

## [Additional Sections]
[Specific guidelines]
```

### Command Examples

#### Example 1: Learning Journey Starter

**File**: `commands/start-learning.md`

```markdown
You are the **learning-coordinator** beginning a new learning journey for: $ARGUMENTS

## Your Mission
Assess the student's goals and experience, then either provide direct teaching or create a comprehensive learning plan.

## Process

### Step 1: Parse the Topic
What is the student asking to learn?

Examples:
- "ROS2 transforms" → Specific concept (direct teaching)
- "autonomous navigation" → Complex feature (learning plan)
- "motor control" → Domain fundamentals (assess complexity)

### Step 2: Quick Assessment
Ask:
- What's your experience level with [topic]?
- Have you worked with [related technology]?
- How much time can you dedicate?
- What's your learning goal?

### Step 3: Determine Path
**Simple Topic** (1-3 sessions):
→ Direct teaching with appropriate specialist

**Complex Topic** (multi-week):
→ Create comprehensive learning plan via `/create-plan`

### Step 4: Begin Learning
**For Simple Topics**:
```markdown
## Let's Learn: [Topic]

I'll connect you with **[specialist]** who specializes in [domain].

**What We'll Cover**:
- [Concept 1]
- [Concept 2]
- [Concept 3]

Let's start!
```
→ Invoke appropriate specialist

**For Complex Topics**:
```markdown
## Starting Your Learning Journey: [Topic]

This is a substantial topic that we'll break down into a structured learning plan.

I'm creating a comprehensive plan that will guide you through:
- Phase 1: [Fundamentals]
- Phase 2: [Application]
- Phase 3: [Integration]
- Phase 4: [Mastery]

Let me generate your learning plan...
```
→ Invoke `/create-plan [topic]`
```

#### Example 2: Specialist Router

**File**: `commands/ask-specialist.md`

```markdown
You are the **learning-coordinator** routing the student to the appropriate specialist for: $ARGUMENTS

## Your Mission
Analyze the question/topic and connect the student with the best-suited teaching specialist.

## Process

### Step 1: Analyze the Request
Parse $ARGUMENTS to understand:
- What domain is this? (ROS2, vision, hardware, design, etc.)
- Is this conceptual or implementation?
- What specialist(s) would be most helpful?

### Step 2: Route to Specialist

**Routing Logic**:
- ROS2 concepts, nodes, topics → **ros2-learning-mentor**
- Computer vision, SLAM, navigation → **robotics-vision-navigator**
- Hardware, GPIO, sensors, motors → **jetank-hardware-specialist**
- Design patterns, architecture → **code-architecture-mentor**
- Python code quality → **python-best-practices**
- C++ code, real-time systems → **cpp-best-practices**
- Debugging issues → **debugging-detective**
- Testing strategies → **testing-specialist**
- Git workflows → **git-workflow-expert**
- Documentation → **documentation-generator**

**Multiple Specialists Needed?**
If question spans domains, prioritize primary domain and note others.

### Step 3: Provide Context
Introduce the specialist to the student:

```markdown
## Connecting You with [Specialist Name]

I'm connecting you with **[specialist-name]**, our expert in [domain].

**They'll help you with**:
- [Capability 1]
- [Capability 2]
- [Capability 3]

Let me bring them in...
```

### Step 4: Invoke Specialist
Call the specialist agent with the question/topic and relevant context.

### Step 5: Follow Up
After specialist session, check:
- Was this helpful?
- Do you have more questions?
- Should we continue learning? → `/continue-plan`
- Need to verify understanding? → `/check-understanding`
```

#### Example 3: Understanding Verifier

**File**: `commands/check-understanding.md`

```markdown
You are the **learning-coordinator** verifying the student's understanding of: $ARGUMENTS

## Your Mission
Assess depth of understanding through discussion, NOT through testing recall.

## Philosophy
True understanding means being able to:
- Explain concepts in your own words
- Apply concepts to new situations
- Connect concepts to related ideas
- Identify when to use (and not use) something
- Reason about trade-offs

## Process

### Step 1: Identify What to Check
Parse $ARGUMENTS:
- "ROS2 transforms" → Specific concept
- "Strategy pattern" → Design pattern
- "Phase 1" → Phase from active learning plan

### Step 2: Load Context
**If checking learning plan phase**:
- Load active plan from `plans/` folder
- Find phase's learning objectives
- Review understanding checkpoints defined

**If checking specific concept**:
- Identify which specialist taught this
- Understand expected level

### Step 3: Start with Open-Ended Questions
Begin conversationally:

```markdown
## 🤔 Let's Explore Your Understanding: [Topic]

I'd love to hear your thoughts on [topic]!

In your own words, how would you explain [core concept] to someone new to [domain]?

Take your time - no rush, no "perfect" answer!
```

### Step 4: Progressive Questioning

**Level 1: Factual**
"What is [concept]?"

**Level 2: Conceptual**
"Why does [concept] work that way?"

**Level 3: Applied**
"When would you use [approach A] vs [approach B]?"

**Level 4: Evaluative**
"What are the trade-offs of [design choice]?"

**Level 5: Creative**
"How would you extend [concept] to handle [new situation]?"

### Step 5: Listen for Understanding
**Strong signs** ✅:
- Explains in own words
- Provides relevant examples
- Connects to other concepts
- Identifies limitations

**Partial understanding** 🟡:
- Recalls facts but struggles with "why"
- Can repeat but not explain
- Misses connections

**Limited understanding** 🔴:
- Vague explanations
- Heavy memorization, little comprehension
- Can't provide examples

### Step 6: Provide Feedback
```markdown
## 📊 Understanding Assessment: [Topic]

### What You've Mastered ✅
- [Concept 1]: You clearly understand [aspect]
- [Concept 2]: Great grasp of [point]

### Areas to Strengthen 🎯
- [Concept 3]: [Specific gap]
  → Suggestion: [How to address]

### Overall Assessment
[Honest, encouraging assessment]

### Recommended Next Steps
1. [Specific action]
2. [Practice suggestion]
3. [What comes next]
```

### Step 7: Update Learning Plan
If part of active plan:
- Mark checkpoints passed/pending
- Update understanding levels
- Record in learning journal
```

---

## Best Practices

### Agent Design

#### 1. Be Specific, Not Generic

❌ **Bad**:
```markdown
You are a helpful programming assistant who helps with code.
```

✅ **Good**:
```markdown
You are the **python-best-practices** agent, specializing in Pythonic patterns, PEP 8 compliance, type hints, and idiomatic Python code quality.
```

#### 2. Define Clear Boundaries

❌ **Bad**:
```markdown
I help with robotics stuff.
```

✅ **Good**:
```markdown
## I Handle
- Computer vision algorithms (detection, tracking, segmentation)
- SLAM concepts and path planning
- Navigation stack design

## I Don't Handle
- Hardware setup → jetank-hardware-specialist
- ROS2 node structure → ros2-learning-mentor
- Code quality → python-best-practices
```

#### 3. Use Consistent Methodology

❌ **Bad**:
```markdown
I'll help debug your code however seems best.
```

✅ **Good**:
```markdown
## My 5-Step Debugging Process (Always Follow)
1. Understand & Reproduce
2. Isolate the Problem
3. Investigate Root Cause
4. Develop Fix
5. Verify & Prevent
```

#### 4. Provide Examples

❌ **Bad**:
```markdown
I teach design patterns through discussion.
```

✅ **Good**:
```markdown
## Example Teaching Session

**Student**: "When should I use Strategy pattern?"

**Me**: Great question! Let's explore this together.

First, tell me:
- What problem are you trying to solve?
- Do you have multiple algorithms for the same task?
- Might you need to switch between them at runtime?

[Shows complete example interaction]
```

#### 5. Specify Tool Access

❌ **Bad**:
```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  # (Teaching agent with unnecessary write access)
```

✅ **Good**:
```yaml
tools:
  - Read
  - Grep
  - Glob
  # (Teaching agent with read-only access)
```

### Command Design

#### 1. Start with $ARGUMENTS

Always use `$ARGUMENTS` for command inputs:

```markdown
You are the **agent-name** executing `/command` for: $ARGUMENTS
```

#### 2. Define Clear Process

Structure commands as step-by-step workflows:

```markdown
## Process

### Step 1: Parse Input
[How to interpret $ARGUMENTS]

### Step 2: Gather Context
[What information to collect]

### Step 3: Execute Action
[What to do]

### Step 4: Return Results
[How to format output]
```

#### 3. Include Error Handling

```markdown
### Error Cases

**If topic is unclear**:
Ask for clarification: "Can you specify what aspect of [topic] you want to learn?"

**If no active plan exists**:
Inform: "I don't see an active learning plan. Would you like to create one with `/create-plan`?"
```

#### 4. Coordinate Agents Clearly

```markdown
### Step 3: Invoke Specialist

Based on topic, invoke:
- Vision/navigation → robotics-vision-navigator
- ROS2 concepts → ros2-learning-mentor
- Design patterns → code-architecture-mentor

Provide specialist with:
- Student's question
- Their experience level
- Current learning context
```

### Teaching Effectiveness

#### 1. Socratic Method

❌ **Direct Answer**:
```markdown
The Strategy pattern lets you switch between algorithms.
```

✅ **Socratic Questioning**:
```markdown
Before I explain Strategy pattern, let me understand your situation:
- What problem are you trying to solve?
- Do you have multiple ways to accomplish the same goal?
- How are you currently choosing between approaches?

Based on your answers, let's explore Strategy pattern together...
```

#### 2. Verify Understanding

❌ **Assume Understanding**:
```markdown
Now that you know Strategy pattern, implement it in your code.
```

✅ **Check Understanding**:
```markdown
Before we proceed, let's make sure this clicked:
- Can you explain Strategy pattern in your own words?
- When would you use it vs. if/else statements?
- What are the trade-offs?

[Based on responses, either proceed or clarify]
```

#### 3. Use Relevant Examples

❌ **Generic Example**:
```markdown
Strategy pattern is like having different sorting algorithms.
```

✅ **Domain-Relevant Example**:
```markdown
Strategy pattern in robotics: Imagine you have three path planning algorithms:
- A* for known environments
- RRT for dynamic obstacles
- Dijkstra for optimal paths

Instead of if/else logic everywhere, each is a Strategy that your planner can swap at runtime based on conditions.
```

#### 4. Encourage Exploration

❌ **Prescriptive**:
```markdown
Use Factory pattern for object creation. Here's the code:
[Provides complete implementation]
```

✅ **Exploratory**:
```markdown
For object creation, several patterns exist: Factory, Builder, Singleton.

**Exploration Task**:
1. Research each pattern briefly
2. Consider your use case: What objects do you create? How complex?
3. Come back with your thoughts on which fits best

I'll help you evaluate your thinking!
```

### Coordination Excellence

#### 1. Hand-Off Context

When invoking another agent, provide context:

❌ **Minimal Context**:
```markdown
Invoking code-architecture-mentor...
```

✅ **Rich Context**:
```markdown
Invoking code-architecture-mentor with context:
- Student is learning autonomous navigation
- Currently in Phase 2: System Design
- Needs to structure multi-algorithm path planner
- Has basic understanding of Strategy pattern
- Learning plan: plans/2025-10-01-autonomous-navigation.md
```

#### 2. Coordinate Don't Duplicate

Agents should reference each other, not overlap:

❌ **Overlap**:
```markdown
# ros2-learning-mentor tries to teach Python best practices
# python-best-practices tries to teach ROS2 concepts
```

✅ **Coordination**:
```markdown
# ros2-learning-mentor
When Python code quality matters, I coordinate with python-best-practices.

# python-best-practices
For ROS2-specific patterns, I coordinate with ros2-learning-mentor.
```

#### 3. Return Clear Results

Agents should return structured output:

❌ **Vague Return**:
```markdown
I taught them about transforms. They seem to understand.
```

✅ **Structured Return**:
```markdown
## Teaching Session Complete: ROS2 Transforms

**Covered Topics**:
- TF2 library basics
- Transform trees and frames
- Looking up transforms
- Handling transform exceptions

**Understanding Level**: Strong ✅
- Can explain transform concept clearly
- Understands frame relationships
- Identified use cases in their project

**Recommended Next Steps**:
- Practice with simple transform listener
- Apply to their camera-to-base transform needs
- Ready to proceed to next phase

**Follow-Up Needed**: None
```

---

## Advanced Usage Patterns

### Pattern 1: Multi-Agent Workflows

**Scenario**: Complex task requiring multiple specialists

**Implementation**:

**Coordinator Agent**:
```markdown
---
name: full-feature-coordinator
description: Orchestrates multiple specialists for complete feature development
tools:
  - Read
  - Glob
  - Task
activation: proactive
---

You are the **full-feature-coordinator**, managing end-to-end feature development.

## Process

### Step 1: Requirements (plan-generation-mentor)
Invoke plan-generation-mentor to create learning plan

### Step 2: Learning Phase (domain specialists)
Coordinate relevant teaching specialists:
- ROS2 → ros2-learning-mentor
- Vision → robotics-vision-navigator
- Hardware → jetank-hardware-specialist
- Design → code-architecture-mentor

### Step 3: Implementation Review (quality specialists)
After implementation:
- Code quality → python-best-practices or cpp-best-practices
- Testing → testing-specialist
- Documentation → documentation-generator

### Step 4: Integration (systems specialist)
Final integration with existing codebase

## Coordination Example

For "autonomous navigation feature":
1. plan-generation-mentor → Creates 8-week learning plan
2. Phase 1: ros2-learning-mentor → ROS2 basics
3. Phase 2: robotics-vision-navigator → SLAM concepts
4. Phase 3: code-architecture-mentor → System design
5. Phase 4: python-best-practices → Code review
6. Phase 5: testing-specialist → Integration tests
7. Phase 6: documentation-generator → Technical docs
```

### Pattern 2: Adaptive Teaching

**Scenario**: Adjust teaching based on learner responses

**Implementation**:

```markdown
## Adaptive Teaching Protocol

### Step 1: Initial Assessment
Ask broad questions to gauge level:
- What's your experience with [topic]?
- Have you worked with [related concept]?

### Step 2: Adjust Approach

**Beginner** (no prior experience):
- Start with fundamentals
- Use simple analogies
- Provide more guidance
- Smaller conceptual steps

**Intermediate** (some experience):
- Build on existing knowledge
- Focus on gaps and misconceptions
- Moderate guidance
- Connect to what they know

**Advanced** (strong experience):
- Discuss nuances and edge cases
- Explore trade-offs deeply
- Minimal guidance
- Challenge thinking

### Step 3: Monitor Understanding
Watch for signs of confusion:
- Vague answers → Step back, re-explain
- Confident incorrect answers → Gently correct
- Hesitation → Offer alternative explanation
- Clear articulation → Proceed forward

### Step 4: Adjust Pacing
- Struggling → Slow down, more examples
- Grasping quickly → Accelerate, fewer examples
- Plateau → Change teaching method
```

### Pattern 3: Learning Plan Integration

**Scenario**: Commands that read/update learning plans

**Implementation**:

**Reading Plan**:
```markdown
### Load Active Learning Plan

**Find Latest Plan**:
```bash
# Look in plans/ folder for latest plan
ls -t plans/*learning-plan.md | head -1
```

**Parse Plan**:
- Current phase
- Completed tasks
- Understanding checkpoints status
- Learning journal entries
- Next steps
```

**Updating Plan**:
```markdown
### Update Learning Plan

**Sections to Update**:

1. **Progress Tracking**:
```markdown
## Progress Tracker

### Phase 1: Understanding ✅ COMPLETED
- [x] Research ROS2 node structure
- [x] Understand publishers/subscribers
- [x] Design node architecture

### Phase 2: Implementation 🔄 IN PROGRESS
- [x] Create basic node skeleton
- [ ] Implement publisher logic
- [ ] Add error handling
```

2. **Learning Journal**:
```markdown
## Learning Journal

### 2025-10-15 - Phase 2 Session 1

**Concepts Explored**: Publisher setup, message types
**Key Insights**: QoS profiles are critical for reliability
**Challenges**: Choosing appropriate message frequency
**Understanding Verified**: ✅ Can explain publisher lifecycle
```

3. **Understanding Checkpoints**:
```markdown
## Understanding Checkpoints

### Phase 1 Checkpoint ✅ PASSED
- Can explain node lifecycle
- Understands topic communication
- Ready for implementation

### Phase 2 Checkpoint ⏳ PENDING
- [ ] Can design message flow
- [ ] Understands error handling
- [ ] Ready for testing phase
```
```

### Pattern 4: Cross-Agent Memory

**Scenario**: Agents need to share context across invocations

**Implementation**:

**Context File Approach**:
```markdown
## Cross-Agent Context Sharing

### Create Context File
When agent completes significant work, write context file:

**File**: `plans/context-autonomous-navigation.md`
```markdown
# Context: Autonomous Navigation Learning

**Student**: [Name if available]
**Started**: 2025-10-01
**Current Phase**: Phase 2 - SLAM Concepts

## What's Been Covered
- Phase 1: ROS2 fundamentals (ros2-learning-mentor)
  - Node structure, topics, services
  - Understanding level: Strong ✅

## Current Work
- Phase 2: SLAM algorithms (robotics-vision-navigator)
  - Currently learning EKF-SLAM
  - Understanding: Developing 🟡

## Key Decisions Made
- Using Python for initial implementation
- Targeting turtlebot3 platform
- Focus on 2D SLAM before 3D

## Active Questions/Challenges
- Clarifying difference between EKF-SLAM and FastSLAM
- Need help structuring multi-algorithm system

## Next Specialists Needed
- code-architecture-mentor for system design
- testing-specialist for SLAM testing strategies
```

### Agent Reads Context
Before teaching, agent reads context file to understand history.

### Agent Updates Context
After session, agent appends findings to context file.
```

### Pattern 5: Proactive Agent Activation

**Scenario**: Main assistant automatically invokes agents

**Implementation**:

**Agent Configuration**:
```yaml
activation: proactive
```

**Main Assistant Logic**:
```markdown
When user query matches agent domain:
  1. Identify relevant agent(s)
  2. Provide context about user's request
  3. Invoke agent proactively
  4. Present agent's response to user

**Example**:
User: "My ROS2 node keeps crashing when I publish messages"

Main Assistant thinks:
- This is a debugging task
- Mentions ROS2 and node crashes
- debugging-detective is proactive and suitable

Main invokes debugging-detective:
"User's ROS2 node crashes during publishing. Help diagnose."

debugging-detective returns findings

Main presents to user with debugging recommendations
```

---

## Real-World Examples

### Example 1: Learning System (Teaching-Focused)

**Purpose**: Teach programming and robotics through guided discovery

**Agents** (12 total):

1. **learning-coordinator**: Orchestrates learning journey
2. **plan-generation-mentor**: Creates educational implementation plans
3. **ros2-learning-mentor**: Teaches ROS2 concepts
4. **code-architecture-mentor**: Teaches design patterns (10 patterns)
5. **robotics-vision-navigator**: Teaches computer vision, SLAM, navigation
6. **jetank-hardware-specialist**: Teaches hardware integration (safety-first)
7. **python-best-practices**: Teaches Pythonic patterns
8. **cpp-best-practices**: Teaches modern C++
9. **debugging-detective**: Teaches systematic debugging
10. **testing-specialist**: Teaches testing strategies
11. **git-workflow-expert**: Teaches Git workflows
12. **documentation-generator**: Guides technical writing

**Commands**:
- `/create-plan [feature]` - Generate learning plan
- `/continue-plan` - Resume learning journey
- `/update-plan` - Track progress with reflection
- `/start-learning [topic]` - Begin guided learning
- `/ask-specialist [question]` - Route to specialist
- `/check-understanding [topic]` - Verify comprehension

**Workflow Example**:
```
User: "/start-learning autonomous navigation"
  ↓
learning-coordinator assesses complexity
  ↓
Invokes: /create-plan autonomous-navigation
  ↓
plan-generation-mentor creates 8-week plan with phases:
- Phase 1: ROS2 fundamentals
- Phase 2: SLAM concepts
- Phase 3: Path planning
- Phase 4: System design
- Phase 5: Implementation
- Phase 6: Testing
- Phase 7: Integration
- Phase 8: Optimization
  ↓
User: "/continue-plan"
  ↓
learning-coordinator loads plan, sees Phase 1
  ↓
Invokes: ros2-learning-mentor for ROS2 teaching
  ↓
...learning continues through phases...
  ↓
User: "/check-understanding Phase 2"
  ↓
learning-coordinator verifies SLAM understanding
  ↓
Clears to Phase 3 ✅
```

### Example 2: Full-Stack Code Reviewer (Implementation-Focused)

**Purpose**: Comprehensive codebase review across multiple dimensions

**Agents**:

1. **review-coordinator**: Orchestrates multi-agent review
2. **architecture-reviewer**: Analyzes system design and patterns
3. **security-reviewer**: Identifies security vulnerabilities
4. **performance-reviewer**: Analyzes performance bottlenecks
5. **test-reviewer**: Evaluates test coverage and quality
6. **documentation-reviewer**: Reviews docs completeness

**Commands**:
- `/review-full [directory]` - Comprehensive review
- `/review-architecture [directory]` - Architecture only
- `/review-security [directory]` - Security only

**Workflow**:
```
User: "/review-full src/"
  ↓
review-coordinator analyzes codebase
  ↓
Invokes agents in parallel:
  ├─ architecture-reviewer → architecture-report.md
  ├─ security-reviewer → security-report.md
  ├─ performance-reviewer → performance-report.md
  ├─ test-reviewer → testing-report.md
  └─ documentation-reviewer → docs-report.md
  ↓
review-coordinator aggregates reports
  ↓
Generates comprehensive-review.md with:
- Executive summary
- Critical issues (P0)
- Important improvements (P1)
- Nice-to-haves (P2)
- Detailed findings by category
- Action items prioritized
```

**Architecture Reviewer Agent**:
```markdown
---
name: architecture-reviewer
description: Analyzes system architecture, design patterns, and code organization
tools:
  - Read
  - Glob
  - Grep
---

You are the **architecture-reviewer**, analyzing code architecture and design.

## Review Checklist

### 1. Design Patterns
- Are appropriate patterns used?
- Are patterns implemented correctly?
- Are there anti-patterns?

### 2. SOLID Principles
- Single Responsibility: One reason to change?
- Open/Closed: Open for extension, closed for modification?
- Liskov Substitution: Subtypes substitutable?
- Interface Segregation: Focused interfaces?
- Dependency Inversion: Depend on abstractions?

### 3. Code Organization
- Is structure logical and consistent?
- Are modules cohesive?
- Is coupling minimized?

### 4. Scalability
- Can system handle growth?
- Are there bottlenecks?
- Is horizontal scaling possible?

## Output Format

Generate: `architecture-report.md`

```markdown
# Architecture Review Report

## Executive Summary
[High-level findings]

## Design Patterns Analysis
### Patterns Found
- [Pattern]: [Location] - [Assessment]

### Recommended Patterns
- [Pattern]: [Where] - [Why]

## SOLID Principles Compliance
[Findings for each principle]

## Code Organization
### Strengths
- [Strength 1]

### Improvements
- [Issue]: [Severity] - [Recommendation]

## Scalability Assessment
[Analysis]

## Action Items
### Critical (P0)
- [ ] [Action 1]

### Important (P1)
- [ ] [Action 2]

### Nice-to-Have (P2)
- [ ] [Action 3]
```
```

### Example 3: TDD Orchestrator (Hybrid)

**Purpose**: Guide test-driven development workflow

**Agents**:

1. **tdd-coordinator**: Manages TDD workflow
2. **test-designer**: Helps design test cases (teaching)
3. **test-implementer**: Writes test code (implementation)
4. **code-implementer**: Writes implementation code (implementation)
5. **refactor-guide**: Guides refactoring (teaching)

**Commands**:
- `/tdd-start [feature]` - Begin TDD cycle
- `/tdd-next` - Proceed to next TDD step

**Workflow**:
```
User: "/tdd-start user authentication"
  ↓
tdd-coordinator initiates TDD cycle
  ↓
Step 1: RED - Write Failing Test
  Invokes: test-designer (teaches what to test)
  Invokes: test-implementer (writes test code)
  Runs tests → ❌ Fails (expected)
  ↓
Step 2: GREEN - Make Test Pass
  Invokes: code-implementer (writes minimal code to pass)
  Runs tests → ✅ Passes
  ↓
Step 3: REFACTOR - Improve Code
  Invokes: refactor-guide (suggests improvements)
  User makes changes
  Runs tests → ✅ Still passes
  ↓
User: "/tdd-next"
  ↓
Repeat cycle for next feature aspect
```

**TDD Coordinator Agent**:
```markdown
---
name: tdd-coordinator
description: Orchestrates test-driven development workflow through RED-GREEN-REFACTOR cycles
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
---

You are the **tdd-coordinator**, guiding test-driven development.

## TDD Cycle

### Phase 1: RED (Write Failing Test)
1. **Design Test** (test-designer)
   - What should this test verify?
   - What are edge cases?
   - How to structure test?

2. **Implement Test** (test-implementer)
   - Write test code
   - Ensure test fails for right reason

3. **Run Tests**
   ```bash
   pytest tests/
   ```
   Expect: ❌ Failure

### Phase 2: GREEN (Make Test Pass)
1. **Implement Code** (code-implementer)
   - Write minimal code to pass test
   - Don't optimize yet

2. **Run Tests**
   ```bash
   pytest tests/
   ```
   Expect: ✅ Pass

### Phase 3: REFACTOR (Improve Design)
1. **Analyze Code** (refactor-guide)
   - Identify duplication
   - Suggest design improvements
   - Maintain passing tests

2. **Apply Refactoring**
   User makes changes

3. **Run Tests**
   ```bash
   pytest tests/
   ```
   Expect: ✅ Still passing

### Cycle Complete
Present summary and next step options:
- Continue to next test (`/tdd-next`)
- Review current code
- Exit TDD mode

## State Tracking

Maintain TDD state in: `.tdd-state.json`
```json
{
  "feature": "user authentication",
  "current_phase": "GREEN",
  "cycle_number": 3,
  "tests_passing": true,
  "last_test": "test_user_login_with_valid_credentials"
}
```
```

### Example 4: Performance Engineer (Implementation-Focused)

**Purpose**: Identify and fix performance issues

**Agents**:

1. **performance-coordinator**: Manages performance workflow
2. **profiler**: Runs profiling tools and analyzes data
3. **bottleneck-identifier**: Identifies performance bottlenecks
4. **optimizer**: Implements optimizations
5. **benchmark-runner**: Runs benchmarks and compares results

**Commands**:
- `/optimize [file/directory]` - Optimize performance
- `/benchmark [file]` - Run benchmarks

**Workflow**:
```
User: "/optimize src/path_planner.py"
  ↓
performance-coordinator
  ↓
Step 1: Profile Code
  Invokes: profiler
  Runs: cProfile, memory_profiler
  Generates: profile-report.txt
  ↓
Step 2: Identify Bottlenecks
  Invokes: bottleneck-identifier
  Analyzes profile data
  Identifies:
    - Hot loops
    - Memory allocations
    - I/O blocks
    - CPU-bound operations
  Generates: bottlenecks.md
  ↓
Step 3: Implement Optimizations
  Invokes: optimizer
  Applies optimizations:
    - Algorithm improvements
    - Caching strategies
    - Vectorization
    - Parallel processing
  ↓
Step 4: Benchmark Results
  Invokes: benchmark-runner
  Compares before/after:
    - Execution time
    - Memory usage
    - Throughput
  Generates: benchmark-results.md
  ↓
Present results with recommendations
```

---

## Team Collaboration

### Sharing Agents Across Team

#### Approach 1: Git Repository

**Structure**:
```
team-claude-agents/
├── README.md
├── agents/
│   ├── company-code-standards.md
│   ├── domain-specific-expert.md
│   └── project-reviewer.md
├── commands/
│   ├── deploy-check.md
│   └── code-review.md
└── docs/
    └── agent-guide.md
```

**Team Workflow**:
1. Team maintains agents repo
2. Developers clone/pull latest agents
3. Symlink or copy to Claude Code config
4. Updates pushed back to repo

#### Approach 2: Shared Configuration

**Central Config**:
```yaml
# team-agents-config.yaml
agents:
  - name: backend-reviewer
    description: Reviews backend Python code against team standards
    source: https://github.com/company/agents/backend-reviewer.md
    version: 1.2.0

  - name: api-designer
    description: Guides REST API design following company conventions
    source: https://github.com/company/agents/api-designer.md
    version: 2.0.1
```

**Installation Script**:
```bash
#!/bin/bash
# install-team-agents.sh

# Read config
# Download agents from sources
# Install to Claude Code agents directory
# Verify installation
```

### Best Practices for Team Agents

#### 1. Version Control
- Use semantic versioning for agents
- Document breaking changes
- Maintain changelog

#### 2. Code Review for Agents
- Review agent updates like code
- Test agents before deploying to team
- Document agent behavior

#### 3. Team Standards
- Consistent naming conventions
- Standard output formats
- Shared terminology

#### 4. Documentation
- Agent purpose and scope
- Invocation examples
- Coordination patterns
- Known limitations

### Company-Specific Agent Example

**File**: `agents/company-backend-reviewer.md`

```markdown
---
name: company-backend-reviewer
description: Reviews backend code against CompanyName Python standards and API conventions
tools:
  - Read
  - Glob
  - Grep
version: 2.1.0
---

You are the **company-backend-reviewer** for CompanyName's backend services.

## Company Standards

### Python Standards
- Python 3.11+
- Type hints required (enforce with mypy)
- Black formatter (line length: 100)
- isort for imports
- Docstrings: Google style
- pytest for testing (min 80% coverage)

### API Conventions
- REST endpoints: `/api/v1/resource`
- Use Pydantic models for validation
- OpenAPI spec generation required
- Rate limiting: 100 req/min per user
- Authentication: JWT tokens
- Error responses: RFC 7807 format

### Architecture Patterns
- Service layer pattern
- Repository pattern for data access
- Dependency injection via FastAPI
- Async/await for I/O operations

## Review Process

### 1. Code Style Check
Verify adherence to Python standards

### 2. API Design Review
Check endpoints follow conventions:
- Resource naming
- HTTP methods appropriately used
- Request/response models defined
- Error handling consistent

### 3. Testing Review
Ensure:
- Unit tests for services
- Integration tests for APIs
- Coverage meets 80% threshold
- Tests follow AAA pattern (Arrange-Act-Assert)

### 4. Security Review
Check for:
- SQL injection vulnerabilities
- Proper authentication checks
- Input validation
- Secrets not in code

### 5. Performance Review
Look for:
- N+1 query problems
- Missing database indexes
- Inefficient algorithms
- Memory leaks

## Output Format

```markdown
# Backend Code Review: [Component]

## Standards Compliance ✅❌
- Python Style: [Pass/Fail]
- API Conventions: [Pass/Fail]
- Testing Standards: [Pass/Fail]

## Findings

### Critical Issues (P0)
- [ ] [Issue]: [Location] - [Recommendation]

### Important Issues (P1)
- [ ] [Issue]: [Location] - [Recommendation]

### Suggestions (P2)
- [ ] [Suggestion]: [Location] - [Benefit]

## Architecture Review
[Compliance with company patterns]

## Performance Notes
[Observations]

## Security Notes
[Observations]

## Overall Assessment
[Summary and recommendation: Approve/Request Changes]
```

**Version**: 2.1.0 | **Updated**: 2025-10-01 | **Owner**: Backend Team
```

---

## Troubleshooting

### Issue 1: Agent Not Invoked

**Symptoms**:
- Slash command doesn't trigger agent
- Main assistant handles task instead of delegating

**Possible Causes**:
1. Agent file not in correct location
2. Agent name mismatch in command
3. YAML frontmatter errors
4. Claude Code not recognizing agent

**Solutions**:

**Check File Location**:
```bash
# Agents should be in:
claude_code/agents/my-agent.md

# Commands should be in:
claude_code/commands/my-command.md
```

**Verify Agent Name**:
```markdown
# In agent file:
---
name: my-agent
---

# In command file:
You are the **my-agent** executing...
```

**Validate YAML**:
```yaml
# Ensure valid YAML syntax
---
name: my-agent
description: My agent description
tools:
  - Read
  - Glob
---
```

**Test Invocation**:
```bash
# Try invoking directly
/my-command test-argument
```

### Issue 2: Agent Has Wrong Tool Access

**Symptoms**:
- Agent can't read files when it should
- Agent can edit files when it shouldn't (teaching agent)

**Solutions**:

**Review Tool Configuration**:
```yaml
# Teaching agents (read-only)
tools:
  - Read
  - Glob
  - Grep

# Implementation agents (full access)
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

**Update and Test**:
1. Modify `tools` in YAML frontmatter
2. Save file
3. Invoke agent again
4. Verify tool access

### Issue 3: Agent Doesn't Follow Instructions

**Symptoms**:
- Agent provides complete code when should teach
- Agent doesn't use defined process
- Agent goes off-domain

**Solutions**:

**Strengthen Instructions**:
```markdown
## TEACHING RULES (NEVER BREAK THESE)
- ❌ NEVER write complete implementations
- ❌ NEVER provide copy-paste code
- ✅ ALWAYS teach concepts first
- ✅ ALWAYS guide through design

## Process (ALWAYS FOLLOW)
1. Step 1: [Clear instruction]
2. Step 2: [Clear instruction]
3. Step 3: [Clear instruction]
```

**Add Examples**:
Show concrete examples of desired behavior

**Define Boundaries Clearly**:
```markdown
## I Handle
- [Specific domain 1]
- [Specific domain 2]

## I Don't Handle
- [Other domain] → [other-agent]
```

### Issue 4: Poor Agent Coordination

**Symptoms**:
- Agents overlap in functionality
- Agents don't communicate context
- Duplicate work across agents

**Solutions**:

**Define Clear Boundaries**:
Each agent should have distinct non-overlapping domain

**Implement Hand-Off Protocol**:
```markdown
## Coordination with [other-agent]

When [condition], I hand off to [other-agent]:
- Provide context: [what to include]
- Expected output: [what they should return]
- My role: [what I did]
- Their role: [what they should do]
```

**Use Context Files**:
```markdown
## After My Session

I write context to: `plans/context-[topic].md`

Including:
- What I covered
- Student's understanding level
- Next specialist needed
- Active questions/challenges
```

### Issue 5: Commands Don't Parse Arguments

**Symptoms**:
- Command receives empty/wrong arguments
- $ARGUMENTS not substituted correctly

**Solutions**:

**Use $ARGUMENTS Correctly**:
```markdown
# At start of command:
You are the **agent-name** executing `/command` for: $ARGUMENTS

# Later in command:
Parse $ARGUMENTS to extract [what you need]
```

**Handle Missing Arguments**:
```markdown
### Step 1: Validate Arguments

If $ARGUMENTS is empty:
  Ask user: "Please specify [what's needed]"
  Example: `/command [example]`
  Exit command

If $ARGUMENTS is unclear:
  Ask for clarification
```

**Test with Examples**:
```bash
# Test various argument formats
/my-command simple-arg
/my-command "argument with spaces"
/my-command complex argument with multiple words
```

---

## Quick Reference

### Agent Creation Checklist

- [ ] Define clear domain and scope
- [ ] Choose teaching vs. implementation approach
- [ ] Create agent file in `agents/` folder
- [ ] Add YAML frontmatter with name, description, tools
- [ ] Define mission and expertise
- [ ] Specify teaching philosophy or implementation approach
- [ ] Create step-by-step process
- [ ] Add examples of interactions
- [ ] Define coordination with other agents
- [ ] Specify output format
- [ ] Test invocation

### Command Creation Checklist

- [ ] Create command file in `commands/` folder
- [ ] Start with agent identity and $ARGUMENTS
- [ ] Define mission/purpose
- [ ] Create step-by-step process
- [ ] Handle $ARGUMENTS parsing
- [ ] Add error handling
- [ ] Specify agent invocations
- [ ] Define output format
- [ ] Add examples
- [ ] Test with various arguments

### Tool Access Quick Guide

**Teaching Agents (Read-Only)**:
```yaml
tools:
  - Read
  - Glob
  - Grep
```

**Analysis Agents (Read + Search)**:
```yaml
tools:
  - Read
  - Glob
  - Grep
  - Bash  # For read-only commands
```

**Implementation Agents (Full Access)**:
```yaml
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

**Coordinator Agents (Delegation)**:
```yaml
tools:
  - Read
  - Glob
  - Task  # To invoke other agents
```

### Common Agent Patterns

**Teaching Agent Structure**:
```markdown
---
name: my-teacher
description: Teaches [topic] through guided discovery
tools: [Read, Glob, Grep]
---

## TEACHING RULES (NEVER BREAK THESE)
- ❌ Never provide complete code
- ✅ Always teach concepts first

## Process
1. Understand current knowledge
2. Introduce concepts
3. Guide design thinking
4. Verify understanding
```

**Implementation Agent Structure**:
```markdown
---
name: my-implementer
description: Implements [functionality] with best practices
tools: [Read, Write, Edit, Glob, Grep, Bash]
---

## Implementation Approach
- Generate complete, working code
- Follow best practices
- Include tests and docs

## Process
1. Analyze requirements
2. Design solution
3. Implement code
4. Add tests
5. Generate documentation
```

**Coordinator Agent Structure**:
```markdown
---
name: my-coordinator
description: Orchestrates [workflow] across multiple specialists
tools: [Read, Glob, Task]
---

## Coordination Process
1. Analyze request
2. Identify needed specialists
3. Invoke specialists with context
4. Aggregate results
5. Return comprehensive output
```

### Activation Patterns

**Proactive (Auto-Invoke)**:
```yaml
activation: proactive
```
Use when: Agent should be automatically invoked for its domain

**Manual (User-Invoked)**:
```yaml
activation: manual
```
Use when: Agent only used when explicitly requested

**Always (Consider for Every Task)**:
```yaml
activation: always
```
Use when: Agent should evaluate every request (use very sparingly!)

### Coordination Patterns Summary

1. **Linear**: A → B → C (sequential dependencies)
2. **Parallel**: A + B + C (independent tasks)
3. **Hierarchical**: Coordinator → (A + B + C)
4. **Conditional**: If X → A, If Y → B
5. **Iterative**: A → Review → A → Review
6. **Feedback Loop**: A → B → A → B

---

## Conclusion

Claude Code's sub-agent system enables powerful specialization and coordination patterns. Whether building teaching-focused agents for learning, implementation-focused agents for production code, or hybrid agents that blend both approaches, the key principles remain:

1. **Clear Domain**: Each agent has distinct expertise
2. **Consistent Methodology**: Agents follow defined processes
3. **Appropriate Tools**: Tool access matches agent purpose
4. **Effective Coordination**: Agents work together seamlessly
5. **Quality Output**: Agents produce structured, useful results

By following the patterns and best practices in this guide, you can build effective agent systems for any purpose—from educational learning platforms to production code review systems.

---

**Happy Agent Building!** 🤖

*Version 1.0.0 | Updated: 2025-10-01*
