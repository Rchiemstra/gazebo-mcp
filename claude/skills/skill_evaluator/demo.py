#!/usr/bin/env python3
"""
Skill Evaluator Demo

Demonstrates the capabilities of the skill evaluator.
"""

import time
import random
from skills.skill_evaluator import operations
from skills.skill_evaluator.core.models import ExecutionRecord


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def simulate_skill_executions(skill_name: str, count: int = 20):
    """
    Simulate skill executions for demonstration purposes.

    Args:
        skill_name: Name of the skill
        count: Number of executions to simulate
    """
    print(f"\nSimulating {count} executions for {skill_name}...")

    tracker = operations.get_history_tracker()
    operations_list = ['analyze', 'process', 'generate', 'validate']

    for i in range(count):
        # Simulate varying success rates and durations
        success = random.random() > 0.15  # 85% success rate
        duration = random.uniform(0.5, 5.0)
        operation = random.choice(operations_list)

        record = ExecutionRecord(
            execution_id=f"sim-{skill_name}-{i}",
            skill_name=skill_name,
            operation=operation,
            parameters={'simulated': True},
            success=success,
            duration=duration,
            timestamp=time.time() - (count - i) * 3600,  # Spread over time
            error="Simulated error" if not success else None,
            error_code="SIMULATION_ERROR" if not success else None,
            result_data={'result': 'success'} if success else None
        )

        tracker.record_execution(record)

    print(f"✓ Created {count} simulated execution records")


def demo_monitor_execution():
    """Demonstrate monitoring a skill execution."""
    print_section("Demo 1: Monitor Execution")

    print("\nMonitoring a skill execution...")
    result = operations.monitor_execution(
        skill_name='test-orchestrator',
        operation='generate_tests',
        parameters={'source_file': 'example.py'},
        collect_metrics=True,
        profile_performance=True
    )

    if result.success:
        print("\n✓ Execution monitored successfully!")
        print(f"  Execution ID: {result.data['execution_id']}")
        print(f"  Duration: {result.data['basic_metrics']['duration']:.3f}s")

        if result.data['warnings']:
            print(f"\n  Warnings ({len(result.data['warnings'])}):")
            for warning in result.data['warnings']:
                print(f"    ⚠  {warning}")

        if result.data['recommendations']:
            print(f"\n  Recommendations ({len(result.data['recommendations'])}):")
            for rec in result.data['recommendations']:
                print(f"    💡 {rec}")
    else:
        print(f"\n✗ Monitoring failed: {result.error}")

    return result


def demo_evaluate_quality(skill_name: str = 'demo-skill'):
    """Demonstrate quality evaluation."""
    print_section("Demo 2: Evaluate Quality")

    print(f"\nEvaluating quality for {skill_name}...")

    # First, simulate some executions
    simulate_skill_executions(skill_name, count=30)

    # Now evaluate
    result = operations.evaluate_quality(
        skill_name=skill_name,
        execution_samples=30,
        include_code_analysis=True
    )

    if result.success:
        print("\n✓ Quality evaluation completed!")
        print(f"\n{result.data['summary']}")

        if result.data['strengths']:
            print(f"\n💪 Strengths:")
            for strength in result.data['strengths']:
                print(f"   • {strength}")

        if result.data['weaknesses']:
            print(f"\n⚠ Weaknesses:")
            for weakness in result.data['weaknesses']:
                print(f"   • {weakness}")

        if result.data['improvement_opportunities']:
            print(f"\n🔧 Top Improvement Opportunities:")
            for i, opp in enumerate(result.data['improvement_opportunities'][:3], 1):
                print(f"   {i}. [{opp['severity'].upper()}] {opp['description']}")
                print(f"      Impact: {opp['expected_impact']}")

        if result.data['priority_fixes']:
            print(f"\n🚨 Priority Fixes:")
            for fix in result.data['priority_fixes']:
                print(f"   • {fix}")
    else:
        print(f"\n✗ Evaluation failed: {result.error}")

    return result


def demo_analyze_performance(skill_name: str = 'demo-skill'):
    """Demonstrate performance analysis."""
    print_section("Demo 3: Analyze Performance")

    print(f"\nAnalyzing performance for {skill_name}...")

    result = operations.analyze_performance(
        skill_name=skill_name,
        baseline_period='7d',
        regression_threshold=0.3
    )

    if result.success:
        print("\n✓ Performance analysis completed!")

        data = result.data
        print(f"\n  Performance Score: {data['performance_score']:.1f}/100")
        print(f"  Regression Detected: {'Yes' if data['has_regression'] else 'No'}")

        comparison = data['comparison']
        print(f"\n  Performance Comparison:")
        print(f"    Baseline Average: {comparison['baseline_avg']:.3f}s")
        print(f"    Current Average:  {comparison['current_avg']:.3f}s")
        print(f"    Change:           {comparison['change_percent']:+.1f}%")

        if data['has_regression']:
            print(f"\n  ⚠ Performance regression detected!")
            print(f"    Action required to restore baseline performance.")
    else:
        print(f"\n✗ Analysis failed: {result.error}")

    return result


