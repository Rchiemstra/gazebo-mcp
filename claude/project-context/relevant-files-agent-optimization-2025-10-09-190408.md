# Agent Optimization Project - Codebase Analysis

**Generated**: 2025-10-09 19:04:08
**Project Goal**: Optimize all 14 teaching specialist agents to increase their effectiveness
**Files Analyzed**: 14 agent definition files

---

## 📊 Executive Summary

This analysis examines the complete teaching agent ecosystem consisting of 14 specialized agents designed to provide educational guidance for robotics development with ROS2, Python, C++, and the JETANK platform.

### Agent Inventory
- **14 total agents** across multiple domains
- **1 master coordinator** (learning-coordinator)
- **3 meta-agents** (plan-generation-mentor, project-plan-orchestrator, file-search-agent)
- **4 core technical specialists** (ROS2, Python, C++, architecture)
- **3 domain specialists** (robotics vision, hardware, debugging)
- **3 development tool agents** (git, testing, documentation)

### Key Strengths Identified
1. **Consistent teaching-first philosophy**: All agents strictly avoid providing complete solutions
2. **Strong safety protocols**: Hardware agents emphasize safety-first approach
3. **Progressive learning structure**: Agents use phases and checkpoints
4. **Specialist coordination**: Clear pathways for agent collaboration
5. **Student-centric design**: Agents check understanding before proceeding

### Areas for Optimization
1. **Inconsistent verification approaches**: Some agents have detailed checkpoints, others don't
2. **Varying question-asking techniques**: Quality and depth of guiding questions differs
3. **Uneven use of examples**: Some agents provide rich analogies, others are sparse
4. **Safety protocol coverage**: Only hardware-related agents emphasize safety
5. **Metacognitive guidance**: Limited explicit teaching of "learning how to learn"
6. **Pattern documentation**: Inconsistent reference materials for common patterns

---

## 🗂️ Agent Files by Category

### Master Coordinator

#### 1. `/home/koen/workspaces/claude_code/agents/learning-coordinator.md`
- **Type**: Master coordination agent
- **Purpose**: Orchestrates learning experiences by delegating to specialized sub-agents
- **Strengths**:
  - Comprehensive reflection-first workflow using `/reflection` command
  - Detailed response framework with understanding checks
  - Strong specialist coordination examples
  - Student learning profile integration
  - Progressive challenge system
- **Teaching Techniques**:
  - Understanding checks before guidance
  - Concept explanation with "why it matters"
  - Step-by-step approaches with student implementation
  - Learning verification checkpoints
  - Questions to guide thinking
- **Patterns Worth Spreading**:
  - Reflection-first approach (unique to this agent)
  - Teaching response framework structure
  - Detailed specialist coordination examples
  - Student learning profile system
  - Progressive challenge levels (Level 1-4)
- **Improvement Opportunities**:
  - Could provide more explicit metacognitive guidance
  - Response templates could be more concise for quick queries

---

### Planning & Orchestration Agents

#### 2. `/home/koen/workspaces/claude_code/agents/plan-generation-mentor.md`
- **Type**: Educational planning specialist
- **Purpose**: Creates detailed, educational implementation plans with progressive learning phases
- **Strengths**:
  - Context-aware planning (checks for relevant-files markdown)
  - Strong learning-focused plan structure
  - Clear phase delineation: Understand → Design → Implement → Refine → Reflect
  - Learning checkpoints integrated into plan phases
  - Learning journal structure for reflection
- **Teaching Techniques**:
  - Research tasks before implementation
  - Decision points where students make choices
  - Understanding checkpoints between phases
  - Specialist mapping for each phase
  - Learning milestone verification
- **Patterns Worth Spreading**:
  - Context-aware planning workflow (Step 0: check for codebase context)
  - Learning journal integration
  - Clear entry/learning/exit checkpoints per phase
  - Explicit decision points marked with guidance questions
- **Improvement Opportunities**:
  - Could include more examples of progressive difficulty
  - Would benefit from common anti-pattern warnings

#### 3. `/home/koen/workspaces/claude_code/agents/project-plan-orchestrator.md`
- **Type**: Sequential workflow coordinator
- **Purpose**: Orchestrates file-search-agent → plan-generation-mentor workflow
- **Strengths**:
  - Clear sequential workflow management
  - State tracking across agent invocations
  - Error handling with alternatives
  - Rich context passing between agents
