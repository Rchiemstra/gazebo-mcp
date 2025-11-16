"""
Test Skill Discovery

Tests whether agents can effectively discover and select the right skills
for specific tasks based on metadata, descriptions, and documentation.

This implements Phase 2.2 of the Anthropic Best Practices Implementation Plan:
evaluating skill discoverability.
"""

import pytest
from pathlib import Path
import yaml
from typing import Dict, List, Any


class SkillMetadata:
    """Represents skill metadata for testing."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.name = None
        self.description = None
        self.category = None
        self.tags = []
        self.operations = []

        self._parse_skill_md()

    def _parse_skill_md(self):
        """Parse SKILL.md to extract metadata."""
        if not self.file_path.exists():
            return

        content = self.file_path.read_text()

        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    self.name = metadata.get('name')
                    self.description = metadata.get('description', '')
                    self.category = metadata.get('category')
                    self.tags = metadata.get('tags', [])
                except yaml.YAMLError:
                    pass

        # Extract operations from content
        lines = content.split('\n')
        in_operations = False
        for line in lines:
            if '## Operations' in line:
                in_operations = True
                continue
            if in_operations and line.startswith('- `'):
                # Extract operation name
                op_name = line.split('`')[1]
                self.operations.append(op_name)
            elif in_operations and line.startswith('##'):
                break


class SkillDiscoveryTester:
    """Tests for skill discovery functionality."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.skills = self._load_all_skills()

    def _load_all_skills(self) -> List[SkillMetadata]:
        """Load metadata for all skills."""
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('_'):
                skill_md = skill_dir / 'SKILL.md'
                if skill_md.exists():
                    skills.append(SkillMetadata(skill_md))

        return skills

    def find_by_keyword(self, keyword: str) -> List[SkillMetadata]:
        """Find skills by keyword in name/description/tags."""
        keyword_lower = keyword.lower()
        matches = []

        for skill in self.skills:
            if (keyword_lower in skill.name.lower() if skill.name else False or
                keyword_lower in skill.description.lower() if skill.description else False or
                any(keyword_lower in tag.lower() for tag in skill.tags)):
                matches.append(skill)

        return matches

    def find_by_category(self, category: str) -> List[SkillMetadata]:
        """Find skills by category."""
        return [s for s in self.skills if s.category == category]

    def find_by_operation(self, operation: str) -> List[SkillMetadata]:
        """Find skills that have a specific operation."""
        return [s for s in self.skills if operation in s.operations]


@pytest.fixture
def skills_dir():
    """Get the skills directory."""
    return Path(__file__).parent.parent / 'skills'


@pytest.fixture
def discovery_tester(skills_dir):
    """Create a SkillDiscoveryTester instance."""
    return SkillDiscoveryTester(skills_dir)


