"""
Dependency Analyzer

Parses and analyzes project dependencies across multiple ecosystems.
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum


class Ecosystem(Enum):
    """Supported package ecosystems."""
    PYTHON = "python"
    NPM = "npm"
    UNKNOWN = "unknown"


class DependencyType(Enum):
    """Type of dependency."""
    DIRECT = "direct"
    TRANSITIVE = "transitive"
    DEV = "dev"


@dataclass
class Dependency:
    """Represents a single dependency."""
    name: str
    version: str
    ecosystem: Ecosystem
    dependency_type: DependencyType
    spec: str  # Original version specification (e.g., "^1.2.3", ">=1.0.0")
    source_file: Optional[str] = None
    transitive_from: Optional[str] = None  # Parent dependency if transitive


@dataclass
class DependencyAnalysis:
    """Results of dependency analysis."""
    project_path: str
    ecosystem: Ecosystem
    total_dependencies: int
    direct_dependencies: int
    transitive_dependencies: int
    dev_dependencies: int
    dependencies: List[Dependency] = field(default_factory=list)
    manifest_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class DependencyAnalyzer:
    """Analyzes project dependencies."""

    def __init__(self):
        self.parsers = {
            Ecosystem.PYTHON: self._analyze_python,
            Ecosystem.NPM: self._analyze_npm,
        }

    def analyze_project(
        self,
        project_path: str,
        ecosystem: Optional[str] = None
    ) -> DependencyAnalysis:
        """
        Analyze dependencies in a project.

        Args:
            project_path: Path to project directory
            ecosystem: Specific ecosystem to analyze (python, npm, auto)

        Returns:
            DependencyAnalysis with results
        """
        project_path = Path(project_path)

        if not project_path.exists():
            return DependencyAnalysis(
                project_path=str(project_path),
                ecosystem=Ecosystem.UNKNOWN,
                total_dependencies=0,
                direct_dependencies=0,
                transitive_dependencies=0,
                dev_dependencies=0,
                errors=[f"Project path does not exist: {project_path}"]
            )

        # Detect ecosystem if not specified
        if ecosystem is None or ecosystem == "auto":
            detected_ecosystem = self._detect_ecosystem(project_path)
        else:
            detected_ecosystem = Ecosystem(ecosystem)

        # Parse dependencies using appropriate parser
        if detected_ecosystem in self.parsers:
            return self.parsers[detected_ecosystem](project_path)
        else:
            return DependencyAnalysis(
                project_path=str(project_path),
                ecosystem=Ecosystem.UNKNOWN,
                total_dependencies=0,
                direct_dependencies=0,
                transitive_dependencies=0,
                dev_dependencies=0,
                errors=[f"Unsupported ecosystem: {detected_ecosystem}"]
            )

    def _detect_ecosystem(self, project_path: Path) -> Ecosystem:
        """Detect project ecosystem from manifest files."""
        # Check for Python
        if (project_path / "requirements.txt").exists() or \
           (project_path / "setup.py").exists() or \
           (project_path / "pyproject.toml").exists() or \
           (project_path / "Pipfile").exists():
            return Ecosystem.PYTHON

        # Check for Node.js
        if (project_path / "package.json").exists():
            return Ecosystem.NPM

        return Ecosystem.UNKNOWN

    def _analyze_python(self, project_path: Path) -> DependencyAnalysis:
        """Analyze Python dependencies."""
        dependencies = []
        manifest_files = []
        errors = []

        # Parse requirements.txt
        req_file = project_path / "requirements.txt"
        if req_file.exists():
            manifest_files.append(str(req_file))
            try:
                parsed = self._parse_requirements_txt(req_file)
                dependencies.extend(parsed)
            except Exception as e:
                errors.append(f"Error parsing requirements.txt: {e}")

        # Parse setup.py
        setup_file = project_path / "setup.py"
        if setup_file.exists():
            manifest_files.append(str(setup_file))
            try:
                parsed = self._parse_setup_py(setup_file)
                dependencies.extend(parsed)
            except Exception as e:
                errors.append(f"Error parsing setup.py: {e}")

        # Parse pyproject.toml
        pyproject_file = project_path / "pyproject.toml"
        if pyproject_file.exists():
            manifest_files.append(str(pyproject_file))
            try:
                parsed = self._parse_pyproject_toml(pyproject_file)
                dependencies.extend(parsed)
            except Exception as e:
                errors.append(f"Error parsing pyproject.toml: {e}")

        # Deduplicate dependencies by name
        unique_deps = {}
        for dep in dependencies:
            if dep.name not in unique_deps:
                unique_deps[dep.name] = dep

        dependencies = list(unique_deps.values())

        # Count by type
        direct_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.DIRECT)
        transitive_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.TRANSITIVE)
        dev_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.DEV)

        return DependencyAnalysis(
            project_path=str(project_path),
            ecosystem=Ecosystem.PYTHON,
            total_dependencies=len(dependencies),
            direct_dependencies=direct_count,
            transitive_dependencies=transitive_count,
            dev_dependencies=dev_count,
            dependencies=dependencies,
            manifest_files=manifest_files,
            errors=errors
        )

    def _parse_requirements_txt(self, file_path: Path) -> List[Dependency]:
        """Parse requirements.txt file."""
        dependencies = []

        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Skip -e (editable) and -r (recursive) lines
                if line.startswith('-e ') or line.startswith('-r '):
                    continue

                # Parse dependency
                dep = self._parse_python_requirement(line, str(file_path))
                if dep:
                    dependencies.append(dep)

        return dependencies

    def _parse_python_requirement(self, requirement: str, source_file: str) -> Optional[Dependency]:
        """Parse a single Python requirement string."""
        # Handle extras: package[extra1,extra2]
        requirement = re.sub(r'\[.*?\]', '', requirement)

        # Common operators: ==, >=, <=, >, <, ~=, !=
        operators = ['==', '>=', '<=', '~=', '!=', '>', '<']

        name = None
        version = None
        spec = requirement

        for op in operators:
            if op in requirement:
                parts = requirement.split(op, 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    version = parts[1].strip().split(',')[0].strip()  # Handle multiple constraints
                    break

        # If no operator found, it's just a package name
        if name is None:
            name = requirement.strip()
            version = "any"
            spec = name

        if not name:
            return None

        return Dependency(
            name=name,
            version=version,
            ecosystem=Ecosystem.PYTHON,
            dependency_type=DependencyType.DIRECT,
            spec=spec,
            source_file=source_file
        )

    def _parse_setup_py(self, file_path: Path) -> List[Dependency]:
        """Parse setup.py file (basic parsing)."""
        dependencies = []

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Look for install_requires
            install_requires_match = re.search(
                r'install_requires\s*=\s*\[(.*?)\]',
                content,
                re.DOTALL
            )

            if install_requires_match:
                requires_str = install_requires_match.group(1)
                # Extract quoted strings
                requirements = re.findall(r'["\']([^"\']+)["\']', requires_str)

                for req in requirements:
                    dep = self._parse_python_requirement(req, str(file_path))
                    if dep:
                        dependencies.append(dep)

        except Exception:
            pass  # Errors handled by caller

        return dependencies

    def _parse_pyproject_toml(self, file_path: Path) -> List[Dependency]:
        """Parse pyproject.toml file (basic parsing)."""
        dependencies = []

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Look for dependencies section
            # This is a simple regex-based parser, not a full TOML parser
            dep_section_match = re.search(
                r'dependencies\s*=\s*\[(.*?)\]',
                content,
                re.DOTALL
            )

            if dep_section_match:
                deps_str = dep_section_match.group(1)
                requirements = re.findall(r'["\']([^"\']+)["\']', deps_str)

                for req in requirements:
                    dep = self._parse_python_requirement(req, str(file_path))
                    if dep:
                        dependencies.append(dep)

        except Exception:
            pass  # Errors handled by caller

        return dependencies

    def _analyze_npm(self, project_path: Path) -> DependencyAnalysis:
        """Analyze npm/Node.js dependencies."""
        dependencies = []
        manifest_files = []
        errors = []

        # Parse package.json
        package_json = project_path / "package.json"
        if not package_json.exists():
            errors.append("package.json not found")
            return DependencyAnalysis(
                project_path=str(project_path),
                ecosystem=Ecosystem.NPM,
                total_dependencies=0,
                direct_dependencies=0,
                transitive_dependencies=0,
                dev_dependencies=0,
                errors=errors
            )

        manifest_files.append(str(package_json))

        try:
            with open(package_json, 'r') as f:
                data = json.load(f)

            # Parse dependencies
            if 'dependencies' in data:
                for name, version in data['dependencies'].items():
                    dependencies.append(Dependency(
                        name=name,
                        version=self._normalize_npm_version(version),
                        ecosystem=Ecosystem.NPM,
                        dependency_type=DependencyType.DIRECT,
                        spec=version,
                        source_file=str(package_json)
                    ))

            # Parse devDependencies
            if 'devDependencies' in data:
                for name, version in data['devDependencies'].items():
                    dependencies.append(Dependency(
                        name=name,
                        version=self._normalize_npm_version(version),
                        ecosystem=Ecosystem.NPM,
                        dependency_type=DependencyType.DEV,
                        spec=version,
                        source_file=str(package_json)
                    ))

            # Parse peerDependencies
            if 'peerDependencies' in data:
                for name, version in data['peerDependencies'].items():
                    dependencies.append(Dependency(
                        name=name,
                        version=self._normalize_npm_version(version),
                        ecosystem=Ecosystem.NPM,
                        dependency_type=DependencyType.DIRECT,
                        spec=version,
                        source_file=str(package_json)
                    ))

        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in package.json: {e}")
        except Exception as e:
            errors.append(f"Error parsing package.json: {e}")

        # Parse package-lock.json for transitive dependencies
        package_lock = project_path / "package-lock.json"
        if package_lock.exists():
            manifest_files.append(str(package_lock))
            try:
                transitive = self._parse_package_lock(package_lock, dependencies)
                dependencies.extend(transitive)
            except Exception as e:
                errors.append(f"Error parsing package-lock.json: {e}")

        # Count by type
        direct_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.DIRECT)
        transitive_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.TRANSITIVE)
        dev_count = sum(1 for d in dependencies if d.dependency_type == DependencyType.DEV)

        return DependencyAnalysis(
            project_path=str(project_path),
            ecosystem=Ecosystem.NPM,
            total_dependencies=len(dependencies),
            direct_dependencies=direct_count,
            transitive_dependencies=transitive_count,
            dev_dependencies=dev_count,
            dependencies=dependencies,
            manifest_files=manifest_files,
            errors=errors
        )

    def _normalize_npm_version(self, version: str) -> str:
        """Normalize npm version string."""
        # Remove semver prefixes
        version = version.lstrip('^~')
        # Remove 'v' prefix
        version = version.lstrip('v')
        return version

    def _parse_package_lock(self, file_path: Path, direct_deps: List[Dependency]) -> List[Dependency]:
        """Parse package-lock.json for transitive dependencies."""
        transitive_deps = []
        direct_names = {dep.name for dep in direct_deps}

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # package-lock.json v2+ format
            if 'packages' in data:
                packages = data['packages']
                for pkg_path, pkg_data in packages.items():
                    if not pkg_path or pkg_path == '':
                        continue  # Skip root

                    name = pkg_path.split('node_modules/')[-1]
                    if name in direct_names:
                        continue  # Skip direct dependencies

                    version = pkg_data.get('version', 'unknown')
                    transitive_deps.append(Dependency(
                        name=name,
                        version=version,
                        ecosystem=Ecosystem.NPM,
                        dependency_type=DependencyType.TRANSITIVE,
                        spec=version,
                        source_file=str(file_path)
                    ))

            # package-lock.json v1 format
            elif 'dependencies' in data:
                self._extract_transitive_deps_v1(
                    data['dependencies'],
                    direct_names,
                    transitive_deps,
                    str(file_path)
                )

        except Exception:
            pass  # Errors handled by caller

        return transitive_deps

    def _extract_transitive_deps_v1(
        self,
        deps: Dict,
        direct_names: Set[str],
        result: List[Dependency],
        source_file: str
    ):
        """Recursively extract transitive dependencies from v1 format."""
        for name, data in deps.items():
            if name not in direct_names:
                version = data.get('version', 'unknown')
                result.append(Dependency(
                    name=name,
                    version=version,
                    ecosystem=Ecosystem.NPM,
                    dependency_type=DependencyType.TRANSITIVE,
                    spec=version,
                    source_file=source_file
                ))

            # Recurse into nested dependencies
            if 'dependencies' in data:
                self._extract_transitive_deps_v1(
                    data['dependencies'],
                    direct_names,
                    result,
                    source_file
                )


def analyze_dependencies(project_path: str, ecosystem: Optional[str] = None) -> Dict:
    """
    Convenience function to analyze dependencies.

    Args:
        project_path: Path to project directory
        ecosystem: Specific ecosystem to analyze (python, npm, auto)

    Returns:
        Dictionary with analysis results
    """
    analyzer = DependencyAnalyzer()
    result = analyzer.analyze_project(project_path, ecosystem)

    return {
        'project_path': result.project_path,
        'ecosystem': result.ecosystem.value,
        'total_dependencies': result.total_dependencies,
        'direct_dependencies': result.direct_dependencies,
        'transitive_dependencies': result.transitive_dependencies,
        'dev_dependencies': result.dev_dependencies,
        'dependencies': [
            {
                'name': dep.name,
                'version': dep.version,
                'type': dep.dependency_type.value,
                'spec': dep.spec,
                'source_file': dep.source_file
            }
            for dep in result.dependencies
        ],
        'manifest_files': result.manifest_files,
        'errors': result.errors
    }