- **Teaching Techniques**:
  - Workflow explanation to user
  - Progress updates during orchestration
  - Clear next steps after completion
- **Patterns Worth Spreading**:
  - Sequential agent coordination protocol
  - Verification at each step
  - Rich context sharing between agents
- **Improvement Opportunities**:
  - Could provide more educational value beyond coordination
  - Limited direct teaching role

#### 4. `/home/koen/workspaces/claude_code/agents/file-search-agent.md`
- **Type**: Codebase analysis specialist
- **Purpose**: Searches and documents relevant files for project planning
- **Strengths**:
  - Multi-strategy search approach
  - Comprehensive file categorization
  - Relationship mapping between files
  - Integration point identification
- **Teaching Techniques**:
  - Systematic search methodology
  - Organized information presentation
  - Pattern recognition in codebases
- **Patterns Worth Spreading**:
  - Multi-strategy search approach
  - Structured markdown output template
  - Relationship mapping
- **Improvement Opportunities**:
  - More explicitly educational (currently utility-focused)
  - Could teach search/analysis methodology

---

### Core Technical Learning Agents

#### 5. `/home/koen/workspaces/claude_code/agents/ros2-learning-mentor.md`
- **Type**: ROS2 robotics learning specialist
- **Purpose**: Teaches ROS2 concepts, node architecture, message types
- **Strengths**:
  - **Safety-first protocol** with comprehensive hardware safety checklist
  - Clear teaching rules prominently displayed
  - Concept → Structure → Questions progression
  - Progressive learning steps with clear phases
- **Teaching Techniques**:
  - "What it is / Why it matters / How it works" pattern
  - Guided discovery questions
  - 6-step learning path (understand → explore → design → implement → test → enhance)
  - Safety checklists before hardware operations
- **Patterns Worth Spreading**:
  - Safety-first protocol structure
  - "What/Why/How" concept explanation pattern
  - 6-step progressive learning path
  - Pre-hardware safety checklist
- **Improvement Opportunities**:
  - Could include more ROS2-specific debugging guidance
  - Would benefit from common ROS2 anti-patterns section

#### 6. `/home/koen/workspaces/claude_code/agents/python-best-practices.md`
- **Type**: Python coding standards specialist
- **Purpose**: Teaches Pythonic thinking and best practices
- **Strengths**:
  - Clear improvement teaching framework
  - Performance thinking questions
  - Code review teaching approach
- **Teaching Techniques**:
  - "What I notice" observation pattern
  - Pythonic thinking questions
  - Pattern examples with "what do you think goes here?"
  - Profiling exercises
- **Patterns Worth Spreading**:
  - "What I notice" code review pattern
  - Performance profiling exercise structure
- **Improvement Opportunities**:
  - Somewhat brief compared to other agents
  - Could use more detailed examples of teaching patterns
  - Would benefit from progressive skill levels
  - Missing analogies that make Pythonic concepts clearer

#### 7. `/home/koen/workspaces/claude_code/agents/cpp-best-practices.md`
- **Type**: C++ coding standards specialist
- **Purpose**: Teaches modern C++ best practices with robotics focus
- **Strengths**:
  - Modern C++ focus (C++14/17/20)
  - Robotics-specific considerations (real-time, embedded)
  - Real-time programming patterns section
- **Teaching Techniques**:
  - "What/Why/How/When" concept pattern
  - Design questions for each pattern
  - Real-time analysis exercises
  - Safety and performance focus
- **Patterns Worth Spreading**:
  - Real-time programming constraints section
  - "What/Why/How/When to use" pattern
  - Memory safety analysis framework
- **Improvement Opportunities**:
  - Could expand on teaching examples
  - Would benefit from more robotics-specific C++ examples
  - Could include common beginner mistakes section

#### 8. `/home/koen/workspaces/claude_code/agents/code-architecture-mentor.md`
- **Type**: Software design patterns specialist
- **Purpose**: Teaches design thinking and architectural patterns
- **Strengths**:
  - **Exceptional pattern library**: 10 detailed patterns with teaching approaches
  - Progressive quality goals (Level 1-4)
  - Pattern selection guide for common robotics problems
  - Pattern comparison teaching (Strategy vs State, Decorator vs Inheritance)
  - Anti-patterns section
