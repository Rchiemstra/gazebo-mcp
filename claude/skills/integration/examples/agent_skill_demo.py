#!/usr/bin/env python3
"""
Agent-Skill Integration Demo

Demonstrates how agents interact with skills through the integration layer.
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from skills.integration import SkillRegistry, SkillLoader, SkillInvoker


def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_section(text):
    """Print formatted section."""
    print("\n" + "-" * 80)
    print(f"  {text}")
    print("-" * 80 + "\n")


def main():
    """Run the demonstration."""
    print_header("AGENT-SKILL INTEGRATION DEMONSTRATION")

    # ===================================================================
    # STEP 1: DISCOVER SKILLS
    # ===================================================================
    print_section("STEP 1: SKILL DISCOVERY")

    print("Initializing Skill Registry...")
    registry = SkillRegistry(skills_dir="skills")

    print("Discovering available skills...\n")
    skills = registry.discover_skills()

    print(f"✅ Discovered {len(skills)} skills:\n")
    for skill in skills:
        status_icon = "✅" if skill.activation == "manual" else "⚡"
        print(f"  {status_icon} {skill.name}")
        print(f"     {skill.description}")
        print(f"     Version: {skill.version} | Category: {skill.category or 'general'}")
        if skill.dependencies:
            print(f"     Dependencies: {', '.join(skill.dependencies)}")
        print()

    # ===================================================================
    # STEP 2: SKILL VALIDATION
    # ===================================================================
    print_section("STEP 2: SKILL VALIDATION")

    print("Validating skills...\n")
    for skill_name in registry.list_skills():
        validation = registry.validate_skill(skill_name)

        if validation.valid:
            print(f"✅ {skill_name}: VALID")
        else:
            print(f"❌ {skill_name}: INVALID")
            for error in validation.errors:
                print(f"   Error: {error}")

        if validation.warnings:
            for warning in validation.warnings:
                print(f"   ⚠️  Warning: {warning}")

    # ===================================================================
    # STEP 3: LOAD SKILLS
    # ===================================================================
    print_section("STEP 3: SKILL LOADING")

    print("Initializing Skill Loader...")
    loader = SkillLoader(registry)

    # Load test-orchestrator
    print("\nLoading test-orchestrator skill...")
    try:
        skill_instance = loader.load_skill("test-orchestrator")
        print(f"✅ Loaded: {skill_instance.name}")
        print(f"   Operations: {len(skill_instance.operations)}")
        if skill_instance.operations:
            for op_name in skill_instance.operations.keys():
                print(f"     - {op_name}")
    except Exception as e:
        print(f"❌ Failed to load: {e}")

    # ===================================================================
    # STEP 4: INVOKE SKILLS
    # ===================================================================
    print_section("STEP 4: SKILL INVOCATION")

    print("Initializing Skill Invoker...")
    invoker = SkillInvoker(loader)

    # Example 1: Analyze code
    print("\nExample 1: Analyze Payment Service\n")
    sample_file = "skills/test_orchestrator/examples/sample_payment_service.py"

    print(f"Agent: Invoke test-orchestrator to analyze {sample_file}")

    result = invoker.invoke(
        skill_name="test-orchestrator",
        operation="analyze_python_file",
        params={"file_path": sample_file}
    )

    if result.success:
        print(f"✅ Success! (took {result.duration:.2f}s)")
        print(f"\n📊 Results:")
        if result.data:
            for key, value in result.data.items():
                if isinstance(value, (int, float, str)):
                    print(f"   {key}: {value}")
    else:
        print(f"❌ Error: {result.error}")
        print(f"   Code: {result.error_code}")

    # Example 2: Generate tests
    print("\nExample 2: Generate Tests\n")

    print("Agent: Generate tests for the analyzed code")

    # For demo, we'll show the request format
    print("\nRequest:")
    print("  skill_name: test-orchestrator")
    print("  operation: generate_tests")
    print("  parameters:")
    print(f"    source_file: {sample_file}")
    print("    target_coverage: 80.0")

    print("\nNote: Full test generation requires proper skill API implementation")
    print("      See test-orchestrator/demo_enhanced.py for working example")

    # ===================================================================
    # STEP 5: BATCH INVOCATION
    # ===================================================================
    print_section("STEP 5: BATCH INVOCATION")

    print("Agent: Analyze multiple files in parallel\n")

    from skills.integration import SkillRequest

    requests = [
        SkillRequest(
            skill_name="test-orchestrator",
            operation="analyze_python_file",
            parameters={"file_path": sample_file}
        ),
    ]

    print(f"Submitting {len(requests)} requests...")
    results = invoker.invoke_batch(requests)

    print(f"\nResults:")
    for i, result in enumerate(results, 1):
        status = "✅" if result.success else "❌"
        print(f"  {status} Request {i}: {result.duration:.2f}s")

    # ===================================================================
    # STEP 6: METRICS
    # ===================================================================
    print_section("STEP 6: SKILL METRICS")

    print("Collecting metrics for test-orchestrator...\n")

    metrics = invoker.get_metrics("test-orchestrator")
    if metrics:
        print(f"📊 Test Orchestrator Metrics:")
        print(f"   Total invocations: {metrics.total_invocations}")
        print(f"   Successful: {metrics.successful_invocations}")
        print(f"   Failed: {metrics.failed_invocations}")
        print(f"   Success rate: {(1 - metrics.error_rate) * 100:.1f}%")
        print(f"   Average duration: {metrics.avg_duration:.2f}s")
        print(f"   Min duration: {metrics.min_duration:.2f}s")
        print(f"   Max duration: {metrics.max_duration:.2f}s")

        if metrics.errors_by_code:
            print(f"\n   Errors by code:")
            for code, count in metrics.errors_by_code.items():
                print(f"     {code}: {count}")
    else:
        print("No metrics available yet")

    # ===================================================================
    # STEP 7: SKILL CHAINING (Example Pattern)
    # ===================================================================
    print_section("STEP 7: SKILL CHAINING PATTERN")

    print("Example: How an agent orchestrates multiple skills\n")

    print("""
