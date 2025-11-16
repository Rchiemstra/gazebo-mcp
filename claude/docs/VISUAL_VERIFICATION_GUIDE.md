# Visual Verification Guide

Comprehensive guide for using visual verification in Claude Code learning workflows.

---

## Overview

Visual verification uses screenshots, diagrams, and interactive demonstrations to verify student understanding and provide feedback. This is especially valuable for:
- Robotics visualizations (sensor data, navigation paths)
- UI/UX implementations
- Data visualizations
- System architecture diagrams
- Hardware setups

---

## Core Capabilities

### 1. Screenshot Verification

Claude Code can read and analyze screenshots to verify:
- ✅ UI implementations match requirements
- ✅ Robot visualizations show correct behavior
- ✅ Plots and graphs display expected data
- ✅ Terminal output matches expected results
- ✅ Hardware connections are correct

### 2. Diagram Analysis

Claude Code can read and interpret:
- Architecture diagrams (Mermaid, PlantUML, images)
- System flow diagrams
- Data flow diagrams
- State machines
- Class diagrams
- Sequence diagrams

### 3. Interactive Verification

Claude Code can guide students through:
- Step-by-step visual checks
- Progressive disclosure of solutions
- Comparison of expected vs actual results
- Debugging visual discrepancies

---

## Pattern 1: Screenshot Verification Workflow

### Basic Pattern

```python
# Student: "My robot visualization isn't working"
# → Student provides screenshot

# Claude Code reads the screenshot
from skills.verification import validate_output

# Analyze screenshot content
# Claude Code can see:
# - Terminal output in screenshot
# - GUI elements and layout
# - Visualization plots
# - Error messages
# - Console logs

# Provide targeted feedback
"I can see your visualization. The issue is..."
```

### Advanced Pattern with Comparison

```python
# 1. Student submits their screenshot
# 2. Claude Code compares against reference

# Verbal comparison (Claude Code describes):
"Comparing your output to expected:
✅ Correct: Path planning shows waypoints
✅ Correct: Robot position updates
❌ Issue: Obstacle detection not visualized
❌ Issue: Grid scale is incorrect (should be 10m, shows 1m)"

# Guide fix:
"Let's fix the grid scale. Check your visualization code around..."
```

---

## Pattern 2: Terminal Output Verification

### Verify Command Output

```python
from skills.verification import validate_output

# Student runs command and shares screenshot
# Claude Code reads terminal output from screenshot

# Example: ROS2 node list verification
expected_nodes = [
    "/camera_node",
    "/lidar_node",
    "/navigation_node"
]

# Claude Code can read screenshot and verify
# Then provide feedback:

if all_nodes_present:
    "✅ All required nodes are running correctly"
else:
    "Missing nodes: /navigation_node. Let's check..."
```

### Verify Error Messages

```python
# Student shares error screenshot
# Claude Code reads and analyzes error

# Provide guidance:
"I can see the error: 'ModuleNotFoundError: No module named cv2'

This means OpenCV isn't installed. Fix:
```bash
pip install opencv-python
```

After installing, run your code again and share the result."
```

---

## Pattern 3: Robot Visualization Verification

### Verify ROS2 RViz Visualization

```markdown
## Student Verification Checklist

Share a screenshot of your RViz window showing:
1. Robot model loaded and visible
2. TF tree showing all transforms
3. LaserScan data displaying
4. Map visualization (if mapping)
5. Path planning visualization (if navigating)

### What Claude Code Checks:
- ✅ Robot model appears correctly
- ✅ Sensor data is being received
- ✅ Transforms are correct (no red errors)
- ✅ Coordinate frames are properly aligned
- ✅ Visualization colors match expected topics
```

### Example Verification

```python
# Student shares RViz screenshot

# Claude Code analysis:
"Looking at your RViz visualization:

✅ Correct:
- Robot model is loaded
- Laser scan data is displaying
- TF frames are correct

❌ Issues:
- Map is not showing → Check if map_server node is running
- Path is red (should be green) → Check navigation topic
- Robot appears rotated 90° → Check your URDF base_link frame

Let's fix the map issue first..."
```

---

## Pattern 4: Data Visualization Verification

### Matplotlib/Seaborn Plots

```python
from skills.verification import validate_output
# Can't directly validate plot pixels, but can verify:
# - Data values in terminal
# - Plot generation code
# - Screenshot analysis

# Student shares plot screenshot

# Claude Code provides feedback:
"Looking at your plot:

✅ Correct:
- Data range is correct (0-100)
- X-axis labels are present
- Title is descriptive

❌ Issues:
- Y-axis should be 'Velocity (m/s)' not 'Speed'
- Missing grid lines (add plt.grid(True))
- Legend is outside plot area

Update your code..."
```

---

## Pattern 5: Hardware Setup Verification

