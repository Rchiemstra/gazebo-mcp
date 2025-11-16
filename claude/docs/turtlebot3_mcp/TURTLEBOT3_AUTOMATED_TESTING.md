# TurtleBot3 Automated Testing Framework

**Version:** 1.0
**Date:** 2025-11-11
**Focus:** Automated testing, scenario generation, and regression validation

---

## Executive Summary

This document defines a comprehensive automated testing framework for TurtleBot3 robotics using the ROS2-Gazebo MCP server. The framework enables:

- **Test Scenario Generation**: Programmatically create diverse test environments
- **Environment Manipulation**: Dynamic obstacle spawning, lighting changes, terrain modification
- **Configuration Testing**: Validate all robot variants (Burger, Waffle, Waffle Pi)
- **Regression Testing**: Automated test suites for CI/CD pipelines
- **Performance Validation**: Benchmark behavior under various conditions
- **Reporting**: Detailed test results with metrics and visualizations

**Key Benefits:**
- 🔄 **Automated regression testing** across robot configurations
- 🎲 **Randomized scenario generation** for robust validation
- 📊 **Performance benchmarking** with detailed metrics
- 🔧 **CI/CD integration** for continuous validation
- 📈 **Trend analysis** over time
- ✅ **Pass/fail validation** with configurable thresholds

---

## Architecture Overview

```
mcp/servers/ros2-gazebo-mcp/
├── adapters/
│   └── testing.py                    # Testing operations
├── core/
│   ├── test_scenario_generator.py    # Scenario generation
│   ├── environment_manipulator.py    # Dynamic env changes
│   └── test_validator.py             # Result validation
├── tests/
│   ├── scenarios/                    # Test scenario definitions
│   │   ├── basic/                   # Basic movement tests
│   │   ├── navigation/              # Navigation tests
│   │   ├── perception/              # Sensor tests
│   │   ├── multi_robot/             # Multi-robot tests
│   │   └── stress/                  # Stress/edge case tests
│   ├── regression/                   # Regression test suites
│   │   ├── suite_basic.yaml
│   │   ├── suite_navigation.yaml
│   │   └── suite_full.yaml
│   ├── fixtures/                     # Test fixtures
│   │   ├── worlds/                  # Test world files
│   │   ├── maps/                    # Test maps
│   │   └── configs/                 # Test configurations
│   └── reports/                      # Test reports (generated)
└── config/
    └── testing/
        ├── thresholds.yaml          # Pass/fail thresholds
        ├── metrics.yaml             # Metric definitions
        └── environments.yaml        # Test environments

skills/ros2_gazebo/
└── testing/
    ├── SKILL.md                     # Testing skill
    ├── operations.py                # Testing operations
    └── examples.md                  # Testing examples
```

---

## Core Components

### 1. Test Scenario Generator (`core/test_scenario_generator.py`)

**Purpose**: Programmatically generate diverse test scenarios

