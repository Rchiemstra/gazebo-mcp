# TurtleBot3 MCP Implementation Guide

**Version:** 1.0
**Date:** 2025-11-11
**Focus:** Open-source TurtleBot3 robotics platform

**Official TurtleBot3 Resources:**
- **GitHub Repository:** https://github.com/ROBOTIS-GIT/turtlebot3
- **E-Manual:** https://emanual.robotis.com/docs/en/platform/turtlebot3/
- **ROS2 Packages:** `ros-humble-turtlebot3*`

---

## Executive Summary

This document provides detailed TurtleBot3-specific implementation for the ROS2-Gazebo MCP server. TurtleBot3 is chosen as the primary platform due to its open-source nature, extensive community support, and comprehensive ROS2 integration.

**TurtleBot3 Advantages:**
- ✅ Fully open-source hardware and software
- ✅ Native ROS2 support
- ✅ Well-documented Gazebo models
- ✅ Active community and examples
- ✅ Multiple variants (Burger, Waffle, Waffle Pi)
- ✅ Extensive navigation stack integration

---

## TurtleBot3 Models

### Model Variants

#### TurtleBot3 Burger
**Specifications:**
- Dimensions: 138mm × 178mm × 192mm
- Weight: ~1kg
- Max speed: 0.22 m/s
- Sensors: LiDAR (360° LDS-01), IMU, Odometry
- Differential drive (2 wheels)

**Use Cases:**
- Basic navigation and SLAM
- Path planning algorithms
- Multi-robot systems
- Education and learning

#### TurtleBot3 Waffle
**Specifications:**
- Dimensions: 281mm × 306mm × 141mm
- Weight: ~1.8kg
- Max speed: 0.26 m/s
- Sensors: LiDAR (360° LDS-01), IMU, Odometry, Camera (Raspberry Pi Cam)
- Differential drive (2 wheels)

**Use Cases:**
- Vision-based navigation
- Object detection and tracking
- Advanced SLAM
- Autonomous delivery

#### TurtleBot3 Waffle Pi
**Specifications:**
- Same as Waffle but with Intel RealSense D435
- RGB-D camera (depth + color)
- Point cloud generation

**Use Cases:**
- 3D mapping
- Depth-based obstacle avoidance
- Complex perception tasks
- Visual servoing

---

## TurtleBot3 Configuration

### Configuration Files

#### TurtleBot3 Robot Configs (`config/robots/turtlebot3/`)

**burger.yaml:**
```yaml
name: turtlebot3_burger
description: TurtleBot3 Burger - Basic education platform

# Physical properties
dimensions:
  length: 0.138  # meters
  width: 0.178
  height: 0.192
  wheel_radius: 0.033
  wheel_separation: 0.160

# Motion limits
velocity_limits:
  linear:
    max: 0.22  # m/s
    min: -0.22
  angular:
    max: 2.84  # rad/s (~163 deg/s)
    min: -2.84

acceleration_limits:
  linear: 2.5   # m/s²
  angular: 3.2  # rad/s²

# Sensors
sensors:
  lidar:
    type: "LDS-01"
    topic: "/scan"
    frame_id: "base_scan"
    range_min: 0.12  # meters
    range_max: 3.5
    angle_min: 0.0
    angle_max: 6.28  # ~360 degrees
    samples: 360

  imu:
    topic: "/imu"
    frame_id: "imu_link"

  odometry:
    topic: "/odom"
    frame_id: "odom"
    child_frame_id: "base_footprint"

# Control topics
control:
  cmd_vel: "/cmd_vel"
  joint_states: "/joint_states"

# Model files
urdf: "turtlebot3_burger.urdf"
sdf: "turtlebot3_burger.sdf"

# Default spawn pose
default_pose:
  x: 0.0
  y: 0.0
  z: 0.01
  roll: 0.0
  pitch: 0.0
  yaw: 0.0
```