def demo_suggest_improvements(skill_name: str = 'demo-skill'):
    """Demonstrate improvement suggestions."""
    print_section("Demo 4: Suggest Improvements")

    print(f"\nGenerating improvement suggestions for {skill_name}...")

    result = operations.suggest_improvements(
        skill_name=skill_name,
        focus_areas=['performance', 'reliability'],
        priority_threshold='medium',
        include_examples=True
    )

    if result.success:
        print("\n✓ Improvement suggestions generated!")

        data = result.data
        print(f"\n  Total Suggestions: {len(data.get('suggestions', []))}")
        print(f"  Auto-Applicable: {len(data.get('auto_applicable', []))}")

        if data['estimated_impact']:
            print(f"\n  Estimated Impact by Category:")
            for category, impact in data['estimated_impact'].items():
                print(f"    {category.title()}: {impact:.1f}")

        if data['suggestions']:
            print(f"\n  Detailed Suggestions:")
            for i, suggestion in enumerate(data['suggestions'][:5], 1):
                print(f"\n  {i}. [{suggestion['severity'].upper()}] {suggestion['category'].title()}")
                print(f"     {suggestion['description']}")
                print(f"     Expected Impact: {suggestion['expected_impact']}")
                print(f"     Confidence: {suggestion['confidence'] * 100:.0f}%")
                if suggestion['can_auto_apply']:
                    print(f"     ✓ Can be auto-applied")
    else:
        print(f"\n✗ Suggestion generation failed: {result.error}")

    return result


def demo_generate_report(skill_name: str = 'demo-skill'):
    """Demonstrate report generation."""
    print_section("Demo 5: Generate Report")

    print(f"\nGenerating evaluation report for {skill_name}...")

    result = operations.generate_report(
        skill_name=skill_name,
        report_type='full',
        time_period='30d',
        include_recommendations=True,
        format='markdown'
    )

    if result.success:
        print("\n✓ Report generated successfully!")
        print(f"\n{result.data['report']}")

        summary = result.data['summary']
        print(f"\n📊 Quick Summary:")
        print(f"   Health Score: {summary['overall_health']:.1f}/100 (Grade: {summary['health_grade']})")
        print(f"   Trend: {summary['trend']}")
        print(f"   Critical Issues: {summary['critical_issues']}")
    else:
        print(f"\n✗ Report generation failed: {result.error}")

    return result


def demo_history_stats():
    """Demonstrate history statistics."""
    print_section("Demo 6: Execution History Statistics")

    tracker = operations.get_history_tracker()
    skills = tracker.get_all_tracked_skills()

    print(f"\n📈 Tracked Skills: {len(skills)}")

    for skill_name in skills:
        stats = tracker.get_execution_stats(skill_name, time_period_days=7)
        print(f"\n  {skill_name}:")
        print(f"    Total Executions: {stats['total_executions']}")
        print(f"    Success Rate: {stats['success_rate']:.1f}%")
        print(f"    Error Rate: {stats['error_rate']:.1f}%")
        print(f"    Avg Duration: {stats['avg_duration']:.3f}s")

        if stats['errors_by_code']:
            print(f"    Top Errors:")
            for error_code, count in list(stats['errors_by_code'].items())[:3]:
                print(f"      • {error_code}: {count}")


def demo_quality_gates():
    """Demonstrate quality gate checks."""
    print_section("Demo 7: Quality Gate Checks")

    monitor = operations.get_monitor()
    skill_name = 'demo-skill'

    print(f"\nChecking quality gates for {skill_name}...")

    gates_result = monitor.check_quality_gates(
        skill_name,
        thresholds={
            'max_error_rate': 20.0,
            'min_success_rate': 80.0,
            'max_avg_duration': 30.0,
            'max_p95_duration': 60.0
        }
    )

    print(f"\n✓ Quality gate check completed!")
    print(f"  Overall: {'PASSED ✓' if gates_result['overall_passed'] else 'FAILED ✗'}")

    print(f"\n  Individual Gates:")
    for gate_name, gate_data in gates_result['gates'].items():
        status = '✓' if gate_data['passed'] else '✗'
        print(f"    {status} {gate_name}: {gate_data['value']:.2f} (threshold: {gate_data['threshold']:.2f})")
        if not gate_data['passed'] and 'message' in gate_data:
            print(f"       {gate_data['message']}")


def run_all_demos():
    """Run all demonstration scenarios."""
    print("\n" + "=" * 70)
    print("  Skill Evaluator - Comprehensive Demo")
    print("  Phase 1: Foundation Features")
    print("=" * 70)

    # Run each demo
    demo_monitor_execution()
    demo_evaluate_quality()
    demo_analyze_performance()
    demo_suggest_improvements()
    demo_generate_report()
    demo_history_stats()
    demo_quality_gates()

    print("\n" + "=" * 70)
    print("  Demo Complete!")
    print("=" * 70)
    print("\nPhase 1 features demonstrated:")
    print("  ✓ Execution monitoring")
    print("  ✓ Quality evaluation")
    print("  ✓ Performance analysis")
    print("  ✓ Improvement suggestions")
    print("  ✓ Report generation")
    print("  ✓ History tracking")
    print("  ✓ Quality gates")
    print("\nUpcoming phases:")
    print("  • Phase 2: Advanced performance analysis and regression detection")
    print("  • Phase 3: AI-powered improvement suggestions with agents")
    print("  • Phase 4: Automated improvement application")
    print("  • Phase 5: Continuous monitoring and alerting")
    print("  • Phase 6: Cross-skill analysis and predictive detection")
    print()


if __name__ == '__main__':
    run_all_demos()