```python
class TestScenarioGenerator:
    """
    Generate test scenarios for robot validation.

    Creates combinations of:
    - Robot configurations
    - Environmental conditions
    - Obstacle layouts
    - Lighting conditions
    - Terrain types
    """

    def generate_obstacle_scenario(
        self,
        world_size: tuple = (10, 10),
        obstacle_count: int = 10,
        obstacle_types: List[str] = None,
        random_seed: int = None
    ) -> Scenario:
        """
        Generate scenario with random obstacles.

        Args:
            world_size: (width, height) in meters
            obstacle_count: Number of obstacles to spawn
            obstacle_types: ["box", "cylinder", "wall", "cone"]
            random_seed: Seed for reproducibility

        Returns:
            Scenario with obstacle positions and properties
        """
        pass

    def generate_navigation_scenario(
        self,
        difficulty: str = "medium",  # "easy", "medium", "hard"
        corridor_width: float = 1.0,
        path_length: float = 10.0,
        include_dynamic_obstacles: bool = False
    ) -> Scenario:
        """
        Generate navigation challenge scenario.

        Creates:
        - Start and goal positions
        - Obstacles along path
        - Narrow passages
        - Dead ends (for hard difficulty)
        """
        pass

    def generate_multi_robot_scenario(
        self,
        robot_count: int = 3,
        area_size: tuple = (20, 20),
        shared_goals: bool = False,
        collision_risk: str = "medium"
    ) -> Scenario:
        """
        Generate multi-robot coordination scenario.

        Tests:
        - Robot-robot collision avoidance
        - Coordinated navigation
        - Resource conflicts
        """
        pass

    def generate_perception_scenario(
        self,
        sensor_type: str = "lidar",  # "lidar", "camera", "depth"
        occlusion_level: str = "low",
        clutter_level: str = "medium",
        lighting: str = "normal"
    ) -> Scenario:
        """
        Generate sensor/perception test scenario.

        Tests:
        - Sensor accuracy
        - Occlusion handling
        - Clutter robustness
        - Lighting variations
        """
        pass

    def generate_stress_scenario(
        self,
        stress_type: str = "obstacle_density",
        intensity: str = "high"
    ) -> Scenario:
        """
        Generate stress test scenario.

        Stress types:
        - "obstacle_density": Many obstacles in small space
        - "narrow_passages": Very tight corridors
        - "dynamic_obstacles": Moving obstacles
        - "sensor_noise": Degraded sensor data
        - "computation": Complex environment
        """
        pass

    def generate_regression_suite(
        self,
        coverage: str = "full"  # "quick", "standard", "full"
    ) -> List[Scenario]:
        """
        Generate complete regression test suite.

        Coverage levels:
        - quick: 10-15 scenarios, ~5 min
        - standard: 50-100 scenarios, ~30 min
        - full: 200+ scenarios, ~2 hours
        """
        pass


@dataclass
class Scenario:
    """Test scenario definition."""
    id: str
    name: str
    description: str

    # Environment
    world_file: str = None
    world_size: tuple = (10, 10)

    # Obstacles
    obstacles: List[Obstacle] = field(default_factory=list)

    # Robot configuration
    robot_model: str = "burger"
    robot_count: int = 1
    spawn_poses: List[dict] = field(default_factory=list)

    # Test parameters
    goals: List[dict] = field(default_factory=list)
    timeout: float = 60.0

    # Environmental conditions
    lighting: dict = None  # {ambient, directional, shadows}
    terrain: dict = None   # {friction, roughness, slope}
    physics: dict = None   # {gravity, time_step}

    # Success criteria
    success_conditions: List[str] = field(default_factory=list)

    # Metadata
    difficulty: str = "medium"
    tags: List[str] = field(default_factory=list)
    expected_duration: float = 60.0


@dataclass
class Obstacle:
    """Obstacle definition."""
    type: str  # "box", "cylinder", "sphere", "wall", "custom"
    pose: dict  # {x, y, z, roll, pitch, yaw}
    dimensions: dict  # {length, width, height} or {radius, height}
    is_static: bool = True
    velocity: dict = None  # For dynamic obstacles
    model_path: str = None  # For custom models
```

---

### 2. Environment Manipulator (`core/environment_manipulator.py`)

**Purpose**: Dynamically modify simulation environment during tests

