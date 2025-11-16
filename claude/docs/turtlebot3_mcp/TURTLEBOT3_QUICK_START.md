# TurtleBot3 Quick Start Guide

**Get started with TurtleBot3 in the ROS2-Gazebo MCP server in 5 minutes**

---

## Installation

### Prerequisites
```bash
# Install ROS2 Humble
sudo apt install ros-humble-desktop

# Install TurtleBot3 packages
sudo apt install ros-humble-turtlebot3*

# Install Gazebo
sudo apt install gazebo ros-humble-gazebo-ros-pkgs

# Set TurtleBot3 model (add to ~/.bashrc)
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```

### Install MCP Server
```bash
cd mcp/servers/ros2-gazebo-mcp
bash scripts/install_deps.sh
```

---

## Quick Examples

### 1. Spawn and Move Robot (30 seconds)

```python
from skills.ros2_gazebo.turtlebot3 import quick_start_burger, move_forward, rotate, stop

# Start simulation
robot = quick_start_burger("my_robot", world="empty")
print(f"Robot spawned at {robot.pose}")

# Move forward 1 meter
move_forward("my_robot", distance=1.0, speed=0.15)

# Rotate 90 degrees
import math
rotate("my_robot", angle=math.pi/2)

# Stop
stop("my_robot")
```

**Result:** Robot spawns in empty world, moves forward, rotates, stops

---

### 2. Read Sensors (1 minute)

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    get_lidar_scan,
    get_obstacle_distances
)

# Start in world with obstacles
robot = quick_start_burger("sensor_test", world="world")

# Get LiDAR scan
scan = get_lidar_scan("sensor_test")
print(f"360° scan: {len(scan.ranges)} measurements")
print(f"Closest obstacle: {scan.summary.min_range}m at {scan.summary.min_range_angle}°")

# Get obstacle distances
obstacles = get_obstacle_distances("sensor_test")
print(f"Front: {obstacles.front}m")
print(f"Left: {obstacles.left}m")
print(f"Right: {obstacles.right}m")
print(f"Clear sectors: {obstacles.clear_sectors}")
```

**Result:** Reads LiDAR data, shows obstacle distances in all directions

---

### 3. Build Map with SLAM (5 minutes)

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    start_slam,
    teleop_key,
    save_slam_map,
    stop_slam
)

# Start in house environment
robot = quick_start_burger("mapper", world="house")

# Start SLAM
slam = start_slam("mapper")
print("SLAM started - drive around to build map")

# Drive with keyboard
teleop_key("mapper")  # W/A/S/D to drive, Q to quit

# Save the map
save_slam_map("mapper", output_path="./maps", map_name="house_map")
print("Map saved to ./maps/house_map.yaml")

stop_slam("mapper")
```

**Result:** Creates map of house environment, saves to file

---

### 4. Autonomous Navigation (3 minutes)

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    start_navigation,
    set_initial_pose,
    navigate_to_goal
)

# Start robot
robot = quick_start_burger("navigator", world="house")

# Start navigation with map
nav = start_navigation("navigator", map_file="./maps/house_map.yaml")

# Tell robot where it starts
set_initial_pose("navigator", x=0.0, y=0.0, yaw=0.0)

# Navigate to goal
result = navigate_to_goal(
    "navigator",
    goal_x=3.0,
    goal_y=2.0,
    goal_yaw=0.0,
    timeout=120.0
)

print(f"Success: {result.success}")
print(f"Distance: {result.distance_traveled}m")
print(f"Time: {result.duration}s")
```

**Result:** Robot autonomously navigates to goal, avoiding obstacles

---

### 5. Multi-Robot Fleet (2 minutes)

```python
from skills.ros2_gazebo.turtlebot3 import (
    spawn_fleet,
    fleet_move_formation
)

# Spawn 3 robots
fleet = spawn_fleet(
    count=3,
    model="burger",
    world="empty",
    formation="line"
)

print(f"Spawned {len(fleet)} robots")

# Move in triangle formation
fleet_move_formation(
    robot_names=[r.name for r in fleet],
    formation="wedge",
    target_center={"x": 5.0, "y": 0.0},
    spacing=1.5
)
```

**Result:** 3 robots spawn and move in coordinated formation

---

## Common Use Cases

### Obstacle Avoidance

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    get_obstacle_distances,
    move_forward,
    rotate,
    stop
)
import math

robot = quick_start_burger("avoider", world="world")

while True:
    obstacles = get_obstacle_distances("avoider")

    if obstacles.front < 0.5:  # Too close
        stop("avoider")
        # Turn towards clearer side
        turn_angle = math.pi/4 if obstacles.left > obstacles.right else -math.pi/4
        rotate("avoider", angle=turn_angle)
    else:
        move_forward("avoider", distance=0.2, speed=0.15)
```

### Wall Following

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    scenario_follow_wall
)

robot = quick_start_burger("follower", world="house")

