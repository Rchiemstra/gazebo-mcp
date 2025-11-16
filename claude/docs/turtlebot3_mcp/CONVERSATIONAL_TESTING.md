# Conversational Testing Interface

**Version:** 1.0
**Date:** 2025-11-11
**Goal:** Natural language testing - just describe what to test, the agent does the rest

---

## Overview

A conversational testing interface that allows you to simply **describe** what you want to test, and the system automatically:

1. ✅ **Generates test scenarios** from your description
2. ✅ **Builds test environments** (obstacles, lighting, terrain)
3. ✅ **Sets test conditions** (weather, failures, noise)
4. ✅ **Defines success criteria** (what "passing" means)
5. ✅ **Executes tests** (single or multiple robots)
6. ✅ **Reports results** (pass/fail, metrics, visualizations)

**No manual scenario creation. No configuration files. Just natural conversation.**

---

## Simple Interface

### The Single Function You Need

```python
from skills.ros2_gazebo.testing import run_test

# Just describe what you want to test
result = run_test("Test navigation through a cluttered warehouse")

# That's it! The agent:
# - Generates warehouse environment
# - Spawns obstacles
# - Creates navigation scenarios
# - Runs tests
# - Returns results
```

---

## How It Works

### Architecture

```
User Request (Natural Language)
    ↓
AI Test Planner (interprets intent)
    ↓
├─► Scenario Generator (creates test scenarios)
├─► Environment Builder (builds world + conditions)
├─► Success Criteria Definer (what should pass)
└─► Test Executor (runs everything)
    ↓
Results Reporter (generates report)
    ↓
Natural Language Summary
```

### AI Test Planner

The AI analyzes your request and extracts:

**From:** "Test navigation in low light with moving obstacles"

**Extracts:**
```python
{
    "test_type": "navigation",
    "environment": "indoor",
    "lighting": {"type": "low", "ambient": 0.2},
    "obstacles": {
        "static": {"count": 10, "pattern": "scattered"},
        "dynamic": {"count": 3, "speed": 0.3}
    },
    "robot_model": "burger",  # default
    "success_criteria": {
        "goal_reached": True,
        "no_collisions": True,
        "completion_time_max": 120
    }
}
```

Then automatically builds and executes everything.

---

## Usage Examples

### Example 1: Basic Navigation Test

```python
from skills.ros2_gazebo.testing import run_test

# Simple request
result = run_test("Test basic navigation")

# Agent automatically:
# - Creates empty world
# - Spawns TurtleBot3 Burger
# - Sets goal 5m away
# - Runs test
# - Reports: PASS (reached goal in 12.3s)

print(f"Result: {result.status}")
print(f"Time: {result.duration}s")
```

**Console Output:**
```
🔧 Building test environment...
   ✓ World: empty
   ✓ Robot: TurtleBot3 Burger spawned at (0, 0)
   ✓ Goal: (5, 0)

🚀 Running test: Basic Navigation
   → Robot moving...
   ✓ Goal reached in 12.3s

✅ PASS
   Duration: 12.3s
   Distance: 5.02m
   Path efficiency: 99.6%
```

---

### Example 2: Obstacle Avoidance

```python
result = run_test("Test obstacle avoidance with 20 random obstacles")

# Agent automatically:
# - Creates world
# - Spawns 20 random obstacles (boxes, cylinders)
# - Creates navigation path through obstacles
# - Runs test
# - Reports collision avoidance success

print(f"Obstacles avoided: {result.metrics.obstacles_avoided}")
print(f"Collisions: {result.metrics.collisions}")
```

**Console Output:**
```
🔧 Building test environment...
   ✓ World: 10m × 10m arena
   ✓ Obstacles: 20 random (12 boxes, 8 cylinders)
   ✓ Robot: TurtleBot3 Burger at (-4, -4)
   ✓ Goal: (4, 4)

🚀 Running test: Obstacle Avoidance
   → Navigating through obstacles...
   ✓ Goal reached

✅ PASS
   Obstacles avoided: 20
   Collisions: 0
   Near misses: 3 (min distance: 0.31m)
   Path efficiency: 73.2%
```

---

### Example 3: Environmental Conditions

```python
result = run_test("""
Test navigation in harsh conditions:
- Very low lighting (night)
- Rough terrain
- Sensor noise
""")

# Agent automatically:
# - Sets ambient light to 0.1
# - Adds terrain roughness
# - Injects 5% sensor noise
# - Runs test
# - Validates performance degradation is acceptable

print(f"Success rate: {result.metrics.success_rate}")
print(f"Performance vs. baseline: {result.metrics.performance_ratio}")
```

