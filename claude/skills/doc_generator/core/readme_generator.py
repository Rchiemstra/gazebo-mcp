"""
README Generator

Generates comprehensive README.md files from project analysis.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Any
import re


@dataclass
class ProjectInfo:
    """Project information extracted from analysis."""
    name: str
    description: str
    version: str
    author: str
    license: str
    python_version: str
    dependencies: List[str]
    dev_dependencies: List[str]
    entry_points: List[str]
    modules: List[str]
    has_tests: bool
    has_ci: bool


@dataclass
class ReadmeSection:
    """A section of the README."""
    title: str
    content: str
    order: int


class ReadmeGenerator:
    """Generates comprehensive README.md files."""

    def __init__(self):
        self.sections: List[ReadmeSection] = []

    def generate(
        self,
        project_path: str,
        include_api: bool = True,
        include_examples: bool = True
    ) -> Dict[str, Any]:
        """
        Generate README.md for a project.

        Args:
            project_path: Path to project root
            include_api: Include API reference section
            include_examples: Include usage examples

        Returns:
            Dictionary with README content and metadata
        """
        project_dir = Path(project_path)

        # Analyze project
        project_info = self._analyze_project(project_dir)

        # Generate sections
        self._generate_header(project_info)
        self._generate_overview(project_info)
        self._generate_features(project_info, project_dir)
        self._generate_installation(project_info)
        self._generate_quick_start(project_info, project_dir, include_examples)

        if include_api:
            self._generate_api_reference(project_info, project_dir)

        self._generate_development(project_info)
        self._generate_testing(project_info)
        self._generate_contributing()
        self._generate_license(project_info)

        # Assemble README
        readme_content = self._assemble_readme()

        return {
            'readme_content': readme_content,
            'sections_generated': [s.title for s in self.sections],
            'project_info': {
                'name': project_info.name,
                'description': project_info.description,
                'version': project_info.version,
                'dependencies': len(project_info.dependencies)
            }
        }

    def _analyze_project(self, project_dir: Path) -> ProjectInfo:
        """Analyze project structure and extract information."""
        name = project_dir.name
        description = self._find_description(project_dir)
        version = self._find_version(project_dir)
        author = self._find_author(project_dir)
        license_type = self._find_license(project_dir)
        python_version = self._find_python_version(project_dir)
        dependencies = self._find_dependencies(project_dir)
        dev_dependencies = self._find_dev_dependencies(project_dir)
        entry_points = self._find_entry_points(project_dir)
        modules = self._find_modules(project_dir)
        has_tests = self._has_tests(project_dir)
        has_ci = self._has_ci(project_dir)

        return ProjectInfo(
            name=name,
            description=description,
            version=version,
            author=author,
            license=license_type,
            python_version=python_version,
            dependencies=dependencies,
            dev_dependencies=dev_dependencies,
            entry_points=entry_points,
            modules=modules,
            has_tests=has_tests,
            has_ci=has_ci
        )

    def _find_description(self, project_dir: Path) -> str:
        """Find project description."""
        # Try setup.py
        setup_py = project_dir / 'setup.py'
        if setup_py.exists():
            content = setup_py.read_text()
            match = re.search(r'description=["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        # Try pyproject.toml
        pyproject = project_dir / 'pyproject.toml'
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        # Try __init__.py
        init_file = project_dir / project_dir.name / '__init__.py'
        if not init_file.exists():
            # Try to find any __init__.py
            init_files = list(project_dir.rglob('__init__.py'))
            if init_files:
                init_file = init_files[0]

        if init_file.exists():
            try:
                tree = ast.parse(init_file.read_text())
                docstring = ast.get_docstring(tree)
                if docstring:
                    # Get first line of docstring
                    return docstring.split('\n')[0]
            except:
                pass

        return f"A Python project - {project_dir.name}"

    def _find_version(self, project_dir: Path) -> str:
        """Find project version."""
        # Try __init__.py
        init_file = project_dir / project_dir.name / '__init__.py'
        if init_file.exists():
            content = init_file.read_text()
            match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        # Try pyproject.toml
        pyproject = project_dir / 'pyproject.toml'
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        return "0.1.0"

    def _find_author(self, project_dir: Path) -> str:
        """Find project author."""
        # Try setup.py
        setup_py = project_dir / 'setup.py'
        if setup_py.exists():
            content = setup_py.read_text()
            match = re.search(r'author=["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        # Try pyproject.toml
        pyproject = project_dir / 'pyproject.toml'
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'authors\s*=\s*\[["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        return "Project Contributors"

    def _find_license(self, project_dir: Path) -> str:
        """Find project license."""
        license_file = project_dir / 'LICENSE'
        if license_file.exists():
            content = license_file.read_text()
            if 'MIT' in content:
                return 'MIT'
            elif 'Apache' in content:
                return 'Apache 2.0'
            elif 'GPL' in content:
                return 'GPL'
            elif 'BSD' in content:
                return 'BSD'

        return 'MIT'

    def _find_python_version(self, project_dir: Path) -> str:
        """Find required Python version."""
        # Try pyproject.toml
        pyproject = project_dir / 'pyproject.toml'
        if pyproject.exists():
            content = pyproject.read_text()
            match = re.search(r'python\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)

        return ">=3.8"

    def _find_dependencies(self, project_dir: Path) -> List[str]:
        """Find project dependencies."""
        dependencies = []

        # Try requirements.txt
        requirements = project_dir / 'requirements.txt'
        if requirements.exists():
            for line in requirements.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name
                    pkg = re.split(r'[>=<]', line)[0].strip()
                    dependencies.append(pkg)

        # Try pyproject.toml
        pyproject = project_dir / 'pyproject.toml'
        if pyproject.exists():
            content = pyproject.read_text()
            # Simple regex to find dependencies
            in_deps = False
            for line in content.splitlines():
                if 'dependencies' in line and '=' in line:
                    in_deps = True
                elif in_deps and ']' in line:
                    in_deps = False
                elif in_deps and '"' in line:
                    match = re.search(r'"([^">=<]+)', line)
                    if match:
                        dependencies.append(match.group(1))

        return dependencies

    def _find_dev_dependencies(self, project_dir: Path) -> List[str]:
        """Find development dependencies."""
        dependencies = []

        # Try requirements-dev.txt
        requirements = project_dir / 'requirements-dev.txt'
        if requirements.exists():
            for line in requirements.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    pkg = re.split(r'[>=<]', line)[0].strip()
                    dependencies.append(pkg)

        return dependencies

    def _find_entry_points(self, project_dir: Path) -> List[str]:
        """Find CLI entry points or main scripts."""
        entry_points = []

        # Look for main.py, cli.py, __main__.py
        for pattern in ['main.py', 'cli.py', '__main__.py']:
            files = list(project_dir.rglob(pattern))
            entry_points.extend([str(f.relative_to(project_dir)) for f in files])

        return entry_points

    def _find_modules(self, project_dir: Path) -> List[str]:
        """Find main modules/packages."""
        modules = []

        # Find directories with __init__.py
        for init_file in project_dir.rglob('__init__.py'):
            module_dir = init_file.parent
            if module_dir != project_dir:
                relative = module_dir.relative_to(project_dir)
                # Only top-level modules
                if len(relative.parts) == 1:
                    modules.append(relative.name)

        return modules

    def _has_tests(self, project_dir: Path) -> bool:
        """Check if project has tests."""
        test_dirs = ['tests', 'test']
        for test_dir in test_dirs:
            if (project_dir / test_dir).exists():
                return True

        # Check for test files
        test_files = list(project_dir.rglob('test_*.py'))
        return len(test_files) > 0

    def _has_ci(self, project_dir: Path) -> bool:
        """Check if project has CI configuration."""
        ci_files = [
            '.github/workflows',
            '.gitlab-ci.yml',
            '.travis.yml',
            'azure-pipelines.yml'
        ]

        for ci_file in ci_files:
            if (project_dir / ci_file).exists():
                return True

        return False

    def _generate_header(self, info: ProjectInfo):
        """Generate README header."""
        content = f"# {info.name}\n\n"
        content += f"{info.description}\n"

        self.sections.append(ReadmeSection(
            title="Header",
            content=content,
            order=1
        ))

    def _generate_overview(self, info: ProjectInfo):
        """Generate overview section."""
        content = "## Overview\n\n"
        content += f"{info.description}\n\n"

        if info.modules:
            content += "### Key Modules\n\n"
            for module in info.modules:
                content += f"- `{module}`: {self._describe_module(module)}\n"
            content += "\n"

        self.sections.append(ReadmeSection(
            title="Overview",
            content=content,
            order=2
        ))

    def _generate_features(self, info: ProjectInfo, project_dir: Path):
        """Generate features section."""
        content = "## Features\n\n"

        # Extract features from code analysis
        features = self._extract_features(project_dir)

        if features:
            for feature in features:
                content += f"- {feature}\n"
        else:
            content += f"- Built with Python {info.python_version}\n"
            if info.has_tests:
                content += "- Comprehensive test suite\n"
            if info.has_ci:
                content += "- Continuous integration\n"
            content += "- Easy to use API\n"

        content += "\n"

        self.sections.append(ReadmeSection(
            title="Features",
            content=content,
            order=3
        ))

    def _generate_installation(self, info: ProjectInfo):
        """Generate installation section."""
        content = "## Installation\n\n"

        content += "### Using pip\n\n"
        content += "```bash\n"
        content += f"pip install {info.name}\n"
        content += "```\n\n"

        content += "### From source\n\n"
        content += "```bash\n"
        content += f"git clone https://github.com/{info.author}/{info.name}.git\n"
        content += f"cd {info.name}\n"
        content += "pip install -e .\n"
        content += "```\n\n"

        if info.dependencies:
            content += "### Dependencies\n\n"
            for dep in info.dependencies[:10]:  # Max 10
                content += f"- {dep}\n"
            if len(info.dependencies) > 10:
                content += f"- ... and {len(info.dependencies) - 10} more\n"
            content += "\n"

        self.sections.append(ReadmeSection(
            title="Installation",
            content=content,
            order=4
        ))

    def _generate_quick_start(
        self,
        info: ProjectInfo,
        project_dir: Path,
        include_examples: bool
    ):
        """Generate quick start section."""
        content = "## Quick Start\n\n"

        if include_examples:
            examples = self._find_examples(project_dir)
            if examples:
                content += "### Basic Usage\n\n"
                content += "```python\n"
                content += examples[0]
                content += "```\n\n"
            else:
                # Generate basic example
                content += "### Basic Usage\n\n"
                content += "```python\n"
                if info.modules:
                    content += f"from {info.modules[0]} import ...\n\n"
                    content += "# Your code here\n"
                content += "```\n\n"

        self.sections.append(ReadmeSection(
            title="Quick Start",
            content=content,
            order=5
        ))

    def _generate_api_reference(self, info: ProjectInfo, project_dir: Path):
        """Generate API reference section."""
        content = "## API Reference\n\n"

        # Analyze main modules
        for module_name in info.modules[:3]:  # Max 3 modules
            module_path = project_dir / module_name / '__init__.py'
            if not module_path.exists():
                continue

            try:
                tree = ast.parse(module_path.read_text())

                # Find exported functions
                functions = []
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        functions.append(node)

                if functions:
                    content += f"### {module_name}\n\n"
                    for func in functions[:5]:  # Max 5 functions
                        content += f"#### `{func.name}()`\n\n"
                        docstring = ast.get_docstring(func)
                        if docstring:
                            # Get first line
                            first_line = docstring.split('\n')[0]
                            content += f"{first_line}\n\n"
                        else:
                            content += f"Function: {func.name}\n\n"

            except:
                pass

        if content == "## API Reference\n\n":
            content += "See source code for detailed API documentation.\n\n"

        self.sections.append(ReadmeSection(
            title="API Reference",
            content=content,
            order=6
        ))

    def _generate_development(self, info: ProjectInfo):
        """Generate development section."""
        content = "## Development\n\n"

        content += "### Setup Development Environment\n\n"
        content += "```bash\n"
        content += f"git clone https://github.com/{info.author}/{info.name}.git\n"
        content += f"cd {info.name}\n"
        content += "pip install -e .[dev]\n"
        content += "```\n\n"

        if info.dev_dependencies:
            content += "### Development Dependencies\n\n"
            for dep in info.dev_dependencies:
                content += f"- {dep}\n"
            content += "\n"

        self.sections.append(ReadmeSection(
            title="Development",
            content=content,
            order=7
        ))

    def _generate_testing(self, info: ProjectInfo):
        """Generate testing section."""
        if not info.has_tests:
            return

        content = "## Testing\n\n"

        content += "Run tests using pytest:\n\n"
        content += "```bash\n"
        content += "pytest\n"
        content += "```\n\n"

        content += "With coverage:\n\n"
        content += "```bash\n"
        content += "pytest --cov\n"
        content += "```\n\n"

        self.sections.append(ReadmeSection(
            title="Testing",
            content=content,
            order=8
        ))

    def _generate_contributing(self):
        """Generate contributing section."""
        content = "## Contributing\n\n"

        content += "Contributions are welcome! Please:\n\n"
        content += "1. Fork the repository\n"
        content += "2. Create a feature branch\n"
        content += "3. Make your changes\n"
        content += "4. Add tests\n"
        content += "5. Submit a pull request\n\n"

        self.sections.append(ReadmeSection(
            title="Contributing",
            content=content,
            order=9
        ))

    def _generate_license(self, info: ProjectInfo):
        """Generate license section."""
        content = "## License\n\n"
        content += f"This project is licensed under the {info.license} License.\n"

        self.sections.append(ReadmeSection(
            title="License",
            content=content,
            order=10
        ))

    def _assemble_readme(self) -> str:
        """Assemble all sections into final README."""
        # Sort sections by order
        sorted_sections = sorted(self.sections, key=lambda s: s.order)

        # Join all content
        readme = "\n".join(s.content for s in sorted_sections)

        return readme.strip() + "\n"

    def _describe_module(self, module_name: str) -> str:
        """Generate description for a module."""
        descriptions = {
            'core': 'Core functionality',
            'utils': 'Utility functions',
            'api': 'API interface',
            'cli': 'Command-line interface',
            'models': 'Data models',
            'handlers': 'Event handlers',
            'services': 'Service layer',
        }

        return descriptions.get(module_name, f'{module_name.capitalize()} module')

    def _extract_features(self, project_dir: Path) -> List[str]:
        """Extract features from project analysis."""
        features = []

        # Look for features in documentation
        readme = project_dir / 'README.md'
        if readme.exists():
            content = readme.read_text()
            # Look for existing features section
            match = re.search(r'## Features\s*(.*?)(?=##|\Z)', content, re.DOTALL)
            if match:
                features_text = match.group(1)
                for line in features_text.splitlines():
                    line = line.strip()
                    if line.startswith('-') or line.startswith('*'):
                        feature = line.lstrip('-*').strip()
                        if feature:
                            features.append(feature)

        return features

    def _find_examples(self, project_dir: Path) -> List[str]:
        """Find code examples in the project."""
        examples = []

        # Look in examples directory
        examples_dir = project_dir / 'examples'
        if examples_dir.exists():
            for example_file in examples_dir.glob('*.py'):
                try:
                    content = example_file.read_text()
                    # Extract first 10 lines as example
                    lines = content.splitlines()[:10]
                    example = '\n'.join(lines)
                    examples.append(example)
                    break  # Just take first example
                except:
                    pass

        # Look in README
        readme = project_dir / 'README.md'
        if readme.exists() and not examples:
            content = readme.read_text()
            # Find code blocks
            matches = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
            if matches:
                examples.append(matches[0])

        return examples


def generate_readme(
    project_path: str,
    include_api: bool = True,
    include_examples: bool = True
) -> Dict[str, Any]:
    """
    Generate comprehensive README.md for a project.

    Args:
        project_path: Path to project root directory
        include_api: Whether to include API reference section
        include_examples: Whether to include usage examples

    Returns:
        Dictionary containing:
        - readme_content: Generated README markdown content
        - sections_generated: List of section titles
        - project_info: Basic project metadata

    Example:
        >>> result = generate_readme(
        ...     project_path='./myproject',
        ...     include_api=True,
        ...     include_examples=True
        ... )
        >>> with open('README.md', 'w') as f:
        ...     f.write(result['readme_content'])
    """
    generator = ReadmeGenerator()
    return generator.generate(project_path, include_api, include_examples)
