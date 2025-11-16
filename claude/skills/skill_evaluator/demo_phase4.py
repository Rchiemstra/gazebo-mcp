"""
Phase 4 Demo: Automated Improvement Application

Demonstrates the safe application of improvements with:
- Risk assessment
- Backup creation
- Dry-run mode
- Approval gates
- Rollback capabilities
"""

from skills.skill_evaluator import operations
from skills.skill_evaluator.core.models import ImprovementSuggestion


def demo_1_dry_run_improvements():
    """Demo 1: Dry-run mode to preview changes without applying."""
    print("\n" + "="*80)
    print("DEMO 1: Dry-Run Mode - Preview Changes")
    print("="*80)

    # Create sample improvements
    improvements = [
        {
            'category': 'performance',
            'severity': 'medium',
            'description': 'Optimize database query by adding index',
            'expected_impact': 'Reduce query time by 50%',
            'confidence': 0.85,
            'can_auto_apply': True,
            'location': 'core/database.py:45'
        },
        {
            'category': 'quality',
            'severity': 'low',
            'description': 'Add docstring to helper function',
            'expected_impact': 'Improve code documentation',
            'confidence': 0.95,
            'can_auto_apply': True,
            'location': 'utils/helpers.py:23'
        }
    ]

    # Apply with dry-run mode
    result = operations.apply_improvements(
        skill_name='test-orchestrator',
        improvements=improvements,
        create_branch=False,
        run_tests=False,
        require_approval=False,
        dry_run=True
    )

    if result.success:
        data = result.data
        print(f"\n✓ Dry-run completed in {result.duration:.2f}s")
        print(f"  Total suggestions: {data['total_suggestions']}")
        print(f"  Would apply: {len(data['applied'])}")
        print(f"  Would fail: {len(data['failed'])}")

        print("\n  Changes that would be applied:")
        for item in data['applied']:
            print(f"    - [{item['risk_level']}] {item['description']}")
    else:
        print(f"\n✗ Dry-run failed: {result.error}")


def demo_2_risk_assessment():
    """Demo 2: Risk assessment with approval gates."""
    print("\n" + "="*80)
    print("DEMO 2: Risk Assessment - Approval Gates")
    print("="*80)

    # Create improvements with varying risk levels
    improvements = [
        # Low risk - documentation
        {
            'category': 'documentation',
            'severity': 'low',
            'description': 'Add missing docstrings',
            'expected_impact': 'Better code documentation',
            'confidence': 0.95,
            'can_auto_apply': True
        },
        # Medium risk - performance optimization
        {
            'category': 'performance',
            'severity': 'medium',
            'description': 'Cache expensive computation',
            'expected_impact': 'Reduce CPU usage by 30%',
            'confidence': 0.80,
            'can_auto_apply': False
        },
        # High risk - structural change
        {
            'category': 'reliability',
            'severity': 'critical',
            'description': 'Fix race condition in concurrent operations',
            'expected_impact': 'Eliminate intermittent failures',
            'confidence': 0.70,
            'can_auto_apply': False
        }
    ]

    # Apply with approval required
    result = operations.apply_improvements(
        skill_name='test-orchestrator',
        improvements=improvements,
        create_branch=True,
        run_tests=True,
        require_approval=True,
        dry_run=True  # Dry-run for demo
    )

    if result.success:
        data = result.data
        print(f"\n✓ Risk assessment completed in {result.duration:.2f}s")
        print(f"  Total suggestions: {data['total_suggestions']}")
        print(f"  Auto-applicable: {len(data['applied'])}")
        print(f"  Requiring approval: {len(data['requires_approval'])}")

        if data['applied']:
            print("\n  Auto-applicable improvements:")
            for item in data['applied']:
                print(f"    - [{item['risk_level'].upper()}] {item['description']}")

        if data['requires_approval']:
            print("\n  Improvements requiring manual approval:")
            for item in data['requires_approval']:
                print(f"    - [{item['risk_level'].upper()}] {item['description']}")
                print(f"      Reason: {item['reason']}")
    else:
        print(f"\n✗ Assessment failed: {result.error}")


