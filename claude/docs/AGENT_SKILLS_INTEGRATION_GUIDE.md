# Agent-Skills Integration Guide

**Purpose**: Complete guide for how Claude Code agents use the skills system
**Date**: 2025-10-19
**Status**: Production Ready

---

## Overview

The skills system provides **data and analytics**, while agents provide **teaching and decisions**. This separation enables intelligent, personalized, adaptive teaching.

**Skills** (Data Layer):
- learning-plan-manager
- code-analysis
- learning-analytics
- interactive-diagram
- session-state

**Agents** (Teaching Layer):
- learning-coordinator
- plan-generation-mentor
- All specialist teaching agents

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent-Skills Flow                         │
└─────────────────────────────────────────────────────────────┘

1. Student Interaction
   ↓
2. Agent invokes Skills
   │
   ├─→ session-state: Get student profile, history
   ├─→ learning-plan-manager: Get current plan, progress
   ├─→ learning-analytics: Detect struggles, get insights
   ├─→ interactive-diagram: Generate visual aids
   └─→ code-analysis: Understand codebase context
   ↓
3. Agent receives Skills data
   ↓
4. Agent makes Teaching Decisions
   - Adapt approach based on student profile
   - Adjust difficulty based on struggles
   - Include visuals for visual learners
   - Celebrate achievements
   ↓
5. Agent provides Personalized Response
   ↓
6. Agent updates Skills
   └─→ session-state: Record effective strategies
```

---

## When Agents Should Use Each Skill

### session-state

**When to use**:
- ✅ **Session start**: Load student profile, welcome by name
- ✅ **Session end**: Record effective strategies, check achievements
- ✅ **Student seems stuck**: Check what worked before
- ✅ **Planning new feature**: Understand student's learning style
- ✅ **Celebrating milestones**: Check for new achievements

**Example queries**:
```
"Get student profile for alex_2025 including recent activity"
"Check achievements for student alex_2025"
"Record that visual diagrams worked well for alex_2025"
"Get teaching insights for alex_2025"
```

**What the skill returns**:
- Student profile (name, learning style, preferences)
- Recent activity (sessions, tasks, time spent)
- Achievements earned
- Teaching insights (effective/ineffective strategies)

### learning-analytics

**When to use**:
- ✅ **Every few messages**: Check if student struggling
- ✅ **Student asks for help repeatedly**: Get struggle analysis
- ✅ **Planning sessions**: Understand typical velocity
- ✅ **Progress check**: Get health assessment
- ✅ **Adaptive teaching**: Get recommendations for adaptation

**Example queries**:
```
"Analyze current learning plan and detect struggles"
"Get velocity metrics for student's current plan"
"Check health status and provide recommendations"
```

**What the skill returns**:
- Velocity metrics (tasks/week, trend)
- Struggle areas with severity
- Health status (excellent, good, needs_attention, struggling)
- Recommendations for teaching adaptation
- Checkpoint performance analysis

### learning-plan-manager

**When to use**:
- ✅ **Session start**: Get current plan and next task
- ✅ **Student asks "what's next"**: Get next recommended task
- ✅ **Progress updates**: Get completion percentage
- ✅ **Planning new work**: See what student already learned
- ✅ **Reflection time**: Access learning journal

**Example queries**:
```
"Get current learning plan and next recommended task"
"Get all completed plans for student"
"Get learning journal entries for current plan"
```

**What the skill returns**:
- Current plan details
- Phase and task information
- Progress percentages
- Next recommended task
- Learning journal entries

### interactive-diagram

**When to use**:
- ✅ **Explaining complex concepts**: Generate concept diagrams
- ✅ **Showing progress**: Generate progress charts
- ✅ **Visual learners**: Include diagrams frequently
- ✅ **Plan overview**: Show Gantt chart timeline
- ✅ **Architecture questions**: Generate dependency graphs

**Example queries**:
```
"Generate progress chart for current learning plan"
"Create learning journey flowchart showing phases"
"Generate Gantt chart for plan timeline"
```

**What the skill returns**:
- Mermaid diagram code (ready to display)
- Diagram metadata (type, title, etc.)
- Can export to markdown or HTML

### code-analysis

**When to use**:
- ✅ **Planning new features**: Find integration points
- ✅ **Architecture questions**: Understand codebase structure
- ✅ **Code review**: Identify code smells
- ✅ **Teaching patterns**: Show existing patterns to follow
- ✅ **Dependency questions**: Understand component relationships

**Example queries**:
```
"Analyze src/ directory to understand architecture"
"Find integration points for navigation feature"
"Analyze code quality and identify code smells"
```

**What the skill returns**:
- File analysis (classes, functions, complexity)
- Design patterns detected
- Integration point suggestions
- Code smells and quality issues
- Dependency relationships

---

## Agent-Specific Integration Patterns

### learning-coordinator (Orchestrator)

**Role**: Master coordinator, uses ALL skills

**Typical flow**:

1. **Session Start**:
```
Skill(session-state): Get student profile and recent activity
Skill(learning-plan-manager): Get current plan and next task
Skill(learning-analytics): Check for any struggles
```

2. **Personalized Welcome**:
```markdown
"Welcome back, {student.name}! 👋