**Console Output:**
```
🔧 Building test environment...
   ✓ Lighting: Night (ambient: 0.1)
   ✓ Terrain: Rough (roughness: 0.15)
   ✓ Sensors: 5% noise injection
   ✓ Robot: TurtleBot3 Burger

🚀 Running test: Harsh Conditions Navigation
   → Navigating in difficult conditions...
   ⚠ Slower than baseline (expected)
   ✓ Goal reached

✅ PASS (with degradation)
   Completion time: 45.2s (baseline: 12.3s, +267%)
   Path efficiency: 62% (baseline: 95%, -35%)
   Performance acceptable for conditions
```

---

### Example 4: Multi-Robot Coordination

```python
result = run_test("""
Test 5 robots coordinating to reach different goals
without colliding with each other
""")

# Agent automatically:
# - Spawns 5 TurtleBot3s
# - Assigns different goals
# - Enables collision avoidance
# - Runs coordination test
# - Reports success

print(f"All goals reached: {result.all_goals_reached}")
print(f"Robot collisions: {result.metrics.robot_collisions}")
```

**Console Output:**
```
🔧 Building test environment...
   ✓ Robots: 5 TurtleBot3 Burgers in grid formation
   ✓ Goals: 5 different locations
   ✓ Collision avoidance: Enabled

🚀 Running test: Multi-Robot Coordination
   → Robot 1: Goal reached (18.2s)
   → Robot 2: Goal reached (21.5s)
   → Robot 3: Goal reached (19.8s)
   → Robot 4: Goal reached (23.1s)
   → Robot 5: Goal reached (20.6s)

✅ PASS
   All goals reached: Yes
   Robot-robot collisions: 0
   Average completion time: 20.6s
   Coordination efficiency: 87%
```

---

### Example 5: Comparative Testing

```python
result = run_test("""
Compare navigation performance of Burger, Waffle, and Waffle Pi
in a maze environment
""")

# Agent automatically:
# - Creates maze world
# - Tests all 3 robot models
# - Runs same scenario for each
# - Compares performance
# - Generates comparison report

print(result.comparison_table)
```

**Console Output:**
```
🔧 Building test environment...
   ✓ World: Maze (complexity: medium)
   ✓ Start: (0, 0)
   ✓ Goal: (8, 8)

🚀 Running comparative tests...
   Testing Burger... ✓ (42.3s)
   Testing Waffle... ✓ (38.7s)
   Testing Waffle Pi... ✓ (35.2s)

✅ ALL PASSED

📊 Comparison:
   Model      | Time    | Path Eff | Sensors Used
   -----------|---------|----------|-------------------
   Burger     | 42.3s   | 68%      | LiDAR
   Waffle     | 38.7s   | 71%      | LiDAR + Camera
   Waffle Pi  | 35.2s ✨ | 76% ✨    | LiDAR + RGB-D

   ✨ Best performer: Waffle Pi (17% faster than Burger)

   Key insight: Depth camera improves path planning by 8%
```

---

### Example 6: Regression Testing

```python
result = run_test("Run full regression suite and compare to baseline")

# Agent automatically:
# - Loads all regression scenarios
# - Executes complete suite
# - Compares to baseline results
# - Identifies regressions
# - Generates detailed report
```

**Console Output:**
```
🔧 Loading regression suite...
   ✓ Suite: Standard Regression
   ✓ Scenarios: 87
   ✓ Baseline: 2025-11-10

🚀 Running regression tests...
   [████████████████████████████████] 87/87 (100%)

   Duration: 28.4 minutes

✅ REGRESSION RESULTS

   Overall: 85/87 passed (97.7%)

   ⚠️ New Failures (2):
      - nav_narrow_corridor_02 (was passing)
      - multi_robot_coordination_03 (was passing)

   ✅ Previously Failing Now Pass (1):
      - perception_low_light_01

   📊 Performance Changes:
      Navigation avg time: 12.3s → 12.1s (-1.6% ✓)
      Memory usage: 245MB → 248MB (+1.2%)

   ⚠️ Action Required:
      Investigate 2 new failures before merge
```

---

### Example 7: Stress Testing

```python
result = run_test("""
Stress test: Find the maximum number of obstacles
the robot can handle before failing
""")

# Agent automatically:
# - Creates scenarios with increasing obstacle counts
# - Tests: 10, 25, 50, 100, 200, 500, 1000 obstacles
# - Finds breaking point
# - Reports maximum capacity

print(f"Max obstacles handled: {result.max_obstacles}")
print(f"Failure point: {result.failure_obstacle_count}")
```

