# Phase 2: learning-analytics Skill - Implementation Plan

**Created**: 2025-10-19
**Status**: In Progress (~60% Complete)
**Target Completion**: 2-3 hours

---

## Executive Summary

Phase 2 implements the **learning-analytics** skill, which analyzes learning plan data to provide:
- Learning velocity tracking and trends
- Struggle area detection
- Checkpoint performance analysis
- Learning pattern recognition
- Time estimation accuracy analysis
- Actionable recommendations for teaching optimization

This skill builds directly on **learning-plan-manager** (Phase 1 ✅) and transforms learning coordination from reactive to proactive.

---

## Current Status

### ✅ Completed (60%)

1. **Technical Specification** ✅
   - Complete spec in `docs/LEARNING_ANALYTICS_TECHNICAL_SPEC.md`
   - 1,128 lines covering all aspects
   - Detailed algorithms, API design, examples

2. **Data Models** ✅
   - `skills/learning_analytics/models.py` (362 lines)
   - 7 main models fully implemented:
     - `VelocityMetrics`
     - `StruggleArea` + `StruggleIndicator`
     - `CheckpointAnalysis` + `CheckpointPerformance`
     - `LearningPattern`
     - `TimeEstimationAnalysis`
     - `LearningRecommendation`
     - `LearningAnalytics` (main output)
   - All Pydantic models with validation

3. **Core Analyzer** ✅
   - `skills/learning_analytics/analyzer.py` (808 lines)
   - `LearningAnalyzer` class fully implemented
   - All major methods complete:
     - `analyze_plan()` - Comprehensive analysis
     - `calculate_velocity()` - Velocity metrics
     - `detect_struggle_areas()` - Struggle detection
     - `analyze_checkpoints()` - Checkpoint analysis
     - `detect_patterns()` - Pattern detection
     - `analyze_time_estimates()` - Time estimation
     - `generate_recommendations()` - Recommendations
   - Helper methods for date parsing, health determination, insights

### ⏳ Remaining (40%)

1. **Package Setup** (5 minutes)
   - Create `__init__.py` to export classes
   - Ensure proper imports

2. **Skill Integration Guide** (20 minutes)
   - Create `skill.md` for agent integration
   - Document skill invocation patterns
   - Provide usage examples for agents

3. **User Documentation** (15 minutes)
   - Create `README.md` with user-facing docs
   - API reference
   - Usage examples

4. **Testing** (45 minutes)
   - Create `examples/test_learning_analytics.py`
   - 7-10 comprehensive tests
   - Test with real learning plans

5. **Agent Integration** (30 minutes)
   - Update `commands/continue-plan.md` to use analytics
   - Optionally update `learning-coordinator` agent

6. **Integration Demo** (15 minutes)
   - Add to `examples/skills_integration_demo.py`
   - Show analytics in action

---

## Implementation Roadmap

### Task 1: Package Setup (5 min)
**File**: `skills/learning_analytics/__init__.py`

```python
"""
Learning Analytics Skill

Analyzes learning plan data to provide insights, detect struggles,
and generate recommendations for teaching optimization.
"""

from .models import (
    # Enums
    StruggleIndicator,
    PatternType,
    RecommendationPriority,
    RecommendationType,

    # Models
    VelocityMetrics,
    StruggleArea,
    CheckpointAnalysis,
    CheckpointPerformance,
    LearningPattern,
    TimeEstimationAnalysis,
    LearningRecommendation,
    LearningAnalytics,
)

from .analyzer import LearningAnalyzer

__all__ = [
    # Enums
    "StruggleIndicator",
    "PatternType",
    "RecommendationPriority",
    "RecommendationType",

    # Models
    "VelocityMetrics",
    "StruggleArea",
    "CheckpointAnalysis",
    "CheckpointPerformance",
    "LearningPattern",
    "TimeEstimationAnalysis",
    "LearningRecommendation",
    "LearningAnalytics",

    # Analyzer
    "LearningAnalyzer",
]
```

---

### Task 2: Skill Integration Guide (20 min)
**File**: `skills/learning_analytics/skill.md`

**Contents**:
- Skill name and description
- Capabilities overview
- When agents should invoke it
- How it works (workflow)
- Output format (JSON examples)
- Usage examples for different agents
- Integration with learning-coordinator
- Best practices

