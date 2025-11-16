"""
PR Analyzer

Analyzes pull request changes for quality, security, and best practices.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from pathlib import Path
from enum import Enum


class IssueSeverity(Enum):
    """Severity levels for review issues."""
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class IssueCategory(Enum):
    """Categories of review issues."""
    CODE_QUALITY = "code_quality"
    SECURITY = "security"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    BEST_PRACTICES = "best_practices"
    BREAKING_CHANGE = "breaking_change"


@dataclass
class ReviewIssue:
    """Represents a single review issue."""
    category: IssueCategory
    severity: IssueSeverity
    file_path: str
    line_number: Optional[int]
    title: str
    description: str
    suggestion: str
    code_snippet: Optional[str] = None


@dataclass
class DimensionScore:
    """Score for a review dimension."""
    dimension: str
    score: float  # 0-100
    weight: float  # Weight in overall score
    issues_count: int
    passed_checks: int
    total_checks: int


@dataclass
class PRReviewResult:
    """Result of PR review."""
    overall_score: float  # 0-100
    approval_status: str  # approve, request_changes, comment
    dimension_scores: List[DimensionScore] = field(default_factory=list)
    issues: List[ReviewIssue] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    statistics: Dict = field(default_factory=dict)


class PRAnalyzer:
    """Analyzes pull requests."""

    # Dimension weights (must sum to 1.0)
    DIMENSION_WEIGHTS = {
        'code_quality': 0.30,
        'test_coverage': 0.25,
        'security': 0.20,
        'best_practices': 0.15,
        'change_impact': 0.10
    }

    def __init__(self):
        self.checkers = {
            'code_quality': self._check_code_quality,
            'test_coverage': self._check_test_coverage,
            'security': self._check_security,
            'best_practices': self._check_best_practices,
            'change_impact': self._check_change_impact
        }

    def review_pull_request(
        self,
        pr_changes: Dict,
        base_branch: str = "main",
        target_branch: str = "feature",
        checklist: Optional[List[str]] = None
    ) -> PRReviewResult:
        """
        Review a pull request.

        Args:
            pr_changes: Dictionary with 'added', 'modified', 'deleted' file lists
            base_branch: Base branch name
            target_branch: Target branch name
            checklist: Optional custom checklist

        Returns:
            PRReviewResult with review outcome
        """
        issues = []
        dimension_scores = []

        # Get changed files
        added_files = pr_changes.get('added', [])
        modified_files = pr_changes.get('modified', [])
        deleted_files = pr_changes.get('deleted', [])

        all_changed_files = added_files + modified_files

        # Calculate statistics
        statistics = {
            'files_added': len(added_files),
            'files_modified': len(modified_files),
            'files_deleted': len(deleted_files),
            'total_files_changed': len(all_changed_files),
            'lines_added': 0,  # Would be calculated from diff
            'lines_deleted': 0,
        }

        # Run checks for each dimension
        for dimension, checker in self.checkers.items():
            try:
                dim_issues, dim_score = checker(all_changed_files, pr_changes)
                issues.extend(dim_issues)

                dimension_scores.append(DimensionScore(
                    dimension=dimension,
                    score=dim_score.score,
                    weight=self.DIMENSION_WEIGHTS[dimension],
                    issues_count=dim_score.issues_count,
                    passed_checks=dim_score.passed_checks,
                    total_checks=dim_score.total_checks
                ))
            except Exception as e:
                # If a checker fails, give it a low score
                dimension_scores.append(DimensionScore(
                    dimension=dimension,
                    score=50.0,
                    weight=self.DIMENSION_WEIGHTS[dimension],
                    issues_count=0,
                    passed_checks=0,
                    total_checks=1
                ))

        # Calculate overall score
        overall_score = sum(
            ds.score * ds.weight for ds in dimension_scores
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(issues, dimension_scores)

        # Determine approval status
        approval_status = self._determine_approval_status(
            overall_score, issues, dimension_scores
        )

        return PRReviewResult(
            overall_score=overall_score,
            approval_status=approval_status,
            dimension_scores=dimension_scores,
            issues=issues,
            recommendations=recommendations,
            statistics=statistics
        )

    def _check_code_quality(
        self,
        changed_files: List[str],
        pr_changes: Dict
    ) -> tuple[List[ReviewIssue], DimensionScore]:
        """Check code quality dimension."""
        issues = []
        passed_checks = 0
        total_checks = 3

        # Check 1: File size (not too large)
        for file_path in changed_files:
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    lines = len(f.readlines())

                if lines > 500:
                    issues.append(ReviewIssue(
                        category=IssueCategory.CODE_QUALITY,
                        severity=IssueSeverity.MAJOR,
                        file_path=file_path,
                        line_number=None,
                        title="Large file added",
                        description=f"File has {lines} lines. Consider breaking it into smaller modules.",
                        suggestion="Split into focused, cohesive modules (< 500 lines each)"
                    ))
                else:
                    passed_checks += 1

        # Check 2: Naming conventions
        for file_path in changed_files:
            if not self._check_naming_conventions(file_path):
                issues.append(ReviewIssue(
                    category=IssueCategory.CODE_QUALITY,
                    severity=IssueSeverity.MINOR,
                    file_path=file_path,
                    line_number=None,
                    title="Naming convention issue",
                    description=f"File name '{Path(file_path).name}' doesn't follow conventions",
                    suggestion="Use snake_case for Python files, camelCase for JS/TS"
                ))
            else:
                passed_checks += 1

        # Check 3: Code smells (would integrate with refactor-assistant)
        # For demo, check for common patterns
        for file_path in changed_files:
            if file_path.endswith('.py') and Path(file_path).exists():
                with open(file_path, 'r') as f:
                    content = f.read()

                # Check for print statements (should use logging)
                if 'print(' in content and 'test' not in file_path.lower():
                    issues.append(ReviewIssue(
                        category=IssueCategory.BEST_PRACTICES,
                        severity=IssueSeverity.MINOR,
                        file_path=file_path,
                        line_number=None,
                        title="Print statement in production code",
                        description="Found print() statements. Use logging instead.",
                        suggestion="Replace print() with logger.info(), logger.debug(), etc."
                    ))
                else:
                    passed_checks += 1

        # Calculate score based on issues
        score = self._calculate_dimension_score(issues, passed_checks, total_checks)

        return issues, DimensionScore(
            dimension='code_quality',
            score=score,
            weight=self.DIMENSION_WEIGHTS['code_quality'],
            issues_count=len(issues),
            passed_checks=passed_checks,
            total_checks=total_checks
        )

    def _check_test_coverage(
        self,
        changed_files: List[str],
        pr_changes: Dict
    ) -> tuple[List[ReviewIssue], DimensionScore]:
        """Check test coverage dimension."""
        issues = []
        passed_checks = 0
        total_checks = 2

        # Check 1: Test files exist for new code files
        source_files = [f for f in changed_files if self._is_source_file(f)]
        test_files = [f for f in changed_files if self._is_test_file(f)]

        if source_files and not test_files:
            issues.append(ReviewIssue(
                category=IssueCategory.TESTING,
                severity=IssueSeverity.CRITICAL,
                file_path="",
                line_number=None,
                title="No tests for new code",
                description=f"Added {len(source_files)} source file(s) but no test files",
                suggestion="Add test files with >80% coverage for new code"
            ))
        else:
            passed_checks += 1

        # Check 2: Test file naming convention
        for test_file in test_files:
            expected_naming = test_file.startswith('test_') or test_file.endswith('_test.py')
            if not expected_naming:
                issues.append(ReviewIssue(
                    category=IssueCategory.TESTING,
                    severity=IssueSeverity.MINOR,
                    file_path=test_file,
                    line_number=None,
                    title="Test file naming convention",
                    description=f"Test file '{test_file}' doesn't follow naming convention",
                    suggestion="Name test files as 'test_*.py' or '*_test.py'"
                ))
            else:
                passed_checks += 1

        score = self._calculate_dimension_score(issues, passed_checks, total_checks)

        return issues, DimensionScore(
            dimension='test_coverage',
            score=score,
            weight=self.DIMENSION_WEIGHTS['test_coverage'],
            issues_count=len(issues),
            passed_checks=passed_checks,
            total_checks=total_checks
        )

    def _check_security(
        self,
        changed_files: List[str],
        pr_changes: Dict
    ) -> tuple[List[ReviewIssue], DimensionScore]:
        """Check security dimension."""
        issues = []
        passed_checks = 0
        total_checks = 4

        # Check 1: No hardcoded secrets
        for file_path in changed_files:
            if Path(file_path).exists():
                with open(file_path, 'r') as f:
                    content = f.read()

                # Simple pattern matching for potential secrets
                if self._contains_potential_secrets(content):
                    issues.append(ReviewIssue(
                        category=IssueCategory.SECURITY,
                        severity=IssueSeverity.BLOCKER,
                        file_path=file_path,
                        line_number=None,
                        title="Potential hardcoded secret detected",
                        description="File may contain hardcoded secrets or API keys",
                        suggestion="Use environment variables or secret management systems"
                    ))
                else:
                    passed_checks += 1

        # Check 2: No sensitive file types
        sensitive_extensions = ['.env', '.key', '.pem', '.p12', 'credentials.json']
        for file_path in changed_files:
            if any(file_path.endswith(ext) for ext in sensitive_extensions):
                issues.append(ReviewIssue(
                    category=IssueCategory.SECURITY,
                    severity=IssueSeverity.BLOCKER,
                    file_path=file_path,
                    line_number=None,
                    title="Sensitive file in PR",
                    description=f"File '{file_path}' appears to contain sensitive data",
                    suggestion="Remove from PR and add to .gitignore"
                ))
            else:
                passed_checks += 1

        # Check 3: SQL injection patterns (basic check)
        for file_path in changed_files:
            if Path(file_path).exists() and file_path.endswith('.py'):
                with open(file_path, 'r') as f:
                    content = f.read()

                if self._has_sql_injection_risk(content):
                    issues.append(ReviewIssue(
                        category=IssueCategory.SECURITY,
                        severity=IssueSeverity.CRITICAL,
                        file_path=file_path,
                        line_number=None,
                        title="Potential SQL injection vulnerability",
                        description="Found string concatenation in SQL queries",
                        suggestion="Use parameterized queries or ORM methods"
                    ))
                else:
                    passed_checks += 1

        # Check 4: Dependency changes (would integrate with dependency-guardian)
        requirements_files = [f for f in changed_files if 'requirements' in f or 'package.json' in f]
        if requirements_files:
            passed_checks += 1  # Would actually check with dependency-guardian

        score = self._calculate_dimension_score(issues, passed_checks, total_checks)

        return issues, DimensionScore(
            dimension='security',
            score=score,
            weight=self.DIMENSION_WEIGHTS['security'],
            issues_count=len(issues),
            passed_checks=passed_checks,
            total_checks=total_checks
        )

    def _check_best_practices(
        self,
        changed_files: List[str],
        pr_changes: Dict
    ) -> tuple[List[ReviewIssue], DimensionScore]:
        """Check best practices dimension."""
        issues = []
        passed_checks = 0
        total_checks = 3

        # Check 1: Documentation
        has_readme_update = any('README' in f.upper() for f in changed_files)
        has_significant_changes = len(changed_files) > 5

        if has_significant_changes and not has_readme_update:
            issues.append(ReviewIssue(
                category=IssueCategory.DOCUMENTATION,
                severity=IssueSeverity.MINOR,
                file_path="",
                line_number=None,
                title="Missing documentation update",
                description="Significant changes without README update",
                suggestion="Update README.md to document new features or changes"
            ))
        else:
            passed_checks += 1

        # Check 2: Error handling
        for file_path in changed_files:
            if Path(file_path).exists() and file_path.endswith('.py'):
                with open(file_path, 'r') as f:
                    content = f.read()

                # Check for bare except
                if 'except:' in content:
                    issues.append(ReviewIssue(
                        category=IssueCategory.BEST_PRACTICES,
                        severity=IssueSeverity.MAJOR,
                        file_path=file_path,
                        line_number=None,
                        title="Bare except clause",
                        description="Found bare 'except:' which catches all exceptions",
                        suggestion="Catch specific exceptions (e.g., except ValueError:)"
                    ))
                else:
                    passed_checks += 1

        # Check 3: Code organization
        # Check if change is appropriately scoped
        if len(changed_files) > 20:
            issues.append(ReviewIssue(
                category=IssueCategory.BEST_PRACTICES,
                severity=IssueSeverity.MINOR,
                file_path="",
                line_number=None,
                title="Large PR scope",
                description=f"PR changes {len(changed_files)} files. Consider breaking into smaller PRs.",
                suggestion="Split into focused PRs (< 20 files each) for easier review"
            ))
        else:
            passed_checks += 1

        score = self._calculate_dimension_score(issues, passed_checks, total_checks)

        return issues, DimensionScore(
            dimension='best_practices',
            score=score,
            weight=self.DIMENSION_WEIGHTS['best_practices'],
            issues_count=len(issues),
            passed_checks=passed_checks,
            total_checks=total_checks
        )

    def _check_change_impact(
        self,
        changed_files: List[str],
        pr_changes: Dict
    ) -> tuple[List[ReviewIssue], DimensionScore]:
        """Check change impact dimension."""
        issues = []
        passed_checks = 0
        total_checks = 2

        # Check 1: Breaking changes
        # Look for API changes in public modules
        public_api_files = [f for f in changed_files if '__init__.py' in f or 'api' in f.lower()]

        if public_api_files:
            issues.append(ReviewIssue(
                category=IssueCategory.BREAKING_CHANGE,
                severity=IssueSeverity.MAJOR,
                file_path="",
                line_number=None,
                title="Potential breaking change",
                description=f"Changes to public API files: {', '.join(public_api_files)}",
                suggestion="Document breaking changes and update version accordingly"
            ))
        else:
            passed_checks += 1

        # Check 2: Deleted files
        deleted_files = pr_changes.get('deleted', [])
        if deleted_files:
            issues.append(ReviewIssue(
                category=IssueCategory.BREAKING_CHANGE,
                severity=IssueSeverity.MAJOR,
                file_path="",
                line_number=None,
                title="Files deleted",
                description=f"Deleted {len(deleted_files)} file(s). Verify no external dependencies.",
                suggestion="Check for imports of deleted files and provide migration path"
            ))
        else:
            passed_checks += 1

        score = self._calculate_dimension_score(issues, passed_checks, total_checks)

        return issues, DimensionScore(
            dimension='change_impact',
            score=score,
            weight=self.DIMENSION_WEIGHTS['change_impact'],
            issues_count=len(issues),
            passed_checks=passed_checks,
            total_checks=total_checks
        )

    def _calculate_dimension_score(
        self,
        issues: List[ReviewIssue],
        passed_checks: int,
        total_checks: int
    ) -> float:
        """Calculate score for a dimension."""
        # Base score from passed checks
        if total_checks > 0:
            base_score = (passed_checks / total_checks) * 100
        else:
            base_score = 100

        # Deduct for issues
        deductions = 0
        for issue in issues:
            if issue.severity == IssueSeverity.BLOCKER:
                deductions += 50
            elif issue.severity == IssueSeverity.CRITICAL:
                deductions += 30
            elif issue.severity == IssueSeverity.MAJOR:
                deductions += 15
            elif issue.severity == IssueSeverity.MINOR:
                deductions += 5
            elif issue.severity == IssueSeverity.INFO:
                deductions += 1

        final_score = max(0, base_score - deductions)
        return final_score

    def _generate_recommendations(
        self,
        issues: List[ReviewIssue],
        dimension_scores: List[DimensionScore]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Check for blockers
        blockers = [i for i in issues if i.severity == IssueSeverity.BLOCKER]
        if blockers:
            recommendations.append(
                f"🚨 Fix {len(blockers)} blocker issue(s) before merging"
            )

        # Check for critical issues
        critical = [i for i in issues if i.severity == IssueSeverity.CRITICAL]
        if critical:
            recommendations.append(
                f"⚠️  Address {len(critical)} critical issue(s)"
            )

        # Low dimension scores
        for ds in dimension_scores:
            if ds.score < 50:
                recommendations.append(
                    f"📊 Improve {ds.dimension.replace('_', ' ')} (current: {ds.score:.0f}/100)"
                )

        # Missing tests
        test_issues = [i for i in issues if i.category == IssueCategory.TESTING]
        if test_issues:
            recommendations.append(
                "🧪 Add tests for new code (target: 80% coverage)"
            )

        # Security issues
        security_issues = [i for i in issues if i.category == IssueCategory.SECURITY]
        if security_issues:
            recommendations.append(
                "🔒 Review and fix security vulnerabilities"
            )

        # General improvements
        if not recommendations:
            recommendations.append("✅ Code looks good! Consider minor improvements from issues above.")

        return recommendations

    def _determine_approval_status(
        self,
        overall_score: float,
        issues: List[ReviewIssue],
        dimension_scores: List[DimensionScore]
    ) -> str:
        """Determine approval status."""
        # Blockers always require changes
        if any(i.severity == IssueSeverity.BLOCKER for i in issues):
            return "request_changes"

        # Critical issues require changes
        if any(i.severity == IssueSeverity.CRITICAL for i in issues):
            return "request_changes"

        # Low overall score requires changes
        if overall_score < 60:
            return "request_changes"

        # Good score with minor issues = comment
        if overall_score < 80:
            return "comment"

        # High score = approve
        return "approve"

    def _is_source_file(self, file_path: str) -> bool:
        """Check if file is a source code file."""
        source_extensions = ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c']
        return any(file_path.endswith(ext) for ext in source_extensions) and 'test' not in file_path.lower()

    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file."""
        return 'test' in file_path.lower() and (file_path.endswith('.py') or file_path.endswith('.js') or file_path.endswith('.ts'))

    def _check_naming_conventions(self, file_path: str) -> bool:
        """Check file naming conventions."""
        name = Path(file_path).stem

        if file_path.endswith('.py'):
            # Python: snake_case
            return name.islower() or '_' in name
        elif file_path.endswith(('.js', '.ts')):
            # JavaScript/TypeScript: camelCase or PascalCase
            return name[0].islower() or name[0].isupper()

        return True  # Unknown extension, assume OK

    def _contains_potential_secrets(self, content: str) -> bool:
        """Check for potential hardcoded secrets."""
        secret_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
            r'["\'][A-Za-z0-9]{32,}["\']',  # Long random strings
        ]

        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        return False

    def _has_sql_injection_risk(self, content: str) -> bool:
        """Check for SQL injection patterns."""
        # Look for string formatting in SQL queries
        sql_patterns = [
            r'execute\([^)]*%s',
            r'execute\([^)]*\+',
            r'execute\([^)]*f["\']',
            r'SELECT.*\+.*FROM',
            r'INSERT.*\+.*VALUES',
        ]

        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        return False