**Console Output:**
```
🔧 Building stress test...
   ✓ Test type: Progressive obstacle density
   ✓ Obstacle counts: [10, 25, 50, 100, 200, 500, 1000]

🚀 Running stress tests...
   10 obstacles... ✓ (14.2s)
   25 obstacles... ✓ (18.7s)
   50 obstacles... ✓ (26.3s)
   100 obstacles... ✓ (45.8s)
   200 obstacles... ⚠ (89.2s, path efficiency: 45%)
   500 obstacles... ❌ (timeout after 120s)

   Test stopped at failure point

📊 STRESS TEST RESULTS

   Maximum obstacles: 200
   Failure point: 500 obstacles

   Performance degradation:
   10 → 100 obstacles: +223% time (acceptable)
   100 → 200 obstacles: +95% time (degraded)
   200 → 500 obstacles: TIMEOUT

   💡 Recommendation:
      Safe operating limit: 150 obstacles
      Performance degrades significantly above 200
```

---

## Advanced Requests

### Complex Scenarios

```python
result = run_test("""
Test delivery robot scenario:
- Start at warehouse (0, 0)
- Pick up package at station A (5, 3)
- Deliver to station B (8, -2)
- Return to warehouse
- Environment: Indoor with furniture obstacles
- Lighting: Office lighting with shadows
- Add 2 moving obstacles (people walking)
- Time limit: 5 minutes
""")
```

**The agent parses all requirements and executes automatically!**

---

### Failure Scenarios

```python
result = run_test("""
Test robustness:
- Start navigation to goal
- After 30 seconds, simulate LiDAR failure for 10 seconds
- Validate robot can continue with degraded sensors
- Success if goal reached despite sensor loss
""")
```

---

### Long-Duration Tests

```python
result = run_test("""
Run patrol scenario for 1 hour:
- 4 waypoints in square pattern
- Loop continuously
- Random obstacles appear every 5 minutes
- Validate no performance degradation over time
- Check for memory leaks
""")
```

---

## Natural Language API

### The Main Function

```python
def run_test(
    description: str,
    robot_model: str = "auto",  # auto, burger, waffle, waffle_pi
    world: str = "auto",         # auto, empty, house, warehouse, custom
    timeout: float = None,       # auto-determined if None
    visualize: bool = True,      # Show in Gazebo
    record: bool = False,        # Record rosbag
    report_format: str = "console"  # console, html, json
) -> TestResult:
    """
    Run test from natural language description.

    The description can include:
    - Test type (navigation, obstacle avoidance, SLAM, etc.)
    - Environment (warehouse, office, outdoor, etc.)
    - Conditions (lighting, weather, terrain, failures)
    - Obstacles (count, type, movement)
    - Success criteria (time limits, accuracy requirements)
    - Robot configuration (model, sensors)
    - Multi-robot scenarios

    Examples:
        run_test("Test navigation")
        run_test("Test in low light with 50 obstacles")
        run_test("Compare all robot models")
        run_test("Stress test with increasing obstacle density")

    Returns:
        TestResult with status, metrics, and report
    """
    pass
```

---

### Batch Testing

```python
def run_tests(
    descriptions: List[str],
    parallel: bool = True
) -> BatchTestResults:
    """
    Run multiple tests from descriptions.

    Example:
        results = run_tests([
            "Test navigation in warehouse",
            "Test obstacle avoidance",
            "Test SLAM mapping",
            "Test multi-robot coordination"
        ])
    """
    pass
```

---

### Test Suites

```python
def run_test_suite(suite_name: str) -> SuiteResults:
    """
    Run predefined test suite by name.

    Example:
        run_test_suite("quick")      # ~5 minutes
        run_test_suite("standard")   # ~30 minutes
        run_test_suite("full")       # ~2 hours
        run_test_suite("nightly")    # Everything
    """
    pass
```

---

## AI Test Planner Implementation

### Request Parser