**waffle.yaml:**
```yaml
name: turtlebot3_waffle
description: TurtleBot3 Waffle - Advanced platform with camera

# Physical properties
dimensions:
  length: 0.281  # meters
  width: 0.306
  height: 0.141
  wheel_radius: 0.033
  wheel_separation: 0.287

# Motion limits (slightly faster than Burger)
velocity_limits:
  linear:
    max: 0.26  # m/s
    min: -0.26
  angular:
    max: 1.82  # rad/s (~104 deg/s)
    min: -1.82

acceleration_limits:
  linear: 2.5
  angular: 3.2

# Sensors (includes camera)
sensors:
  lidar:
    type: "LDS-01"
    topic: "/scan"
    frame_id: "base_scan"
    range_min: 0.12
    range_max: 3.5
    angle_min: 0.0
    angle_max: 6.28
    samples: 360

  camera:
    topic: "/camera/image_raw"
    info_topic: "/camera/camera_info"
    frame_id: "camera_rgb_optical_frame"
    width: 640
    height: 480
    fov: 1.085  # ~62 degrees

  imu:
    topic: "/imu"
    frame_id: "imu_link"

  odometry:
    topic: "/odom"
    frame_id: "odom"
    child_frame_id: "base_footprint"

# Control topics
control:
  cmd_vel: "/cmd_vel"
  joint_states: "/joint_states"

# Model files
urdf: "turtlebot3_waffle.urdf"
sdf: "turtlebot3_waffle.sdf"

# Default spawn pose
default_pose:
  x: 0.0
  y: 0.0
  z: 0.01
  roll: 0.0
  pitch: 0.0
  yaw: 0.0
```

**waffle_pi.yaml:**
```yaml
name: turtlebot3_waffle_pi
description: TurtleBot3 Waffle Pi - Advanced platform with depth camera

# Same physical properties as Waffle
dimensions:
  length: 0.281
  width: 0.306
  height: 0.141
  wheel_radius: 0.033
  wheel_separation: 0.287

velocity_limits:
  linear:
    max: 0.26
    min: -0.26
  angular:
    max: 1.82
    min: -1.82

acceleration_limits:
  linear: 2.5
  angular: 3.2

# Sensors (includes RealSense D435)
sensors:
  lidar:
    type: "LDS-01"
    topic: "/scan"
    frame_id: "base_scan"
    range_min: 0.12
    range_max: 3.5
    angle_min: 0.0
    angle_max: 6.28
    samples: 360

  camera_rgb:
    topic: "/camera/color/image_raw"
    info_topic: "/camera/color/camera_info"
    frame_id: "camera_rgb_optical_frame"
    width: 640
    height: 480

  camera_depth:
    topic: "/camera/depth/image_raw"
    info_topic: "/camera/depth/camera_info"
    frame_id: "camera_depth_optical_frame"
    width: 640
    height: 480
    range_min: 0.2  # meters
    range_max: 3.0

  pointcloud:
    topic: "/camera/depth/points"
    frame_id: "camera_depth_optical_frame"

  imu:
    topic: "/imu"
    frame_id: "imu_link"

  odometry:
    topic: "/odom"
    frame_id: "odom"
    child_frame_id: "base_footprint"

# Control topics
control:
  cmd_vel: "/cmd_vel"
  joint_states: "/joint_states"

# Model files
urdf: "turtlebot3_waffle_pi.urdf"
sdf: "turtlebot3_waffle_pi.sdf"

default_pose:
  x: 0.0
  y: 0.0
  z: 0.01
  roll: 0.0
  pitch: 0.0
  yaw: 0.0
```

---

## TurtleBot3 Gazebo Worlds

### Available Worlds (`config/worlds/turtlebot3/`)

#### 1. Empty World
**File:** `empty.world`
**Description:** Flat ground plane, no obstacles
**Use Case:** Basic movement testing, velocity control

#### 2. TurtleBot3 World
**File:** `turtlebot3_world.world`
**Description:** Indoor environment with obstacles, walls, and objects
**Features:**
- Various obstacle shapes
- Narrow passages
- Open areas
**Use Case:** Navigation algorithm testing, obstacle avoidance