class TestSkillDiscovery:
    """Test cases for skill discovery."""

    def test_all_skills_have_metadata(self, discovery_tester):
        """Test that all skills have proper SKILL.md with metadata."""
        for skill in discovery_tester.skills:
            assert skill.name is not None, f"Skill at {skill.file_path} missing name"
            assert skill.description, f"Skill {skill.name} missing description"
            assert len(skill.description) > 20, f"Skill {skill.name} description too short"

    def test_discover_testing_skills(self, discovery_tester):
        """Test discovering skills related to testing."""
        results = discovery_tester.find_by_keyword('test')

        # Should find test_orchestrator at minimum
        skill_names = [s.name for s in results]
        assert 'test-orchestrator' in skill_names or 'test_orchestrator' in skill_names, \
            "Cannot discover test orchestrator by keyword 'test'"

    def test_discover_code_analysis_skills(self, discovery_tester):
        """Test discovering skills for code analysis."""
        results = discovery_tester.find_by_keyword('analysis')

        # Should find code_analysis skill
        skill_names = [s.name for s in results]
        assert any('analysis' in name for name in skill_names), \
            "Cannot discover analysis skills by keyword"

    def test_discover_by_category_testing(self, discovery_tester):
        """Test discovering skills by testing category."""
        results = discovery_tester.find_by_category('testing')

        # Should find at least one testing skill
        assert len(results) > 0, "No skills found in testing category"

    def test_discover_by_category_infrastructure(self, discovery_tester):
        """Test discovering infrastructure skills."""
        results = discovery_tester.find_by_category('infrastructure')

        # skill_evaluator should be in this category
        skill_names = [s.name for s in results]
        assert 'skill-evaluator' in skill_names or 'skill_evaluator' in skill_names, \
            "Cannot discover skill evaluator in infrastructure category"

    def test_discover_refactoring_skills(self, discovery_tester):
        """Test discovering skills for refactoring."""
        results = discovery_tester.find_by_keyword('refactor')

        skill_names = [s.name for s in results]
        assert any('refactor' in name for name in skill_names), \
            "Cannot discover refactoring skills"

    def test_discover_git_skills(self, discovery_tester):
        """Test discovering git-related skills."""
        results = discovery_tester.find_by_keyword('git')

        skill_names = [s.name for s in results]
        assert len(results) > 0, "Cannot discover git-related skills"

    def test_discover_learning_skills(self, discovery_tester):
        """Test discovering learning/teaching skills."""
        results = discovery_tester.find_by_keyword('learning')

        assert len(results) > 0, "Cannot discover learning-related skills"

    def test_all_skills_have_operations(self, discovery_tester):
        """Test that all skills document their operations."""
        skills_without_ops = []

        for skill in discovery_tester.skills:
            # Skip if it's a placeholder or not fully implemented
            if not (skill.file_path.parent / 'operations.py').exists():
                continue

            if not skill.operations:
                skills_without_ops.append(skill.name)

        assert len(skills_without_ops) == 0, \
            f"Skills missing operations documentation: {skills_without_ops}"

    def test_skill_descriptions_are_specific(self, discovery_tester):
        """Test that skill descriptions are specific and informative."""
        for skill in discovery_tester.skills:
            desc = skill.description

            # Check for vague descriptions
            vague_terms = ['helps with', 'provides functionality', 'utility for']
            has_vague = any(term in desc.lower() for term in vague_terms)

            # Descriptions should be specific about what they do
            assert len(desc) > 40 or not has_vague, \
                f"Skill {skill.name} has vague description: {desc}"

    def test_skills_have_appropriate_tags(self, discovery_tester):
        """Test that skills have relevant tags for discovery."""
        for skill in discovery_tester.skills:
            # Skip if no operations.py (not fully implemented)
            if not (skill.file_path.parent / 'operations.py').exists():
                continue

            assert len(skill.tags) > 0, \
                f"Skill {skill.name} has no tags for discovery"

            # Tags should be lowercase for consistency
            for tag in skill.tags:
                assert tag == tag.lower(), \
                    f"Skill {skill.name} has non-lowercase tag: {tag}"

    def test_categories_are_valid(self, discovery_tester):
        """Test that skills use valid category values."""
        valid_categories = {
            'testing', 'analysis', 'refactoring', 'documentation',
            'git', 'learning', 'infrastructure', 'code-quality',
            'dependencies', 'verification', 'evaluation'
        }

        for skill in discovery_tester.skills:
            if skill.category:
                assert skill.category in valid_categories, \
                    f"Skill {skill.name} has invalid category: {skill.category}"


class TestSkillSearchScenarios:
    """Real-world skill discovery scenarios."""

    def test_scenario_need_to_write_tests(self, discovery_tester):
        """Agent needs to write tests for code."""
        # Keywords an agent might use
        results = (
            discovery_tester.find_by_keyword('test') +
            discovery_tester.find_by_category('testing')
        )

        # Remove duplicates
        unique_skills = {s.name for s in results}

        assert len(unique_skills) > 0, \
            "Cannot discover test-writing skills"

    def test_scenario_need_to_analyze_code_quality(self, discovery_tester):
        """Agent needs to analyze code quality."""
        results = (
            discovery_tester.find_by_keyword('analysis') +
            discovery_tester.find_by_keyword('quality') +
            discovery_tester.find_by_category('analysis')
        )

        unique_skills = {s.name for s in results}
        assert len(unique_skills) > 0, \
            "Cannot discover code analysis skills"

    def test_scenario_need_to_manage_dependencies(self, discovery_tester):
        """Agent needs to manage project dependencies."""
        results = discovery_tester.find_by_keyword('dependency')

        assert len(results) > 0, \
            "Cannot discover dependency management skills"

    def test_scenario_need_to_create_documentation(self, discovery_tester):
        """Agent needs to generate documentation."""
        results = (
            discovery_tester.find_by_keyword('doc') +
            discovery_tester.find_by_category('documentation')
        )

        unique_skills = {s.name for s in results}
        assert len(unique_skills) > 0, \
            "Cannot discover documentation generation skills"

    def test_scenario_need_to_refactor_code(self, discovery_tester):
        """Agent needs to refactor complex code."""
        results = (
            discovery_tester.find_by_keyword('refactor') +
            discovery_tester.find_by_category('refactoring')
        )

        unique_skills = {s.name for s in results}
        assert len(unique_skills) > 0, \
            "Cannot discover refactoring skills"

    def test_scenario_need_to_review_pr(self, discovery_tester):
        """Agent needs to review a pull request."""
        results = (
            discovery_tester.find_by_keyword('review') +
            discovery_tester.find_by_keyword('pr') +
            discovery_tester.find_by_keyword('pull request')
        )

        unique_skills = {s.name for s in results}
        assert len(unique_skills) > 0, \
            "Cannot discover PR review skills"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
