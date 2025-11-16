# Tool Design Audit Report

**Date**: 2025-11-07
**Total Commands**: 59 (30 skills + 29 agents)
**Audit Scope**: All skills and agents

---

## Executive Summary

### Current State
The existing commands provide solid functionality but lack consistency in structure, metadata, and formatting. Key improvements needed:

1. **Frontmatter standardization** - Missing fields, inconsistent format
2. **ROS version updates** - Many files still reference ROS1
3. **Output formatting** - Inconsistent result presentation
4. **Error messages** - Need to be more actionable
5. **Progressive disclosure** - Examples could be extracted

### Priority Recommendations

**HIGH PRIORITY** (Quick fixes, high impact):
1. ✅ Standardize YAML frontmatter across all files
2. ✅ Update ROS1 references to ROS2
3. ✅ Add exit codes to all skills

**MEDIUM PRIORITY** (Improve UX):
4. ⚠️ Standardize output format templates
5. ⚠️ Enhance error messages with actionable guidance
6. ⚠️ Add response_format options (concise/detailed)

**LOW PRIORITY** (Optimization):
7. ℹ️ Extract large examples to reference files
8. ℹ️ Add token-efficient alternatives
9. ℹ️ Create shared troubleshooting guides

---

## Audit Findings by Category

### 1. Frontmatter Consistency

**Current State**: Inconsistent metadata across files

**Issues Found**:
- ❌ Missing `category` field in ~40 files
- ❌ Missing `complexity` field in ~45 files
- ❌ Missing `requires` field in ~50 files
- ❌ Inconsistent `argument-hint` format
- ⚠️ Some files missing `model` specification

**Required Frontmatter Template**:
```yaml
---
description: [Clear, specific description under 100 chars]
argument-hint: [arg1] [optional-arg2]
model: claude-haiku-4-5-20251001  # or sonnet-4-5 for complex
category: [workflow|ros|modbus|git|verification|analysis|robot|meta]
complexity: [low|medium|high]
requires: [comma-separated dependencies, e.g., "git, python"]
---
```

**Action Items**:
```bash
# Files needing category/complexity additions:
- skills/git/*.md (3 files)
- skills/ros/*.md (8 files)
- skills/modbus/*.md (2 files)
- skills/analysis/*.md (4 files)
- skills/robot/*.md (4 files)
- skills/meta/*.md (2 files)
- agents/*/*.md (29 files)
```

### 2. ROS Version Updates

**Current State**: Many files still reference ROS1/catkin

**Files Needing Updates**:
- `skills/ros/cmake-gen.md` - References ROS1, catkin
- `skills/ros/package-xml-gen.md` - ROS1 package.xml format
- `skills/ros/launch-gen.md` - May reference XML launch files
- `skills/ros/cpp-node-template.md` - Uses ROS1 patterns
- `skills/ros/py-node-template.md` - Uses rospy instead of rclpy
- `agents/ros/create-ros-node.md` - ROS1 workflow
- `agents/ros/ros-pkg-create.md` - catkin workspace
- `agents/workspace/catkin-workspace.md` - Entire file is ROS1

**ROS2 Updates Needed**:
- catkin → colcon
- rosrun/roslaunch → ros2 run/ros2 launch
- rospy → rclpy
- roscpp → rclcpp
- package.xml format 2 → format 3
- CMakeLists.txt for ament_cmake
- XML launch files → Python launch files
- Parameter declaration (ROS2 requirement)

### 3. Output Formatting

**Current State**: Inconsistent result presentation

**Patterns Observed**:
✅ **Good** (verification skills):
- Clear section headers with separators
- Status indicators (✅ ❌ ⚠️)
- Structured output with recommendations
- Next steps clearly stated

⚠️ **Inconsistent** (older skills):
- Plain text output without formatting
- No status indicators
- Recommendations buried in text
- Unclear next steps