Last session: {activity.last_session}
Tasks this week: {activity.tasks_completed}
{if achievements:} 🎉 You unlocked: {achievement}

Based on your {profile.learning_style} learning style, I'll {adaptation}.

You're on {plan.current_phase}, next up: {plan.next_task}

{if analytics.struggles:} I noticed {struggle} - let's focus there today.

Ready to continue?"
```

3. **During Session** (every 3-4 messages):
```
Skill(learning-analytics): Check for struggles
{if struggling:}
  - Adapt teaching approach
  - Route to specialist
  - Break tasks smaller
```

4. **After Explaining Concept**:
```
{if student.learning_style == "visual":}
  Skill(interactive-diagram): Generate concept diagram
  Include diagram in explanation
```

5. **Session End**:
```
Skill(session-state): End session and check achievements
{if new achievements:}
  Celebrate achievements
Skill(session-state): Record which teaching strategies worked
```

**Key principle**: Always personalize, never generic!

---

### plan-generation-mentor (Planner)

**Role**: Creates personalized learning plans, uses 4 skills

**Typical flow**:

1. **Understand Student**:
```
Skill(session-state): Get student profile, history, velocity
Skill(learning-plan-manager): Get completed plans (what they know)
```

2. **Understand Codebase**:
```
Skill(code-analysis): Analyze relevant code for integration points
```

3. **Estimate Timeline**:
```
Skill(learning-analytics): Get student's typical velocity
→ Use for realistic time estimates
```

4. **Create Personalized Plan**:
```markdown
# {Feature} Learning Plan - Personalized for {student.name}

## 🎯 Tailored for Your Learning Style
Based on your profile:
- ✅ {learning_style} approach (e.g., "Visual diagrams in each phase")
- ✅ {difficulty} level challenges
- ✅ Paced at {velocity} tasks/week
- ✅ Building on your completed "{previous_plan}"

{if learning_style == "visual":}
## 📊 Your Learning Timeline
{Gantt chart from interactive-diagram}
```

5. **Add Visual Timeline**:
```
Skill(interactive-diagram): Generate Gantt chart
Include in plan
```

**Key principle**: Personalize based on student data!

---

### Specialist Agents (Teachers)

**Examples**: robotics-vision-navigator, ros2-learning-mentor, etc.

**Role**: Teach specific topics, use 2-3 skills

**Typical flow**:

1. **Check Student Context** (optional, for personalization):
```
Skill(session-state): Get student's learning style
→ Adapt explanation style
```

2. **Teach Concept**:
```
{if student.learning_style == "visual":}
  Skill(interactive-diagram): Generate concept diagram
  Include visual explanation

{if student.learning_style == "hands-on":}
  Provide experiment, not just theory