```python
class TestRequestParser:
    """
    Parse natural language test requests.

    Extracts:
    - Test type
    - Environment requirements
    - Conditions
    - Success criteria
    - Robot configuration
    """

    def parse(self, description: str) -> TestSpecification:
        """
        Parse natural language description.

        Uses LLM to understand intent and extract structured data.
        """

        # Use Claude to parse the request
        prompt = f"""
        Parse this test request into structured format:

        "{description}"

        Extract:
        1. Test type (navigation, obstacle_avoidance, slam, multi_robot, etc.)
        2. Environment (type, size, obstacles)
        3. Conditions (lighting, terrain, weather, failures)
        4. Robot configuration (model, count, sensors)
        5. Success criteria (goals, time limits, accuracy)
        6. Special requirements

        Return JSON format.
        """

        # Get structured response from LLM
        response = call_llm(prompt)

        # Convert to TestSpecification
        spec = TestSpecification.from_json(response)

        return spec


@dataclass
class TestSpecification:
    """Structured test specification from natural language."""

    # Test type
    test_type: str  # "navigation", "obstacle_avoidance", etc.

    # Environment
    world_type: str = "empty"  # "empty", "warehouse", "office", etc.
    world_size: tuple = (10, 10)

    # Obstacles
    static_obstacles: ObstacleConfig = None
    dynamic_obstacles: ObstacleConfig = None

    # Conditions
    lighting: LightingConfig = None
    terrain: TerrainConfig = None
    weather: WeatherConfig = None
    failures: List[FailureConfig] = None

    # Robot configuration
    robot_model: str = "burger"
    robot_count: int = 1
    robot_positions: List[dict] = None

    # Goals
    goals: List[dict] = None
    waypoints: List[dict] = None

    # Success criteria
    success_criteria: SuccessCriteria = None

    # Constraints
    timeout: float = 120.0

    # Metadata
    description: str = ""
    tags: List[str] = None
```

---

### Automatic Environment Builder

```python
class AutoEnvironmentBuilder:
    """
    Automatically build test environment from specification.

    Creates:
    - Gazebo world
    - Obstacles
    - Lighting
    - Terrain
    - Initial conditions
    """

    def build(self, spec: TestSpecification) -> Environment:
        """Build complete test environment."""

        # 1. Create or load world
        world = self._create_world(spec.world_type, spec.world_size)

        # 2. Spawn obstacles
        if spec.static_obstacles:
            self._spawn_static_obstacles(spec.static_obstacles)

        if spec.dynamic_obstacles:
            self._spawn_dynamic_obstacles(spec.dynamic_obstacles)

        # 3. Set conditions
        if spec.lighting:
            self._set_lighting(spec.lighting)

        if spec.terrain:
            self._modify_terrain(spec.terrain)

        # 4. Spawn robot(s)
        robots = self._spawn_robots(
            spec.robot_model,
            spec.robot_count,
            spec.robot_positions
        )

        # 5. Set up goals
        if spec.goals:
            self._set_goals(spec.goals)

        return Environment(
            world=world,
            robots=robots,
            obstacles=self.obstacles,
            conditions=self.conditions
        )

    def _create_world(self, world_type: str, size: tuple):
        """Create appropriate world type."""

        world_templates = {
            "empty": self._create_empty_world,
            "warehouse": self._create_warehouse,
            "office": self._create_office,
            "outdoor": self._create_outdoor,
            "maze": self._create_maze
        }

        creator = world_templates.get(world_type, self._create_empty_world)
        return creator(size)

    def _create_warehouse(self, size: tuple):
        """Create warehouse-like environment."""
        # Rectangular space with shelf-like obstacles
        # Industrial lighting
        # Smooth concrete floor
        pass

    def _create_office(self, size: tuple):
        """Create office-like environment."""
        # Cubicles and furniture
        # Office lighting
        # Carpet floor (higher friction)
        pass
```

---

### Intelligent Success Criteria

