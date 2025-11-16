# Agent Skill Usage Examples

**Purpose**: Practical examples showing how agents use Phase 1 skills (learning-plan-manager and code-analysis) to enhance their capabilities.

**Created**: 2025-10-19
**Version**: 1.0

---

## Table of Contents

1. [Overview](#overview)
2. [Skill Invocation Basics](#skill-invocation-basics)
3. [learning-plan-manager Examples](#learning-plan-manager-examples)
4. [code-analysis Examples](#code-analysis-examples)
5. [Combined Skill Workflows](#combined-skill-workflows)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

---

## Overview

### What Are Skills?

Skills are capability extensions that agents can invoke within their workflow using the `Skill` tool. Unlike agents (which spawn separate AI instances), skills run as Python code and return structured data.

### Phase 1 Skills

#### learning-plan-manager
- **Purpose**: Structured operations on learning plan markdown files
- **Used by**: learning-coordinator, plan-generation-mentor
- **Returns**: JSON with plan data, progress stats, task information
- **Key operations**: Load plans, track progress, update tasks, generate reports

#### code-analysis
- **Purpose**: Deep Python static code analysis with AST parsing
- **Used by**: file-search-agent, plan-generation-mentor, code-architecture-mentor
- **Returns**: JSON with code structure, patterns, complexity, integration points
- **Key operations**: Analyze files/codebases, detect patterns, suggest integration points

---

## Skill Invocation Basics

### How Agents Invoke Skills

Agents use the `Skill` tool with a natural language query:

```markdown
Skill(skill-name) with query:
"Natural language description of what you want the skill to do"
```

### Example Invocations

```markdown
# Learning plan manager
Skill(learning-plan-manager) with query:
"Find the latest learning plan and get current phase"

# Code analysis
Skill(code-analysis) with query:
"Analyze src/ directory and identify integration points for navigation feature"
```

### What Skills Return

Skills return **structured JSON** that agents can parse and interpret. The JSON format varies by skill but is always well-documented in the skill's documentation.

---

## learning-plan-manager Examples

### Example 1: Learning Coordinator Loading Plan

**Scenario**: Student runs `/continue-plan` and learning-coordinator needs to load their progress.

**Agent**: learning-coordinator

**Invocation**:
```markdown
Skill(learning-plan-manager) with query:
"Find the latest learning plan in plans/ directory and return current status"
```

**Skill Returns**:
```json
{
  "plan_found": true,
  "file_path": "plans/2025-10-15-navigation-system-learning-plan.md",
  "metadata": {
    "title": "Navigation System - Learning Implementation Plan",
    "created": "2025-10-15",
    "estimated_time": "3 weeks",
    "complexity": "Intermediate"
  },
  "current_phase": {
    "number": 2,
    "title": "Basic Implementation",
    "learning_goals": [
      "Implement core functionality",
      "Practice algorithm implementation",
      "Experience iterative development"
    ],
    "started_at": "2025-10-17",
    "completed_at": null
  },
  "next_task": {
    "id": "task-2-2",
    "phase_number": 2,
    "title": "Test basic navigation",
    "status": "NOT_STARTED",
    "description": "Verify basic functionality works..."
  },
  "progress": {
    "overall_percentage": 35.5,
    "phases": {"completed": 1, "in_progress": 1, "total": 4},
    "tasks": {"completed": 8, "in_progress": 1, "total": 22},
    "checkpoints": {"passed": 2, "total": 4}
  }
}
```

**How Agent Uses This**:
```markdown
# Agent processes the JSON and responds to student:

👋 Welcome Back to Your Learning Journey!

### Where We Left Off
You're currently in Phase 2 (Basic Implementation) of the Navigation System project.
You've completed 35.5% of the plan with 8 out of 22 tasks done!

### Current Phase: Basic Implementation
**Learning goals**:
- Implement core functionality
- Practice algorithm implementation
- Experience iterative development

### Next Task: Test basic navigation
Before we proceed, let's verify your basic functionality works.

Are you ready to continue with this task, or would you like to review Phase 1 concepts first?
```

---

### Example 2: Updating Task Status

**Scenario**: Student completes a task, coordinator updates the plan.

**Agent**: learning-coordinator

**Invocation**:
```markdown
Skill(learning-plan-manager) with query:
"Update task-2-2 status to COMPLETED in the latest plan and add note:
'Basic navigation tested with simple obstacle course. Path finding works correctly.'"
```

**Skill Returns**:
```json
{
  "success": true,
  "updated_task": {
    "id": "task-2-2",
    "title": "Test basic navigation",
    "status": "COMPLETED",
    "notes": "Basic navigation tested with simple obstacle course. Path finding works correctly.",
    "completed_at": "2025-10-19"
  },
  "new_progress": {
    "overall_percentage": 40.2,
    "tasks": {"completed": 9, "in_progress": 0, "total": 22}
  }
}
```

**How Agent Uses This**:
```markdown
✅ Great work! I've marked "Test basic navigation" as complete.

Your progress is now 40.2% (9/22 tasks completed).

The next task is "task-2-3: Refine based on testing results".
Ready to move forward?
```

---

### Example 3: Generating Progress Report

**Scenario**: Student asks "How am I doing?" or end of session summary.

**Agent**: learning-coordinator

**Invocation**:
```markdown
Skill(learning-plan-manager) with query:
"Generate a comprehensive progress report for the latest learning plan"
```

**Skill Returns**:
```json
{
  "report_generated": true,
  "summary": {
    "plan_title": "Navigation System - Learning Implementation Plan",
    "overall_progress": 40.2,
    "time_elapsed": "4 days",
    "estimated_remaining": "17 days"
  },
  "phase_breakdown": [
    {
      "phase": 1,
      "title": "Understanding & Research",
      "status": "COMPLETED",
      "completion_date": "2025-10-17",
      "tasks_completed": 5,
      "checkpoint_passed": true
    },
    {
      "phase": 2,
      "title": "Basic Implementation",
      "status": "IN_PROGRESS",
      "tasks_completed": 4,
      "tasks_remaining": 3,
      "checkpoint_passed": false
    }
  ],
  "recent_accomplishments": [
    "Completed Phase 1 checkpoint - demonstrated understanding of path planning algorithms",
    "Implemented basic A* algorithm",
    "Successfully tested navigation with simple obstacles"
  ],
  "next_milestones": [
    "Complete Phase 2 tasks (3 remaining)",
    "Pass Phase 2 checkpoint",
    "Begin Phase 3: Enhancement & Quality"
  ]
}
```

**How Agent Uses This**:
```markdown
## 📊 Your Learning Progress Report

### Overall Progress: 40.2%
You've been working on this for 4 days with an estimated 17 days remaining.

### Phase Breakdown
✅ **Phase 1: Understanding & Research** - COMPLETED (Oct 17)
   - All 5 tasks done
   - Checkpoint passed ✓

🔄 **Phase 2: Basic Implementation** - IN PROGRESS
   - 4 of 7 tasks completed
   - Checkpoint not yet attempted

### Recent Accomplishments
- ✅ Completed Phase 1 checkpoint - demonstrated understanding of path planning algorithms
- ✅ Implemented basic A* algorithm
- ✅ Successfully tested navigation with simple obstacles

### Next Milestones
- Complete 3 remaining Phase 2 tasks
- Pass Phase 2 checkpoint
- Begin Phase 3: Enhancement & Quality

Great progress! You're ahead of schedule. 🚀
```

---

### Example 4: Searching for Specific Tasks

**Scenario**: Student says "I want to work on testing" - find all testing-related tasks.

**Agent**: learning-coordinator

**Invocation**:
```markdown
Skill(learning-plan-manager) with query:
"Search for all tasks related to 'testing' or 'test' in the latest plan"
```

**Skill Returns**:
```json
{
  "tasks_found": 4,
  "tasks": [
    {
      "id": "task-2-2",
      "phase": 2,
      "title": "Test basic navigation",
      "status": "COMPLETED",
      "description": "Verify basic functionality with simple test cases..."
    },
    {
      "id": "task-3-4",
      "phase": 3,
      "title": "Write unit tests for path planner",
      "status": "NOT_STARTED",
      "description": "Create comprehensive test suite..."
    },
    {
      "id": "task-3-5",
      "phase": 3,
      "title": "Test edge cases and failure modes",
      "status": "NOT_STARTED",
      "description": "Test with challenging scenarios..."
    },
    {
      "id": "task-4-2",
      "phase": 4,
      "title": "Run integration tests",
      "status": "NOT_STARTED",
      "description": "Test full system integration..."
    }
  ]
}
```

**How Agent Uses This**:
```markdown
I found 4 testing-related tasks in your plan:

✅ **Phase 2** - Test basic navigation (COMPLETED)

⏳ **Phase 3** - Testing tasks you'll work on soon:
   - Write unit tests for path planner
   - Test edge cases and failure modes

⏳ **Phase 4** - Future testing:
   - Run integration tests

Since you've completed basic testing in Phase 2, let's focus on finishing
the remaining Phase 2 tasks first. Then we can dive deeper into comprehensive
testing in Phase 3.

Would you like to continue with the current Phase 2 tasks, or do you have
specific testing questions?
```

---

## code-analysis Examples

### Example 5: File Search Agent Gathering Context

**Scenario**: User asks to plan a new "export to CSV" feature. File-search-agent gathers context first.

**Agent**: file-search-agent

**Invocation**:
```markdown
Skill(code-analysis) with query:
"Analyze src/ directory and find all components related to data export,
file handling, and client management to understand where CSV export should integrate"
```

**Skill Returns**:
```json
{
  "analysis_complete": true,
  "total_files": 15,
  "total_lines": 3420,
  "files": [
    {
      "file_path": "src/client.py",
      "total_lines": 345,
      "classes": [
        {
          "name": "Client",
          "line_start": 45,
          "line_end": 230,
          "methods": ["export_data", "save_to_file", "load_from_file"],
          "complexity": {"cyclomatic_complexity": 8}
        }
      ],
      "functions": [
        {
          "name": "export_data",
          "line_start": 156,
          "line_end": 189,
          "complexity": {"cyclomatic_complexity": 6}
        }
      ]
    },
    {
      "file_path": "src/exporters/base.py",
      "total_lines": 156,
      "classes": [
        {
          "name": "DataExporter",
          "line_start": 12,
          "line_end": 85,
          "is_abstract": true,
          "complexity": {"cyclomatic_complexity": 3}
        }
      ]
    }
  ],
  "patterns_found": {
    "Factory": ["src/exporters/base.py"],
    "Strategy": ["src/formatters/json_formatter.py"]
  },
  "integration_points": [
    {
      "name": "export_data",
      "file_path": "src/client.py",
      "line_number": 156,
      "entity_type": "function",
      "reason": "Existing export function that handles multiple formats. Extend for CSV support."
    },
    {
      "name": "DataExporter",
      "file_path": "src/exporters/base.py",
      "line_number": 12,
      "entity_type": "class",
      "reason": "Abstract base class for exporters. Create CSVExporter subclass following Factory pattern."
    },
    {
      "name": "register_exporter",
      "file_path": "src/exporters/base.py",
      "line_number": 94,
      "entity_type": "function",
      "reason": "Factory registration point. Register CSV exporter here."
    }
  ],
  "dependency_graph": {
    "nodes": ["src/client.py", "src/exporters/base.py", "src/formatters/json_formatter.py"],
    "edges": [
      {"from": "src/client.py", "to": "src/exporters/base.py", "import": "DataExporter"},
      {"from": "src/exporters/json_exporter.py", "to": "src/exporters/base.py", "import": "DataExporter"},
      {"from": "src/exporters/json_exporter.py", "to": "src/formatters/json_formatter.py", "import": "JSONFormatter"}
    ]
  }
}
```

**How Agent Uses This**:
```markdown
# Agent creates project-context markdown file

# Project Context: CSV Export Feature

**Generated**: 2025-10-19
**Search Query**: "Add CSV export functionality"
**Files Found**: 15
**Analysis Method**: code-analysis skill + Glob/Grep

---

## 📊 Executive Summary

### Code Intelligence (from code-analysis skill)
- **Design Patterns Found**: Factory, Strategy
- **Average Complexity**: Low-Medium (3-8)
- **Integration Points**: 3 locations identified for CSV export
- **Code Quality**: Clean - no circular dependencies detected
- **Dependency Health**: No circular dependencies

---

## 🗂️ Core Implementation Files

### 1. `src/client.py` (345 lines)
- **Purpose**: Main client interface for data operations
- **Key Components**:
  - `Client` class (Lines 45-230, Complexity: 8)
  - `export_data()` function (Lines 156-189, Complexity: 6)
- **Design Pattern**: N/A (client code)
- **Integration Points**:
  - `export_data()` at line 156: Add CSV format option here
  - Currently handles JSON and XML formats
  - Complexity is moderate (6) - be careful when extending

### 2. `src/exporters/base.py` (156 lines)
- **Purpose**: Abstract base class for all exporters
- **Key Components**:
  - `DataExporter` class (Lines 12-85, Complexity: 3)
  - `register_exporter()` function (Line 94)
- **Design Pattern**: Factory (detected by code-analysis)
- **Integration Points**:
  - Create `CSVExporter` subclass extending `DataExporter`
  - Register CSV exporter at line 94 using `register_exporter()`
  - Low complexity (3) - good starting point for learning

### 3. `src/formatters/json_formatter.py` (124 lines)
- **Purpose**: JSON formatting strategy
- **Design Pattern**: Strategy (detected by code-analysis)
- **Relevance**: Template for creating `csv_formatter.py`
- **Note**: Follow same interface for consistency

---

## 🔗 File Relationships

### Dependency Map (from code-analysis)
```
src/client.py (Complexity: 8)
  └─ imports: DataExporter from src/exporters/base.py

src/exporters/json_exporter.py (Complexity: 4)
  ├─ imports: DataExporter from src/exporters/base.py
  └─ imports: JSONFormatter from src/formatters/json_formatter.py
```

### Integration Points
1. **Extension Point**: `src/client.py:156` - `export_data()` function
   - Reason: Main export entry point, add CSV option here
   - Complexity: Medium (6) - requires careful modification

2. **Base Class**: `src/exporters/base.py:12` - `DataExporter` class
   - Reason: Factory pattern base, create CSVExporter subclass
   - Complexity: Low (3) - easy to extend

3. **Registration**: `src/exporters/base.py:94` - `register_exporter()` function
   - Reason: Factory registration point
   - Complexity: Low - straightforward addition

---

## 💡 Planning Recommendations

### Files to Modify
1. **`src/client.py:156`** (Complexity: 6, Function)
   - Why: Add CSV option to export_data() function
   - What: Add "csv" case to format selection logic
   - Integration point: Line 156 in export_data()
   - Caution: Keep complexity low - function already at 6

2. **`src/exporters/base.py:94`** (Complexity: 3)
   - Why: Register CSV exporter in factory
   - What: Call register_exporter("csv", CSVExporter)

### New Files to Create
1. **`src/formatters/csv_formatter.py`**
   - Purpose: CSV formatting logic
   - Why here: Matches existing formatter structure
   - Pattern to use: Strategy (matches json_formatter.py)
   - Should integrate with: CSVExporter class

2. **`src/exporters/csv_exporter.py`**
   - Purpose: CSV exporter implementation
   - Pattern to use: Factory (extend DataExporter)
   - Should integrate with: csv_formatter.py

### Existing Patterns to Follow
- **Design Patterns**: Factory pattern detected in base.py
  - Your CSVExporter should extend DataExporter
  - Register with factory using register_exporter()
- **Code Structure**: Average complexity is 3-6, keep CSV exporter similar
- **Testing approach**: Check existing test files for patterns

---

## 🎯 Next Steps for Planning Agent

The planning agent should:
1. Review `src/exporters/base.py:12-85` to understand Factory pattern
2. Study `src/formatters/json_formatter.py` as template for CSV formatter
3. Follow Factory pattern for consistency
4. Target complexity < 5 for CSV components
5. Plan integration at line 156 in client.py

**Priority Order** (based on code-analysis):
1. `src/exporters/base.py` - Low complexity, good starting point
2. `src/formatters/json_formatter.py` - Template to follow
3. `src/client.py:156` - Integration point (moderate complexity)
```

---

### Example 6: Plan Generation with Code Analysis

**Scenario**: plan-generation-mentor creates context-aware learning plan.

**Agent**: plan-generation-mentor

**Invocation**:
```markdown
Skill(code-analysis) with query:
"Analyze src/ and identify existing pattern for adding new agent types,
to help plan implementation of custom learning agent"
```

**Skill Returns**:
```json
{
  "analysis_complete": true,
  "integration_points": [
    {
      "name": "AgentRegistry",
      "file_path": "src/agents/registry.py",
      "line_number": 23,
      "entity_type": "class",
      "reason": "Singleton registry for agents. New agents register here."
    },
    {
      "name": "BaseAgent",
      "file_path": "src/agents/base.py",
      "line_number": 15,
      "entity_type": "class",
      "reason": "Abstract base class all agents extend. Implements common functionality."
    },
    {
      "name": "register_agent",
      "file_path": "src/agents/registry.py",
      "line_number": 67,
      "entity_type": "method",
      "reason": "Registration method for new agents."
    }
  ],
  "patterns_found": {
    "Singleton": ["src/agents/registry.py"],
    "Factory": ["src/agents/factory.py"]
  },
  "files": [
    {
      "file_path": "src/agents/base.py",
      "complexity": {"average_complexity": 4},
      "classes": [{
        "name": "BaseAgent",
        "is_abstract": true,
        "methods": ["process", "validate", "execute"]
      }]
    }
  ]
}
```

**How Agent Uses This** (in generated learning plan):
```markdown
## Phase 1: Understanding Agent Architecture

### Task 1.1: Study Existing Agent Pattern
**Learning Activity**: Analyze the agent system architecture

**Files to Read**:
1. `src/agents/base.py:15-120` - BaseAgent abstract class
   - **Complexity**: Low (4) - Good starting point
   - **Pattern**: This is your template!
   - **Questions**: What methods must you implement? What's provided?

2. `src/agents/registry.py:23-90` - AgentRegistry singleton
   - **Pattern**: Singleton pattern (maintains single registry instance)
   - **Questions**: How do agents register? When does registration happen?

**Understanding Goals**:
- Why use Singleton for registry?
- What's the Factory pattern role?
- How do agents integrate with the system?

**Specialist Support**: code-architecture-mentor can explain Singleton pattern

### Task 1.2: Design Your Learning Agent
**Design Decision**: How will your agent extend BaseAgent?

**Context from Code Analysis**:
- **Must extend**: `BaseAgent` at src/agents/base.py:15
- **Must implement**: process(), validate(), execute() methods
- **Must register**: Using register_agent() at src/agents/registry.py:67
- **Complexity target**: Keep it ~4 like other agents

**Design Questions**:
- What makes a "learning agent" unique?
- What additional methods might you need?
- How will it interact with other agents?

**Checkpoint**: Have design that follows existing pattern?
```

---

### Example 7: Architecture Understanding

**Scenario**: code-architecture-mentor helping student understand system design.

**Agent**: code-architecture-mentor

**Invocation**:
```markdown
Skill(code-analysis) with query:
"Analyze src/ to provide architectural overview showing design patterns,
complexity distribution, and how components interact"
```

**Skill Returns**:
```json
{
  "analysis_complete": true,
  "total_files": 42,
  "patterns_found": {
    "Singleton": ["src/agents/registry.py", "src/config/settings.py"],
    "Factory": ["src/agents/factory.py", "src/exporters/base.py"],
    "Strategy": ["src/formatters/json_formatter.py", "src/formatters/xml_formatter.py"],
    "Observer": ["src/events/publisher.py"]
  },
  "complexity_distribution": {
    "simple": 28,      // complexity < 5
    "moderate": 10,    // complexity 5-10
    "complex": 4       // complexity > 10
  },
  "entry_points": [
    "src/main.py:main",
    "src/api/server.py:start_server",
    "src/cli/app.py:run_cli"
  ],
  "dependency_graph": {
    "circular_dependencies": [],
    "most_depended_on": [
      "src/agents/base.py",
      "src/config/settings.py",
      "src/utils/logging.py"
    ]
  }
}
```

**How Agent Uses This** (teaching response):
```markdown
Let me help you understand the architecture of this codebase!

## 🏗️ Architectural Overview

### Design Patterns in Use

The codebase uses 4 main design patterns:

1. **Singleton Pattern** (2 instances)
   - `src/agents/registry.py` - Ensures single agent registry
   - `src/config/settings.py` - Global configuration
   - **Why**: These should only exist once in the application

2. **Factory Pattern** (2 instances)
   - `src/agents/factory.py` - Creates agents dynamically
   - `src/exporters/base.py` - Creates exporters by type
   - **Why**: Decouples creation from usage, easy to extend

3. **Strategy Pattern** (2 instances)
   - `src/formatters/json_formatter.py` - JSON formatting strategy
   - `src/formatters/xml_formatter.py` - XML formatting strategy
   - **Why**: Interchangeable algorithms, easy to add new formats

4. **Observer Pattern** (1 instance)
   - `src/events/publisher.py` - Event notification system
   - **Why**: Loose coupling between components

### Complexity Analysis

The codebase is generally well-structured:
- 📗 **28 simple files** (complexity < 5) - Easy to modify
- 📙 **10 moderate files** (complexity 5-10) - Requires care
- 📕 **4 complex files** (complexity > 10) - Needs attention

**Recommendation**: When adding new features, target complexity < 5
to match the majority of the codebase.

### System Entry Points

The application has 3 main entry points:
1. `src/main.py:main()` - Main application entry
2. `src/api/server.py:start_server()` - API server mode
3. `src/cli/app.py:run_cli()` - Command-line interface

### Dependency Health

✅ **Good news**: No circular dependencies detected!

**Core dependencies** (most files depend on these):
- `src/agents/base.py` - Agent base class (foundation)
- `src/config/settings.py` - Configuration (used everywhere)
- `src/utils/logging.py` - Logging utilities (cross-cutting)

### Architectural Recommendations

When adding new features:
1. **Follow existing patterns** - Use Factory for new object types
2. **Keep complexity low** - Match the existing average (~5)
3. **Avoid circular deps** - Keep the clean dependency graph
4. **Extend base classes** - Don't reinvent what exists

Do you have questions about any of these patterns?
```

---

## Combined Skill Workflows

### Example 8: Complete Feature Planning Workflow

**Scenario**: User says "Help me plan adding navigation to my robot".

**Workflow**: Orchestrator coordinates file-search and plan-generation.

#### Step 1: File Search Agent Gathers Context

```markdown
Skill(code-analysis) with query:
"Analyze robot codebase in src/ and identify existing components related to
movement, control, sensors that would interact with navigation system"
```

Returns: Comprehensive codebase analysis with integration points.

#### Step 2: File Search Agent Creates Context Markdown

Generates `project-context/relevant-files-2025-10-19-14-30.md` with:
- All relevant files
- Integration points
- Existing patterns
- Complexity metrics

#### Step 3: Plan Generation Mentor Reads Context

```markdown
Read: project-context/relevant-files-2025-10-19-14-30.md
```

#### Step 4: Plan Generation Creates Context-Aware Plan

Uses the context to create learning plan with:
- Specific files to study
- Actual integration points with line numbers
- Patterns to follow from existing code
- Complexity targets based on codebase

#### Step 5: Learning Coordinator Executes Plan

```markdown
Skill(learning-plan-manager) with query:
"Load plan from plans/2025-10-19-navigation-system-learning-plan.md"
```

Tracks progress as student works through phases.

**Result**: Student gets context-aware, structured learning journey with:
- ✅ Relevant codebase files identified
- ✅ Integration points specified
- ✅ Patterns to follow documented
- ✅ Progress tracked automatically
- ✅ Teaching specialists coordinated

---

## Error Handling

### Handling Skill Errors

Skills may return errors. Agents should handle gracefully:

```markdown
Skill(code-analysis) with query:
"Analyze non-existent-directory/"
```

**Possible Error Response**:
```json
{
  "error": true,
  "error_type": "DirectoryNotFound",
  "message": "Directory 'non-existent-directory/' does not exist",
  "suggestion": "Check the directory path and try again"
}
```

**Agent Response**:
```markdown
I tried to analyze the directory but couldn't find it.

Could you verify the directory path? Here are the common source directories
I can see:
- src/
- lib/
- modules/

Which directory would you like me to analyze?
```

### No Data Found

```markdown
Skill(learning-plan-manager) with query:
"Find latest learning plan"
```

**Response when no plans exist**:
```json
{
  "plan_found": false,
  "plans_directory": "plans/",
  "message": "No learning plans found in plans/ directory"
}
```

**Agent Response**:
```markdown
I don't see any existing learning plans. Would you like me to create a new one?

What feature or topic would you like to learn about?
```

---

## Best Practices

### 1. Use Skills Appropriately

✅ **DO**: Use skills for data gathering and analysis
```markdown
Skill(code-analysis) with query: "Analyze src/ for patterns"
# Agent interprets results and teaches
```

❌ **DON'T**: Expect skills to teach or make decisions
```markdown
# Skills don't teach - agents do!
```

### 2. Parse and Interpret Results

✅ **DO**: Extract relevant information and present it educationally
```markdown
# Agent extracts from skill JSON:
"I found a Factory pattern at line 23. Let's discuss why this pattern
is useful and how you might extend it..."
```

❌ **DON'T**: Dump raw JSON to students
```markdown
# Don't show students raw skill output
```

### 3. Handle Missing Data

✅ **DO**: Provide alternatives when skills can't help
```markdown
"The code-analysis skill works best with Python code. Since this is C++,
let's use traditional codebase exploration techniques instead..."
```

### 4. Combine Skills When Appropriate

✅ **DO**: Use both skills for comprehensive workflows
```markdown
# 1. Use code-analysis to understand codebase
# 2. Create context-aware learning plan
# 3. Use learning-plan-manager to track progress
```

### 5. Maintain Teaching Philosophy

✅ **DO**: Use skill data to guide, not solve
```markdown
"The analysis shows a Factory pattern at line 45.
Before we look at it, what do you know about the Factory pattern?
Let's explore how it's used here and why..."
```

❌ **DON'T**: Use skills to provide complete solutions
```markdown
# Don't use skill output to solve problems for students
```

---

## Summary

### Key Takeaways

1. **Skills provide data, agents provide teaching**
   - Skills return structured JSON
   - Agents interpret and present educationally

2. **learning-plan-manager automates plan operations**
   - No more manual markdown parsing
   - Structured progress tracking
   - Automatic calculations

3. **code-analysis provides deep intelligence**
   - AST-based code understanding
   - Pattern detection
   - Integration point identification
   - Complexity analysis

4. **Combined workflows are powerful**
   - file-search-agent uses code-analysis
   - plan-generation-mentor uses both
   - learning-coordinator uses learning-plan-manager

5. **Teaching philosophy preserved**
   - Skills enhance capabilities
   - Agents still guide, don't solve
   - Students still learn through discovery

---

## Next Steps

### For Agent Developers

1. Review your agent's purpose
2. Identify where skills can enhance capabilities
3. Add skill invocations to agent prompts
4. Test workflows end-to-end
5. Document skill usage in agent files

### For Skill Developers

1. Ensure JSON output is well-documented
2. Provide clear error messages
3. Include usage examples in skill.md
4. Test with real agent workflows
5. Consider edge cases and errors

---

**Document End**