**Template**: Follow same structure as `learning-plan-manager/skill.md`

---

### Task 3: User Documentation (15 min)
**File**: `skills/learning_analytics/README.md`

**Sections**:
1. Overview
2. Features
3. Dependencies
4. Installation
5. Usage
6. API Reference
7. Examples
8. Integration with Agents
9. Output Format
10. Performance

---

### Task 4: Comprehensive Testing (45 min)
**File**: `examples/test_learning_analytics.py`

**Tests** (7-10 tests):
1. **Test Basic Analysis** - Analyze a simple plan
2. **Test Velocity Calculation** - Various completion patterns
3. **Test Struggle Detection** - Tasks stuck for different durations
4. **Test Checkpoint Analysis** - Passed/failed checkpoints
5. **Test Pattern Detection** - Steady vs burst progress
6. **Test Time Estimation** - Accurate, optimistic, pessimistic
7. **Test Recommendations** - Priority and types
8. **Test Overall Health** - Health determination logic
9. **Test Edge Cases** - Empty plan, no completions
10. **Test Real Plan** - Analyze actual learning plan from `plans/`

**Test Structure**:
```python
from skills.learning_analytics import LearningAnalyzer
from skills.learning_plan_manager import LearningPlanManager

def test_velocity_calculation():
    """Test velocity metrics calculation"""
    manager = LearningPlanManager()
    plan = manager.load_plan("plans/...")

    analyzer = LearningAnalyzer()
    analytics = analyzer.analyze_plan(plan)

    assert analytics.velocity_metrics.tasks_per_week >= 0
    assert analytics.velocity_metrics.velocity_trend in ["increasing", "stable", "decreasing"]

def test_struggle_detection():
    """Test struggle area detection"""
    # Create or load plan with long-running tasks
    # Verify struggles detected with correct severity

def test_recommendations():
    """Test recommendation generation"""
    # Verify recommendations have correct priority
    # Verify critical issues flagged
```

---

### Task 5: Agent Integration (30 min)

#### Option A: Update continue-plan command
**File**: `commands/continue-plan.md`

Add section:
```markdown
### Using learning-analytics for Adaptive Teaching

**Use analytics to detect struggles:**
```
Skill(learning-analytics) with query:
"Analyze current plan and identify any struggles or areas needing attention"
```

**Response includes:**
- Struggle areas with severity
- Recommendations prioritized
- Overall learning health
- Velocity trends

**Act on insights:**
- If struggling: Offer specialist help
- If behind: Adjust pacing
- If excelling: Celebrate and advance
```

#### Option B: Create new learning-coordinator agent
**File**: `agents/learning-coordinator.md` (if it exists)

Add analytics integration instructions.

---

### Task 6: Integration Demo (15 min)
**File**: `examples/skills_integration_demo.py`

Add demo:
```python
def demo_learning_analytics():
    """Demo: Learning Analytics Skill"""
    print("\n" + "="*60)
    print("Demo 5: Learning Analytics")
    print("="*60)

    manager = LearningPlanManager()
    analyzer = LearningAnalyzer()

    plan = manager.find_latest_plan()
    if not plan:
        print("No plans found")
        return

    analytics = analyzer.analyze_plan(plan)

    print(f"\nPlan: {analytics.plan_title}")
    print(f"Overall Health: {analytics.overall_health}")
    print(f"\nVelocity: {analytics.velocity_metrics.tasks_per_week} tasks/week")
    print(f"Trend: {analytics.velocity_metrics.velocity_trend}")

    if analytics.struggle_areas:
        print(f"\n⚠️  Struggle Areas: {len(analytics.struggle_areas)}")
        for struggle in analytics.struggle_areas[:3]:
            print(f"  - {struggle.task_title} ({struggle.severity})")

    print(f"\nCheckpoint Pass Rate: {analytics.checkpoint_analysis.pass_rate}%")

    if analytics.recommendations:
        print(f"\nTop Recommendations:")
        for rec in analytics.recommendations[:3]:
            print(f"  [{rec.priority.value.upper()}] {rec.title}")
```

---

## Testing Strategy

