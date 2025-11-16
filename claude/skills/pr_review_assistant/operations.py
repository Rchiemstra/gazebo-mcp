"""
PR Review Assistant Operations

Standardized operations interface for agent invocation.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time

# Import core functions
from .core.pr_analyzer import review_pull_request as _review_pull_request
from .core.comment_generator import generate_review_comment as _generate_review_comment


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def review_pull_request(
    pr_changes: Dict[str, Any],
    base_branch: str = "main",
    target_branch: str = "feature",
    checklist: Optional[List[str]] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Perform comprehensive pull request review.

    Args:
        pr_changes: Dictionary with 'added', 'modified', 'deleted' file lists
        base_branch: Base branch name (default: main)
        target_branch: Target branch name (default: feature)
        checklist: Optional custom review checklist
        response_format: "summary" (overview) or "detailed" (all review comments)
        **kwargs: Additional parameters

    Returns:
        OperationResult with review results

    Token Efficiency:
        - Use response_format="summary" for high-level review results
        - Use response_format="detailed" for all comments and suggestions
        - Summary mode saves 85-95% tokens for large PRs
    """
    start_time = time.time()

    try:
        result = _review_pull_request(
            pr_changes=pr_changes,
            base_branch=base_branch,
            target_branch=target_branch,
            checklist=checklist
        )

        duration = time.time() - start_time

        # Build response based on format
        if response_format == "summary":
            comments = result.get('comments', [])
            data = {
                "total_comments": len(comments),
                "by_category": {},
                "by_severity": {},
                "overall_score": result.get('overall_score'),
                "recommendation": result.get('recommendation'),
                "files_reviewed": len(pr_changes.get('added', [])) + len(pr_changes.get('modified', [])),
                "efficiency_tip": (
                    f"Reviewed {len(pr_changes.get('added', [])) + len(pr_changes.get('modified', []))} files, found {len(comments)} comments. "
                    f"Using summary mode for efficiency. For all review comments:\n"
                    f"review_pull_request(pr_changes, response_format='detailed')"
                )
            }
            # Count by category and severity
            for comment in comments:
                cat = comment.get('category', 'general')
                sev = comment.get('severity', 'info')
                data["by_category"][cat] = data["by_category"].get(cat, 0) + 1
                data["by_severity"][sev] = data["by_severity"].get(sev, 0) + 1
        else:
            # Detailed format - include everything
            data = result

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "pr-review-assistant",
                "operation": "review_pull_request",
                "version": "0.1.0",
                "base_branch": base_branch,
                "target_branch": target_branch,
                "files_reviewed": len(pr_changes.get('added', [])) + len(pr_changes.get('modified', [])),
                "response_format": response_format
            }
        )

    except KeyError as e:
        return OperationResult(
            success=False,
            error=f"Invalid pr_changes format: missing required key {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "pr_changes must be a dict with 'added', 'modified', and 'deleted' keys",
                    "Each key should contain a list of file paths",
                    "Use Bash('git diff --name-status') to get file changes",
                    "Example format: {'added': ['file1.py'], 'modified': ['file2.py'], 'deleted': []}"
                ],
                "example_fix": "review_pull_request({'added': ['src/new.py'], 'modified': ['src/old.py'], 'deleted': []})"
            }
        )
    except FileNotFoundError as e:
        return OperationResult(
            success=False,
            error=f"Cannot find file in PR changes: {str(e)}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure all files in pr_changes exist in the repository",
                    "Use Bash('git status') to see actual changed files",
                    "Verify file paths are relative to repository root",
                    "Check if files were properly staged/committed"
                ],
                "example_fix": "review_pull_request({'added': ['src/actual_file.py'], 'modified': [], 'deleted': []})"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"PR review failed: {str(e)}",
            error_code="REVIEW_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if pr_changes dict is properly formatted",
                    "Verify all file paths exist and are readable",
                    "Try with a smaller changeset first to isolate the issue",
                    "Ensure base_branch and target_branch are valid branch names"
                ],
                "example_fix": "review_pull_request({'added': [], 'modified': ['simple.py'], 'deleted': []}, base_branch='main')"
            }
        )