```python
class SuccessCriteriaDefiner:
    """
    Automatically define success criteria based on test type.

    Uses domain knowledge and best practices.
    """

    def define(
        self,
        test_type: str,
        spec: TestSpecification
    ) -> SuccessCriteria:
        """Define appropriate success criteria."""

        criteria_templates = {
            "navigation": self._navigation_criteria,
            "obstacle_avoidance": self._obstacle_avoidance_criteria,
            "slam": self._slam_criteria,
            "multi_robot": self._multi_robot_criteria,
            "perception": self._perception_criteria
        }

        definer = criteria_templates.get(
            test_type,
            self._default_criteria
        )

        return definer(spec)

    def _navigation_criteria(self, spec: TestSpecification):
        """Success criteria for navigation tests."""

        return SuccessCriteria(
            # Primary
            goal_reached=True,
            position_tolerance=0.1,  # 10cm
            orientation_tolerance=0.15,  # ~8.6 degrees

            # Safety
            no_collisions=True,
            min_obstacle_distance=0.25,  # 25cm safety margin

            # Performance
            completion_time_max=self._estimate_time(spec),
            path_efficiency_min=0.65,  # Path should be reasonably direct

            # Resource usage
            cpu_usage_max=80.0,  # percent
            memory_usage_max=512.0,  # MB

            # Robustness
            recovery_attempts_max=3
        )

    def _obstacle_avoidance_criteria(self, spec: TestSpecification):
        """Success criteria for obstacle avoidance tests."""

        obstacle_count = spec.static_obstacles.count if spec.static_obstacles else 0

        return SuccessCriteria(
            # Primary
            goal_reached=True,
            no_collisions=True,

            # Obstacle-specific
            obstacles_detected_min=obstacle_count * 0.9,  # Detect 90%+
            false_positive_max=obstacle_count * 0.1,  # <10% false positives

            # Safety margins based on obstacle density
            min_obstacle_distance=self._safe_distance(obstacle_count),

            # Performance (relaxed for more obstacles)
            path_efficiency_min=max(0.5, 0.85 - obstacle_count * 0.01),
            completion_time_max=60 + obstacle_count * 2  # +2s per obstacle
        )

    def _estimate_time(self, spec: TestSpecification) -> float:
        """Estimate reasonable completion time."""

        # Calculate distance to goal
        if spec.goals:
            goal = spec.goals[0]
            distance = math.sqrt(goal['x']**2 + goal['y']**2)
        else:
            distance = 5.0  # default

        # Base time (assuming 0.15 m/s average speed)
        base_time = distance / 0.15

        # Add overhead for obstacles
        if spec.static_obstacles:
            base_time *= (1 + spec.static_obstacles.count * 0.05)

        # Add overhead for conditions
        if spec.lighting and spec.lighting.ambient < 0.3:
            base_time *= 1.5  # 50% slower in dark

        if spec.terrain and spec.terrain.roughness > 0.1:
            base_time *= 1.3  # 30% slower on rough terrain

        return base_time * 1.5  # 50% safety margin
```

---

## Example Conversations

### Conversation 1: Iterative Testing

```
User: "Test navigation"

Agent: 🔧 Building test environment...
       ✓ World: empty
       ✓ Robot: TurtleBot3 Burger
       ✓ Goal: 5m forward

       🚀 Running test...
       ✅ PASS (12.3s)

User: "Now test with obstacles"

Agent: 🔧 Adding obstacles to current environment...
       ✓ Obstacles: 10 random boxes

       🚀 Running test...
       ✅ PASS (23.7s, all obstacles avoided)

User: "Make it harder - 50 obstacles"

Agent: 🔧 Increasing obstacle count...
       ✓ Obstacles: 50 random (boxes, cylinders)

       🚀 Running test...
       ⚠️ PASS with warnings (89.2s)

       Path efficiency: 45% (below 65% threshold)
       Near misses: 12 (minimum distance: 0.26m)

       💡 Performance degraded significantly.
          Consider reducing obstacles or increasing area.

User: "Run with Waffle Pi instead"

Agent: 🔧 Switching robot model...
       ✓ Robot: TurtleBot3 Waffle Pi (with RGB-D)

       🚀 Running test...
       ✅ PASS (67.3s)

       📊 Comparison with Burger:
          Time: 67.3s vs 89.2s (24% faster ✨)
          Path efficiency: 58% vs 45% (29% better ✨)

       💡 Depth camera significantly improves navigation
          in cluttered environments!
```

---

### Conversation 2: Finding Limits

```
User: "Find the maximum obstacle density the robot can handle"

Agent: 🔧 Setting up stress test...
       ✓ Test: Progressive obstacle density
       ✓ Counts: [10, 25, 50, 100, 200, 500]

       🚀 Running stress tests...
       [████████████████████████████████] 6/6

       📊 RESULTS:

       10: ✓ 14.2s
       25: ✓ 18.7s
       50: ✓ 26.3s
       100: ✓ 45.8s
       200: ⚠️ 89.2s (degraded)
       500: ❌ TIMEOUT

       💡 Maximum: 200 obstacles
          Safe limit: 150 obstacles

       Would you like to test intermediate values (250, 300, 400)
       to find exact failure point?

User: "Yes"

Agent: 🚀 Running refined tests...

       250: ❌ TIMEOUT (stuck after 73s)

       💡 Failure point is between 200-250 obstacles

       Final recommendation:
       - Safe operating limit: 150 obstacles
       - Maximum capability: 200 obstacles
       - Failure above: 250 obstacles
```

