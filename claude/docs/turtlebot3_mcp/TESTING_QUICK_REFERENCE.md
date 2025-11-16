# Testing Quick Reference

**Just describe what you want to test - the agent does the rest!**

---

## The One Function You Need

```python
from skills.ros2_gazebo.testing import run_test

result = run_test("your test description here")
```

That's it! No configuration, no setup, no scenario files needed.

---

## Quick Examples

### Basic Tests

```python
# Simple navigation
run_test("Test navigation")

# With obstacles
run_test("Test navigation with 20 obstacles")

# Different environment
run_test("Test navigation in a warehouse")

# Specific robot
run_test("Test navigation with Waffle Pi")
```

### Environmental Conditions

```python
# Lighting
run_test("Test navigation in low light")
run_test("Test in complete darkness")
run_test("Test with varying lighting conditions")

# Terrain
run_test("Test on rough terrain")
run_test("Test on slippery surface")
run_test("Test going uphill")

# Weather
run_test("Test in foggy conditions")
run_test("Test with strong wind")
```

### Obstacle Scenarios

```python
# Static obstacles
run_test("Test with 50 random obstacles")
run_test("Test in cluttered warehouse")
run_test("Test in narrow corridors")

# Dynamic obstacles
run_test("Test with 5 moving obstacles")
run_test("Test with people walking around")
```

### Multi-Robot

```python
# Coordination
run_test("Test 5 robots coordinating to different goals")

# Formation
run_test("Test 3 robots moving in triangle formation")

# Collision avoidance
run_test("Test 10 robots in confined space without collisions")
```

### Comparisons

```python
# Compare models
run_test("Compare Burger, Waffle, and Waffle Pi performance")

# Compare conditions
run_test("Test navigation in normal vs low light")

# Before/after
run_test("Compare current navigation vs baseline")
```

### Stress Tests

```python
# Find limits
run_test("Find maximum obstacle density robot can handle")

# Long duration
run_test("Run patrol for 1 hour without degradation")

# Resource usage
run_test("Test memory usage with 100 robots")
```

### Failure Scenarios

```python
# Sensor failures
run_test("Test with LiDAR dropout for 10 seconds")

# Communication loss
run_test("Test navigation with intermittent network loss")

# Actuator faults
run_test("Test with one wheel 50% power")
```

### Regression

```python
# Quick check
run_test("Run quick regression suite")

# Full validation
run_test("Run full regression and compare to baseline")

# Specific feature
run_test("Test all navigation scenarios")
```

---

## Complex Scenarios

### Delivery Mission

```python
run_test("""
Test delivery robot:
- Start at warehouse (0, 0)
- Pick up at station A (5, 3)
- Deliver to station B (8, -2)
- Return to warehouse
- Environment: indoor with furniture
- Time limit: 5 minutes
""")
```

### Patrol Route

```python
run_test("""
Test security patrol:
- 4 waypoints in building perimeter
- Loop continuously for 30 minutes
- Random obstacles appear every 5 minutes
- Validate no performance degradation
""")
```

### Multi-Robot Warehouse

```python
run_test("""
Test warehouse automation:
- 10 robots picking and delivering
- 50 shelf obstacles
- Coordinated movement to avoid collisions
- Each robot completes 5 deliveries
- Success if all deliveries complete in 10 minutes
""")
```

---

## Understanding Results

### Console Output Format

```
🔧 Building test environment...
   ✓ World: warehouse
   ✓ Obstacles: 20 random
   ✓ Robot: TurtleBot3 Burger

🚀 Running test: Navigation in Warehouse
   → Robot navigating...
   ✓ Goal reached

✅ PASS
   Duration: 23.7s
   Distance: 8.2m
   Path efficiency: 73%
   Obstacles avoided: 20
   Collisions: 0
```

### Result Object

```python
result = run_test("Test navigation")

# Status
print(result.status)  # "pass", "fail", "warning"

# Metrics
print(result.metrics.duration)          # 23.7
print(result.metrics.distance_traveled) # 8.2
print(result.metrics.path_efficiency)   # 0.73
print(result.metrics.collisions)        # 0

# Validation
print(result.validation.passed)        # True
print(result.validation.failures)      # []
print(result.validation.warnings)      # []

# Artifacts
print(result.rosbag_path)   # "/tmp/test_12345.bag"
print(result.report_path)   # "/tmp/test_12345.html"
```

---

## Advanced Options

### Specify Robot Model

```python
run_test("Test navigation", robot_model="waffle_pi")
```

### Custom Timeout

```python
run_test("Test navigation", timeout=300.0)  # 5 minutes
```

### Record Data

```python
run_test("Test navigation", record=True)  # Saves rosbag
```

### Different Report Format

