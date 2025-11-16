#!/usr/bin/env python3
"""
Unified Validation Script for Skills and Agents

This script validates all skills and agents in the project, providing
comprehensive reports and appropriate exit codes for CI/CD integration.

Usage:
    python scripts/validate-all.py [OPTIONS]

Options:
    --skills-only    Validate skills only
    --agents-only    Validate agents only
    --json          Output results in JSON format
    --verbose       Verbose output with detailed information
    --help          Show this help message

Exit Codes:
    0: All validations passed
    1: Validation errors found
    2: Warnings only (no errors)

Author: Claude Code Team
Created: 2025-11-10
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import existing validation modules
try:
    from skills.integration.skill_registry import SkillRegistry
except ImportError:
    SkillRegistry = None

import re
import yaml


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str  # 'error' or 'warning'
    message: str
    location: str = ""


@dataclass
class ValidationResult:
    """Represents validation result for a single item."""
    name: str
    type: str  # 'skill' or 'agent'
    passed: bool
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue]
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SkillValidator:
    """Validates skills using SkillRegistry and additional checks."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        if SkillRegistry:
            try:
                self.registry = SkillRegistry(str(skills_dir))
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize SkillRegistry: {e}")
                self.registry = None
        else:
            self.registry = None

    def validate_all(self) -> List[ValidationResult]:
        """
        Validate all skills.

        Returns:
            List of ValidationResult objects
        """
        results = []

        if not self.skills_dir.exists():
            return results

        # Get all skill directories
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

        # Directories to skip (not skills, but infrastructure/utilities)
        skip_dirs = {"integration", "common", "execution"}

        for skill_dir in skill_dirs:
            if skill_dir.name in skip_dirs:
                continue  # Skip infrastructure/utility directories

            result = self.validate_skill(skill_dir)
            results.append(result)

        return results

    def validate_skill(self, skill_dir: Path) -> ValidationResult:
        """
        Validate a single skill.

        Args:
            skill_dir: Path to skill directory

        Returns:
            ValidationResult
        """
        skill_name = skill_dir.name
        errors = []
        warnings = []
        metadata = {}

        # Check required files
        skill_md = skill_dir / "skill.md"
        operations_py = skill_dir / "operations.py"
        init_py = skill_dir / "__init__.py"

        if not skill_md.exists():
            errors.append(ValidationIssue(
                severity="error",
                message="Missing required file: skill.md",
                location=str(skill_dir)
            ))
        else:
            # Validate skill.md
            skill_md_issues = self._validate_skill_md(skill_md)
            errors.extend([i for i in skill_md_issues if i.severity == "error"])
            warnings.extend([i for i in skill_md_issues if i.severity == "warning"])

            # Extract metadata
            try:
                with open(skill_md, 'r') as f:
                    content = f.read()
                    if content.startswith('---'):
                        yaml_end = content.find('---', 3)
                        if yaml_end != -1:
                            yaml_content = content[3:yaml_end]
                            metadata = yaml.safe_load(yaml_content) or {}
            except Exception as e:
                errors.append(ValidationIssue(
                    severity="error",
                    message=f"Failed to parse skill.md frontmatter: {e}",
                    location=str(skill_md)
                ))

        if not operations_py.exists():
            errors.append(ValidationIssue(
                severity="error",
                message="Missing required file: operations.py",
                location=str(skill_dir)
            ))
        else:
            # Validate operations.py
            ops_issues = self._validate_operations_py(operations_py)
            errors.extend([i for i in ops_issues if i.severity == "error"])
            warnings.extend([i for i in ops_issues if i.severity == "warning"])

        if not init_py.exists():
            errors.append(ValidationIssue(
                severity="error",
                message="Missing required file: __init__.py",
                location=str(skill_dir)
            ))

        # Check recommended files
        readme_md = skill_dir / "README.md"
        if not readme_md.exists():
            warnings.append(ValidationIssue(
                severity="warning",
                message="Missing recommended file: README.md",
                location=str(skill_dir)
            ))

        demo_py = skill_dir / "demo.py"
        if not demo_py.exists():
            warnings.append(ValidationIssue(
                severity="warning",
                message="Missing recommended file: demo.py",
                location=str(skill_dir)
            ))

        tests_dir = skill_dir / "tests"
        if not tests_dir.exists():
            warnings.append(ValidationIssue(
                severity="warning",
                message="Missing recommended directory: tests/",
                location=str(skill_dir)
            ))

        # Use SkillRegistry validation if available
        if self.registry:
            try:
                # Use frontmatter name if available, otherwise fall back to directory name
                registry_skill_name = metadata.get('name', skill_name) if metadata else skill_name
                registry_result = self.registry.validate_skill(registry_skill_name)
                if hasattr(registry_result, 'errors') and registry_result.errors:
                    for error in registry_result.errors:
                        errors.append(ValidationIssue(
                            severity="error",
                            message=error,
                            location=skill_name
                        ))
                if hasattr(registry_result, 'warnings') and registry_result.warnings:
                    for warning in registry_result.warnings:
                        warnings.append(ValidationIssue(
                            severity="warning",
                            message=warning,
                            location=skill_name
                        ))
            except Exception as e:
                errors.append(ValidationIssue(
                    severity="error",
                    message=f"SkillRegistry validation failed: {e}",
                    location=skill_name
                ))

        return ValidationResult(
            name=skill_name,
            type="skill",
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _validate_skill_md(self, skill_md: Path) -> List[ValidationIssue]:
        """Validate skill.md file."""
        issues = []

        try:
            with open(skill_md, 'r') as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith('---'):
                issues.append(ValidationIssue(
                    severity="error",
                    message="skill.md must start with YAML frontmatter (---)",
                    location=str(skill_md)
                ))
                return issues

            # Extract and parse YAML
            yaml_end = content.find('---', 3)
            if yaml_end == -1:
                issues.append(ValidationIssue(
                    severity="error",
                    message="skill.md YAML frontmatter not properly closed (missing closing ---)",
                    location=str(skill_md)
                ))
                return issues

            yaml_content = content[3:yaml_end]
            try:
                metadata = yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                issues.append(ValidationIssue(
                    severity="error",
                    message=f"Invalid YAML in skill.md: {e}",
                    location=str(skill_md)
                ))
                return issues

            # Check required fields
            required_fields = ['name', 'version', 'description', 'operations']
            for field in required_fields:
                if field not in metadata:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Missing required field in skill.md: {field}",
                        location=str(skill_md)
                    ))

            # Validate name format (kebab-case)
            if 'name' in metadata:
                name = metadata['name']
                if not re.match(r'^[a-z][a-z0-9-]*$', name):
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Invalid name format: '{name}'. Must be kebab-case.",
                        location=str(skill_md)
                    ))

            # Validate version format (semver)
            if 'version' in metadata:
                version = metadata['version']
                if not re.match(r'^\d+\.\d+\.\d+', str(version)):
                    issues.append(ValidationIssue(
                        severity="warning",
                        message=f"Version '{version}' should follow semantic versioning (X.Y.Z)",
                        location=str(skill_md)
                    ))

            # Validate operations
            if 'operations' in metadata:
                operations = metadata['operations']
                if not isinstance(operations, dict):
                    issues.append(ValidationIssue(
                        severity="error",
                        message="'operations' field must be a dictionary",
                        location=str(skill_md)
                    ))
                elif len(operations) == 0:
                    issues.append(ValidationIssue(
                        severity="warning",
                        message="No operations defined in skill.md",
                        location=str(skill_md)
                    ))

        except Exception as e:
            issues.append(ValidationIssue(
                severity="error",
                message=f"Failed to validate skill.md: {e}",
                location=str(skill_md)
            ))

        return issues

    def _validate_operations_py(self, operations_py: Path) -> List[ValidationIssue]:
        """Validate operations.py file."""
        issues = []

        try:
            with open(operations_py, 'r') as f:
                content = f.read()

            # Check for OperationResult
            if 'class OperationResult' not in content and 'from .operations import OperationResult' not in content:
                issues.append(ValidationIssue(
                    severity="error",
                    message="operations.py must define or import OperationResult dataclass",
                    location=str(operations_py)
                ))

            # Check for time tracking
            if 'import time' not in content:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="operations.py should import 'time' for duration tracking",
                    location=str(operations_py)
                ))

            # Check for error handling
            if 'try:' not in content or 'except' not in content:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="operations.py should include try-except blocks for error handling",
                    location=str(operations_py)
                ))

            # Check for standard error codes
            if 'error_code' not in content.lower():
                issues.append(ValidationIssue(
                    severity="warning",
                    message="operations.py should use standardized error codes",
                    location=str(operations_py)
                ))

        except Exception as e:
            issues.append(ValidationIssue(
                severity="error",
                message=f"Failed to validate operations.py: {e}",
                location=str(operations_py)
            ))

        return issues


