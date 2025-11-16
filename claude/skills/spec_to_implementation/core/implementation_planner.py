"""
Implementation Planner

Creates detailed implementation plans from specifications.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional

from .spec_parser import Specification, Requirement


class TaskType(Enum):
    """Type of implementation task."""
    SCAFFOLD = "scaffold"
    IMPLEMENT = "implement"
    TEST = "test"
    DOCUMENT = "document"
    VALIDATE = "validate"
    REFACTOR = "refactor"


class ComplexityLevel(Enum):
    """Complexity estimation."""
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class ImplementationTask:
    """A single implementation task."""
    id: str
    task_type: TaskType
    description: str
    estimated_complexity: ComplexityLevel
    dependencies: List[str] = field(default_factory=list)
    files_to_create: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    requirements_addressed: List[str] = field(default_factory=list)


@dataclass
class ImplementationPlan:
    """Complete implementation plan."""
    title: str
    overview: str
    tasks: List[ImplementationTask]
    estimated_complexity: ComplexityLevel
    files_to_create: List[str]
    files_to_modify: List[str]
    dependencies_needed: List[str]
    risks: List[str]
    total_requirements: int


class ImplementationPlanner:
    """Creates implementation plans from specifications."""

    def create_plan(
        self,
        spec: Specification,
        project_context: Optional[str] = None
    ) -> ImplementationPlan:
        """
        Create implementation plan from specification.

        Args:
            spec: Parsed specification
            project_context: Optional path to existing project

        Returns:
            Detailed implementation plan
        """
        tasks = []
        files_to_create = []
        files_to_modify = []
        risks = []

        # 1. Create scaffolding task
        scaffold_task = self._create_scaffold_task(spec)
        tasks.append(scaffold_task)
        files_to_create.extend(scaffold_task.files_to_create)

        # 2. Create implementation tasks for each requirement
        for req in spec.requirements:
            impl_task = self._create_implementation_task(req, spec)
            tasks.append(impl_task)

            files_to_create.extend(impl_task.files_to_create)
            files_to_modify.extend(impl_task.files_to_modify)

        # 3. Create test generation task
        test_task = self._create_test_task(spec)
        tasks.append(test_task)
        files_to_create.extend(test_task.files_to_create)

        # 4. Create documentation task
        doc_task = self._create_documentation_task(spec)
        tasks.append(doc_task)

        # 5. Create validation task
        validation_task = self._create_validation_task(spec)
        tasks.append(validation_task)

        # Estimate overall complexity
        overall_complexity = self._estimate_overall_complexity(spec, tasks)

        # Identify risks
        risks = self._identify_risks(spec, tasks)

        # Remove duplicates from file lists
        files_to_create = list(set(files_to_create))
        files_to_modify = list(set(files_to_modify))

        return ImplementationPlan(
            title=f"Implementation Plan: {spec.title}",
            overview=spec.description,
            tasks=tasks,
            estimated_complexity=overall_complexity,
            files_to_create=files_to_create,
            files_to_modify=files_to_modify,
            dependencies_needed=spec.dependencies,
            risks=risks,
            total_requirements=len(spec.requirements)
        )

    def _create_scaffold_task(self, spec: Specification) -> ImplementationTask:
        """Create task for scaffolding."""
        # Determine main module name from title
        module_name = self._title_to_module_name(spec.title)

        files = [
            f"{module_name}/__init__.py",
            f"{module_name}/core.py",
        ]

        return ImplementationTask(
            id="TASK-001",
            task_type=TaskType.SCAFFOLD,
            description="Create project structure and boilerplate",
            estimated_complexity=ComplexityLevel.SIMPLE,
            files_to_create=files,
            requirements_addressed=[]
        )

    def _create_implementation_task(
        self,
        requirement: Requirement,
        spec: Specification
    ) -> ImplementationTask:
        """Create implementation task for a requirement."""
        # Generate task ID
        task_id = requirement.id.replace("REQ", "TASK")

        # Determine complexity
        complexity = self._estimate_requirement_complexity(requirement, spec)

        # Determine files needed
        module_name = self._title_to_module_name(spec.title)
        files_to_create = []
        files_to_modify = [f"{module_name}/core.py"]

        # Check if requirement needs separate module
        if complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.VERY_COMPLEX]:
            # Extract feature name from requirement
            feature_name = self._extract_feature_name(requirement.description)
            if feature_name:
                files_to_create.append(f"{module_name}/{feature_name}.py")

        return ImplementationTask(
            id=task_id,
            task_type=TaskType.IMPLEMENT,
            description=f"Implement: {requirement.description}",
            estimated_complexity=complexity,
            files_to_create=files_to_create,
            files_to_modify=files_to_modify,
            requirements_addressed=[requirement.id]
        )

    def _create_test_task(self, spec: Specification) -> ImplementationTask:
        """Create task for test generation."""
        module_name = self._title_to_module_name(spec.title)

        files = [
            f"tests/test_{module_name}.py",
        ]

        return ImplementationTask(
            id=f"TASK-{900:03d}",
            task_type=TaskType.TEST,
            description="Generate comprehensive test suite",
            estimated_complexity=ComplexityLevel.MODERATE,
            dependencies=["TASK-001"] + [req.id.replace("REQ", "TASK") for req in spec.requirements],
            files_to_create=files,
            requirements_addressed=[req.id for req in spec.requirements]
        )

    def _create_documentation_task(self, spec: Specification) -> ImplementationTask:
        """Create task for documentation."""
        module_name = self._title_to_module_name(spec.title)

        files = [
            f"{module_name}/README.md",
        ]

        return ImplementationTask(
            id=f"TASK-{950:03d}",
            task_type=TaskType.DOCUMENT,
            description="Generate documentation and docstrings",
            estimated_complexity=ComplexityLevel.SIMPLE,
            dependencies=[f"TASK-{900:03d}"],
            files_to_create=files,
            requirements_addressed=[]
        )

    def _create_validation_task(self, spec: Specification) -> ImplementationTask:
        """Create task for validation."""
        return ImplementationTask(
            id=f"TASK-{999:03d}",
            task_type=TaskType.VALIDATE,
            description="Validate code quality and completeness",
            estimated_complexity=ComplexityLevel.SIMPLE,
            dependencies=[f"TASK-{950:03d}"],
            files_to_create=[],
            files_to_modify=[],
            requirements_addressed=[]
        )

    def _estimate_requirement_complexity(
        self,
        requirement: Requirement,
        spec: Specification
    ) -> ComplexityLevel:
        """Estimate complexity of a requirement."""
        desc = requirement.description.lower()

        # Simple indicators
        simple_indicators = ['display', 'show', 'print', 'format', 'validate']
        if any(word in desc for word in simple_indicators):
            return ComplexityLevel.SIMPLE

        # Complex indicators
        complex_indicators = [
            'algorithm', 'optimize', 'parse', 'analyze',
            'integrate', 'synchronize', 'concurrent'
        ]
        if any(word in desc for word in complex_indicators):
            return ComplexityLevel.COMPLEX

        # Very complex indicators
        very_complex_indicators = [
            'distributed', 'real-time', 'machine learning',
            'ai', 'cryptographic', 'protocol'
        ]
        if any(word in desc for word in very_complex_indicators):
            return ComplexityLevel.VERY_COMPLEX

        # Check dependencies
        if requirement.dependencies:
            return ComplexityLevel.MODERATE

        # Default
        return ComplexityLevel.MODERATE

    def _estimate_overall_complexity(
        self,
        spec: Specification,
        tasks: List[ImplementationTask]
    ) -> ComplexityLevel:
        """Estimate overall implementation complexity."""
        # Count requirements
        num_requirements = len(spec.requirements)

        # Count complex tasks
        complex_count = sum(
            1 for task in tasks
            if task.estimated_complexity in [
                ComplexityLevel.COMPLEX,
                ComplexityLevel.VERY_COMPLEX
            ]
        )

        # Determine overall
        if num_requirements == 0:
            return ComplexityLevel.TRIVIAL

        if num_requirements <= 3 and complex_count == 0:
            return ComplexityLevel.SIMPLE

        if num_requirements <= 5 and complex_count <= 1:
            return ComplexityLevel.MODERATE

        if num_requirements <= 10 and complex_count <= 3:
            return ComplexityLevel.COMPLEX

        return ComplexityLevel.VERY_COMPLEX

    def _identify_risks(
        self,
        spec: Specification,
        tasks: List[ImplementationTask]
    ) -> List[str]:
        """Identify implementation risks."""
        risks = []

        # Check for complex requirements
        complex_tasks = [
            task for task in tasks
            if task.estimated_complexity in [
                ComplexityLevel.COMPLEX,
                ComplexityLevel.VERY_COMPLEX
            ]
        ]

        if complex_tasks:
            risks.append(
                f"{len(complex_tasks)} complex task(s) requiring careful implementation"
            )

        # Check for external dependencies
        if spec.dependencies:
            risks.append(
                f"{len(spec.dependencies)} external dependencies may cause integration issues"
            )

        # Check for missing acceptance criteria
        reqs_without_criteria = [
            req for req in spec.requirements
            if not req.acceptance_criteria
        ]

        if reqs_without_criteria:
            risks.append(
                f"{len(reqs_without_criteria)} requirements lack clear acceptance criteria"
            )

        # Check for vague requirements
        vague_keywords = ['somehow', 'maybe', 'possibly', 'probably', 'might']
        vague_reqs = [
            req for req in spec.requirements
            if any(word in req.description.lower() for word in vague_keywords)
        ]

        if vague_reqs:
            risks.append(
                f"{len(vague_reqs)} requirements are vaguely defined"
            )

        return risks

    def _title_to_module_name(self, title: str) -> str:
        """Convert title to module name."""
        # Remove special characters
        name = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in title)

        # Convert to snake_case
        words = name.lower().split()
        return '_'.join(words)

    def _extract_feature_name(self, description: str) -> Optional[str]:
        """Extract feature name from requirement description."""
        # Look for nouns that might be feature names
        words = description.split()

        # Skip common words
        skip_words = {
            'the', 'a', 'an', 'should', 'must', 'will', 'can',
            'be', 'have', 'do', 'system', 'user', 'allow', 'enable'
        }

        meaningful_words = [
            word.lower().strip('.,;:!?')
            for word in words
            if word.lower() not in skip_words and len(word) > 3
        ]

        if meaningful_words:
            # Return first meaningful word as feature name
            return meaningful_words[0]

        return None
