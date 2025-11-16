"""
Interactive Diagram Skill

Generates visual learning aids including architecture diagrams, progress charts,
learning flowcharts, and dependency graphs using Mermaid syntax.

This skill enhances learning through visualization by creating:
- Architecture diagrams from code-analysis data
- Progress charts from learning-analytics data
- Learning journey flowcharts
- Gantt charts for timelines
- Concept maps and flowcharts
"""

from .models import (
    # Enums
    DiagramType,

    # Style
    DiagramStyle,

    # Diagrams
    Diagram,
    DiagramCollection,
)

from .generator import DiagramGenerator

from .mermaid_builder import (
    MermaidBuilder,
    sanitize_mermaid_label,
    generate_node_id,
    get_color_for_status,
)

__all__ = [
    # Enums
    "DiagramType",

    # Style
    "DiagramStyle",

    # Diagrams
    "Diagram",
    "DiagramCollection",

    # Generator
    "DiagramGenerator",

    # Builder utilities
    "MermaidBuilder",
    "sanitize_mermaid_label",
    "generate_node_id",
    "get_color_for_status",
]

__version__ = "1.0.0"