```

3. **After Teaching**:
```
Skill(session-state): Record strategy effectiveness
"Recorded that {strategy} worked well for {student}"
```

**Key principle**: Adapt to student's learning style!

---

## Skill Invocation Syntax

### In Agent Prompts

Agents invoke skills using natural language:

```
Skill(skill-name) with query:
"Natural language description of what you want"
```

### Examples

**Good invocations**:
```
Skill(session-state) with query:
"Get student profile for alex_2025 including preferences and recent activity"

Skill(learning-analytics) with query:
"Analyze current learning plan and check if student is struggling with any tasks"

Skill(interactive-diagram) with query:
"Generate a progress chart showing completed vs remaining tasks"
```

**Bad invocations** (too vague):
```
Skill(session-state) with query: "Get student"
Skill(learning-analytics) with query: "Check stuff"
```

---

## Personalization Patterns

### Based on Learning Style

**Visual Learners** (`learning_style: "visual"`):
```python
# Agent should:
- Use interactive-diagram frequently
- Include diagrams in every explanation
- Show progress visually
- Use charts, flowcharts, architecture diagrams

# Example:
"Let me show you this visually:
{diagram}
As you can see from the diagram..."
```

**Hands-On Learners** (`learning_style: "hands_on"`):
```python
# Agent should:
- Provide experiments to try
- Less theory, more practice
- "Try this and see what happens" approach
- Incremental experimentation

# Example:
"Let's experiment! Try implementing just the {small_piece} first.
Run it and observe what happens. What do you notice?"
```

**Reading Learners** (`learning_style: "reading"`):
```python
# Agent should:
- Provide documentation links
- Detailed written explanations
- Research tasks
- References to read

# Example:
"Here are some resources to read:
1. {documentation_link}
2. {tutorial}

After reading, what questions do you have?"
```

### Based on Difficulty Preference

**Beginner** (`difficulty_preference: "beginner"`):
```python
# Agent should:
- Smaller tasks (break down more)
- More checkpoints
- Simpler vocabulary
- More examples

# Example:
"Let's start very simple. First, just try getting the {basic_version} working.
Don't worry about {advanced_feature} yet - we'll get there!"
```

**Intermediate** (`difficulty_preference: "intermediate"`):
```python
# Agent should:
- Moderate task size
- Balance guidance and independence
- Assume some background knowledge
- Challenge appropriately

# Example:
"Given your experience with {previous_concept}, this should feel familiar.
The main new concept is {concept}. Try implementing it, and I'm here if you get stuck."
```

**Advanced** (`difficulty_preference: "advanced"`):
```python
# Agent should:
- Larger, complex tasks
- Fewer checkpoints
- Assume strong background
- Push boundaries

# Example:
"This is a complex challenge requiring {concepts}. I'll point you to the key considerations,
but I trust you to design the solution. What's your initial approach?"
```

### Based on Velocity

**Slow Learner** (`velocity < 2 tasks/week`):
```python
# Agent should:
- Build in more time
- Break tasks smaller
- More frequent checkpoints
- Extra encouragement

# Example:
"Take your time with this - it's a meaty concept. Let's break it into 3 smaller steps.
Start with step 1, and come back when ready for step 2."
```

**Fast Learner** (`velocity > 5 tasks/week`):
```python
# Agent should:
- Larger tasks
- Fewer interruptions
- Optional bonus challenges
- Stretch goals

# Example:
"You're moving quickly! Here's the core task. If you finish early,
here's an optional challenge: {bonus_challenge}"
```

### Based on Struggle Detection

**No Struggles** (`health_status: "excellent"`):
```python
# Agent should:
- Maintain current approach
- Maybe increase difficulty slightly
- Celebrate success
- Encourage momentum

# Example:
"You're doing fantastic! Your velocity is strong and no struggles detected.
Ready to keep this momentum going?"
```

**Needs Attention** (`health_status: "needs_attention"`):
```python
# Agent should:
- Slow down
- Simplify explanations
- Route to specialist
- More frequent checkins
- Smaller tasks

