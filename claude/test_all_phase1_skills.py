"""
Test All Phase 1 Skills Integration

Comprehensive test of all Phase 1 skills with the operations interface.
"""

from skills.integration import SkillInvoker, SkillLoader, SkillRegistry

def test_all_skills():
    """Test all Phase 1 skills."""
    print("="*80)
    print("  PHASE 1 SKILLS INTEGRATION TEST")
    print("="*80)
    print()

    # Initialize integration layer
    registry = SkillRegistry('skills')
    skills = registry.discover_skills()
    loader = SkillLoader(registry)
    invoker = SkillInvoker(loader)

    print(f"✅ Discovered {len(skills)} total skills")
    print()

    # Phase 1 skills
    phase1_skills = {
        'test-orchestrator': ['analyze_file', 'generate_tests', 'analyze_coverage'],
        'refactor-assistant': ['detect_code_smells', 'suggest_refactorings', 'apply_refactoring', 'analyze_complexity'],
        'pr-review-assistant': ['review_pull_request', 'generate_review_comment', 'analyze_change_impact', 'check_pr_quality'],
        'dependency-guardian': ['analyze_dependencies', 'check_vulnerabilities', 'check_updates'],
        'spec-to-implementation': ['implement_from_spec', 'analyze_spec']
    }

    print("-" * 80)
    print("  SKILL DISCOVERY AND VALIDATION")
    print("-" * 80)
    print()

    for skill_name, expected_ops in phase1_skills.items():
        metadata = registry.get_skill(skill_name)
        if metadata:
            actual_ops = list(metadata.operations.keys())
            ops_match = set(expected_ops) == set(actual_ops)
            status = "✅" if ops_match else "⚠️"
            print(f"{status} {skill_name}")
            print(f"   Version: {metadata.version}")
            print(f"   Operations: {actual_ops}")
            if not ops_match:
                print(f"   Expected: {expected_ops}")
            print()
        else:
            print(f"❌ {skill_name}: NOT FOUND")
            print()

    print("-" * 80)
    print("  OPERATION INVOCATION TESTS")
    print("-" * 80)
    print()

    # Test 1: test-orchestrator analyze_file
    print("1️⃣  test-orchestrator.analyze_file")
    result = invoker.invoke(
        'test-orchestrator',
        'analyze_file',
        {'source_file': 'skills/test_orchestrator/examples/sample_payment_service.py'}
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Functions: {result.data.get('total_functions', 0)}")
        print(f"   Complexity: {result.data.get('total_complexity', 0)}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    # Test 2: refactor-assistant detect_code_smells
    print("2️⃣  refactor-assistant.detect_code_smells")
    result = invoker.invoke(
        'refactor-assistant',
        'detect_code_smells',
        {'file_path': 'skills/refactor_assistant/examples/legacy_code.py', 'severity_threshold': 'medium'}
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Total smells: {result.data.get('total_smells', 0)}")
        print(f"   By severity: {result.data.get('by_severity', {})}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    # Test 3: pr-review-assistant check_pr_quality
    print("3️⃣  pr-review-assistant.check_pr_quality")
    pr_changes = {
        'added': ['src/feature.py', 'tests/test_feature.py', 'README.md'],
        'modified': ['src/main.py'],
        'deleted': []
    }
    result = invoker.invoke(
        'pr-review-assistant',
        'check_pr_quality',
        {'pr_changes': pr_changes}
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Has tests: {result.data.get('has_tests')}")
        print(f"   Has docs: {result.data.get('has_documentation')}")
        print(f"   Quality score: {result.data.get('overall_quality_score')}/100")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    # Test 4: dependency-guardian analyze_dependencies
    print("4️⃣  dependency-guardian.analyze_dependencies")
    result = invoker.invoke(
        'dependency-guardian',
        'analyze_dependencies',
        {'project_path': 'skills/dependency_guardian', 'ecosystem': 'python'}
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Project: {result.data.get('project_path', 'unknown')}")
        print(f"   Ecosystem: {result.data.get('ecosystem', 'unknown')}")
        print(f"   Dependencies: {result.data.get('total_dependencies', 0)}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    print("-" * 80)
    print("  METRICS SUMMARY")
    print("-" * 80)
    print()

    for skill_name in phase1_skills.keys():
        metrics = invoker.get_metrics(skill_name)
        if metrics:
            print(f"📊 {skill_name}")
            print(f"   Invocations: {metrics.total_invocations}")
            print(f"   Success rate: {(1 - metrics.error_rate) * 100:.1f}%")
            if metrics.total_invocations > 0:
                print(f"   Avg duration: {metrics.avg_duration:.3f}s")
            print()

    print("="*80)
    print("  TEST COMPLETE")
    print("="*80)
    print()
    print("✅ All Phase 1 skills are operational and integrated!")
    print()


if __name__ == "__main__":
    test_all_skills()