def demo_3_backup_and_rollback():
    """Demo 3: Backup creation and rollback capabilities."""
    print("\n" + "="*80)
    print("DEMO 3: Backup and Rollback")
    print("="*80)

    from skills.skill_evaluator.core.improvement_applicator import ImprovementApplicator

    applicator = ImprovementApplicator()

    # List existing backups
    backups = applicator.list_backups()
    print(f"\n✓ Found {len(backups)} existing backups")

    if backups:
        print("\n  Recent backups:")
        for backup in backups[:3]:
            print(f"    - {backup['backup_id']}")
            print(f"      Created: {backup['created']}")
            print(f"      Size: {backup['size_mb']:.2f} MB")

    # Apply improvements with backup
    improvements = [
        {
            'category': 'quality',
            'severity': 'low',
            'description': 'Format code with black',
            'expected_impact': 'Consistent code formatting',
            'confidence': 0.95,
            'can_auto_apply': True
        }
    ]

    result = operations.apply_improvements(
        skill_name='test-orchestrator',
        improvements=improvements,
        create_branch=True,
        run_tests=False,
        require_approval=False,
        dry_run=True
    )

    if result.success:
        data = result.data
        if data.get('backup_id'):
            print(f"\n✓ Backup created: {data['backup_id']}")
            print(f"  Rollback available: {data['rollback_available']}")
            print(f"  Branch created: {data.get('branch_name', 'N/A')}")
        else:
            print("\n  (Dry-run mode - no backup created)")


def demo_4_apply_suggestions_from_evaluation():
    """Demo 4: Complete workflow - evaluate, suggest, apply."""
    print("\n" + "="*80)
    print("DEMO 4: Complete Workflow - Evaluate → Suggest → Apply")
    print("="*80)

    skill_name = 'test-orchestrator'

    # Step 1: Suggest improvements
    print(f"\nStep 1: Generating improvement suggestions for '{skill_name}'...")
    suggest_result = operations.suggest_improvements(
        skill_name=skill_name,
        focus_areas=['performance', 'reliability'],
        priority_threshold='medium',
        use_ai_agents=True
    )

    if not suggest_result.success:
        print(f"✗ Failed to generate suggestions: {suggest_result.error}")
        return

    suggestions_data = suggest_result.data
    print(f"✓ Generated {suggestions_data.get('total_suggestions', 0)} suggestions")
    print(f"  Filtered to {suggestions_data.get('filtered_suggestions', 0)} (priority: medium+)")
    print(f"  Auto-applicable: {len(suggestions_data.get('auto_applicable', []))}")

    if not suggestions_data.get('auto_applicable'):
        print("\n  No auto-applicable suggestions available")
        return

    # Step 2: Apply auto-applicable improvements
    print(f"\nStep 2: Applying auto-applicable improvements (dry-run)...")
    apply_result = operations.apply_improvements(
        skill_name=skill_name,
        improvements=suggestions_data['auto_applicable'],
        create_branch=True,
        run_tests=True,
        require_approval=True,
        dry_run=True
    )

    if apply_result.success:
        apply_data = apply_result.data
        print(f"✓ Application completed in {apply_result.duration:.2f}s")
        print(f"  Applied: {len(apply_data['applied'])}")
        print(f"  Failed: {len(apply_data['failed'])}")
        print(f"  Requires approval: {len(apply_data['requires_approval'])}")

        if apply_data['applied']:
            print("\n  Successfully applied:")
            for item in apply_data['applied'][:3]:
                print(f"    - {item['description']}")
    else:
        print(f"✗ Application failed: {apply_result.error}")


