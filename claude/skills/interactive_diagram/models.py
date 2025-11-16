"""
Data models for interactive-diagram skill.

Defines Pydantic models for:
- Diagram types and styles
- Diagram output with Mermaid code
- Diagram collections
"""

from typing import List, Dict, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# Enums
# ============================================================================

class DiagramType(str, Enum):
    """Types of diagrams that can be generated"""

    # Code structure diagrams
    CLASS_DIAGRAM = "class_diagram"
    DEPENDENCY_GRAPH = "dependency_graph"
    CALL_FLOW = "call_flow"

    # Learning progress diagrams
    PROGRESS_CHART = "progress_chart"
    LEARNING_JOURNEY = "learning_journey"
    VELOCITY_TREND = "velocity_trend"

    # Planning diagrams
    GANTT_CHART = "gantt_chart"
    MILESTONE_MAP = "milestone_map"

    # General diagrams
    FLOWCHART = "flowchart"
    CONCEPT_MAP = "concept_map"


# ============================================================================
# Style Models
# ============================================================================

class DiagramStyle(BaseModel):
    """Styling options for diagrams"""

    theme: str = Field(
        default="default",
        description="Mermaid theme: default, forest, dark, neutral"
    )

    show_labels: bool = Field(
        default=True,
        description="Show labels on nodes/edges"
    )

    show_legend: bool = Field(
        default=True,
        description="Include legend explaining colors/symbols"
    )

    color_scheme: Dict[str, str] = Field(
        default_factory=dict,
        description="Custom color mappings (status -> color)"
    )

    orientation: str = Field(
        default="TD",
        description="Diagram direction: TD (top-down), LR (left-right), etc."
    )


# ============================================================================
# Diagram Models
# ============================================================================

class Diagram(BaseModel):
    """Generated diagram with Mermaid code"""

    diagram_type: DiagramType
    title: str
    description: Optional[str] = None

    mermaid_code: str = Field(
        description="Mermaid diagram syntax"
    )

    style: DiagramStyle = Field(
        default_factory=DiagramStyle
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (data source, generation time, etc.)"
    )

    interactive_elements: List[str] = Field(
        default_factory=list,
        description="List of clickable/interactive elements"
    )

    def to_markdown(self) -> str:
        """
        Convert diagram to markdown format.

        Returns:
            Markdown string with Mermaid code block
        """
        md = f"## {self.title}\n\n"
        if self.description:
            md += f"{self.description}\n\n"
        md += "```mermaid\n"
        md += self.mermaid_code
        md += "\n```\n"
        return md

    def to_html(self) -> str:
        """
        Convert diagram to HTML format.

        Returns:
            HTML string with mermaid div
        """
        html = f"<h2>{self.title}</h2>\n"
        if self.description:
            html += f"<p>{self.description}</p>\n"
        html += f'<div class="mermaid">\n{self.mermaid_code}\n</div>\n'
        return html

    def save_markdown(self, filepath: str):
        """Save diagram as markdown file"""
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())


class DiagramCollection(BaseModel):
    """Collection of related diagrams"""

    title: str
    description: Optional[str] = None
    diagrams: List[Diagram] = Field(default_factory=list)

    created_at: Optional[str] = None

    def add_diagram(self, diagram: Diagram):
        """Add a diagram to the collection"""
        self.diagrams.append(diagram)

    def to_markdown(self) -> str:
        """
        Export entire collection as markdown.

        Returns:
            Markdown string with all diagrams
        """
        md = f"# {self.title}\n\n"
        if self.description:
            md += f"{self.description}\n\n"

        if self.created_at:
            md += f"*Generated: {self.created_at}*\n\n"

        md += "---\n\n"

        for i, diagram in enumerate(self.diagrams, 1):
            md += diagram.to_markdown()
            if i < len(self.diagrams):
                md += "\n---\n\n"

        return md

    def save_markdown(self, filepath: str):
        """Save collection as markdown file"""
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())
