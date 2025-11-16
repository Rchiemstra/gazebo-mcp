"""
Skill Evaluator - Phase 5 Demo
Comprehensive Reporting & Improvement History

Demonstrates:
- Multi-format report generation (Markdown, JSON, HTML)
- Multiple report types (full, summary, trends, comparison)
- Improvement history tracking
- Dashboard data generation
- Improvement effectiveness analysis
"""

import time
from skills.skill_evaluator import operations
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker
from datetime import datetime


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def demo_1_report_formats():
    """Demo 1: Generate reports in different formats."""
    print_section("DEMO 1: Report Formats (Markdown, JSON, HTML)")

    skill_name = 'test-orchestrator'

    print(f"Generating reports for skill: {skill_name}\n")

    # Markdown report (default)
    print("1. Markdown Report (Summary)")
    print("-" * 40)
    result = operations.generate_report(
        skill_name=skill_name,
        report_type='summary',
        time_period='30d',
        format='markdown'
    )

    if result.success:
        print(result.data['report'][:500] + "...\n")  # First 500 chars
        print(f"✓ Generated markdown report ({len(result.data['report'])} characters)")
    else:
        print(f"✗ Failed: {result.error}")

    print()

    # JSON report
    print("2. JSON Report (Summary)")
    print("-" * 40)
    result = operations.generate_report(
        skill_name=skill_name,
        report_type='summary',
        time_period='30d',
        format='json'
    )

    if result.success:
        import json
        data = result.data.get('report_data', {}).get('data', {})
        print(json.dumps(data.get('summary', {}), indent=2))
        print(f"\n✓ Generated JSON report")
    else:
        print(f"✗ Failed: {result.error}")

    print()

    # HTML report
    print("3. HTML Report (Summary)")
    print("-" * 40)
    result = operations.generate_report(
        skill_name=skill_name,
        report_type='summary',
        time_period='30d',
        format='html'
    )

    if result.success:
        html = result.data['report']
        print(html[:300] + "...")  # First 300 chars
        print(f"\n✓ Generated HTML report ({len(html)} characters)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_2_report_types():
    """Demo 2: Different report types."""
    print_section("DEMO 2: Report Types (Full, Summary, Trends)")

    skill_name = 'refactor-assistant'

    print(f"Generating different report types for: {skill_name}\n")

    report_types = ['summary', 'full', 'trends']

    for report_type in report_types:
        print(f"\n{report_type.upper()} Report")
        print("-" * 40)

        result = operations.generate_report(
            skill_name=skill_name,
            report_type=report_type,
            time_period='7d',
            format='markdown',
            include_recommendations=True,
            include_trends=(report_type != 'summary'),
            include_history=(report_type == 'full')
        )

        if result.success:
            report_preview = result.data['report'][:400]
            print(report_preview + "...")
            print(f"\n✓ Generated {report_type} report")
            print(f"  - Health Score: {result.data['summary']['overall_health']:.1f}/100")
            print(f"  - Health Grade: {result.data['summary']['health_grade']}")
            print(f"  - Trend: {result.data['summary']['trend']}")
            print(f"  - Report Size: {len(result.data['report'])} characters")
        else:
            print(f"✗ Failed: {result.error}")


def demo_3_improvement_history():
    """Demo 3: Improvement history tracking."""
    print_section("DEMO 3: Improvement History Tracking")

    skill_name = 'test-orchestrator'

    print(f"Simulating improvement tracking for: {skill_name}\n")

    # Get ExecutionHistoryTracker instance
    tracker = ExecutionHistoryTracker()

    # Simulate recording some improvements
    print("1. Recording improvements...")
    print("-" * 40)

    improvements = [
        {
            'category': 'performance',
            'severity': 'high',
            'description': 'Optimized test discovery algorithm',
            'expected_impact': 'Reduce discovery time by 40%',
            'applied_by': 'skill-evaluator',
            'validation_status': {'success': True, 'tests_passed': 15}
        },
        {
            'category': 'reliability',
            'severity': 'critical',
            'description': 'Fixed race condition in parallel test execution',
            'expected_impact': 'Eliminate intermittent failures',
            'applied_by': 'skill-evaluator',
            'validation_status': {'success': True, 'tests_passed': 20}
        },
        {
            'category': 'code_quality',
            'severity': 'medium',
            'description': 'Refactored test result aggregation',
            'expected_impact': 'Improved maintainability',
            'applied_by': 'skill-evaluator',
            'validation_status': {'success': True, 'tests_passed': 12}
        }
    ]

    for imp in improvements:
        tracker.record_improvement(skill_name, imp)
        print(f"  ✓ Recorded: {imp['description']}")

    print()

    # Get improvement history
    print("2. Retrieving improvement history...")
    print("-" * 40)

    history = tracker.get_improvement_history(skill_name, limit=10)
    print(f"Total improvements found: {len(history)}\n")

    for i, imp in enumerate(history[:3], 1):
        print(f"{i}. [{imp.get('severity', 'N/A').upper()}] {imp.get('description', 'N/A')}")
        print(f"   Category: {imp.get('category', 'N/A')}")
        print(f"   Timestamp: {imp.get('timestamp', 'N/A')[:19]}")
        print(f"   Validation: {'✓ Passed' if imp.get('validation_status', {}).get('success') else '✗ Failed'}")
        print()

    # Get improvement statistics
    print("3. Improvement statistics...")
    print("-" * 40)

    stats = tracker.get_improvement_stats(skill_name, time_period_days=30)

    print(f"Total Improvements: {stats['total_improvements']}")
    print(f"Success Rate: {stats['success_rate']:.1f}%")
    print(f"\nBy Category:")
    for category, count in stats['by_category'].items():
        print(f"  - {category}: {count}")
    print(f"\nBy Severity:")
    for severity, count in stats['by_severity'].items():
        print(f"  - {severity}: {count}")


def demo_4_full_report_with_improvements():
    """Demo 4: Full report including improvement history."""
    print_section("DEMO 4: Full Report with Improvement History")

    skill_name = 'pr-review-assistant'

    print(f"Generating comprehensive report for: {skill_name}\n")

    result = operations.generate_report(
        skill_name=skill_name,
        report_type='full',
        time_period='30d',
        format='markdown',
        include_recommendations=True,
        include_trends=True,
        include_history=True,
        include_improvements=True
    )

    if result.success:
        print("Report Preview:")
        print("-" * 80)
        print(result.data['report'][:800])
        print("\n... (truncated) ...\n")

        print("\nReport Summary:")
        print("-" * 40)
        summary = result.data['summary']
        print(f"Overall Health: {summary['overall_health']:.1f}/100 ({summary['health_grade']})")
        print(f"Trend: {summary['trend']}")
        print(f"Critical Issues: {summary['critical_issues']}")
        print(f"Recent Improvements: {summary['recent_improvements']}")

        print("\nImprovement Stats:")
        print("-" * 40)
        imp_stats = result.data.get('improvement_stats')
        if imp_stats:
            print(f"Total Improvements: {imp_stats['total_improvements']}")
            print(f"Success Rate: {imp_stats.get('success_rate', 0):.1f}%")
        else:
            print("No improvement history available")

        print(f"\n✓ Full report generated successfully")
        print(f"  Duration: {result.duration:.3f}s")
        print(f"  Report Size: {len(result.data['report'])} characters")

    else:
        print(f"✗ Failed: {result.error}")


def demo_5_dashboard_data():
    """Demo 5: Dashboard-ready data generation."""
    print_section("DEMO 5: Dashboard Data Generation")

    skill_name = 'doc-generator'

    print(f"Generating dashboard data for: {skill_name}\n")

    result = operations.generate_report(
        skill_name=skill_name,
        report_type='summary',
        time_period='30d',
        format='markdown',
        include_improvements=True
    )

    if result.success:
        dashboard = result.data.get('dashboard_data', {})

        print("Dashboard Data Structure:")
        print("-" * 40)

        print(f"\nHealth Status:")
        health = dashboard.get('health', {})
        print(f"  Score: {health.get('score', 0):.1f}/100")
        print(f"  Grade: {health.get('grade', 'N/A')}")
        print(f"  Trend: {health.get('trend', 'N/A')}")
        print(f"  Indicator: {health.get('indicator', 'N/A')}")

        print(f"\nScores Breakdown:")
        scores = dashboard.get('scores', {})
        for metric, value in scores.items():
            print(f"  {metric.replace('_', ' ').title()}: {value:.1f}/100")

        print(f"\nStatistics:")
        stats = dashboard.get('statistics', {})
        print(f"  Total Executions: {stats.get('total_executions', 0)}")
        print(f"  Success Rate: {stats.get('success_rate', 0)*100:.1f}%")
        print(f"  Error Rate: {stats.get('error_rate', 0)*100:.1f}%")
        print(f"  Avg Duration: {stats.get('avg_duration', 0):.3f}s")

        print(f"\nAlerts:")
        alerts = dashboard.get('alerts', {})
        print(f"  Critical Issues: {alerts.get('critical_issues', 0)}")
        print(f"  Has Regression: {alerts.get('has_regression', False)}")

        print(f"\nRecommendations:")
        recs = dashboard.get('recommendations', {})
        print(f"  Total: {recs.get('total', 0)}")
        print(f"  Auto-Applicable: {recs.get('auto_applicable', 0)}")

        print(f"\n✓ Dashboard data ready for visualization")

    else:
        print(f"✗ Failed: {result.error}")


def demo_6_improvement_effectiveness():
    """Demo 6: Analyze improvement effectiveness."""
    print_section("DEMO 6: Improvement Effectiveness Analysis")

    skill_name = 'test-orchestrator'

    print(f"Analyzing improvement effectiveness for: {skill_name}\n")

    tracker = ExecutionHistoryTracker()

    # Simulate some improvements with impact data
    print("1. Simulating improvements with measured impact...")
    print("-" * 40)

    improvements_with_impact = [
        {
            'category': 'performance',
            'severity': 'high',
            'description': 'Optimized database queries',
            'expected_impact': 'Reduce query time by 50%',
            'validation_status': {'success': True}
        },
        {
            'category': 'reliability',
            'severity': 'critical',
            'description': 'Fixed memory leak',
            'expected_impact': 'Eliminate crashes',
            'validation_status': {'success': True}
        }
    ]

    improvement_ids = []
    for imp in improvements_with_impact:
        tracker.record_improvement(skill_name, imp)
        # Get the improvement_id
        history = tracker.get_improvement_history(skill_name, limit=1)
        if history:
            imp_id = history[0].get('improvement_id')
            improvement_ids.append(imp_id)
            print(f"  ✓ Recorded: {imp['description']}")

    print()

    # Update with impact data
    print("2. Updating with measured impact data...")
    print("-" * 40)

    impact_data = [
        {
            'actual_impact': 'Query time reduced from 2.5s to 1.1s',
            'improvement_percentage': 56.0,
            'metrics_before': {'avg_duration': 2.5},
            'metrics_after': {'avg_duration': 1.1},
            'verified': True
        },
        {
            'actual_impact': 'No crashes reported in 30 days',
            'improvement_percentage': 100.0,
            'metrics_before': {'crashes_per_day': 3.2},
            'metrics_after': {'crashes_per_day': 0.0},
            'verified': True
        }
    ]

    for imp_id, impact in zip(improvement_ids, impact_data):
        if tracker.update_improvement_impact(skill_name, imp_id, impact):
            print(f"  ✓ Updated impact for improvement: {imp_id}")

    print()

    # Analyze effectiveness
    print("3. Effectiveness analysis...")
    print("-" * 40)

    analysis = tracker.analyze_improvement_effectiveness(
        skill_name=skill_name,
        time_period_days=90
    )

    if analysis.get('has_data'):
        print(f"Total Improvements: {analysis['total_improvements']}")
        print(f"Measured Improvements: {analysis['measured_improvements']}")
        print(f"Measurement Rate: {analysis['measurement_rate']:.1f}%")
        print(f"Verified Positive: {analysis['verified_positive']}")
        print(f"Verified Negative: {analysis['verified_negative']}")
        print(f"Effectiveness Rate: {analysis['effectiveness_rate']:.1f}%")

        if analysis.get('avg_impact_by_category'):
            print(f"\nAverage Impact by Category:")
            for category, avg_impact in analysis['avg_impact_by_category'].items():
                print(f"  {category}: +{avg_impact:.1f}%")

        if analysis.get('most_effective_category'):
            print(f"\nMost Effective Category: {analysis['most_effective_category']}")

        if analysis.get('recommendations'):
            print(f"\nRecommendations:")
            for rec in analysis['recommendations']:
                print(f"  - {rec}")

        print(f"\n✓ Effectiveness analysis complete")
    else:
        print(f"⚠ {analysis.get('message', 'No data available')}")


def demo_7_custom_report():
    """Demo 7: Customized report with specific options."""
    print_section("DEMO 7: Customized Report Options")

    skill_name = 'git-workflow-assistant'

    print(f"Generating customized report for: {skill_name}\n")

    print("Options:")
    print("  - Report Type: summary")
    print("  - Time Period: 7 days")
    print("  - Format: markdown")
    print("  - Include Recommendations: Yes")
    print("  - Include Trends: No (summary report)")
    print("  - Include History: No (summary report)")
    print("  - Include Improvements: Yes")
    print()

    result = operations.generate_report(
        skill_name=skill_name,
        report_type='summary',
        time_period='7d',
        format='markdown',
        include_recommendations=True,
        include_trends=False,
        include_history=False,
        include_improvements=True
    )

    if result.success:
        print("Generated Report:")
        print("-" * 80)
        print(result.data['report'])
        print()

        print(f"✓ Customized report generated successfully")
        print(f"  Duration: {result.duration:.3f}s")

    else:
        print(f"✗ Failed: {result.error}")


def run_all_demos():
    """Run all Phase 5 demos."""
    print("\n" + "="*80)
    print("  SKILL EVALUATOR - PHASE 5 DEMONSTRATIONS")
    print("  Comprehensive Reporting & Improvement History")
    print("="*80)

    demos = [
        ("Report Formats", demo_1_report_formats),
        ("Report Types", demo_2_report_types),
        ("Improvement History", demo_3_improvement_history),
        ("Full Report with Improvements", demo_4_full_report_with_improvements),
        ("Dashboard Data", demo_5_dashboard_data),
        ("Improvement Effectiveness", demo_6_improvement_effectiveness),
        ("Custom Report", demo_7_custom_report)
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            print(f"\n\nRunning Demo {i}/{len(demos)}: {name}")
            time.sleep(0.5)  # Brief pause between demos
            demo_func()
        except Exception as e:
            print(f"\n✗ Demo {i} failed with error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("  ALL PHASE 5 DEMONSTRATIONS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    run_all_demos()