- **Teaching Techniques**:
  - "Teaching Questions" before pattern introduction
  - "When to Teach This" guidance
  - Trade-offs explicitly stated
  - Pattern selection process (4 steps)
  - Robotics-specific applications
- **Patterns Worth Spreading**:
  - **Teaching reference library structure**: Detailed pattern teaching guides
  - Progressive quality levels with questions
  - Pattern selection guide for domain-specific problems
  - Side-by-side pattern comparison
  - Anti-pattern recognition teaching
- **Improvement Opportunities**:
  - Very comprehensive; could be overwhelming for beginners
  - Could include "quick reference" version for experienced students

---

### Domain Specialists

#### 9. `/home/koen/workspaces/claude_code/agents/robotics-vision-navigator.md`
- **Type**: Computer vision and navigation specialist
- **Purpose**: Teaches SLAM, object detection, path planning
- **Strengths**:
  - **Very comprehensive reference implementations** (for teacher use)
  - Clear separation: teaching vs reference material
  - Progressive learning phases (4 weeks structured)
  - Strong theoretical foundation explanations
- **Teaching Techniques**:
  - "What to Teach" / "Key Concepts" / "Teaching Questions" structure
  - Example patterns with "how would you..." questions
  - Learning exercises with goals
  - Phase-based skill progression
- **Patterns Worth Spreading**:
  - Reference implementation clearly marked "For Teacher Only"
  - Learning progression by weeks
  - Example pattern with fill-in-the-blank style
- **Improvement Opportunities**:
  - Reference implementations are extensive; might tempt copy-paste
  - Could use more analogies for complex vision concepts
  - Would benefit from visual diagram descriptions

#### 10. `/home/koen/workspaces/claude_code/agents/jetank-hardware-specialist.md`
- **Type**: Hardware integration specialist
- **Purpose**: Teaches JETANK platform hardware integration safely
- **Strengths**:
  - **Excellent safety-first protocol**: Most comprehensive of all agents
  - Detailed hardware specifications and pin mappings
  - Hardware troubleshooting guide
  - Calibration procedures
  - Hardware testing framework
  - Reference implementations clearly marked for teacher
- **Teaching Techniques**:
  - Safety discussion ALWAYS first
  - "What to Teach" / "Key Concepts" / "Safety Discussion" / "Teaching Questions"
  - Learning exercises with incremental testing
  - Hardware-specific troubleshooting commands
- **Patterns Worth Spreading**:
  - Safety-first protocol (most detailed)
  - Hardware safety checklist
  - "Start at 10% power" incremental testing approach
  - Troubleshooting guide with actual commands
  - Calibration procedures as learning exercises
- **Improvement Opportunities**:
  - Could include more common beginner hardware mistakes
  - Would benefit from safety incident scenarios

#### 11. `/home/koen/workspaces/claude_code/agents/debugging-detective.md`
- **Type**: Debugging methodology specialist
- **Purpose**: Teaches systematic debugging approaches
- **Strengths**:
  - Scientific method for debugging
  - Robotics-specific investigation order
  - Progressive debugging skills by week
  - Error message analysis framework
- **Teaching Techniques**:
  - 5-step scientific method (observe → hypothesize → predict → test → analyze)
  - Isolation techniques teaching
  - "Your debugging mission" action items
  - Debugging mindset cultivation
- **Patterns Worth Spreading**:
  - Scientific method framework for debugging
  - Robotics-specific investigation checklist
  - Progressive skills by week
  - Debugging mindset principles
- **Improvement Opportunities**:
  - Could include more specific ROS2 debugging examples
  - Would benefit from common bug patterns library
  - Could use debugging decision tree

---

### Development Tool Specialists

#### 12. `/home/koen/workspaces/claude_code/agents/testing-specialist.md`
- **Type**: Testing methodology specialist
- **Purpose**: Guides students in writing tests and TDD
- **Strengths**:
  - Clear testing philosophy
  - Testing pyramid structure (70/20/10)
  - Robotics-specific testing strategies
  - Test as executable specifications concept
- **Teaching Techniques**:
  - "What to test and why" guidance
  - Test structure examples to adapt
  - Testing strategy framework
  - Behavior vs implementation focus
- **Patterns Worth Spreading**:
  - Testing pyramid with percentages
  - Tests as specifications concept
  - Robotics-specific testing categories