```python
class EnvironmentManipulator:
    """
    Manipulate simulation environment in real-time.

    Enables dynamic testing by changing conditions during execution.
    """

    def __init__(self, gazebo_bridge: GazeboBridge):
        self.gazebo = gazebo_bridge

    # ========================================================================
    # Obstacle Manipulation
    # ========================================================================

    def spawn_obstacle(
        self,
        obstacle: Obstacle,
        obstacle_id: str = None
    ) -> str:
        """
        Spawn obstacle in simulation.

        Returns:
            Obstacle ID for later manipulation
        """
        pass

    def move_obstacle(
        self,
        obstacle_id: str,
        target_pose: dict,
        duration: float = 1.0
    ):
        """Move obstacle to new position over time."""
        pass

    def remove_obstacle(self, obstacle_id: str):
        """Remove obstacle from simulation."""
        pass

    def spawn_obstacle_pattern(
        self,
        pattern: str,  # "grid", "circle", "wall", "maze"
        params: dict
    ) -> List[str]:
        """
        Spawn multiple obstacles in pattern.

        Examples:
        - grid: {rows: 5, cols: 5, spacing: 1.0}
        - circle: {radius: 3.0, count: 8}
        - wall: {length: 5.0, height: 2.0, thickness: 0.1}
        - maze: {size: 10, complexity: 0.5}
        """
        pass

    def create_moving_obstacle(
        self,
        obstacle: Obstacle,
        path: List[dict],
        speed: float = 0.5,
        loop: bool = True
    ) -> str:
        """
        Create obstacle that moves along path.

        Useful for testing dynamic obstacle avoidance.
        """
        pass

    # ========================================================================
    # Lighting Manipulation
    # ========================================================================

    def set_ambient_light(self, intensity: float):
        """
        Set ambient light level (0.0 to 1.0).

        Tests:
        - Camera performance in low light
        - Vision algorithm robustness
        """
        pass

    def set_directional_light(
        self,
        direction: dict,  # {x, y, z}
        intensity: float,
        cast_shadows: bool = True
    ):
        """
        Set directional light (simulates sun).

        Tests:
        - Shadow handling
        - Glare/reflection robustness
        """
        pass

    def add_point_light(
        self,
        position: dict,
        intensity: float,
        color: dict = {"r": 1.0, "g": 1.0, "b": 1.0}
    ) -> str:
        """
        Add point light source.

        Tests:
        - Varying lighting conditions
        - Multiple light sources
        """
        pass

    def simulate_day_night_cycle(
        self,
        cycle_duration: float = 60.0,
        start_time: str = "noon"
    ):
        """
        Simulate day/night lighting cycle.

        Tests robot performance across lighting conditions.
        """
        pass

    # ========================================================================
    # Terrain Manipulation
    # ========================================================================

    def set_ground_friction(self, friction: float):
        """
        Modify ground friction (0.0 to 1.0).

        Tests:
        - Slippery surfaces
        - High-friction terrain
        - Traction loss scenarios
        """
        pass

    def add_terrain_slope(
        self,
        region: dict,  # {x_min, x_max, y_min, y_max}
        slope_angle: float,  # radians
        slope_direction: float  # radians
    ):
        """
        Add sloped terrain region.

        Tests:
        - Uphill/downhill navigation
        - Tilt sensor accuracy
        - Power consumption changes
        """
        pass

    def add_rough_terrain(
        self,
        region: dict,
        roughness: float = 0.1
    ):
        """
        Add rough/uneven terrain.

        Tests:
        - Odometry accuracy on rough terrain
        - Sensor noise handling
        - Stability
        """
        pass

    # ========================================================================
    # Physics Manipulation
    # ========================================================================

    def set_gravity(self, gravity: dict = {"x": 0, "y": 0, "z": -9.81}):
        """
        Modify gravity.

        Tests:
        - Low gravity scenarios
        - Different planetary conditions
        """
        pass

    def set_wind(
        self,
        velocity: dict,  # {x, y, z} m/s
        turbulence: float = 0.0
    ):
        """
        Add wind force.

        Tests:
        - External force resistance
        - Control stability
        """
        pass

    def inject_sensor_noise(
        self,
        sensor_topic: str,
        noise_type: str = "gaussian",
        noise_params: dict = {"mean": 0, "std": 0.01}
    ):
        """
        Add noise to sensor readings.

        Tests:
        - Sensor fusion robustness
        - Filtering algorithm effectiveness
        """
        pass

    # ========================================================================
    # Composite Operations
    # ========================================================================

    def apply_environment_preset(self, preset: str):
        """
        Apply predefined environment configuration.

        Presets:
        - "nominal": Standard testing conditions
        - "harsh": Difficult conditions (low light, rough terrain)
        - "extreme": Very challenging (sensor noise, wind, slopes)
        - "indoor": Indoor lighting, smooth terrain
        - "outdoor": Outdoor lighting, varied terrain
        """
        pass

    def randomize_environment(
        self,
        randomize_lighting: bool = True,
        randomize_obstacles: bool = True,
        randomize_terrain: bool = False,
        seed: int = None
    ):
        """
        Randomize environment for robustness testing.

        Creates unpredictable conditions to test adaptability.
        """
        pass
```

---

### 3. Test Validator (`core/test_validator.py`)

**Purpose**: Validate test results against criteria and thresholds

```python
class TestValidator:
    """
    Validate test execution results.

    Determines pass/fail based on configurable criteria.
    """

    def __init__(self, thresholds_config: str = "config/testing/thresholds.yaml"):
        self.thresholds = self._load_thresholds(thresholds_config)

    def validate_navigation_test(
        self,
        result: NavigationResult,
        scenario: Scenario
    ) -> ValidationResult:
        """
        Validate navigation test result.

        Checks:
        - Goal reached within tolerance
        - Completed within timeout
        - Path efficiency (actual vs. optimal)
        - Collisions avoided
        - Recovery behavior if failures
        """
        pass

    def validate_perception_test(
        self,
        result: PerceptionResult,
        ground_truth: dict
    ) -> ValidationResult:
        """
        Validate perception/sensor test.

        Checks:
        - Obstacle detection accuracy
        - False positive/negative rate
        - Detection latency
        - Confidence scores
        """
        pass

    def validate_motion_test(
        self,
        result: MotionResult,
        expected: dict
    ) -> ValidationResult:
        """
        Validate motion control test.

        Checks:
        - Position accuracy
        - Velocity accuracy
        - Response time
        - Overshoot/oscillation
        """
        pass

    def validate_multi_robot_test(
        self,
        results: List[NavigationResult],
        scenario: Scenario
    ) -> ValidationResult:
        """
        Validate multi-robot coordination test.

        Checks:
        - All robots reached goals
        - No inter-robot collisions
        - Coordination efficiency
        - Deadlock avoidance
        """
        pass

    def validate_performance_metrics(
        self,
        metrics: PerformanceMetrics,
        benchmark: dict = None
    ) -> ValidationResult:
        """
        Validate performance metrics.

        Checks:
        - Computational efficiency
        - Memory usage
        - Network bandwidth
        - Response times
        """
        pass

    def compare_regression(
        self,
        current_results: TestSuiteResults,
        baseline_results: TestSuiteResults,
        tolerance: float = 0.05
    ) -> RegressionReport:
        """
        Compare results against baseline for regression detection.

        Identifies:
        - Performance regressions
        - New failures
        - Improvements
        """
        pass


@dataclass
class ValidationResult:
    """Test validation result."""
    passed: bool
    score: float  # 0.0 to 1.0

    # Detailed results
    checks: List[CheckResult] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    # Failure information
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Metadata
    validation_time: float = 0.0


@dataclass
class CheckResult:
    """Individual check result."""
    name: str
    passed: bool
    expected: Any
    actual: Any
    threshold: Any = None
    message: str = ""
```

