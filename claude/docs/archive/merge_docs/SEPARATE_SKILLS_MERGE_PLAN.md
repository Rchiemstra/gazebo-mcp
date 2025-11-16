# Separate Skills Merge Plan - Complete Analysis

**Date:** 2025-11-10
**Status:** Ready for approval
**Source:** separate_skills/claude/ (67 ROS/robotics commands)
**Target:** ~/.claude/commands/ (user-global installation)

---

## Executive Summary

The `separate_skills/claude/` directory contains **67 production-ready Claude Code markdown commands** specialized for ROS2/robotics development. These complement (not replace) the existing workspace structure.

**Recommendation:** Install to `~/.claude/commands/` for user-global access while preserving workspace structure.

---

## What We Have

### Uploaded Skills (35 commands)
- **Meta:** `/create-skill`, `/create-agent`
- **Workflow:** `/gather-context`, `/plan`, `/explore`, `/compact-context`, `/context-snapshot`, `/context-restore`
- **Git:** `/git-stage`, `/git-commit-msg`, `/git-commit`
- **ROS:** `/cmake-gen`, `/package-xml-gen`, `/launch-gen`, `/ros-msg-gen`, `/cpp-node-template`, `/py-node-template`, `/yaml-config`, `/ros-package-structure`
- **Modbus:** `/modbus-handler`, `/register-map-parser`
- **Analysis:** `/ros-graph-analyze`, `/bag-analyze`, `/tf-visualize`, `/code-pattern-detect`
- **Robot:** `/urdf-builder`, `/protocol-translate`, `/diagnostic-logger`, `/calibration-helper`
- **Debugging:** `/diagnose-error`
- **Verification:** `/verify-build`, `/verify-tests`, `/verify-lint`, `/verify-ros-node`, `/verify-integration`

### Uploaded Agents (32 commands)
- **Workflow:** `/dev`, `/dev-tdd`, `/dev-visual`, `/dev-quick`, `/execute`
- **ROS:** `/create-ros-node`, `/ros-debug`, `/ros-test-gen`, `/ros-launch-mgr`, `/ros-msg-design`, `/ros-bridge-build`, `/ros-pkg-create`, `/api-documenter`
- **Modbus:** `/modbus-bridge`, `/modbus-client-gen`, `/modbus-server-gen`, `/modbus-doc`, `/register-mapper`
- **C++:** `/cpp-refactor`, `/cpp-optimize`, `/cmake-build`
- **Python:** `/py-analyze`, `/py-type-check`
- **Testing:** `/sim-validator`, `/hw-mocker`
- **Quality:** `/pattern-detector`, `/cross-lang-review`, `/realtime-check`
- **Documentation:** `/arch-diagram`
- **Workspace:** `/catkin-workspace`
- **Deployment:** `/deploy-script`, `/param-config`

### Documentation (19 files)
- **Main:** CLAUDE.md (complete reference)
- **Best Practices:** best-practices.md, cpp-best-practices.md, python-best-practices.md
- **Patterns:** ros-patterns.md, modbus-patterns.md, error-patterns.md
- **Examples:** 8 example files (cpp-node-examples.md, py-node-examples.md, etc.)
- **Guides:** TOKEN_OPTIMIZATION_GUIDE.md, ERROR_HANDLING_QUICK_REFERENCE.md, test-strategies.md, verification-checklist.md

### Context Templates (5 files)
- generic-context-template.md
- cpp-context-template.md
- python-context-template.md
- ros-context-template.md
- modbus-context-template.md

---

## Current Workspace Structure

### What We Already Have
- **20 Python Skills** (in `skills/`): code_analysis, test_orchestrator, git_workflow_assistant, etc.
  - **Format:** Python packages with operations.py
  - **Purpose:** General-purpose development tools
  - **Integration:** Import-based (from skills.x import y)

- **17 Markdown Agents** (in `agents/`): learning-coordinator, plan-generation-mentor, etc.
  - **Format:** Markdown with frontmatter
  - **Purpose:** Teaching/mentoring agents
  - **Integration:** Claude Code CLI commands