### Verify Physical Connections

```markdown
## Hardware Verification Checklist

Share photos of:
1. Breadboard connections
2. Sensor wiring
3. Power connections
4. Pin assignments

### Claude Code Reviews:
- ✅ Correct pin connections
- ⚠️ Potential short circuits
- ⚠️ Reversed polarity
- ✅ Proper ground connections
- ⚠️ Missing pull-up resistors
```

### Example Check

```python
# Student shares breadboard photo

# Claude Code analysis:
"Checking your wiring:

✅ Correct:
- VCC connected to 3.3V
- GND properly connected
- SDA connected to GPIO 2

⚠️ Issues:
- SCL appears connected to GPIO 4 (should be GPIO 3)
- Missing pull-up resistors on SDA/SCL lines
- Power LED not connected (optional but helpful)

Let's fix the SCL connection first..."
```

---

## Pattern 6: Interactive Verification Session

### Step-by-Step Visual Verification

```markdown
## Progressive Verification

### Step 1: Basic Setup
Student: Share screenshot of your project structure
Claude Code: ✅ Verified - correct files present

### Step 2: Initial Run
Student: Share screenshot of first run output
Claude Code: ❌ Error detected - guide fix

### Step 3: After Fix
Student: Share updated screenshot
Claude Code: ✅ Error fixed, move to next step

### Step 4: Feature Test
Student: Share screenshot of feature working
Claude Code: ✅ Feature working correctly - explain why
```

---

## Pattern 7: Diagram-Based Learning

### Architecture Verification

```python
# Student creates architecture diagram (Mermaid, draw.io, etc.)
# Shares screenshot or code

# Claude Code reviews:
"Looking at your architecture:

✅ Strengths:
- Clear component separation
- Data flow is logical
- Proper layering (UI → Logic → Data)

💡 Suggestions:
- Add error handling path
- Show retry mechanism
- Include cache layer
- Specify protocols (HTTP/gRPC/etc.)

Let's enhance it with error handling..."
```

### State Machine Verification

```python
# Student creates state machine diagram
# Claude Code verifies:

"Reviewing your state machine:

✅ Correct:
- All states are reachable
- Transitions are labeled
- Initial state is marked

❌ Issues:
- Missing 'Error' state
- No transition from 'Processing' to 'Error'
- 'Done' state should transition back to 'Idle'

Add error handling states..."
```

---

## Pattern 8: Compare Expected vs Actual

### Visual Comparison Template

```markdown
## Expected vs Actual Comparison

### Expected Output:
```
[Describe expected visualization]
- Robot at position (0, 0)
- Facing 0° (north)
- Green path to goal
- Obstacles in red
```

### Your Output:
[Student shares screenshot]

### Comparison:
✅ Match: Robot position
✅ Match: Obstacle colors
❌ Mismatch: Robot facing 90° instead of 0°
❌ Mismatch: No path visualization

### Fix:
The orientation issue suggests...
```

---

## Best Practices

### For Students

1. **Provide Clear Screenshots**
   - Full window capture (not cropped)
   - Readable text (no blur)
   - Include relevant context (terminal, GUI, etc.)
   - Multiple angles for hardware

2. **Include Context**
   - What were you trying to do?
   - What did you expect to see?
   - What actually happened?
   - Screenshot of the result

3. **Progressive Disclosure**
   - Share initial attempt first
   - Get feedback
   - Implement fix
   - Share updated screenshot
   - Iterate

4. **Annotate If Needed**
   - Circle problem areas
   - Add arrows to important parts
   - Label components
   - Highlight error messages

### For Teaching Agents

1. **Analyze Systematically**
   - What's correct? (positive feedback first)
   - What's incorrect?
   - What's missing?
   - What's unexpected?

2. **Provide Specific Feedback**
   - ✅ "The laser scan shows 360 points - correct"
   - ❌ NOT "Looks wrong"
   - ✅ "Robot orientation is 90° rotated - check URDF base_link"
   - ❌ NOT "Check your code"

3. **Guide, Don't Solve**
   - Point out the issue location
   - Ask guiding questions
   - Provide hints, not solutions
   - Verify understanding

4. **Use Visual References**
   - Describe what SHOULD appear
   - Compare to what DOES appear
   - Explain the difference
   - Guide to fix

---

## Integration with Verification Skill

### Combine Code + Visual Verification

```python
from skills.verification import validate_code, validate_output

# 1. Validate student's code
code_result = validate_code(student_code)

# 2. Student runs code and shares screenshot
# 3. Claude Code analyzes screenshot

# 4. Combine feedback
if code_result.success and screenshot_shows_correct_output:
    "✅ Code is valid AND output is correct - great work!"
elif code_result.success and not screenshot_shows_correct_output:
    "Code is valid but output is incorrect. Let's debug the logic..."
elif not code_result.success:
    "Let's fix the code errors first, then we'll check the output..."
```