**Standard Output Template** (from tool-design-guide.md):
```
[Skill Name]: [target]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SECTION HEADER]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: [✅ SUCCESS | ⚠️ WARNINGS | ❌ FAILED]

[Key information]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. [Actionable step]
2. [Actionable step]
```

**Files Needing Format Updates**: ~30 skills/agents

### 4. Error Message Quality

**Current State**: Variable quality of error handling

**Issues Found**:
- Some skills lack error handling sections
- Generic error messages without fixes
- Missing common issues documentation
- No error exit codes

**Best Practice** (from verification skills):
```markdown
## Common Issues

### Issue: [Problem Description]

**Symptoms**: [How to recognize it]

**Cause**: [Why it happens]

**Solution**:
\`\`\`
[Specific code/commands to fix]
\`\`\`

**Reference**: [Where to learn more]
```

**Files Needing Error Enhancements**: ~25 files

### 5. Exit Code Standards

**Current State**: Only verification skills have exit codes

**Recommended Standard**:
```markdown
## Exit Codes

- **0**: Success (all checks passed, operation completed)
- **1**: Warnings (operation succeeded with non-critical issues)
- **2**: Failure (operation failed, manual intervention needed)
- **3**: Cannot execute (prerequisites not met, tool unavailable)
```

**Files Needing Exit Codes**: ~45 files

### 6. Progressive Disclosure Opportunities

**Current State**: Some files have very long examples inline

**Files with Large Examples** (candidates for extraction):
- `skills/ros/cpp-node-template.md` (~340 lines) - Extract templates
- `skills/ros/py-node-template.md` (~200 lines) - Extract templates
- `skills/ros/launch-gen.md` - Extract launch examples
- `skills/modbus/modbus-handler.md` - Extract protocol examples
- `agents/modbus/modbus-bridge.md` - Extract integration examples

**Proposed Structure**:
```
Original file: cpp-node-template.md (concise version)
Reference: cpp-node-templates.md (detailed examples)
Usage: "See detailed examples in: cpp-node-templates.md"
```

**Token Savings**: ~30-40% per affected file

---

## Detailed File-by-File Assessment

### Skills (30 files)

#### Meta (2 files)
- `create-skill.md` - ⚠️ Needs frontmatter standardization, Phase 9 enhancement
- `create-agent.md` - ⚠️ Needs frontmatter standardization, Phase 9 enhancement

#### Workflow (2 files)
- `gather-context.md` - ⚠️ Phase 3 enhancement needed
- `plan.md` - ✅ Relatively good, needs minor frontmatter

#### Git (3 files)
- `git-commit.md` - ❌ Missing argument-hint, category, exit codes
- `git-commit-msg.md` - ❌ Missing category, complexity, exit codes
- `git-stage.md` - ❌ Missing category, complexity, exit codes

#### ROS (8 files)
- `cmake-gen.md` - ❌ ROS1 references, missing category
- `package-xml-gen.md` - ❌ ROS1 format, missing category
- `launch-gen.md` - ⚠️ May have ROS1 references
- `ros-msg-gen.md` - ⚠️ Check for ROS1 patterns
- `cpp-node-template.md` - ❌ ROS1 patterns, long examples
- `py-node-template.md` - ❌ Uses rospy not rclpy
- `ros-package-structure.md` - ⚠️ catkin structure
- `yaml-config.md` - ✅ Relatively good

#### Modbus (2 files)
- `modbus-handler.md` - ⚠️ Needs frontmatter
- `register-map-parser.md` - ⚠️ Needs frontmatter

#### Verification (5 files)
- `verify-ros-node.md` - ✅ Excellent (created in Phase 2)
- `verify-build.md` - ✅ Excellent (created in Phase 2)
- `verify-tests.md` - ✅ Excellent (created in Phase 2)
- `verify-lint.md` - ✅ Excellent (created in Phase 2)
- `verify-integration.md` - ✅ Excellent (created in Phase 2)