# Example:
"I notice you've been stuck on {task} for a while. Let's pause and make sure
you understand {prerequisite_concept}. Can you explain {concept} in your own words?"
```

---

## Recording Teaching Effectiveness

Agents should record what works:

```
# After student successfully completes task:
Skill(session-state) with query:
"Record that visual diagrams with step-by-step annotations worked well for alex_2025"

# After student seems confused by approach:
Skill(session-state) with query:
"Record that abstract mathematical explanations were not effective for alex_2025"

# After specialist interaction:
Skill(session-state) with query:
"Record that robotics-vision-navigator was helpful for alex_2025"
```

This data is then used to personalize future teaching!

---

## Common Integration Mistakes

### ❌ Mistake 1: Not Using Skills Proactively

**Wrong**:
```
Agent: "Hi! What would you like to work on?"
{waits for student to ask about progress}
```

**Right**:
```
{At session start:}
Skill(session-state): Get student
Skill(learning-plan-manager): Get progress
Skill(learning-analytics): Check struggles

Agent: "Welcome back, {name}! You completed {n} tasks this week.
{if struggles:} I notice you're struggling with {topic}. Let's focus there.
Ready to continue with {next_task}?"
```

### ❌ Mistake 2: Using Generic Responses

**Wrong**:
```
Agent: "Good job on completing that task! What's next?"
```

**Right**:
```
Skill(session-state): Check achievements