---

## Testing Operations API

### Testing Adapter (`adapters/testing.py`)

```python
"""
Automated testing operations for TurtleBot3.

High-level testing API for scenario execution and validation.
"""

# ============================================================================
# 1. Scenario Execution
# ============================================================================

def execute_scenario(
    scenario: Scenario,
    robot_config: dict = None,
    record: bool = True
) -> TestResult:
    """
    Execute single test scenario.

    Args:
        scenario: Scenario definition
        robot_config: Override robot configuration
        record: Record rosbag for playback

    Returns:
        TestResult with metrics and validation
    """
    pass

def execute_scenario_batch(
    scenarios: List[Scenario],
    parallel: bool = False,
    max_workers: int = 4
) -> List[TestResult]:
    """
    Execute multiple scenarios.

    Args:
        scenarios: List of scenarios
        parallel: Run scenarios in parallel (separate Gazebo instances)
        max_workers: Max parallel executions

    Returns:
        List of TestResults
    """
    pass

def execute_regression_suite(
    suite_file: str,
    robot_models: List[str] = ["burger", "waffle", "waffle_pi"],
    generate_report: bool = True
) -> RegressionResults:
    """
    Execute regression test suite.

    Tests all specified robot models against all scenarios in suite.

    Args:
        suite_file: Path to suite YAML
        robot_models: Robot variants to test
        generate_report: Create HTML/PDF report

    Returns:
        RegressionResults with pass/fail summary
    """
    pass


# ============================================================================
# 2. Scenario Generation
# ============================================================================

def generate_random_scenarios(
    count: int = 10,
    difficulty_range: tuple = ("easy", "hard"),
    scenario_types: List[str] = None,
    seed: int = None
) -> List[Scenario]:
    """
    Generate random test scenarios.

    Args:
        count: Number of scenarios
        difficulty_range: (min, max) difficulty
        scenario_types: ["navigation", "perception", "multi_robot"]
        seed: Random seed for reproducibility

    Returns:
        List of generated scenarios
    """
    pass

def generate_scenario_from_template(
    template: str,
    variations: dict
) -> List[Scenario]:
    """
    Generate scenario variations from template.

    Example:
        template = "navigation_corridor"
        variations = {
            "corridor_width": [0.5, 1.0, 1.5, 2.0],
            "obstacle_count": [0, 5, 10, 20]
        }
        # Generates 4x4=16 scenarios
    """
    pass


# ============================================================================
# 3. Environment Manipulation
# ============================================================================

def spawn_test_obstacles(
    obstacle_config: dict,
    world: str = "current"
) -> List[str]:
    """
    Spawn obstacles for testing.

    Args:
        obstacle_config: {
            "pattern": "grid" | "random" | "custom",
            "count": 10,
            "types": ["box", "cylinder"],
            "region": {"x": [-5, 5], "y": [-5, 5]}
        }

    Returns:
        List of obstacle IDs
    """
    pass

def modify_lighting(
    lighting_config: dict
):
    """
    Modify simulation lighting.

    Args:
        lighting_config: {
            "ambient": 0.5,  # 0-1
            "directional": {"intensity": 0.8, "direction": [0, 0, -1]},
            "shadows": True
        }
    """
    pass

def modify_terrain(
    terrain_config: dict
):
    """
    Modify terrain properties.

    Args:
        terrain_config: {
            "friction": 0.8,  # 0-1
            "roughness": 0.1,  # 0-1
            "slope": {"angle": 0.1, "direction": 0.0}  # radians
        }
    """
    pass

def inject_test_failures(
    failure_type: str,
    params: dict
):
    """
    Inject failures for robustness testing.

    Failure types:
    - "sensor_dropout": Simulate sensor failure
    - "communication_loss": Simulate network loss
    - "actuator_fault": Simulate motor issues
    - "computation_delay": Add processing latency
    """
    pass


# ============================================================================
# 4. Performance Benchmarking
# ============================================================================

def benchmark_navigation(
    robot_model: str,
    difficulty: str = "medium",
    iterations: int = 10
) -> BenchmarkResults:
    """
    Benchmark navigation performance.

    Measures:
    - Success rate
    - Average completion time
    - Path efficiency
    - CPU/memory usage
    """
    pass

def benchmark_perception(
    robot_model: str,
    sensor_type: str = "lidar",
    scenarios: List[Scenario] = None
) -> BenchmarkResults:
    """
    Benchmark perception performance.

    Measures:
    - Detection accuracy
    - Processing latency
    - False positive/negative rates
    - Resource usage
    """
    pass

def benchmark_multi_robot(
    robot_count: int,
    scenario_type: str = "coordination",
    iterations: int = 5
) -> BenchmarkResults:
    """
    Benchmark multi-robot performance.

    Measures:
    - Coordination efficiency
    - Collision avoidance success
    - Scalability (time vs. robot count)
    """
    pass

def compare_robot_models(
    scenarios: List[Scenario],
    models: List[str] = ["burger", "waffle", "waffle_pi"]
) -> ComparisonReport:
    """
    Compare performance across robot models.

    Generates comparative analysis of:
    - Success rates
    - Performance metrics
    - Strengths/weaknesses
    """
    pass


# ============================================================================
# 5. Regression Testing
# ============================================================================

def run_quick_regression() -> RegressionResults:
    """
    Run quick regression suite (~5 minutes).

    Essential tests only:
    - Basic movement
    - Sensor reading
    - Simple navigation
    """
    pass

def run_standard_regression() -> RegressionResults:
    """
    Run standard regression suite (~30 minutes).

    Comprehensive coverage:
    - All basic operations
    - Navigation scenarios
    - Multi-robot basics
    """
    pass

def run_full_regression() -> RegressionResults:
    """
    Run full regression suite (~2 hours).

    Complete validation:
    - All scenarios
    - All robot models
    - Stress tests
    - Edge cases
    """
    pass

def run_nightly_tests() -> RegressionResults:
    """
    Run nightly test suite.

    Extensive testing for overnight CI/CD:
    - Full regression
    - Performance benchmarks
    - Long-duration tests
    """
    pass


# ============================================================================
# 6. Test Reporting
# ============================================================================

def generate_test_report(
    results: TestSuiteResults,
    format: str = "html",  # "html", "pdf", "json", "junit"
    output_path: str = "reports/"
) -> str:
    """
    Generate test report.

    Includes:
    - Summary statistics
    - Pass/fail breakdown
    - Performance metrics
    - Visualizations
    - Failure details

    Returns:
        Path to generated report
    """
    pass

def generate_regression_report(
    current: RegressionResults,
    baseline: RegressionResults = None,
    format: str = "html"
) -> str:
    """
    Generate regression comparison report.

    Shows:
    - Changes from baseline
    - New failures
    - Performance changes
    - Trend analysis
    """
    pass

def export_metrics(
    results: TestSuiteResults,
    format: str = "prometheus"  # "prometheus", "influxdb", "json"
) -> str:
    """
    Export metrics for monitoring systems.

    Integration with:
    - Prometheus
    - InfluxDB
    - Grafana
    """
    pass


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class TestResult:
    """Single test execution result."""
    scenario_id: str
    robot_model: str

    # Execution
    success: bool
    duration: float
    timestamp: float

    # Validation
    validation: ValidationResult

    # Metrics
    metrics: PerformanceMetrics

    # Data
    rosbag_path: str = None
    log_path: str = None

    # Environment
    environment_config: dict = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """Performance metrics from test."""
    # Navigation metrics
    distance_traveled: float = 0.0
    path_efficiency: float = 0.0  # actual/optimal
    avg_velocity: float = 0.0
    max_velocity: float = 0.0

    # Perception metrics
    detection_accuracy: float = 0.0
    false_positives: int = 0
    false_negatives: int = 0
    avg_detection_latency: float = 0.0

    # Resource metrics
    avg_cpu_usage: float = 0.0
    max_cpu_usage: float = 0.0
    avg_memory_mb: float = 0.0
    max_memory_mb: float = 0.0

    # Timing metrics
    response_times: List[float] = field(default_factory=list)
    computation_times: dict = field(default_factory=dict)

    # Safety metrics
    collisions: int = 0
    near_misses: int = 0
    emergency_stops: int = 0


@dataclass
class RegressionResults:
    """Regression test suite results."""
    suite_name: str
    total_tests: int
    passed: int
    failed: int
    skipped: int

    # Results
    test_results: List[TestResult] = field(default_factory=list)

    # Comparison (if baseline provided)
    new_failures: List[str] = field(default_factory=list)
    new_passes: List[str] = field(default_factory=list)
    performance_changes: dict = field(default_factory=dict)

    # Summary
    total_duration: float = 0.0
    timestamp: float = 0.0

    # Artifacts
    report_path: str = None
    metrics_file: str = None


@dataclass
class BenchmarkResults:
    """Benchmark execution results."""
    benchmark_name: str
    robot_model: str
    iterations: int

    # Aggregate metrics
    success_rate: float  # 0-1
    avg_duration: float
    std_duration: float
    min_duration: float
    max_duration: float

    # Detailed metrics
    metrics: List[PerformanceMetrics] = field(default_factory=list)

    # Statistical analysis
    confidence_interval_95: tuple = None
    outliers: List[int] = field(default_factory=list)
```

