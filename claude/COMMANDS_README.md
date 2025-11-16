# Claude Code Commands - Learning System

This repository contains a comprehensive learning-focused command system for Claude Code, built around teaching programming and robotics concepts rather than just generating code.

## 🎯 Philosophy

All commands follow a **teaching-first approach**:
- **Guide**, don't solve
- **Ask questions**, don't provide answers
- **Teach concepts**, don't write complete code
- **Verify understanding**, don't skip checkpoints
- **Encourage exploration**, don't dictate solutions

## 📚 Command Categories

### 🗺️ Learning Plan Management

#### `/create-plan [feature-name]`
Creates a comprehensive learning-focused implementation plan.

**What it does:**
- Generates educational plan breaking features into learning phases
- Includes research tasks, design exercises, understanding checkpoints
- Maps which specialist agents help in each phase
- Creates learning journal structure for reflection

**Example:**
```bash
/create-plan autonomous-navigation
```

**Output:** `plans/YYYY-MM-DD-autonomous-navigation-learning-plan.md`

**When to use:**
- Complex multi-week projects
- Features requiring multiple concepts
- Want structured learning journey
- Need to coordinate multiple specialists

---

#### `/continue-plan`
Resumes work on an existing learning plan.

**What it does:**
- Loads most recent learning plan
- Assesses current progress and understanding
- Provides warm welcome-back message
- Offers options: continue, review, assess, or adjust
- Coordinates with appropriate specialists

**Example:**
```bash
/continue-plan
```

**When to use:**
- Returning to previous learning session
- Want to pick up where you left off
- Need progress summary
- Ready for next learning phase

---

#### `/update-plan`
Updates learning plan with progress and reflections.

**What it does:**
- Marks completed tasks and checkpoints
- Adds learning journal entries
- Documents insights and challenges
- Verifies understanding before phase completion
- Provides encouragement and next steps

**Example:**
```bash
/update-plan
```

**When to use:**
- After completing learning tasks
- Want to document progress
- Need to reflect on learning
- Before moving to next phase

---

### 🎓 Learning Sessions

#### `/start-learning [topic]`
Begins a new guided learning experience.

**What it does:**
- Assesses your experience level
- Determines if simple guidance or full plan needed
- Engages appropriate specialist agents
- Sets clear learning expectations
- Provides first learning activity

**Examples:**
```bash
/start-learning PID controllers          # Simple topic → Direct teaching
/start-learning autonomous navigation     # Complex → Full learning plan
/start-learning motor control with GPIO   # Hardware → Safety-first approach
```

**When to use:**
- Starting new topic or feature
- Want guided learning experience
- Need assessment of prerequis
ites
- Ready to begin structured learning

---

#### `/ask-specialist [question or topic]`
Connects you with the appropriate teaching specialist.

**What it does:**
- Analyzes your question/need
- Routes to best-suited specialist agent
- Provides context to specialist
- Sets teaching expectations
- Follows up after session

**Examples:**
```bash
/ask-specialist How do ROS2 transforms work?
/ask-specialist I have 3 algorithms, how should I structure my code?
/ask-specialist Why is my navigation node crashing?
/ask-specialist How do I control motors safely?
```

**When to use:**
- Have specific question
- Need expert guidance
- Stuck on a concept
- Want design advice

---

#### `/check-understanding [topic]`
Verifies your understanding through discussion.

**What it does:**
- Assesses depth of understanding (not memorization)
- Uses progressive questioning (factual → conceptual → applied)
- Provides constructive feedback
- Identifies gaps and addresses them
- Determines if ready to proceed

**Examples:**
```bash
/check-understanding ROS2 transforms
/check-understanding Strategy pattern
/check-understanding Phase 1
```

**When to use:**
- Before moving to next phase
- Want to verify learning
- Unsure if ready to proceed
- Need honest assessment

---

### 🤖 ROS2-Specific Commands

#### `/learn-ros2-node [node-purpose]`
Guides you through creating a ROS2 node (teaching approach).

**What it does:**
- Discusses node design before code
- Teaches ROS2 node structure and concepts
- Guides on message types and topics
- Shows testing strategies
- Helps with integration

**Example:**
```bash
/learn-ros2-node sensor data processor
```

**When to use:**
- Learning ROS2 node development
- Want to understand structure
- Need design guidance
- First time creating nodes

---

#### `/new-node [node-purpose]` *(kept for quick generation)*
Creates a production-ready ROS2 node (implementation approach).