#### Analysis (4 files)
- `bag-analyze.md` - ⚠️ Needs frontmatter, output format
- `code-pattern-detect.md` - ⚠️ Needs frontmatter, output format
- `ros-graph-analyze.md` - ⚠️ Needs frontmatter, output format
- `tf-visualize.md` - ⚠️ Needs frontmatter, output format

#### Robot (4 files)
- `urdf-builder.md` - ⚠️ Needs frontmatter
- `protocol-translate.md` - ⚠️ Needs frontmatter
- `diagnostic-logger.md` - ⚠️ Needs frontmatter
- `calibration-helper.md` - ⚠️ Needs frontmatter

### Agents (29 files)

#### Workflow (2 files)
- `dev.md` - ⚠️ Phase 7 enhancement needed
- `execute.md` - ✅ Enhanced in Phase 2, needs minor frontmatter

#### ROS (8 files)
- `create-ros-node.md` - ❌ ROS1 workflow, needs update
- `ros-debug.md` - ⚠️ Check for ROS1 commands
- `ros-test-gen.md` - ⚠️ Check for ROS1 patterns
- `ros-launch-mgr.md` - ⚠️ XML vs Python launches
- `ros-msg-design.md` - ⚠️ Check message patterns
- `ros-bridge-build.md` - ⚠️ Check for ROS1
- `ros-pkg-create.md` - ❌ catkin workspace
- `api-documenter.md` - ⚠️ Check for ROS1

#### Modbus (5 files)
- `modbus-bridge.md` - ⚠️ Needs frontmatter
- `modbus-client-gen.md` - ⚠️ Needs frontmatter
- `modbus-server-gen.md` - ⚠️ Needs frontmatter
- `modbus-doc.md` - ⚠️ Needs frontmatter
- `register-mapper.md` - ⚠️ Needs frontmatter

#### C++ (3 files)
- `cpp-refactor.md` - ⚠️ Needs frontmatter
- `cpp-optimize.md` - ⚠️ Needs frontmatter, should reference cpp-best-practices.md
- `cmake-build.md` - ❌ catkin build commands

#### Python (2 files)
- `py-analyze.md` - ⚠️ Needs frontmatter, should reference python-best-practices.md
- `py-type-check.md` - ⚠️ Needs frontmatter

#### Testing (2 files)
- `sim-validator.md` - ⚠️ Needs frontmatter
- `hw-mocker.md` - ⚠️ Needs frontmatter

#### Quality (3 files)
- `pattern-detector.md` - ⚠️ Needs frontmatter
- `cross-lang-review.md` - ⚠️ Needs frontmatter
- `realtime-check.md` - ⚠️ Needs frontmatter, should reference cpp-best-practices.md

#### Documentation (1 file)
- `arch-diagram.md` - ⚠️ Needs frontmatter

#### Workspace (1 file)
- `catkin-workspace.md` - ❌ Entire file is ROS1/catkin

#### Deployment (2 files)
- `deploy-script.md` - ⚠️ Needs frontmatter
- `param-config.md` - ⚠️ Needs frontmatter, ROS2 parameter format

---

## Implementation Priority Matrix

### Critical (Do First)
**Impact: High | Effort: Low**

1. Add missing frontmatter fields (category, complexity, requires)
   - Files: ~45
   - Time: 30 minutes
   - Impact: Consistency, discoverability

2. Update ROS1 → ROS2 references
   - Files: ~12
   - Time: 2 hours
   - Impact: Correctness, usability

3. Add exit codes to skills
   - Files: ~45
   - Time: 45 minutes
   - Impact: Better error handling

### Important (Do Second)
**Impact: Medium | Effort: Medium**

4. Standardize output formats
   - Files: ~30
   - Time: 3 hours
   - Impact: Professional appearance, consistency

5. Enhance error messages
   - Files: ~25
   - Time: 2 hours
   - Impact: Better user guidance

### Nice to Have (Do Later)
**Impact: Medium | Effort: High**