- **3 Phase Meta Tools** (created in Phases 1-3):
  - SkillRegistry for skill discovery
  - Enhanced context_manager
  - Complete documentation (TOKEN_EFFICIENCY_COMPLETE.md, TOOL_DESIGN_EXCELLENCE_COMPLETE.md)

---

## Key Differences

| Aspect | Workspace | separate_skills/claude/ |
|--------|-----------|-------------------------|
| **Format** | Mixed (Python + Markdown) | Pure Markdown commands |
| **Purpose** | General development + learning | ROS/robotics-focused |
| **Scope** | Broad (testing, docs, learning) | Deep (ROS2, Modbus, robotics) |
| **Integration** | Python skill system | Claude Code commands |
| **Installation** | Project-specific | User's ~/.claude/commands/ |
| **Domain** | Generic software | Robotics/embedded systems |
| **Dependencies** | Python runtime | Claude Code CLI only |

---

## Naming Analysis - NO CONFLICTS!

**Workspace agents:**
- `agent-creator.md`, `skill-creator.md`
- `git-workflow-expert.md`, `cpp-best-practices.md`

**separate_skills commands:**
- `/create-agent`, `/create-skill`
- `/git-commit`, `/cpp-node-template`

**Result:** Different naming patterns = No conflicts

---

## Recommended Strategy: Parallel Installation

### Why This Approach?

1. ✅ **No Conflicts** - Different namespaces, different purposes
2. ✅ **Complementary** - Workspace = general dev, separate_skills = ROS-specific
3. ✅ **User Choice** - Developers can choose which tools to use
4. ✅ **Easy Rollback** - Can uninstall cleanly if needed
5. ✅ **Global Access** - ROS commands available to all projects

### Installation Structure

```
~/.claude/commands/           ← Global ROS/robotics commands
├── skills/
│   ├── analysis/
│   ├── git/
│   ├── meta/
│   ├── modbus/
│   ├── robot/
│   ├── ros/
│   ├── verification/
│   └── workflow/
└── agents/
    ├── cpp/
    ├── deployment/
    ├── documentation/
    ├── modbus/
    ├── python/
    ├── quality/
    ├── ros/
    ├── testing/
    ├── workflow/
    └── workspace/

~/.claude/                    ← Global documentation
├── CLAUDE.md
├── *-patterns.md
├── *-examples.md
├── context-templates/
└── settings.local.json

/workspace/                   ← Project-specific (unchanged)
├── skills/                   ← Python packages
├── agents/                   ← Teaching agents
├── docs/                     ← Workspace docs
└── templates/
```

---

## Implementation Plan

### Phase 1: Pre-Installation Validation (5 min)

**Actions:**
```bash
# 1. Verify separate_skills structure
ls -la separate_skills/claude/commands/skills/
ls -la separate_skills/claude/commands/agents/

# 2. Check target directory
ls -la ~/.claude/ 2>/dev/null || echo "Will create ~/.claude/"

# 3. Verify no naming conflicts
# (Already confirmed - different naming patterns)
```

**Expected Output:**
- 35 skills in separate_skills/claude/commands/skills/
- 32 agents in separate_skills/claude/commands/agents/
- ~/.claude/ either doesn't exist or is ready for installation

---

### Phase 2: Backup Existing ~/.claude/ (if exists) (2 min)

**Actions:**
```bash
# Create backup if ~/.claude/ exists
if [ -d ~/.claude ]; then
    backup_dir=~/.claude.backup.$(date +%Y%m%d_%H%M%S)
    cp -r ~/.claude "$backup_dir"
    echo "Backup created: $backup_dir"
fi
```

---

### Phase 3: Install Commands (2 min)

**Actions:**
```bash
# Create directory structure
mkdir -p ~/.claude/commands

# Copy skills and agents
cp -r separate_skills/claude/commands/* ~/.claude/commands/

# Verify installation
echo "Skills installed: $(find ~/.claude/commands/skills -name '*.md' | wc -l)"
echo "Agents installed: $(find ~/.claude/commands/agents -name '*.md' | wc -l)"
```

**Expected Output:**
```
Skills installed: 35
Agents installed: 32
```

---

### Phase 4: Install Documentation (2 min)