### Unit Tests
- Test each analyzer method independently
- Use synthetic data for edge cases
- Verify calculations are correct

### Integration Tests
- Test with real learning plans from `plans/`
- Verify recommendations make sense
- Check health determination logic

### Performance Tests
- Analyze large plans (50+ tasks)
- Ensure < 1 second for typical plans
- Memory usage < 100MB

---

## Success Criteria

Phase 2 complete when:

- [x] Models fully implemented ✅
- [x] Analyzer fully implemented ✅
- [ ] __init__.py created
- [ ] skill.md created (agent integration guide)
- [ ] README.md created (user documentation)
- [ ] Tests created and passing (7+/7+)
- [ ] Integration demo added
- [ ] Agent integration (continue-plan updated)
- [ ] All files committed to git
- [ ] Documentation complete

**Target**: All checkboxes ✅

---

## Timeline Estimate

| Task | Estimated Time | Status |
|------|----------------|--------|
| Technical Spec | 1 hour | ✅ Complete |
| Data Models | 1 hour | ✅ Complete |
| Core Analyzer | 2 hours | ✅ Complete |
| __init__.py | 5 min | ⏳ Todo |
| skill.md | 20 min | ⏳ Todo |
| README.md | 15 min | ⏳ Todo |
| Tests | 45 min | ⏳ Todo |
| Agent Integration | 30 min | ⏳ Todo |
| Integration Demo | 15 min | ⏳ Todo |
| **TOTAL** | **~6 hours** | **60% done** |

**Remaining**: ~2-3 hours

---

## Files to Create/Modify

### New Files (6)
```
skills/learning_analytics/
├── __init__.py              (NEW - 50 lines)
├── skill.md                 (NEW - 400 lines)
└── README.md                (NEW - 300 lines)

examples/
└── test_learning_analytics.py  (NEW - 350 lines)
```

### Modified Files (2)
```
commands/
└── continue-plan.md         (MODIFY - add analytics section)

examples/
└── skills_integration_demo.py  (MODIFY - add demo 5)
```

**Total new lines**: ~1,100 lines (docs + tests)

---

## Dependencies

### Required (from Phase 1)
- ✅ `learning-plan-manager` skill
- ✅ `LearningPlan`, `Task`, `TaskStatus`, `CheckpointStatus` models

### Python Libraries
- ✅ `datetime` (standard library)
- ✅ `statistics` (standard library)
- ✅ `pydantic` (already in use)

**No new dependencies needed!**

---

## Risk Assessment

### Low Risk ✅
- Core implementation done
- No new dependencies
- Clear spec to follow
- Models validated

### Mitigations
- If tests fail: Debug with synthetic data first
- If integration issues: Test standalone before agent integration
- If performance issues: Profile and optimize

---

## Next Phase Preview

After Phase 2 completes, recommended Phase 3:

**interactive-diagram** skill (High Priority)
- Generate visual learning aids
- Use code-analysis data for architecture diagrams
- Use learning-analytics for progress visualization
- Major UX improvement
- Estimated: 4-5 hours

---

## Appendix: Example Analytics Output

```json
{
  "plan_title": "Navigation System - Learning Implementation Plan",
  "overall_health": "good",
  "velocity_metrics": {
    "tasks_per_week": 2.5,
    "velocity_trend": "stable",
    "on_track": true
  },
  "struggle_areas": [
    {
      "task_title": "Implement A* algorithm",
      "severity": "moderate",
      "recommendation": "Consider breaking into smaller pieces",
      "specialist_suggestion": "robotics-vision-navigator"
    }
  ],
  "checkpoint_analysis": {
    "pass_rate": 100.0,
    "first_try_pass_rate": 100.0
  },
  "recommendations": [
    {
      "priority": "high",
      "title": "Schedule A* algorithm review",
      "description": "Task taking 2x expected time"
    }
  ],
  "key_insights": [
    "Maintaining steady 2.5 tasks per week",
    "Strong conceptual understanding (100% checkpoint pass rate)",
    "Currently struggling with A* algorithm implementation"
  ]
}
```

---

**Plan Status**: Ready to implement remaining 40%

**Next Action**: Create __init__.py, then skill.md, then tests

---

*Implementation Plan End*
