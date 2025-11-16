# Common Utilities

**NOTE:** This is NOT a skill. This directory contains common utility code shared across multiple skills.

## Purpose

This directory provides shared utilities and common functionality used by other skills, such as:
- Shared data models
- Common helper functions
- Utility classes
- Shared constants

## Usage

Other skills import from this directory as needed:

```python
from skills.common import some_utility
```

## Why This Exists

Rather than duplicating code across skills, common functionality is centralized here for:
- **Maintainability**: Update once, use everywhere
- **Consistency**: Same behavior across skills
- **Reduced Duplication**: DRY principle

## Validation Note

This directory is intentionally excluded from skill validation as it's not a skill itself.
It does not need skill.md or operations.py files.
