"""
Documentation Analyzer

Analyzes code to identify documentation needs and quality.
"""

import ast
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any


class DocQuality(Enum):
    """Documentation quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    MISSING = "missing"


class IssueType(Enum):
    """Documentation issue types."""
    MISSING_DOCSTRING = "missing_docstring"
    INCOMPLETE_PARAMS = "incomplete_params"
    MISSING_RETURN = "missing_return"
    MISSING_RAISES = "missing_raises"
    MISSING_EXAMPLES = "missing_examples"
    OUTDATED = "outdated"
    TOO_SHORT = "too_short"
    NO_TYPE_HINTS = "no_type_hints"


@dataclass
class FunctionInfo:
    """Information about a function or method."""
    name: str
    line_number: int
    is_method: bool
    is_private: bool
    parameters: List[str]
    return_type: Optional[str]
    raises: List[str]
    complexity: int
    has_docstring: bool
    docstring: Optional[str] = None
    docstring_quality: DocQuality = DocQuality.MISSING
    type_hints: Dict[str, str] = field(default_factory=dict)


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    line_number: int
    base_classes: List[str]
    methods: List[FunctionInfo]
    attributes: List[str]
    has_docstring: bool
    docstring: Optional[str] = None
    docstring_quality: DocQuality = DocQuality.MISSING
    is_dataclass: bool = False


@dataclass
class ModuleInfo:
    """Information about a module."""
    file_path: str
    module_name: str
    has_docstring: bool
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[str]
    lines_of_code: int
    docstring: Optional[str] = None


@dataclass
class DocIssue:
    """Documentation quality issue."""
    issue_type: IssueType
    severity: str  # 'high', 'medium', 'low'
    location: str
    line_number: int
    description: str
    suggestion: str


@dataclass
class DocAnalysisResult:
    """Results of documentation analysis."""
    coverage_score: float
    quality_score: float
    modules_analyzed: int
    functions_analyzed: int
    classes_analyzed: int
    documented_functions: int
    documented_classes: int
    missing_docstrings: List[str]
    quality_issues: List[DocIssue]
    recommendations: List[str]
    module_info: List[ModuleInfo]


class DocumentationAnalyzer:
    """Analyzes code documentation coverage and quality."""

    def __init__(self):
        self.modules: List[ModuleInfo] = []
        self.issues: List[DocIssue] = []

    def analyze_project(self, project_path: str) -> DocAnalysisResult:
        """
        Analyze documentation for entire project.

        Args:
            project_path: Path to project root

        Returns:
            Analysis results with coverage and quality metrics
        """
        project_dir = Path(project_path)

        # Find all Python files
        python_files = list(project_dir.rglob("*.py"))
        python_files = [f for f in python_files if not self._should_skip(f)]

        # Analyze each file
        for file_path in python_files:
            module_info = self.analyze_file(str(file_path))
            if module_info:
                self.modules.append(module_info)

        return self._generate_results()

    def analyze_file(self, file_path: str) -> Optional[ModuleInfo]:
        """
        Analyze documentation for a single file.

        Args:
            file_path: Path to Python file

        Returns:
            Module information or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception:
            return None

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        # Extract module info
        module_name = Path(file_path).stem
        module_docstring = ast.get_docstring(tree)

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Analyze top-level functions and classes
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_info = self._analyze_function(node, file_path, False)
                functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node, file_path)
                classes.append(class_info)

        lines_of_code = len(source.splitlines())

        return ModuleInfo(
            file_path=file_path,
            module_name=module_name,
            has_docstring=module_docstring is not None,
            docstring=module_docstring,
            functions=functions,
            classes=classes,
            imports=imports,
            lines_of_code=lines_of_code
        )

    def _analyze_function(
        self,
        node: ast.FunctionDef,
        file_path: str,
        is_method: bool
    ) -> FunctionInfo:
        """Analyze a function or method."""
        # Get function name and line number
        name = node.name
        line_number = node.lineno
        is_private = name.startswith('_') and not name.startswith('__')

        # Get parameters
        parameters = [arg.arg for arg in node.args.args]

        # Get return type
        return_type = None
        if node.returns:
            return_type = ast.unparse(node.returns)

        # Get type hints
        type_hints = {}
        for arg in node.args.args:
            if arg.annotation:
                type_hints[arg.arg] = ast.unparse(arg.annotation)

        # Get docstring
        docstring = ast.get_docstring(node)
        has_docstring = docstring is not None

        # Analyze raises
        raises = self._extract_raises(node)

        # Calculate complexity
        complexity = self._calculate_complexity(node)

        # Assess docstring quality
        quality = self._assess_docstring_quality(
            docstring, parameters, return_type, raises
        )

        # Check for issues
        if not has_docstring:
            self.issues.append(DocIssue(
                issue_type=IssueType.MISSING_DOCSTRING,
                severity='high' if not is_private else 'medium',
                location=f"{Path(file_path).name}::{name}",
                line_number=line_number,
                description=f"Function '{name}' has no docstring",
                suggestion="Add comprehensive docstring with description, parameters, and return value"
            ))
        elif quality in [DocQuality.POOR, DocQuality.FAIR]:
            self._check_docstring_completeness(
                name, file_path, line_number, docstring, parameters, return_type, raises
            )

        return FunctionInfo(
            name=name,
            line_number=line_number,
            is_method=is_method,
            is_private=is_private,
            parameters=parameters,
            return_type=return_type,
            raises=raises,
            complexity=complexity,
            has_docstring=has_docstring,
            docstring=docstring,
            docstring_quality=quality,
            type_hints=type_hints
        )

    def _analyze_class(self, node: ast.ClassDef, file_path: str) -> ClassInfo:
        """Analyze a class."""
        name = node.name
        line_number = node.lineno

        # Get base classes
        base_classes = [ast.unparse(base) for base in node.bases]

        # Check if it's a dataclass
        is_dataclass = any(
            isinstance(d, ast.Name) and d.id == 'dataclass'
            for d in node.decorator_list
        )

        # Get attributes
        attributes = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attributes.append(item.target.id)

        # Analyze methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_function(item, file_path, True)
                methods.append(method_info)

        # Get docstring
        docstring = ast.get_docstring(node)
        has_docstring = docstring is not None

        # Assess quality
        quality = self._assess_class_docstring_quality(
            docstring, attributes, methods
        )

        # Check for issues
        if not has_docstring:
            self.issues.append(DocIssue(
                issue_type=IssueType.MISSING_DOCSTRING,
                severity='high',
                location=f"{Path(file_path).name}::{name}",
                line_number=line_number,
                description=f"Class '{name}' has no docstring",
                suggestion="Add class docstring describing purpose and attributes"
            ))

        return ClassInfo(
            name=name,
            line_number=line_number,
            base_classes=base_classes,
            methods=methods,
            attributes=attributes,
            has_docstring=has_docstring,
            docstring=docstring,
            docstring_quality=quality,
            is_dataclass=is_dataclass
        )

    def _extract_raises(self, node: ast.FunctionDef) -> List[str]:
        """Extract exceptions that function can raise."""
        raises = []

        for item in ast.walk(node):
            if isinstance(item, ast.Raise):
                if item.exc:
                    if isinstance(item.exc, ast.Call):
                        if isinstance(item.exc.func, ast.Name):
                            raises.append(item.exc.func.id)
                    elif isinstance(item.exc, ast.Name):
                        raises.append(item.exc.id)

        return list(set(raises))

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1

        for item in ast.walk(node):
            if isinstance(item, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(item, ast.BoolOp):
                complexity += len(item.values) - 1

        return complexity

    def _assess_docstring_quality(
        self,
        docstring: Optional[str],
        parameters: List[str],
        return_type: Optional[str],
        raises: List[str]
    ) -> DocQuality:
        """Assess the quality of a docstring."""
        if not docstring:
            return DocQuality.MISSING

        # Remove 'self' and 'cls' from parameters
        params_to_check = [p for p in parameters if p not in ('self', 'cls')]

        docstring_lower = docstring.lower()

        # Check length
        if len(docstring) < 10:
            return DocQuality.POOR

        # Count documented elements
        score = 0
        max_score = 0

        # Check description (always needed)
        max_score += 2
        if len(docstring.split('\n')[0]) > 20:
            score += 2
        elif len(docstring) > 10:
            score += 1

        # Check parameters
        if params_to_check:
            max_score += 2
            params_documented = sum(
                1 for p in params_to_check
                if p.lower() in docstring_lower
            )
            if params_documented == len(params_to_check):
                score += 2
            elif params_documented > 0:
                score += 1

        # Check return documentation
        if return_type or 'return' in docstring_lower:
            max_score += 1
            if 'return' in docstring_lower:
                score += 1

        # Check raises documentation
        if raises:
            max_score += 1
            if 'raise' in docstring_lower or 'except' in docstring_lower:
                score += 1

        # Calculate quality
        if max_score == 0:
            return DocQuality.GOOD

        percentage = (score / max_score) * 100

        if percentage >= 90:
            return DocQuality.EXCELLENT
        elif percentage >= 70:
            return DocQuality.GOOD
        elif percentage >= 50:
            return DocQuality.FAIR
        else:
            return DocQuality.POOR

    def _assess_class_docstring_quality(
        self,
        docstring: Optional[str],
        attributes: List[str],
        methods: List[FunctionInfo]
    ) -> DocQuality:
        """Assess the quality of a class docstring."""
        if not docstring:
            return DocQuality.MISSING

        if len(docstring) < 10:
            return DocQuality.POOR

        docstring_lower = docstring.lower()

        # Check if attributes are documented
        if attributes:
            attrs_documented = sum(
                1 for a in attributes
                if a.lower() in docstring_lower
            )
            if attrs_documented == len(attributes):
                return DocQuality.EXCELLENT
            elif attrs_documented > len(attributes) / 2:
                return DocQuality.GOOD
            elif attrs_documented > 0:
                return DocQuality.FAIR
            else:
                return DocQuality.POOR

        # For classes without attributes, check description length
        if len(docstring) > 50:
            return DocQuality.GOOD
        else:
            return DocQuality.FAIR

    def _check_docstring_completeness(
        self,
        name: str,
        file_path: str,
        line_number: int,
        docstring: str,
        parameters: List[str],
        return_type: Optional[str],
        raises: List[str]
    ):
        """Check if docstring is complete and add issues."""
        params_to_check = [p for p in parameters if p not in ('self', 'cls')]
        docstring_lower = docstring.lower()

        # Check parameters
        if params_to_check:
            missing_params = [
                p for p in params_to_check
                if p.lower() not in docstring_lower
            ]
            if missing_params:
                self.issues.append(DocIssue(
                    issue_type=IssueType.INCOMPLETE_PARAMS,
                    severity='medium',
                    location=f"{Path(file_path).name}::{name}",
                    line_number=line_number,
                    description=f"Parameters not documented: {', '.join(missing_params)}",
                    suggestion="Add parameter documentation in docstring"
                ))

        # Check return
        if return_type and 'return' not in docstring_lower:
            self.issues.append(DocIssue(
                issue_type=IssueType.MISSING_RETURN,
                severity='medium',
                location=f"{Path(file_path).name}::{name}",
                line_number=line_number,
                description="Return value not documented",
                suggestion="Add return value documentation"
            ))

        # Check raises
        if raises and 'raise' not in docstring_lower:
            self.issues.append(DocIssue(
                issue_type=IssueType.MISSING_RAISES,
                severity='low',
                location=f"{Path(file_path).name}::{name}",
                line_number=line_number,
                description=f"Exceptions not documented: {', '.join(raises)}",
                suggestion="Document exceptions that can be raised"
            ))

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'__pycache__', '.git', 'venv', 'env', 'node_modules', '.tox'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)

    def _generate_results(self) -> DocAnalysisResult:
        """Generate analysis results."""
        total_functions = 0
        documented_functions = 0
        total_classes = 0
        documented_classes = 0
        missing_docstrings = []

        for module in self.modules:
            # Module-level docstring
            if not module.has_docstring:
                missing_docstrings.append(f"{Path(module.file_path).name} (module)")

            # Functions
            for func in module.functions:
                total_functions += 1
                if func.has_docstring:
                    documented_functions += 1
                else:
                    missing_docstrings.append(f"{Path(module.file_path).name}::{func.name}")

            # Classes
            for cls in module.classes:
                total_classes += 1
                if cls.has_docstring:
                    documented_classes += 1
                else:
                    missing_docstrings.append(f"{Path(module.file_path).name}::{cls.name}")

                # Class methods
                for method in cls.methods:
                    total_functions += 1
                    if method.has_docstring:
                        documented_functions += 1
                    else:
                        missing_docstrings.append(
                            f"{Path(module.file_path).name}::{cls.name}.{method.name}"
                        )

        # Calculate coverage score
        total_items = len(self.modules) + total_functions + total_classes
        documented_items = (
            sum(1 for m in self.modules if m.has_docstring) +
            documented_functions +
            documented_classes
        )

        coverage_score = 0.0
        if total_items > 0:
            coverage_score = (documented_items / total_items) * 100

        # Calculate quality score based on issues
        quality_score = 100.0
        for issue in self.issues:
            if issue.severity == 'high':
                quality_score -= 5
            elif issue.severity == 'medium':
                quality_score -= 2
            elif issue.severity == 'low':
                quality_score -= 1

        quality_score = max(0.0, quality_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            coverage_score, len(missing_docstrings)
        )

        return DocAnalysisResult(
            coverage_score=coverage_score,
            quality_score=quality_score,
            modules_analyzed=len(self.modules),
            functions_analyzed=total_functions,
            classes_analyzed=total_classes,
            documented_functions=documented_functions,
            documented_classes=documented_classes,
            missing_docstrings=missing_docstrings,
            quality_issues=self.issues,
            recommendations=recommendations,
            module_info=self.modules
        )

    def _generate_recommendations(
        self,
        coverage_score: float,
        missing_count: int
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if coverage_score < 50:
            recommendations.append(
                "📚 Documentation coverage is critically low - prioritize adding docstrings"
            )
        elif coverage_score < 80:
            recommendations.append(
                "📝 Improve documentation coverage by adding missing docstrings"
            )

        if missing_count > 0:
            recommendations.append(
                f"🎯 Add docstrings to {missing_count} undocumented items"
            )

        # Issue-based recommendations
        issue_types = {}
        for issue in self.issues:
            issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

        if IssueType.INCOMPLETE_PARAMS in issue_types:
            recommendations.append(
                f"📋 Document parameters for {issue_types[IssueType.INCOMPLETE_PARAMS]} functions"
            )

        if IssueType.MISSING_RETURN in issue_types:
            recommendations.append(
                f"↩️  Add return value documentation for {issue_types[IssueType.MISSING_RETURN]} functions"
            )

        if not recommendations:
            recommendations.append("✅ Documentation quality is excellent - keep it up!")

        return recommendations


def analyze_documentation(project_path: str) -> Dict[str, Any]:
    """
    Analyze documentation coverage and quality for a project.

    Args:
        project_path: Path to project root directory

    Returns:
        Dictionary with analysis results including coverage score,
        quality issues, and recommendations
    """
    analyzer = DocumentationAnalyzer()
    result = analyzer.analyze_project(project_path)

    return {
        'coverage_score': result.coverage_score,
        'quality_score': result.quality_score,
        'statistics': {
            'modules_analyzed': result.modules_analyzed,
            'functions_analyzed': result.functions_analyzed,
            'classes_analyzed': result.classes_analyzed,
            'documented_functions': result.documented_functions,
            'documented_classes': result.documented_classes,
        },
        'missing_docstrings': result.missing_docstrings,
        'quality_issues': [
            {
                'type': issue.issue_type.value,
                'severity': issue.severity,
                'location': issue.location,
                'line_number': issue.line_number,
                'description': issue.description,
                'suggestion': issue.suggestion
            }
            for issue in result.quality_issues
        ],
        'recommendations': result.recommendations
    }
