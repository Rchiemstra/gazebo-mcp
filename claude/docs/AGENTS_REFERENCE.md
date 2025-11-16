# Agents Reference

Quick reference for all available teaching agents in the Claude Learning System.

**Last Updated**: 2025-10-09
**Total Agents**: 14

---

## 🎯 Quick Selection Guide

**Need to learn a concept?**
- General learning → `learning-coordinator`
- ROS2 concepts → `ros2-learning-mentor`
- Design patterns → `code-architecture-mentor`
- Vision/navigation → `robotics-vision-navigator`
- Ask any specialist → `/ask-specialist <question>`

**Need a project plan?**
- Context-aware plan → `/create-project-plan <feature>`
- Learning-focused plan → `/create-plan <feature>`

**Need code review/guidance?**
- Python code → `python-best-practices`
- C++ code → `cpp-best-practices`
- Architecture → `code-architecture-mentor`

**Need help debugging?**
- Systematic debugging → `debugging-detective`

**Need documentation help?**
- Writing docs → `documentation-generator`

**Need testing guidance?**
- Test design → `testing-specialist`

**Need hardware help?**
- JETANK robot → `jetank-hardware-specialist`

**Need Git help?**
- Version control → `git-workflow-expert`

---

## 📋 All Agents by Category

### Coordinators (Proactive)
Orchestrate learning experiences and coordinate other agents.

#### learning-coordinator
- **Purpose**: Master learning orchestrator for comprehensive coding education
- **When to use**: Any learning request, general guidance
- **Tools**: Read, Write, Bash, Python
- **Activation**: Proactive
- **Special features**: Reflection-first approach, coordinates all specialists
- **Example**: "I want to learn autonomous navigation"

#### project-plan-orchestrator
- **Purpose**: Creates context-aware project plans by coordinating file search and planning agents
- **When to use**: Need comprehensive project plan with codebase analysis
- **Tools**: Read, Write, Task, Glob
- **Activation**: Proactive
- **Special features**: Sequential workflow management, state tracking
- **Example**: `/create-project-plan add obstacle avoidance`

---

### Planning & Structure (Proactive)

#### plan-generation-mentor
- **Purpose**: Creates detailed, educational implementation plans
- **When to use**: Need structured learning journey for complex features
- **Tools**: Read, Write
- **Activation**: Proactive
- **Special features**: Progressive phases, learning checkpoints, journal structure
- **Example**: "Create a learning plan for SLAM implementation"

---

### Domain Specialists - ROS2 & Robotics (Proactive)

#### ros2-learning-mentor
- **Purpose**: ROS2 concepts and robotics teaching specialist
- **When to use**: Learning ROS2 nodes, topics, services, navigation stack
- **Tools**: Read, Write, Bash, Python
- **Activation**: Proactive
- **Special features**: Safety-first teaching protocol, hardware awareness
- **Example**: "Teach me about ROS2 publishers and subscribers"

#### robotics-vision-navigator
- **Purpose**: Computer vision and autonomous navigation teaching specialist
- **When to use**: SLAM, object detection, path planning, sensor fusion
- **Tools**: Read, Write, Bash, Python
- **Activation**: Proactive
- **Special features**: Progressive vision learning (Weeks 1-12), algorithm comparison
- **Example**: "Help me understand visual SLAM"

#### jetank-hardware-specialist
- **Purpose**: JETANK robot hardware integration teaching specialist
- **When to use**: Sensor integration, motor control, GPIO, hardware safety
- **Tools**: Read, Write, Bash, Python
- **Activation**: Proactive
- **Special features**: Safety-first protocols, hardware checklists, incremental testing
- **Example**: "How do I safely control the JETANK motors?"

---

### Development Specialists (Manual)

#### python-best-practices
- **Purpose**: Python coding standards and performance specialist
- **When to use**: Python code review, Pythonic patterns, performance optimization
- **Tools**: Read, Write, Python
- **Activation**: Manual
- **Special features**: Teaches Pythonic thinking, async patterns, type hints
- **Example**: "Review my Python class design"

#### cpp-best-practices
- **Purpose**: C++ coding standards and modern practices specialist
- **When to use**: C++ code review, modern C++, robotics-specific patterns
- **Tools**: Read, Write, Bash
- **Activation**: Manual
- **Special features**: Modern C++ (C++11/14/17), real-time systems, memory management
- **Example**: "How should I structure my C++ ROS2 node?"

#### code-architecture-mentor
- **Purpose**: Software design patterns and architecture specialist
- **When to use**: Design decisions, refactoring, SOLID principles, pattern selection
- **Tools**: Read, Write, Python
- **Activation**: Manual
- **Special features**: 10 design patterns library, progressive quality levels, pattern comparison
- **Example**: "When should I use Strategy vs State pattern?"

---

### Quality & Process Specialists (Manual)

#### debugging-detective
- **Purpose**: Debugging methodology and troubleshooting specialist
- **When to use**: Systematic bug investigation, debugging strategy
- **Tools**: Read, Write, Bash, Python
- **Activation**: Manual
- **Special features**: Scientific method for bugs, isolation techniques, progressive debugging skills
- **Example**: "Help me debug this ROS2 node that's crashing"

