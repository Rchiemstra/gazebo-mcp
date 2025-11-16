You are executing the `/create-project-plan` command for: $ARGUMENTS

## Your Mission

Invoke the **project-plan-orchestrator** to create a comprehensive, context-aware project plan that:
1. Analyzes the codebase to find relevant files
2. Uses that analysis to inform the planning process
3. Generates an educational implementation plan

## Command Process

### Step 1: Validate Input
Check if $ARGUMENTS contains a clear project description:
- Is there a feature/functionality described?
- Is the scope clear enough to search for files?

**If unclear or empty**:
```markdown
## ⚠️ Project Description Needed

Please provide a description of what you want to plan:

**Examples**:
- `/create-project-plan autonomous navigation system`
- `/create-project-plan computer vision object detection`
- `/create-project-plan motor control with PID`
- `/create-project-plan web API for robot control`

**Usage**: `/create-project-plan [feature description]`
```
Stop execution and wait for user input.

### Step 2: Invoke Project Plan Orchestrator
Call the project-plan-orchestrator agent with the user's request:

```
Agent: project-plan-orchestrator
Prompt: "Create a comprehensive project plan for: $ARGUMENTS

Please orchestrate the sequential workflow:
1. Use file-search-agent to find and document relevant files
2. Use plan-generation-mentor to create context-aware plan
3. Ensure the plan references actual codebase files

User request: $ARGUMENTS
"
```

### Step 3: Present Results
After orchestration completes, present a summary:

```markdown
## ✅ Project Plan Created Successfully!

### 📋 What Was Generated

**1. Codebase Analysis**
- File: `project-context/relevant-files-[timestamp].md`
- Contains: Comprehensive list of relevant files with analysis
- Files found: [X] files across [Y] categories

**2. Learning Implementation Plan**
- File: `plans/[date]-[feature]-learning-plan.md`
- Phases: [X] learning phases
- Duration: Estimated [N] weeks
- Context: Integrated with existing codebase structure

### 🚀 Next Steps

**Option 1: Review the Plan**
- Read the generated plan: `plans/[date]-[feature]-learning-plan.md`
- Check codebase analysis: `project-context/relevant-files-[timestamp].md`
- Ask questions about any phase or component

**Option 2: Start Learning**
- Use `/continue-plan` to begin Phase 1
- The learning-coordinator will guide you through each phase
- Specialists will be available to help with concepts

**Option 3: Modify the Plan**
- Use `/update-plan` to adjust phases or add details
- Request changes to focus areas
- Adjust timeline or complexity

### 💡 Understanding Your Plan

Your plan includes:
- 📚 **Research tasks** to understand concepts and existing code
- 🎯 **Design decisions** you'll make with guidance
- 🔨 **Implementation phases** with progressive complexity
- ✅ **Learning checkpoints** to verify understanding
- 👥 **Specialist support** for each phase

This is a **learning journey**, not just a task list!

---

Ready to start? Use `/continue-plan` to begin Phase 1!
```

## Error Handling

### If Orchestrator Fails
```markdown
## ⚠️ Plan Generation Encountered an Issue

The orchestration process had a problem:
[Error details]

### Alternatives:

**Option 1**: Try a more specific description
- Current: $ARGUMENTS
- Try: [Suggest more specific version]

**Option 2**: Manual planning
- I can create a general plan without codebase analysis
- Use `/create-plan $ARGUMENTS` for standard planning

**Option 3**: Phased approach
- Start with codebase analysis only
- Then create plan manually with that context

What would you like to do?
```

### If No Files Found
```markdown
## 📋 Plan Created (New Feature)

The codebase analysis found no existing files related to this feature.
This appears to be a completely new addition!

Your plan has been created with:
- ✅ General project structure guidance
- ✅ Recommendations for where to place new files
- ✅ Pattern suggestions based on project style
- ✅ Learning phases for building from scratch

File: `plans/[date]-[feature]-learning-plan.md`

This is a fresh start - exciting! Use `/continue-plan` to begin.
```

## Usage Examples

### Example 1: Robotics Feature
```bash
/create-project-plan autonomous navigation with obstacle avoidance
```

**Expected Result**:
- Finds: robot control files, sensor files, config files
- Analyzes: existing movement system, available sensors
- Plans: integration with current control, new navigation module
- Output: Context-aware plan with specific file modifications

### Example 2: Vision Feature
```bash
/create-project-plan object detection and tracking
```

**Expected Result**:
- Finds: camera interface, image processing code
- Analyzes: existing vision pipeline, ROS2 nodes
- Plans: detection algorithm integration, tracking system
- Output: Plan with existing vision code integration points

### Example 3: API Feature
```bash
/create-project-plan REST API for robot control
```

**Expected Result**:
- Finds: current control interfaces, command handlers
- Analyzes: existing command structure, safety mechanisms
- Plans: API layer, authentication, rate limiting
- Output: Plan showing how API wraps existing control

## Integration with Learning System

After plan creation:
- Plan is ready for `/continue-plan` command
- learning-coordinator can guide through phases
- Specialists are mapped for each phase
- Progress can be tracked with `/update-plan`

## Command Philosophy

This command is **the starting point** for substantial projects:
- Provides **context-aware** planning (not generic)
- Creates **educational** plans (learning-focused)
- Enables **informed** development (knows existing code)
- Supports **iterative** learning (phases with checkpoints)

Use this when:
- ✅ Starting a new feature that might touch existing code
- ✅ Complex projects needing structured learning approach
- ✅ Want to understand existing codebase before building
- ✅ Need comprehensive plan with multiple phases

Don't use for:
- ❌ Quick questions or simple modifications
- ❌ Debugging specific issues (use debugging-detective)
- ❌ Learning a concept without implementing (use /ask-specialist)

## Success Criteria

Command succeeds when:
- ✅ Relevant files documented comprehensively
- ✅ Learning plan created with phases
- ✅ Plan references actual codebase files
- ✅ Integration points identified
- ✅ User has clear next steps

## Remember

This command **orchestrates** a sophisticated workflow:
1. Intelligence gathering (file search)
2. Context-aware planning (plan generation)
3. Educational structure (learning phases)

The result is not just a TODO list, but a **learning implementation journey** that respects and integrates with existing code!