---

## Test Suite Definitions

### Regression Suite Example (`tests/regression/suite_navigation.yaml`)

```yaml
# Navigation Regression Test Suite

name: "navigation_regression"
description: "Comprehensive navigation testing across robot configurations"
version: "1.0"
timeout: 1800  # 30 minutes

# Robot configurations to test
robot_models:
  - burger
  - waffle
  - waffle_pi

# Test scenarios
scenarios:
  # Basic navigation
  - id: "nav_basic_01"
    name: "Point-to-point navigation - Easy"
    type: "navigation"
    world: "empty"
    difficulty: "easy"
    start: {x: 0, y: 0, yaw: 0}
    goal: {x: 5, y: 0, yaw: 0}
    timeout: 60
    success_criteria:
      - "goal_reached"
      - "no_collisions"
      - "completion_time < 45"

  - id: "nav_basic_02"
    name: "Point-to-point navigation - Medium"
    type: "navigation"
    world: "world"
    difficulty: "medium"
    start: {x: -2, y: -2, yaw: 0}
    goal: {x: 2, y: 2, yaw: 0}
    obstacles: "random:10"
    timeout: 120
    success_criteria:
      - "goal_reached"
      - "no_collisions"
      - "path_efficiency > 0.7"

  # Waypoint navigation
  - id: "nav_waypoint_01"
    name: "Multi-waypoint navigation"
    type: "waypoint_navigation"
    world: "house"
    waypoints:
      - {x: 1, y: 0, yaw: 0}
      - {x: 1, y: 2, yaw: 1.57}
      - {x: -1, y: 2, yaw: 3.14}
      - {x: 0, y: 0, yaw: 0}
    timeout: 300
    success_criteria:
      - "all_waypoints_reached"
      - "no_collisions"

  # Obstacle avoidance
  - id: "nav_avoid_01"
    name: "Dynamic obstacle avoidance"
    type: "navigation"
    world: "empty"
    start: {x: -5, y: 0, yaw: 0}
    goal: {x: 5, y: 0, yaw: 0}
    dynamic_obstacles:
      - type: "box"
        path: [{x: 0, y: -3}, {x: 0, y: 3}]
        speed: 0.3
        loop: true
    timeout: 120
    success_criteria:
      - "goal_reached"
      - "no_collisions"
      - "maintained_safe_distance > 0.3"

  # Narrow passages
  - id: "nav_narrow_01"
    name: "Narrow corridor navigation"
    type: "navigation"
    world: "custom"
    corridor_width: 0.5  # Just wider than robot
    corridor_length: 5.0
    timeout: 90
    success_criteria:
      - "goal_reached"
      - "no_collisions"

  # Recovery behaviors
  - id: "nav_recovery_01"
    name: "Recovery from stuck situation"
    type: "navigation"
    world: "custom"
    start_in_corner: true
    goal: {x: 5, y: 5, yaw: 0}
    timeout: 150
    success_criteria:
      - "goal_reached"
      - "recovery_attempts < 5"

# Performance thresholds
thresholds:
  navigation:
    success_rate_min: 0.90  # 90% of tests must pass
    avg_completion_time_max: 120  # seconds
    path_efficiency_min: 0.65
    collision_count_max: 0

# Reporting
report:
  formats: ["html", "junit"]
  include_videos: true
  include_plots: true
  metrics:
    - "success_rate"
    - "completion_time"
    - "path_efficiency"
    - "cpu_usage"
    - "memory_usage"
```