class FeatureImplementationAgent:
    def __init__(self, invoker):
        self.invoker = invoker

    def implement_feature(self, requirement):
        # Step 1: Analyze codebase
        analysis = self.invoker.invoke(
            "code-analysis",
            "analyze_codebase",
            {"path": "src/"}
        )

        # Step 2: Generate specification
        spec = self.generate_specification(requirement, analysis.data)

        # Step 3: Implement code
        code = self.generate_code(spec)

        # Step 4: Generate tests
        tests = self.invoker.invoke(
            "test-orchestrator",
            "generate_tests",
            {"source_code": code}
        )

        # Step 5: Validate quality
        quality = self.invoker.invoke(
            "test-orchestrator",
            "score_quality",
            {"test_code": tests.data["test_file"]}
        )

        # Step 6: Create PR
        if quality.data["overall_score"] > 70:
            pr = self.invoker.invoke(
                "pr-review-assistant",
                "create_pr",
                {
                    "changes": code,
                    "tests": tests.data,
                    "quality_score": quality.data
                }
            )
            return pr.data
        else:
            return {"error": "Quality score too low", "score": quality.data}
    """)

    print("\nThis pattern enables:")
    print("  ✅ Complex multi-step workflows")
    print("  ✅ Conditional logic based on results")
    print("  ✅ Quality gates")
    print("  ✅ Error handling at each step")

    # ===================================================================
    # STEP 8: ERROR HANDLING
    # ===================================================================
    print_section("STEP 8: ERROR HANDLING")

    print("Demonstrating error handling patterns...\n")

    # Try to invoke non-existent skill
    print("1. Non-existent skill:")
    result = invoker.invoke("non-existent-skill", "some_operation", {})
    print(f"   Status: {'✅' if result.success else '❌'}")
    print(f"   Error: {result.error}")
    print(f"   Code: {result.error_code}")

    # Try to invoke non-existent operation
    print("\n2. Non-existent operation:")
    result = invoker.invoke("test-orchestrator", "non_existent_op", {})
    print(f"   Status: {'✅' if result.success else '❌'}")
    print(f"   Error: {result.error}")
    print(f"   Code: {result.error_code}")

    print("\n3. Agent error handling pattern:")
    print("""
def safe_skill_invoke(invoker, skill, operation, params):
    result = invoker.invoke(skill, operation, params)

    if not result.success:
        if result.error_code == SkillError.SKILL_NOT_FOUND:
            return {"error": "Skill not available", "fallback": True}
        elif result.error_code == SkillError.TIMEOUT:
            return {"error": "Operation timed out", "retry": True}
        elif result.error_code == SkillError.INVALID_PARAMETERS:
            return {"error": f"Invalid params: {result.error}"}
        else:
            return {"error": "Unexpected error", "details": result.error}

    return result.data
    """)

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print_section("SUMMARY")

    print("Integration Layer Components:")
    print("  ✅ SkillRegistry - Discovered and validated skills")
    print("  ✅ SkillLoader - Dynamically loaded skills on demand")
    print("  ✅ SkillInvoker - Executed operations with error handling")
    print()

    print("Key Features Demonstrated:")
    print("  ✅ Automatic skill discovery")
    print("  ✅ Dependency resolution")
    print("  ✅ Standardized request/response protocol")
    print("  ✅ Error handling with specific error codes")
    print("  ✅ Performance metrics")
    print("  ✅ Batch invocation")
    print("  ✅ Skill chaining patterns")
    print()

    print("Agent Benefits:")
    print("  🚀 Easy skill integration")
    print("  🔌 Plug-and-play architecture")
    print("  📊 Built-in monitoring")
    print("  🛡️  Error resilience")
    print("  ⚡ High performance")
    print()

    print_header("DEMONSTRATION COMPLETE")

    return 0


if __name__ == "__main__":
    sys.exit(main())