Agent: "Excellent work completing {task}!
{if new achievement:} 🎉 You just unlocked {achievement}!
Based on your {velocity}, you're {on_track/ahead/behind} schedule.
Next up: {next_task}"
```

### ❌ Mistake 3: Ignoring Learning Style

**Wrong**:
```
{Student's learning_style is "visual"}
Agent: {provides long text explanation without diagrams}
```

**Right**:
```
{Student's learning_style is "visual"}
Skill(interactive-diagram): Generate concept diagram

Agent: "Let me show you this visually:
{diagram}
As you can see from the diagram, {explanation}..."
```

### ❌ Mistake 4: Not Detecting Struggles

**Wrong**:
```
{Student stuck for 2 weeks}
Agent: {continues same approach}
```

**Right**:
```
{Every few messages:}
Skill(learning-analytics): Check for struggles

{if struggling detected:}
Agent: "I notice you've been working on this for a while.
Let's try a different approach. Would it help if I {alternative_approach}?
Or should I connect you with {specialist}?"
```

### ❌ Mistake 5: Not Recording What Works

**Wrong**:
```
{Student succeeds with visual diagrams}
Agent: {doesn't record this}
{Next session uses text-only explanations}
```

**Right**:
```
{Student succeeds with visual diagrams}
Skill(session-state): Record strategy effectiveness

{Next session:}
Skill(session-state): Get teaching insights
{sees visual diagrams worked}
Agent: {uses visual diagrams again}
```

---

## Complete Example: Session Flow

### Student "Alex" Returns

**Step 1: Session Start**
```
Skill(session-state) with query: "Get student alex_2025"
Skill(learning-plan-manager) with query: "Get current plan progress"
Skill(learning-analytics) with query: "Check for struggles"
```

**Returns**:
```json
{
  "student": {
    "name": "Alex",
    "learning_style": "visual",
    "velocity": 3.5
  },
  "activity": {
    "last_session": "yesterday",
    "tasks_this_week": 3
  },
  "achievements": [{"id": "7_day_streak", "title": "7-Day Streak"}],
  "plan": {
    "title": "Navigation",
    "progress": 45,
    "next_task": "Path Planning"
  },
  "analytics": {
    "health": "good",
    "struggles": []
  }
}
```

**Step 2: Personalized Welcome**
```markdown
Welcome back, Alex! 👋

Great to see you again - last session was just yesterday!

Your progress this week:
- 3 tasks completed
- Velocity: 3.5 tasks/week (right on track! ✅)

🎉 New Achievement: **7-Day Streak** 🔥🔥

{Skill(interactive-diagram): Generate progress chart}
{diagram showing 45% complete}

Based on your visual learning style, I'll include diagrams throughout today's session.

You're on the Navigation plan (45% complete). Next up: **Path Planning Algorithm**.

The analytics show you're doing great - no struggles detected!

Ready to tackle path planning?
```

**Step 3: Teaching with Personalization**
```markdown
Alex: "How does path planning work?"

{Student prefers visual}
Skill(interactive-diagram) with query: "Generate concept diagram for path planning algorithm"

Agent: "Great question! Let me show you visually:

{diagram showing path planning flow}

As you can see from the diagram, path planning has these key steps:
1. {step 1 with visual reference}
2. {step 2 with visual reference}
...

Try implementing step 1 first - what's your initial approach?"
```

**Step 4: Detecting if Student Struggles** (later in session)
```
Skill(learning-analytics) with query: "Check current task status"

{if student stuck for 30+ min:}
Agent: "I notice you've been on this step for a bit. That's totally normal - it's a tricky concept!

Would it help to:
1. See a simpler example first?
2. Break this into smaller sub-steps?
3. Talk with robotics-vision-navigator about path planning specifically?

What sounds most helpful?"
```

**Step 5: Session End**
```
Skill(session-state) with query: "End session for alex_2025 and check achievements"
Skill(session-state) with query: "Record that visual diagrams and step-by-step breakdown worked well"

Agent: "Great session, Alex!

You completed:
- ✅ Path Planning Algorithm (Task 2.3)
- ✅ Path Planning Tests (Task 2.4)

🎉 New Achievement: **Task Machine** ⚡⚡⚡ (10 tasks in one session!)

Your velocity is strong at 3.5 tasks/week. At this pace, you'll complete the Navigation plan in ~2 weeks.

Next session, we'll tackle: **Obstacle Avoidance**.

See you next time! 👋"
```

---

## Benefits of Skills Integration

### Before Skills (Generic Teaching)
```
Agent: "Hi! What do you want to learn?"
Student: "Path planning"
Agent: "Path planning involves finding optimal routes. Here's how it works: {generic explanation}"
Student: {struggles}
Agent: {same approach, no adaptation}
```

### After Skills (Personalized Teaching)
```
Agent: "Welcome back, Alex! 👋 You completed 3 tasks this week. 🎉 7-Day Streak!
{visual progress chart}
Next: Path Planning. Ready?"

Student: "How does path planning work?"

Agent: {checks Alex prefers visual learning}
"Let me show you visually: {diagram}
Since visual diagrams worked well for you before, I'm using them again."

Student: {struggles}

Agent: {analytics detects struggle}
"I notice this is tricky. Let's try smaller steps.
{adapts teaching based on data}
{routes to specialist}
{records what works for next time}"
```

**Key differences**:
- ✅ Personalized by name
- ✅ Shows concrete progress
- ✅ Celebrates achievements
- ✅ Adapts to learning style
- ✅ Detects and responds to struggles
- ✅ Learns and improves over time

---

## Summary

**Skills provide data, agents make decisions:**

```
Skills (What):           Agents (How):
- Student profile        → Personalize teaching
- Learning history       → Build on prior knowledge
- Current progress       → Show encouragement
- Struggle detection     → Adapt approach
- Achievements           → Celebrate milestones
- Code analysis          → Guide integration
- Visual diagrams        → Enhance explanations
```

**Integration Principles**:
1. **Proactive**: Use skills at session start, not when asked
2. **Personalize**: Adapt to student's style, pace, preferences
3. **Detect**: Monitor for struggles, adapt teaching
4. **Celebrate**: Check and show achievements
5. **Learn**: Record what works, use it next time
6. **Visual**: Use diagrams for visual learners
7. **Contextualize**: Use code analysis for specific guidance

**Result**: Agents transform from reactive, generic helpers into proactive, personalized, adaptive learning mentors.

---

**Version**: 1.0
**Date**: 2025-10-19
**Status**: Production Ready

*Complete guide to agent-skills integration for the Claude Code learning system*