#### 3. TurtleBot3 House
**File:** `turtlebot3_house.world`
**Description:** Residential environment with rooms
**Features:**
- Multiple rooms
- Furniture
- Doors and corridors
**Use Case:** Indoor navigation, room-to-room planning, realistic scenarios

#### 4. TurtleBot3 Stage
**File:** `turtlebot3_stage_1.world`, `turtlebot3_stage_2.world`, etc.
**Description:** Competition-style environments
**Features:**
- Complex maze layouts
- Dead ends
- Multiple paths
**Use Case:** Path planning challenges, exploration algorithms

#### 5. Custom Multi-Robot Arena
**File:** `multi_robot_arena.world`
**Description:** Large open space for multi-robot scenarios
**Features:**
- Flat area (20m × 20m)
- Scattered obstacles
- Charging stations
**Use Case:** Multi-robot coordination, fleet management

---

## TurtleBot3 Operations

### Specialized TurtleBot3 Adapter (`adapters/turtlebot3.py`)

```python
"""
TurtleBot3-specific operations.

High-level operations optimized for TurtleBot3 platform.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

# ============================================================================
# 1. Quick Start Operations
# ============================================================================

def quick_start_burger(
    robot_name: str = "tb3_burger",
    world: str = "empty",
    position: dict = None
) -> TurtleBot3Info:
    """
    Quick start TurtleBot3 Burger simulation.

    One command to:
    - Launch Gazebo with specified world
    - Spawn TurtleBot3 Burger
    - Initialize all sensors
    - Set up control topics

    Args:
        robot_name: Name for the robot
        world: World name ("empty", "house", "world", "stage_1")
        position: Optional spawn position {x, y, yaw}

    Returns:
        TurtleBot3Info with all topics and status

    Example:
        robot = quick_start_burger("my_robot", world="house")
        print(f"Robot ready at {robot.pose}")
        print(f"LiDAR topic: {robot.sensors.lidar_topic}")
    """
    pass

def quick_start_waffle(
    robot_name: str = "tb3_waffle",
    world: str = "empty",
    position: dict = None,
    enable_camera: bool = True
) -> TurtleBot3Info:
    """Quick start TurtleBot3 Waffle with camera."""
    pass

def quick_start_waffle_pi(
    robot_name: str = "tb3_waffle_pi",
    world: str = "empty",
    position: dict = None,
    enable_rgbd: bool = True
) -> TurtleBot3Info:
    """Quick start TurtleBot3 Waffle Pi with RealSense."""
    pass


# ============================================================================
# 2. Motion Control (Optimized for TurtleBot3)
# ============================================================================

def move_forward(
    robot_name: str,
    distance: float,
    speed: float = 0.15
) -> MoveResult:
    """
    Move TurtleBot3 forward by specified distance.

    Args:
        robot_name: Robot identifier
        distance: Distance in meters (positive = forward, negative = backward)
        speed: Linear speed in m/s (0.0 to 0.22 for Burger, 0.26 for Waffle)

    Returns:
        MoveResult with actual distance traveled and duration
    """
    pass

def rotate(
    robot_name: str,
    angle: float,
    angular_speed: float = 0.5
) -> MoveResult:
    """
    Rotate TurtleBot3 by specified angle.

    Args:
        robot_name: Robot identifier
        angle: Angle in radians (positive = CCW, negative = CW)
        angular_speed: Angular speed in rad/s

    Returns:
        MoveResult with actual angle rotated and duration
    """
    pass

def move_to_point(
    robot_name: str,
    target_x: float,
    target_y: float,
    speed: float = 0.15
) -> MoveResult:
    """
    Move TurtleBot3 to target point (simple control).

    Uses proportional control for heading and speed.
    Does NOT use Nav2 - suitable for open areas without obstacles.

    Args:
        robot_name: Robot identifier
        target_x: Target X coordinate (meters)
        target_y: Target Y coordinate (meters)
        speed: Maximum linear speed

    Returns:
        MoveResult with path taken
    """
    pass

def stop(robot_name: str):
    """Immediately stop TurtleBot3."""
    pass


# ============================================================================
# 3. Teleoperation
# ============================================================================

def teleop_key(robot_name: str) -> TeleopSession:
    """
    Start keyboard teleoperation session.

    Controls:
        W/↑ - Forward
        S/↓ - Backward
        A/← - Rotate left
        D/→ - Rotate right
        Space - Stop
        Q - Quit

    Returns:
        TeleopSession that can be stopped
    """
    pass

def teleop_twist(
    robot_name: str,
    linear: float,
    angular: float,
    duration: float = None
) -> CommandResult:
    """
    Send twist command (for external control).

    Args:
        robot_name: Robot identifier
        linear: Linear velocity (-0.22 to 0.22 m/s for Burger)
        angular: Angular velocity (-2.84 to 2.84 rad/s for Burger)
        duration: Duration to apply (None = continuous until stopped)
    """
    pass


# ============================================================================
# 4. Sensor Access (TurtleBot3-optimized)
# ============================================================================

def get_lidar_scan(robot_name: str, timeout: float = 5.0) -> LidarScan:
    """
    Get LiDAR scan from TurtleBot3.

    Returns:
        LidarScan with 360 range measurements and analysis
    """
    pass

def get_obstacle_distances(robot_name: str) -> ObstacleDistances:
    """
    Get obstacle distances in cardinal directions.

    Returns token-efficient summary:
        {
            "front": 1.2,      # meters
            "back": 0.5,
            "left": 2.0,
            "right": 1.5,
            "front_left": 1.0,
            "front_right": 1.1,
            "clear_sectors": [90, 180],  # Angles with no obstacles
            "closest": {"distance": 0.5, "angle": 180}
        }
    """
    pass

def get_camera_image(robot_name: str) -> CameraImage:
    """Get camera image (Waffle/Waffle Pi only)."""
    pass

def get_depth_image(robot_name: str) -> DepthImage:
    """Get depth image (Waffle Pi only)."""
    pass

def get_point_cloud(robot_name: str) -> PointCloud:
    """Get point cloud (Waffle Pi only)."""
    pass

def detect_obstacles_from_depth(
    robot_name: str,
    min_distance: float = 0.3
) -> List[Obstacle]:
    """
    Detect obstacles from depth camera.

    Returns list of obstacles with:
        - Position (x, y, z)
        - Distance
        - Bounding box
    """
    pass


# ============================================================================
# 5. SLAM Operations
# ============================================================================

def start_slam(
    robot_name: str,
    slam_method: str = "slam_toolbox"
) -> SLAMSession:
    """
    Start SLAM mapping.

    Args:
        robot_name: Robot identifier
        slam_method: "slam_toolbox" or "cartographer"

    Returns:
        SLAMSession with map topic and controls
    """
    pass

def get_slam_map(robot_name: str) -> OccupancyGrid:
    """Get current SLAM map."""
    pass

def save_slam_map(
    robot_name: str,
    output_path: str,
    map_name: str = "my_map"
):
    """
    Save SLAM map to files.

    Creates:
        - {map_name}.yaml (map metadata)
        - {map_name}.pgm (map image)
    """
    pass

def stop_slam(robot_name: str):
    """Stop SLAM session."""
    pass


# ============================================================================
# 6. Navigation (Nav2 Integration)
# ============================================================================

def start_navigation(
    robot_name: str,
    map_file: str = None,
    use_slam: bool = False
) -> NavigationSession:
    """
    Start Nav2 navigation stack.

    Args:
        robot_name: Robot identifier
        map_file: Path to map YAML (required unless use_slam=True)
        use_slam: Use SLAM for mapping instead of pre-made map

    Returns:
        NavigationSession with navigation controls
    """
    pass

def set_initial_pose(
    robot_name: str,
    x: float,
    y: float,
    yaw: float
):
    """
    Set initial pose for localization (AMCL).

    Args:
        x, y: Position in map frame (meters)
        yaw: Orientation in radians
    """
    pass

def navigate_to_goal(
    robot_name: str,
    goal_x: float,
    goal_y: float,
    goal_yaw: float = 0.0,
    timeout: float = 300.0
) -> NavigationResult:
    """
    Navigate to goal pose.

    Uses Nav2 with:
        - AMCL localization
        - Global planner (NavFn or SMAC)
        - Local planner (DWB)
        - Recovery behaviors

    Returns:
        NavigationResult with success status and path taken
    """
    pass

def navigate_waypoints(
    robot_name: str,
    waypoints: List[Dict],
    loop: bool = False
) -> NavigationResult:
    """
    Navigate through multiple waypoints.

    Args:
        waypoints: List of {x, y, yaw} poses
        loop: Return to start after last waypoint
    """
    pass

def cancel_navigation(robot_name: str):
    """Cancel current navigation goal."""
    pass

def get_navigation_status(robot_name: str) -> NavStatus:
    """
    Get current navigation status.

    Returns:
        - Current goal
        - Progress
        - Current behavior
        - Estimated time remaining
    """
    pass


# ============================================================================
# 7. Multi-Robot Operations
# ============================================================================

def spawn_fleet(
    count: int,
    model: str = "burger",
    world: str = "multi_robot_arena",
    formation: str = "grid"
) -> List[TurtleBot3Info]:
    """
    Spawn multiple TurtleBot3 robots.

    Args:
        count: Number of robots
        model: "burger", "waffle", or "waffle_pi"
        world: Gazebo world
        formation: "grid", "line", "circle", "random"

    Returns:
        List of TurtleBot3Info for each robot
    """
    pass

def fleet_move_formation(
    robot_names: List[str],
    formation: str,
    target_center: Dict,
    spacing: float = 1.0
) -> MultiRobotResult:
    """
    Move fleet in formation.

    Args:
        robot_names: List of robot identifiers
        formation: "line", "column", "wedge", "circle"
        target_center: Center point {x, y}
        spacing: Distance between robots (meters)
    """
    pass

def fleet_coordinate_navigation(
    robot_names: List[str],
    goals: List[Dict],
    avoid_collisions: bool = True
) -> MultiRobotResult:
    """
    Coordinate navigation for multiple robots.

    Handles:
        - Collision avoidance between robots
        - Path coordination
        - Priority management
    """
    pass


# ============================================================================
# 8. Scenarios & Challenges
# ============================================================================

def scenario_explore_and_map(
    robot_name: str,
    world: str = "house",
    exploration_time: float = 300.0
) -> ExplorationResult:
    """
    Autonomous exploration and mapping scenario.

    Robot will:
        1. Start SLAM
        2. Explore unknown areas
        3. Build complete map
        4. Return to start

    Returns:
        - Map coverage percentage
        - Exploration path
        - Final map
        - Time taken
    """
    pass

def scenario_point_to_point(
    robot_name: str,
    start: Dict,
    goal: Dict,
    world: str = "world",
    obstacles: str = "dynamic"
) -> NavigationResult:
    """
    Point-to-point navigation challenge.

    Tests:
        - Path planning
        - Obstacle avoidance
        - Re-planning on failures
    """
    pass

def scenario_delivery_mission(
    robot_name: str,
    pickup_points: List[Dict],
    delivery_points: List[Dict],
    map_file: str
) -> DeliveryResult:
    """
    Multi-waypoint delivery mission.

    Simulates delivery robot:
        - Navigate to pickup locations
        - Navigate to delivery locations
        - Return to base

    Tracks:
        - Success rate
        - Time per delivery
        - Total distance
    """
    pass

def scenario_follow_wall(
    robot_name: str,
    duration: float = 60.0,
    wall_distance: float = 0.3
) -> FollowResult:
    """
    Wall-following behavior.

    Uses LiDAR to maintain distance from wall.
    Tests reactive control algorithms.
    """
    pass


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class TurtleBot3Info:
    """TurtleBot3 robot information."""
    name: str
    model: str  # "burger", "waffle", "waffle_pi"
    namespace: str

    # Current state
    pose: Dict  # {x, y, z, roll, pitch, yaw}
    velocity: Dict  # {linear, angular}

    # Topics
    topics: Dict  # All topic names

    # Sensors available
    has_lidar: bool
    has_camera: bool
    has_depth_camera: bool
    has_imu: bool

    # Control info
    max_linear_speed: float
    max_angular_speed: float

@dataclass
class LidarScan:
    """LiDAR scan data."""
    timestamp: float
    ranges: List[float]  # 360 measurements
    angle_min: float
    angle_max: float
    angle_increment: float

    # Token-efficient summary
    summary: ScanSummary

@dataclass
class ScanSummary:
    """Token-efficient scan summary."""
    min_range: float
    min_range_angle: float
    obstacles_detected: int
    clear_sectors: List[int]  # Angles with clear path
    front_clear: bool
    left_clear: bool
    right_clear: bool
    back_clear: bool

@dataclass
class ObstacleDistances:
    """Obstacle distances in cardinal directions."""
    front: float
    back: float
    left: float
    right: float
    front_left: float
    front_right: float
    back_left: float
    back_right: float

    clear_sectors: List[int]  # Angles with no obstacles
    closest: Dict  # {distance, angle}

@dataclass
class NavigationResult:
    """Navigation operation result."""
    success: bool
    goal_reached: bool
    distance_traveled: float
    duration: float
    path_taken: List[Dict]  # Waypoints
    failures: List[str]  # Any failures/recoveries

@dataclass
class ExplorationResult:
    """Exploration scenario result."""
    map_coverage: float  # Percentage
    area_explored: float  # m²
    duration: float
    distance_traveled: float
    final_map: OccupancyGrid
    exploration_path: List[Dict]
```

