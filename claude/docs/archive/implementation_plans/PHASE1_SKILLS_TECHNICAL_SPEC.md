# Phase 1 Skills - Technical Specification

**Document Version**: 1.0
**Created**: 2025-10-19
**Skills Covered**: learning-plan-manager, code-analysis

---

## Table of Contents

1. [Overview](#overview)
2. [Skill 1: learning-plan-manager](#skill-1-learning-plan-manager)
3. [Skill 2: code-analysis](#skill-2-code-analysis)
4. [Integration Architecture](#integration-architecture)
5. [Implementation Roadmap](#implementation-roadmap)
6. [Testing Strategy](#testing-strategy)

---

## Overview

### Purpose

Phase 1 skills provide foundational capabilities that:
- **Eliminate manual markdown parsing** in agents
- **Enable structured data operations** on learning plans
- **Provide deep code intelligence** beyond basic Grep/Glob
- **Transform context-aware planning** with real architectural insights

### Design Principles

1. **Teaching-First**: Skills provide data/capabilities, agents interpret and teach
2. **Structured Output**: All skills return well-defined data structures
3. **Agent-Friendly**: APIs designed for agent consumption
4. **Composable**: Skills work independently and together
5. **Stateless**: Each skill invocation is independent (state managed externally)

### Technology Stack

```python
# Core
- Python 3.11+
- Pydantic for data validation
- asyncio for async operations

# Parsing
- tree-sitter (multi-language AST parsing)
- ast (Python built-in for Python analysis)
- markdown (CommonMark for learning plans)

# Analysis
- networkx (dependency graphs)
- pygments (syntax highlighting/tokenization)
- radon (code metrics)

# Utilities
- pathlib (path handling)
- typing (type hints)
- dataclasses (lightweight models)
```

---

## Skill 1: learning-plan-manager

### 1.1 Purpose & Scope

**What it does:**
- Parse learning plan markdown files into structured data
- Provide CRUD operations on plan sections
- Track completion state and progress
- Generate exports (JSON, HTML, PDF)
- Validate plan format and structure

**What it doesn't do:**
- Generate learning content (agents do that)
- Make learning decisions (agents do that)
- Modify teaching philosophy (agents control that)

### 1.2 Data Models

```python
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    """Task completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"

class CheckpointStatus(str, Enum):
    """Understanding checkpoint status"""
    NOT_REACHED = "not_reached"
    IN_REVIEW = "in_review"
    PASSED = "passed"
    NEEDS_WORK = "needs_work"

class ComplexityLevel(str, Enum):
    """Learning complexity"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Task(BaseModel):
    """Individual learning task"""
    id: str = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: str = Field(description="Task description/instructions")
    status: TaskStatus = TaskStatus.NOT_STARTED
    learning_activity: Optional[str] = None
    research_questions: List[str] = Field(default_factory=list)
    checkpoint_questions: List[str] = Field(default_factory=list)
    specialist_agents: List[str] = Field(default_factory=list)
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

class Checkpoint(BaseModel):
    """Understanding checkpoint"""
    id: str = Field(description="Unique checkpoint identifier")
    title: str = Field(description="Checkpoint title")
    questions: List[str] = Field(description="Questions to verify understanding")
    status: CheckpointStatus = CheckpointStatus.NOT_REACHED
    passed_at: Optional[datetime] = None
    notes: Optional[str] = None

class Phase(BaseModel):
    """Learning phase"""
    id: str = Field(description="Unique phase identifier")
    number: int = Field(description="Phase number (1-based)")
    title: str = Field(description="Phase title")
    duration: Optional[str] = Field(description="e.g., 'Week 1-2'")
    learning_goals: List[str] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    checkpoints: List[Checkpoint] = Field(default_factory=list)
    specialist_support: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of specialist name to their role in this phase"
    )
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class JournalEntry(BaseModel):
    """Learning journal entry"""
    id: str = Field(description="Unique entry identifier")
    date: datetime = Field(default_factory=datetime.now)
    session_number: Optional[int] = None
    concepts_explored: Optional[str] = None
    key_insights: Optional[str] = None
    challenges: Optional[str] = None
    practice_done: Optional[str] = None
    questions_for_next_time: List[str] = Field(default_factory=list)
    raw_content: str = Field(description="Full markdown content")

class Prerequisite(BaseModel):
    """Prerequisite check item"""
    description: str
    completed: bool = False
    context: Optional[str] = None

class LearningPlanMetadata(BaseModel):
    """Plan header metadata"""
    title: str
    created: datetime
    last_updated: datetime
    estimated_time: str
    complexity_level: ComplexityLevel
    progress_summary: Optional[str] = None

class LearningPlan(BaseModel):
    """Complete learning plan structure"""
    metadata: LearningPlanMetadata
    learning_objectives: Dict[str, List[str]] = Field(
        description="Categories: 'what_you_will_learn', 'skills_you_will_develop', 'outcomes'"
    )
    prerequisites: List[Prerequisite] = Field(default_factory=list)
    phases: List[Phase] = Field(default_factory=list)
    learning_team: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of agent name to their role"
    )
    milestones: List[str] = Field(default_factory=list)
    journal_entries: List[JournalEntry] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    common_pitfalls: List[str] = Field(default_factory=list)
    file_path: Optional[str] = Field(description="Path to source markdown file")

    def get_current_phase(self) -> Optional[Phase]:
        """Get the currently active phase"""
        for phase in self.phases:
            if phase.started_at and not phase.completed_at:
                return phase
            # If no started phases, return first incomplete
            if not phase.started_at:
                return phase
        return None

    def get_next_task(self, phase_id: Optional[str] = None) -> Optional[Task]:
        """Get the next task to work on"""
        target_phase = self.get_current_phase() if not phase_id else self._get_phase_by_id(phase_id)
        if not target_phase:
            return None

        for task in target_phase.tasks:
            if task.status in [TaskStatus.NOT_STARTED, TaskStatus.IN_PROGRESS]:
                return task
        return None

    def calculate_progress(self) -> Dict[str, Any]:
        """Calculate progress statistics"""
        total_phases = len(self.phases)
        completed_phases = sum(1 for p in self.phases if p.completed_at)

        total_tasks = sum(len(p.tasks) for p in self.phases)
        completed_tasks = sum(
            sum(1 for t in p.tasks if t.status == TaskStatus.COMPLETED)
            for p in self.phases
        )

        total_checkpoints = sum(len(p.checkpoints) for p in self.phases)
        passed_checkpoints = sum(
            sum(1 for c in p.checkpoints if c.status == CheckpointStatus.PASSED)
            for p in self.phases
        )

        return {
            "phases": {
                "total": total_phases,
                "completed": completed_phases,
                "percentage": (completed_phases / total_phases * 100) if total_phases else 0
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "percentage": (completed_tasks / total_tasks * 100) if total_tasks else 0
            },
            "checkpoints": {
                "total": total_checkpoints,
                "passed": passed_checkpoints,
                "percentage": (passed_checkpoints / total_checkpoints * 100) if total_checkpoints else 0
            },
            "overall_percentage": (
                (completed_tasks / total_tasks * 0.7 + passed_checkpoints / total_checkpoints * 0.3) * 100
                if total_tasks and total_checkpoints else 0
            )
        }

    def _get_phase_by_id(self, phase_id: str) -> Optional[Phase]:
        """Helper to find phase by ID"""
        return next((p for p in self.phases if p.id == phase_id), None)
```

### 1.3 Core API

```python
from pathlib import Path
from typing import Optional, Dict, Any, List
import re
from datetime import datetime

class LearningPlanManager:
    """
    Main interface for learning plan operations.

    Usage in skills:
        manager = LearningPlanManager()
        plan = manager.load_plan("plans/2025-10-09-agent-optimization-learning-plan.md")
        progress = plan.calculate_progress()
        next_task = plan.get_next_task()
    """

    def __init__(self, plans_dir: Path = Path("plans")):
        self.plans_dir = plans_dir
        self.parser = LearningPlanParser()
        self.writer = LearningPlanWriter()
        self.validator = LearningPlanValidator()

    # ===== READ OPERATIONS =====

    def load_plan(self, file_path: str | Path) -> LearningPlan:
        """
        Load and parse a learning plan from markdown.

        Args:
            file_path: Path to learning plan markdown file

        Returns:
            Parsed LearningPlan object

        Raises:
            FileNotFoundError: If plan file doesn't exist
            ValidationError: If plan format is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Learning plan not found: {path}")

        content = path.read_text()
        plan = self.parser.parse(content)
        plan.file_path = str(path)

        # Validate structure
        self.validator.validate(plan)

        return plan

    def find_latest_plan(self) -> Optional[LearningPlan]:
        """
        Find the most recently updated learning plan.

        Returns:
            Latest LearningPlan or None if no plans exist
        """
        plan_files = list(self.plans_dir.glob("*-learning-plan.md"))
        if not plan_files:
            return None

        # Sort by last modified time
        latest_file = max(plan_files, key=lambda p: p.stat().st_mtime)
        return self.load_plan(latest_file)

    def list_plans(self) -> List[Dict[str, Any]]:
        """
        List all available learning plans with metadata.

        Returns:
            List of plan summaries
        """
        plans = []
        for plan_file in self.plans_dir.glob("*-learning-plan.md"):
            try:
                plan = self.load_plan(plan_file)
                progress = plan.calculate_progress()
                plans.append({
                    "file": str(plan_file),
                    "title": plan.metadata.title,
                    "created": plan.metadata.created,
                    "updated": plan.metadata.last_updated,
                    "progress": progress["overall_percentage"],
                    "current_phase": plan.get_current_phase().title if plan.get_current_phase() else None
                })
            except Exception as e:
                # Log but don't fail on individual plan errors
                print(f"Warning: Could not load {plan_file}: {e}")

        return sorted(plans, key=lambda p: p["updated"], reverse=True)

    # ===== WRITE OPERATIONS =====

    def update_task_status(
        self,
        plan: LearningPlan,
        task_id: str,
        status: TaskStatus,
        notes: Optional[str] = None
    ) -> LearningPlan:
        """
        Update a task's status.

        Args:
            plan: LearningPlan to update
            task_id: Task identifier
            status: New status
            notes: Optional notes about the update

        Returns:
            Updated LearningPlan
        """
        for phase in plan.phases:
            for task in phase.tasks:
                if task.id == task_id:
                    task.status = status
                    if notes:
                        task.notes = notes
                    if status == TaskStatus.COMPLETED:
                        task.completed_at = datetime.now()
                    break

        plan.metadata.last_updated = datetime.now()
        return plan

    def update_checkpoint_status(
        self,
        plan: LearningPlan,
        checkpoint_id: str,
        status: CheckpointStatus,
        notes: Optional[str] = None
    ) -> LearningPlan:
        """Update a checkpoint's status"""
        for phase in plan.phases:
            for checkpoint in phase.checkpoints:
                if checkpoint.id == checkpoint_id:
                    checkpoint.status = status
                    if notes:
                        checkpoint.notes = notes
                    if status == CheckpointStatus.PASSED:
                        checkpoint.passed_at = datetime.now()
                    break

        plan.metadata.last_updated = datetime.now()
        return plan

    def add_journal_entry(
        self,
        plan: LearningPlan,
        entry: JournalEntry
    ) -> LearningPlan:
        """Add a new journal entry"""
        plan.journal_entries.append(entry)
        plan.metadata.last_updated = datetime.now()
        return plan

    def mark_phase_started(self, plan: LearningPlan, phase_id: str) -> LearningPlan:
        """Mark a phase as started"""
        phase = plan._get_phase_by_id(phase_id)
        if phase and not phase.started_at:
            phase.started_at = datetime.now()
            plan.metadata.last_updated = datetime.now()
        return plan

    def mark_phase_completed(self, plan: LearningPlan, phase_id: str) -> LearningPlan:
        """Mark a phase as completed"""
        phase = plan._get_phase_by_id(phase_id)
        if phase and not phase.completed_at:
            phase.completed_at = datetime.now()
            plan.metadata.last_updated = datetime.now()
        return plan

    def save_plan(self, plan: LearningPlan) -> Path:
        """
        Save plan back to markdown file.

        Args:
            plan: LearningPlan to save

        Returns:
            Path to saved file
        """
        if not plan.file_path:
            raise ValueError("Plan must have file_path set to save")

        markdown_content = self.writer.write(plan)
        path = Path(plan.file_path)
        path.write_text(markdown_content)

        return path

    # ===== QUERY OPERATIONS =====

    def get_phase_summary(self, plan: LearningPlan, phase_id: str) -> Dict[str, Any]:
        """Get detailed summary of a phase"""
        phase = plan._get_phase_by_id(phase_id)
        if not phase:
            return {}

        return {
            "id": phase.id,
            "number": phase.number,
            "title": phase.title,
            "duration": phase.duration,
            "started": phase.started_at,
            "completed": phase.completed_at,
            "learning_goals": phase.learning_goals,
            "tasks": {
                "total": len(phase.tasks),
                "completed": sum(1 for t in phase.tasks if t.status == TaskStatus.COMPLETED),
                "in_progress": sum(1 for t in phase.tasks if t.status == TaskStatus.IN_PROGRESS),
                "not_started": sum(1 for t in phase.tasks if t.status == TaskStatus.NOT_STARTED)
            },
            "checkpoints": {
                "total": len(phase.checkpoints),
                "passed": sum(1 for c in phase.checkpoints if c.status == CheckpointStatus.PASSED)
            },
            "specialists": phase.specialist_support
        }

    def search_tasks(self, plan: LearningPlan, query: str) -> List[Task]:
        """Search for tasks matching query"""
        results = []
        query_lower = query.lower()

        for phase in plan.phases:
            for task in phase.tasks:
                if (query_lower in task.title.lower() or
                    query_lower in task.description.lower()):
                    results.append(task)

        return results

    # ===== EXPORT OPERATIONS =====

    def export_json(self, plan: LearningPlan) -> str:
        """Export plan as JSON"""
        return plan.model_dump_json(indent=2)

    def export_progress_report(self, plan: LearningPlan) -> str:
        """Generate a human-readable progress report"""
        progress = plan.calculate_progress()
        current_phase = plan.get_current_phase()
        next_task = plan.get_next_task()

        report = f"""# Learning Progress Report

## {plan.metadata.title}

**Last Updated**: {plan.metadata.last_updated.strftime("%Y-%m-%d %H:%M")}
**Estimated Time**: {plan.metadata.estimated_time}
**Complexity**: {plan.metadata.complexity_level.value}

## Overall Progress: {progress['overall_percentage']:.1f}%

### Phases: {progress['phases']['completed']}/{progress['phases']['total']} ({progress['phases']['percentage']:.1f}%)
### Tasks: {progress['tasks']['completed']}/{progress['tasks']['total']} ({progress['tasks']['percentage']:.1f}%)
### Checkpoints: {progress['checkpoints']['passed']}/{progress['checkpoints']['total']} ({progress['checkpoints']['percentage']:.1f}%)

## Current Status

"""
        if current_phase:
            report += f"**Current Phase**: Phase {current_phase.number} - {current_phase.title}\n\n"

        if next_task:
            report += f"**Next Task**: {next_task.title}\n\n"

        # Add phase breakdown
        report += "## Phase Breakdown\n\n"
        for phase in plan.phases:
            status_icon = "✅" if phase.completed_at else "🔄" if phase.started_at else "⏳"
            report += f"### {status_icon} Phase {phase.number}: {phase.title}\n\n"

            phase_summary = self.get_phase_summary(plan, phase.id)
            report += f"- Tasks: {phase_summary['tasks']['completed']}/{phase_summary['tasks']['total']}\n"
            report += f"- Checkpoints: {phase_summary['checkpoints']['passed']}/{phase_summary['checkpoints']['total']}\n"
            if phase.started_at:
                report += f"- Started: {phase.started_at.strftime('%Y-%m-%d')}\n"
            if phase.completed_at:
                report += f"- Completed: {phase.completed_at.strftime('%Y-%m-%d')}\n"
            report += "\n"

        return report


class LearningPlanParser:
    """Parses markdown learning plans into LearningPlan objects"""

    def parse(self, markdown_content: str) -> LearningPlan:
        """Parse markdown content into LearningPlan"""
        # Implementation: Parse markdown sections using regex and markdown parser
        # This is a complex parser - see implementation details below
        pass


class LearningPlanWriter:
    """Writes LearningPlan objects back to markdown"""

    def write(self, plan: LearningPlan) -> str:
        """Convert LearningPlan to markdown"""
        # Implementation: Generate markdown from structured data
        # Preserves the teaching-focused format
        pass


class LearningPlanValidator:
    """Validates learning plan structure"""

    def validate(self, plan: LearningPlan) -> None:
        """Validate plan structure, raises ValidationError if invalid"""
        # Check required sections
        # Validate phase numbering
        # Ensure checkpoints exist
        # Verify specialist references are valid
        pass
```

### 1.4 Skill Definition

```markdown
---
name: learning-plan-manager
description: Structured operations on learning plan markdown files. Parse, query, update, and export learning plans without manual markdown manipulation.
tools:
  - Read
  - Write
activation: manual
---

You are the **learning-plan-manager** skill, providing structured data operations on learning plan markdown files.

## Your Capabilities

You can:
- **Parse** learning plan markdown into structured data
- **Query** plan status, progress, current phase, next tasks
- **Update** task status, checkpoints, journal entries
- **Export** to JSON, HTML, PDF, progress reports
- **Validate** plan structure and format

## When Invoked

Agents invoke you when they need to:
1. Find the current phase in a learning plan
2. Get the next task to work on
3. Update task or checkpoint status
4. Add journal entries
5. Calculate progress statistics
6. Generate progress reports
7. Search for specific tasks

## How You Work

1. **Load** the learning plan from markdown
2. **Parse** into LearningPlan object with phases, tasks, checkpoints
3. **Process** the requested operation
4. **Return** structured data (JSON) or updated markdown

## Output Format

Always return results as structured JSON that agents can easily consume:

```json
{
  "operation": "query_current_phase",
  "result": {
    "phase_number": 1,
    "phase_title": "Understanding & Research",
    "next_task": {
      "id": "task-1-2",
      "title": "Pattern Analysis Exercise",
      "status": "not_started"
    },
    "progress": {
      "overall_percentage": 23.5,
      "tasks_completed": 5,
      "tasks_total": 21
    }
  }
}
```

## Usage Examples

### Example 1: Find Current Status
```
Query: What phase is the student in for the agent-optimization plan?

Action: Load plan, identify current phase
Response: {
  "current_phase": "Phase 1: Understanding & Research",
  "phase_number": 1,
  "next_task": "Task 1.2: Pattern Analysis Exercise",
  "progress_percentage": 23.5
}
```

### Example 2: Update Task Status
```
Query: Mark task-1-1 as completed

Action: Load plan, update task status, save
Response: {
  "task_id": "task-1-1",
  "previous_status": "in_progress",
  "new_status": "completed",
  "completed_at": "2025-10-19T10:30:00",
  "overall_progress": 28.3
}
```

### Example 3: Generate Progress Report
```
Query: Generate a progress report

Action: Load plan, calculate all metrics, format report
Response: (Full markdown progress report)
```

## Integration with Agents

Agents should use you for:
- **continue-plan command**: Find where student left off
- **update-plan command**: Track completions
- **learning-coordinator**: Monitor student progress
- **plan-generation-mentor**: Validate generated plans

## Important Notes

- You parse and manipulate data, agents provide teaching guidance
- You preserve the markdown format and teaching philosophy
- You validate structure but don't judge content
- You're stateless - each invocation is independent

Ready to provide structured learning plan operations!
```

### 1.5 Implementation Details

#### Parser Implementation Strategy

```python
# Key parsing challenges and solutions:

1. Metadata Section
   - Use regex to extract YAML-like frontmatter
   - Parse dates, complexity levels, progress indicators

2. Learning Objectives
   - Identify section by header (##)
   - Parse subsections (###)
   - Extract bullet points into lists

3. Prerequisites
   - Find checkbox items (- [ ] or - [x])
   - Track completion status
   - Extract context notes

4. Phases
   - Identify by "## Phase N:" header
   - Extract learning goals, tasks, checkpoints
   - Parse task metadata (status markers like ✅, 🔄, ⏳)
   - Handle nested structures

5. Journal Entries
   - Parse by date headers (###)
   - Extract structured fields
   - Preserve raw content for flexible format

6. State Markers
   - Detect progress indicators in text (✅, 🔄, ⏳)
   - Parse "IN PROGRESS", "COMPLETED" markers
   - Track timestamps from text
```

---

## Skill 2: code-analysis

### 2.1 Purpose & Scope

**What it does:**
- Parse source code into AST (Abstract Syntax Tree)
- Extract architectural patterns and structures
- Calculate code complexity metrics
- Build dependency graphs
- Detect design patterns
- Identify integration points
- Find anti-patterns and code smells

**What it doesn't do:**
- Execute code or run tests
- Suggest specific fixes (agents do that)
- Make architectural decisions (agents guide students)
- Modify code (that's Edit tool's job)

### 2.2 Data Models

```python
from enum import Enum
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field
from pathlib import Path

class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    C = "c"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    GO = "go"

class NodeType(str, Enum):
    """AST node types"""
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    IMPORT = "import"
    MODULE = "module"
    INTERFACE = "interface"
    STRUCT = "struct"

class DesignPattern(str, Enum):
    """Detected design patterns"""
    SINGLETON = "singleton"
    FACTORY = "factory"
    OBSERVER = "observer"
    STRATEGY = "strategy"
    DECORATOR = "decorator"
    ADAPTER = "adapter"
    COMMAND = "command"
    TEMPLATE_METHOD = "template_method"
    STATE = "state"
    FACADE = "facade"

class CodeSmell(str, Enum):
    """Common code smells"""
    LONG_METHOD = "long_method"
    LONG_CLASS = "long_class"
    TOO_MANY_PARAMETERS = "too_many_parameters"
    DUPLICATE_CODE = "duplicate_code"
    DEAD_CODE = "dead_code"
    COMPLEX_CONDITIONAL = "complex_conditional"
    MUTABLE_DEFAULT_ARG = "mutable_default_arg"  # Python
    MAGIC_NUMBER = "magic_number"

class ComplexityMetrics(BaseModel):
    """Code complexity metrics"""
    cyclomatic_complexity: int = Field(description="McCabe complexity")
    cognitive_complexity: int = Field(description="Cognitive complexity score")
    halstead_volume: Optional[float] = None
    maintainability_index: Optional[float] = None
    lines_of_code: int = 0
    comment_lines: int = 0
    blank_lines: int = 0

class CodeNode(BaseModel):
    """Represents a code entity (class, function, etc.)"""
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Entity name")
    node_type: NodeType
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parameters: List[str] = Field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)
    complexity: Optional[ComplexityMetrics] = None
    dependencies: List[str] = Field(default_factory=list, description="IDs of nodes this depends on")
    is_public: bool = True
    is_async: bool = False

class FileAnalysis(BaseModel):
    """Analysis of a single file"""
    file_path: str
    language: Language
    nodes: List[CodeNode] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    exports: List[str] = Field(default_factory=list)
    patterns: List[DesignPattern] = Field(default_factory=list)
    smells: List[Dict[str, Any]] = Field(default_factory=list)
    complexity: ComplexityMetrics
    lines_of_code: int
    test_file: bool = False

class DependencyGraph(BaseModel):
    """Dependency graph representation"""
    nodes: Dict[str, CodeNode] = Field(description="Map of node ID to node")
    edges: List[Dict[str, str]] = Field(description="List of {from, to} edges")

    def get_dependents(self, node_id: str) -> List[str]:
        """Get all nodes that depend on this node"""
        return [e["from"] for e in self.edges if e["to"] == node_id]

    def get_dependencies(self, node_id: str) -> List[str]:
        """Get all nodes this node depends on"""
        node = self.nodes.get(node_id)
        return node.dependencies if node else []

    def find_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependency chains"""
        # Implementation: Graph cycle detection
        pass

class ArchitecturalPattern(BaseModel):
    """Detected architectural pattern"""
    pattern: str = Field(description="Pattern name (e.g., 'MVC', 'Layered')")
    confidence: float = Field(description="Confidence score 0-1")
    evidence: List[str] = Field(description="Why we think this pattern exists")
    files_involved: List[str] = Field(default_factory=list)

class IntegrationPoint(BaseModel):
    """Identified integration point in codebase"""
    name: str
    location: str = Field(description="File:line")
    integration_type: str = Field(description="e.g., 'REST API', 'Database', 'ROS2 Topic'")
    description: str
    related_files: List[str] = Field(default_factory=list)

class CodebaseAnalysis(BaseModel):
    """Complete codebase analysis"""
    root_path: str
    language_breakdown: Dict[Language, int] = Field(description="Lines per language")
    files_analyzed: List[FileAnalysis] = Field(default_factory=list)
    dependency_graph: DependencyGraph
    architectural_patterns: List[ArchitecturalPattern] = Field(default_factory=list)
    integration_points: List[IntegrationPoint] = Field(default_factory=list)
    entry_points: List[str] = Field(description="Main files, __init__.py, etc.")
    test_coverage_estimate: Optional[float] = None

    def get_files_by_pattern(self, pattern: DesignPattern) -> List[str]:
        """Find files implementing a specific pattern"""
        return [
            f.file_path for f in self.files_analyzed
            if pattern in f.patterns
        ]

    def find_related_files(self, file_path: str, max_depth: int = 2) -> List[str]:
        """Find files related through dependencies"""
        # Implementation: BFS through dependency graph
        pass

    def suggest_integration_locations(self, feature_type: str) -> List[IntegrationPoint]:
        """Suggest where to integrate a new feature"""
        # Implementation: Pattern matching and heuristics
        pass
```

### 2.3 Core API

```python
from pathlib import Path
from typing import List, Optional, Dict, Any
import ast
import tree_sitter

class CodeAnalyzer:
    """
    Main interface for code analysis operations.

    Usage in skills:
        analyzer = CodeAnalyzer()
        analysis = analyzer.analyze_codebase("src/")
        patterns = analysis.architectural_patterns
        integration_points = analysis.suggest_integration_locations("ROS2 Node")
    """

    def __init__(self):
        self.python_analyzer = PythonAnalyzer()
        self.cpp_analyzer = CppAnalyzer()
        self.pattern_detector = PatternDetector()
        self.metrics_calculator = MetricsCalculator()

    # ===== CODEBASE-LEVEL ANALYSIS =====

    def analyze_codebase(
        self,
        root_path: str | Path,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        max_files: Optional[int] = None
    ) -> CodebaseAnalysis:
        """
        Analyze an entire codebase.

        Args:
            root_path: Root directory to analyze
            include_patterns: Glob patterns to include (e.g., ["src/**/*.py"])
            exclude_patterns: Patterns to exclude (e.g., ["**/test_*.py"])
            max_files: Maximum files to analyze (for large codebases)

        Returns:
            Complete CodebaseAnalysis
        """
        root = Path(root_path)

        # Discover files
        files_to_analyze = self._discover_files(
            root, include_patterns, exclude_patterns, max_files
        )

        # Analyze each file
        file_analyses = []
        for file_path in files_to_analyze:
            try:
                analysis = self.analyze_file(file_path)
                file_analyses.append(analysis)
            except Exception as e:
                print(f"Warning: Could not analyze {file_path}: {e}")

        # Build dependency graph
        dep_graph = self._build_dependency_graph(file_analyses)

        # Detect architectural patterns
        arch_patterns = self.pattern_detector.detect_architectural_patterns(
            file_analyses, dep_graph
        )

        # Find integration points
        integration_points = self._identify_integration_points(file_analyses)

        # Calculate language breakdown
        language_breakdown = self._calculate_language_breakdown(file_analyses)

        # Find entry points
        entry_points = self._find_entry_points(file_analyses)

        return CodebaseAnalysis(
            root_path=str(root),
            language_breakdown=language_breakdown,
            files_analyzed=file_analyses,
            dependency_graph=dep_graph,
            architectural_patterns=arch_patterns,
            integration_points=integration_points,
            entry_points=entry_points
        )

    # ===== FILE-LEVEL ANALYSIS =====

    def analyze_file(self, file_path: str | Path) -> FileAnalysis:
        """
        Analyze a single source file.

        Args:
            file_path: Path to source file

        Returns:
            FileAnalysis for the file
        """
        path = Path(file_path)
        language = self._detect_language(path)

        if language == Language.PYTHON:
            return self.python_analyzer.analyze(path)
        elif language in [Language.CPP, Language.C]:
            return self.cpp_analyzer.analyze(path)
        else:
            # Generic analysis for other languages
            return self._generic_analysis(path, language)

    # ===== PATTERN DETECTION =====

    def detect_patterns(self, file_path: str | Path) -> List[DesignPattern]:
        """
        Detect design patterns in a file.

        Returns:
            List of detected patterns
        """
        analysis = self.analyze_file(file_path)
        return self.pattern_detector.detect_file_patterns(analysis)

    def detect_code_smells(self, file_path: str | Path) -> List[Dict[str, Any]]:
        """
        Detect code smells in a file.

        Returns:
            List of code smells with locations and descriptions
        """
        analysis = self.analyze_file(file_path)
        return self._detect_smells(analysis)

    # ===== METRICS =====

    def calculate_complexity(self, file_path: str | Path) -> ComplexityMetrics:
        """Calculate complexity metrics for a file"""
        analysis = self.analyze_file(file_path)
        return analysis.complexity

    def calculate_function_complexity(
        self,
        file_path: str | Path,
        function_name: str
    ) -> Optional[ComplexityMetrics]:
        """Calculate complexity for a specific function"""
        analysis = self.analyze_file(file_path)
        for node in analysis.nodes:
            if node.name == function_name and node.node_type in [NodeType.FUNCTION, NodeType.METHOD]:
                return node.complexity
        return None

    # ===== DEPENDENCY ANALYSIS =====

    def build_call_graph(
        self,
        root_path: str | Path,
        entry_point: Optional[str] = None
    ) -> DependencyGraph:
        """
        Build a call graph showing function/method calls.

        Args:
            root_path: Root directory
            entry_point: Optional entry point file to start from

        Returns:
            DependencyGraph representing call relationships
        """
        analysis = self.analyze_codebase(root_path)
        return analysis.dependency_graph

    def find_integration_points(
        self,
        root_path: str | Path,
        feature_description: str
    ) -> List[IntegrationPoint]:
        """
        Find suitable integration points for a new feature.

        Args:
            root_path: Codebase root
            feature_description: Description of feature to integrate

        Returns:
            List of suggested integration points
        """
        analysis = self.analyze_codebase(root_path)
        return analysis.suggest_integration_locations(feature_description)

    # ===== HELPER METHODS =====

    def _detect_language(self, file_path: Path) -> Language:
        """Detect programming language from file extension"""
        ext = file_path.suffix.lower()
        mapping = {
            ".py": Language.PYTHON,
            ".cpp": Language.CPP,
            ".cc": Language.CPP,
            ".cxx": Language.CPP,
            ".hpp": Language.CPP,
            ".h": Language.C,  # Could be C or C++, context needed
            ".c": Language.C,
            ".js": Language.JAVASCRIPT,
            ".ts": Language.TYPESCRIPT,
            ".rs": Language.RUST,
            ".go": Language.GO
        }
        return mapping.get(ext, Language.PYTHON)  # Default to Python

    def _discover_files(
        self,
        root: Path,
        include: Optional[List[str]],
        exclude: Optional[List[str]],
        max_files: Optional[int]
    ) -> List[Path]:
        """Discover files to analyze based on patterns"""
        # Default patterns if not specified
        if not include:
            include = ["**/*.py", "**/*.cpp", "**/*.c", "**/*.h"]

        exclude = exclude or ["**/__pycache__/**", "**/node_modules/**", "**/.git/**"]

        files = []
        for pattern in include:
            for file_path in root.glob(pattern):
                if file_path.is_file():
                    # Check exclusions
                    if not any(file_path.match(ex_pattern) for ex_pattern in exclude):
                        files.append(file_path)
                        if max_files and len(files) >= max_files:
                            return files

        return files

    def _build_dependency_graph(self, file_analyses: List[FileAnalysis]) -> DependencyGraph:
        """Build dependency graph from file analyses"""
        # Implementation: Create nodes and edges from imports and calls
        pass

    def _identify_integration_points(self, file_analyses: List[FileAnalysis]) -> List[IntegrationPoint]:
        """Identify integration points (APIs, interfaces, etc.)"""
        # Implementation: Look for public APIs, ROS2 topics, REST endpoints, etc.
        pass

    def _calculate_language_breakdown(self, file_analyses: List[FileAnalysis]) -> Dict[Language, int]:
        """Calculate lines of code per language"""
        breakdown = {}
        for analysis in file_analyses:
            if analysis.language not in breakdown:
                breakdown[analysis.language] = 0
            breakdown[analysis.language] += analysis.lines_of_code
        return breakdown

    def _find_entry_points(self, file_analyses: List[FileAnalysis]) -> List[str]:
        """Find entry point files (main.py, __init__.py, etc.)"""
        entry_points = []
        for analysis in file_analyses:
            file_name = Path(analysis.file_path).name
            if file_name in ["main.py", "__main__.py", "__init__.py", "app.py", "index.js"]:
                entry_points.append(analysis.file_path)
            # Also check for if __name__ == "__main__":
            for node in analysis.nodes:
                if node.name == "__main__":
                    entry_points.append(analysis.file_path)
                    break
        return entry_points

    def _detect_smells(self, analysis: FileAnalysis) -> List[Dict[str, Any]]:
        """Detect code smells in a file analysis"""
        smells = []

        for node in analysis.nodes:
            # Long method
            if node.complexity and node.complexity.cyclomatic_complexity > 10:
                smells.append({
                    "smell": CodeSmell.LONG_METHOD,
                    "location": f"{analysis.file_path}:{node.line_start}",
                    "name": node.name,
                    "description": f"Method {node.name} has high complexity ({node.complexity.cyclomatic_complexity})",
                    "severity": "medium"
                })

            # Too many parameters
            if len(node.parameters) > 5:
                smells.append({
                    "smell": CodeSmell.TOO_MANY_PARAMETERS,
                    "location": f"{analysis.file_path}:{node.line_start}",
                    "name": node.name,
                    "description": f"{node.name} has {len(node.parameters)} parameters",
                    "severity": "low"
                })

        # Long class
        if analysis.complexity.lines_of_code > 500:
            smells.append({
                "smell": CodeSmell.LONG_CLASS,
                "location": analysis.file_path,
                "description": f"File has {analysis.complexity.lines_of_code} lines",
                "severity": "medium"
            })

        return smells


class PythonAnalyzer:
    """Python-specific code analysis using ast module"""

    def analyze(self, file_path: Path) -> FileAnalysis:
        """Analyze a Python file"""
        content = file_path.read_text()
        tree = ast.parse(content)

        nodes = []
        imports = []

        # Extract nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                nodes.append(self._extract_class(node, str(file_path)))
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                nodes.append(self._extract_function(node, str(file_path)))
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.extend(self._extract_imports(node))

        # Calculate metrics
        complexity = self._calculate_file_complexity(tree)

        # Detect patterns
        patterns = self._detect_patterns(tree, nodes)

        return FileAnalysis(
            file_path=str(file_path),
            language=Language.PYTHON,
            nodes=nodes,
            imports=imports,
            patterns=patterns,
            complexity=complexity,
            lines_of_code=len(content.splitlines()),
            test_file=self._is_test_file(file_path)
        )

    def _extract_class(self, node: ast.ClassDef, file_path: str) -> CodeNode:
        """Extract class information"""
        # Implementation: Extract class details
        pass

    def _extract_function(self, node: ast.FunctionDef, file_path: str) -> CodeNode:
        """Extract function information"""
        # Calculate complexity for function
        complexity = self._calculate_function_complexity(node)

        return CodeNode(
            id=f"{file_path}:{node.name}",
            name=node.name,
            node_type=NodeType.FUNCTION,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=ast.get_docstring(node),
            parameters=[arg.arg for arg in node.args.args],
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            complexity=complexity,
            is_async=isinstance(node, ast.AsyncFunctionDef)
        )

    def _extract_imports(self, node: ast.Import | ast.ImportFrom) -> List[str]:
        """Extract import names"""
        if isinstance(node, ast.Import):
            return [alias.name for alias in node.names]
        else:  # ImportFrom
            module = node.module or ""
            return [f"{module}.{alias.name}" for alias in node.names]

    def _calculate_function_complexity(self, node: ast.FunctionDef) -> ComplexityMetrics:
        """Calculate cyclomatic complexity for a function"""
        # Count decision points
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            # Each if, for, while, except adds 1
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            # Each boolean operator adds 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        loc = node.end_lineno - node.lineno + 1 if node.end_lineno else 0

        return ComplexityMetrics(
            cyclomatic_complexity=complexity,
            cognitive_complexity=complexity,  # Simplified
            lines_of_code=loc,
            comment_lines=0,  # Would need to parse comments
            blank_lines=0
        )

    def _calculate_file_complexity(self, tree: ast.AST) -> ComplexityMetrics:
        """Calculate overall file complexity"""
        # Sum of all function complexities
        pass

    def _detect_patterns(self, tree: ast.AST, nodes: List[CodeNode]) -> List[DesignPattern]:
        """Detect design patterns in Python code"""
        patterns = []

        # Singleton pattern detection
        if self._has_singleton_pattern(tree):
            patterns.append(DesignPattern.SINGLETON)

        # Factory pattern detection
        if self._has_factory_pattern(nodes):
            patterns.append(DesignPattern.FACTORY)

        # Decorator pattern (Python decorators)
        if self._has_decorator_pattern(nodes):
            patterns.append(DesignPattern.DECORATOR)

        return patterns

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file"""
        return (
            file_path.name.startswith("test_") or
            file_path.name.endswith("_test.py") or
            "test" in file_path.parts
        )

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return "unknown"

    def _has_singleton_pattern(self, tree: ast.AST) -> bool:
        """Detect singleton pattern"""
        # Look for __new__ override or module-level instance
        pass

    def _has_factory_pattern(self, nodes: List[CodeNode]) -> bool:
        """Detect factory pattern"""
        # Look for create_* methods or Factory classes
        pass

    def _has_decorator_pattern(self, nodes: List[CodeNode]) -> bool:
        """Detect decorator pattern (not Python @decorators)"""
        # Look for wrapper classes
        pass


class CppAnalyzer:
    """C++ code analysis using tree-sitter"""

    def __init__(self):
        # Initialize tree-sitter for C++
        pass

    def analyze(self, file_path: Path) -> FileAnalysis:
        """Analyze a C++ file"""
        # Implementation using tree-sitter
        pass


class PatternDetector:
    """Detects design patterns and architectural patterns"""

    def detect_file_patterns(self, analysis: FileAnalysis) -> List[DesignPattern]:
        """Detect design patterns in a single file"""
        pass

    def detect_architectural_patterns(
        self,
        file_analyses: List[FileAnalysis],
        dep_graph: DependencyGraph
    ) -> List[ArchitecturalPattern]:
        """Detect architectural patterns across codebase"""
        patterns = []

        # MVC pattern
        if self._has_mvc_structure(file_analyses):
            patterns.append(ArchitecturalPattern(
                pattern="MVC",
                confidence=0.8,
                evidence=[
                    "Found model/ directory with data classes",
                    "Found view/ directory with UI components",
                    "Found controller/ directory with business logic"
                ],
                files_involved=self._get_mvc_files(file_analyses)
            ))

        # Layered architecture
        if self._has_layered_structure(file_analyses):
            patterns.append(ArchitecturalPattern(
                pattern="Layered",
                confidence=0.7,
                evidence=[
                    "Found src/ with subdirectories for different layers",
                    "Clear separation between data access and business logic"
                ],
                files_involved=[]
            ))

        # Microservices (multiple main entry points)
        if self._has_microservices_structure(file_analyses):
            patterns.append(ArchitecturalPattern(
                pattern="Microservices",
                confidence=0.6,
                evidence=["Multiple independent entry points found"],
                files_involved=[]
            ))

        return patterns

    def _has_mvc_structure(self, analyses: List[FileAnalysis]) -> bool:
        """Check for MVC pattern"""
        paths = [a.file_path for a in analyses]
        has_model = any("model" in p.lower() for p in paths)
        has_view = any("view" in p.lower() for p in paths)
        has_controller = any("controller" in p.lower() for p in paths)
        return has_model and has_view and has_controller

    def _has_layered_structure(self, analyses: List[FileAnalysis]) -> bool:
        """Check for layered architecture"""
        # Look for common layer names
        pass

    def _has_microservices_structure(self, analyses: List[FileAnalysis]) -> bool:
        """Check for microservices pattern"""
        # Count independent entry points
        pass

    def _get_mvc_files(self, analyses: List[FileAnalysis]) -> List[str]:
        """Get files involved in MVC pattern"""
        return [
            a.file_path for a in analyses
            if any(keyword in a.file_path.lower() for keyword in ["model", "view", "controller"])
        ]


class MetricsCalculator:
    """Calculate various code metrics"""

    def calculate_maintainability_index(self, complexity: ComplexityMetrics) -> float:
        """Calculate maintainability index (0-100)"""
        # Microsoft formula
        pass

    def calculate_halstead_metrics(self, code: str) -> Dict[str, float]:
        """Calculate Halstead complexity metrics"""
        pass
```

### 2.4 Skill Definition

```markdown
---
name: code-analysis
description: Deep static code analysis providing AST parsing, complexity metrics, dependency graphs, pattern detection, and integration point identification. Goes far beyond basic Grep/Glob.
tools:
  - Read
  - Glob
  - Grep
activation: manual
---

You are the **code-analysis** skill, providing deep static analysis of source code.

## Your Capabilities

You can:
- **Parse** code into Abstract Syntax Trees (AST)
- **Extract** classes, functions, methods, variables
- **Calculate** complexity metrics (cyclomatic, cognitive, Halstead)
- **Build** dependency and call graphs
- **Detect** design patterns (Singleton, Factory, Observer, etc.)
- **Identify** architectural patterns (MVC, Layered, Microservices)
- **Find** integration points for new features
- **Detect** code smells and anti-patterns
- **Analyze** entire codebases or single files

## When Invoked

Agents invoke you when they need to:
1. Understand codebase architecture
2. Find where to integrate a new feature
3. Detect what patterns are already in use
4. Calculate code complexity
5. Build dependency graphs
6. Find related files
7. Identify code smells for refactoring

## How You Work

1. **Discover** files to analyze (using Glob)
2. **Read** source files
3. **Parse** into AST using language-specific parsers
4. **Extract** structural information
5. **Calculate** metrics and detect patterns
6. **Build** dependency graphs
7. **Return** structured analysis

## Output Format

Return structured JSON that agents can interpret:

```json
{
  "operation": "analyze_codebase",
  "root_path": "src/",
  "summary": {
    "total_files": 45,
    "total_lines": 5243,
    "languages": {
      "python": 4500,
      "cpp": 743
    },
    "patterns_detected": ["MVC", "Singleton", "Factory"],
    "entry_points": ["src/main.py", "src/cli.py"]
  },
  "integration_points": [
    {
      "name": "AgentClient",
      "location": "src/agent_client.py:25",
      "type": "Class",
      "description": "Main client for agent SDK integration",
      "suggested_for": "Adding new agent types"
    }
  ],
  "dependency_graph": {
    "nodes_count": 123,
    "circular_dependencies": []
  }
}
```

## Usage Examples

### Example 1: Find Integration Points
```
Query: Where should I integrate a new ROS2 node type in this codebase?

Action:
1. Analyze codebase structure
2. Find existing ROS2 node patterns
3. Identify extension points
4. Suggest integration locations

Response: {
  "suggested_locations": [
    {
      "file": "src/ros2_nodes/base_node.py",
      "reason": "Base class for ROS2 nodes, implement here",
      "pattern": "Template Method pattern detected",
      "example_subclasses": ["SensorNode", "ControllerNode"]
    }
  ]
}
```

### Example 2: Detect Patterns
```
Query: What design patterns are used in src/agents/?

Action: Analyze agent files, detect patterns

Response: {
  "patterns_found": [
    {
      "pattern": "Factory",
      "files": ["agent_factory.py"],
      "confidence": 0.9,
      "evidence": "create_agent() methods for different agent types"
    },
    {
      "pattern": "Strategy",
      "files": ["learning_strategy.py", "teaching_strategy.py"],
      "confidence": 0.85,
      "evidence": "Interchangeable algorithm classes"
    }
  ]
}
```

### Example 3: Calculate Complexity
```
Query: Which functions in this file are too complex?

Action: Analyze file, calculate complexity, flag high-complexity functions

Response: {
  "file": "src/complex_module.py",
  "high_complexity_functions": [
    {
      "name": "process_learning_data",
      "line": 45,
      "cyclomatic_complexity": 15,
      "cognitive_complexity": 18,
      "recommendation": "Consider breaking into smaller functions"
    }
  ]
}
```

## Integration with Agents

Agents should use you for:
- **file-search-agent**: Enhanced codebase understanding
- **code-architecture-mentor**: Identifying existing patterns
- **python-best-practices**: Finding anti-patterns
- **debugging-detective**: Understanding code paths
- **plan-generation-mentor**: Finding integration points for new features

## Language Support

- **Full Support**: Python (using ast module)
- **Good Support**: C++ (using tree-sitter)
- **Basic Support**: JavaScript, TypeScript, Rust, Go

## Important Notes

- You analyze code structure, agents interpret and teach
- You detect patterns, agents explain when to use them
- You find complexity, agents guide refactoring
- You're read-only - never modify code

Ready to provide deep code intelligence!
```

### 2.5 Implementation Priority

**Phase 2A (Weeks 1-2): Python Analysis**
- Implement Python AST parser
- Extract classes, functions, imports
- Calculate basic complexity metrics
- Detect simple patterns (Singleton, Factory)

**Phase 2B (Weeks 3): Dependency Graphs**
- Build import dependency graph
- Detect circular dependencies
- Find related files

**Phase 2C (Week 4): Pattern Detection & Integration**
- Architectural pattern detection
- Integration point identification
- Code smell detection

**Phase 2D (Future): Extended Language Support**
- Implement C++ analyzer with tree-sitter
- Add JavaScript/TypeScript support

---

## Integration Architecture

### How Skills Work with Agents

```
┌─────────────────────────────────────────────────────────┐
│ Agent (e.g., file-search-agent)                         │
│                                                          │
│ Task: Find where to add obstacle avoidance feature      │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Invokes skill via Skill tool
                 ↓
┌─────────────────────────────────────────────────────────┐
│ code-analysis skill                                      │
│                                                          │
│ 1. Analyze codebase (src/navigation/)                   │
│ 2. Build dependency graph                               │
│ 3. Detect patterns (Path Planning → Strategy pattern)   │
│ 4. Identify integration points                          │
│ 5. Return structured JSON                               │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Returns analysis results
                 ↓
┌─────────────────────────────────────────────────────────┐
│ Agent interprets results                                 │
│                                                          │
│ - Sees PathPlanner base class exists                    │
│ - Sees Strategy pattern for algorithms                  │
│ - Formulates teaching response                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ Agent teaches, doesn't just report
                 ↓
┌─────────────────────────────────────────────────────────┐
│ Student Response                                         │
│                                                          │
│ "I see there's a PathPlanner base class. This uses      │
│  the Strategy pattern, which makes sense because you    │
│  can swap different algorithms (A*, RRT, etc.).         │
│                                                          │
│  To add obstacle avoidance, you could:                  │
│  1. Extend the PathPlanner interface if needed          │
│  2. Create a new algorithm strategy                     │
│  3. Integrate with existing sensor data flow            │
│                                                          │
│  What approach sounds right to you?"                    │
└─────────────────────────────────────────────────────────┘
```

### Skill Invocation Pattern

```python
# In agent prompt (e.g., file-search-agent)

When you need deep code analysis:

1. Use Skill tool to invoke code-analysis:
   "Analyze src/navigation/ and find integration points for obstacle avoidance"

2. Receive structured JSON response with:
   - Architectural patterns
   - Existing classes and interfaces
   - Integration point suggestions
   - Related files

3. Interpret results and create teaching response:
   - Don't just report findings
   - Explain what the patterns mean
   - Guide student to understand architecture
   - Ask questions about design choices
   - Suggest exploration, not implementation

4. Use findings to create better context documentation
```

### Integration with Existing Commands

#### /create-project-plan Enhancement

```markdown
**Before** (without skills):
1. project-plan-orchestrator invokes file-search-agent
2. file-search-agent uses Glob/Grep to find files
3. file-search-agent reads files and makes basic notes
4. plan-generation-mentor reads notes, creates plan

**After** (with code-analysis skill):
1. project-plan-orchestrator invokes file-search-agent
2. file-search-agent uses Skill(code-analysis) for deep analysis
3. code-analysis returns:
   - Architectural patterns (MVC, Layered, etc.)
   - Integration points with reasoning
   - Dependency relationships
   - Complexity hotspots
4. file-search-agent interprets and documents findings
5. plan-generation-mentor creates plan with:
   - Specific files to modify
   - Patterns to follow
   - Integration points identified
   - Architecture-aware guidance
```

#### /continue-plan Enhancement

```markdown
**Before** (without skills):
1. learning-coordinator reads plan markdown
2. Manually parses to find current phase
3. Searches for next task
4. Updates plan by rewriting entire file

**After** (with learning-plan-manager skill):
1. learning-coordinator uses Skill(learning-plan-manager)
2. Skill returns structured data:
   - Current phase
   - Next task
   - Progress percentage
   - Recent journal entries
3. learning-coordinator formulates teaching response
4. Updates via skill (surgical updates, not full rewrite)
```

---

## Implementation Roadmap

### Week 1-2: learning-plan-manager Foundation

**Deliverables:**
- [ ] Data models (Pydantic schemas)
- [ ] Parser for learning plan markdown
- [ ] Basic CRUD operations
- [ ] Unit tests for parser
- [ ] Example usage with existing plans

**Testing:**
- Parse all existing learning plans
- Validate structure
- Test roundtrip (parse → modify → write → parse)

### Week 3-4: learning-plan-manager Complete

**Deliverables:**
- [ ] Writer (structured data → markdown)
- [ ] Validator
- [ ] Export functions (JSON, progress reports)
- [ ] Query operations (search, filters)
- [ ] Integration tests with continue-plan command
- [ ] Skill definition file

**Testing:**
- Test with learning-coordinator agent
- Verify continue-plan works with skill
- Test all CRUD operations

### Week 5-6: code-analysis Foundation

**Deliverables:**
- [ ] Data models for code analysis
- [ ] Python AST analyzer
- [ ] Basic complexity metrics
- [ ] Import dependency graph
- [ ] Unit tests for Python analyzer

**Testing:**
- Analyze src/claude_learning/ directory
- Validate AST parsing
- Test complexity calculations

### Week 7-8: code-analysis Complete

**Deliverables:**
- [ ] Pattern detection (Singleton, Factory, Strategy)
- [ ] Architectural pattern detection
- [ ] Integration point identification
- [ ] Code smell detection
- [ ] Skill definition file
- [ ] Integration with file-search-agent

**Testing:**
- Test on entire codebase
- Verify pattern detection accuracy
- Test integration point suggestions
- Integration test with create-project-plan

---

## Testing Strategy

### Unit Tests

```python
# tests/skills/test_learning_plan_manager.py

import pytest
from skills.learning_plan_manager import LearningPlanManager, TaskStatus

def test_parse_learning_plan():
    """Test parsing a learning plan markdown file"""
    manager = LearningPlanManager()
    plan = manager.load_plan("tests/fixtures/sample-learning-plan.md")

    assert plan.metadata.title == "Sample Learning Plan"
    assert len(plan.phases) == 3
    assert plan.get_current_phase().number == 1

def test_update_task_status():
    """Test updating task status"""
    manager = LearningPlanManager()
    plan = manager.load_plan("tests/fixtures/sample-learning-plan.md")

    task = plan.get_next_task()
    assert task.status == TaskStatus.NOT_STARTED

    plan = manager.update_task_status(plan, task.id, TaskStatus.COMPLETED)

    updated_task = next(t for phase in plan.phases for t in phase.tasks if t.id == task.id)
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.completed_at is not None

def test_calculate_progress():
    """Test progress calculation"""
    manager = LearningPlanManager()
    plan = manager.load_plan("tests/fixtures/sample-learning-plan.md")

    progress = plan.calculate_progress()

    assert "phases" in progress
    assert "tasks" in progress
    assert "overall_percentage" in progress
    assert 0 <= progress["overall_percentage"] <= 100

# tests/skills/test_code_analysis.py

import pytest
from skills.code_analysis import CodeAnalyzer, Language, DesignPattern

def test_analyze_python_file():
    """Test analyzing a Python file"""
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_file("src/claude_learning/agent_client.py")

    assert analysis.language == Language.PYTHON
    assert len(analysis.nodes) > 0
    assert len(analysis.imports) > 0

def test_calculate_complexity():
    """Test complexity calculation"""
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_file("tests/fixtures/complex_function.py")

    # Find the complex function
    func = next(n for n in analysis.nodes if n.name == "complex_function")

    assert func.complexity.cyclomatic_complexity > 1
    assert func.complexity.lines_of_code > 0

def test_detect_singleton_pattern():
    """Test singleton pattern detection"""
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_file("tests/fixtures/singleton_example.py")

    assert DesignPattern.SINGLETON in analysis.patterns

def test_analyze_codebase():
    """Test full codebase analysis"""
    analyzer = CodeAnalyzer()
    analysis = analyzer.analyze_codebase(
        "src/claude_learning/",
        max_files=10
    )

    assert len(analysis.files_analyzed) > 0
    assert len(analysis.entry_points) > 0
    assert analysis.dependency_graph is not None
```

### Integration Tests

```python
# tests/integration/test_skills_with_agents.py

import pytest
from skills.learning_plan_manager import LearningPlanManager
from skills.code_analysis import CodeAnalyzer

def test_continue_plan_with_skill():
    """Test that continue-plan command works with learning-plan-manager skill"""
    # Simulate agent invoking skill
    manager = LearningPlanManager()
    plan = manager.find_latest_plan()

    assert plan is not None

    current = plan.get_current_phase()
    next_task = plan.get_next_task()
    progress = plan.calculate_progress()

    # Agent should receive all this data
    assert current is not None
    assert "overall_percentage" in progress

def test_file_search_with_code_analysis():
    """Test that file-search-agent can use code-analysis skill"""
    analyzer = CodeAnalyzer()

    # Analyze codebase
    analysis = analyzer.analyze_codebase("src/")

    # Find integration points for a feature
    integration_points = analysis.suggest_integration_locations("new agent type")

    # Should find the agent factory or base class
    assert len(integration_points) > 0
```

### Manual Testing Checklist

**learning-plan-manager:**
- [ ] Can parse all existing learning plans without errors
- [ ] Can find current phase correctly
- [ ] Can update task status and save
- [ ] Progress calculation matches manual count
- [ ] Export to JSON works
- [ ] Progress report is readable and accurate

**code-analysis:**
- [ ] Can analyze entire src/ directory
- [ ] Detects known patterns in codebase
- [ ] Complexity metrics are reasonable
- [ ] Integration points make sense
- [ ] No false positives in pattern detection

---

## Success Criteria

### Phase 1 Complete When:

**learning-plan-manager:**
- ✅ Can parse all learning plan formats
- ✅ CRUD operations work reliably
- ✅ Integration with /continue-plan successful
- ✅ Export formats generate correctly
- ✅ 90%+ test coverage
- ✅ Documentation complete

**code-analysis:**
- ✅ Python analysis fully functional
- ✅ Pattern detection achieves 80%+ accuracy
- ✅ Integration points are useful
- ✅ Dependency graph builds correctly
- ✅ Integration with file-search-agent successful
- ✅ 85%+ test coverage
- ✅ Documentation complete

**Overall:**
- ✅ Both skills deployed and available via Skill tool
- ✅ Agents successfully use skills
- ✅ User-visible improvement in plan continuation
- ✅ User-visible improvement in project plan quality
- ✅ No regressions in existing functionality

---

## Next Steps After Phase 1

1. **Gather Usage Data**
   - Track skill invocations
   - Measure agent satisfaction (via outputs)
   - Collect user feedback

2. **Iterate Based on Feedback**
   - Refine pattern detection
   - Add missing functionality
   - Improve performance

3. **Phase 2 Skills**
   - learning-analytics (depends on learning-plan-manager)
   - interactive-diagram (can use code-analysis data)

4. **Documentation**
   - Create user guide for skills
   - Document best practices for agents using skills
   - Add examples to agent prompts

---

**Document End**
