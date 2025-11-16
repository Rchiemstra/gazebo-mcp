"""
Integration Example: Using skill_evaluator through the skills system

This demonstrates how the skill_evaluator can be invoked through
the standard skills integration system, making it callable by
Claude Code or any other client.
"""

from skills.integration.skill_loader import SkillLoader
from skills.integration.skill_registry import SkillRegistry
from skills.integration.skill_invoker import SkillInvoker


def demonstrate_skill_invocation():
    """Demonstrate invoking skill_evaluator through the skills system."""

    print("="*80)
    print("  Skill Evaluator - Integration System Demo")
    print("="*80)

    # Step 1: Setup the skills system
    print("\n1. Setting up skills system...")
    registry = SkillRegistry()

    # Discover all skills (including skill-evaluator)
    discovered = registry.discover_skills()
    print(f"   ✓ Discovered {len(discovered)} skills")

    # Check if skill-evaluator is registered
    evaluator_metadata = registry.get_skill('skill-evaluator')
    if evaluator_metadata:
        print(f"   ✓ skill-evaluator found!")
        print(f"     Version: {evaluator_metadata.version}")
        print(f"     Operations: {len(evaluator_metadata.operations)}")
    else:
        print(f"   ✗ skill-evaluator not found in registry")
        return

    # Step 2: Create loader and invoker
    print("\n2. Creating skill loader and invoker...")
    loader = SkillLoader(registry)
    invoker = SkillInvoker(loader)
    print("   ✓ Ready to invoke skills")

    # Step 3: Invoke skill_evaluator operations
    print("\n3. Invoking skill-evaluator operations...\n")

    # Example 1: Monitor execution
    print("   Example 1: monitor_execution")
    print("   " + "-"*60)
    result1 = invoker.invoke(
        skill_name='skill-evaluator',
        operation='monitor_execution',
        params={
            'skill_name': 'test-orchestrator',
            'operation': 'run_tests',
            'parameters': {'test_path': 'tests/'}
        }
    )
    print(f"   Success: {result1.success}")
    print(f"   Duration: {result1.duration:.3f}s")
    if result1.success and result1.data:
        print(f"   Execution ID: {result1.data.get('execution_id', 'N/A')}")

    # Example 2: Evaluate quality
    print("\n   Example 2: evaluate_quality")
    print("   " + "-"*60)
    result2 = invoker.invoke(
        skill_name='skill-evaluator',
        operation='evaluate_quality',
        params={
            'skill_name': 'test-orchestrator',
            'execution_samples': 50
        }
    )
    print(f"   Success: {result2.success}")
    print(f"   Duration: {result2.duration:.3f}s")
    if result2.success and result2.data:
        print(f"   Health Score: {result2.data.get('health_score', 'N/A')}/100")

    # Example 3: Benchmark skills
    print("\n   Example 3: benchmark_skills")
    print("   " + "-"*60)
    result3 = invoker.invoke(
        skill_name='skill-evaluator',
        operation='benchmark_skills',
        params={
            'time_period_days': 7,
            'min_executions': 5
        }
    )
    print(f"   Success: {result3.success}")
    print(f"   Duration: {result3.duration:.3f}s")
    if result3.success and result3.data:
        print(f"   Skills Benchmarked: {result3.data.get('total_benchmarked', 'N/A')}")

    # Example 4: Generate report
    print("\n   Example 4: generate_report")
    print("   " + "-"*60)
    result4 = invoker.invoke(
        skill_name='skill-evaluator',
        operation='generate_report',
        params={
            'skill_name': 'test-orchestrator',
            'report_type': 'summary',
            'format': 'markdown'
        }
    )
    print(f"   Success: {result4.success}")
    print(f"   Duration: {result4.duration:.3f}s")
    if result4.success and result4.data:
        report = result4.data.get('report', '')
        print(f"   Report Preview: {report[:100]}...")

    # Step 4: Check metrics
    print("\n4. Skill invocation metrics...")
    print("   " + "-"*60)
    metrics = invoker.get_metrics('skill-evaluator')
    if metrics:
        print(f"   Total Invocations: {metrics.total_invocations}")
        print(f"   Success Rate: {(metrics.successful_invocations/metrics.total_invocations*100):.1f}%")
        print(f"   Avg Duration: {metrics.avg_duration:.3f}s")

    print("\n" + "="*80)
    print("  Integration Demo Complete!")
    print("="*80)
    print("\n✓ The skill-evaluator can be invoked through the skills system")
    print("✓ All operations are accessible via SkillInvoker")
    print("✓ Ready for integration with Claude Code or other clients")


if __name__ == "__main__":
    demonstrate_skill_invocation()
