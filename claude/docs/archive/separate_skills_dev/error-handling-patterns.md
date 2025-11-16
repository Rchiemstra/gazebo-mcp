# Error Handling Patterns - Implementation Guide

Practical guide for implementing consistent error handling across all skills and agents.

**Created**: 2025-11-10
**Status**: Active
**Audience**: Skill/agent developers

---

## Table of Contents

1. [Error Handling Philosophy](#error-handling-philosophy)
2. [Standard Error Format](#standard-error-format)
3. [Exit Code Standards](#exit-code-standards)
4. [Error Message Templates](#error-message-templates)
5. [Implementation Patterns](#implementation-patterns)
6. [Testing Error Handling](#testing-error-handling)
7. [Quick Reference](#quick-reference)

---

## Error Handling Philosophy

### Core Principles

1. **Fail Fast, Fail Clearly**: Detect errors early and report them clearly
2. **Actionable Feedback**: Every error message should guide the user toward a solution
3. **Context is Key**: Include what, where, when, and why
4. **Consistent Format**: Use standard error message structure
5. **Progressive Recovery**: Try to recover gracefully where possible

### Error Hierarchy

```
FATAL    → Cannot continue, immediate shutdown required
  ↓
ERROR    → Operation failed, manual intervention needed
  ↓
WARNING  → Non-critical issue, operation continued
  ↓
INFO     → Normal operational message
  ↓
DEBUG    → Diagnostic information
```

---

## Standard Error Format

### Error Message Template

```
[COMPONENT] ERROR: <what went wrong>
  Context: <relevant state/values>
  Cause: <why it happened>
  Action: <what to do next>
```

### Examples

**Good Error Message**:
```
[ModbusClient] ERROR: Connection timeout after 3 attempts
  Context: host=192.168.1.100, port=502, timeout=5.0s
  Cause: Device not responding or network unreachable
  Action: Verify device power and network connectivity, then retry
```

**Bad Error Message**:
```
Error: Failed
```

### Components

**COMPONENT**: Identify the source
- Use skill/agent name, node name, or module name
- Examples: `[ROS Node]`, `[ModbusClient]`, `[BuildSystem]`

**What went wrong**: Brief description
- Be specific but concise
- Examples: "Connection timeout", "Invalid parameter", "File not found"

**Context**: Relevant state
- Include values that help debug
- Examples: IP addresses, parameter values, file paths

**Cause**: Why it happened
- Explain the root cause if known
- Examples: "Device not responding", "Parameter out of range"

**Action**: What to do next
- Provide specific next steps
- Examples: "Check network connectivity", "Verify parameter range"

---

## Exit Code Standards

### Standard Exit Codes

All skills and agents **must** include these exit codes:

```markdown
## Exit Codes

- **0**: Success (operation completed successfully)
- **1**: Warnings (operation succeeded with non-critical issues)
- **2**: Failure (operation failed, manual intervention needed)
- **3**: Cannot execute (prerequisites not met, tool unavailable)
```

### Exit Code Usage

**Exit Code 0 - Success**:
- Operation completed as expected
- All outputs generated
- No errors or warnings

**Exit Code 1 - Warnings**:
- Operation succeeded but with caveats
- Non-critical issues detected
- Examples: Deprecated API used, performance concern

**Exit Code 2 - Failure**:
- Operation could not complete
- User intervention required
- Examples: Build failed, tests failed, connection error

**Exit Code 3 - Cannot Execute**:
- Prerequisites not met
- Tool or dependency missing
- Examples: ROS not sourced, required file missing

### Implementation

**Python**:
```python
import sys

# Success
sys.exit(0)

# Warning
rospy.logwarn("Operation succeeded with warnings")
sys.exit(1)

# Failure
rospy.logerr("Operation failed: connection timeout")
sys.exit(2)

# Cannot execute
rospy.logfatal("ROS environment not sourced")
sys.exit(3)
```

**Bash**:
```bash
# Success
exit 0

# Warning
echo "WARNING: Operation succeeded with issues" >&2
exit 1

# Failure
echo "ERROR: Operation failed" >&2
exit 2

# Cannot execute
echo "FATAL: Prerequisites not met" >&2
exit 3
```

---

## Error Message Templates

### Validation Errors

```python
def validate_parameter(value, min_val, max_val, name):
    """Validate parameter with clear error message."""
    if value is None:
        raise ValueError(
            f"[Validator] ERROR: Parameter '{name}' is required\n"
            f"  Context: value=None\n"
            f"  Cause: Parameter not provided\n"
            f"  Action: Provide a value for '{name}'"
        )

    if not (min_val <= value <= max_val):
        raise ValueError(
            f"[Validator] ERROR: Parameter '{name}' out of range\n"
            f"  Context: value={value}, valid_range=[{min_val}, {max_val}]\n"
            f"  Cause: Value exceeds acceptable bounds\n"
            f"  Action: Set '{name}' between {min_val} and {max_val}"
        )
```

### Connection Errors

```python
def connect_with_retry(host, port, max_retries=3):
    """Connect with retries and clear error messages."""
    for attempt in range(max_retries):
        try:
            client = create_client(host, port)
            client.connect()
            rospy.loginfo(f"Connected to {host}:{port}")
            return client
        except ConnectionError as e:
            rospy.logwarn(
                f"[Connection] WARNING: Attempt {attempt + 1}/{max_retries} failed\n"
                f"  Context: host={host}, port={port}\n"
                f"  Cause: {str(e)}\n"
                f"  Action: Retrying in {2**attempt}s..."
            )
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    # All retries failed
    raise ConnectionError(
        f"[Connection] ERROR: Failed after {max_retries} attempts\n"
        f"  Context: host={host}, port={port}\n"
        f"  Cause: Device unreachable or network issue\n"
        f"  Action: 1) Verify device power\n"
        f"          2) Check network connectivity: ping {host}\n"
        f"          3) Verify port: nc -zv {host} {port}"
    )
```

### File Operation Errors

```python
def load_config_file(filename):
    """Load config with comprehensive error handling."""
    import os
    import yaml

    # Check file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"[ConfigLoader] ERROR: Configuration file not found\n"
            f"  Context: path={filename}\n"
            f"  Cause: File does not exist\n"
            f"  Action: 1) Check file path is correct\n"
            f"          2) Verify file was created\n"
            f"          3) Check current directory: {os.getcwd()}"
        )

    # Check readable
    if not os.access(filename, os.R_OK):
        raise PermissionError(
            f"[ConfigLoader] ERROR: Cannot read configuration file\n"
            f"  Context: path={filename}\n"
            f"  Cause: Insufficient permissions\n"
            f"  Action: chmod +r {filename}"
        )

    # Parse YAML
    try:
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        raise ValueError(
            f"[ConfigLoader] ERROR: Invalid YAML syntax\n"
            f"  Context: file={filename}, line={e.problem_mark.line if hasattr(e, 'problem_mark') else 'unknown'}\n"
            f"  Cause: {str(e)}\n"
            f"  Action: 1) Validate YAML syntax\n"
            f"          2) Check for tabs (use spaces only)\n"
            f"          3) Verify proper indentation"
        )
```

---

## Implementation Patterns

### Pattern 1: Input Validation

**Always validate inputs before processing**:

```python
def process_sensor_data(data):
    """Process sensor data with validation."""
    # Validate input
    if data is None:
        raise ValueError("[Processor] ERROR: Sensor data is None")

    if not isinstance(data, list):
        raise TypeError(
            f"[Processor] ERROR: Invalid data type\n"
            f"  Context: received={type(data).__name__}, expected=list\n"
            f"  Cause: Incorrect data type passed\n"
            f"  Action: Ensure sensor returns list of measurements"
        )

    if len(data) == 0:
        raise ValueError("[Processor] ERROR: Empty sensor data")

    # Process data
    return [process_point(p) for p in data]
```

### Pattern 2: Graceful Degradation

**Provide fallback when primary method fails**:

```python
class SensorInterface:
    """Sensor interface with graceful degradation."""

    def __init__(self):
        self.primary = PrimarySensor()
        self.backup = BackupSensor()
        self.using_backup = False

    def get_reading(self):
        """Get sensor reading with fallback."""
        # Try primary
        if not self.using_backup:
            try:
                return self.primary.read()
            except Exception as e:
                rospy.logwarn(
                    f"[SensorInterface] WARNING: Primary sensor failed\n"
                    f"  Context: error={str(e)}\n"
                    f"  Cause: Primary sensor not responding\n"
                    f"  Action: Switching to backup sensor"
                )
                self.using_backup = True

        # Use backup
        try:
            return self.backup.read()
        except Exception as e:
            raise RuntimeError(
                f"[SensorInterface] ERROR: Both sensors failed\n"
                f"  Context: primary_failed=True, backup_failed=True\n"
                f"  Cause: No sensors available\n"
                f"  Action: 1) Check sensor connections\n"
                f"          2) Restart sensor nodes\n"
                f"          3) Verify sensor power"
            )
```

### Pattern 3: Context Preservation

**Maintain context through error chain**:

```python
def high_level_operation():
    """High-level operation with context preservation."""
    try:
        result = mid_level_operation()
        return result
    except Exception as e:
        # Wrap with additional context
        raise RuntimeError(
            f"[HighLevel] ERROR: Operation failed\n"
            f"  Context: operation=high_level_operation\n"
            f"  Cause: {str(e)}\n"
            f"  Action: See nested error above for details"
        ) from e  # Preserve original exception

def mid_level_operation():
    """Mid-level operation."""
    try:
        return low_level_operation()
    except ValueError as e:
        raise RuntimeError(
            f"[MidLevel] ERROR: Validation failed\n"
            f"  Context: operation=mid_level_operation\n"
            f"  Cause: {str(e)}"
        ) from e
```

---

## Testing Error Handling

### Unit Tests for Error Conditions

```python
import pytest

def test_validates_input_not_none():
    """Test that None input raises clear error."""
    with pytest.raises(ValueError) as exc_info:
        process_sensor_data(None)

    error_msg = str(exc_info.value)
    assert "[Processor] ERROR" in error_msg
    assert "None" in error_msg

def test_validates_input_type():
    """Test that wrong type raises clear error."""
    with pytest.raises(TypeError) as exc_info:
        process_sensor_data("invalid")

    error_msg = str(exc_info.value)
    assert "Invalid data type" in error_msg
    assert "expected=list" in error_msg

def test_validates_empty_data():
    """Test that empty data raises error."""
    with pytest.raises(ValueError) as exc_info:
        process_sensor_data([])

    error_msg = str(exc_info.value)
    assert "Empty sensor data" in error_msg
```

### Integration Tests for Error Recovery

```python
def test_fallback_to_backup_sensor():
    """Test graceful degradation to backup sensor."""
    interface = SensorInterface()

    # Simulate primary failure
    interface.primary.fail()

    # Should still get reading from backup
    reading = interface.get_reading()
    assert reading is not None
    assert interface.using_backup is True
```

---

## Quick Reference

### Adding Error Handling to a Skill

**Checklist**:
- [ ] Add "## Exit Codes" section at end of file
- [ ] Validate all inputs with clear error messages
- [ ] Use standard error message format
- [ ] Include context in error messages
- [ ] Provide actionable guidance
- [ ] Reference `.claude/error-patterns.md` where relevant
- [ ] Add unit tests for error conditions

**Template Section for Skills**:
```markdown
## Error Handling

**For comprehensive error patterns**, see: `.claude/error-patterns.md`

Common errors:
- **[Error Type 1]**: Cause and solution
- **[Error Type 2]**: Cause and solution
- **[Error Type 3]**: Cause and solution

## Exit Codes

- **0**: Success (operation completed successfully)
- **1**: Warnings (operation succeeded with non-critical issues)
- **2**: Failure (operation failed, manual intervention needed)
- **3**: Cannot execute (prerequisites not met, tool unavailable)
```

### Error Message Checklist

When writing error messages, ensure:
- [ ] Component name in brackets: `[Component]`
- [ ] Severity level: `ERROR`, `WARNING`, `FATAL`
- [ ] Brief description of what failed
- [ ] Context: relevant values and state
- [ ] Cause: why it happened
- [ ] Action: what to do next
- [ ] Formatted for readability

### Common Mistake: Vague Errors

❌ **Bad**:
```python
raise Exception("Error")
raise Exception("Failed to process")
raise Exception("Invalid input")
```

✅ **Good**:
```python
raise ValueError(
    f"[Validator] ERROR: Parameter 'rate' out of range\n"
    f"  Context: rate={rate}, valid_range=[1, 100]\n"
    f"  Cause: Value exceeds maximum\n"
    f"  Action: Set rate between 1 and 100 Hz"
)
```

---

## Integration with Skills

### Skills Requiring Error Handling Updates

**High Priority** (user-facing, failure-prone):
- Verification skills (build, test, lint, integration)
- Connection skills (modbus-bridge, modbus-client)
- File operation skills (yaml-config, package-xml-gen)

**Medium Priority** (less common failures):
- Template generation skills
- Analysis skills
- Documentation skills

**Low Priority** (rarely fail):
- Meta skills
- Simple utilities

### Standardization Roadmap

1. ✅ Create error-patterns.md reference
2. ✅ Create diagnose-error skill
3. ✅ Create this implementation guide
4. **Next**: Add error references to 5 representative skills
5. **Future**: Systematically update all 59 commands

---

## Resources

**Reference Documentation**:
- `.claude/error-patterns.md` - Comprehensive error patterns by domain
- `.claude/best-practices.md` - General software engineering practices
- `.claude/[domain]-best-practices.md` - Domain-specific guidelines

**Tools**:
- `/diagnose-error` - Analyze error messages and get debugging guidance

**Implementation**:
- This guide (`docs/error-handling-patterns.md`) - How to implement
- `docs/token-optimization.md` - Keep error messages concise

---

**Last Updated**: 2025-11-10
**Maintainer**: Development team
**Review Schedule**: After adding 10+ new skills
