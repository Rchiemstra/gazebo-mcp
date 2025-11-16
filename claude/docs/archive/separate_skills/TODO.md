# Claude Agents & Skills Development TODO

This file tracks the development of agents and skills for robotics development with ROS1, Python, C++, and Modbus.

## Architecture Overview

**Meta Layer** → **Workflow Layer** → **Foundation Skills** → **Domain-Specific Agents**

## Progress: 51/51 Complete ✓

## Model Configuration

- **Items 1-6** (Meta & Workflow Layer): Created with Sonnet 4.5, run with Sonnet 4.5
- **Items 7-51** (All Skills & Domain Agents): **Created with Sonnet 4.5**, but **run with Haiku 4.5** for faster, cost-efficient execution

---

## Meta Layer - Agent/Skill Creators

- [x] 1. Create skill-creator agent - Meta-agent that generates Claude Code skills/commands
- [x] 2. Create agent-creator agent - Meta-agent that generates Claude Code agents using skills

## Workflow Layer - Default Development Process

- [x] 3. Create context-gatherer skill - Analyzes codebase and creates context document
- [x] 4. Create plan-generator skill - Uses context document to create detailed implementation plan
- [x] 5. Create plan-executor agent - Implements based on the detailed plan
- [x] 6. Create development-orchestrator agent - Combines context gathering, planning, and execution into default workflow

---

**Note:** All items below (#7-51) should be **created with Sonnet 4.5** for quality, but configured to **run with Haiku 4.5** for faster, cost-efficient execution.

---

## Foundation Skills - ROS Development

- [x] 7. Create ROS package structure skill - Validates and generates ROS package layout
- [x] 8. Create CMakeLists generator skill - Generates/modifies CMakeLists.txt for ROS
- [x] 9. Create package.xml generator skill - Generates/modifies package.xml files
- [x] 10. Create launch file generator skill - Generates ROS launch file XML/Python
- [x] 11. Create msg/srv/action generator skill - Generates ROS interface definition files
- [x] 12. Create C++ node template skill - Generates C++ ROS node boilerplate
- [x] 13. Create Python node template skill - Generates Python ROS node boilerplate
- [x] 14. Create YAML config handler skill - Reads/writes/validates YAML parameter files

## Foundation Skills - Modbus Integration

- [x] 15. Create Modbus protocol handler skill - Encodes/decodes Modbus TCP/RTU messages
- [x] 16. Create register map parser skill - Parses Modbus register definitions

## Foundation Skills - Analysis & Debugging

- [x] 17. Create ROS graph analyzer skill - Analyzes rostopic/rosnode/rosservice output
- [x] 18. Create bag-file-analyzer skill - Analyzes ROS bag files and extracts statistics
- [x] 19. Create tf-tree-visualizer skill - Generates TF tree documentation
- [x] 20. Create code pattern detector skill - Identifies patterns/anti-patterns in code

## Foundation Skills - Robot Modeling & Utilities

- [x] 21. Create URDF builder skill - Assists with URDF/xacro file creation
- [x] 22. Create protocol-translator skill - Converts between industrial protocols
- [x] 23. Create diagnostic-logger skill - Creates diagnostic publishing code
- [x] 24. Create calibration-helper skill - Generates calibration routines

## Domain-Specific Agents - High Priority

- [x] 25. Create ros-node-creator agent - Creates new ROS nodes with proper structure
- [x] 26. Create modbus-ros-bridge agent - Bidirectional bridges between Modbus and ROS
- [x] 27. Create ros-debugger agent - Analyzes ROS graphs and diagnoses issues
- [x] 28. Create catkin-workspace-manager agent - Manages catkin workspace setup
- [x] 29. Create ros-test-suite-generator agent - Creates unit and integration tests
- [x] 30. Create modbus-register-mapper agent - Generates register mapping documentation
- [x] 31. Create ros-launcher agent - Generates and manages launch files
- [x] 32. Create cpp-ros-refactor agent - Refactors C++ ROS nodes with best practices
- [x] 33. Create parameter-config-generator agent - Creates YAML parameter files
- [x] 34. Create deployment-scripter agent - Creates deployment scripts for robot systems

## Domain-Specific Agents - ROS Development

- [x] 35. Create ros-msg-designer agent - Creates custom ROS messages/services/actions
- [x] 36. Create ros-bridge-builder agent - Creates bridge nodes for data translation
- [x] 37. Create ros-package-creator agent - Scaffolds new ROS packages
- [x] 38. Create ros-api-documenter agent - Generates documentation for ROS interfaces

## Domain-Specific Agents - Modbus Integration

- [x] 39. Create modbus-client-generator agent - Generates Modbus TCP/RTU client code
- [x] 40. Create modbus-server-generator agent - Creates Modbus server implementations
- [x] 41. Create modbus-map-documenter agent - Generates Modbus register map documentation

## Domain-Specific Agents - C++ Development

- [x] 42. Create cpp-performance-optimizer agent - Optimizes C++ for real-time performance
- [x] 43. Create cmake-builder agent - Creates and maintains CMakeLists.txt files

## Domain-Specific Agents - Python Development

- [x] 44. Create python-ros-analyzer agent - Checks Python ROS nodes for common issues
- [x] 45. Create python-type-checker agent - Adds type hints and runs mypy validation

## Domain-Specific Agents - Testing & Validation

- [x] 46. Create simulation-validator agent - Generates test scenarios for simulators
- [x] 47. Create hardware-interface-mocker agent - Creates mock hardware interfaces

## Domain-Specific Agents - Code Quality

- [x] 48. Create ros-pattern-detector agent - Identifies anti-patterns in ROS code
- [x] 49. Create cross-language-reviewer agent - Reviews Python/C++ integration code
- [x] 50. Create realtime-safety-checker agent - Analyzes code for real-time safety
- [x] 51. Create architecture-diagrammer agent - Creates system architecture diagrams

---

## Development Workflow

Once the workflow layer is complete, all new development will follow this pattern:

1. **Context Gathering** - Analyze existing code, identify patterns, gather dependencies
2. **Planning** - Create detailed implementation plan based on context
3. **Execution** - Implement according to plan
4. **Validation** - Test and verify implementation

## Next Steps

Start with **skill-creator agent** (#1) to accelerate the creation of all foundation skills.

---

*Last Updated: 2025-10-20 - ALL 51 SKILLS & AGENTS COMPLETE ✓