---

## CI/CD Integration

### GitHub Actions Example (`.github/workflows/regression-tests.yml`)

```yaml
name: TurtleBot3 Regression Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Nightly at 2 AM

jobs:
  quick-regression:
    runs-on: ubuntu-22.04
    strategy:
      matrix:
        robot_model: [burger, waffle, waffle_pi]

    steps:
      - uses: actions/checkout@v3

      - name: Setup ROS2
        uses: ros-tooling/setup-ros@v0.6
        with:
          required-ros-distributions: humble

      - name: Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y ros-humble-turtlebot3* gazebo
          pip install -r requirements.txt

      - name: Run Quick Regression
        run: |
          export TURTLEBOT3_MODEL=${{ matrix.robot_model }}
          python -m pytest tests/regression/test_quick.py \
            --robot-model=${{ matrix.robot_model }} \
            --junit-xml=results/junit-${{ matrix.robot_model }}.xml \
            --html=results/report-${{ matrix.robot_model }}.html

      - name: Upload Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results-${{ matrix.robot_model }}
          path: results/

      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: results/junit-*.xml

  standard-regression:
    runs-on: ubuntu-22.04
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Setup ROS2
        uses: ros-tooling/setup-ros@v0.6
        with:
          required-ros-distributions: humble

      - name: Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y ros-humble-turtlebot3* gazebo
          pip install -r requirements.txt

      - name: Run Standard Regression
        run: |
          python tests/run_regression.py \
            --suite=standard \
            --report-format=html \
            --report-format=junit \
            --output-dir=results/

      - name: Upload Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: standard-regression-results
          path: results/

      - name: Check Regression
        run: |
          python tests/check_regression.py \
            --current=results/metrics.json \
            --baseline=baseline/metrics.json \
            --tolerance=0.05

  nightly-full-regression:
    runs-on: ubuntu-22.04
    if: github.event_name == 'schedule'
    timeout-minutes: 180  # 3 hours

    steps:
      - uses: actions/checkout@v3

      - name: Setup ROS2
        uses: ros-tooling/setup-ros@v0.6
        with:
          required-ros-distributions: humble

      - name: Install Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y ros-humble-turtlebot3* gazebo
          pip install -r requirements.txt

      - name: Run Full Regression
        run: |
          python tests/run_regression.py \
            --suite=full \
            --all-robot-models \
            --report-format=html \
            --report-format=junit \
            --output-dir=results/

      - name: Generate Trend Report
        run: |
          python tests/generate_trend_report.py \
            --results=results/ \
            --history=test-history/ \
            --output=results/trends.html

      - name: Upload Results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: nightly-regression-results
          path: results/

      - name: Notify on Failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Nightly regression tests failed!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Usage Examples

### Example 1: Generate and Execute Test Scenario

```python
from skills.ros2_gazebo.testing import (
    generate_random_scenarios,
    execute_scenario,
    generate_test_report
)