def generate_review_comment(
    review_result: Dict[str, Any],
    format: str = "github",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Generate formatted review comment from review results.

    Args:
        review_result: Result from review_pull_request operation
        format: Output format (github, gitlab, markdown)
        response_format: "summary" (brief) or "detailed" (with metadata)
        **kwargs: Additional parameters

    Returns:
        OperationResult with formatted comment

    Token Efficiency:
        - Use response_format="summary" for just the formatted comment
        - Use response_format="detailed" for comment plus statistics and metadata
    """
    start_time = time.time()

    try:
        comment = _generate_review_comment(
            review_result=review_result,
            format=format
        )

        duration = time.time() - start_time

        data = {
            "comment": comment,
            "format": format
        }

        if response_format == "detailed":
            data.update({
                "length": len(comment),
                "overall_score": review_result.get('overall_score', 0),
                "issues_count": review_result.get('issues_count', 0),
                "files_reviewed": review_result.get('files_reviewed', 0)
            })

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "pr-review-assistant",
                "operation": "generate_review_comment",
                "version": "0.1.0",
                "format": format
            }
        )

    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid format or review result: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Valid formats are: 'github', 'gitlab', 'markdown'",
                    "Ensure review_result is from review_pull_request operation",
                    "Check that review_result contains required fields",
                    "Verify format parameter is a string"
                ],
                "example_fix": "generate_review_comment(review_result, format='github')"
            }
        )
    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Comment generation failed: {str(e)}",
            error_code="GENERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure review_result has valid structure",
                    "Try with format='markdown' for simpler output",
                    "Verify review_result contains comments and overall_score",
                    "Check if review_result is from a successful review operation"
                ],
                "example_fix": "generate_review_comment(review_result, format='markdown')"
            }
        )


def analyze_change_impact(
    pr_changes: Dict[str, Any],
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze the impact of PR changes.

    Args:
        pr_changes: Dictionary with 'added', 'modified', 'deleted' file lists
        response_format: "summary" (metrics only) or "detailed" (with file lists)
        **kwargs: Additional parameters

    Returns:
        OperationResult with impact analysis

    Token Efficiency:
        - Use response_format="summary" for risk assessment and metrics
        - Use response_format="detailed" for complete file lists
        - Summary mode saves 80-90% tokens for large PRs
    """
    start_time = time.time()

    try:
        # Extract file statistics
        added_files = pr_changes.get('added', [])
        modified_files = pr_changes.get('modified', [])
        deleted_files = pr_changes.get('deleted', [])

        # Calculate impact metrics
        total_files_changed = len(added_files) + len(modified_files) + len(deleted_files)

        # Categorize changes by file type
        file_types = {}
        for file in added_files + modified_files:
            ext = Path(file).suffix or 'no_extension'
            file_types[ext] = file_types.get(ext, 0) + 1

        # Assess risk level
        risk_level = "low"
        if total_files_changed > 20:
            risk_level = "high"
        elif total_files_changed > 10:
            risk_level = "medium"

        # Build recommendations
        recommendations = []
        if len(deleted_files) > 5:
            recommendations.append("Large number of deletions - verify no breaking changes")
        if total_files_changed > 15:
            recommendations.append("Large changeset - consider splitting into smaller PRs")
        if len(added_files) > len(modified_files) * 2:
            recommendations.append("Many new files - ensure proper documentation")

        # Build response based on format
        if response_format == "summary":
            impact_data = {
                "total_files_changed": total_files_changed,
                "files_added": len(added_files),
                "files_modified": len(modified_files),
                "files_deleted": len(deleted_files),
                "file_types": file_types,
                "risk_level": risk_level,
                "top_recommendations": recommendations[:3],
                "efficiency_tip": (
                    f"Analyzed {total_files_changed} files (risk: {risk_level}). "
                    f"Using summary mode for efficiency. For complete file lists:\n"
                    f"analyze_change_impact(pr_changes, response_format='detailed')"
                )
            }
        else:
            # Detailed format - include file lists
            impact_data = {
                "total_files_changed": total_files_changed,
                "files_added": len(added_files),
                "files_modified": len(modified_files),
                "files_deleted": len(deleted_files),
                "added_files": added_files,
                "modified_files": modified_files,
                "deleted_files": deleted_files,
                "file_types": file_types,
                "risk_level": risk_level,
                "recommendations": recommendations
            }

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=impact_data,
            duration=duration,
            metadata={
                "skill": "pr-review-assistant",
                "operation": "analyze_change_impact",
                "version": "0.1.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Impact analysis failed: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure pr_changes is a dict with 'added', 'modified', 'deleted' keys",
                    "Verify all file paths in pr_changes are strings",
                    "Check if file paths are valid (can contain Path-compatible strings)",
                    "Try with a simpler pr_changes structure first"
                ],
                "example_fix": "analyze_change_impact({'added': ['new.py'], 'modified': ['old.py'], 'deleted': []})"
            }
        )


