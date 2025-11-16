# Complete Guide to Claude Code Learning System

## 📚 Table of Contents

1. [Overview](#overview)
2. [Philosophy](#philosophy)
3. [System Architecture](#system-architecture)
4. [Teaching Specialists](#teaching-specialists)
5. [Commands Reference](#commands-reference)
6. [Learning Workflows](#learning-workflows)
7. [Best Practices](#best-practices)
8. [Customization Guide](#customization-guide)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Claude Code Learning System is a comprehensive teaching framework designed to guide you through learning programming and robotics concepts through **guided discovery** rather than code generation.

### What Makes This Different?

**Traditional AI Coding Tools:**
- Generate complete code solutions
- Focus on speed and automation
- Little to no learning involved
- You copy-paste without understanding

**This Learning System:**
- Guides you through understanding concepts
- Teaches through questions and patterns
- Verifies comprehension before advancing
- You build solutions yourself with guidance
- Deep understanding of how and why things work

### Key Components

- **12 Teaching Specialists** - Expert agents for different domains
- **9 Learning Commands** - Slash commands for learning workflows
- **Learning Plans** - Structured multi-week learning journeys
- **Understanding Checkpoints** - Verification of comprehension
- **Learning Journals** - Reflection and consolidation

---

## Philosophy

### Core Principles

#### 1. **Understanding Over Speed**
Learning takes time. We prioritize deep comprehension over quick solutions.

**Bad:** "Create navigation system" → Complete code in 5 minutes
**Good:** "Create navigation system" → 6-week learning journey with full understanding

#### 2. **Guide, Don't Solve**
Teaching specialists guide you to the solution, they don't provide it.

**What They Do:**
- ✅ Explain concepts and principles
- ✅ Ask questions to develop thinking
- ✅ Show patterns and examples (2-5 lines)
- ✅ Guide design decisions
- ✅ Verify understanding

**What They Don't Do:**
- ❌ Write complete implementations
- ❌ Make all technical decisions
- ❌ Provide copy-paste solutions
- ❌ Skip understanding verification

#### 3. **Progressive Learning**
Build understanding in stages, from fundamentals to advanced topics.

**Learning Phases:**
1. **Understanding & Research** - Explore concepts
2. **Design & Architecture** - Plan your approach
3. **Basic Implementation** - Build core functionality
4. **Enhancement & Quality** - Refine and optimize
5. **Reflection & Mastery** - Consolidate learning

#### 4. **Active Learning**
You learn by doing, not by watching or copying.

**Your Role:**
- Research concepts and technologies
- Make design decisions (with guidance)
- Implement solutions yourself
- Debug and iterate
- Reflect on what you learned

#### 5. **Verifiable Understanding**
Before advancing, prove comprehension through discussion.

**Understanding Means:**
- Can explain in your own words
- Can apply to new situations
- Understand trade-offs and limitations
- Know when to use (and not use) something

---

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Learning Coordinator                     │
│          (Orchestrates learning journey)                     │
└──────────┬─────────────────────────────────────┬────────────┘
           │                                     │
    ┌──────▼──────┐                      ┌──────▼──────┐
    │   Commands  │                      │   Agents    │
    │  (Workflows)│                      │(Specialists)│
    └──────┬──────┘                      └──────┬──────┘
           │                                     │
    ┌──────▼──────────────────┐         ┌──────▼──────────────┐
    │ • start-learning        │         │ • ros2-learning     │
    │ • continue-plan         │         │ • python-practices  │
    │ • update-plan           │         │ • code-architecture │
    │ • ask-specialist        │         │ • robotics-vision   │
    │ • check-understanding   │         │ • hardware-spec     │
    │ • create-plan           │         │ • debugging-det     │
    │ • learn-ros2-node       │         │ • testing-spec      │
    └─────────────────────────┘         │ • git-workflow      │
                                        │ • documentation     │
                                        │ • cpp-practices     │
                                        │ • plan-generation   │
                                        │ • learning-coord    │
                                        └─────────────────────┘
```

### Data Flow

```
Student Request
    ↓
[Command Execution]
    ↓
Learning Coordinator
    ↓
[Assesses & Routes]
    ↓
Specialist Agent(s) ←→ [Teaching Session]
    ↓
Understanding Verification
    ↓
Progress Update → Learning Plan
    ↓
Next Learning Step
```

### File Organization

```
claude_code/
│
├── docs/                        # Documentation
│   ├── LEARNING_SYSTEM_GUIDE.md    # This file
│   └── [other guides]
│
├── commands/                    # Learning command definitions
│   ├── create-plan.md              # Plan generation
│   ├── continue-plan.md            # Resume learning
│   ├── update-plan.md              # Progress tracking
│   ├── start-learning.md           # Begin journey
│   ├── ask-specialist.md           # Get help
│   └── check-understanding.md      # Verify learning
│
├── agents/                      # Teaching specialists
│   ├── learning-coordinator.md     # Master coordinator
│   ├── plan-generation-mentor.md   # Plan creator
│   ├── ros2-learning-mentor.md     # ROS2 teacher
│   ├── code-architecture-mentor.md # Design patterns
│   ├── python-best-practices.md    # Python teacher
│   ├── cpp-best-practices.md       # C++ teacher
│   ├── robotics-vision-navigator.md # Vision/nav teacher
│   ├── jetank-hardware-specialist.md # Hardware teacher
│   ├── debugging-detective.md      # Debug methodology
│   ├── testing-specialist.md       # Testing teacher
│   ├── git-workflow-expert.md      # Git teacher
│   └── documentation-generator.md  # Doc writing teacher
│
├── ros2/                        # ROS2-specific commands
│   ├── learn-ros2-node.md          # Teaching approach
│   ├── new-node.md                 # Production generation
│   ├── debug-node.md               # Debug guidance
│   └── test-integration.md         # Integration testing
│
├── review/                      # Code review commands
│   ├── code-review.md              # Code quality review
│   └── architecture-review.md      # Architecture review
│
└── plans/                       # Generated learning plans
    └── YYYY-MM-DD-[topic]-learning-plan.md
```

---

## Teaching Specialists

### 1. **learning-coordinator**
**Role:** Master orchestrator of the learning journey

**Responsibilities:**
- Coordinates all teaching specialists
- Tracks overall learning progress
- Maintains student learning profile
- Ensures teaching consistency
- Provides encouragement and motivation

**When Engaged:**
- All learning sessions start here
- Coordinates between specialists
- Manages learning plans
- Tracks understanding checkpoints

**Student Profile (Customizable):**
```markdown
### Experience Level
- ROS2: Beginner
- Python: Intermediate
- Robotics: Beginner
- Hardware: Beginner

### Learning Style
- Hands-on experimentation
- Deep understanding over speed
- Real-world robotics examples
```

---

### 2. **plan-generation-mentor**
**Role:** Creates educational learning plans

**Specializes In:**
- Breaking complex features into learning phases
- Creating research tasks and design exercises
- Mapping specialists to learning phases
- Building understanding checkpoints
- Structuring learning journals

**Creates Plans With:**
- Learning objectives (concepts & skills)
- Prerequisites checks
- Progressive phases (research → design → implement → reflect)
- Specialist coordination map
- Understanding milestones
- Reflection prompts

**Example Plan Structure:**
```markdown
# Feature Name - Learning Implementation Plan

## Learning Objectives
- Concepts to understand
- Skills to develop

## Prerequisites Check
- Required knowledge

## Learning Phases
### Phase 1: Understanding & Research
- Research tasks
- Understanding checkpoints
- Specialist: [who helps]

### Phase 2: Design & Architecture
- Design exercises
- Decision points
- Specialist: [who helps]

[... more phases ...]

## Learning Journal
[Space for reflections]
```

---

### 3. **ros2-learning-mentor**
**Role:** ROS2 concepts and architecture teacher

**Specializes In:**
- ROS2 nodes, topics, services, actions
- Message types and communication
- Launch files and packages
- Coordinate transforms (tf2)
- ROS2 best practices

**Teaching Approach:**
- Safety-first for hardware integration
- Concept explanation before code
- Structure guidance, not complete nodes
- Integration and testing strategies
- Progressive learning steps

**Key Topics:**
- Publisher/Subscriber patterns
- Node lifecycle and architecture
- QoS profiles and communication
- Parameter handling
- ROS2 ecosystem understanding

---

### 4. **code-architecture-mentor**
**Role:** Design patterns and software architecture teacher

**Specializes In:**
- 10 Design Patterns with robotics examples
- SOLID principles
- System architecture design
- Component interaction patterns
- Code organization

**Design Patterns Taught:**

**Creational:**
- Factory Pattern (sensor creation)
- Singleton Pattern (hardware resources)
- Builder Pattern (robot configuration)

**Structural:**
- Strategy Pattern (algorithm switching)
- Observer Pattern (event-driven systems)
- Adapter Pattern (interface compatibility)
- Decorator Pattern (feature composition)

**Behavioral:**
- State Pattern (operational modes)
- Command Pattern (command queuing)
- Template Method (common workflows)

**Teaching Method:**
- Present 2-3 pattern options for problem
- Explain trade-offs of each
- Guide selection based on specific needs
- Teach chosen pattern conceptually
- Guide implementation design

**Pattern Selection Guide:**
```markdown
Problem: Multiple sensor types to create
→ Consider: Factory, Abstract Factory, Builder
→ Questions: Creation complexity? Related groups? Config options?
→ Guide to best choice

Problem: Different navigation algorithms
→ Consider: Strategy, State, Template Method
→ Questions: When chosen? Share structure? State-dependent?
→ Guide to best choice
```

---

### 5. **python-best-practices**
**Role:** Pythonic patterns and code quality teacher

**Specializes In:**
- Pythonic thinking and idioms
- Code readability and style
- Performance optimization
- Data structures and algorithms
- Type hints and documentation

**Teaching Focus:**
- Show Pythonic alternatives
- Guide code improvement
- Explain performance implications
- Teach stdlib usage

---

### 6. **cpp-best-practices**
**Role:** Modern C++ and real-time systems teacher

**Specializes In:**
- Modern C++ (C++14/17/20)
- Real-time programming
- Memory management (RAII, smart pointers)
- Robotics-specific C++ patterns
- Performance optimization

**Key Topics:**
- RAII and resource management
- Move semantics
- Real-time constraints
- Lock-free programming
- Hardware abstraction

---

### 7. **robotics-vision-navigator**
**Role:** Computer vision and navigation teacher

**Specializes In:**
- Computer vision concepts
- SLAM algorithms
- Path planning (A*, RRT, Dijkstra)
- Object detection
- Sensor fusion

**Teaching Approach:**
- Concept explanations first
- Algorithm comparison and trade-offs
- Progressive complexity
- Reference implementations (teacher use only)

**Key Topics:**
- Camera calibration theory
- Feature detection concepts
- Navigation algorithms
- Obstacle avoidance strategies
- Map representation

---

### 8. **jetank-hardware-specialist**
**Role:** Hardware integration and safety teacher

**Specializes In:**
- GPIO and PWM control
- Motor controllers
- Sensor interfacing
- JETANK-specific hardware
- Safety-first practices

**Safety Protocol (Always First):**
- Discuss testing environment
- Explain safety implications
- Provide emergency stop procedures
- Start with minimal power
- Incremental testing

**Hardware Topics:**
- Motor control (PWM, H-bridge)
- Sensor integration (I2C, SPI)
- Servo control (PCA9685)
- Power management
- Hardware testing strategies

---

### 9. **debugging-detective**
**Role:** Systematic debugging methodology teacher

**Specializes In:**
- Debugging approaches
- Problem investigation
- Error analysis
- Systematic troubleshooting

**Teaching Method:**
- Never fix bugs directly
- Teach investigation process
- Guide hypothesis formation
- Help test hypotheses
- Verify the fix

**Debugging Process:**
1. Problem definition
2. Information gathering
3. Hypothesis formation
4. Systematic testing
5. Analysis and verification

---

### 10. **testing-specialist**
**Role:** Testing strategies and TDD teacher

**Specializes In:**
- Test design principles
- Unit testing strategies
- Integration testing
- TDD methodology
- Robotics-specific testing

**Testing Pyramid:**
- Many unit tests (70%)
- Some integration tests (20%)
- Few system tests (10%)

**Teaching Focus:**
- What to test and why
- Test structure guidance
- Guide test design
- Don't write tests for them

---

### 11. **git-workflow-expert**
**Role:** Version control and collaboration teacher

**Specializes In:**
- Git concepts and mental models
- Branching strategies
- Commit best practices
- Collaboration workflows

**Teaching Approach:**
- Teach Git thinking, not just commands
- Explain "why" behind practices
- Guide workflow selection
- Help understand and recover from problems

---

### 12. **documentation-generator**
**Role:** Technical writing and documentation teacher

**Specializes In:**
- API documentation
- Technical writing
- Code comments
- README files

**Teaching Approach:**
- Guide what to document
- Provide templates to adapt
- Help improve their writing
- Don't write docs for them

---

## Commands Reference

### Learning Plan Commands

#### `/create-plan [feature-name]`

**Purpose:** Generate a comprehensive learning-focused implementation plan

**What It Creates:**
- Multi-week learning journey
- Progressive learning phases
- Research tasks and design exercises
- Understanding checkpoints
- Specialist coordination map
- Learning journal structure

**Example:**
```bash
/create-plan autonomous-navigation
```

**Output:** `plans/2025-10-01-autonomous-navigation-learning-plan.md`

**Use When:**
- Starting complex multi-week project
- Need structured learning approach
- Multiple concepts to learn
- Want to coordinate specialists

**Plan Structure:**
```markdown
# [Feature] - Learning Implementation Plan

## Learning Objectives
- What you'll learn
- Skills you'll develop

## Prerequisites Check
- Required knowledge

## Learning Phases
### Phase 1: Understanding & Research (Week 1-2)
- Research tasks
- Design exercises
- Understanding checkpoint
- Specialist: [agent]

### Phase 2: Design & Architecture (Week 3-4)
[...]

## Learning Team
- Which specialists help where

## Learning Milestones
- Phase completion criteria

## Learning Journal
- Session reflections
```

---

#### `/continue-plan`

**Purpose:** Resume learning from existing plan

**What It Does:**
- Loads most recent learning plan
- Assesses current progress
- Reviews learning journal
- Provides warm welcome back
- Offers options: continue/review/assess/adjust

**Example:**
```bash
/continue-plan
```

**Provides:**
```markdown
## Welcome Back!

### Where We Left Off
[Progress summary]

### What You've Learned
✅ Concept 1
✅ Concept 2
🔄 Currently working on...

### Options:
1. Continue learning
2. Review previous concepts
3. Take assessment
4. Adjust plan
5. Switch focus

What would you like to do?
```

**Use When:**
- Returning to learning session
- Been away and need context
- Want progress summary
- Ready to continue

---

#### `/update-plan`

**Purpose:** Document progress and reflections

**What It Updates:**
- Task completion status
- Learning journal entries
- Understanding checkpoint progress
- Phase completion
- Specialist consultations

**Example:**
```bash
/update-plan
```

**Updates With:**
```markdown
### [Date] - Session Notes

**Concepts Explored:**
- [What studied]

**Key Insights:**
- [What clicked]

**Challenges:**
- [What was hard]

**Practice Done:**
- [What implemented]

**Understanding:**
- Can explain: [A, B]
- Still unclear: [C]

**Questions:**
- [Open questions]
```

**Use When:**
- After completing learning tasks
- End of learning session
- Want to reflect
- Before phase transition

---

### Learning Session Commands

#### `/start-learning [topic]`

**Purpose:** Begin new guided learning experience

**What It Does:**
- Assesses experience level
- Checks prerequisites
- Determines approach (simple vs complex)
- Creates plan or starts direct teaching
- Engages appropriate specialists
- Sets clear expectations

**Examples:**
```bash
# Simple topic
/start-learning PID controllers
→ Direct teaching session (1-2 hours)

# Complex project
/start-learning autonomous navigation
→ Full learning plan (6-8 weeks)

# Hardware topic
/start-learning motor control
→ Safety-first approach
```

**Process:**
1. Understand request
2. Quick assessment
3. Decide approach
4. Set expectations
5. Begin learning

**Use When:**
- Starting new topic
- Want guided approach
- Need level assessment
- Beginning learning journey

---

#### `/ask-specialist [question or topic]`

**Purpose:** Connect with appropriate teaching specialist

**What It Does:**
- Analyzes your question
- Routes to best specialist
- Provides context to specialist
- Monitors teaching quality
- Follows up after session

**Examples:**
```bash
/ask-specialist How do ROS2 transforms work?
→ ros2-learning-mentor

/ask-specialist Strategy vs State pattern?
→ code-architecture-mentor

/ask-specialist My node is crashing
→ debugging-detective

/ask-specialist Safe motor control
→ jetank-hardware-specialist
```

**Routing Logic:**
- ROS2/robotics concepts → ros2-learning-mentor
- Vision/navigation → robotics-vision-navigator
- Hardware → jetank-hardware-specialist
- Python code → python-best-practices
- C++ code → cpp-best-practices
- Design patterns → code-architecture-mentor
- Testing → testing-specialist
- Debugging → debugging-detective
- Git → git-workflow-expert
- Documentation → documentation-generator

**Use When:**
- Have specific question
- Stuck on concept
- Need design guidance
- Want expert help

---

#### `/check-understanding [topic]`

**Purpose:** Verify comprehension through discussion

**What It Does:**
- Assesses depth of understanding
- Uses progressive questioning
- Provides constructive feedback
- Identifies gaps
- Determines readiness to proceed

**Examples:**
```bash
/check-understanding ROS2 transforms
/check-understanding Strategy pattern
/check-understanding Phase 1
```

**Assessment Levels:**
1. **Factual** - What is it?
2. **Conceptual** - Why does it work?
3. **Applied** - When to use it?
4. **Evaluative** - Trade-offs?
5. **Creative** - How to extend it?

**Outcomes:**
- 🟢 **Strong** - Ready to proceed
- 🟡 **Partial** - More practice needed
- 🔴 **Limited** - Review with specialist

**Use When:**
- Before advancing phases
- Verify learning
- Unsure if ready
- Checkpoint assessment

---

### ROS2 Commands

#### `/learn-ros2-node [node-purpose]`

**Purpose:** Learn to create ROS2 node (teaching approach)

**What It Does:**
- Discusses node design first
- Teaches ROS2 concepts
- Guides implementation (not complete code)
- Shows testing strategies
- Helps with integration

**Example:**
```bash
/learn-ros2-node motor controller
```

**Teaching Flow:**
1. Understand node purpose
2. Design discussion
3. ROS2 pattern teaching
4. Package organization
5. Implementation guidance
6. Message type selection
7. Testing strategy
8. Common pitfalls
9. Integration points
10. Next steps

**Use When:**
- Learning ROS2
- First time creating nodes
- Want to understand structure
- Need design guidance

---

#### `/new-node [node-purpose]`

**Purpose:** Generate production ROS2 node

**What It Does:**
- Creates complete node implementation
- Sets up package structure
- Includes launch files
- Adds tests and documentation

**Example:**
```bash
/new-node camera processor
```

**Use When:**
- Already understand ROS2
- Need production code
- Quick node skeleton
- Not in learning mode

---

## Learning Workflows

### Workflow 1: Simple Concept Learning

**Scenario:** "I want to understand PID controllers"

```
┌─────────────────────────────┐
│ /start-learning PID control │
└──────────┬──────────────────┘
           │
    ┌──────▼────────────────────┐
    │ Learning Coordinator      │
    │ - Assesses: Simple topic  │
    │ - Direct teaching chosen  │
    └──────┬────────────────────┘
           │
    ┌──────▼────────────────────────┐
    │ code-architecture-mentor      │
    │ - Explains PID concepts       │
    │ - Shows control loop patterns │
    │ - Guides simple implementation│
    └──────┬────────────────────────┘
           │
    ┌──────▼──────────────────────┐
    │ Student implements          │
    │ with guidance               │
    └──────┬──────────────────────┘
           │
    ┌──────▼───────────────────────┐
    │ /check-understanding PID     │
    │ - Verify comprehension       │
    │ - Ready to use in projects!  │
    └──────────────────────────────┘
```

**Timeline:** 1-2 sessions
**Outcome:** Understanding + simple implementation

---

### Workflow 2: Complex Feature Development

**Scenario:** "I want to build autonomous navigation"

```
Day 1:
┌────────────────────────────────────┐
│ /start-learning autonomous-nav     │
└──────────┬─────────────────────────┘
           │
    ┌──────▼──────────────────────────┐
    │ Learning Coordinator            │
    │ - Assesses: Complex project     │
    │ - Delegates to plan-generation  │
    └──────┬──────────────────────────┘
           │
    ┌──────▼──────────────────────────┐
    │ plan-generation-mentor          │
    │ - Creates 6-8 week learning plan│
    │ - Maps 5 phases with checkpoints│
    │ - Identifies specialists needed │
    └──────┬──────────────────────────┘
           │
           ▼
plans/2025-10-01-autonomous-nav-learning-plan.md

    ┌──────────────────────────────────┐
    │ Phase 1: Understanding (Week 1-2)│
    │ - Research path planning         │
    │ - Study SLAM concepts            │
    │ - Compare algorithms             │
    │ Specialist: robotics-vision      │
    └──────┬───────────────────────────┘
           │
Day 3:     ▼
┌──────────────────────────────────────┐
│ /ask-specialist A* vs RRT?           │
│ → robotics-vision-navigator          │
│   - Explains comparison              │
│   - Guides decision factors          │
└──────┬───────────────────────────────┘
       │
Day 7: ▼
┌──────────────────────────────────────┐
│ /update-plan                          │
│ - Document research completed        │
│ - Reflection on algorithms learned   │
│ - Questions for Phase 2              │
└──────┬───────────────────────────────┘
       │
Day 10:▼
┌──────────────────────────────────────┐
│ /check-understanding Phase 1         │
│ - Can explain algorithms?            │
│ - Understand trade-offs?             │
│ - Ready for design phase?            │
│ → ✅ Cleared to proceed              │
└──────┬───────────────────────────────┘
       │
Day 11:▼
┌──────────────────────────────────────┐
│ /continue-plan                        │
│ Phase 2: Design & Architecture       │
│ - System architecture design         │
│ - Component interaction              │
│ Specialist: code-architecture-mentor │
└──────────────────────────────────────┘

[Continues through Phases 3, 4, 5...]
```

**Timeline:** 6-8 weeks
**Outcome:** Deep understanding + working system

---

### Workflow 3: Getting Unstuck

**Scenario:** "My navigation node crashes"

```
┌─────────────────────────────────────────┐
│ /ask-specialist My nav node crashes    │
└──────────┬──────────────────────────────┘
           │
    ┌──────▼────────────────────────────┐
    │ Learning Coordinator              │
    │ - Identifies: Debugging issue     │
    │ - Routes to: debugging-detective  │
    └──────┬────────────────────────────┘
           │
    ┌──────▼────────────────────────────┐
    │ debugging-detective               │
    │ - Teaches investigation process   │
    │ - Guides hypothesis formation     │
    │ - Helps test hypotheses           │
    │ - Student finds & fixes bug       │
    └──────┬────────────────────────────┘
           │
           ▼
    Bug understood and fixed!
    Learning: Systematic debugging
```

**Timeline:** 1 session
**Outcome:** Bug fixed + debugging skills learned

---

### Workflow 4: Design Decision Help

**Scenario:** "I have 3 algorithms, how to structure?"

```
┌─────────────────────────────────────────────┐
│ /ask-specialist 3 algorithms, structure?   │
└──────────┬──────────────────────────────────┘
           │
    ┌──────▼────────────────────────────────┐
    │ Learning Coordinator                  │
    │ - Identifies: Design pattern question │
    │ - Routes to: code-architecture-mentor │
    └──────┬────────────────────────────────┘
           │
    ┌──────▼────────────────────────────────────┐
    │ code-architecture-mentor                  │
    │ - Asks: When are algorithms chosen?       │
    │ - Compares: Strategy vs State vs Template │
    │ - Explains trade-offs                     │
    │ - Guides: Strategy pattern chosen         │
    │ - Teaches pattern conceptually            │
    │ - Student designs implementation          │
    └──────┬────────────────────────────────────┘
           │
           ▼
    Design completed with pattern knowledge!
```

**Timeline:** 1 session
**Outcome:** Solution designed + pattern learned

---

### Workflow 5: ROS2 Node Creation

**Scenario:** "Learn to create sensor node"

```
┌─────────────────────────────────────┐
│ /learn-ros2-node sensor processor   │
└──────────┬──────────────────────────┘
           │
    ┌──────▼────────────────────────┐
    │ ros2-learning-mentor          │
    │ - Discusses node purpose      │
    │ - Design questions            │
    │ - Teaches node structure      │
    │ - Guides implementation       │
    │ - Testing strategies          │
    └──────┬────────────────────────┘
           │
           ▼
    Student implements node
    with guidance (not complete code)
           │
           ▼
┌──────────────────────────────────────┐
│ Node working!                        │
│ Understanding: ROS2 node structure   │
│ Can now create other nodes           │
└──────────────────────────────────────┘
```

**Timeline:** 1-2 sessions
**Outcome:** Working node + ROS2 understanding

---

## Best Practices

### For Students

#### 1. **Start with Clear Goals**

**Good:**
- "I want to understand how SLAM works and implement basic version"
- "Learn ROS2 well enough to build custom nodes"
- "Master design patterns for robotics applications"

**Bad:**
- "Make my robot work"
- "Generate navigation code"
- "Fix everything"

#### 2. **Be Honest About Experience Level**

The system adapts to your level:
- **Beginner** - More concept teaching, simpler exercises
- **Intermediate** - Balanced guidance, medium complexity
- **Advanced** - Less guidance, complex challenges

Don't pretend to know more or less than you do!

#### 3. **Use Learning Journal Regularly**

Document after each session:
- What you learned (not just did)
- What clicked or made sense
- What's still confusing
- Questions for next time

**Why:** Reflection solidifies learning!

#### 4. **Verify Understanding Before Advancing**

Use `/check-understanding` at phase boundaries:
- Can you explain concepts?
- Can you apply to new situations?
- Do you understand trade-offs?

**Don't rush** - solid foundations matter!

#### 5. **Ask Questions Freely**

Use `/ask-specialist` whenever stuck:
- No question is too simple
- Better to ask than guess
- Specialists are patient teachers
- Questions show you're thinking!

#### 6. **Practice Active Learning**

- **Research** concepts yourself first
- **Try** implementations before asking
- **Experiment** with approaches
- **Debug** your own code first
- **Reflect** on what you learn

**Don't:** Wait for answers to be given!

#### 7. **Take Time for Reflection**

After completing phases:
- What was most valuable?
- What would you do differently?
- How does this connect to other learning?
- What do you want to explore deeper?

#### 8. **Maintain Consistent Pace**

Learning is a marathon, not a sprint:
- Regular sessions better than cramming
- Take breaks when frustrated
- Let concepts "marinate"
- Revisit difficult topics

#### 9. **Celebrate Progress**

Acknowledge milestones:
- Completed phases
- Concepts mastered
- Working implementations
- Teaching others what you learned

#### 10. **Build on Fundamentals**

Master basics before advancing:
- Understand core concepts deeply
- Practice fundamental skills
- Don't skip "boring" parts
- Foundation enables advanced work

---

### For Effective Learning Sessions

#### Before Session

**Prepare:**
- Review previous session notes
- Think about questions from last time
- Try researching concepts first
- Have development environment ready

#### During Session

**Engage Actively:**
- Ask "why" and "how" questions
- Explain your thinking
- Try approaches before asking
- Take notes on key insights

**Don't:**
- Just copy examples
- Skip understanding for speed
- Avoid difficult concepts
- Multitask during learning

#### After Session

**Consolidate:**
- Update learning journal
- Implement what you learned
- Test your understanding
- Identify next questions

---

### For Working with Specialists

#### Getting Best Help

**Good Questions:**
- "I'm trying to understand [concept]. Can you explain [specific part]?"
- "I researched [topic] and think [understanding]. Is that right?"
- "I'm choosing between [A] and [B]. What factors should I consider?"
- "I tried [approach] but [result]. What might I be missing?"

**Less Effective:**
- "How do I do [task]?" (too broad)
- "Give me code for [feature]" (not learning)
- "This is broken, fix it" (no learning)

#### Understanding Teaching Style

Specialists will:
- ✅ Explain concepts and principles
- ✅ Ask questions to guide thinking
- ✅ Show small examples (2-5 lines)
- ✅ Present options with trade-offs
- ✅ Verify understanding

They won't:
- ❌ Write complete solutions
- ❌ Make decisions for you
- ❌ Skip conceptual understanding
- ❌ Provide copy-paste code

#### If Stuck with Specialist

- Ask for different explanation
- Request analogy or example
- Break down into smaller parts
- Try different specialist
- Use `/ask-specialist` to switch

---

## Customization Guide

### Customizing Student Profile

Edit `agents/learning-coordinator.md`:

```markdown
## My Student Learning Profile

### Experience Level
- ROS2: [Your level]
- Python: [Your level]
- Robotics: [Your level]
- Hardware: [Your level]

### Learning Style Preferences
- Approach: [Your preference]
- Pace: [Your preference]
- Feedback: [Your preference]
- Challenge: [Your preference]
- Examples: [Your preference]

### Teaching Adaptations
- [How specialists should adapt to you]
```

### Customizing Specialist Teaching

Edit individual agent files in `agents/`:

**Example - Adjusting code-architecture-mentor:**
```markdown
## My Focus Areas
- Emphasize: [Patterns you want to focus on]
- De-emphasize: [Patterns less relevant]
- Examples from: [Your domain]
- Challenge level: [Adjust difficulty]
```

### Customizing Commands

Edit command files in `commands/`:

**Example - Adjusting create-plan:**
```markdown
### 2. Create Learning-Focused Plan

Adjust phase structure:
- Phase 1: [Your preferred structure]
- Phase 2: [Your preferred structure]
- Timeline: [Your available time]
```

### Adding Custom Specialist

Create new agent file in `agents/`:

```markdown
---
name: your-specialist
description: [What they teach]
tools: read, write, bash, python
model: sonnet
---

You are [role description]

## TEACHING APPROACH
[Your teaching principles]

## Specialization
[What they know]

## Teaching Method
[How they teach]
```

Then add to learning-coordinator's specialist list.

### Customizing Plan Templates

Edit `agents/plan-generation-mentor.md`:

```markdown
## Plan Template Structure

Adjust template sections:
- Required: [Your must-haves]
- Optional: [Your nice-to-haves]
- Format: [Your preferences]
```

---

## Troubleshooting

### Common Issues

#### "Learning is too slow"

**Problem:** Want faster progress
**Solution:**
- Remember: Understanding vs speed trade-off
- Can use `/new-node` for production when you already understand
- Learning compounds - invest time now, go faster later
- Adjust plan timeline in `/update-plan` if needed

#### "Specialist not giving complete code"

**Problem:** Expected code generation
**Solution:**
- This is intentional! Teaching approach.
- Specialists guide, don't solve
- You learn by implementing yourself
- Request patterns/examples: "Can you show a small example?"

#### "Don't know which specialist to ask"

**Problem:** Unsure who to consult
**Solution:**
- Use `/ask-specialist [question]` - learning-coordinator routes
- Check specialist list in this guide
- Try one - coordinator will redirect if wrong
- Learning plans specify specialists per phase

#### "Checkpoint questions too hard"

**Problem:** Understanding check failing
**Solution:**
- Not failure - identifying gaps!
- Ask specialist to re-explain differently
- Break concept into smaller parts
- More practice with concept needed
- Understanding takes time - be patient

#### "Lost track in complex learning plan"

**Problem:** Confused about progress
**Solution:**
- Use `/continue-plan` - shows status
- Review learning journal
- Use `/check-understanding` for current phase
- Can adjust plan with `/update-plan`
- Ask learning-coordinator for summary

#### "Multiple specialists saying different things"

**Problem:** Conflicting advice
**Solution:**
- Different perspectives are valuable!
- Ask for clarification: "How does this relate to [other advice]?"
- Learning-coordinator can reconcile
- Often both valid - context dependent

#### "Forgot what I learned previously"

**Problem:** Memory gaps
**Solution:**
- Review learning journal regularly
- Use spaced repetition
- Teach concepts to someone else
- Re-do checkpoints periodically
- Regular `/update-plan` helps retention

#### "Want to skip boring parts"

**Problem:** Fundamentals seem tedious
**Solution:**
- Fundamentals enable advanced work
- Try applying to interesting project
- Ask specialist: "Why is this important?"
- Small time investment, big payoff
- Can't build on shaky foundation

#### "Specialist session went off track"

**Problem:** Not addressing your question
**Solution:**
- Redirect: "Going back to my original question..."
- Be specific about what you need
- Try different specialist
- Ask learning-coordinator to intervene

---

### Getting Additional Help

1. **Use `/ask-specialist`** for specific issues
2. **Review this guide** for clarification
3. **Check command documentation** in COMMANDS_README.md
4. **Look at agent files** in `agents/` folder
5. **Review example learning plans** in `plans/` folder

---

## Appendix

### Quick Reference Cards

#### Commands Quick Reference
```
Learning Plans:
  /create-plan [feature]     - Generate learning plan
  /continue-plan             - Resume learning
  /update-plan               - Track progress

Learning Sessions:
  /start-learning [topic]    - Begin journey
  /ask-specialist [question] - Get expert help
  /check-understanding [topic] - Verify learning

ROS2:
  /learn-ros2-node [purpose] - Learn node creation
  /new-node [purpose]        - Generate node (prod)
```

#### Specialists Quick Reference
```
Planning:
  learning-coordinator       - Master orchestrator
  plan-generation-mentor     - Creates learning plans

Core Learning:
  ros2-learning-mentor       - ROS2 teacher
  python-best-practices      - Python teacher
  cpp-best-practices         - C++ teacher
  code-architecture-mentor   - Design patterns teacher

Domain Experts:
  robotics-vision-navigator  - Vision/nav teacher
  jetank-hardware-specialist - Hardware teacher
  debugging-detective        - Debug methodology
  testing-specialist         - Testing teacher

Dev Tools:
  git-workflow-expert        - Git teacher
  documentation-generator    - Doc writing teacher
```

#### Learning Phase Pattern
```
Phase 1: Understanding & Research
  → Study concepts
  → Compare approaches
  → Design thinking

Phase 2: Design & Architecture
  → System design
  → Component planning
  → Pattern selection

Phase 3: Basic Implementation
  → Core functionality
  → Guided building
  → Iterative development

Phase 4: Enhancement & Quality
  → Feature completion
  → Testing & optimization
  → Code quality

Phase 5: Reflection & Mastery
  → Learning consolidation
  → Teaching others
  → Project completion
```

---

### Learning Resources

#### ROS2 Learning
- Official ROS2 Documentation
- ROS2 Tutorials (for concepts, not copy)
- `ros2 --help` command exploration

#### Design Patterns
- Gang of Four patterns (research)
- Refactoring Guru (visual examples)
- Your own code-architecture-mentor agent!

#### Python
- Python official docs
- Real Python (concepts)
- Your python-best-practices agent

#### C++
- CPP Reference
- Modern C++ guides
- Your cpp-best-practices agent

#### Robotics
- Robotics textbooks (concepts)
- Research papers (algorithms)
- Your robotics specialists!

---

### Glossary

**Learning Plan** - Structured multi-week educational journey with phases, checkpoints, and reflection

**Learning Phase** - Stage of learning focusing on specific aspect (research, design, implement, reflect)

**Understanding Checkpoint** - Verification point where comprehension is assessed before proceeding

**Learning Journal** - Reflection space documenting insights, challenges, and progress

**Teaching Specialist** - AI agent specialized in teaching specific domain through guided learning

**Learning Coordinator** - Master orchestrator managing overall learning journey and specialist coordination

**Progressive Learning** - Building understanding in stages from fundamentals to advanced

**Active Learning** - Learning by doing, researching, and implementing rather than passive receiving

**Guided Discovery** - Teaching approach where student discovers solutions with guidance

**Pattern** - Small code example (2-5 lines) showing structure, not complete solution

---

## Conclusion

The Claude Code Learning System is designed to help you **truly learn** programming and robotics, not just generate working code.

### Key Takeaways

1. **Understanding > Speed** - Take time to learn deeply
2. **You Build It** - With guidance, not for you
3. **Progressive Learning** - Fundamentals → Advanced
4. **Verify Understanding** - Before advancing
5. **Reflect Regularly** - Consolidate learning
6. **Ask Questions** - Specialists are here to teach
7. **Practice Actively** - Learn by doing
8. **Be Patient** - Deep learning takes time

### Your Learning Journey Starts Here

```bash
# Ready to begin?
/start-learning [your-topic]

# Have a question?
/ask-specialist [your-question]

# Starting a big project?
/create-plan [your-feature]
```

**Remember:** You're not using an AI code generator - you're working with a personal teaching team dedicated to your learning success! 🎓🚀

Happy Learning! 🌟