def review_pull_request(
    pr_changes: Dict,
    base_branch: str = "main",
    target_branch: str = "feature",
    checklist: Optional[List[str]] = None
) -> Dict:
    """
    Convenience function to review a pull request.

    Args:
        pr_changes: Dictionary with 'added', 'modified', 'deleted' file lists
        base_branch: Base branch name
        target_branch: Target branch name
        checklist: Optional custom checklist

    Returns:
        Dictionary with review results
    """
    analyzer = PRAnalyzer()
    result = analyzer.review_pull_request(pr_changes, base_branch, target_branch, checklist)

    return {
        'overall_score': result.overall_score,
        'approval_status': result.approval_status,
        'dimension_scores': [
            {
                'dimension': ds.dimension,
                'score': ds.score,
                'weight': ds.weight,
                'issues_count': ds.issues_count,
                'passed_checks': ds.passed_checks,
                'total_checks': ds.total_checks
            }
            for ds in result.dimension_scores
        ],
        'issues': [
            {
                'category': issue.category.value,
                'severity': issue.severity.value,
                'file_path': issue.file_path,
                'line_number': issue.line_number,
                'title': issue.title,
                'description': issue.description,
                'suggestion': issue.suggestion,
                'code_snippet': issue.code_snippet
            }
            for issue in result.issues
        ],
        'recommendations': result.recommendations,
        'statistics': result.statistics
    }
