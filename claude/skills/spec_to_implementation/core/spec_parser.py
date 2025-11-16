"""
Specification Parser

Parses feature specifications from various formats.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any


class SpecFormat(Enum):
    """Specification format types."""
    MARKDOWN = "markdown"
    YAML = "yaml"
    JSON = "json"
    PLAIN_TEXT = "plain_text"


class RequirementType(Enum):
    """Type of requirement."""
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"


@dataclass
class Requirement:
    """A single requirement."""
    id: str
    type: RequirementType
    description: str
    priority: str  # 'high', 'medium', 'low'
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class Specification:
    """Parsed specification."""
    title: str
    description: str
    requirements: List[Requirement]
    constraints: List[str]
    dependencies: List[str]
    inputs: List[Dict[str, str]]
    outputs: List[Dict[str, str]]
    examples: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class SpecificationParser:
    """Parses specifications from various formats."""

    def parse_file(self, file_path: str) -> Specification:
        """
        Parse specification from file.

        Args:
            file_path: Path to specification file

        Returns:
            Parsed specification
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Specification file not found: {file_path}")

        # Determine format
        content = path.read_text(encoding='utf-8')
        format_type = self._detect_format(file_path, content)

        # Parse based on format
        if format_type == SpecFormat.MARKDOWN:
            return self._parse_markdown(content)
        elif format_type == SpecFormat.PLAIN_TEXT:
            return self._parse_plain_text(content)
        else:
            # Default to markdown
            return self._parse_markdown(content)

    def _detect_format(self, file_path: str, content: str) -> SpecFormat:
        """Detect specification format."""
        path = Path(file_path)

        if path.suffix.lower() in ['.md', '.markdown']:
            return SpecFormat.MARKDOWN
        elif path.suffix.lower() in ['.yml', '.yaml']:
            return SpecFormat.YAML
        elif path.suffix.lower() == '.json':
            return SpecFormat.JSON
        else:
            # Check content
            if content.strip().startswith('#'):
                return SpecFormat.MARKDOWN
            return SpecFormat.PLAIN_TEXT

    def _parse_markdown(self, content: str) -> Specification:
        """Parse markdown specification."""
        lines = content.splitlines()

        title = ""
        description = ""
        requirements = []
        constraints = []
        dependencies = []
        inputs = []
        outputs = []
        examples = []

        current_section = None
        current_content = []

        for line in lines:
            # Check for headers
            if line.startswith('# '):
                # Main title
                if not title:
                    title = line[2:].strip()
                continue

            elif line.startswith('## '):
                # Process previous section
                if current_section and current_content:
                    self._process_section(
                        current_section,
                        current_content,
                        requirements,
                        constraints,
                        dependencies,
                        inputs,
                        outputs,
                        examples
                    )

                # Start new section
                current_section = line[3:].strip().lower()
                current_content = []
                continue

            # Add to current section
            if current_section:
                current_content.append(line)
            elif not description and line.strip():
                # First paragraph after title is description
                description += line.strip() + " "

        # Process last section
        if current_section and current_content:
            self._process_section(
                current_section,
                current_content,
                requirements,
                constraints,
                dependencies,
                inputs,
                outputs,
                examples
            )

        # Extract requirements from description if none found
        if not requirements and description:
            requirements = self._extract_implicit_requirements(description)

        return Specification(
            title=title or "Untitled Specification",
            description=description.strip(),
            requirements=requirements,
            constraints=constraints,
            dependencies=dependencies,
            inputs=inputs,
            outputs=outputs,
            examples=examples
        )

    def _process_section(
        self,
        section: str,
        content: List[str],
        requirements: List[Requirement],
        constraints: List[str],
        dependencies: List[str],
        inputs: List[Dict[str, str]],
        outputs: List[Dict[str, str]],
        examples: List[str]
    ):
        """Process a section of the specification."""
        text = '\n'.join(content)

        if 'requirement' in section or 'feature' in section:
            # Extract requirements
            reqs = self._extract_requirements(text)
            requirements.extend(reqs)

        elif 'constraint' in section or 'limitation' in section:
            # Extract constraints
            items = self._extract_list_items(text)
            constraints.extend(items)

        elif 'dependenc' in section:
            # Extract dependencies
            items = self._extract_list_items(text)
            dependencies.extend(items)

        elif 'input' in section:
            # Extract inputs
            items = self._extract_parameters(text)
            inputs.extend(items)

        elif 'output' in section or 'return' in section:
            # Extract outputs
            items = self._extract_parameters(text)
            outputs.extend(items)

        elif 'example' in section or 'usage' in section:
            # Extract examples
            examples.append(text)

    def _extract_requirements(self, text: str) -> List[Requirement]:
        """Extract requirements from text."""
        requirements = []

        # Look for numbered or bulleted lists
        lines = text.splitlines()
        req_id = 1

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check if line is a requirement
            if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                # Remove bullet/number
                desc = re.sub(r'^[-*•]\s*', '', line)
                desc = re.sub(r'^\d+\.\s*', '', desc)

                if desc:
                    # Determine priority
                    priority = 'medium'
                    if any(word in desc.lower() for word in ['must', 'critical', 'required']):
                        priority = 'high'
                    elif any(word in desc.lower() for word in ['should', 'nice', 'optional']):
                        priority = 'low'

                    # Determine type
                    req_type = RequirementType.FUNCTIONAL
                    if any(word in desc.lower() for word in ['performance', 'scalability', 'security']):
                        req_type = RequirementType.NON_FUNCTIONAL

                    requirements.append(Requirement(
                        id=f"REQ-{req_id:03d}",
                        type=req_type,
                        description=desc,
                        priority=priority
                    ))
                    req_id += 1

        return requirements

    def _extract_implicit_requirements(self, description: str) -> List[Requirement]:
        """Extract implicit requirements from description."""
        requirements = []

        # Look for action verbs
        sentences = description.split('.')
        req_id = 1

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check for requirement indicators
            if any(verb in sentence.lower() for verb in [
                'should', 'must', 'need', 'require', 'allow', 'enable',
                'provide', 'support', 'implement', 'create'
            ]):
                requirements.append(Requirement(
                    id=f"REQ-{req_id:03d}",
                    type=RequirementType.FUNCTIONAL,
                    description=sentence,
                    priority='medium'
                ))
                req_id += 1

        return requirements

    def _extract_list_items(self, text: str) -> List[str]:
        """Extract items from bulleted/numbered list."""
        items = []
        lines = text.splitlines()

        for line in lines:
            line = line.strip()

            if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                # Remove bullet/number
                item = re.sub(r'^[-*•]\s*', '', line)
                item = re.sub(r'^\d+\.\s*', '', item)

                if item:
                    items.append(item)

        return items

    def _extract_parameters(self, text: str) -> List[Dict[str, str]]:
        """Extract parameters from text."""
        parameters = []
        lines = text.splitlines()

        for line in lines:
            line = line.strip()

            # Look for parameter patterns: name: type - description
            match = re.match(r'^-?\s*`?(\w+)`?\s*(?:\(([^)]+)\))?\s*:?\s*-?\s*(.+)', line)
            if match:
                name, param_type, description = match.groups()
                parameters.append({
                    'name': name,
                    'type': param_type or 'any',
                    'description': description.strip()
                })

        return parameters

    def _parse_plain_text(self, content: str) -> Specification:
        """Parse plain text specification."""
        lines = content.splitlines()

        # Try to extract title (first non-empty line)
        title = ""
        description = ""

        for line in lines:
            line = line.strip()
            if line:
                if not title:
                    title = line
                else:
                    description += line + " "

        # Extract implicit requirements
        requirements = self._extract_implicit_requirements(content)

        return Specification(
            title=title or "Untitled Specification",
            description=description.strip(),
            requirements=requirements,
            constraints=[],
            dependencies=[],
            inputs=[],
            outputs=[],
            examples=[]
        )
