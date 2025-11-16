"""
Mermaid diagram builder utilities.

Provides helper classes and functions for generating Mermaid syntax.
"""

from typing import List, Optional, Dict
import re


# ============================================================================
# Helper Functions
# ============================================================================

def sanitize_mermaid_label(text: str) -> str:
    """
    Escape special characters for Mermaid.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text safe for Mermaid
    """
    # Replace problematic characters
    text = text.replace('"', "'")
    text = text.replace('\n', '<br/>')
    text = text.replace('[', '(')
    text = text.replace(']', ')')
    return text


def generate_node_id(name: str) -> str:
    """
    Generate safe node ID from name.

    Args:
        name: Original name

    Returns:
        Safe node ID (alphanumeric + underscores)
    """
    # Remove special characters, keep alphanumeric and underscores
    node_id = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove consecutive underscores
    node_id = re.sub(r'_+', '_', node_id)
    # Remove leading/trailing underscores
    node_id = node_id.strip('_')
    # Ensure starts with letter
    if node_id and node_id[0].isdigit():
        node_id = 'n_' + node_id
    return node_id or 'node'


def get_color_for_status(status: str) -> str:
    """
    Map status to color.

    Args:
        status: Status string (completed, in_progress, not_started, etc.)

    Returns:
        Hex color code
    """
    status_colors = {
        'completed': '#90EE90',      # Light green
        'done': '#90EE90',
        'passed': '#90EE90',
        'in_progress': '#87CEEB',    # Sky blue
        'active': '#87CEEB',
        'current': '#87CEEB',
        'not_started': '#D3D3D3',    # Light gray
        'pending': '#D3D3D3',
        'failed': '#FFB6C1',         # Light red
        'error': '#FFB6C1',
        'blocked': '#FFD700',        # Gold
        'warning': '#FFD700',
        'excellent': '#00FF00',      # Bright green
        'good': '#90EE90',
        'needs_attention': '#FFA500', # Orange
        'struggling': '#FF6347',     # Tomato red
    }

    return status_colors.get(status.lower(), '#FFFFFF')


# ============================================================================
# Mermaid Builder
# ============================================================================