# Generate 5 random navigation scenarios
scenarios = generate_random_scenarios(
    count=5,
    difficulty_range=("medium", "hard"),
    scenario_types=["navigation"],
    seed=42  # Reproducible
)

# Execute each scenario
results = []
for scenario in scenarios:
    result = execute_scenario(
        scenario,
        robot_config={"model": "burger"},
        record=True  # Record rosbag
    )
    results.append(result)
    print(f"{scenario.name}: {'PASS' if result.success else 'FAIL'}")

# Generate HTML report
report_path = generate_test_report(
    results,
    format="html",
    output_path="./test_reports/"
)
print(f"Report generated: {report_path}")
```

### Example 2: Environment Manipulation During Test

```python
from skills.ros2_gazebo.testing import (
    spawn_test_obstacles,
    modify_lighting,
    execute_scenario
)
from skills.ros2_gazebo.turtlebot3 import quick_start_burger, navigate_to_goal
import time

# Start robot
robot = quick_start_burger("test_robot", world="empty")

# Spawn initial obstacles
obstacles = spawn_test_obstacles({
    "pattern": "random",
    "count": 10,
    "types": ["box", "cylinder"],
    "region": {"x": [0, 5], "y": [-2, 2]}
})

# Start navigation
navigate_to_goal("test_robot", goal_x=5, goal_y=0, timeout=120)

# After 30 seconds, change lighting
time.sleep(30)
modify_lighting({"ambient": 0.3})  # Dim lighting

# After 60 seconds, add more obstacles
time.sleep(30)
new_obstacles = spawn_test_obstacles({
    "pattern": "random",
    "count": 5,
    "region": {"x": [3, 5], "y": [-1, 1]}
})

# Test continues with new conditions...
```

### Example 3: Regression Testing

```python
from skills.ros2_gazebo.testing import (
    run_standard_regression,
    generate_regression_report,
    compare_regression
)

# Run current regression suite
current_results = run_standard_regression()

# Load baseline results
import json
with open("baseline/regression_results.json") as f:
    baseline_results = json.load(f)

# Compare
regression_report = generate_regression_report(
    current=current_results,
    baseline=baseline_results,
    format="html"
)

# Check for regressions
if current_results.new_failures:
    print("⚠️ NEW FAILURES DETECTED:")
    for failure in current_results.new_failures:
        print(f"  - {failure}")
else:
    print("✅ No regressions detected")

# Performance comparison
if current_results.performance_changes:
    print("\n📊 PERFORMANCE CHANGES:")
    for metric, change in current_results.performance_changes.items():
        if change > 0.05:  # 5% slower
            print(f"  ⚠️ {metric}: +{change*100:.1f}% (regression)")
        elif change < -0.05:  # 5% faster
            print(f"  ✅ {metric}: {change*100:.1f}% (improvement)")
