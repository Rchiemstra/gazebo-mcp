"""
Interactive Diagram Generator

Generates visual diagrams from skills data (code-analysis, learning-analytics, learning-plan-manager).
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from .models import Diagram, DiagramType, DiagramStyle, DiagramCollection
from .mermaid_builder import (
    MermaidBuilder,
    sanitize_mermaid_label,
    generate_node_id,
    get_color_for_status
)


class DiagramGenerator:
    """Generates visual diagrams from skill data"""

    def __init__(self):
        """Initialize generator"""
        pass

    # ========================================================================
    # CODE STRUCTURE DIAGRAMS
    # ========================================================================

    def generate_class_diagram(
        self,
        code_analysis,
        focus_files: Optional[List[str]] = None,
        max_classes: int = 10
    ) -> Diagram:
        """
        Generate class diagram from code analysis.

        Args:
            code_analysis: CodebaseAnalysis object from code-analysis skill
            focus_files: Optional list of files to focus on
            max_classes: Maximum number of classes to include

        Returns:
            Diagram with class diagram
        """
        builder = MermaidBuilder("classDiagram")
        builder.add_header()

        # Extract classes from code analysis
        classes_found = []

        for file_analysis in code_analysis.files[:max_classes]:
            for cls in file_analysis.classes:
                if focus_files and file_analysis.file_path not in focus_files:
                    continue

                class_name = cls.name

                # Add class with methods
                methods = [f"+{m.name}()" for m in cls.methods[:5]]  # Limit methods
                builder.add_class_definition(class_name, methods)

                classes_found.append(class_name)

        # Add relationships if detectable
        # (Simplified: just show that classes exist, relationships are complex)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.CLASS_DIAGRAM,
            title="Class Architecture Diagram",
            description=f"Class structure showing {len(classes_found)} classes",
            mermaid_code=mermaid_code,
            metadata={
                "classes_count": len(classes_found),
                "source": "code-analysis"
            }
        )

    def generate_dependency_graph(
        self,
        code_analysis,
        max_files: int = 15
    ) -> Diagram:
        """
        Generate dependency graph from code analysis.

        Args:
            code_analysis: CodebaseAnalysis object
            max_files: Maximum number of files to show

        Returns:
            Diagram with dependency graph
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("LR")

        # Build dependency graph from imports
        file_nodes = {}

        # First, create nodes for files
        for i, file_analysis in enumerate(code_analysis.files[:max_files]):
            file_path = file_analysis.file_path
            # Get just the filename
            filename = file_path.split('/')[-1]
            node_id = generate_node_id(filename)

            file_nodes[file_path] = node_id
            builder.add_node(node_id, filename, "rect")

        # Then add edges for dependencies (imports)
        edges_added = set()
        for file_analysis in code_analysis.files[:max_files]:
            from_id = file_nodes.get(file_analysis.file_path)
            if not from_id:
                continue

            for import_item in file_analysis.imports[:5]:  # Limit imports
                # Try to find the imported file
                import_name = import_item.get('module', '')

                # Simplified: just show that there's a dependency
                # (Real implementation would resolve imports to files)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.DEPENDENCY_GRAPH,
            title="Code Dependency Graph",
            description=f"File dependencies for {len(file_nodes)} files",
            mermaid_code=mermaid_code,
            metadata={
                "files_count": len(file_nodes),
                "source": "code-analysis"
            }
        )

    # ========================================================================
    # LEARNING PROGRESS DIAGRAMS
    # ========================================================================

    def generate_progress_chart(
        self,
        analytics
    ) -> Diagram:
        """
        Generate progress pie chart from learning analytics.

        Args:
            analytics: LearningAnalytics object from learning-analytics skill

        Returns:
            Diagram with progress chart
        """
        builder = MermaidBuilder("pie")
        builder.add_header()

        # Add title
        builder.add_pie_title("Learning Progress")

        # Get task counts
        completed = analytics.velocity_metrics.tasks_completed_total
        total_tasks = completed

        # Try to get total from metadata if available
        if hasattr(analytics, 'metadata'):
            total_tasks = analytics.metadata.get('total_tasks', completed)

        in_progress = len([s for s in analytics.struggle_areas if s.severity in ['minor', 'moderate']])
        not_started = max(0, total_tasks - completed - in_progress)

        # Add slices
        if completed > 0:
            builder.add_pie_slice("Completed", completed)
        if in_progress > 0:
            builder.add_pie_slice("In Progress", in_progress)
        if not_started > 0:
            builder.add_pie_slice("Not Started", not_started)

        # If no data, show placeholder
        if completed == 0 and in_progress == 0 and not_started == 0:
            builder.add_pie_slice("No Data Yet", 1)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.PROGRESS_CHART,
            title="Your Learning Progress",
            description=f"{completed} tasks completed out of {total_tasks}",
            mermaid_code=mermaid_code,
            metadata={
                "completed": completed,
                "in_progress": in_progress,
                "not_started": not_started,
                "source": "learning-analytics"
            }
        )

    def generate_learning_journey(
        self,
        plan,
        analytics=None
    ) -> Diagram:
        """
        Generate learning journey flowchart.

        Args:
            plan: LearningPlan object from learning-plan-manager
            analytics: Optional LearningAnalytics for status coloring

        Returns:
            Diagram with learning journey flowchart
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("TD")

        # Start node
        builder.add_node("Start", "Start Learning", "stadium")

        previous_node = "Start"

        # Add phases
        for phase in plan.phases[:4]:  # Limit to 4 phases
            phase_id = f"P{phase.number}"
            phase_label = f"Phase {phase.number}: {phase.title}"

            builder.add_node(phase_id, phase_label, "rect")
            builder.add_edge(previous_node, phase_id)

            # Add checkpoint if exists
            if phase.checkpoints:
                checkpoint = phase.checkpoints[0]
                checkpoint_id = f"C{phase.number}"
                checkpoint_label = f"Checkpoint {phase.number}"

                builder.add_node(checkpoint_id, checkpoint_label, "diamond")
                builder.add_edge(phase_id, checkpoint_id)

                # Color based on status if analytics available
                if hasattr(checkpoint, 'status'):
                    color = get_color_for_status(checkpoint.status.value if hasattr(checkpoint.status, 'value') else str(checkpoint.status))
                    builder.add_style(checkpoint_id, color)

                previous_node = checkpoint_id
            else:
                previous_node = phase_id

            # Color phase based on completion
            if hasattr(phase, 'completed_at') and phase.completed_at:
                builder.add_style(phase_id, get_color_for_status('completed'))
            elif hasattr(phase, 'started_at') and phase.started_at:
                builder.add_style(phase_id, get_color_for_status('in_progress'))
            else:
                builder.add_style(phase_id, get_color_for_status('not_started'))

        # End node
        builder.add_node("End", "Complete!", "stadium")
        builder.add_edge(previous_node, "End")
        builder.add_style("End", get_color_for_status('excellent'))

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.LEARNING_JOURNEY,
            title="Your Learning Journey",
            description=f"Visual roadmap through {len(plan.phases)} phases",
            mermaid_code=mermaid_code,
            metadata={
                "phases_count": len(plan.phases),
                "source": "learning-plan-manager"
            }
        )

    def generate_velocity_trend(
        self,
        analytics,
        show_weeks: int = 4
    ) -> Diagram:
        """
        Generate velocity trend visualization.

        Args:
            analytics: LearningAnalytics object
            show_weeks: Number of weeks to show

        Returns:
            Diagram with velocity trend
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("LR")

        # Add velocity data
        # (Simplified: show overall and recent)
        overall_velocity = analytics.velocity_metrics.overall_velocity
        recent_velocity = analytics.velocity_metrics.recent_velocity
        trend = analytics.velocity_metrics.velocity_trend

        # Create trend visualization
        builder.add_node("Overall", f"Overall<br/>{overall_velocity} tasks/week", "rect")
        builder.add_node("Recent", f"Recent<br/>{recent_velocity} tasks/week", "rect")

        builder.add_edge("Overall", "Recent", trend.capitalize())

        # Color based on trend
        if trend == "increasing":
            builder.add_style("Recent", get_color_for_status('excellent'))
        elif trend == "decreasing":
            builder.add_style("Recent", get_color_for_status('warning'))
        else:
            builder.add_style("Recent", get_color_for_status('good'))

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.VELOCITY_TREND,
            title="Learning Velocity Trend",
            description=f"Your learning pace is {trend}",
            mermaid_code=mermaid_code,
            metadata={
                "overall_velocity": overall_velocity,
                "recent_velocity": recent_velocity,
                "trend": trend,
                "source": "learning-analytics"
            }
        )

    # ========================================================================
    # PLANNING DIAGRAMS
    # ========================================================================

    def generate_gantt_chart(
        self,
        plan,
        analytics=None
    ) -> Diagram:
        """
        Generate Gantt chart for learning plan timeline.

        Args:
            plan: LearningPlan object
            analytics: Optional analytics for actual vs estimated

        Returns:
            Diagram with Gantt chart
        """
        builder = MermaidBuilder("gantt")
        builder.add_header()

        # Add config
        builder.add_gantt_config("YYYY-MM-DD")

        # Add title
        builder.lines.append(f"    title {sanitize_mermaid_label(plan.metadata.title)}")

        # Estimate start date
        start_date = datetime.now()
        if hasattr(plan.metadata, 'created') and plan.metadata.created:
            try:
                start_date = datetime.fromisoformat(plan.metadata.created.replace('Z', '+00:00'))
            except:
                pass

        current_date = start_date

        # Add phases as sections
        for phase in plan.phases[:4]:  # Limit to 4 phases
            builder.add_gantt_section(f"Phase {phase.number}: {phase.title}")

            # Add tasks
            for task in phase.tasks[:5]:  # Limit tasks per phase
                # Determine status
                status = ""
                if hasattr(task, 'status'):
                    task_status = task.status.value if hasattr(task.status, 'value') else str(task.status)
                    if task_status == "COMPLETED":
                        status = "done"
                    elif task_status == "IN_PROGRESS":
                        status = "active"

                # Estimate duration (default 3 days)
                duration = "3d"

                # Format date
                date_str = current_date.strftime("%Y-%m-%d")

                builder.add_gantt_task(task.title, status, date_str, duration)

                # Move to next task
                current_date += timedelta(days=3)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.GANTT_CHART,
            title="Learning Plan Timeline",
            description="Timeline view of your learning journey",
            mermaid_code=mermaid_code,
            metadata={
                "phases_count": len(plan.phases),
                "source": "learning-plan-manager"
            }
        )

    def generate_milestone_map(
        self,
        plan
    ) -> Diagram:
        """
        Generate milestone roadmap.

        Args:
            plan: LearningPlan object

        Returns:
            Diagram with milestone map
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("LR")

        # Extract checkpoints as milestones
        builder.add_node("Start", "Start", "circle")
        previous_node = "Start"

        milestone_count = 0

        for phase in plan.phases:
            # Add phase as milestone
            phase_id = f"M{phase.number}"
            builder.add_node(phase_id, f"Phase {phase.number}", "rect")
            builder.add_edge(previous_node, phase_id)

            # Color based on completion
            if hasattr(phase, 'completed_at') and phase.completed_at:
                builder.add_style(phase_id, get_color_for_status('completed'))
            elif hasattr(phase, 'started_at') and phase.started_at:
                builder.add_style(phase_id, get_color_for_status('in_progress'))

            previous_node = phase_id
            milestone_count += 1

            # Add checkpoint
            if phase.checkpoints:
                checkpoint = phase.checkpoints[0]
                cp_id = f"CP{phase.number}"
                builder.add_node(cp_id, f"Checkpoint", "diamond")
                builder.add_edge(phase_id, cp_id)

                # Color checkpoint
                if hasattr(checkpoint, 'status'):
                    color = get_color_for_status(checkpoint.status.value if hasattr(checkpoint.status, 'value') else str(checkpoint.status))
                    builder.add_style(cp_id, color)

                previous_node = cp_id
                milestone_count += 1

        # End
        builder.add_node("End", "Complete!", "circle")
        builder.add_edge(previous_node, "End")
        builder.add_style("End", get_color_for_status('excellent'))

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.MILESTONE_MAP,
            title="Learning Milestones",
            description=f"Key milestones and checkpoints ({milestone_count} total)",
            mermaid_code=mermaid_code,
            metadata={
                "milestones_count": milestone_count,
                "source": "learning-plan-manager"
            }
        )

    # ========================================================================
    # GENERAL DIAGRAMS
    # ========================================================================

    def generate_flowchart(
        self,
        steps: List[Dict[str, Any]],
        title: str = "Process Flowchart",
        description: str = None
    ) -> Diagram:
        """
        Generate flowchart from steps.

        Args:
            steps: List of step dictionaries with 'id', 'label', 'type', 'next'
            title: Diagram title
            description: Diagram description

        Returns:
            Diagram with flowchart
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("TD")

        # Add nodes
        for step in steps:
            step_id = step.get('id', generate_node_id(step.get('label', 'step')))
            label = step.get('label', 'Step')
            step_type = step.get('type', 'process')

            # Map type to shape
            shape_map = {
                'start': 'stadium',
                'end': 'stadium',
                'process': 'rect',
                'decision': 'diamond',
                'data': 'asymmetric'
            }
            shape = shape_map.get(step_type, 'rect')

            builder.add_node(step_id, label, shape)

            # Color special types
            if step_type == 'start':
                builder.add_style(step_id, get_color_for_status('excellent'))
            elif step_type == 'end':
                builder.add_style(step_id, get_color_for_status('completed'))

        # Add edges
        for step in steps:
            step_id = step.get('id', generate_node_id(step.get('label', 'step')))
            next_steps = step.get('next', [])

            if isinstance(next_steps, str):
                next_steps = [next_steps]

            for next_step in next_steps:
                if isinstance(next_step, dict):
                    next_id = next_step.get('id')
                    edge_label = next_step.get('label', '')
                else:
                    next_id = next_step
                    edge_label = ''

                builder.add_edge(step_id, next_id, edge_label)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.FLOWCHART,
            title=title,
            description=description or f"Flowchart with {len(steps)} steps",
            mermaid_code=mermaid_code,
            metadata={
                "steps_count": len(steps)
            }
        )

    def generate_concept_map(
        self,
        concepts: List[str],
        relationships: List[tuple],
        title: str = "Concept Map",
        description: str = None
    ) -> Diagram:
        """
        Generate concept relationship map.

        Args:
            concepts: List of concept names
            relationships: List of (from_concept, to_concept, relationship_label) tuples
            title: Diagram title
            description: Diagram description

        Returns:
            Diagram with concept map
        """
        builder = MermaidBuilder("flowchart")
        builder.add_header("TD")

        # Add concept nodes
        concept_ids = {}
        for concept in concepts:
            concept_id = generate_node_id(concept)
            concept_ids[concept] = concept_id
            builder.add_node(concept_id, concept, "round")

        # Add relationships
        for from_concept, to_concept, label in relationships:
            from_id = concept_ids.get(from_concept)
            to_id = concept_ids.get(to_concept)

            if from_id and to_id:
                builder.add_edge(from_id, to_id, label)

        mermaid_code = builder.build()

        return Diagram(
            diagram_type=DiagramType.CONCEPT_MAP,
            title=title,
            description=description or f"Concept map with {len(concepts)} concepts",
            mermaid_code=mermaid_code,
            metadata={
                "concepts_count": len(concepts),
                "relationships_count": len(relationships)
            }
        )

    # ========================================================================
    # COLLECTION GENERATORS
    # ========================================================================

    def generate_complete_progress_report(
        self,
        plan,
        analytics
    ) -> DiagramCollection:
        """
        Generate complete progress report with multiple diagrams.

        Args:
            plan: LearningPlan object
            analytics: LearningAnalytics object

        Returns:
            DiagramCollection with multiple progress diagrams
        """
        collection = DiagramCollection(
            title="Complete Learning Progress Report",
            description="Visual overview of your learning journey",
            created_at=datetime.now().isoformat()
        )

        # Add progress chart
        collection.add_diagram(self.generate_progress_chart(analytics))

        # Add learning journey
        collection.add_diagram(self.generate_learning_journey(plan, analytics))

        # Add velocity trend
        collection.add_diagram(self.generate_velocity_trend(analytics))

        # Add Gantt chart
        collection.add_diagram(self.generate_gantt_chart(plan, analytics))

        return collection