---

## Implementation Priority

### Phase 1: Basic TurtleBot3 Operations (Week 1-2)
- [ ] TurtleBot3 configuration files (burger.yaml, waffle.yaml, waffle_pi.yaml)
- [ ] Quick start operations
- [ ] Basic motion control (move_forward, rotate, stop)
- [ ] LiDAR sensor access
- [ ] Teleoperation

**Deliverables:**
- Spawn TurtleBot3 in Gazebo
- Move robot with simple commands
- Read LiDAR data
- Keyboard control

### Phase 2: Navigation & SLAM (Week 3-4)
- [ ] SLAM integration (SLAM Toolbox)
- [ ] Map saving/loading
- [ ] Nav2 integration
- [ ] Waypoint navigation
- [ ] Localization (AMCL)

**Deliverables:**
- Build map with SLAM
- Navigate using pre-made map
- Multi-waypoint missions

### Phase 3: Advanced Sensors (Week 5)
- [ ] Camera integration (Waffle)
- [ ] Depth camera integration (Waffle Pi)
- [ ] Point cloud processing
- [ ] Vision-based obstacle detection

**Deliverables:**
- Capture camera images
- Process depth data
- Detect obstacles from vision

### Phase 4: Multi-Robot (Week 6)
- [ ] Fleet spawning
- [ ] Multi-robot coordination
- [ ] Formation control
- [ ] Collision avoidance

