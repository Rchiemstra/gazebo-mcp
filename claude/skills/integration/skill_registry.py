"""
Skill Registry

Discovers and catalogs available skills.
"""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set


@dataclass
class SkillMetadata:
    """Metadata about a skill."""
    name: str
    description: str
    version: str = "1.0.0"
    author: Optional[str] = None
    tools: List[str] = field(default_factory=list)
    activation: str = "manual"  # manual or automatic
    dependencies: List[str] = field(default_factory=list)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    path: Optional[Path] = None
    operations: Dict[str, str] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of skill validation."""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class SkillRegistry:
    """Registry for discovering and managing skills."""

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self._skills: Dict[str, SkillMetadata] = {}
        self._discovered = False

    def discover_skills(self) -> List[SkillMetadata]:
        """
        Discover all skills in the skills directory.

        Returns:
            List of SkillMetadata for discovered skills
        """
        if self._discovered:
            return list(self._skills.values())

        self._skills.clear()

        # Find all skill.md files
        skill_files = list(self.skills_dir.glob("*/skill.md"))

        for skill_file in skill_files:
            try:
                metadata = self._parse_skill_file(skill_file)
                if metadata:
                    self._skills[metadata.name] = metadata
            except Exception as e:
                print(f"Warning: Failed to parse {skill_file}: {e}")

        self._discovered = True
        return list(self._skills.values())

    def get_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """
        Get metadata for a specific skill.

        Args:
            skill_name: Name of the skill

        Returns:
            SkillMetadata or None if not found
        """
        if not self._discovered:
            self.discover_skills()

        return self._skills.get(skill_name)

    def list_skills(self, category: Optional[str] = None, tag: Optional[str] = None) -> List[str]:
        """
        List available skills, optionally filtered.

        Args:
            category: Filter by category
            tag: Filter by tag

        Returns:
            List of skill names
        """
        if not self._discovered:
            self.discover_skills()

        skills = self._skills.values()

        if category:
            skills = [s for s in skills if s.category == category]

        if tag:
            skills = [s for s in skills if tag in s.tags]

        return [s.name for s in skills]

    def validate_skill(self, skill_name: str) -> ValidationResult:
        """
        Validate a skill's definition and dependencies.

        Args:
            skill_name: Name of the skill to validate

        Returns:
            ValidationResult with errors and warnings
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return ValidationResult(
                valid=False,
                errors=[f"Skill '{skill_name}' not found"]
            )

        errors = []
        warnings = []

        # Check for required fields
        if not skill.name:
            errors.append("Skill name is required")
        if not skill.description:
            errors.append("Skill description is required")

        # Check dependencies
        for dep in skill.dependencies:
            if dep not in self._skills:
                errors.append(f"Dependency '{dep}' not found")

        # Check if skill directory exists
        if skill.path and not skill.path.exists():
            errors.append(f"Skill directory does not exist: {skill.path}")

        # Warnings
        if not skill.tools:
            warnings.append("No tools specified")

        if not skill.version or skill.version == "1.0.0":
            warnings.append("Consider specifying explicit version")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def get_skill_dependencies(self, skill_name: str) -> Set[str]:
        """
        Get all dependencies for a skill (including transitive).

        Args:
            skill_name: Name of the skill

        Returns:
            Set of dependency skill names
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return set()

        dependencies = set()
        to_process = list(skill.dependencies)

        while to_process:
            dep_name = to_process.pop(0)
            if dep_name in dependencies:
                continue

            dependencies.add(dep_name)

            dep_skill = self.get_skill(dep_name)
            if dep_skill:
                to_process.extend(dep_skill.dependencies)

        return dependencies

    def _parse_skill_file(self, skill_file: Path) -> Optional[SkillMetadata]:
        """Parse a skill.md file and extract metadata."""
        with open(skill_file, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return None

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError:
            return None

        # Extract operations from frontmatter first, then from content
        operations = {}

        # Get operations from YAML frontmatter if present
        if 'operations' in frontmatter and isinstance(frontmatter['operations'], dict):
            operations = frontmatter['operations']
        else:
            # Fall back to extracting from content
            operations = self._extract_operations(content)

        return SkillMetadata(
            name=frontmatter.get('name', ''),
            description=frontmatter.get('description', ''),
            version=frontmatter.get('version', '1.0.0'),
            author=frontmatter.get('author'),
            tools=frontmatter.get('tools', []),
            activation=frontmatter.get('activation', 'manual'),
            dependencies=frontmatter.get('dependencies', []),
            category=frontmatter.get('category'),
            tags=frontmatter.get('tags', []),
            path=skill_file.parent,
            operations=operations
        )

    def _extract_operations(self, content: str) -> Dict[str, str]:
        """Extract operation names and descriptions from skill documentation."""
        operations = {}

        # Find operation sections (## Operations or ### operation_name)
        operation_pattern = r'###\s+(\w+)\s*\n\s*(.+?)(?=\n###|\n##|$)'
        matches = re.finditer(operation_pattern, content, re.DOTALL)

        for match in matches:
            op_name = match.group(1)
            op_desc = match.group(2).strip().split('\n')[0]  # First line only
            operations[op_name] = op_desc

        return operations

    def get_skills_by_category(self) -> Dict[str, List[str]]:
        """
        Group skills by category.

        Returns:
            Dict mapping category to list of skill names
        """
        if not self._discovered:
            self.discover_skills()

        by_category = {}
        for skill in self._skills.values():
            category = skill.category or "uncategorized"
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill.name)

        return by_category

    def search_skills(self, query: str) -> List[SkillMetadata]:
        """
        Search skills by name, description, or tags.

        Args:
            query: Search query

        Returns:
            List of matching skills
        """
        if not self._discovered:
            self.discover_skills()

        query = query.lower()
        results = []

        for skill in self._skills.values():
            if (query in skill.name.lower() or
                query in skill.description.lower() or
                any(query in tag.lower() for tag in skill.tags)):
                results.append(skill)

        return results
