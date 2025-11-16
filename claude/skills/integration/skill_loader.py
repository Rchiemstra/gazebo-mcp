"""
Skill Loader

Dynamically loads and initializes skills.
"""

import importlib
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Optional, Any
from .skill_registry import SkillRegistry, SkillMetadata


@dataclass
class SkillInstance:
    """An instance of a loaded skill."""
    name: str
    metadata: SkillMetadata
    module: Any
    operations: Dict[str, callable]


class SkillLoader:
    """Loads skills dynamically."""

    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self._loaded_skills: Dict[str, SkillInstance] = {}

    def load_skill(self, skill_name: str) -> SkillInstance:
        """
        Load a skill by name.

        Args:
            skill_name: Name of the skill to load

        Returns:
            SkillInstance

        Raises:
            ValueError: If skill not found or cannot be loaded
        """
        # Check if already loaded
        if skill_name in self._loaded_skills:
            return self._loaded_skills[skill_name]

        # Get metadata
        metadata = self.registry.get_skill(skill_name)
        if not metadata:
            raise ValueError(f"Skill '{skill_name}' not found in registry")

        # Load dependencies first
        for dep in metadata.dependencies:
            if dep not in self._loaded_skills:
                self.load_skill(dep)

        # Load the skill module
        try:
            module = self._load_module(metadata)
            operations = self._discover_operations(module, metadata)

            instance = SkillInstance(
                name=skill_name,
                metadata=metadata,
                module=module,
                operations=operations
            )

            self._loaded_skills[skill_name] = instance
            return instance

        except Exception as e:
            raise ValueError(f"Failed to load skill '{skill_name}': {e}")

    def reload_skill(self, skill_name: str) -> SkillInstance:
        """
        Reload a skill (useful for development).

        Args:
            skill_name: Name of the skill to reload

        Returns:
            SkillInstance
        """
        if skill_name in self._loaded_skills:
            self.unload_skill(skill_name)

        return self.load_skill(skill_name)

    def unload_skill(self, skill_name: str) -> None:
        """
        Unload a skill.

        Args:
            skill_name: Name of the skill to unload
        """
        if skill_name in self._loaded_skills:
            instance = self._loaded_skills[skill_name]

            # Remove from sys.modules if present
            module_name = instance.module.__name__
            if module_name in sys.modules:
                del sys.modules[module_name]

            del self._loaded_skills[skill_name]

    def get_loaded_skills(self) -> list[str]:
        """
        Get list of currently loaded skills.

        Returns:
            List of skill names
        """
        return list(self._loaded_skills.keys())

    def get_skill_instance(self, skill_name: str) -> Optional[SkillInstance]:
        """
        Get a loaded skill instance.

        Args:
            skill_name: Name of the skill

        Returns:
            SkillInstance or None if not loaded
        """
        return self._loaded_skills.get(skill_name)

    def _load_module(self, metadata: SkillMetadata) -> Any:
        """Load the Python module for a skill."""
        if not metadata.path:
            raise ValueError(f"No path specified for skill '{metadata.name}'")

        # Add skill directory to path if not already there
        skill_parent = str(metadata.path.parent)
        if skill_parent not in sys.path:
            sys.path.insert(0, skill_parent)

        # Try to import the skill's __init__.py
        skill_dir_name = metadata.path.name
        try:
            module = importlib.import_module(skill_dir_name)
            return module
        except ImportError as e:
            # If no __init__.py, create a minimal module namespace
            print(f"Warning: Could not import {skill_dir_name} as module: {e}")
            print(f"Creating namespace for skill directory")

            # Create a simple namespace object
            from types import SimpleNamespace
            module = SimpleNamespace()
            module.__name__ = skill_dir_name
            module.__path__ = str(metadata.path)

            # Try to load core modules
            core_path = metadata.path / "core"
            if core_path.exists():
                # Import core modules
                sys.path.insert(0, str(metadata.path))
                try:
                    core = importlib.import_module("core")
                    module.core = core
                except ImportError:
                    pass

            return module

    def _discover_operations(self, module: Any, metadata: SkillMetadata) -> Dict[str, callable]:
        """
        Discover callable operations in a skill module.

        Args:
            module: Loaded module
            metadata: Skill metadata

        Returns:
            Dict mapping operation names to callables
        """
        operations = {}

        # Look for explicitly defined operations in metadata
        for op_name in metadata.operations.keys():
            # Try to find the operation function/class
            if hasattr(module, op_name):
                operations[op_name] = getattr(module, op_name)

        # Also look for common entry points
        common_entry_points = [
            'analyze', 'generate', 'execute', 'process', 'create',
            'get', 'list', 'update', 'delete'
        ]

        for entry_point in common_entry_points:
            if hasattr(module, entry_point) and entry_point not in operations:
                operations[entry_point] = getattr(module, entry_point)

        return operations