---

## Advanced Patterns

### Pattern: Multi-Stage Visual Verification

```markdown
## Robot Navigation Verification

### Stage 1: Sensor Verification
Student: Share RViz screenshot showing sensor data
Claude Code: Verify sensors are working

### Stage 2: Localization Verification
Student: Share screenshot of robot localization
Claude Code: Verify robot knows its position

### Stage 3: Path Planning Verification
Student: Share screenshot of planned path
Claude Code: Verify path makes sense

### Stage 4: Execution Verification
Student: Share video/screenshots of robot moving
Claude Code: Verify execution matches plan

### Stage 5: Goal Achievement
Student: Share final position screenshot
Claude Code: Verify goal was reached correctly
```

### Pattern: Debug via Visualization

```python
# Student: "My robot isn't reaching the goal"
# Claude Code guides visual debugging

"""
Let's debug this step by step with visualizations:

1. First, share screenshot of RViz showing:
   - Current robot position
   - Goal position
   - Planned path

[Student shares]

I see the issue - your path goes through an obstacle.

2. Now share screenshot showing:
   - Obstacle layer in costmap
   - Inflation radius

[Student shares]

The inflation radius is too small. Let's fix it.

3. After updating, share screenshot showing:
   - New path that avoids obstacles

[Student shares]

✅ Perfect! Now the path is valid. Try running it.
"""
```

---

## Common Verification Scenarios

### 1. ROS2 Robot Visualization
- ✅ All TF frames present
- ✅ Sensor data displaying
- ✅ Robot model correct
- ✅ Map loaded
- ✅ Path planning active

### 2. Data Science Plots
- ✅ Correct axis labels
- ✅ Data range accurate
- ✅ Legend present
- ✅ Title descriptive
- ✅ Grid appropriate

### 3. Web UI
- ✅ Layout matches mockup
- ✅ Colors correct
- ✅ Responsive design
- ✅ Interactive elements work
- ✅ No console errors

### 4. Hardware Setup
- ✅ Wiring matches schematic
- ✅ Polarity correct
- ✅ Connections secure
- ✅ LEDs indicate power
- ✅ No shorts detected

### 5. Terminal Output
- ✅ Expected messages appear
- ✅ No error messages
- ✅ Correct values displayed
- ✅ Timing appropriate
- ✅ Format matches spec

---

## Example: Complete Visual Verification Workflow

```markdown
## Student: "Help me verify my navigation system"

### Verification Checklist

#### 1. Environment Setup
□ Share screenshot of RViz with map loaded
   Claude Code: Verify map is correct

#### 2. Sensor Verification
□ Share screenshot showing laser scan data
   Claude Code: Verify sensor data is clean

#### 3. Localization Check
□ Share screenshot of robot position estimate
   Claude Code: Verify AMCL convergence

#### 4. Goal Setting
□ Share screenshot after setting nav goal
   Claude Code: Verify goal is reachable

#### 5. Path Planning
□ Share screenshot showing planned path
   Claude Code: Verify path avoids obstacles

#### 6. Execution
□ Share video or series of screenshots
   Claude Code: Verify smooth execution

#### 7. Goal Achievement
□ Share screenshot of robot at goal
   Claude Code: Verify position accuracy

### Feedback at Each Stage

Stage 1: ✅ Map loaded correctly
Stage 2: ⚠️ Laser scan has noise - add filter
Stage 3: ❌ AMCL not converging - increase particles
... etc ...
```

---

## Tools and Technologies

### Screenshot Tools
- **Linux**: `gnome-screenshot`, `spectacle`, `flameshot`
- **macOS**: Cmd+Shift+4
- **Windows**: Snipping Tool, Win+Shift+S

### Diagram Tools
- **Mermaid**: Text-based diagrams (in markdown)
- **PlantUML**: UML diagrams from text
- **draw.io**: Visual diagram editor
- **Excalidraw**: Hand-drawn style diagrams

### Recording Tools
- **asciinema**: Terminal session recording
- **Peek**: Simple screen recorder (Linux)
- **OBS**: Full-featured screen recording

---

## Summary

Visual verification is powerful for:
- ✅ Verifying implementations that are inherently visual
- ✅ Debugging issues that appear in output
- ✅ Teaching concepts through visualization
- ✅ Providing concrete, specific feedback
- ✅ Building student confidence through visible success

**Key Principles:**
1. Visual evidence builds confidence
2. Screenshots enable specific feedback
3. Progressive verification builds understanding
4. Combine code + visual verification
5. Guide students through visual debugging

**Remember:** Visual verification complements, but doesn't replace, code verification and testing. Use all three together for comprehensive learning!

---

*Last Updated: 2025-11-09*