class MermaidBuilder:
    """
    Helper class for building Mermaid diagram syntax.

    Provides methods to incrementally build Mermaid diagrams.
    """

    def __init__(self, diagram_type: str = "flowchart"):
        """
        Initialize builder.

        Args:
            diagram_type: Type of Mermaid diagram (flowchart, classDiagram, etc.)
        """
        self.diagram_type = diagram_type
        self.lines: List[str] = []
        self.styles: List[str] = []
        self.subgraphs: List[str] = []

    def add_header(self, direction: str = "TD"):
        """
        Add diagram header.

        Args:
            direction: Diagram orientation (TD, LR, BT, RL)
        """
        if self.diagram_type == "flowchart":
            self.lines.append(f"flowchart {direction}")
        elif self.diagram_type == "graph":
            self.lines.append(f"graph {direction}")
        elif self.diagram_type == "classDiagram":
            self.lines.append("classDiagram")
        elif self.diagram_type == "gantt":
            self.lines.append("gantt")
        elif self.diagram_type == "pie":
            self.lines.append("pie")
        else:
            self.lines.append(self.diagram_type)

    def add_node(self, node_id: str, label: str, shape: str = "rect"):
        """
        Add a node to the diagram.

        Args:
            node_id: Unique node identifier
            label: Node label text
            shape: Node shape (rect, round, stadium, circle, diamond, etc.)
        """
        label = sanitize_mermaid_label(label)

        shape_syntax = {
            'rect': f'{node_id}[{label}]',
            'round': f'{node_id}({label})',
            'stadium': f'{node_id}([{label}])',
            'circle': f'{node_id}(({label}))',
            'diamond': f'{node_id}{{{label}}}',
            'hexagon': f'{node_id}{{{{{label}}}}}',
            'asymmetric': f'{node_id}>{label}]',
        }

        syntax = shape_syntax.get(shape, f'{node_id}[{label}]')
        self.lines.append(f"    {syntax}")

    def add_edge(self, from_id: str, to_id: str, label: str = "", style: str = "solid"):
        """
        Add an edge between nodes.

        Args:
            from_id: Source node ID
            to_id: Target node ID
            label: Edge label (optional)
            style: Edge style (solid, dotted, thick)
        """
        label = sanitize_mermaid_label(label) if label else ""

        if style == "dotted":
            arrow = "-.." if label else "-..-"
        elif style == "thick":
            arrow = "==>" if label else "==="
        else:
            arrow = "-->" if label else "---"

        if label:
            self.lines.append(f"    {from_id} {arrow}|{label}| {to_id}")
        else:
            self.lines.append(f"    {from_id} {arrow} {to_id}")

    def add_class_definition(self, class_name: str, methods: List[str], attributes: List[str] = None):
        """
        Add a class definition (for class diagrams).

        Args:
            class_name: Name of the class
            methods: List of method signatures
            attributes: List of attributes (optional)
        """
        self.lines.append(f"    class {class_name} {{")

        if attributes:
            for attr in attributes:
                self.lines.append(f"        {sanitize_mermaid_label(attr)}")

        if methods:
            for method in methods:
                self.lines.append(f"        {sanitize_mermaid_label(method)}")

        self.lines.append("    }")

    def add_relationship(self, from_class: str, to_class: str, rel_type: str = "association"):
        """
        Add a relationship between classes (for class diagrams).

        Args:
            from_class: Source class
            to_class: Target class
            rel_type: Relationship type (inheritance, composition, aggregation, association)
        """
        rel_syntax = {
            'inheritance': '<|--',
            'composition': '*--',
            'aggregation': 'o--',
            'association': '-->'
        }

        syntax = rel_syntax.get(rel_type, '-->')
        self.lines.append(f"    {from_class} {syntax} {to_class}")

    def add_style(self, node_id: str, fill: str, stroke: str = "", text_color: str = ""):
        """
        Add styling to a node.

        Args:
            node_id: Node ID to style
            fill: Fill color (hex)
            stroke: Stroke color (hex, optional)
            text_color: Text color (hex, optional)
        """
        style_parts = [f"fill:{fill}"]

        if stroke:
            style_parts.append(f"stroke:{stroke}")

        if text_color:
            style_parts.append(f"color:{text_color}")

        style_str = ",".join(style_parts)
        self.styles.append(f"    style {node_id} {style_str}")

    def add_subgraph(self, title: str, content: List[str]):
        """
        Add a subgraph (group of nodes).

        Args:
            title: Subgraph title
            content: List of node IDs in subgraph
        """
        subgraph_id = generate_node_id(title)
        self.lines.append(f"    subgraph {subgraph_id}[{sanitize_mermaid_label(title)}]")

        for item in content:
            self.lines.append(f"        {item}")

        self.lines.append("    end")

    def add_gantt_config(self, date_format: str = "YYYY-MM-DD"):
        """
        Add Gantt chart configuration.

        Args:
            date_format: Date format string
        """
        self.lines.append(f"    dateFormat {date_format}")

    def add_gantt_section(self, section_name: str):
        """
        Add a Gantt chart section.

        Args:
            section_name: Name of the section
        """
        self.lines.append(f"    section {section_name}")

    def add_gantt_task(self, task_name: str, status: str, start_date: str, duration: str):
        """
        Add a Gantt chart task.

        Args:
            task_name: Name of the task
            status: Task status (done, active, crit, or empty)
            start_date: Start date
            duration: Duration (e.g., "3d", "1w")
        """
        status_str = f":{status}, " if status else ":"
        self.lines.append(f"    {task_name} {status_str}{start_date}, {duration}")

    def add_pie_slice(self, label: str, value: float):
        """
        Add a pie chart slice.

        Args:
            label: Slice label
            value: Slice value
        """
        label = sanitize_mermaid_label(label)
        self.lines.append(f'    "{label}" : {value}')

    def add_pie_title(self, title: str):
        """
        Add pie chart title.

        Args:
            title: Chart title
        """
        self.lines.append(f"    title {sanitize_mermaid_label(title)}")

    def build(self) -> str:
        """
        Build and return complete Mermaid code.

        Returns:
            Complete Mermaid diagram syntax
        """
        result = []

        # Add diagram lines
        result.extend(self.lines)

        # Add styles
        if self.styles:
            result.append("")
            result.extend(self.styles)

        return "\n".join(result)