**Actions:**
```bash
# Copy reference documentation
cp separate_skills/claude/*.md ~/.claude/
cp -r separate_skills/claude/context-templates ~/.claude/
cp separate_skills/claude/settings.local.json ~/.claude/

# List installed docs
ls ~/.claude/*.md
```

**Expected Output:**
- 19 documentation files in ~/.claude/
- context-templates/ directory
- settings.local.json

---

### Phase 5: Verification (5 min)

**Actions:**
```bash
# 1. Verify structure
tree -L 3 ~/.claude/

# 2. Test command accessibility (if Claude Code CLI available)
# Note: This assumes Claude Code CLI is configured
# /dev --help
# /create-ros-node --help

# 3. Verify documentation
cat ~/.claude/CLAUDE.md | head -50
```

**Expected Output:**
- Complete directory structure
- Commands accessible via Claude Code CLI
- Documentation readable

---

### Phase 6: Update Workspace Documentation (10 min)

**Actions:**
1. Update `README.md` with section on available command systems
2. Create `docs/COMMANDS_REFERENCE.md` linking to ~/.claude/CLAUDE.md
3. Update `docs/TOOL_DESIGN_EXCELLENCE_COMPLETE.md` to reference ROS commands

**New README Section:**
```markdown
## Available Command Systems

This workspace provides multiple layers of development tools:

### 1. Workspace Python Skills (General Purpose)
Located: `skills/`
- General software development tools
- Import-based: `from skills.code_analysis import analyze_file`
- Examples: code_analysis, test_orchestrator, refactor_assistant

### 2. Workspace Agents (Teaching/Mentoring)
Located: `agents/`
- Teaching and mentoring agents
- Examples: learning-coordinator, plan-generation-mentor

### 3. ROS/Robotics Commands (Domain-Specific)
Located: `~/.claude/commands/` (user-global)
- 67 specialized ROS2/robotics commands
- Usage: `/command-name [arguments]`
- Reference: `~/.claude/CLAUDE.md`
- Examples: /create-ros-node, /verify-build, /dev

**When to use what:**
- **Python skills:** Complex operations, data analysis, code generation
- **Agents:** Learning, planning, coordinated workflows
- **ROS commands:** Quick ROS tasks, package creation, verification
```

---

### Phase 7: Testing (15 min)

**Test Cases:**
```bash
# Test 1: Context gathering
/gather-context "Understand ROS package structure"

# Test 2: ROS node creation
/create-ros-node test_sensor_node python

# Test 3: Verification
/verify-ros-node test_sensor_node

# Test 4: Complete workflow
/dev "Create a simple ROS2 publisher node"

# Test 5: Git integration
/git-stage src/test_node.py
/git-commit-msg
/git-commit

# Test 6: Documentation generation
/api-documenter test_sensor_node
```

**Expected Results:**
- All commands execute without errors
- Output follows documented formats
- Verification passes for created artifacts

---

## Alternative Strategies (For Reference)

### Strategy B: Workspace-Local Installation

**If you prefer project-specific commands:**
```bash
# Copy to workspace
mkdir -p .claude/commands
cp -r separate_skills/claude/commands/* .claude/commands/
cp separate_skills/claude/*.md .claude/
```

**Pros:**
- Project self-contained
- Team shares same commands
- Version controlled

**Cons:**
- Duplicates across projects
- Not available to other projects
- Larger repository

---

### Strategy C: Selective Integration

**If you only want specific commands:**
```bash
# Copy only ROS commands
cp -r separate_skills/claude/commands/skills/ros ~/.claude/commands/skills/
cp -r separate_skills/claude/commands/agents/ros ~/.claude/commands/agents/

# Copy only relevant docs
cp separate_skills/claude/ros-patterns.md ~/.claude/
cp separate_skills/claude/ros-*.md ~/.claude/
```

**Pros:**
- Smaller footprint
- Focused on needed domains
- Less to maintain

**Cons:**
- Miss out on workflow tools
- Incomplete documentation
- May need other commands later

---

## Rollback Plan

If issues arise:

```bash
# Remove installed commands
rm -rf ~/.claude/commands/skills/*
rm -rf ~/.claude/commands/agents/*

# Restore from backup
backup_dir=$(ls -dt ~/.claude.backup.* | head -1)
cp -r "$backup_dir"/* ~/.claude/

# Or clean install
rm -rf ~/.claude
# Reinstall from backup or start fresh
```

---

## Benefits of This Approach

### For Individual Developers
- ✅ **67 new ROS commands** available globally
- ✅ **Complete workflows** (/dev, /dev-tdd, /dev-visual)
- ✅ **Verification tools** (/verify-build, /verify-tests, /verify-ros-node)
- ✅ **Quick actions** (/create-ros-node, /git-commit, /launch-gen)
- ✅ **Reference documentation** always available

### For Teams
- ✅ **Standardized workflows** across team members
- ✅ **Consistent verification** before commits
- ✅ **Shared patterns** (ros-patterns.md, modbus-patterns.md)
- ✅ **Template-based creation** (context-templates/)
- ✅ **Quality gates** (verification-checklist.md)

### For Projects
- ✅ **Faster ROS development** with specialized tools
- ✅ **Better code quality** with verification skills
- ✅ **Consistent structure** following best practices
- ✅ **Comprehensive docs** with examples
- ✅ **Multiple workflow options** (quick, TDD, visual)

---

## Post-Installation Next Steps

### Week 1: Learning
1. Read `~/.claude/CLAUDE.md` - Overview of all 67 commands
2. Try `/dev "Create a simple ROS node"` - Experience complete workflow
3. Explore `/gather-context`, `/plan`, `/execute` - Understand phased approach
4. Test verification: `/verify-build`, `/verify-tests`, `/verify-lint`

### Week 2: Integration
1. Use `/create-ros-node` for new nodes
2. Implement `/dev-tdd` workflow on a feature
3. Apply `/verify-ros-node` to existing nodes
4. Create context snapshots with `/context-snapshot`

### Week 3: Team Adoption
1. Share CLAUDE.md with team
2. Demonstrate /dev workflow in team meeting
3. Establish verification standards using installed skills
4. Create team-specific context templates

---

## Success Criteria

Installation is successful when:
- ✅ 35 skills installed in ~/.claude/commands/skills/
- ✅ 32 agents installed in ~/.claude/commands/agents/
- ✅ 19 documentation files in ~/.claude/
- ✅ 5 context templates in ~/.claude/context-templates/
- ✅ Commands accessible via Claude Code CLI
- ✅ Test workflows execute successfully
- ✅ Documentation is readable and navigable
- ✅ Workspace README updated with reference

---

## Risk Assessment

### Low Risk ✅
- **Installation**: Simple file copy, no code execution
- **Conflicts**: None identified (different namespaces)
- **Rollback**: Easy (backup created, can restore)
- **Impact**: Additive only, doesn't modify workspace

### Mitigations
- **Backup before install**: Preserve existing ~/.claude/
- **Verification steps**: Confirm counts after copy
- **Test cases**: Validate functionality before team rollout
- **Documentation**: Clear usage guide in README

---

## Summary

**What:** Install 67 ROS/robotics Claude Code commands to ~/.claude/commands/

**Why:** Provides specialized tools for ROS development without conflicting with workspace structure

**How:** Simple copy operation with verification

**When:** Ready to proceed after approval

**Impact:** Positive - adds capabilities, no conflicts, easy rollback

**Effort:** 30 minutes installation + testing

**Value:** HIGH - Complete ROS development toolkit

---

## Approval Checklist

Before proceeding, confirm:
- [ ] Understand this installs to ~/.claude/ (user-global)
- [ ] Understand workspace structure remains unchanged
- [ ] Understand commands are additive (no conflicts)
- [ ] Understand rollback plan if needed
- [ ] Ready to test workflows after installation
- [ ] Team will be informed of new commands

---

## Ready to Proceed?

**Recommended Action:** Proceed with Parallel Installation (Strategy A)

**Next Step:** Execute Phase 1-7 of implementation plan

**Estimated Time:** 30-40 minutes total

**Expected Outcome:** 67 new commands available, workspace enhanced, team productive

---

**Status:** Awaiting approval to proceed
**Created:** 2025-11-10
**Last Updated:** 2025-11-10