**Deliverables:**
- Spawn multiple TurtleBot3s
- Coordinate movement
- Formation patterns

### Phase 5: Scenarios & Examples (Week 7)
- [ ] Exploration scenario
- [ ] Delivery mission
- [ ] Wall following
- [ ] Point-to-point challenges

**Deliverables:**
- Pre-built scenarios
- Performance metrics
- Example workflows

---

## Example Workflows

### Example 1: Basic Movement

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    move_forward,
    rotate,
    stop,
    get_lidar_scan
)

# Start simulation
robot = quick_start_burger("my_robot", world="empty")

# Move forward 1 meter
result = move_forward("my_robot", distance=1.0, speed=0.15)
print(f"Moved {result.distance_traveled}m in {result.duration}s")

# Rotate 90 degrees (π/2 radians)
import math
rotate("my_robot", angle=math.pi/2, angular_speed=0.5)

# Check surroundings
scan = get_lidar_scan("my_robot")
print(f"Front clear: {scan.summary.front_clear}")
print(f"Closest obstacle: {scan.summary.min_range}m")

# Stop
stop("my_robot")
```

### Example 2: Mapping with SLAM

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    start_slam,
    teleop_key,
    save_slam_map,
    stop_slam
)

# Start robot in house environment
robot = quick_start_burger("mapper", world="house")

# Start SLAM
slam = start_slam("mapper", slam_method="slam_toolbox")
print(f"SLAM started. Map topic: {slam.map_topic}")

# Manual exploration with keyboard
teleop = teleop_key("mapper")
print("Drive around to build map. Press Q to finish.")

# Wait for user to finish (teleop blocks until Q pressed)
# ...

# Save map
save_slam_map("mapper", output_path="/tmp", map_name="house_map")
print("Map saved to /tmp/house_map.yaml")

# Stop SLAM
stop_slam("mapper")
```