def check_pr_quality(
    pr_changes: Dict[str, Any],
    include_tests: bool = True,
    include_security: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Quick quality check for PR changes.

    Args:
        pr_changes: Dictionary with 'added', 'modified', 'deleted' file lists
        include_tests: Check for test coverage (default: True)
        include_security: Check for security issues (default: True)
        response_format: "summary" (score & gates) or "detailed" (all checks)
        **kwargs: Additional parameters

    Returns:
        OperationResult with quality check results

    Token Efficiency:
        - Use response_format="summary" for pass/fail and score
        - Use response_format="detailed" for complete check results
        - Summary mode saves 70-85% tokens
    """
    start_time = time.time()

    try:
        quality_checks = {
            "has_tests": False,
            "has_documentation": False,
            "follows_conventions": True,
            "security_concerns": []
        }

        all_files = pr_changes.get('added', []) + pr_changes.get('modified', [])

        # Check for tests
        if include_tests:
            test_files = [f for f in all_files if 'test' in f.lower() or f.endswith('_test.py') or f.endswith('.test.js')]
            quality_checks["has_tests"] = len(test_files) > 0
            quality_checks["test_files"] = test_files

        # Check for documentation
        doc_files = [f for f in all_files if f.endswith('.md') or 'doc' in f.lower() or f == 'README']
        quality_checks["has_documentation"] = len(doc_files) > 0

        # Basic security checks
        if include_security:
            for file in all_files:
                if any(keyword in file.lower() for keyword in ['password', 'secret', 'key', 'token', 'credential']):
                    quality_checks["security_concerns"].append(f"Potential sensitive data in: {file}")

        # Overall quality score
        score = 0
        if quality_checks["has_tests"]:
            score += 40
        if quality_checks["has_documentation"]:
            score += 30
        if quality_checks["follows_conventions"]:
            score += 20
        if len(quality_checks["security_concerns"]) == 0:
            score += 10

        quality_level = "excellent" if score >= 90 else "good" if score >= 70 else "needs_improvement"

        # Build response based on format
        if response_format == "summary":
            data = {
                "overall_quality_score": score,
                "quality_level": quality_level,
                "has_tests": quality_checks["has_tests"],
                "has_documentation": quality_checks["has_documentation"],
                "security_issues_count": len(quality_checks["security_concerns"]),
                "passed": score >= 70,
                "efficiency_tip": (
                    f"Quality score: {score}/100 ({quality_level}). "
                    f"Using summary mode for efficiency. For detailed checks:\n"
                    f"check_pr_quality(pr_changes, response_format='detailed')"
                )
            }
        else:
            # Detailed format - include everything
            quality_checks["overall_quality_score"] = score
            quality_checks["quality_level"] = quality_level
            data = quality_checks

        duration = time.time() - start_time

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "pr-review-assistant",
                "operation": "check_pr_quality",
                "version": "0.1.0",
                "response_format": response_format
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Quality check failed: {str(e)}",
            error_code="CHECK_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure pr_changes is a dict with 'added', 'modified', 'deleted' keys",
                    "Verify file paths are valid strings",
                    "Try with include_tests=False and include_security=False to isolate the issue",
                    "Check if file paths don't contain special characters causing issues"
                ],
                "example_fix": "check_pr_quality({'added': ['file.py'], 'modified': [], 'deleted': []}, include_tests=True)"
            }
        )


# Export all operations
__all__ = [
    "review_pull_request",
    "generate_review_comment",
    "analyze_change_impact",
    "check_pr_quality",
    "OperationResult"
]
