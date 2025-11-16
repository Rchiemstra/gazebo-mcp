# Context-Aware Project Planning System

A sophisticated multi-agent system that creates comprehensive, codebase-aware project plans by orchestrating specialized agents in sequence.

---

## Overview

This system creates **intelligent project plans** that understand your existing codebase by:
1. **Searching** your code to find relevant files
2. **Analyzing** those files to understand structure and patterns
3. **Planning** with full context of what exists and where things should integrate

**Result**: Plans that reference actual files, identify real integration points, and follow existing patterns!

---

## Architecture

### Three Core Agents

#### 1. **project-plan-orchestrator** 🎭
*The conductor of the workflow*

**Role**: Manages sequential execution of agents
- Invokes file-search-agent first
- Waits for codebase analysis completion
- Passes results to plan-generation-mentor
- Monitors workflow and handles errors
- Reports final results to user

**Location**: `agents/project-plan-orchestrator.md`

#### 2. **file-search-agent** 🔍
*The intelligence gatherer*

**Role**: Finds and documents relevant files
- Searches by filename, content, and type
- Reads files to understand purpose
- Analyzes relationships and dependencies
- Identifies integration points
- Creates comprehensive markdown documentation

**Location**: `agents/file-search-agent.md`

**Output**: `project-context/relevant-files-[timestamp].md`

#### 3. **plan-generation-mentor** (Enhanced) 📋
*The educational planner*

**Role**: Creates learning-focused implementation plans
- Now reads codebase context from file-search-agent
- References actual files in the plan
- Identifies specific integration points
- Suggests modifications to existing files
- Follows existing code patterns

**Location**: `agents/plan-generation-mentor.md` (updated)

**Output**: `plans/[date]-[feature]-learning-plan.md`

---

## Workflow Sequence

```
User runs: /create-project-plan [feature description]
    ↓
┌─────────────────────────────────────────────┐
│ project-plan-orchestrator                   │
│ (Coordinates the entire workflow)           │
└─────────────────────────────────────────────┘
    ↓
    ↓ Step 1: Invoke file-search-agent
    ↓
┌─────────────────────────────────────────────┐
│ file-search-agent                           │
│ • Searches codebase with Glob/Grep          │
│ • Analyzes relevant files                   │
│ • Documents findings in markdown            │
│ • Output: project-context/relevant-files... │
└─────────────────────────────────────────────┘
    ↓
    ↓ Step 2: Read analysis results
    ↓
┌─────────────────────────────────────────────┐
│ Verification                                │
│ • Confirm markdown file created             │
│ • Validate file contains useful info        │
│ • Prepare context for next agent            │
└─────────────────────────────────────────────┘
    ↓
    ↓ Step 3: Invoke plan-generation-mentor
    ↓         with codebase context
    ↓
┌─────────────────────────────────────────────┐
│ plan-generation-mentor                      │
│ • Reads relevant files markdown             │
│ • Creates context-aware plan                │
│ • References actual files                   │
│ • Identifies integration points             │
│ • Output: plans/[date]-[feature]-plan.md    │
└─────────────────────────────────────────────┘
    ↓
    ↓ Step 4: Present results
    ↓
┌─────────────────────────────────────────────┐
│ User receives:                              │
│ • Path to codebase analysis                 │
│ • Path to generated plan                    │
│ • Summary of what was created               │
│ • Next steps to begin implementation        │
└─────────────────────────────────────────────┘
```

---

## Usage

### Quick Start

```bash
/create-project-plan autonomous navigation system
```

That's it! The system handles the rest.

### What Happens

1. **Codebase Search** (1-2 minutes)
   - Searches for navigation-related files
   - Finds robot control, sensors, config files
   - Analyzes structure and relationships
   - Documents in `project-context/relevant-files-[timestamp].md`

2. **Plan Generation** (2-3 minutes)
   - Reads the codebase analysis
   - Creates educational implementation plan
   - References specific files to modify
   - Identifies integration points
   - Saves to `plans/[date]-navigation-learning-plan.md`

3. **Results Presented**
   - Shows what was generated
   - Provides next steps
   - Ready to start with `/continue-plan`

### Example Results

#### Codebase Analysis File
```markdown
# Project Context: Autonomous Navigation System

**Files Found**: 15

## Core Implementation Files

### 1. `src/robot_control.py`
- **Purpose**: Main robot movement control
- **Relevance**: Navigation will send commands here
- **Integration Point**: Line 145 - command handler
- **Key Components**:
  - `RobotController` class
  - `move_forward()`, `turn()` methods

### 2. `config/robot_params.yaml`
- **Purpose**: Robot configuration parameters
- **Relevance**: Navigation parameters go here
- **Modification Needed**: Add navigation section
...
```

