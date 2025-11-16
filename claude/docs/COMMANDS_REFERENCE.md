# Commands Reference

This document provides quick access to all command systems available in the Claude Code workspace.

## Quick Links

- **ROS/Robotics Commands:** See `~/.claude/CLAUDE.md` for complete reference
- **Workspace Commands:** See `COMMANDS_README.md` for learning and teaching commands
- **Python Skills API:** See individual skill documentation in `skills/*/SKILL.md`

---

## Command Systems Overview

### 1. ROS/Robotics Commands (67 commands)

**Location:** `~/.claude/commands/`
**Complete Reference:** `~/.claude/CLAUDE.md`

#### Quick Access by Category

**Workflow Commands:**
- `/dev` - Complete development workflow
- `/dev-tdd` - Test-driven development workflow
- `/dev-visual` - Visual development workflow
- `/dev-quick` - Quick prototyping workflow
- `/execute` - Execute predefined tasks
- `/gather-context` - Gather project context
- `/plan` - Create implementation plan

**ROS Commands:**
- `/create-ros-node` - Create new ROS2 node with best practices
- `/ros-debug` - Debug ROS2 node issues
- `/ros-test-gen` - Generate ROS2 tests
- `/ros-launch-mgr` - Manage launch files
- `/ros-msg-design` - Design ROS2 messages
- `/ros-bridge-build` - Build ROS bridges
- `/ros-pkg-create` - Create ROS2 package
- `/cmake-gen` - Generate CMakeLists.txt
- `/package-xml-gen` - Generate package.xml
- `/launch-gen` - Generate launch files
- `/ros-msg-gen` - Generate message definitions
- `/cpp-node-template` - C++ node template
- `/py-node-template` - Python node template

**Verification Commands:**
- `/verify-build` - Verify build succeeds
- `/verify-tests` - Verify tests pass
- `/verify-lint` - Verify code style
- `/verify-ros-node` - Verify ROS node functionality
- `/verify-integration` - Verify system integration

**Git Commands:**
- `/git-stage` - Stage files for commit
- `/git-commit-msg` - Generate commit message
- `/git-commit` - Commit staged changes

**Modbus Commands:**
- `/modbus-bridge` - Create Modbus-ROS bridge
- `/modbus-client-gen` - Generate Modbus client
- `/modbus-server-gen` - Generate Modbus server
- `/modbus-doc` - Document Modbus integration
- `/register-mapper` - Map Modbus registers
- `/modbus-handler` - Handle Modbus communication
- `/register-map-parser` - Parse register maps

**Analysis Commands:**
- `/ros-graph-analyze` - Analyze ROS computation graph
- `/bag-analyze` - Analyze ROS bag files
- `/tf-visualize` - Visualize TF transforms
- `/code-pattern-detect` - Detect code patterns

**Meta Commands:**
- `/create-skill` - Create new command
- `/create-agent` - Create new agent

**And 25+ more commands** - See `~/.claude/CLAUDE.md` for complete list

---

### 2. Learning & Teaching Commands

**Location:** `commands/` and `agents/`
**Complete Reference:** `COMMANDS_README.md`

**Learning Plans:**
- `/create-plan` - Generate educational implementation plans
- `/continue-plan` - Resume learning journey
- `/update-plan` - Track progress and reflect

**Learning Sessions:**
- `/start-learning` - Begin guided learning
- `/ask-specialist` - Consult teaching specialists
- `/check-understanding` - Verify comprehension

**ROS2 Learning:**
- `/learn-ros2-node` - Learn to create ROS2 nodes (teaching approach)
- `/new-node` - Generate ROS2 nodes (production approach)

**Git Learning:**
- `/git-start-feature` - Create feature branch with guidance
- `/git-stage-commit` - Commit with learning feedback

**Teaching Agents:**
- `learning-coordinator` - Main learning coordinator
- `plan-generation-mentor` - Learning plan generation
- `ros2-learning-mentor` - ROS2 concepts teaching
- `code-architecture-mentor` - Design patterns teaching
- And 10+ more specialist agents

---

### 3. Python Skills (Programmatic API)

**Location:** `skills/`
**Usage:** Import-based Python operations

**Available Skills:**
- `code_analysis` - Analyze code quality and complexity
- `test_orchestrator` - Coordinate test execution
- `refactor_assistant` - Suggest code improvements
- `git_workflow_assistant` - Git workflow automation
- `context_manager` - Manage conversation context
- `skill_registry` - Discover available skills
- And more...

**Example Usage:**
```python
from skills.code_analysis import analyze_file, OperationResult
from skills.common.registry import SkillRegistry

# Analyze a file
result = analyze_file("src/main.py", response_format="summary")
if result.success:
    print(result.data)

# Discover available skills
skills = SkillRegistry.discover_skills()
for name, info in skills.items():
    print(f"{name}: {len(info.operations)} operations")
```

**API Documentation:**
Each skill has a `SKILL.md` file with:
- Operation reference
- Parameter documentation
- Usage examples
- Error codes
- Integration patterns

---

## When to Use Each System

### Use ROS/Robotics Commands When:
- You need quick ROS2 development tasks
- Creating packages, nodes, or launch files
- Verifying builds, tests, or code quality
- Following complete workflows (/dev, /dev-tdd)
- Working with Modbus integration
- Debugging ROS nodes

### Use Learning Commands When:
- Learning new concepts or technologies
- Creating multi-week learning plans
- Getting explanations from teaching specialists
- Verifying your understanding
- Tracking learning progress

### Use Python Skills When:
- Building programmatic tools or scripts
- Complex data processing operations
- Integrating with other Python code
- Need fine-grained control over operations
- Building custom agents or workflows

---

## Documentation Locations

| Type | Location | Description |
|------|----------|-------------|
| ROS Commands | `~/.claude/CLAUDE.md` | Complete 67-command reference |
| ROS Patterns | `~/.claude/ros-patterns.md` | ROS2 best practices |
| Context Templates | `~/.claude/context-templates/` | Ready-to-use templates |
| Learning Commands | `COMMANDS_README.md` | Teaching command reference |
| Python Skills | `skills/*/SKILL.md` | Individual skill docs |
| Workspace Design | `docs/TOOL_DESIGN_EXCELLENCE_COMPLETE.md` | Design principles |
| Token Efficiency | `docs/TOKEN_EFFICIENCY_COMPLETE.md` | Optimization guide |

---

## Getting Started

### For ROS Development:
```bash
# Read the complete reference
cat ~/.claude/CLAUDE.md

# Try the complete workflow
/dev "Create a simple ROS2 publisher"

# Or create a node directly
/create-ros-node my_sensor_node python
```

### For Learning:
```bash
# Start a learning journey
/start-learning autonomous navigation

# Get help from specialists
/ask-specialist "How do ROS2 QoS settings work?"
```

### For Programmatic Use:
```python
# Discover what's available
from skills.common.registry import SkillRegistry
skills = SkillRegistry.list_skills()
print(skills)

# Use a skill
from skills.code_analysis import analyze_file
result = analyze_file("path/to/file.py")
```

---

## Additional Resources

- **Installation:** `INSTALLATION.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **SDK Integration:** `docs/SDK_INTEGRATION.md`
- **Git Integration:** `docs/GIT_INTEGRATION.md`
- **MCP Efficiency:** `docs/MCP_EFFICIENCY_SUMMARY.md`

---

**Updated:** 2025-11-10
**Commands Available:** 67 ROS + 8 Learning + 20+ Skills = 95+ tools
