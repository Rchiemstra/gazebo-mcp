"""
Comment Generator

Generates formatted review comments for pull requests.
"""

from typing import Dict, List


class CommentGenerator:
    """Generates formatted PR review comments."""

    def generate_review_comment(
        self,
        review_result: Dict,
        format: str = "github"
    ) -> str:
        """
        Generate formatted review comment.

        Args:
            review_result: Result from review_pull_request
            format: Output format (github, gitlab, markdown)

        Returns:
            Formatted comment string
        """
        if format in ['github', 'gitlab', 'markdown']:
            return self._generate_markdown_comment(review_result)
        else:
            return self._generate_markdown_comment(review_result)

    def _generate_markdown_comment(self, result: Dict) -> str:
        """Generate markdown-formatted comment."""
        lines = []

        # Header
        lines.append("## 🤖 Automated Code Review")
        lines.append("")

        # Overall score
        status_emoji = self._get_status_emoji(result['approval_status'])
        lines.append(f"**Overall Score:** {result['overall_score']:.1f}/100 {status_emoji}")
        lines.append(f"**Status:** {self._format_status(result['approval_status'])}")
        lines.append("")

        # Dimension scores
        lines.append("### 📊 Review Dimensions")
        lines.append("")

        for dim in result['dimension_scores']:
            bar = self._create_score_bar(dim['score'])
            lines.append(f"**{self._format_dimension_name(dim['dimension'])}** "
                        f"({dim['weight']*100:.0f}% weight)")
            lines.append(f"Score: {dim['score']:.1f}/100 {bar}")
            lines.append(f"Checks: {dim['passed_checks']}/{dim['total_checks']} passed")
            lines.append("")

        # Issues
        if result['issues']:
            lines.append(f"### ⚠️ Issues Found ({len(result['issues'])})")
            lines.append("")

            # Group by severity
            issues_by_severity = self._group_issues_by_severity(result['issues'])

            for severity in ['blocker', 'critical', 'major', 'minor', 'info']:
                if severity in issues_by_severity:
                    issues = issues_by_severity[severity]
                    emoji = self._get_severity_emoji(severity)
                    lines.append(f"#### {emoji} {severity.title()} ({len(issues)})")
                    lines.append("")

                    for issue in issues:
                        lines.append(f"**{issue['title']}**")
                        if issue['file_path']:
                            lines.append(f"📁 File: `{issue['file_path']}`")
                        if issue['line_number']:
                            lines.append(f"📍 Line: {issue['line_number']}")
                        lines.append(f"📝 {issue['description']}")
                        lines.append(f"💡 {issue['suggestion']}")
                        lines.append("")

        # Recommendations
        if result['recommendations']:
            lines.append("### 💡 Recommendations")
            lines.append("")

            for rec in result['recommendations']:
                lines.append(f"- {rec}")

            lines.append("")

        # Statistics
        stats = result['statistics']
        lines.append("### 📈 Change Statistics")
        lines.append("")
        lines.append(f"- Files Added: {stats['files_added']}")
        lines.append(f"- Files Modified: {stats['files_modified']}")
        lines.append(f"- Files Deleted: {stats['files_deleted']}")
        lines.append(f"- Total Files Changed: {stats['total_files_changed']}")
        lines.append("")

        # Footer
        lines.append("---")
        lines.append("*This review was generated automatically. "
                    "Please review the suggestions and apply where appropriate.*")

        return "\n".join(lines)

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for approval status."""
        emoji_map = {
            'approve': '✅',
            'request_changes': '❌',
            'comment': '💬'
        }
        return emoji_map.get(status, '❓')

    def _format_status(self, status: str) -> str:
        """Format approval status."""
        status_map = {
            'approve': '✅ **APPROVED** - Ready to merge',
            'request_changes': '❌ **CHANGES REQUESTED** - Please address issues',
            'comment': '💬 **COMMENTED** - Minor improvements suggested'
        }
        return status_map.get(status, status)

    def _format_dimension_name(self, dimension: str) -> str:
        """Format dimension name."""
        return dimension.replace('_', ' ').title()

    def _create_score_bar(self, score: float) -> str:
        """Create visual score bar."""
        filled = int(score / 10)
        empty = 10 - filled

        if score >= 80:
            return '🟢 ' + '█' * filled + '░' * empty
        elif score >= 60:
            return '🟡 ' + '█' * filled + '░' * empty
        else:
            return '🔴 ' + '█' * filled + '░' * empty

    def _group_issues_by_severity(self, issues: List[Dict]) -> Dict[str, List[Dict]]:
        """Group issues by severity level."""
        grouped = {}

        for issue in issues:
            severity = issue['severity']
            if severity not in grouped:
                grouped[severity] = []
            grouped[severity].append(issue)

        return grouped

    def _get_severity_emoji(self, severity: str) -> str:
        """Get emoji for severity level."""
        emoji_map = {
            'blocker': '🚫',
            'critical': '🔴',
            'major': '🟠',
            'minor': '🟡',
            'info': '🔵'
        }
        return emoji_map.get(severity, '⚪')


def generate_review_comment(review_result: Dict, format: str = "github") -> str:
    """
    Convenience function to generate review comment.

    Args:
        review_result: Result from review_pull_request
        format: Output format (github, gitlab, markdown)

    Returns:
        Formatted comment string
    """
    generator = CommentGenerator()
    return generator.generate_review_comment(review_result, format)