- **Improvement Opportunities**:
  - Relatively brief compared to complexity of topic
  - Could use more detailed TDD teaching progression
  - Would benefit from test design exercises
  - Missing mock/stub teaching approach

#### 13. `/home/koen/workspaces/claude_code/agents/git-workflow-expert.md`
- **Type**: Git and version control specialist
- **Purpose**: Teaches Git workflows and collaboration
- **Strengths**:
  - Git mental models emphasis
  - Workflow expertise across strategies
  - Commit best practices
- **Teaching Techniques**:
  - "Why" before "how" approach
  - Mental model teaching
  - Troubleshooting guidance
- **Patterns Worth Spreading**:
  - Mental model focus
  - Conventional commit format
- **Improvement Opportunities**:
  - **Most underdeveloped agent**: Very brief compared to others
  - Lacks detailed teaching framework
  - No progressive learning structure
  - Could use interactive Git exercises
  - Missing collaboration scenario examples
  - Would benefit from recovery scenarios teaching

#### 14. `/home/koen/workspaces/claude_code/agents/documentation-generator.md`
- **Type**: Technical writing specialist
- **Purpose**: Guides documentation creation
- **Strengths**:
  - Documentation philosophy
  - Multiple documentation types covered
  - Clear format examples
- **Teaching Techniques**:
  - Template-based guidance
  - "What to document and why"
  - Documentation as communication
- **Patterns Worth Spreading**:
  - Documentation types taxonomy
  - "Documentation is code for humans"
- **Improvement Opportunities**:
  - **Second most underdeveloped**: Very brief
  - Lacks teaching progression
  - No examples of teaching someone to write docs
  - Could use "before/after" documentation examples
  - Missing audience-awareness teaching
  - Would benefit from documentation review framework

---

## 🔍 Cross-Agent Pattern Analysis

### Common Strengths Across All Agents

1. **Universal Teaching Rules Section**
   - Every agent has clear "NEVER/ALWAYS" rules
   - Prominently placed at top of agent definition
   - Consistently prohibits complete solutions

2. **Concept-First Approach**
   - All agents emphasize understanding before implementation
   - Theory precedes practice

3. **Question-Based Guidance**
   - Every agent uses questions to guide thinking
   - Varies in quality and depth

4. **Small Code Snippets**
   - All agents limit examples to 2-5 lines
   - Used as patterns, not solutions

### Pattern Variations Worth Standardizing

#### 1. Concept Explanation Patterns

**Best Pattern** (from ROS2, C++, Hardware agents):
```
**What it is**: [Clear explanation]
**Why it matters**: [Relevance to domain]
**How it works**: [Conceptual breakdown]
**When to use it**: [Specific scenarios]
**Your thinking exercise**: [Questions to explore]
```

**Variations Found**:
- Python: "Pythonic thinking questions"
- Debugging: "What this tells us / Investigation Questions"
- Architecture: Very detailed pattern library

**Recommendation**: Standardize on the 5-part "What/Why/How/When/Exercise" pattern

#### 2. Safety Protocols

**Best Implementation** (Hardware, ROS2):
```
## 🛡️ SAFETY-FIRST TEACHING PROTOCOL

### Before ANY Hardware Code/Guidance:
[Checklist of safety considerations]

### Safety Teaching Requirements:
1. Environment Check
2. Emergency Procedures
3. Incremental Testing
4. Damage Prevention
5. Learning Mindset
```

**Currently Limited To**: Hardware and ROS2 agents

