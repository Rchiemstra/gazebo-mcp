"""
Skill Evaluator - Phase 6 Demo
Advanced Features: Cross-Skill Analysis & Benchmarking

Demonstrates:
- Cross-skill interaction analysis
- Dependency chain detection
- Workflow pattern recognition
- Bottleneck identification
- Skill benchmarking and comparison
- Leaderboard generation
- Workflow optimization suggestions
"""

import time
from skills.skill_evaluator import operations
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker
from skills.skill_evaluator.core.models import ExecutionRecord
from datetime import datetime


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def setup_test_data():
    """Create some test execution data for demonstration."""
    tracker = ExecutionHistoryTracker()

    # Simulate some skill executions with realistic patterns
    test_skills = [
        'test-orchestrator',
        'refactor-assistant',
        'pr-review-assistant',
        'doc-generator',
        'git-workflow-assistant'
    ]

    current_time = datetime.now().timestamp()

    # Create execution sequences to demonstrate dependencies
    for i in range(20):
        # Pattern 1: test-orchestrator -> refactor-assistant
        record1 = ExecutionRecord(
            execution_id=f"test-orchestrator-{i}",
            skill_name='test-orchestrator',
            operation='run_tests',
            timestamp=current_time - (i * 3600),  # Every hour
            duration=2.5 + (i % 3) * 0.5,
            success=i % 10 != 0,  # 90% success rate
            parameters={},
            result_data={}
        )
        tracker.record_execution(record1)

        # Followed by refactor-assistant
        record2 = ExecutionRecord(
            execution_id=f"refactor-assistant-{i}",
            skill_name='refactor-assistant',
            operation='detect_smells',
            timestamp=current_time - (i * 3600) + 3,  # 3 seconds later
            duration=1.8 + (i % 2) * 0.3,
            success=i % 8 != 0,  # 87.5% success rate
            parameters={},
            result_data={}
        )
        tracker.record_execution(record2)

        # Pattern 2: pr-review-assistant -> doc-generator
        if i % 2 == 0:
            record3 = ExecutionRecord(
                execution_id=f"pr-review-assistant-{i}",
                skill_name='pr-review-assistant',
                operation='review_pr',
                timestamp=current_time - (i * 3600) + 10,
                duration=3.2 + (i % 4) * 0.4,
                success=i % 12 != 0,  # 91.7% success rate
                parameters={},
                result_data={}
            )
            tracker.record_execution(record3)

            record4 = ExecutionRecord(
                execution_id=f"doc-generator-{i}",
                skill_name='doc-generator',
                operation='generate_docs',
                timestamp=current_time - (i * 3600) + 15,
                duration=2.1 + (i % 3) * 0.2,
                success=True,  # 100% success rate
                parameters={},
                result_data={}
            )
            tracker.record_execution(record4)

        # Pattern 3: git-workflow-assistant used independently
        if i % 3 == 0:
            record5 = ExecutionRecord(
                execution_id=f"git-workflow-assistant-{i}",
                skill_name='git-workflow-assistant',
                operation='create_branch',
                timestamp=current_time - (i * 3600) + 30,
                duration=0.8 + (i % 2) * 0.1,
                success=True,  # 100% success rate
                parameters={},
                result_data={}
            )
            tracker.record_execution(record5)

    print("✓ Test data setup complete")
    print(f"  - Created execution records for {len(test_skills)} skills")
    print(f"  - Simulated common workflow patterns")
    print(f"  - Added realistic success rates and durations")