#### Generated Plan
```markdown
# Autonomous Navigation - Learning Implementation Plan

## Phase 1: Understanding Existing Codebase

### Task 1.1: Review Current Control System
**Files to Read**:
- `src/robot_control.py:45-200` - Understand movement control
- `config/robot_params.yaml` - See parameter structure

**Understanding Questions**:
- How does robot_control.py handle movement commands?
- What coordinate frame is used?
- Where should navigation integrate?

**Integration Points Identified**:
- Modify: `src/robot_control.py:145` - Add navigation handler
- Extend: `config/robot_params.yaml` - Add nav parameters
- Create: `src/navigation_planner.py` - New module
...
```

### Advanced Usage

#### Direct Agent Invocation
You can invoke agents individually for testing:

```bash
# Test file search only
Task: file-search-agent
Prompt: "Search for navigation-related files"

# Test plan generation with existing analysis
Task: plan-generation-mentor
Prompt: "Create plan for navigation using project-context/relevant-files-2025-10-07.md"
```

---

## Features

### 🎯 Context-Aware Planning

**Before (Generic Planning)**:
> "Create a navigation module with path planning"

**After (Context-Aware)**:
> "Create `src/navigation_planner.py` following the pattern in `src/robot_control.py`.
> Integrate at `robot_control.py:145` where commands are handled.
> Add parameters to `config/robot_params.yaml` under a new `navigation:` section.
> Launch via `launch/robot_bringup.launch.py` similar to sensor nodes at line 67."

### 🔍 Comprehensive Codebase Analysis

Finds:
- ✅ Core implementation files
- ✅ Configuration files
- ✅ Launch files
- ✅ Test files
- ✅ Related utilities
- ✅ Documentation
- ✅ Dependencies

Analyzes:
- ✅ File purposes
- ✅ Key components (classes, functions)
- ✅ Relationships between files
- ✅ Integration points
- ✅ Existing patterns to follow

### 📋 Educational Planning

Plans include:
- ✅ Research tasks to understand existing code
- ✅ Design decisions with guidance
- ✅ Progressive implementation phases
- ✅ Learning checkpoints
- ✅ Specialist support mapping
- ✅ Specific file references

### 🔄 Sequential Execution

Agents run in order:
- ✅ File search completes before planning
- ✅ Results verified at each step
- ✅ Context passed between agents
- ✅ Errors handled gracefully
- ✅ User kept informed of progress

---

## File Structure

```
claude_code/
├── agents/
│   ├── project-plan-orchestrator.md    ← Orchestrator (NEW)
│   ├── file-search-agent.md            ← File searcher (NEW)
│   ├── plan-generation-mentor.md       ← Planner (ENHANCED)
│   └── [other agents...]
├── commands/
│   ├── create-project-plan.md          ← Easy invocation (NEW)
│   └── [other commands...]
├── project-context/                     ← Analysis storage (NEW)
│   ├── README.md
│   └── relevant-files-[timestamp].md
└── plans/                              ← Generated plans
    └── [date]-[feature]-learning-plan.md
```

---

## Integration with Existing System

### Works With

**learning-coordinator**:
- Can invoke orchestrator for complex features
- Uses generated plans with `/continue-plan`
- Coordinates specialists during implementation

**plan-generation-mentor**:
- Enhanced to use codebase context
- Maintains educational focus
- Now references actual files

**Other Agents**:
- All teaching agents can reference the plans
- Plans map which specialists help in each phase
- Seamless integration with existing workflow

### Commands

**New**:
- `/create-project-plan [feature]` - Full workflow

**Existing** (still work):
- `/create-plan [feature]` - Standard planning
- `/continue-plan` - Begin implementation
- `/update-plan` - Track progress
- All other commands unchanged

---

## Benefits

### For Complex Projects

✅ **Understands Context**: Knows what code already exists
✅ **Specific Guidance**: References actual files and line numbers
✅ **Integration Ready**: Identifies exact connection points
✅ **Pattern Aware**: Follows existing code style and structure
✅ **Comprehensive**: Finds all related files, not just obvious ones

### For Learning

✅ **Educational**: Plans focus on understanding, not just implementation
✅ **Progressive**: Builds knowledge in phases
✅ **Guided**: Provides questions and research tasks
✅ **Supported**: Maps specialists to help in each phase
✅ **Checkpoint**: Verifies learning before advancing

### For Collaboration