**What it does:**
- Analyzes requirements
- Creates node implementation
- Sets up package structure
- Includes testing and documentation

**Example:**
```bash
/new-node camera image processor
```

**When to use:**
- Already understand ROS2 nodes
- Need quick node skeleton
- Production code needed
- Not in learning mode

---

### 🔍 Code Review Commands (in `review/` folder)

#### Code Review
Reviews code quality with teaching focus.

#### Architecture Review
Reviews system architecture and design patterns.

---

### 🧪 Testing Commands (in `ros2/` folder)

#### Debug Node
Helps debug ROS2 nodes systematically.

#### Test Integration
Guides ROS2 integration testing.

---

## 🤖 Available Specialist Agents

The commands coordinate with these teaching specialists:

### Planning & Coordination
- **plan-generation-mentor** - Creates learning-focused plans

### Core Learning
- **ros2-learning-mentor** - ROS2 concepts and architecture
- **python-best-practices** - Pythonic patterns and quality
- **cpp-best-practices** - Modern C++ and real-time systems
- **code-architecture-mentor** - Design patterns and architecture

### Domain Specialists
- **robotics-vision-navigator** - Computer vision, SLAM, navigation
- **jetank-hardware-specialist** - Hardware integration, GPIO, sensors
- **debugging-detective** - Systematic debugging methodology
- **testing-specialist** - Testing strategies and TDD

### Development Tools
- **git-workflow-expert** - Version control workflows
- **documentation-generator** - Technical writing guidance

---

## 📖 Learning Workflow Examples

### Example 1: Simple Concept Learning

```bash
# Quick learning session for specific concept
/start-learning coordinate transforms

# → Direct teaching from ros2-learning-mentor
# → 1-2 session experience
# → Conceptual understanding + simple examples
```

---

### Example 2: Complex Feature Development

```bash
# Day 1: Start learning journey
/start-learning autonomous navigation
# → Creates comprehensive learning plan
# → Phase 1: Understanding & Research begins

# Day 3: Continue learning
/continue-plan
# → Resumes Phase 1
# → Research tasks on path planning

# Day 7: Update progress
/update-plan
# → Documents learning
# → Verifies understanding
# → Ready for Phase 2?

# Day 10: Check understanding before advancing
/check-understanding Phase 1 concepts
# → Assessment through questions
# → Feedback on understanding
# → Cleared to proceed!

# Day 11: Continue to Phase 2
/continue-plan
# → Phase 2: Design & Architecture begins
```

---

### Example 3: Getting Help During Learning

```bash
# While working through learning plan, get stuck
/ask-specialist How do I choose between Strategy and State pattern?

# → Connects with code-architecture-mentor
# → Comparative teaching session
# → Guidance on decision factors
# → Returns to learning plan
```

---

### Example 4: Creating ROS2 Node (Learning Mode)

```bash
# First time creating a node
/learn-ros2-node motor controller

# → Design discussion first
# → ROS2 structure teaching
# → Implementation guidance (not complete code)
# → Testing strategies
# → Integration help
```

---

## 🎯 Quick Reference

### When to Use Which Command

**Starting something new?**
- `/start-learning [topic]`

**Returning to learning?**
- `/continue-plan`

**Made progress?**
- `/update-plan`

**Have a specific question?**
- `/ask-specialist [question]`

**Want to verify understanding?**
- `/check-understanding [topic]`

**Creating ROS2 node (learning)?**
- `/learn-ros2-node [purpose]`

**Creating ROS2 node (production)?**
- `/new-node [purpose]`

---

## 📁 File Organization

```
claude_code/
├── commands/
│   ├── create-plan.md           # Learning plan generation
│   ├── continue-plan.md          # Resume learning
│   ├── update-plan.md            # Progress tracking
│   ├── start-learning.md         # Begin learning journey
│   ├── ask-specialist.md         # Specialist routing
│   └── check-understanding.md    # Understanding verification
│
├── ros2/
│   ├── learn-ros2-node.md       # ROS2 node teaching
│   ├── new-node.md              # ROS2 node generation
│   ├── debug-node.md            # ROS2 debugging
│   └── test-integration.md      # ROS2 integration testing
│
├── review/
│   ├── code-review.md           # Code review guidance
│   └── architecture-review.md   # Architecture review
│
├── agents/
│   └── [14 specialist agents]   # Teaching specialists
│
└── plans/
    └── [Your learning plans]    # Generated plans stored here
```

---

## 🌟 Learning Tips