### Example 3: Autonomous Navigation

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    start_navigation,
    set_initial_pose,
    navigate_to_goal,
    get_navigation_status
)

# Start robot
robot = quick_start_burger("navigator", world="house")

# Start navigation with pre-made map
nav = start_navigation(
    "navigator",
    map_file="/tmp/house_map.yaml",
    use_slam=False
)

# Set initial pose (where robot thinks it is)
set_initial_pose("navigator", x=0.0, y=0.0, yaw=0.0)

# Navigate to kitchen (example coordinates)
result = navigate_to_goal(
    "navigator",
    goal_x=3.5,
    goal_y=2.0,
    goal_yaw=1.57,  # 90 degrees
    timeout=120.0
)

if result.success:
    print(f"Reached goal! Traveled {result.distance_traveled}m")
else:
    print(f"Navigation failed: {result.failures}")
```

### Example 4: Obstacle Avoidance

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    get_obstacle_distances,
    move_forward,
    rotate,
    stop
)
import time
import math

# Start robot
robot = quick_start_burger("avoider", world="world")

# Simple obstacle avoidance loop
for _ in range(100):  # Run for 100 iterations
    # Check surroundings
    obstacles = get_obstacle_distances("avoider")

    if obstacles.front < 0.5:  # Obstacle within 0.5m
        print("Obstacle ahead! Turning...")
        stop("avoider")

        # Turn towards clearer direction
        if obstacles.left > obstacles.right:
            rotate("avoider", angle=math.pi/4)  # Turn left 45°
        else:
            rotate("avoider", angle=-math.pi/4)  # Turn right 45°
    else:
        # Move forward
        move_forward("avoider", distance=0.3, speed=0.15)

    time.sleep(0.1)

stop("avoider")
```