6. Extract examples to reference files
   - Files: ~8
   - Time: 4 hours
   - Impact: Token efficiency

7. Add response_format options
   - Files: ~20
   - Time: 3 hours
   - Impact: Flexibility

---

## Automated Update Script Ideas

### Script 1: Frontmatter Standardization
```bash
#!/bin/bash
# add-frontmatter.sh
# Adds missing frontmatter fields to all commands

for file in .claude/commands/**/*.md; do
    # Parse existing frontmatter
    # Determine category from directory
    # Estimate complexity from file length
    # Add missing fields
done
```

### Script 2: ROS Version Update
```bash
#!/bin/bash
# ros1-to-ros2.sh
# Updates ROS1 references to ROS2

sed -i 's/catkin build/colcon build/g' **/*.md
sed -i 's/rosrun/ros2 run/g' **/*.md
sed -i 's/roslaunch/ros2 launch/g' **/*.md
# ... more replacements
```

### Script 3: Exit Code Addition
```bash
#!/bin/bash
# add-exit-codes.sh
# Adds exit code section to skills without one

for file in .claude/commands/skills/**/*.md; do
    if ! grep -q "Exit Codes" "$file"; then
        # Append standard exit code section
    fi
done
```

---

## Metrics

### Completion Status by Category

| Category | Total Files | Needs Work | % Complete |
|----------|-------------|------------|------------|
| Verification | 5 | 0 | 100% ✅ |
| Workflow | 4 | 2 | 50% |
| Git | 3 | 3 | 0% |
| ROS Skills | 8 | 7 | 13% |
| ROS Agents | 8 | 7 | 13% |
| Modbus | 7 | 7 | 0% |
| C++ | 3 | 3 | 0% |
| Python | 2 | 2 | 0% |
| Testing | 2 | 2 | 0% |
| Quality | 3 | 3 | 0% |
| Analysis | 4 | 4 | 0% |
| Robot | 4 | 4 | 0% |
| Meta | 2 | 2 | 0% |
| Others | 4 | 4 | 0% |
| **TOTAL** | **59** | **50** | **15%** |

### Estimated Effort

| Task | Files | Hours | Priority |
|------|-------|-------|----------|
| Frontmatter | 45 | 0.5 | HIGH |
| ROS updates | 12 | 2.0 | HIGH |
| Exit codes | 45 | 0.75 | HIGH |
| Output format | 30 | 3.0 | MEDIUM |
| Error messages | 25 | 2.0 | MEDIUM |
| Extract examples | 8 | 4.0 | LOW |
| Response formats | 20 | 3.0 | LOW |
| **TOTAL** | - | **15.25** | - |

---

## Recommendations

### Phase 1 Tasks (Aligns with Plan)
The Phase 1 "Progressive Disclosure Pattern" tasks directly address findings:
1. ✅ Standardize YAML frontmatter - Addresses Finding #1
2. ✅ Extract examples to reference files - Addresses Finding #6
3. ✅ Create shared reference docs - Supports error message improvements

### Quick Wins for Next Session
1. **Batch update frontmatter** - Use script or systematic approach
2. **Update top 12 ROS files** - Highest impact for correctness
3. **Add exit codes** - Simple addition, big improvement

### Long-term Improvements
1. Create templates for new skills/agents
2. Set up pre-commit hooks for frontmatter validation
3. Automate ROS version checks
4. Add linting for command consistency

---

## Conclusion

**Status**: 15% of files meet current best practices standard

**Key Insight**: The verification skills created in Phase 2 represent the quality standard. All other files should be brought to this level.

**Recommendation**: Proceed with Phase 1 tasks (frontmatter standardization, example extraction) as they directly address the largest gaps identified in this audit.

**Next Steps**:
1. Execute Phase 1 tasks systematically
2. Use tool-design-guide.md as reference
3. Update files in batches by category
4. Test updated commands for consistency
5. Update this audit report as work progresses
