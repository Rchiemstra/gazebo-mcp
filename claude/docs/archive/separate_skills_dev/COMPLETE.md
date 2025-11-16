# Claude Agents & Skills - COMPLETE ✓

All 51 agents and skills have been created!

## Usage

All commands are available as slash commands in Claude Code:

### Development Workflow
- `/dev [task]` - Complete development workflow (context → plan → execute)
- `/gather-context [task]` - Analyze codebase  
- `/plan` - Create implementation plan
- `/execute` - Execute the plan

### Meta Tools
- `/create-skill [name] [desc]` - Generate new skill
- `/create-agent [name] [desc]` - Generate new agent

### ROS Development
- `/ros-package-structure [name]` - Package layout
- `/cmake-gen [package]` - CMakeLists.txt
- `/package-xml-gen [package]` - package.xml
- `/launch-gen [node]` - Launch files
- `/ros-msg-gen [type] [name]` - Messages/services/actions
- `/cpp-node-template [name] [type]` - C++ node boilerplate
- `/py-node-template [name] [type]` - Python node boilerplate
- `/yaml-config [name]` - YAML configuration

### Modbus Integration
- `/modbus-handler [operation]` - Encode/decode Modbus
- `/register-map-parser [file]` - Parse register maps

### Analysis & Debugging
- `/ros-graph-analyze` - Analyze ROS graph
- `/bag-analyze [file]` - Analyze bag files
- `/tf-visualize` - TF tree documentation
- `/code-pattern-detect [dir]` - Find code patterns

### Robot Modeling
- `/urdf-builder [robot]` - URDF/xacro assistance
- `/diagnostic-logger [node]` - Diagnostics code
- `/calibration-helper [device]` - Calibration routines
- `/protocol-translate [source] [target]` - Protocol translation

### High-Level Agents
- `/create-ros-node [name] [lang]` - Complete ROS node creation
- `/modbus-bridge [ip] [map]` - Modbus-ROS bridge
- `/ros-debug` - System diagnostics
- `/catkin-workspace` - Workspace management
- `/ros-test-gen` - Test generation
- `/modbus-client-gen [type] [config]` - Modbus client
- `/modbus-server-gen [map]` - Modbus server
- `/cpp-optimize [file]` - C++ optimization
- `/py-analyze [file]` - Python analysis
- `/py-type-check [file]` - Add type hints
- `/sim-validator` - Simulation testing
- `/hw-mocker` - Mock hardware
- `/ros-pkg-create` - Package scaffolding
- `/pattern-detector` - Anti-pattern detection
- `/cross-lang-review` - Python/C++ review
- `/realtime-check` - Real-time safety
- `/ros-msg-design` - Message design
- `/ros-bridge-build` - Bridge nodes
- `/api-documenter` - API documentation
- `/arch-diagram` - Architecture diagrams
- `/modbus-doc` - Modbus documentation
- `/cmake-build` - CMakeLists management

## Quick Start

```bash
# Complete workflow for new feature
/dev Create a ROS node that publishes sensor data

# Create a new ROS node manually
/create-ros-node temperature_sensor python

# Create a Modbus-ROS bridge
/modbus-bridge 192.168.1.100 registers.yaml

# Debug ROS system
/ros-debug

# Generate tests
/ros-test-gen my_package
```

## Architecture

**Meta Layer** (2)
- skill-creator, agent-creator

**Workflow Layer** (4)  
- context-gatherer, plan-generator, plan-executor, development-orchestrator

**Foundation Skills** (18)
- ROS: 8 skills
- Modbus: 2 skills
- Analysis: 4 skills
- Utilities: 4 skills

**Domain Agents** (27)
- High-priority: 10 agents
- ROS Development: 5 agents
- Modbus Integration: 3 agents
- Code Quality: 5 agents
- Testing & Validation: 2 agents
- Documentation: 2 agents

Total: **51 skills and agents** ready to use!