```

### Example 4: Benchmarking Robot Models

```python
from skills.ros2_gazebo.testing import (
    compare_robot_models,
    generate_random_scenarios
)

# Generate test scenarios
scenarios = generate_random_scenarios(
    count=20,
    difficulty_range=("easy", "hard"),
    scenario_types=["navigation", "perception"]
)

# Compare all three models
comparison = compare_robot_models(
    scenarios=scenarios,
    models=["burger", "waffle", "waffle_pi"]
)

# Print results
print("\n📊 ROBOT MODEL COMPARISON:")
print(f"\n{'Model':<15} {'Success Rate':<15} {'Avg Time':<15} {'Avg CPU %':<15}")
print("-" * 60)
for model, stats in comparison.model_stats.items():
    print(f"{model:<15} {stats.success_rate:>14.1%} {stats.avg_time:>14.2f}s {stats.avg_cpu:>14.1f}%")

# Detailed comparison report
report_path = comparison.generate_report(format="html")
print(f"\nDetailed report: {report_path}")
```

### Example 5: Stress Testing

```python
from skills.ros2_gazebo.testing import (
    generate_scenario_from_template,
    execute_scenario_batch
)

# Generate stress test scenarios with increasing difficulty
stress_scenarios = generate_scenario_from_template(
    template="obstacle_density",
    variations={
        "obstacle_count": [10, 25, 50, 100, 200],
        "area_size": [(10, 10), (10, 10), (10, 10), (10, 10), (10, 10)]
    }
)

# Execute all scenarios
results = execute_scenario_batch(
    scenarios=stress_scenarios,
    parallel=False  # Sequential for fair comparison
)

# Analyze breaking point
for i, result in enumerate(results):
    scenario = stress_scenarios[i]
    status = "PASS" if result.success else "FAIL"
    print(f"Obstacles: {scenario.obstacles.count:3d} - {status} " +
          f"(time: {result.duration:.1f}s, " +
          f"CPU: {result.metrics.avg_cpu_usage:.1f}%)")

# Find where robot starts failing
failure_point = next((i for i, r in enumerate(results) if not r.success), len(results))
if failure_point < len(results):
    print(f"\n⚠️ Robot fails at {stress_scenarios[failure_point].obstacles.count} obstacles")
else:
    print(f"\n✅ Robot handled all obstacle densities up to {stress_scenarios[-1].obstacles.count}")
```

---

## Implementation Priority

### Phase 1: Core Testing Framework (Week 1-2)
- [ ] Test scenario data structures
- [ ] Basic scenario execution
- [ ] Environment manipulator (obstacles)
- [ ] Test validator (basic checks)
- [ ] Simple report generation

**Deliverables:**
- Execute custom scenarios
- Spawn/remove obstacles
- Validate pass/fail
- Generate JSON reports

### Phase 2: Scenario Generation (Week 3)
- [ ] Random scenario generator
- [ ] Template-based generation
- [ ] Obstacle patterns
- [ ] Difficulty scaling

**Deliverables:**
- Generate navigation scenarios
- Create obstacle layouts
- Randomized testing

### Phase 3: Environment Manipulation (Week 4)
- [ ] Lighting control
- [ ] Terrain modification
- [ ] Physics manipulation
- [ ] Sensor noise injection

**Deliverables:**
- Dynamic lighting changes
- Terrain slopes/friction
- Robust environment testing

### Phase 4: Regression Testing (Week 5)
- [ ] Regression suite definitions
- [ ] Baseline comparison
- [ ] Performance tracking
- [ ] Trend analysis

**Deliverables:**
- YAML test suites
- Regression detection
- Performance metrics

### Phase 5: CI/CD Integration (Week 6)
- [ ] GitHub Actions workflows
- [ ] JUnit XML export
- [ ] HTML report generation
- [ ] Metrics export (Prometheus)

**Deliverables:**
- Automated CI/CD pipeline
- Test result dashboards
- Continuous monitoring

### Phase 6: Advanced Features (Week 7)
- [ ] Multi-robot testing
- [ ] Stress testing
- [ ] Failure injection
- [ ] Benchmarking suite

**Deliverables:**
- Complete testing framework
- Comprehensive documentation
- Example test suites

---

## Success Metrics

- ✅ Generate 100+ test scenarios automatically
- ✅ Execute regression suite in <30 minutes
- ✅ Detect performance regressions >5%
- ✅ 95%+ test coverage of robot operations
- ✅ CI/CD integration with automated reporting
- ✅ Support for parallel test execution

---

## Next Steps

1. **Implement Phase 1** (Core framework)
2. **Create example scenarios** (Navigation, perception)
3. **Build test suites** (Quick, standard, full)
4. **Set up CI/CD** (GitHub Actions)
5. **Generate baselines** (Performance benchmarks)

**Ready to implement:** All testing architecture and APIs defined. Can proceed with Phase 1 development.