class AgentValidator:
    """Validates agents."""

    VALID_TOOLS = [
        "Read", "Write", "Edit", "Glob", "Grep", "Bash",
        "Python", "Task", "WebFetch", "WebSearch", "NotebookEdit"
    ]

    VALID_MODELS = ["sonnet", "opus", "haiku"]
    VALID_ACTIVATIONS = ["proactive", "manual", "always"]

    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir

    def validate_all(self) -> List[ValidationResult]:
        """
        Validate all agents.

        Returns:
            List of ValidationResult objects
        """
        results = []

        if not self.agents_dir.exists():
            return results

        # Get all agent files
        agent_files = list(self.agents_dir.glob("*.md"))

        for agent_file in agent_files:
            result = self.validate_agent(agent_file)
            results.append(result)

        return results

    def validate_agent(self, agent_file: Path) -> ValidationResult:
        """
        Validate a single agent.

        Args:
            agent_file: Path to agent markdown file

        Returns:
            ValidationResult
        """
        agent_name = agent_file.stem
        errors = []
        warnings = []
        metadata = {}

        try:
            with open(agent_file, 'r') as f:
                content = f.read()

            # Check for YAML frontmatter
            if not content.startswith('---'):
                errors.append(ValidationIssue(
                    severity="error",
                    message="Agent file must start with YAML frontmatter (---)",
                    location=str(agent_file)
                ))
                return ValidationResult(
                    name=agent_name,
                    type="agent",
                    passed=False,
                    errors=errors,
                    warnings=warnings,
                    metadata=metadata
                )

            # Extract and parse YAML
            yaml_end = content.find('---', 3)
            if yaml_end == -1:
                errors.append(ValidationIssue(
                    severity="error",
                    message="YAML frontmatter not properly closed (missing closing ---)",
                    location=str(agent_file)
                ))
                return ValidationResult(
                    name=agent_name,
                    type="agent",
                    passed=False,
                    errors=errors,
                    warnings=warnings,
                    metadata=metadata
                )

            yaml_content = content[3:yaml_end]
            try:
                metadata = yaml.safe_load(yaml_content) or {}
            except yaml.YAMLError as e:
                errors.append(ValidationIssue(
                    severity="error",
                    message=f"Invalid YAML: {e}",
                    location=str(agent_file)
                ))
                return ValidationResult(
                    name=agent_name,
                    type="agent",
                    passed=False,
                    errors=errors,
                    warnings=warnings,
                    metadata=metadata
                )

            # Check required fields
            required_fields = ['name', 'description', 'tools', 'model']
            for field in required_fields:
                if field not in metadata:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Missing required field: {field}",
                        location=str(agent_file)
                    ))

            # Validate name format (kebab-case)
            if 'name' in metadata:
                name = metadata['name']
                if not re.match(r'^[a-z][a-z0-9-]*$', name):
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Invalid name format: '{name}'. Must be kebab-case.",
                        location=str(agent_file)
                    ))
                if name != agent_name:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Name in frontmatter ('{name}') doesn't match filename ('{agent_name}')",
                        location=str(agent_file)
                    ))

            # Validate description length
            if 'description' in metadata:
                desc = metadata['description']
                if len(desc) < 20:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Description too short ({len(desc)} chars). Minimum 20 characters.",
                        location=str(agent_file)
                    ))
                if len(desc) > 300:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Description too long ({len(desc)} chars). Maximum 300 characters.",
                        location=str(agent_file)
                    ))

            # Validate tools
            if 'tools' in metadata:
                tools = metadata['tools']
                if not isinstance(tools, list):
                    errors.append(ValidationIssue(
                        severity="error",
                        message="'tools' field must be a list",
                        location=str(agent_file)
                    ))
                else:
                    invalid_tools = [t for t in tools if t not in self.VALID_TOOLS]
                    if invalid_tools:
                        errors.append(ValidationIssue(
                            severity="error",
                            message=f"Invalid tools: {', '.join(invalid_tools)}. Valid tools: {', '.join(self.VALID_TOOLS)}",
                            location=str(agent_file)
                        ))
                    if len(tools) == 0:
                        errors.append(ValidationIssue(
                            severity="error",
                            message="At least one tool must be specified",
                            location=str(agent_file)
                        ))
                    if len(tools) > 6:
                        warnings.append(ValidationIssue(
                            severity="warning",
                            message=f"Many tools specified ({len(tools)}). Consider using minimal necessary tools.",
                            location=str(agent_file)
                        ))

            # Validate model
            if 'model' in metadata:
                model = metadata['model']
                if model not in self.VALID_MODELS:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Invalid model: '{model}'. Valid models: {', '.join(self.VALID_MODELS)}",
                        location=str(agent_file)
                    ))

            # Validate activation (optional field)
            if 'activation' in metadata:
                activation = metadata['activation']
                if activation not in self.VALID_ACTIVATIONS:
                    errors.append(ValidationIssue(
                        severity="error",
                        message=f"Invalid activation: '{activation}'. Valid: {', '.join(self.VALID_ACTIVATIONS)}",
                        location=str(agent_file)
                    ))
                if activation == 'always':
                    warnings.append(ValidationIssue(
                        severity="warning",
                        message="Activation mode 'always' should be used sparingly",
                        location=str(agent_file)
                    ))

            # Check for content after frontmatter
            body = content[yaml_end + 3:].strip()
            if len(body) < 100:
                warnings.append(ValidationIssue(
                    severity="warning",
                    message="Agent body seems very short. Consider adding more detailed instructions.",
                    location=str(agent_file)
                ))

            # Check for teaching approach (for teaching agents)
            if 'teach' in metadata.get('description', '').lower() or 'guide' in metadata.get('description', '').lower():
                if '❌ NEVER' not in body or '✅ ALWAYS' not in body:
                    warnings.append(ValidationIssue(
                        severity="warning",
                        message="Teaching agent should include '❌ NEVER' and '✅ ALWAYS' guidelines",
                        location=str(agent_file)
                    ))

        except Exception as e:
            errors.append(ValidationIssue(
                severity="error",
                message=f"Failed to validate agent: {e}",
                location=str(agent_file)
            ))

        return ValidationResult(
            name=agent_name,
            type="agent",
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )


def print_results(results: List[ValidationResult], verbose: bool = False):
    """
    Print validation results in human-readable format.

    Args:
        results: List of ValidationResult objects
        verbose: Whether to show verbose output
    """
    skill_results = [r for r in results if r.type == "skill"]
    agent_results = [r for r in results if r.type == "agent"]

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    # Print skills
    if skill_results:
        print("\n🔍 Validating Skills...")
        print("=" * 70)
        for result in skill_results:
            if result.passed and len(result.warnings) == 0:
                ops_count = len(result.metadata.get('operations', {})) if result.metadata else 0
                print(f"✅ {result.name} ({ops_count} operations)")
            elif result.passed:
                print(f"⚠️  {result.name} ({len(result.warnings)} warnings)")
            else:
                print(f"❌ {result.name} ({len(result.errors)} errors)")

            if verbose or not result.passed:
                for error in result.errors:
                    print(f"   ❌ ERROR: {error.message}")
                    if error.location:
                        print(f"      Location: {error.location}")
                for warning in result.warnings:
                    if verbose:
                        print(f"   ⚠️  WARNING: {warning.message}")
                        if warning.location:
                            print(f"      Location: {warning.location}")

    # Print agents
    if agent_results:
        print("\n🔍 Validating Agents...")
        print("=" * 70)
        for result in agent_results:
            if result.passed and len(result.warnings) == 0:
                print(f"✅ {result.name}")
            elif result.passed:
                print(f"⚠️  {result.name} ({len(result.warnings)} warnings)")
            else:
                print(f"❌ {result.name} ({len(result.errors)} errors)")

            if verbose or not result.passed:
                for error in result.errors:
                    print(f"   ❌ ERROR: {error.message}")
                    if error.location:
                        print(f"      Location: {error.location}")
                for warning in result.warnings:
                    if verbose:
                        print(f"   ⚠️  WARNING: {warning.message}")
                        if warning.location:
                            print(f"      Location: {warning.location}")

    # Print summary
    print("\n" + "━" * 70)
    print("Summary:")
    print("━" * 70)
    print(f"✅ {len([r for r in results if r.passed])} passed")
    print(f"❌ {len([r for r in results if not r.passed])} failed")
    print(f"⚠️  {total_warnings} warnings")

    if total_errors > 0:
        print(f"\n❌ Validation failed with {total_errors} errors")
    elif total_warnings > 0:
        print(f"\n⚠️  Validation passed with {total_warnings} warnings")
    else:
        print("\n✅ All validations passed!")