#### testing-specialist
- **Purpose**: Testing methodology and TDD teaching specialist
- **When to use**: Test design, TDD guidance, quality practices
- **Tools**: Read, Write, Bash, Python
- **Activation**: Manual
- **Special features**: TDD cycle teaching, robotics-specific testing
- **Example**: "How should I test my path planning algorithm?"

#### git-workflow-expert
- **Purpose**: Git and version control teaching specialist
- **When to use**: Git workflows, branching strategies, collaborative development
- **Tools**: Read, Write, Bash
- **Activation**: Manual
- **Special features**: Teaches Git thinking, not just commands
- **Example**: "What's the best Git workflow for robotics development?"

#### documentation-generator
- **Purpose**: Technical writing and documentation specialist
- **When to use**: Documentation structure, technical writing, API docs
- **Tools**: Read, Write
- **Activation**: Manual
- **Special features**: Teaches documentation best practices, audience awareness
- **Example**: "Help me structure my project documentation"

---

### Utility Agents (Manual)

#### file-search-agent
- **Purpose**: Searches project files and creates comprehensive markdown documentation
- **When to use**: Need codebase analysis for project planning
- **Tools**: Read, Write, Glob, Grep
- **Activation**: Manual
- **Special features**: Creates `relevant-files-*.md` documents, categorizes by purpose
- **Note**: Usually invoked by `project-plan-orchestrator`, not directly

---

## 🔄 How Agents Work Together

### Common Workflows

**1. Learning Journey**
```
User → learning-coordinator → specialist agents → learning-coordinator (summary)
```

**2. Context-Aware Project Planning**
```
/create-project-plan → project-plan-orchestrator → file-search-agent → plan-generation-mentor
```

**3. Specialized Consultation**
```
/ask-specialist → learning-coordinator routes to → appropriate specialist
```

**4. Guided Implementation**
```
User → plan-generation-mentor (creates plan) → User implements with specialist guidance
```

---

## 🎓 Teaching Philosophy

All agents follow these principles:
- ❌ **NEVER** provide complete solutions
- ✅ **ALWAYS** teach concepts first
- ✅ **ALWAYS** ask guiding questions (Socratic method)
- ✅ **ALWAYS** provide structure, not implementation
- ✅ **ALWAYS** verify understanding with checkpoints

---

## 📌 Activation Modes

### Proactive (6 agents)
Auto-invoked when their domain is mentioned:
- learning-coordinator
- project-plan-orchestrator
- plan-generation-mentor
- ros2-learning-mentor
- robotics-vision-navigator
- jetank-hardware-specialist

### Manual (8 agents)
Invoked explicitly by user or coordinator:
- python-best-practices
- cpp-best-practices
- code-architecture-mentor
- debugging-detective
- testing-specialist
- git-workflow-expert
- documentation-generator
- file-search-agent

---

## 🛠️ Available Tools by Agent

| Agent | Read | Write | Bash | Python | Glob | Grep | Task |
|-------|------|-------|------|--------|------|------|------|
| learning-coordinator | ✓ | ✓ | ✓ | ✓ | | | |
| project-plan-orchestrator | ✓ | ✓ | | | ✓ | | ✓ |
| plan-generation-mentor | ✓ | ✓ | | | | | |
| ros2-learning-mentor | ✓ | ✓ | ✓ | ✓ | | | |
| robotics-vision-navigator | ✓ | ✓ | ✓ | ✓ | | | |
| jetank-hardware-specialist | ✓ | ✓ | ✓ | ✓ | | | |
| python-best-practices | ✓ | ✓ | | ✓ | | | |
| cpp-best-practices | ✓ | ✓ | ✓ | | | | |
| code-architecture-mentor | ✓ | ✓ | | ✓ | | | |
| debugging-detective | ✓ | ✓ | ✓ | ✓ | | | |
| testing-specialist | ✓ | ✓ | ✓ | ✓ | | | |
| git-workflow-expert | ✓ | ✓ | ✓ | | | | |
| documentation-generator | ✓ | ✓ | | | | | |
| file-search-agent | ✓ | ✓ | | | ✓ | ✓ | |

---

## 📚 Related Documentation

- **[SUB_AGENTS_GUIDE.md](./SUB_AGENTS_GUIDE.md)** - Comprehensive guide with examples
- **[PROJECT_PLANNING_SYSTEM.md](./PROJECT_PLANNING_SYSTEM.md)** - Context-aware planning system
- **[COMMANDS_README.md](./COMMANDS_README.md)** - All available slash commands
- **[CREATING_NEW_AGENTS.md](./CREATING_NEW_AGENTS.md)** - How to create new agents

---

## 🔍 Finding the Right Agent

**By Task Type:**
- Learn concept → Domain specialist (ROS2, vision, hardware)
- Review code → Language specialist (Python, C++)
- Design system → code-architecture-mentor
- Debug problem → debugging-detective
- Plan project → plan-generation-mentor or project-plan-orchestrator
- Write tests → testing-specialist
- Document code → documentation-generator
- Git workflow → git-workflow-expert

**By Domain:**
- ROS2 → ros2-learning-mentor
- Computer vision/SLAM → robotics-vision-navigator
- Hardware/sensors → jetank-hardware-specialist
- Python → python-best-practices
- C++ → cpp-best-practices

**Not Sure?**
Start with `learning-coordinator` - it will route you to the right specialist!

---

*This reference is auto-updated when agents are added or modified.*