def demo_5_safety_gates():
    """Demo 5: Safety gate evaluation for different improvement types."""
    print("\n" + "="*80)
    print("DEMO 5: Safety Gates - Risk Assessment")
    print("="*80)

    from skills.skill_evaluator.core.improvement_applicator import SafetyGate
    from skills.skill_evaluator.core.models import ImprovementSuggestion

    # Create improvements with different risk profiles
    test_cases = [
        ImprovementSuggestion(
            category='documentation',
            severity='low',
            description='Add docstrings',
            expected_impact='Better docs',
            confidence=0.95,
            can_auto_apply=True
        ),
        ImprovementSuggestion(
            category='performance',
            severity='medium',
            description='Optimize loop',
            expected_impact='20% faster',
            confidence=0.75,
            can_auto_apply=False
        ),
        ImprovementSuggestion(
            category='reliability',
            severity='high',
            description='Fix memory leak',
            expected_impact='Stable memory usage',
            confidence=0.85,
            can_auto_apply=False
        ),
        ImprovementSuggestion(
            category='security',
            severity='critical',
            description='Fix SQL injection vulnerability',
            expected_impact='Eliminate security risk',
            confidence=0.90,
            can_auto_apply=False
        )
    ]

    print("\n  Risk Assessment Results:")
    for i, suggestion in enumerate(test_cases, 1):
        risk = SafetyGate.assess_risk(suggestion)
        print(f"\n  {i}. {suggestion.description}")
        print(f"     Category: {suggestion.category} | Severity: {suggestion.severity}")
        print(f"     Risk Level: {risk['risk_level'].upper()}")
        print(f"     Risk Score: {risk['risk_score']}/4")
        print(f"     Requires Approval: {'Yes' if risk['requires_approval'] else 'No'}")
        print(f"     Requires Testing: {'Yes' if risk['requires_testing'] else 'No'}")
        print(f"     Requires Review: {'Yes' if risk['requires_review'] else 'No'}")


def demo_6_rollback_operation():
    """Demo 6: Rollback demonstration."""
    print("\n" + "="*80)
    print("DEMO 6: Rollback Operation")
    print("="*80)

    from skills.skill_evaluator.core.improvement_applicator import ImprovementApplicator

    applicator = ImprovementApplicator()

    # List backups
    backups = applicator.list_backups(skill_name='test-orchestrator')

    if not backups:
        print("\n  No backups available for test-orchestrator")
        print("  (Create some by applying improvements first)")
        return

    print(f"\n✓ Found {len(backups)} backups for test-orchestrator")

    # Show most recent backup
    latest = backups[0]
    print(f"\n  Latest backup: {latest['backup_id']}")
    print(f"  Created: {latest['created']}")
    print(f"  Size: {latest['size_mb']:.2f} MB")

    # Note: We don't actually rollback in demo to avoid modifying the system
    print("\n  To rollback, use:")
    print(f"    applicator.rollback('{latest['backup_id']}')")


def run_all_demos():
    """Run all Phase 4 demos."""
    print("\n" + "#"*80)
    print("# PHASE 4 DEMONSTRATION: Automated Improvement Application")
    print("#"*80)
    print("\nDemonstrating safe improvement application with:")
    print("  • Risk assessment and safety gates")
    print("  • Backup creation and rollback")
    print("  • Dry-run mode for previewing changes")
    print("  • Approval gates for high-risk changes")
    print("  • Git integration (simulated)")
    print("  • Test validation integration points")

    # Run all demos
    demo_1_dry_run_improvements()
    demo_2_risk_assessment()
    demo_3_backup_and_rollback()
    demo_4_apply_suggestions_from_evaluation()
    demo_5_safety_gates()
    demo_6_rollback_operation()

    print("\n" + "#"*80)
    print("# Phase 4 demonstrations complete!")
    print("#"*80)
    print("\nKey Features Demonstrated:")
    print("  ✓ Dry-run mode for safe previewing")
    print("  ✓ Risk assessment with 4-level safety gates")
    print("  ✓ Automatic backup creation")
    print("  ✓ Rollback capabilities")
    print("  ✓ Approval gates for high-risk changes")
    print("  ✓ Complete evaluation → suggestion → application workflow")
    print("\nNote: Phase 4 uses simulation for git and test operations.")
    print("Full integration with git-workflow-assistant and test-orchestrator")
    print("will be completed in production deployment.")


if __name__ == '__main__':
    run_all_demos()