def demo_1_skill_interactions():
    """Demo 1: Analyze skill interactions."""
    print_section("DEMO 1: Skill Interaction Analysis")

    print("Analyzing how skills interact with each other...\n")

    result = operations.analyze_skill_interactions(
        time_period_days=7,
        min_interactions=2
    )

    if result.success:
        data = result.data

        print(f"Total Skills Analyzed: {data['total_skills']}")
        print(f"Interacting Pairs: {data['interacting_pairs']}")
        print(f"Total Interactions: {data['total_interactions']}")
        print()

        if data['top_interactions']:
            print("Top Skill Interactions:")
            print("-" * 60)
            for i, interaction in enumerate(data['top_interactions'][:5], 1):
                skills = ' ↔ '.join(interaction['skills'])
                print(f"{i}. {skills}")
                print(f"   Interactions: {interaction['interaction_count']}")
                print(f"   Avg time between: {interaction['avg_time_between']:.2f}s")
                print()

        if data['skill_clusters']:
            print("Skill Clusters (frequently interacting groups):")
            print("-" * 60)
            for i, cluster in enumerate(data['skill_clusters'], 1):
                print(f"{i}. {', '.join(cluster)}")

        print(f"\n✓ Analysis complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_2_dependency_chains():
    """Demo 2: Detect dependency chains."""
    print_section("DEMO 2: Dependency Chain Detection")

    print("Detecting common skill execution sequences...\n")

    result = operations.detect_dependency_chains(
        time_period_days=7
    )

    if result.success:
        data = result.data

        print(f"Total Sequences Found: {data['total_sequences']}")
        print(f"Total Occurrences: {data['total_occurrences']}")
        print()

        if data['top_chains']:
            print("Most Common Dependency Chains:")
            print("-" * 70)
            for i, chain in enumerate(data['top_chains'][:5], 1):
                print(f"{i}. {chain['from_skill']} → {chain['to_skill']}")
                print(f"   Occurrences: {chain['occurrences']}")
                print(f"   Success Rate: {chain['reliability']['success_rate']:.1f}%")
                print(f"   Avg Time Between: {chain['reliability']['avg_time_between']:.2f}s")
                print()

        if data['circular_dependencies']:
            print("⚠️  Circular Dependencies Detected:")
            print("-" * 60)
            for cycle in data['circular_dependencies']:
                print(f"   {' → '.join(cycle)}")
        else:
            print("✓ No circular dependencies detected")

        print(f"\n✓ Analysis complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_3_workflow_patterns():
    """Demo 3: Analyze workflow patterns."""
    print_section("DEMO 3: Workflow Pattern Analysis")

    print("Identifying common workflow patterns...\n")

    result = operations.analyze_workflow_patterns(
        time_period_days=7,
        min_pattern_length=2,
        max_pattern_length=4
    )

    if result.success:
        data = result.data

        print(f"Patterns Found: {data['total_patterns_found']}")
        print()

        if data['top_patterns']:
            print("Top Workflow Patterns:")
            print("-" * 70)
            for i, pattern in enumerate(data['top_patterns'][:5], 1):
                workflow = ' → '.join(pattern['pattern'])
                print(f"{i}. {workflow}")
                print(f"   Occurrences: {pattern['occurrences']}")
                print(f"   Success Rate: {pattern['success_rate']:.1f}%")
                print(f"   Avg Duration: {pattern['avg_duration']:.2f}s")
                print(f"   Pattern Length: {pattern['length']} skills")
                print()

        print(f"✓ Analysis complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_4_bottleneck_detection():
    """Demo 4: Identify bottlenecks."""
    print_section("DEMO 4: Bottleneck Identification")

    print("Identifying skills that may be bottlenecks...\n")

    result = operations.identify_bottlenecks(
        time_period_days=7
    )

    if result.success:
        data = result.data

        print(f"Skills Analyzed: {data['total_analyzed']}")
        print()

        # Show bottlenecks by severity
        for severity in ['critical', 'high', 'medium', 'low']:
            bottlenecks = data['by_severity'][severity]
            if bottlenecks:
                icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                print(f"{icon} {severity.upper()} Priority Bottlenecks:")
                print("-" * 60)
                for b in bottlenecks[:3]:
                    print(f"  • {b['skill']}")
                    print(f"    Bottleneck Score: {b['bottleneck_score']:.1f}/100")
                    print(f"    Frequency: {b['frequency']} executions")
                    print(f"    Avg Duration: {b['avg_duration']:.2f}s")
                    print(f"    Error Rate: {b['error_rate']:.1f}%")
                    print()

        if data['recommendations']:
            print("Recommendations:")
            print("-" * 60)
            for rec in data['recommendations']:
                print(f"  • {rec}")

        print(f"\n✓ Analysis complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_5_workflow_optimizations():
    """Demo 5: Suggest workflow optimizations."""
    print_section("DEMO 5: Workflow Optimization Suggestions")

    print("Analyzing workflows for optimization opportunities...\n")

    result = operations.suggest_workflow_optimizations(
        time_period_days=7
    )

    if result.success:
        data = result.data

        if data.get('has_data'):
            print(f"Total Suggestions: {data['total_suggestions']}")
            print()

            if data.get('priority_actions'):
                print("🔴 Priority Actions:")
                print("-" * 70)
                for action in data['priority_actions']:
                    severity_icon = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[action['severity']]
                    print(f"{severity_icon} [{action['type'].upper()}] {action['severity'].upper()}")
                    print(f"   {action['description']}")
                    print(f"   Recommendation: {action['recommendation']}")
                    print(f"   Impact: {action['impact']}")
                    print()

            print("All Suggestions:")
            print("-" * 70)
            for i, suggestion in enumerate(data['suggestions'], 1):
                print(f"{i}. [{suggestion['severity'].upper()}] {suggestion['description']}")
                print(f"   Recommendation: {suggestion['recommendation']}")
                print()
        else:
            print("✓ No optimization suggestions - workflows are performing well!")

        print(f"✓ Analysis complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_6_benchmarking():
    """Demo 6: Benchmark multiple skills."""
    print_section("DEMO 6: Skill Benchmarking")

    print("Benchmarking all skills for comparison...\n")

    result = operations.benchmark_skills(
        skill_names=None,  # All skills
        time_period_days=7,
        min_executions=5
    )

    if result.success:
        data = result.data

        print(f"Skills Benchmarked: {data['total_benchmarked']}")
        print()

        print("Leaderboard (Top 5):")
        print("-" * 70)
        for entry in data['leaderboard'][:5]:
            print(f"{entry['rank']}. {entry['skill_name']}")
            print(f"   Health Score: {entry['health_score']:.1f}/100")
            print(f"   Percentile Rank: {entry['percentile_rank']:.1f}")
            print(f"   Success Rate: {entry['success_rate']:.1f}%")
            print(f"   Avg Duration: {entry['avg_duration']:.2f}s")
            print()

        print("Comparative Statistics:")
        print("-" * 60)
        stats = data['comparative_stats']
        print(f"  Duration (avg): {stats['duration']['mean']:.2f}s")
        print(f"  Success Rate (avg): {stats['success_rate']['mean']:.1f}%")
        print(f"  Health Score (avg): {stats['health_score']['mean']:.1f}/100")
        print()

        if data['top_performers']:
            print(f"✓ Top Performers: {', '.join(data['top_performers'])}")
        if data['underperformers']:
            print(f"⚠️  Underperformers: {', '.join(data['underperformers'])}")

        print(f"\n✓ Benchmarking complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_7_skill_comparison():
    """Demo 7: Compare two skills head-to-head."""
    print_section("DEMO 7: Head-to-Head Skill Comparison")

    skill1 = 'test-orchestrator'
    skill2 = 'refactor-assistant'

    print(f"Comparing {skill1} vs {skill2}...\n")

    result = operations.compare_skills(
        skill1=skill1,
        skill2=skill2,
        time_period_days=7
    )

    if result.success:
        comp = result.data['comparison']

        print("Comparison Results:")
        print("=" * 70)

        # Performance
        print("\n📊 Performance")
        print("-" * 60)
        perf = comp['metrics']['performance']
        print(f"  {skill1}: {perf['skill1_avg_duration']:.2f}s")
        print(f"  {skill2}: {perf['skill2_avg_duration']:.2f}s")
        print(f"  Winner: {perf['winner']} (faster by {abs(perf['difference_seconds']):.2f}s)")

        # Reliability
        print("\n🛡️  Reliability")
        print("-" * 60)
        rel = comp['metrics']['reliability']
        print(f"  {skill1}: {rel['skill1_success_rate']:.1f}%")
        print(f"  {skill2}: {rel['skill2_success_rate']:.1f}%")
        print(f"  Winner: {rel['winner']} (+{abs(rel['difference_percent']):.1f}%)")

        # Health
        print("\n💚 Health Score")
        print("-" * 60)
        health = comp['metrics']['health']
        print(f"  {skill1}: {health['skill1_health_score']:.1f}/100")
        print(f"  {skill2}: {health['skill2_health_score']:.1f}/100")
        print(f"  Winner: {health['winner']} (+{abs(health['difference_points']):.1f} points)")

        # Overall winner
        print("\n🏆 Overall Winner")
        print("-" * 60)
        winner = comp['overall_winner']
        print(f"  Winner: {winner['winner']}")
        print(f"  Score: {winner['score']}")
        print(f"  Margin: {winner['margin']}")

        # Recommendations
        if result.data.get('recommendations'):
            print("\n💡 Recommendations:")
            print("-" * 60)
            for rec in result.data['recommendations']:
                print(f"  • {rec}")

        print(f"\n✓ Comparison complete (Duration: {result.duration:.3f}s)")
    else:
        print(f"✗ Failed: {result.error}")


def demo_8_leaderboard():
    """Demo 8: Generate category leaderboards."""
    print_section("DEMO 8: Category Leaderboards")

    categories = ['overall', 'performance', 'reliability', 'quality']

    for category in categories:
        print(f"\n{category.upper()} Leaderboard:")
        print("-" * 60)

        result = operations.generate_leaderboard(
            category=category,
            time_period_days=7,
            top_n=5
        )

        if result.success:
            for entry in result.data['leaderboard']:
                print(f"{entry['rank']}. {entry['skill_name']}")
                print(f"   Score: {entry['score']:.1f}")
        else:
            print(f"   (No data available)")

        print()

    print("✓ All leaderboards generated")


def run_all_demos():
    """Run all Phase 6 demos."""
    print("\n" + "="*80)
    print("  SKILL EVALUATOR - PHASE 6 DEMONSTRATIONS")
    print("  Advanced Features: Cross-Skill Analysis & Benchmarking")
    print("="*80)

    # Setup test data first
    print_section("SETUP: Creating Test Data")
    setup_test_data()

    demos = [
        ("Skill Interaction Analysis", demo_1_skill_interactions),
        ("Dependency Chain Detection", demo_2_dependency_chains),
        ("Workflow Pattern Analysis", demo_3_workflow_patterns),
        ("Bottleneck Identification", demo_4_bottleneck_detection),
        ("Workflow Optimization Suggestions", demo_5_workflow_optimizations),
        ("Skill Benchmarking", demo_6_benchmarking),
        ("Head-to-Head Comparison", demo_7_skill_comparison),
        ("Category Leaderboards", demo_8_leaderboard)
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            print(f"\n\nRunning Demo {i}/{len(demos)}: {name}")
            time.sleep(0.3)  # Brief pause between demos
            demo_func()
        except Exception as e:
            print(f"\n✗ Demo {i} failed with error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("  ALL PHASE 6 DEMONSTRATIONS COMPLETE")
    print("="*80)
    print("\nPhase 6 Features Demonstrated:")
    print("  ✓ Cross-skill interaction analysis")
    print("  ✓ Dependency chain detection")
    print("  ✓ Workflow pattern recognition")
    print("  ✓ Bottleneck identification")
    print("  ✓ Workflow optimization suggestions")
    print("  ✓ Multi-skill benchmarking")
    print("  ✓ Head-to-head skill comparison")
    print("  ✓ Category-based leaderboards")


if __name__ == "__main__":
    run_all_demos()