### Example 5: Multi-Robot Coordination

```python
from skills.ros2_gazebo.turtlebot3 import (
    spawn_fleet,
    fleet_move_formation,
    fleet_coordinate_navigation
)

# Spawn 4 robots in grid formation
fleet = spawn_fleet(
    count=4,
    model="burger",
    world="multi_robot_arena",
    formation="grid"
)

robot_names = [robot.name for robot in fleet]
print(f"Spawned {len(fleet)} robots: {robot_names}")

# Move fleet to new location in line formation
fleet_move_formation(
    robot_names,
    formation="line",
    target_center={"x": 5.0, "y": 0.0},
    spacing=1.0
)

# Send to individual goals with coordination
goals = [
    {"x": 8.0, "y": 8.0, "yaw": 0.0},
    {"x": -8.0, "y": 8.0, "yaw": 0.0},
    {"x": -8.0, "y": -8.0, "yaw": 0.0},
    {"x": 8.0, "y": -8.0, "yaw": 0.0}
]

result = fleet_coordinate_navigation(
    robot_names,
    goals,
    avoid_collisions=True
)

print(f"All robots reached goals: {result.all_succeeded}")
```

### Example 6: Exploration Challenge

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    scenario_explore_and_map
)

# Start robot in unknown environment
robot = quick_start_burger("explorer", world="house")

