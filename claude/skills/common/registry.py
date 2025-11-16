"""
Skill Registry - Central discovery and validation for Claude Code skills

Provides mechanisms for agents to discover available skills, validate dependencies,
and retrieve skill metadata at runtime.

Created: 2025-11-10
Version: 0.1.0
"""

import os
import importlib
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SkillInfo:
    """
    Information about a discovered skill.

    Attributes:
        name (str): Skill name (directory name)
        path (Path): Full path to skill directory
        version (str): Skill version from __version__
        operations (List[str]): List of available operations
        has_skill_md (bool): Whether SKILL.md exists
        has_tests (bool): Whether tests directory exists
        dependencies (List[str]): Other skills this depends on
    """
    name: str
    path: Path
    version: str
    operations: List[str]
    has_skill_md: bool
    has_tests: bool
    dependencies: List[str]


class SkillRegistry:
    """
    Central registry for skill discovery and validation.

    This class provides static methods for discovering available skills,
    validating dependencies, and retrieving skill metadata. It enables
    agents to dynamically check skill availability and handle missing
    optional skills gracefully.

    Example:
        # Discover all skills
        skills = SkillRegistry.discover_skills()
        print(f"Found {len(skills)} skills")

        # Validate dependencies before using
        required = ['code_analysis', 'refactor_assistant']
        if SkillRegistry.validate_dependencies(required):
            # Safe to proceed
            pass

        # Get skill API info
        api = SkillRegistry.get_skill_api('code_analysis')
        print(f"Operations: {api['operations']}")
    """

    _SKILLS_DIR = Path(__file__).parent.parent  # skills/ directory
    _CACHE: Optional[Dict[str, SkillInfo]] = None

    @classmethod
    def discover_skills(cls, force_refresh: bool = False) -> Dict[str, SkillInfo]:
        """
        Scan skills directory and return information about available skills.

        Args:
            force_refresh (bool): If True, bypass cache and rescan directory

        Returns:
            Dict[str, SkillInfo]: Mapping of skill names to SkillInfo objects

        Example:
            skills = SkillRegistry.discover_skills()
            for name, info in skills.items():
                print(f"{name}: {len(info.operations)} operations")
        """
        # Return cached result unless force refresh
        if cls._CACHE is not None and not force_refresh:
            return cls._CACHE

        skills = {}
        logger.info(f"Discovering skills in: {cls._SKILLS_DIR}")

        for item in cls._SKILLS_DIR.iterdir():
            # Skip non-directories and special directories
            if not item.is_dir():
                continue
            if item.name.startswith(('_', '.')):
                continue
            if item.name in ('common', 'integration', '__pycache__'):
                continue

            # Try to load skill info
            try:
                skill_info = cls._load_skill_info(item)
                if skill_info:
                    skills[item.name] = skill_info
                    logger.debug(f"Discovered skill: {item.name}")
            except Exception as e:
                logger.warning(f"Failed to load skill {item.name}: {e}")
                continue

        cls._CACHE = skills
        logger.info(f"Discovered {len(skills)} skills")
        return skills

    @classmethod
    def _load_skill_info(cls, skill_path: Path) -> Optional[SkillInfo]:
        """
        Load information about a skill from its directory.

        Args:
            skill_path (Path): Path to skill directory

        Returns:
            Optional[SkillInfo]: SkillInfo object or None if invalid
        """
        skill_name = skill_path.name

        # Check for __init__.py (required for valid skill)
        init_file = skill_path / "__init__.py"
        if not init_file.exists():
            logger.debug(f"Skipping {skill_name}: no __init__.py")
            return None

        # Try to import the skill to get version and operations
        version = "unknown"
        operations = []

        try:
            # Import the skill module
            module_name = f"skills.{skill_name}"
            module = importlib.import_module(module_name)

            # Get version
            if hasattr(module, '__version__'):
                version = module.__version__

            # Get exported operations (from __all__ or dir())
            if hasattr(module, '__all__'):
                all_exports = module.__all__
            else:
                all_exports = [name for name in dir(module) if not name.startswith('_')]

            # Filter to callable operations (exclude classes like OperationResult)
            for name in all_exports:
                attr = getattr(module, name, None)
                if callable(attr) and not inspect.isclass(attr):
                    # Exclude common utility classes
                    if name not in ('OperationResult', 'ErrorCodes'):
                        operations.append(name)

        except ImportError as e:
            logger.debug(f"Could not import {skill_name}: {e}")
            # Still create SkillInfo but with limited data
            pass
        except Exception as e:
            logger.warning(f"Error loading {skill_name}: {e}")
            return None

        # Check for SKILL.md
        has_skill_md = (skill_path / "SKILL.md").exists() or (skill_path / "skill.md").exists()

        # Check for tests
        has_tests = (skill_path / "tests").exists() and (skill_path / "tests").is_dir()

        # TODO: Parse dependencies from SKILL.md frontmatter or requirements
        dependencies = []

        return SkillInfo(
            name=skill_name,
            path=skill_path,
            version=version,
            operations=operations,
            has_skill_md=has_skill_md,
            has_tests=has_tests,
            dependencies=dependencies
        )

    @classmethod
    def validate_dependencies(cls, required_skills: List[str]) -> Tuple[bool, List[str]]:
        """
        Check if required skills are available.

        Args:
            required_skills (List[str]): List of skill names needed

        Returns:
            Tuple[bool, List[str]]: (all_available, list_of_missing)

        Example:
            valid, missing = SkillRegistry.validate_dependencies([
                'code_analysis',
                'refactor_assistant'
            ])

            if not valid:
                print(f"Missing skills: {missing}")
                raise MissingSkillError(f"Required skills not available: {missing}")
        """
        available_skills = cls.discover_skills()
        missing = []

        for skill_name in required_skills:
            if skill_name not in available_skills:
                missing.append(skill_name)
                logger.warning(f"Required skill not found: {skill_name}")

        all_available = len(missing) == 0
        return all_available, missing

    @classmethod
    def get_skill_api(cls, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get API documentation for a skill.

        Args:
            skill_name (str): Name of the skill

        Returns:
            Optional[Dict[str, Any]]: Skill API information or None if not found

        Returns dictionary with:
            - name: Skill name
            - version: Skill version
            - operations: List of available operations
            - operation_docs: Dict mapping operation names to docstrings
            - path: Path to skill directory
            - has_skill_md: Whether SKILL.md exists
            - has_tests: Whether tests exist

        Example:
            api = SkillRegistry.get_skill_api('code_analysis')
            if api:
                print(f"Code Analysis v{api['version']}")
                print(f"Operations: {', '.join(api['operations'])}")
                for op, doc in api['operation_docs'].items():
                    print(f"  {op}: {doc}")
        """
        skills = cls.discover_skills()

        if skill_name not in skills:
            logger.warning(f"Skill not found: {skill_name}")
            return None

        skill_info = skills[skill_name]

        # Try to get operation docstrings
        operation_docs = {}
        try:
            module_name = f"skills.{skill_name}"
            module = importlib.import_module(module_name)

            for op_name in skill_info.operations:
                func = getattr(module, op_name, None)
                if func and callable(func):
                    doc = inspect.getdoc(func)
                    if doc:
                        # Get first line of docstring as summary
                        summary = doc.split('\n')[0]
                        operation_docs[op_name] = summary
                    else:
                        operation_docs[op_name] = "No documentation available"

        except Exception as e:
            logger.debug(f"Could not load operation docs for {skill_name}: {e}")

        return {
            'name': skill_info.name,
            'version': skill_info.version,
            'operations': skill_info.operations,
            'operation_docs': operation_docs,
            'path': str(skill_info.path),
            'has_skill_md': skill_info.has_skill_md,
            'has_tests': skill_info.has_tests,
            'dependencies': skill_info.dependencies
        }

    @classmethod
    def list_skills(cls, category: Optional[str] = None) -> List[str]:
        """
        Get list of available skill names.

        Args:
            category (Optional[str]): Filter by category (if implemented)

        Returns:
            List[str]: List of skill names

        Example:
            all_skills = SkillRegistry.list_skills()
            print(f"Available: {', '.join(all_skills)}")
        """
        skills = cls.discover_skills()
        # TODO: Implement category filtering from SKILL.md metadata
        return sorted(skills.keys())

    @classmethod
    def get_skill_operations(cls, skill_name: str) -> List[str]:
        """
        Get list of operations provided by a skill.

        Args:
            skill_name (str): Name of the skill

        Returns:
            List[str]: List of operation names, empty if skill not found

        Example:
            ops = SkillRegistry.get_skill_operations('code_analysis')
            print(f"Available operations: {ops}")
        """
        skills = cls.discover_skills()
        if skill_name in skills:
            return skills[skill_name].operations
        return []

    @classmethod
    def skill_exists(cls, skill_name: str) -> bool:
        """
        Check if a skill exists.

        Args:
            skill_name (str): Name of the skill

        Returns:
            bool: True if skill exists

        Example:
            if SkillRegistry.skill_exists('code_analysis'):
                from skills.code_analysis import analyze_file
        """
        skills = cls.discover_skills()
        return skill_name in skills

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear the skill discovery cache.

        Use this if skills are added/removed at runtime.

        Example:
            # After creating a new skill
            SkillRegistry.clear_cache()
            skills = SkillRegistry.discover_skills(force_refresh=True)
        """
        cls._CACHE = None
        logger.info("Skill registry cache cleared")


class MissingSkillError(Exception):
    """
    Raised when a required skill is not available.

    Attributes:
        message (str): Error message
        missing_skills (List[str]): List of missing skill names
    """

    def __init__(self, message: str, missing_skills: Optional[List[str]] = None):
        self.message = message
        self.missing_skills = missing_skills or []
        super().__init__(self.message)

    def __str__(self):
        if self.missing_skills:
            skills_str = ", ".join(self.missing_skills)
            return f"{self.message}\nMissing skills: {skills_str}"
        return self.message


# Convenience function for agents
def require_skills(skill_names: List[str]) -> None:
    """
    Validate required skills are available, raise error if not.

    Args:
        skill_names (List[str]): List of required skill names

    Raises:
        MissingSkillError: If any required skills are missing

    Example:
        # At the start of an agent
        try:
            require_skills(['code_analysis', 'refactor_assistant'])
        except MissingSkillError as e:
            logger.error(f"Cannot proceed: {e}")
            raise
    """
    valid, missing = SkillRegistry.validate_dependencies(skill_names)
    if not valid:
        raise MissingSkillError(
            f"Required skills not available: {', '.join(missing)}",
            missing_skills=missing
        )


# Export public API
__all__ = [
    'SkillRegistry',
    'SkillInfo',
    'MissingSkillError',
    'require_skills'
]