result = scenario_follow_wall(
    "follower",
    duration=60.0,
    wall_distance=0.3  # Stay 30cm from wall
)

print(f"Followed wall for {result.distance}m")
```

### Patrol Route

```python
from skills.ros2_gazebo.turtlebot3 import (
    quick_start_burger,
    start_navigation,
    navigate_waypoints
)

robot = quick_start_burger("patrol", world="house")
nav = start_navigation("patrol", map_file="house_map.yaml")

# Define patrol waypoints
waypoints = [
    {"x": 1.0, "y": 0.0, "yaw": 0.0},
    {"x": 1.0, "y": 2.0, "yaw": 1.57},
    {"x": -1.0, "y": 2.0, "yaw": 3.14},
    {"x": -1.0, "y": 0.0, "yaw": -1.57}
]

# Patrol continuously
result = navigate_waypoints(
    "patrol",
    waypoints=waypoints,
    loop=True  # Return to start and repeat
)
```

---

## Available Worlds

### Empty World
- **File:** `empty.world`
- **Use for:** Basic movement testing
- **Features:** Flat ground, no obstacles

### TurtleBot3 World
- **File:** `turtlebot3_world.world`
- **Use for:** Obstacle avoidance, navigation
- **Features:** Various obstacles, narrow passages

### TurtleBot3 House
- **File:** `turtlebot3_house.world`
- **Use for:** Indoor navigation, SLAM
- **Features:** Rooms, furniture, realistic environment

### TurtleBot3 Stage
- **File:** `turtlebot3_stage_1.world`
- **Use for:** Path planning challenges
- **Features:** Maze-like layout, complex paths

---

## TurtleBot3 Models

### Burger (Basic)
- **Speed:** 0.22 m/s
- **Sensors:** LiDAR, IMU, Odometry
- **Best for:** Learning, basic navigation

### Waffle (Advanced)
- **Speed:** 0.26 m/s
- **Sensors:** LiDAR, Camera, IMU, Odometry
- **Best for:** Vision-based tasks

### Waffle Pi (Professional)
- **Speed:** 0.26 m/s
- **Sensors:** LiDAR, RGB-D Camera, IMU, Odometry
- **Best for:** 3D mapping, complex perception

---

## Performance Tips

### Token Efficiency

```python
# ❌ INEFFICIENT - Returns full 360-point scan (5000 tokens)
scan = get_lidar_scan("robot")
all_ranges = scan.ranges  # 360 floats

# ✅ EFFICIENT - Returns summary (200 tokens)
scan = get_lidar_scan("robot")
summary = scan.summary  # Analyzed sectors
print(f"Front clear: {summary.front_clear}")
print(f"Min range: {summary.min_range}")
```

### Speed vs. Accuracy

```python
# Fast movement (less accurate)
move_forward("robot", distance=1.0, speed=0.22)

# Precise movement (more accurate)
move_forward("robot", distance=1.0, speed=0.1)
```

### Navigation Timeouts

```python
# Short distance - short timeout
navigate_to_goal("robot", 1.0, 1.0, timeout=30.0)

# Long distance - longer timeout
navigate_to_goal("robot", 10.0, 10.0, timeout=300.0)
```

---

## Troubleshooting

### Robot doesn't move
```bash
# Check if cmd_vel topic exists
ros2 topic list | grep cmd_vel

# Check if robot is receiving commands
ros2 topic echo /cmd_vel
```

### SLAM not working
```bash
# Check if scan topic is publishing
ros2 topic hz /scan

# Ensure SLAM node is running
ros2 node list | grep slam
```

### Navigation fails
```python
# Check localization
from skills.ros2_gazebo.turtlebot3 import get_amcl_pose

pose = get_amcl_pose("robot")
print(f"Robot thinks it's at: {pose}")

# Re-set initial pose if wrong
set_initial_pose("robot", x=0, y=0, yaw=0)
```

### Camera not working (Waffle/Waffle Pi only)
```python
# Use correct model
robot = quick_start_waffle("robot", world="house")  # NOT burger

# Check camera topic
from skills.ros2_gazebo.turtlebot3 import get_camera_image
image = get_camera_image("robot")
```

---

## Next Steps

1. **Try examples above** - Run each quick example
2. **Read full docs** - See `TURTLEBOT3_MCP_IMPLEMENTATION.md`
3. **Explore scenarios** - Try pre-built challenges
4. **Build custom workflows** - Combine operations for your use case

---

## Reference

- **Full API:** `docs/TURTLEBOT3_MCP_IMPLEMENTATION.md`
- **Base MCP Plan:** `docs/ROS2_GAZEBO_MCP_PLAN.md`
- **TurtleBot3 Docs:** https://emanual.robotis.com/docs/en/platform/turtlebot3/
- **ROS2 Nav2:** https://navigation.ros.org/

---

**Ready to start!** Pick an example above and run it.