**Recommendation**: Extend safety thinking to all domains
- Testing: Test safety (don't delete production data)
- Git: Repository safety (backup before complex operations)
- Python/C++: Code safety (input validation, resource cleanup)

#### 3. Progressive Learning Structures

**Best Pattern** (ROS2, Architecture, Vision):
```
### Level 1: [Basic skill]
### Level 2: [Intermediate skill]
### Level 3: [Advanced skill]
### Level 4: [Expert skill]

OR

### Week 1-2: [Foundation]
### Week 3-4: [Building]
### Week 5-6: [Integration]
### Week 7-8: [Mastery]
```

**Missing From**: Python, Testing, Git, Documentation

**Recommendation**: All agents should include progressive skill levels

#### 4. Understanding Verification

**Best Pattern** (Plan-generation, Learning-coordinator):
```
### Understanding Checkpoint ✋
Before moving to [next phase], you should be able to:
1. Explain [concept] in your own words
2. Demonstrate [skill]
3. Identify [edge cases/trade-offs]

**Check with learning-coordinator when ready!**
```

**Inconsistently Applied**: Some agents have detailed checkpoints, others don't

**Recommendation**: Standardize checkpoint format and frequency

#### 5. Specialist Coordination

**Best Pattern** (Learning-coordinator):
```
**[specialist-name]**: [What they help with]
  - Ask about: [Appropriate questions]
  - Don't ask for: [Inappropriate requests]
```

**Well-implemented**: Learning-coordinator, Plan-generation
**Could Improve**: Individual specialists don't always clearly state when to hand off

**Recommendation**: Each specialist should include "When to consult other specialists" section

---

## 🎯 Teaching Technique Analysis

### Question-Asking Quality

#### Excellent Examples:

**Architecture Mentor**:
```
Q: How many parameters does your constructor have?
Q: Which parameters are required vs optional?
Q: How readable is the object creation code?
```
- Specific, actionable questions
- Guides toward pattern discovery
- Builds design thinking skills

**Debugging Detective**:
```
Q: What exactly are you trying to achieve?
Q: What actually happens?
Q: When does this occur? (always/sometimes/specific conditions?)
```
- Systematic information gathering
- Scientific method application
- Reproducibility focus

#### Areas for Improvement:

**Python Best Practices**:
```
Q: Could you use a list comprehension here?
Q: Would a context manager make this cleaner?
```
- Good but could be more scaffolded
- Could provide more "thinking process" questions

**Git Workflow Expert**:
- Very few example questions
- Could use scenario-based questions
- Missing mental model building questions

### Analogy and Example Usage

#### Strong Analogy Examples:

**ROS2 Mentor**:
- "Think of it like tuning a musical instrument" (calibration)
- Clear real-world connections

**Code Architecture**:
- Extensive pattern examples with trade-offs
- Before/after comparisons (Decorator vs Inheritance)

#### Missing Analogies:

**Python, C++, Testing, Git, Documentation**:
- Minimal use of analogies
- Could benefit from domain-specific metaphors
- Would help with complex concept understanding

### Examples and Patterns Quality

#### Best Practice (Architecture):
```
**Example Situation**: "I have 3 path planning algorithms - how to switch?"
**Teaching Approach**: [Guided questions]
**Pattern Structure**: [Skeleton with questions]
**When to use**: [Specific criteria]
**Trade-offs**: [Pros and cons explicitly listed]
```

#### Could Improve:
- **Python**: Pattern examples are brief
- **Testing**: Limited test design examples
- **Git**: Minimal workflow examples

---

## 💡 Key Insights and Recommendations

### 1. Consistency Opportunities

**Finding**: Agent quality varies significantly
- **Most Developed**: learning-coordinator, code-architecture-mentor, robotics-vision-navigator, jetank-hardware-specialist
- **Least Developed**: git-workflow-expert, documentation-generator, testing-specialist

**Recommendation**: Bring underdeveloped agents up to the standard of top agents

### 2. Safety Protocol Expansion

**Finding**: Excellent safety protocols limited to hardware domains
**Recommendation**: Create "safety thinking" for all domains:
- **Testing**: Data safety, test isolation
- **Git**: Repository safety, backup practices
- **Python/C++**: Resource safety, error handling
- **Documentation**: Information safety, accuracy verification

### 3. Progressive Learning Standardization

**Finding**: Some agents have clear skill progression, others don't
**Recommendation**: All agents should include:
- Beginner → Intermediate → Advanced → Expert levels
- Clear skill markers for each level
- Understanding checkpoints between levels

### 4. Metacognitive Teaching Enhancement

**Finding**: Limited explicit "learning how to learn" guidance
**Recommendation**: Add metacognitive elements:
- How to approach learning this topic
- How to know when you understand
- How to self-assess progress
- How to debug your own understanding

### 5. Question Quality Standardization

**Finding**: Question quality varies widely
**Recommendation**: Create question taxonomy:
- **Understanding questions**: Check comprehension
- **Application questions**: Apply to scenarios
- **Analysis questions**: Break down problems
- **Synthesis questions**: Combine concepts
- **Evaluation questions**: Assess trade-offs

### 6. Collaboration Clarity

**Finding**: Some agents don't clearly state when to hand off
**Recommendation**: Each specialist should include:
- "I can help you with..." section
- "Consult [other agent] for..." section
- "When to coordinate multiple specialists" guidance

### 7. Anti-Pattern Libraries

**Finding**: Only architecture agent has anti-patterns section
**Recommendation**: All agents should document common mistakes:
- What beginners typically try
- Why it doesn't work
- How to recognize the mistake
- What to do instead

### 8. Reference Material Consistency

**Finding**: Some agents have extensive references (vision, hardware), others minimal
**Recommendation**: Standardize reference sections:
- Common patterns library
- Troubleshooting guide
- Quick reference / cheat sheet
- Further learning resources

---

## 🔗 Agent Relationships and Coordination

### Current Coordination Patterns

```
learning-coordinator (Master)
    ├─── plan-generation-mentor (Plans complex features)
    │    └─── Coordinates all specialists in phases
    ├─── ros2-learning-mentor
    │    └─── Hands off to: python/cpp, architecture, hardware, testing
    ├─── robotics-vision-navigator
    │    └─── Hands off to: ros2, architecture, python
    ├─── jetank-hardware-specialist
    │    └─── Hands off to: ros2, python, testing
    ├─── code-architecture-mentor
    │    └─── Works with all technical agents
    ├─── debugging-detective
    │    └─── Works with all agents when issues arise
    └─── [Other specialists]
```

### Coordination Gaps

1. **Unclear Handoff Points**: Some agents don't specify when to involve others
2. **Circular Dependencies**: Risk of agents referring back and forth
3. **Missing Coordination Protocols**: No standard "how to hand off" guidance

### Recommended Coordination Enhancements

1. **Explicit Handoff Triggers**:
   ```
   ## When to Consult Other Specialists

   Involve [specialist] when:
   - [Specific trigger 1]
   - [Specific trigger 2]

   Example handoff: "[specialist], help with [specific task]..."
   ```

2. **Coordination Matrix**: Document which agents commonly work together
3. **Escalation Paths**: When multiple specialists needed, who coordinates?

---

## 📋 Optimization Priority Matrix

### High Impact, High Effort
1. Standardize all agents to architecture-mentor quality level
2. Create comprehensive anti-pattern libraries for all domains
3. Develop metacognitive teaching framework across agents

### High Impact, Low Effort
1. Add safety protocols to all agents (adapt hardware model)
2. Standardize concept explanation pattern (What/Why/How/When/Exercise)
3. Add "When to consult other specialists" sections
4. Create understanding checkpoint templates

### Medium Impact, Low Effort
1. Improve question quality in underdeveloped agents
2. Add analogies to agents lacking them
3. Standardize progressive skill levels
4. Create quick reference sections

### Low Impact, High Effort
1. Complete rewrite of reference implementations
2. Create visual diagrams for all concepts

---

## 🎓 Best Practices to Propagate

### From Learning-Coordinator
- Reflection-first approach
- Student learning profile integration
- Progressive challenge system (Level 1-4)
- Detailed specialist coordination examples

### From Plan-Generation-Mentor
- Context-aware planning (checks for relevant files)
- Learning journal structure
- Clear checkpoints (entry/learning/exit)
- Decision point marking

### From Code-Architecture-Mentor
- Comprehensive pattern library with teaching notes
- Pattern selection guide for domain problems
- Pattern comparison teaching
- Anti-pattern recognition
- Trade-offs explicitly stated

### From ROS2/Hardware Specialists
- Safety-first protocol
- "What/Why/How" concept pattern
- Progressive learning by weeks
- Hardware-specific safety checklists

### From Debugging-Detective
- Scientific method framework
- Progressive skills by week
- Debugging mindset cultivation
- Systematic investigation order

---

## 🚀 Next Steps for Optimization

This analysis provides the foundation for creating a comprehensive optimization plan that will:

1. **Standardize** teaching approaches across all agents
2. **Enhance** underdeveloped agents to match top-tier quality
3. **Extend** best practices (safety, progression, checkpoints) universally
4. **Improve** question-asking and analogy use across the board
5. **Clarify** specialist coordination and handoff protocols
6. **Add** metacognitive and anti-pattern guidance

The learning plan will detail how to accomplish these optimizations systematically while maintaining the teaching-first philosophy that makes these agents effective.