def output_json(results: List[ValidationResult]):
    """
    Output results in JSON format.

    Args:
        results: List of ValidationResult objects
    """
    output = {
        "summary": {
            "total": len(results),
            "passed": len([r for r in results if r.passed]),
            "failed": len([r for r in results if not r.passed]),
            "errors": sum(len(r.errors) for r in results),
            "warnings": sum(len(r.warnings) for r in results)
        },
        "results": []
    }

    for result in results:
        output["results"].append({
            "name": result.name,
            "type": result.type,
            "passed": result.passed,
            "errors": [{"severity": e.severity, "message": e.message, "location": e.location} for e in result.errors],
            "warnings": [{"severity": w.severity, "message": w.message, "location": w.location} for w in result.warnings],
            "metadata": result.metadata
        })

    print(json.dumps(output, indent=2))


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Validate all skills and agents in the project",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--skills-only", action="store_true", help="Validate skills only")
    parser.add_argument("--agents-only", action="store_true", help="Validate agents only")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    results = []

    # Validate skills
    if not args.agents_only:
        skills_dir = PROJECT_ROOT / "skills"
        skill_validator = SkillValidator(skills_dir)
        skill_results = skill_validator.validate_all()
        results.extend(skill_results)

    # Validate agents
    if not args.skills_only:
        agents_dir = PROJECT_ROOT / "agents"
        agent_validator = AgentValidator(agents_dir)
        agent_results = agent_validator.validate_all()
        results.extend(agent_results)

    # Output results
    if args.json:
        output_json(results)
    else:
        print("=" * 70)
        print("Unified Validation - Skills and Agents")
        print("=" * 70)
        print_results(results, verbose=args.verbose)

    # Determine exit code
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    if total_errors > 0:
        return 1
    elif total_warnings > 0:
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