✅ **Documented**: All analysis saved for reference
✅ **Reproducible**: Can regenerate plans as code evolves
✅ **Shareable**: Analysis files show project structure to others
✅ **Maintainable**: Plans evolve with codebase

---

## Use Cases

### 1. Adding Major Feature
```bash
/create-project-plan autonomous navigation with SLAM
```
**Result**: Plan that integrates with existing robot control, sensors, and ROS2 setup

### 2. Refactoring System
```bash
/create-project-plan refactor control system to use strategy pattern
```
**Result**: Plan showing which files to modify and how to restructure

### 3. New API Layer
```bash
/create-project-plan REST API for robot control
```
**Result**: Plan showing how to wrap existing control interfaces

### 4. Hardware Integration
```bash
/create-project-plan integrate LIDAR sensor
```
**Result**: Plan referencing existing sensor setup and launch files

---

## Configuration

### Agent Tools

**project-plan-orchestrator**:
- Read, Write, Task (for invoking agents)

**file-search-agent**:
- Read, Write, Glob, Grep (for searching)

**plan-generation-mentor**:
- Read, Write (for reading context and creating plans)

### Activation

**project-plan-orchestrator**: `proactive`
- Main assistant can invoke automatically

**file-search-agent**: `manual`
- Only invoked by orchestrator

**plan-generation-mentor**: (existing)
- Can be invoked directly or by orchestrator

---

## Troubleshooting

### No Files Found

**Cause**: Feature is entirely new, no existing code

**Result**: Plan proceeds without context, provides general structure

**Action**: Normal - plan will guide creating from scratch

### Search Takes Long

**Cause**: Large codebase with many files

**Result**: May take 2-3 minutes

**Action**: Normal - comprehensive analysis takes time

### Plan Doesn't Reference Files

**Cause**: Orchestrator may not have passed context correctly

**Action**: Check `project-context/` for analysis file, can invoke plan-generation-mentor manually with that file

### Orchestration Fails

**Cause**: Agent error or invalid prompt

**Action**: Try simpler description, or use `/create-plan` for standard planning

---

## Best Practices

### Writing Good Prompts

**Good** ✅:
```bash
/create-project-plan autonomous navigation system
/create-project-plan computer vision object detection
/create-project-plan web API for remote control
```

**Too Vague** ❌:
```bash
/create-project-plan help me
/create-project-plan coding
```

**Too Specific** ⚠️:
```bash
/create-project-plan modify line 145 in robot_control.py
# (Just do this directly, don't need full planning)
```

### When to Use

**Use this system for**:
- ✅ Major new features (multi-file, complex)
- ✅ Integration with existing code
- ✅ Refactoring projects
- ✅ Learning implementations (multi-week)

**Don't use for**:
- ❌ Quick bug fixes
- ❌ Single file modifications
- ❌ Learning concepts (use `/ask-specialist`)
- ❌ Debugging (use debugging-detective)

### Maintaining Plans

**Keep Analysis Files**:
- Valuable documentation of codebase structure
- Shows what existed when plan was made
- Can reference later for similar projects

**Update Plans**:
- Use `/update-plan` as you progress
- Add learning journal entries
- Mark phases complete

**Regenerate When Needed**:
- If codebase changes significantly
- If plan scope expands
- If starting related feature

---

## Future Enhancements

Potential improvements:
- Parallel file search for speed
- Incremental analysis (cached results)
- Visualization of file relationships
- Integration with git history
- Automatic plan updates on code changes
- Multi-language support (currently Python/ROS2 focused)

---

## Summary

The Context-Aware Project Planning System transforms generic planning into **intelligent, codebase-aware guidance** by:

1. **🔍 Understanding** what code exists
2. **🎯 Planning** with full context
3. **📋 Generating** educational implementation guides
4. **🔄 Orchestrating** the workflow seamlessly

**Result**: Plans that work with your actual codebase, not against it!

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/create-project-plan [feature]` | Create context-aware plan |
| `/continue-plan` | Start implementing the plan |
| `/update-plan` | Track progress and reflect |

| File Location | Contents |
|--------------|----------|
| `project-context/relevant-files-*.md` | Codebase analysis |
| `plans/*-learning-plan.md` | Generated plans |

| Agent | Role |
|-------|------|
| project-plan-orchestrator | Coordinates workflow |
| file-search-agent | Finds and analyzes files |
| plan-generation-mentor | Creates context-aware plans |

---

**Ready to create intelligent plans? Try:**
```bash
/create-project-plan [your feature description]
```

Happy planning! 🚀
