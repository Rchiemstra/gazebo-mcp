"""
Test suite for learning-analytics skill

Tests all major analytics functionality:
- Velocity calculation
- Struggle detection
- Checkpoint analysis
- Pattern detection
- Time estimation
- Recommendation generation
- Overall health determination
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.learning_analytics import (
    LearningAnalyzer,
    RecommendationPriority,
    StruggleIndicator
)
from skills.learning_plan_manager import LearningPlanManager

def print_header(title):
    """Print formatted test header"""
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def print_section(title):
    """Print formatted section header"""
    print(f"\n{title}")
    print("-" * 40)

# ============================================================================
# Test Setup
# ============================================================================

def setup():
    """Initialize managers and analyzer"""
    manager = LearningPlanManager()
    analyzer = LearningAnalyzer()
    return manager, analyzer

# ============================================================================
# Test 1: Basic Analysis
# ============================================================================

def test_basic_analysis():
    """Test basic plan analysis"""
    print_header("Test 1: Basic Analysis")

    manager, analyzer = setup()

    # Load a plan
    print("\n1. Loading learning plan...")
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print(f"✅ Loaded: {plan.metadata.title}")

    # Analyze
    print("\n2. Performing analysis...")
    analytics = analyzer.analyze_plan(plan)

    print(f"✅ Analysis complete")
    print(f"   Overall Health: {analytics.overall_health}")
    print(f"   Velocity: {analytics.velocity_metrics.tasks_per_week} tasks/week")
    print(f"   Struggle Areas: {len(analytics.struggle_areas)}")
    print(f"   Recommendations: {len(analytics.recommendations)}")

    # Verify structure
    assert analytics.plan_title == plan.metadata.title
    assert analytics.overall_health in ["excellent", "good", "needs_attention", "struggling"]
    assert analytics.velocity_metrics is not None
    assert analytics.checkpoint_analysis is not None

    return True

# ============================================================================
# Test 2: Velocity Calculation
# ============================================================================

def test_velocity_calculation():
    """Test velocity metrics calculation"""
    print_header("Test 2: Velocity Calculation")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Calculating velocity metrics...")
    velocity = analyzer.calculate_velocity(plan)

    print(f"✅ Velocity calculated")
    print(f"   Tasks per week: {velocity.tasks_per_week}")
    print(f"   Tasks completed: {velocity.tasks_completed_total}")
    print(f"   Days active: {velocity.days_active}")
    print(f"   Trend: {velocity.velocity_trend}")
    print(f"   Recent velocity: {velocity.recent_velocity}")
    print(f"   Overall velocity: {velocity.overall_velocity}")
    print(f"   On track: {velocity.on_track}")

    if velocity.estimated_completion_date:
        print(f"   Est. completion: {velocity.estimated_completion_date}")

    # Verify
    assert velocity.tasks_per_week >= 0
    assert velocity.tasks_completed_total >= 0
    assert velocity.velocity_trend in ["increasing", "stable", "decreasing", "unknown"]
    assert isinstance(velocity.on_track, bool)

    return True

# ============================================================================
# Test 3: Struggle Detection
# ============================================================================

def test_struggle_detection():
    """Test struggle area detection"""
    print_header("Test 3: Struggle Detection")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Detecting struggle areas...")
    struggles = analyzer.detect_struggle_areas(plan)

    print(f"✅ Found {len(struggles)} struggle area(s)")

    if struggles:
        print("\nStruggle Details:")
        for i, struggle in enumerate(struggles, 1):
            print(f"\n{i}. {struggle.task_title}")
            print(f"   Severity: {struggle.severity}")
            print(f"   Indicators: {[ind.value for ind in struggle.indicators]}")
            if struggle.duration_days:
                print(f"   Duration: {struggle.duration_days} days")
            print(f"   Recommendation: {struggle.recommendation}")
            if struggle.specialist_suggestion:
                print(f"   Specialist: {struggle.specialist_suggestion}")

            # Verify struggle structure
            assert struggle.severity in ["minor", "moderate", "severe"]
            assert len(struggle.indicators) > 0
    else:
        print("✅ No struggles detected (student doing well!)")

    return True

# ============================================================================
# Test 4: Checkpoint Analysis
# ============================================================================

def test_checkpoint_analysis():
    """Test checkpoint performance analysis"""
    print_header("Test 4: Checkpoint Analysis")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Analyzing checkpoints...")
    checkpoint_analysis = analyzer.analyze_checkpoints(plan)

    print(f"✅ Checkpoint analysis complete")
    print(f"   Total checkpoints: {checkpoint_analysis.total_checkpoints}")
    print(f"   Passed: {checkpoint_analysis.passed_checkpoints}")
    print(f"   Failed: {checkpoint_analysis.failed_checkpoints}")
    print(f"   Not attempted: {checkpoint_analysis.not_attempted_checkpoints}")
    print(f"   Pass rate: {checkpoint_analysis.pass_rate}%")
    print(f"   First-try pass rate: {checkpoint_analysis.first_try_pass_rate}%")

    if checkpoint_analysis.patterns:
        print(f"\nPatterns detected:")
        for pattern in checkpoint_analysis.patterns:
            print(f"   - {pattern}")

    # Verify
    total = (checkpoint_analysis.passed_checkpoints +
             checkpoint_analysis.failed_checkpoints +
             checkpoint_analysis.not_attempted_checkpoints)
    assert total == checkpoint_analysis.total_checkpoints
    assert 0 <= checkpoint_analysis.pass_rate <= 100
    assert 0 <= checkpoint_analysis.first_try_pass_rate <= 100

    return True

# ============================================================================
# Test 5: Pattern Detection
# ============================================================================

def test_pattern_detection():
    """Test learning pattern detection"""
    print_header("Test 5: Pattern Detection")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Detecting learning patterns...")
    patterns = analyzer.detect_patterns(plan)

    print(f"✅ Found {len(patterns)} pattern(s)")

    if patterns:
        print("\nPattern Details:")
        for i, pattern in enumerate(patterns, 1):
            print(f"\n{i}. {pattern.pattern_type.value}")
            print(f"   Confidence: {pattern.confidence:.2f}")
            print(f"   Description: {pattern.description}")
            print(f"   Impact: {pattern.impact}")
            print(f"   Recommendation: {pattern.recommendation}")
            print(f"   Evidence:")
            for evidence in pattern.evidence:
                print(f"     - {evidence}")

            # Verify pattern structure
            assert 0 <= pattern.confidence <= 1
            assert pattern.impact in ["positive", "neutral", "negative"]
    else:
        print("✅ No patterns detected yet (need more completed tasks)")

    return True

# ============================================================================
# Test 6: Time Estimation Analysis
# ============================================================================

def test_time_estimation():
    """Test time estimation accuracy analysis"""
    print_header("Test 6: Time Estimation Analysis")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Analyzing time estimates...")
    time_est = analyzer.analyze_time_estimates(plan)

    print(f"✅ Time estimation analysis complete")
    if time_est.estimated_total_weeks:
        print(f"   Estimated total: {time_est.estimated_total_weeks} weeks")
    print(f"   Actual so far: {time_est.actual_weeks_so_far} weeks")
    if time_est.projected_total_weeks:
        print(f"   Projected total: {time_est.projected_total_weeks} weeks")
    if time_est.estimation_accuracy:
        print(f"   Accuracy: {time_est.estimation_accuracy}")
    if time_est.variance_percentage:
        print(f"   Variance: {time_est.variance_percentage}%")

    if time_est.recommendations:
        print(f"\nRecommendations:")
        for rec in time_est.recommendations:
            print(f"   - {rec}")

    # Verify
    assert time_est.actual_weeks_so_far >= 0
    if time_est.estimation_accuracy:
        assert time_est.estimation_accuracy in ["accurate", "optimistic", "pessimistic"]

    return True

# ============================================================================
# Test 7: Recommendation Generation
# ============================================================================

def test_recommendations():
    """Test recommendation generation"""
    print_header("Test 7: Recommendation Generation")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Generating recommendations...")
    analytics = analyzer.analyze_plan(plan)
    recommendations = analytics.recommendations

    print(f"✅ Generated {len(recommendations)} recommendation(s)")

    if recommendations:
        print("\nRecommendation Details:")

        # Group by priority
        by_priority = {}
        for rec in recommendations:
            priority = rec.priority.value
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append(rec)

        for priority in ["critical", "high", "medium", "low"]:
            if priority in by_priority:
                print(f"\n{priority.upper()} Priority:")
                for rec in by_priority[priority]:
                    print(f"\n  • {rec.title}")
                    print(f"    Type: {rec.recommendation_type.value}")
                    print(f"    Rationale: {rec.rationale}")
                    print(f"    Action: {rec.suggested_action}")
                    if rec.target_agent:
                        print(f"    Target: {rec.target_agent}")

        # Verify recommendations are sorted by priority
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3
        }

        for i in range(len(recommendations) - 1):
            assert priority_order[recommendations[i].priority] <= priority_order[recommendations[i+1].priority], \
                "Recommendations not sorted by priority"

    else:
        print("✅ No recommendations (plan going well!)")

    return True

# ============================================================================
# Test 8: Overall Health Determination
# ============================================================================

def test_overall_health():
    """Test overall health determination"""
    print_header("Test 8: Overall Health Determination")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Analyzing overall learning health...")
    analytics = analyzer.analyze_plan(plan)

    print(f"✅ Overall Health: {analytics.overall_health}")

    # Show what contributed to health determination
    print("\nHealth Factors:")
    print(f"  Velocity trend: {analytics.velocity_metrics.velocity_trend}")
    print(f"  On track: {analytics.velocity_metrics.on_track}")
    print(f"  Severe struggles: {sum(1 for s in analytics.struggle_areas if s.severity == 'severe')}")
    print(f"  Critical recommendations: {sum(1 for r in analytics.recommendations if r.priority == RecommendationPriority.CRITICAL)}")

    # Verify health is valid
    assert analytics.overall_health in ["excellent", "good", "needs_attention", "struggling"]

    return True

# ============================================================================
# Test 9: Key Insights
# ============================================================================

def test_key_insights():
    """Test key insights extraction"""
    print_header("Test 9: Key Insights")

    manager, analyzer = setup()
    plan = manager.find_latest_plan()

    if not plan:
        print("⚠️  No plans found - skipping test")
        return False

    print("\n1. Extracting key insights...")
    analytics = analyzer.analyze_plan(plan)

    print(f"✅ Extracted {len(analytics.key_insights)} key insight(s)")

    if analytics.key_insights:
        print("\nKey Insights:")
        for i, insight in enumerate(analytics.key_insights, 1):
            print(f"  {i}. {insight}")

    print(f"\nStrengths ({len(analytics.strengths)}):")
    for strength in analytics.strengths:
        print(f"  ✓ {strength}")

    print(f"\nGrowth Areas ({len(analytics.growth_areas)}):")
    for area in analytics.growth_areas:
        print(f"  → {area}")

    # Verify
    assert len(analytics.key_insights) <= 5  # Should be top 5
    assert isinstance(analytics.strengths, list)
    assert isinstance(analytics.growth_areas, list)

    return True

# ============================================================================
# Test 10: Real Plan Analysis
# ============================================================================

def test_real_plan_analysis():
    """Test analysis on real learning plan"""
    print_header("Test 10: Real Plan Analysis")

    manager, analyzer = setup()

    print("\n1. Finding all available plans...")
    all_plans = manager.list_plans()

    if not all_plans:
        print("⚠️  No plans found - skipping test")
        return False

    print(f"✅ Found {len(all_plans)} plan(s)")

    # Analyze the first plan
    print("\n2. Analyzing first plan...")
    plan = manager.load_plan(all_plans[0]["file"])
    analytics = analyzer.analyze_plan(plan)

    print(f"\n✅ Complete Analysis Results:")
    print(f"\nPlan: {analytics.plan_title}")
    print(f"Health: {analytics.overall_health}")
    print(f"\nMetrics:")
    print(f"  • Velocity: {analytics.velocity_metrics.tasks_per_week} tasks/week")
    print(f"  • Trend: {analytics.velocity_metrics.velocity_trend}")
    print(f"  • Checkpoint pass rate: {analytics.checkpoint_analysis.pass_rate}%")
    print(f"  • Struggles: {len(analytics.struggle_areas)}")
    print(f"  • Patterns: {len(analytics.learning_patterns)}")
    print(f"  • Recommendations: {len(analytics.recommendations)}")

    # Export to JSON to verify serializability
    print("\n3. Testing JSON export...")
    json_output = analytics.model_dump_json(indent=2)
    print(f"✅ JSON export successful ({len(json_output)} bytes)")

    return True

# ============================================================================
# Main Test Runner
# ============================================================================

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Learning Analytics - Test Suite")
    print("="*60)

    tests = [
        ("Basic Analysis", test_basic_analysis),
        ("Velocity Calculation", test_velocity_calculation),
        ("Struggle Detection", test_struggle_detection),
        ("Checkpoint Analysis", test_checkpoint_analysis),
        ("Pattern Detection", test_pattern_detection),
        ("Time Estimation", test_time_estimation),
        ("Recommendations", test_recommendations),
        ("Overall Health", test_overall_health),
        ("Key Insights", test_key_insights),
        ("Real Plan Analysis", test_real_plan_analysis),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    if passed == total:
        print(f"\n✅ All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