### For Best Learning Experience:

1. **Start with `/start-learning`** for new topics
2. **Use `/check-understanding`** before advancing phases
3. **Update progress regularly** with `/update-plan`
4. **Ask questions anytime** with `/ask-specialist`
5. **Be patient** - understanding takes time!
6. **Reflect** - use learning journal sections
7. **Practice** - implement what you learn
8. **Iterate** - first attempts don't need to be perfect

### Remember:

- 💭 **Understanding > Speed**: Take time to grasp concepts
- 🔄 **Iterate**: Learn by trying and improving
- ❓ **Ask**: No question is too simple
- 🎯 **Focus**: Master fundamentals first
- 🌱 **Grow**: Challenges are learning opportunities

---

## 🔧 Customization

These commands work with the learning coordinator and specialist agents in the `agents/` folder. The teaching approach can be customized by:

1. **Student Profile**: Update learning-coordinator's student profile
2. **Specialist Agents**: Modify agent teaching styles
3. **Command Behavior**: Edit command `.md` files
4. **Plan Templates**: Adjust plan-generation-mentor templates

---

## 📞 Getting Help

- Use `/ask-specialist` for topic-specific help
- Use `/check-understanding` to verify learning
- Review specialist agent files in `agents/` folder
- Check active learning plan in `plans/` folder

---

## 🎓 Philosophy in Practice

This system treats you as a **learner**, not a code-generation tool user:

**Traditional Approach:**
- "Create navigation system" → Complete code generated
- No learning, just copy-paste
- No understanding of how it works

**This Learning System:**
- "Create navigation system" → Learning plan generated
- Research → Design → Implement → Reflect
- Deep understanding of concepts
- Guided by teaching specialists
- You build it yourself with guidance

**Result:** You learn to build, not just use pre-built code! 🚀

---

## 🔧 Git Automation Commands

### `/git-start-feature [feature-name]`
Creates a new feature branch for development work.

**What it does:**
- Validates current Git state
- Creates appropriately named branch (feature/fix/refactor/etc.)
- Sets up remote tracking
- Prepares for development workflow

**Examples:**
```bash
/git-start-feature stereo-camera
# Creates: feature/stereo-camera

/git-start-feature fix/camera-init
# Creates: fix/camera-init

/git-start-feature refactor/motor-control
# Creates: refactor/motor-control
```

**Branch Types:**
- `feature/<name>` - New features (default)
- `fix/<name>` - Bug fixes
- `refactor/<name>` - Code refactoring
- `docs/<name>` - Documentation
- `test/<name>` - Testing work
- `experimental/<name>` - Experiments

**Delegates to:** git-automation-agent

---

### `/git-stage-commit [message]`
Commits completed development stage with descriptive message.

**What it does:**
- Checks Git status and changed files
- Generates conventional commit message
- Stages and commits changes
- Reports commit details

**Examples:**
```bash
# Auto-generate commit message from context
/git-stage-commit

# Custom stage message
/git-stage-commit "stage 2 - stereo matching implementation"

# Full custom message
/git-stage-commit "feat(perception): add GPU-accelerated stereo matching"
```

**Commit Format:**
Follows Conventional Commits:
```
<type>(<scope>): <description>

- Detailed changes
- More details

Refs: #issue
```

**Types:** feat, fix, refactor, docs, test, perf, chore, build, ci

**Delegates to:** git-automation-agent

**Integration with Plans:**
When working on a plan, automatically includes stage information in commits:
```bash
# Working on plan stage 1
/git-stage-commit
# Commits: "feat(perception): stage 1 - camera interface"
```

---

## 🔄 Git Workflow Integration

### Automated Development Flow

```bash
# 1. Create plan
/create-plan "stereo camera perception"

# 2. Start feature branch
/git-start-feature stereo-camera

# 3. Work on stage 1
# ... code camera interface ...

# 4. Commit stage 1
/git-stage-commit
# → "feat(perception): stage 1 - camera interface"

# 5. Work on stage 2
# ... code stereo processor ...

# 6. Commit stage 2
/git-stage-commit
# → "feat(perception): stage 2 - stereo processor"

# 7. Continue until plan complete
/continue-plan
```

### Benefits
- **Automatic context**: Commits include plan/stage info
- **Consistent naming**: Follows branch and commit conventions
- **Progress tracking**: Git history reflects learning journey
- **Safe automation**: Validates state before operations
- **Error handling**: Recovers from common Git issues

---

Happy Learning! 🎉