# Run autonomous exploration
result = scenario_explore_and_map(
    "explorer",
    world="house",
    exploration_time=300.0  # 5 minutes
)

print(f"Exploration Results:")
print(f"  Coverage: {result.map_coverage}%")
print(f"  Area explored: {result.area_explored} m²")
print(f"  Distance traveled: {result.distance_traveled} m")
print(f"  Duration: {result.duration} s")

# Map is automatically saved
print(f"Map saved to exploration_map.yaml")
```

---

## Testing Strategy

### Unit Tests

```python
# tests/turtlebot3/test_basic_operations.py
def test_spawn_burger():
    """Test spawning TurtleBot3 Burger."""
    robot = quick_start_burger("test_robot", world="empty")
    assert robot.model == "burger"
    assert robot.has_lidar == True
    assert robot.has_camera == False

def test_move_forward():
    """Test forward movement."""
    robot = quick_start_burger("test_robot", world="empty")
    result = move_forward("test_robot", distance=1.0, speed=0.15)
    assert result.success == True
    assert abs(result.distance_traveled - 1.0) < 0.05  # 5cm tolerance

def test_rotate():
    """Test rotation."""
    import math
    robot = quick_start_burger("test_robot", world="empty")
    result = rotate("test_robot", angle=math.pi/2)
    assert result.success == True
```

### Integration Tests

```python
# tests/turtlebot3/test_navigation.py
def test_slam_mapping():
    """Test SLAM mapping."""
    robot = quick_start_burger("slam_test", world="world")
    slam = start_slam("slam_test")

    # Move robot around
    move_forward("slam_test", 1.0)
    rotate("slam_test", math.pi/2)
    move_forward("slam_test", 1.0)

    # Get map
    map_data = get_slam_map("slam_test")
    assert map_data is not None
    assert map_data.width > 0
    assert map_data.height > 0

    stop_slam("slam_test")

def test_autonomous_navigation():
    """Test Nav2 navigation."""
    robot = quick_start_burger("nav_test", world="world")

    # Start nav with test map
    nav = start_navigation("nav_test", map_file="test_map.yaml")
    set_initial_pose("nav_test", 0, 0, 0)

    # Navigate to goal
    result = navigate_to_goal("nav_test", 2.0, 2.0, timeout=60.0)
    assert result.success == True
    assert result.goal_reached == True
```

### Performance Tests

```python
# tests/turtlebot3/test_performance.py
def test_token_efficiency():
    """Test token reduction for sensor data."""
    robot = quick_start_burger("perf_test", world="world")

    # Get full scan
    scan = get_lidar_scan("perf_test")
    full_size = len(str(scan.ranges))  # ~3600 chars for 360 floats
    summary_size = len(str(scan.summary))  # ~200 chars

    reduction = (1 - summary_size / full_size) * 100
    assert reduction > 90  # >90% token reduction
```

---

## Performance Metrics

### Expected Token Savings

| Operation | Full Data | Filtered | Savings |
|-----------|-----------|----------|---------|
| LiDAR scan (360 points) | 5,000 tokens | 200 tokens | 96% |
| Camera image (640×480) | 100,000 tokens | 1,000 tokens | 99% |
| Topic list (50 topics) | 10,000 tokens | 500 tokens | 95% |
| Map data (100×100) | 15,000 tokens | 800 tokens | 95% |

### Latency Targets

- Robot spawn: <5s
- Motion command: <50ms
- Sensor read: <100ms
- SLAM initialization: <3s
- Navigation goal: <500ms

---

## Next Steps

1. **Implement Phase 1** (Basic operations)
2. **Create example worlds** (TurtleBot3-specific)
3. **Build test suite** (Unit + integration)
4. **Document examples** (Jupyter notebooks)
5. **Performance validation** (Token efficiency)

**Ready to implement:** All TurtleBot3 configurations and basic operations defined. Can proceed with coding Phase 1.
