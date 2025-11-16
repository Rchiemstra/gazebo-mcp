"""
Report Generator for Skill Evaluator

Generates comprehensive evaluation reports in multiple formats with
visualizations, trends, and recommendations.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import asdict

from skills.skill_evaluator.core.models import SkillEvaluationMetrics, ImprovementSuggestion


class ReportGenerator:
    """
    Generates comprehensive evaluation reports in multiple formats.

    Supports:
    - Multiple report types: full, summary, trends, comparison
    - Multiple formats: markdown, JSON, HTML
    - Rich visualizations: charts, tables, progress indicators
    - Dashboard-ready data structures
    """

    def __init__(self, history_tracker):
        """
        Initialize the report generator.

        Args:
            history_tracker: ExecutionHistoryTracker instance for data access
        """
        self.history_tracker = history_tracker

    def generate_report(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        report_type: str = "full",
        format: str = "markdown",
        time_period_days: int = 30,
        include_recommendations: bool = True,
        include_trends: bool = True,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive evaluation report.

        Args:
            skill_name: Name of the skill being reported on
            metrics: SkillEvaluationMetrics from evaluation
            report_type: Type of report ('full', 'summary', 'trends', 'comparison')
            format: Output format ('markdown', 'json', 'html')
            time_period_days: Time period covered by the report
            include_recommendations: Include improvement recommendations
            include_trends: Include trend analysis
            include_history: Include execution history

        Returns:
            Dictionary containing report content and metadata
        """
        if format == "json":
            return self._generate_json_report(
                skill_name, metrics, report_type, time_period_days,
                include_recommendations, include_trends, include_history
            )
        elif format == "html":
            return self._generate_html_report(
                skill_name, metrics, report_type, time_period_days,
                include_recommendations, include_trends, include_history
            )
        else:  # markdown (default)
            return self._generate_markdown_report(
                skill_name, metrics, report_type, time_period_days,
                include_recommendations, include_trends, include_history
            )

    def _generate_markdown_report(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        report_type: str,
        time_period_days: int,
        include_recommendations: bool,
        include_trends: bool,
        include_history: bool
    ) -> Dict[str, Any]:
        """Generate a markdown-formatted report."""

        if report_type == "summary":
            report = self._generate_summary_markdown(skill_name, metrics, time_period_days)
        elif report_type == "trends":
            report = self._generate_trends_markdown(skill_name, metrics, time_period_days)
        elif report_type == "comparison":
            report = self._generate_comparison_markdown(skill_name, metrics, time_period_days)
        else:  # full
            report = self._generate_full_markdown(
                skill_name, metrics, time_period_days,
                include_recommendations, include_trends, include_history
            )

        return {
            'content': report,
            'format': 'markdown',
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'skill_name': skill_name,
            'time_period_days': time_period_days
        }

    def _generate_full_markdown(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        time_period_days: int,
        include_recommendations: bool,
        include_trends: bool,
        include_history: bool
    ) -> str:
        """Generate a full markdown report with all sections."""

        report = f"""# Skill Evaluation Report: {skill_name}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Period:** Last {time_period_days} days
**Evaluation ID:** {metrics.evaluation_id}

---

## Executive Summary

{self._format_health_badge(metrics.overall_health_score)} **Overall Health Score:** {metrics.overall_health_score:.1f}/100 ({metrics.get_health_grade()})

**Health Trend:** {self._format_trend_indicator(metrics.health_trend)} {metrics.health_trend.title()}

{self._format_health_bar(metrics.overall_health_score)}

### Key Metrics

| Dimension | Score | Grade | Status |
|-----------|-------|-------|--------|
| Quality | {metrics.quality_scores.overall_score():.1f}/100 | {self._get_grade(metrics.quality_scores.overall_score())} | {self._format_status(metrics.quality_scores.overall_score())} |
| Performance | {metrics.performance_scores.overall_score():.1f}/100 | {self._get_grade(metrics.performance_scores.overall_score())} | {self._format_status(metrics.performance_scores.overall_score())} |
| Reliability | {metrics.reliability_scores.overall_score():.1f}/100 | {self._get_grade(metrics.reliability_scores.overall_score())} | {self._format_status(metrics.reliability_scores.overall_score())} |
| Code Quality | {metrics.code_quality_scores.overall_score():.1f}/100 | {self._get_grade(metrics.code_quality_scores.overall_score())} | {self._format_status(metrics.code_quality_scores.overall_score())} |

---

## Detailed Analysis

### Quality Assessment

**Output Quality Score:** {metrics.quality_scores.output_quality_score:.1f}/100
**Correctness Score:** {metrics.quality_scores.correctness_score:.1f}/100
**Consistency Score:** {metrics.quality_scores.consistency_score:.1f}/100

{self._format_progress_bar("Output Quality", metrics.quality_scores.output_quality_score)}
{self._format_progress_bar("Correctness", metrics.quality_scores.correctness_score)}
{self._format_progress_bar("Consistency", metrics.quality_scores.consistency_score)}

### Performance Metrics

**Performance Score:** {metrics.performance_scores.performance_score:.1f}/100
**Resource Efficiency:** {metrics.performance_scores.resource_efficiency:.1f}/100

{self._format_progress_bar("Performance", metrics.performance_scores.performance_score)}
{self._format_progress_bar("Resource Efficiency", metrics.performance_scores.resource_efficiency)}

"""

        if metrics.performance_scores.has_regression:
            report += f"""
### ⚠️ Performance Regression Detected

{self._format_regression_details(metrics.performance_scores.regression_details)}
"""

        report += f"""
### Reliability Assessment

**Reliability Score:** {metrics.reliability_scores.reliability_score:.1f}/100
**Error Handling Quality:** {metrics.reliability_scores.error_handling_quality:.1f}/100
**Recovery Capability:** {metrics.reliability_scores.recovery_capability:.1f}/100

{self._format_progress_bar("Reliability", metrics.reliability_scores.reliability_score)}
{self._format_progress_bar("Error Handling", metrics.reliability_scores.error_handling_quality)}
{self._format_progress_bar("Recovery", metrics.reliability_scores.recovery_capability)}

### Code Quality Metrics

**Code Quality Score:** {metrics.code_quality_scores.code_quality_score:.1f}/100
**Maintainability Index:** {metrics.code_quality_scores.maintainability_index:.1f}/100
**Complexity Score:** {metrics.code_quality_scores.complexity_score:.1f}/100
**Test Coverage:** {metrics.code_quality_scores.test_coverage:.1f}%

{self._format_progress_bar("Code Quality", metrics.code_quality_scores.code_quality_score)}
{self._format_progress_bar("Maintainability", metrics.code_quality_scores.maintainability_index)}
{self._format_progress_bar("Complexity", 100 - metrics.code_quality_scores.complexity_score)}  # Inverted: lower is better
{self._format_progress_bar("Test Coverage", metrics.code_quality_scores.test_coverage)}

---

## Strengths & Weaknesses

### ✅ Strengths

"""
        for strength in metrics.strengths:
            report += f"- {strength}\n"

        report += "\n### ⚠️ Areas for Improvement\n\n"
        for weakness in metrics.weaknesses:
            report += f"- {weakness}\n"

        if metrics.priority_fixes:
            report += "\n### 🔴 Priority Fixes\n\n"
            for fix in metrics.priority_fixes:
                report += f"- **{fix}**\n"

        if include_recommendations and metrics.improvement_opportunities:
            report += self._format_recommendations_section(metrics.improvement_opportunities)

        if include_trends:
            report += self._format_trends_section(skill_name, time_period_days)

        if include_history:
            report += self._format_history_section(skill_name, time_period_days)

        report += f"""
---

## Report Metadata

- **Evaluation ID:** {metrics.evaluation_id}
- **Generated:** {datetime.now().isoformat()}
- **Time Period:** {time_period_days} days
- **Report Type:** Full Evaluation
- **Format:** Markdown

---

*Generated by Skill Evaluator v0.5.0*
"""

        return report

    def _generate_summary_markdown(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        time_period_days: int
    ) -> str:
        """Generate a concise summary report."""

        report = f"""# Skill Summary: {skill_name}

**Health Score:** {metrics.overall_health_score:.1f}/100 ({metrics.get_health_grade()})
**Trend:** {metrics.health_trend.title()}
**Period:** Last {time_period_days} days

## Quick Stats

{self._format_health_bar(metrics.overall_health_score)}

| Metric | Score |
|--------|-------|
| Quality | {metrics.quality_scores.overall_score():.1f}/100 |
| Performance | {metrics.performance_scores.overall_score():.1f}/100 |
| Reliability | {metrics.reliability_scores.overall_score():.1f}/100 |
| Code Quality | {metrics.code_quality_scores.overall_score():.1f}/100 |

## Top Issues

"""
        for i, fix in enumerate(metrics.priority_fixes[:3], 1):
            report += f"{i}. {fix}\n"

        if not metrics.priority_fixes:
            report += "*No critical issues detected*\n"

        report += f"""
## Top Recommendations

"""
        for i, suggestion in enumerate(metrics.improvement_opportunities[:3], 1):
            report += f"{i}. [{suggestion.severity.upper()}] {suggestion.description}\n"

        if not metrics.improvement_opportunities:
            report += "*No recommendations at this time*\n"

        return report

    def _generate_trends_markdown(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        time_period_days: int
    ) -> str:
        """Generate a trends-focused report."""

        report = f"""# Trend Analysis: {skill_name}

**Period:** Last {time_period_days} days
**Current Health:** {metrics.overall_health_score:.1f}/100
**Trend:** {self._format_trend_indicator(metrics.health_trend)} {metrics.health_trend.title()}

## Health Trend

{self._format_trend_chart(skill_name, time_period_days)}

## Performance Trends

"""

        if metrics.performance_scores.has_regression:
            report += "⚠️ **Regression Detected**\n\n"
            report += self._format_regression_details(metrics.performance_scores.regression_details)
        else:
            report += "✅ No significant performance regressions detected\n"

        return report

    def _generate_comparison_markdown(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        time_period_days: int
    ) -> str:
        """Generate a comparison report (compares current vs baseline)."""

        report = f"""# Performance Comparison: {skill_name}

**Period:** Last {time_period_days} days

## Current vs Baseline

| Metric | Current | Baseline | Change |
|--------|---------|----------|--------|
| Health Score | {metrics.overall_health_score:.1f} | - | - |
| Quality | {metrics.quality_scores.overall_score():.1f} | - | - |
| Performance | {metrics.performance_scores.overall_score():.1f} | - | - |
| Reliability | {metrics.reliability_scores.overall_score():.1f} | - | - |

*Note: Baseline comparison requires historical data tracking*

"""

        return report

    def _generate_json_report(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        report_type: str,
        time_period_days: int,
        include_recommendations: bool,
        include_trends: bool,
        include_history: bool
    ) -> Dict[str, Any]:
        """Generate a JSON-formatted report."""

        data = {
            'skill_name': skill_name,
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'time_period_days': time_period_days,
            'evaluation_id': metrics.evaluation_id,
            'summary': {
                'overall_health_score': metrics.overall_health_score,
                'health_grade': metrics.get_health_grade(),
                'health_trend': metrics.health_trend,
                'has_regression': metrics.performance_scores.has_regression
            },
            'scores': {
                'quality': {
                    'overall': metrics.quality_scores.overall_score(),
                    'output_quality': metrics.quality_scores.output_quality_score,
                    'correctness': metrics.quality_scores.correctness_score,
                    'consistency': metrics.quality_scores.consistency_score
                },
                'performance': {
                    'overall': metrics.performance_scores.overall_score(),
                    'performance_score': metrics.performance_scores.performance_score,
                    'resource_efficiency': metrics.performance_scores.resource_efficiency
                },
                'reliability': {
                    'overall': metrics.reliability_scores.overall_score(),
                    'reliability_score': metrics.reliability_scores.reliability_score,
                    'error_handling': metrics.reliability_scores.error_handling_quality,
                    'recovery': metrics.reliability_scores.recovery_capability
                },
                'code_quality': {
                    'overall': metrics.code_quality_scores.overall_score(),
                    'code_quality_score': metrics.code_quality_scores.code_quality_score,
                    'maintainability': metrics.code_quality_scores.maintainability_index,
                    'complexity': metrics.code_quality_scores.complexity_score,
                    'test_coverage': metrics.code_quality_scores.test_coverage
                }
            },
            'strengths': metrics.strengths,
            'weaknesses': metrics.weaknesses,
            'priority_fixes': metrics.priority_fixes
        }

        if include_recommendations:
            data['recommendations'] = [
                s.to_dict() for s in metrics.improvement_opportunities
            ]

        if metrics.performance_scores.has_regression and metrics.performance_scores.regression_details:
            data['regression_details'] = metrics.performance_scores.regression_details

        content = json.dumps(data, indent=2)

        return {
            'content': content,
            'data': data,
            'format': 'json',
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'skill_name': skill_name,
            'time_period_days': time_period_days
        }

    def _generate_html_report(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        report_type: str,
        time_period_days: int,
        include_recommendations: bool,
        include_trends: bool,
        include_history: bool
    ) -> Dict[str, Any]:
        """Generate an HTML-formatted report."""

        # Simple HTML template
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Skill Evaluation Report: {skill_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .score {{ font-size: 2em; font-weight: bold; }}
        .grade {{ color: {self._get_grade_color(metrics.overall_health_score)}; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .strength {{ color: green; }}
        .weakness {{ color: orange; }}
        .priority {{ color: red; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Skill Evaluation Report: {skill_name}</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Period:</strong> Last {time_period_days} days</p>

    <h2>Executive Summary</h2>
    <p class="score">Overall Health Score: <span class="grade">{metrics.overall_health_score:.1f}/100</span> ({metrics.get_health_grade()})</p>
    <p><strong>Trend:</strong> {metrics.health_trend.title()}</p>

    <h2>Scores</h2>
    <table>
        <tr>
            <th>Dimension</th>
            <th>Score</th>
            <th>Grade</th>
        </tr>
        <tr>
            <td>Quality</td>
            <td>{metrics.quality_scores.overall_score():.1f}/100</td>
            <td>{self._get_grade(metrics.quality_scores.overall_score())}</td>
        </tr>
        <tr>
            <td>Performance</td>
            <td>{metrics.performance_scores.overall_score():.1f}/100</td>
            <td>{self._get_grade(metrics.performance_scores.overall_score())}</td>
        </tr>
        <tr>
            <td>Reliability</td>
            <td>{metrics.reliability_scores.overall_score():.1f}/100</td>
            <td>{self._get_grade(metrics.reliability_scores.overall_score())}</td>
        </tr>
        <tr>
            <td>Code Quality</td>
            <td>{metrics.code_quality_scores.overall_score():.1f}/100</td>
            <td>{self._get_grade(metrics.code_quality_scores.overall_score())}</td>
        </tr>
    </table>

    <h2>Strengths</h2>
    <ul>
"""
        for strength in metrics.strengths:
            html += f"        <li class='strength'>{strength}</li>\n"

        html += """    </ul>

    <h2>Areas for Improvement</h2>
    <ul>
"""
        for weakness in metrics.weaknesses:
            html += f"        <li class='weakness'>{weakness}</li>\n"

        html += """    </ul>
</body>
</html>
"""

        return {
            'content': html,
            'format': 'html',
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'skill_name': skill_name,
            'time_period_days': time_period_days
        }

    # Helper methods for formatting

    def _format_health_badge(self, score: float) -> str:
        """Format a health badge based on score."""
        if score >= 90:
            return "🟢"
        elif score >= 70:
            return "🟡"
        elif score >= 50:
            return "🟠"
        else:
            return "🔴"

    def _format_trend_indicator(self, trend: str) -> str:
        """Format a trend indicator."""
        if trend == "improving":
            return "📈"
        elif trend == "declining":
            return "📉"
        else:
            return "➡️"

    def _format_health_bar(self, score: float) -> str:
        """Format a visual health bar."""
        filled = int(score / 5)  # 20 blocks for 0-100
        empty = 20 - filled
        bar = "█" * filled + "░" * empty
        return f"`[{bar}] {score:.1f}%`"

    def _format_progress_bar(self, label: str, value: float, width: int = 20) -> str:
        """Format a progress bar for a metric."""
        filled = int(value / 5)  # 20 blocks for 0-100
        empty = width - filled
        bar = "▓" * filled + "░" * empty
        return f"**{label}:** `[{bar}] {value:.1f}%`"

    def _format_status(self, score: float) -> str:
        """Format a status indicator."""
        if score >= 90:
            return "✅ Excellent"
        elif score >= 70:
            return "✓ Good"
        elif score >= 50:
            return "⚠️ Fair"
        else:
            return "❌ Needs Improvement"

    def _get_grade(self, score: float) -> str:
        """Get letter grade from score."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _get_grade_color(self, score: float) -> str:
        """Get color for grade (HTML)."""
        if score >= 90:
            return "#4CAF50"  # Green
        elif score >= 70:
            return "#FFC107"  # Yellow
        elif score >= 50:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red

    def _format_regression_details(self, details: Optional[Dict]) -> str:
        """Format regression details."""
        if not details:
            return "*No regression details available*"

        result = f"""**Regression Type:** {details.get('type', 'Unknown')}
**Severity:** {details.get('severity', 'Unknown')}
**Impact:** {details.get('impact', 'Unknown')}

"""
        if 'description' in details:
            result += f"{details['description']}\n"

        return result

    def _format_recommendations_section(self, suggestions: List[ImprovementSuggestion]) -> str:
        """Format the recommendations section."""

        section = "\n---\n\n## Improvement Recommendations\n\n"

        # Group by severity
        critical = [s for s in suggestions if s.severity == 'critical']
        high = [s for s in suggestions if s.severity == 'high']
        medium = [s for s in suggestions if s.severity == 'medium']
        low = [s for s in suggestions if s.severity == 'low']

        if critical:
            section += "### 🔴 Critical Priority\n\n"
            for i, s in enumerate(critical, 1):
                section += self._format_suggestion(i, s)

        if high:
            section += "\n### 🟠 High Priority\n\n"
            for i, s in enumerate(high, 1):
                section += self._format_suggestion(i, s)

        if medium:
            section += "\n### 🟡 Medium Priority\n\n"
            for i, s in enumerate(medium, 1):
                section += self._format_suggestion(i, s)

        if low:
            section += "\n### 🟢 Low Priority\n\n"
            for i, s in enumerate(low, 1):
                section += self._format_suggestion(i, s)

        return section

    def _format_suggestion(self, number: int, suggestion: ImprovementSuggestion) -> str:
        """Format a single suggestion."""
        auto_apply = "✓ Auto-applicable" if suggestion.can_auto_apply else "⚠️ Manual review required"

        result = f"""**{number}. {suggestion.description}**

- **Category:** {suggestion.category.title()}
- **Expected Impact:** {suggestion.expected_impact}
- **Confidence:** {suggestion.confidence*100:.0f}%
- **Status:** {auto_apply}
"""

        if suggestion.location:
            result += f"- **Location:** `{suggestion.location}`\n"

        result += "\n"
        return result

    def _format_trends_section(self, skill_name: str, time_period_days: int) -> str:
        """Format the trends analysis section."""

        section = "\n---\n\n## Trend Analysis\n\n"
        section += f"*Analysis based on last {time_period_days} days of execution data*\n\n"
        section += self._format_trend_chart(skill_name, time_period_days)

        return section

    def _format_trend_chart(self, skill_name: str, time_period_days: int) -> str:
        """Format a simple ASCII trend chart."""

        # Get historical data
        from datetime import datetime, timedelta
        since = (datetime.now() - timedelta(days=time_period_days)).timestamp()

        executions = self.history_tracker.get_recent_executions(
            skill_name=skill_name,
            limit=1000,
            since=since
        )

        if len(executions) < 5:
            return "*Insufficient data for trend analysis*\n"

        # Simple trend indicator based on recent vs older executions
        recent = executions[:len(executions)//3]
        older = executions[len(executions)//3:]

        recent_avg = sum(1 for e in recent if e.get('success', False)) / len(recent) * 100 if recent else 0
        older_avg = sum(1 for e in older if e.get('success', False)) / len(older) * 100 if older else 0

        trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"

        chart = f"""**Success Rate Trend:** {self._format_trend_indicator(trend)} {trend.title()}

- Recent period: {recent_avg:.1f}% success rate
- Earlier period: {older_avg:.1f}% success rate
- Total executions: {len(executions)}

"""
        return chart

    def _format_history_section(self, skill_name: str, time_period_days: int) -> str:
        """Format the execution history section."""

        section = "\n---\n\n## Execution History\n\n"

        # Get execution statistics (this method does support time_period_days)
        stats = self.history_tracker.get_execution_stats(
            skill_name=skill_name,
            time_period_days=time_period_days
        )

        section += f"""**Total Executions:** {stats['total_executions']}
**Success Rate:** {stats['success_rate']*100:.1f}%
**Average Duration:** {stats['avg_duration']:.3f}s
**Error Rate:** {stats['error_rate']*100:.1f}%

"""

        if stats.get('operations'):
            section += "### Operations Breakdown\n\n"
            section += "| Operation | Count | Success Rate |\n"
            section += "|-----------|-------|-------------|\n"
            for op, data in stats['operations'].items():
                section += f"| {op} | {data['count']} | {data.get('success_rate', 0)*100:.1f}% |\n"
            section += "\n"

        return section

    def generate_dashboard_data(
        self,
        skill_name: str,
        metrics: SkillEvaluationMetrics,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate dashboard-ready data structure.

        Returns a structured dictionary optimized for dashboard visualization.
        """

        stats = self.history_tracker.get_execution_stats(
            skill_name=skill_name,
            time_period_days=time_period_days
        )

        return {
            'skill_name': skill_name,
            'timestamp': datetime.now().isoformat(),
            'health': {
                'score': metrics.overall_health_score,
                'grade': metrics.get_health_grade(),
                'trend': metrics.health_trend,
                'indicator': self._format_health_badge(metrics.overall_health_score)
            },
            'scores': {
                'quality': metrics.quality_scores.overall_score(),
                'performance': metrics.performance_scores.overall_score(),
                'reliability': metrics.reliability_scores.overall_score(),
                'code_quality': metrics.code_quality_scores.overall_score()
            },
            'statistics': {
                'total_executions': stats['total_executions'],
                'success_rate': stats['success_rate'],
                'error_rate': stats['error_rate'],
                'avg_duration': stats['avg_duration']
            },
            'alerts': {
                'critical_issues': len(metrics.priority_fixes),
                'has_regression': metrics.performance_scores.has_regression,
                'priority_fixes': metrics.priority_fixes[:5]
            },
            'recommendations': {
                'total': len(metrics.improvement_opportunities),
                'auto_applicable': len([s for s in metrics.improvement_opportunities if s.can_auto_apply]),
                'top_3': [s.to_dict() for s in metrics.improvement_opportunities[:3]]
            },
            'time_period_days': time_period_days
        }