```python
run_test("Test navigation", report_format="html")  # or "json"
```

### No Visualization

```python
run_test("Test navigation", visualize=False)  # Headless
```

---

## Batch Testing

### Multiple Tests

```python
from skills.ros2_gazebo.testing import run_tests

results = run_tests([
    "Test navigation",
    "Test obstacle avoidance",
    "Test SLAM mapping",
    "Test multi-robot coordination"
])

# Check all passed
if all(r.status == "pass" for r in results):
    print("✅ All tests passed!")
```

### Parallel Execution

```python
results = run_tests([
    "Test Burger in warehouse",
    "Test Waffle in warehouse",
    "Test Waffle Pi in warehouse"
], parallel=True)  # Run simultaneously
```

---

## Test Suites

### Predefined Suites

```python
from skills.ros2_gazebo.testing import run_test_suite

# Quick (~5 min)
run_test_suite("quick")

# Standard (~30 min)
run_test_suite("standard")

# Full (~2 hours)
run_test_suite("full")

# Nightly (complete)
run_test_suite("nightly")
```

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Tests
  run: |
    python -c "
    from skills.ros2_gazebo.testing import run_test
    result = run_test('Run quick regression')
    exit(0 if result.status == 'pass' else 1)
    "
```

### Command Line

```bash
# Run test from command line
python -c "from skills.ros2_gazebo.testing import run_test; run_test('Test navigation')"

# With parameters
python -c "from skills.ros2_gazebo.testing import run_test; \
           result = run_test('Test navigation', robot_model='waffle'); \
           print(f'Status: {result.status}')"
```

---

## Tips

### Be Specific

```python
# ❌ Vague
run_test("Test robot")

# ✅ Specific
run_test("Test navigation through warehouse with 20 obstacles")
```

### Describe Conditions

```python
# ❌ Missing details
run_test("Test in bad conditions")

# ✅ Clear conditions
run_test("Test navigation in low light (20% ambient) with sensor noise")
```

### State Success Criteria

```python
# ❌ Unclear
run_test("Test if robot is fast")

# ✅ Clear
run_test("Test navigation completing in under 30 seconds")
```

### Include Context

```python
# ❌ No context
run_test("Test")

# ✅ With context
run_test("Test delivery scenario: warehouse pickup and delivery in 5 minutes")
```

---

## Common Patterns

### Find Breaking Point

```python
run_test("Find maximum obstacle count robot can handle")
```

### Compare Configurations

```python
run_test("Compare all robot models in maze environment")
```

### Validate Robustness

```python
run_test("Test navigation with random failures every 30 seconds for 5 minutes")
```

### Measure Performance

```python
run_test("Benchmark navigation speed across 10 random scenarios")
```

### Regression Check

```python
run_test("Run all navigation tests and compare to yesterday's baseline")
```

---

## Error Handling

### If Test Fails

```python
result = run_test("Test navigation")

if result.status == "fail":
    print("❌ Test failed")
    print(f"Reason: {result.validation.failures}")
    print(f"Suggestions: {result.validation.warnings}")

    # Get rosbag for debugging
    print(f"Recording: {result.rosbag_path}")
```

### Timeout Issues

```python
# Increase timeout
run_test("Complex navigation", timeout=600.0)  # 10 minutes
```

### Environment Issues

```python
# Simplify environment
run_test("Test navigation in empty world first")

# Then add complexity
run_test("Test navigation in empty world with 5 obstacles")
```

---

## Examples by Category

### Navigation
```python
run_test("Test point-to-point navigation")
run_test("Test waypoint following with 5 waypoints")
run_test("Test navigation around corners")
run_test("Test navigation through doorway")
```

### Obstacle Avoidance
```python
run_test("Test static obstacle avoidance")
run_test("Test dynamic obstacle avoidance")
run_test("Test in densely cluttered space")
run_test("Test narrow corridor navigation")
```

### SLAM
```python
run_test("Test SLAM mapping in house environment")
run_test("Test localization accuracy")
run_test("Test loop closure detection")
run_test("Test mapping large area")
```

### Perception
```python
run_test("Test LiDAR obstacle detection")
run_test("Test camera object recognition")
run_test("Test depth-based navigation")
run_test("Test sensor fusion accuracy")
```

### Multi-Robot
```python
run_test("Test 3-robot formation control")
run_test("Test robot-robot collision avoidance")
run_test("Test coordinated exploration")
run_test("Test load balancing across 10 robots")
```

---

## Summary

**Simple Testing:**
```python
run_test("describe what you want to test")
```

**The agent automatically:**
1. Understands your request
2. Generates scenarios
3. Builds environment
4. Sets conditions
5. Defines success criteria
6. Runs test
7. Reports results

**No configuration files. No manual setup. Just describe and run!**