---

## Implementation

### Core Implementation

```python
# skills/ros2_gazebo/testing/conversational.py

from typing import Optional
from dataclasses import dataclass

def run_test(
    description: str,
    robot_model: str = "auto",
    world: str = "auto",
    timeout: float = None,
    visualize: bool = True,
    record: bool = False,
    report_format: str = "console"
) -> TestResult:
    """
    Run test from natural language description.
    """

    # 1. Parse request
    parser = TestRequestParser()
    spec = parser.parse(description)

    # 2. Apply overrides
    if robot_model != "auto":
        spec.robot_model = robot_model
    if world != "auto":
        spec.world_type = world
    if timeout:
        spec.timeout = timeout

    # 3. Define success criteria
    criteria_definer = SuccessCriteriaDefiner()
    spec.success_criteria = criteria_definer.define(spec.test_type, spec)

    # 4. Build environment
    env_builder = AutoEnvironmentBuilder()
    environment = env_builder.build(spec)

    # 5. Execute test
    executor = TestExecutor(visualize=visualize, record=record)
    result = executor.execute(spec, environment)

    # 6. Validate
    validator = TestValidator()
    validation = validator.validate(result, spec.success_criteria)
    result.validation = validation

    # 7. Generate report
    reporter = TestReporter(format=report_format)
    report = reporter.generate(result, spec)

    # 8. Print to console (if console format)
    if report_format == "console":
        print(report)

    return result


@dataclass
class TestResult:
    """Test execution result."""

    # Status
    status: str  # "pass", "fail", "warning"

    # Execution
    duration: float
    timestamp: float

    # Validation
    validation: ValidationResult

    # Metrics
    metrics: PerformanceMetrics

    # Environment
    specification: TestSpecification
    environment: Environment

    # Artifacts
    report: str = None
    rosbag_path: str = None
    video_path: str = None

    # Comparison (if available)
    baseline: TestResult = None
    comparison: ComparisonReport = None
```

---

## Benefits

### For Users

✅ **No configuration needed** - Just describe what you want
✅ **Natural language** - Talk like you would to a person
✅ **Automatic everything** - Environment, scenarios, validation
✅ **Intelligent defaults** - Sensible settings for all tests
✅ **Immediate feedback** - Clear console output
✅ **Easy iteration** - Refine tests conversationally

### For Developers

✅ **Rapid testing** - Test ideas in seconds
✅ **Comprehensive coverage** - AI generates diverse scenarios
✅ **Consistent results** - Automated criteria
✅ **Easy debugging** - Clear failure reporting
✅ **CI/CD friendly** - Simple single-line calls

### For Researchers

✅ **Experiment quickly** - Try ideas fast
✅ **Reproducible** - Same description = same test
✅ **Comparative** - Easy model/algorithm comparison
✅ **Scalable** - From quick tests to extensive suites

---

## Integration with Existing System

### Standalone Usage

```python
from skills.ros2_gazebo.testing import run_test

result = run_test("Test navigation in warehouse")
```

### With Existing Framework

```python
from skills.ros2_gazebo.testing import (
    run_test,
    generate_scenario_from_template,
    execute_scenario
)

# Natural language
quick_result = run_test("Test basic navigation")

# Or use manual scenario if needed
scenario = generate_scenario_from_template(...)
detailed_result = execute_scenario(scenario)
```

### In CI/CD

```bash
# .github/workflows/tests.yml

- name: Run Tests
  run: |
    python -c "
    from skills.ros2_gazebo.testing import run_test

    result = run_test('Run quick regression suite')
    exit(0 if result.status == 'pass' else 1)
    "
```

---

## Next Steps

1. **Implement TestRequestParser** (LLM-based parsing)
2. **Build AutoEnvironmentBuilder** (world creation)
3. **Create SuccessCriteriaDefiner** (intelligent criteria)
4. **Develop TestExecutor** (run tests)
5. **Add TestReporter** (formatted output)
6. **Test with examples** (validate parsing)
7. **Integrate with CI/CD** (automation)

---

## Summary

**Simple Goal:** Just say what you want to test

**System Does:**
1. ✅ Understands your request
2. ✅ Generates test scenarios
3. ✅ Builds environment
4. ✅ Sets conditions
5. ✅ Defines success criteria
6. ✅ Runs tests
7. ✅ Reports results

**Result:** Testing becomes as simple as having a conversation!

```python
# That's all you need:
result = run_test("Test navigation through a warehouse with moving obstacles in low light")

# The agent handles everything else!
```
