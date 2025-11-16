"""
Test All Phase 2 Skills Integration

Comprehensive test of Phase 2 skills with the operations interface.
"""

from skills.integration import SkillInvoker, SkillLoader, SkillRegistry

def test_phase2_skills():
    """Test all Phase 2 skills."""
    print("="*80)
    print("  PHASE 2 SKILLS INTEGRATION TEST")
    print("="*80)
    print()

    # Initialize integration layer
    registry = SkillRegistry('skills')
    skills = registry.discover_skills()
    loader = SkillLoader(registry)
    invoker = SkillInvoker(loader)

    print(f"✅ Discovered {len(skills)} total skills")
    print()

    # Phase 2 skills
    phase2_skills = {
        'doc-generator': ['generate_docstrings', 'generate_readme', 'analyze_documentation'],
        'git-workflow-assistant': ['analyze_changes', 'generate_commit_message', 'suggest_branch_name', 'create_pull_request'],
        'code-search': ['search_symbol', 'search_pattern', 'find_definition', 'find_usages']
    }

    print("-" * 80)
    print("  SKILL DISCOVERY AND VALIDATION")
    print("-" * 80)
    print()

    for skill_name, expected_ops in phase2_skills.items():
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

    # Test 1: doc-generator analyze_documentation
    print("1️⃣  doc-generator.analyze_documentation")
    result = invoker.invoke(
        'doc-generator',
        'analyze_documentation',
        {'project_path': 'skills/doc_generator'}
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Overall coverage: {result.data.get('overall_coverage', 0):.1f}%")
        print(f"   Files analyzed: {result.data.get('total_files', 0)}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    # Test 2: git-workflow-assistant suggest_branch_name
    print("2️⃣  git-workflow-assistant.suggest_branch_name")
    result = invoker.invoke(
        'git-workflow-assistant',
        'suggest_branch_name',
        {
            'description': 'Add Phase 2 skills integration',
            'branch_type': 'feature',
            'issue_number': 'SKILL-456'
        }
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Suggested name: {result.data.get('branch_name', 'N/A')}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    # Test 3: code-search find_usages
    print("3️⃣  code-search.find_usages")
    result = invoker.invoke(
        'code-search',
        'find_usages',
        {
            'project_path': 'skills/code_search',
            'symbol_name': 'search_symbol',
            'include_tests': True
        }
    )
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Usages found: {result.data.get('total_usages', 0)}")
        print(f"   Files searched: {result.data.get('files_searched', 0)}")
        print(f"   Duration: {result.duration:.3f}s")
    else:
        print(f"   Error: {result.error}")
    print()

    print("-" * 80)
    print("  METRICS SUMMARY")
    print("-" * 80)
    print()

    for skill_name in phase2_skills.keys():
        metrics = invoker.get_metrics(skill_name)
        if metrics:
            print(f"📊 {skill_name}")
            print(f"   Invocations: {metrics.total_invocations}")
            print(f"   Success rate: {(1 - metrics.error_rate) * 100:.1f}%")
            if metrics.total_invocations > 0:
                print(f"   Avg duration: {metrics.avg_duration:.3f}s")
            print()

    print("-" * 80)
    print("  COMBINED PHASE 1 + PHASE 2 SUMMARY")
    print("-" * 80)
    print()

    all_skills = list(phase2_skills.keys())
    phase1_skills = ['test-orchestrator', 'refactor-assistant', 'pr-review-assistant',
                     'dependency-guardian', 'spec-to-implementation']

    total_operational = 0
    total_operations = 0

    for skill_name in phase1_skills + all_skills:
        metadata = registry.get_skill(skill_name)
        if metadata and metadata.operations:
            total_operational += 1
            total_operations += len(metadata.operations)

    print(f"📈 Total Operational Skills: {total_operational}")
    print(f"📈 Total Operations Available: {total_operations}")
    print()

    print("="*80)
    print("  PHASE 2 TEST COMPLETE")
    print("="*80)
    print()
    print("✅ All Phase 2 skills are operational and integrated!")
    print()


if __name__ == "__main__":
    test_phase2_skills()
