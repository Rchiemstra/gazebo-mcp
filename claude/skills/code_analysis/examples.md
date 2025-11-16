# Code Analysis - Usage Examples

Real-world examples demonstrating how to use code_analysis effectively with massive token savings.

---

## Example 1: Quick Codebase Overview

**Scenario:** You've just cloned a new repository and want to understand its structure.

```python
from skills.code_analysis.operations import analyze_codebase

# Get high-level overview (summary format - fast!)
result = analyze_codebase("src/")

if result.success:
    print("Codebase Overview:")
    print(f"  Total files: {result.data['total_files']}")
    print(f"  Total lines: {result.data['total_lines']}")
    print(f"  Average complexity: {result.data['avg_complexity']:.1f}")

    print(f"\nEntry points:")
    for entry in result.data['entry_points']:
        print(f"  - {entry}")

    print(f"\nDesign patterns found:")
    for pattern, count in result.data['patterns_summary'].items():
        print(f"  {pattern}: {count}")

    print(f"\nIntegration points: {result.data['integration_points_count']}")
```

**Output:**
```
Codebase Overview:
  Total files: 145
  Total lines: 12,450
  Average complexity: 4.2

Entry points:
  - main.py
  - app.py
  - cli.py

Design patterns found:
  singleton: 3
  factory: 5
  observer: 2
  decorator: 8
  strategy: 1

Integration points: 23
```

---

## Example 2: The 99% Token Reduction Pattern

**Scenario:** Large codebase (1000 files) - need to find payment-related code.

```python
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

# ❌ INEFFICIENT WAY (50,000 tokens!)
# result = analyze_codebase("large_project/", response_format="detailed")
# # Returns ALL 1000 files with full details
# # Agent receives 50,000 tokens

# ✅ EFFICIENT WAY (500 tokens - 99% savings!)

# Step 1: Get summary to understand scope
overview = analyze_codebase("large_project/")
print(f"Codebase has {overview.data['total_files']} files")

# Step 2: Get filtered data (optimized for local filtering)
result = analyze_codebase("large_project/", response_format="filtered")
# Returns: 2,000 tokens (all 1000 files with minimal data)

# Step 3: Filter locally - runs in YOUR code (0 tokens!)
payment_files = ResultFilter.search(
    result.data["files"],
    "payment",
    ["path", "name"]
)
print(f"Found {len(payment_files)} payment-related files")

# Step 4: Get top 5 most complex
top_complex = ResultFilter.top_n_by_field(payment_files, "max_complexity", 5)

# Agent receives only 5 files (~250 tokens)
# Total: 1,000 + 2,000 + 250 = 3,250 tokens
# Savings: 46,750 tokens (93.5%)!

print("\nTop 5 complex payment files:")
for file_data in top_complex:
    print(f"  {file_data['path']}: complexity {file_data['max_complexity']}")
```

**Output:**
```
Codebase has 1000 files
Found 23 payment-related files

Top 5 complex payment files:
  src/payment/processor.py: complexity 15
  src/payment/refund.py: complexity 12
  src/payment/stripe_adapter.py: complexity 10
  src/payment/validation.py: complexity 9
  src/payment/receipt.py: complexity 7
```

---

## Example 3: Finding Refactoring Candidates

**Scenario:** Identify high-complexity code that needs refactoring.

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

# Step 1: Get all files with complexity metrics
result = analyze_codebase("src/", response_format="filtered")

# Step 2: Find files with high average complexity
complex_files = ResultFilter.top_n_by_field(
    result.data["files"],
    "avg_complexity",
    10
)

print("Top 10 Files for Refactoring:")
print("="*60)
for i, file_data in enumerate(complex_files, 1):
    print(f"{i}. {file_data['path']}")
    print(f"   Avg complexity: {file_data['avg_complexity']:.1f}")
    print(f"   Max complexity: {file_data['max_complexity']}")
    print(f"   Functions: {file_data['functions_count']}")

# Step 3: Deep dive into most complex file
most_complex = complex_files[0]
print(f"\n{'='*60}")
print(f"Analyzing: {most_complex['path']}")
print(f"{'='*60}")

details = analyze_file(most_complex['path'], response_format="detailed")

# Find complex functions
print("\nComplex Functions (complexity > 10):")
complex_functions = [
    f for f in details.data['functions']
    if f['complexity'] > 10
]

for func in sorted(complex_functions, key=lambda f: f['complexity'], reverse=True):
    print(f"\n  {func['name']} (line {func['line_number']})")
    print(f"    Complexity: {func['complexity']}")
    print(f"    Parameters: {len(func['parameters'])}")
    if func['raises']:
        print(f"    Raises: {', '.join(func['raises'])}")
    if func['calls']:
        print(f"    Calls: {', '.join(func['calls'][:5])}...")
```

**Output:**
```
Top 10 Files for Refactoring:
============================================================
1. src/services/order_processor.py
   Avg complexity: 8.5
   Max complexity: 18
   Functions: 12

2. src/payment/transaction.py
   Avg complexity: 7.2
   Max complexity: 15
   Functions: 15

...

============================================================
Analyzing: src/services/order_processor.py
============================================================

Complex Functions (complexity > 10):

  process_order (line 45)
    Complexity: 18
    Parameters: 4
    Raises: ValueError, OrderError, PaymentError
    Calls: validate_order, check_inventory, process_payment, send_confirmation...

  calculate_shipping (line 156)
    Complexity: 12
    Parameters: 3
    Raises: ShippingError
    Calls: get_address, calculate_distance, get_rates...
```

---

## Example 4: Dependency Analysis

**Scenario:** Understand how modules depend on each other.

```python
from skills.code_analysis.operations import analyze_file

# Analyze a service file
result = analyze_file("src/services/order_service.py", response_format="detailed")

print("Import Analysis:")
print("="*60)

# Categorize imports
stdlib_imports = []
third_party = []
local_imports = []

for imp in result.data['imports']:
    module = imp['module']
    if module.startswith('.'):
        local_imports.append(imp)
    elif module in ['os', 'sys', 'datetime', 'typing', 'json']:
        stdlib_imports.append(imp)
    else:
        third_party.append(imp)

print(f"\nStandard Library ({len(stdlib_imports)}):")
for imp in stdlib_imports:
    print(f"  from {imp['module']} import {', '.join(imp['names'])}")

print(f"\nThird Party ({len(third_party)}):")
for imp in third_party:
    print(f"  from {imp['module']} import {', '.join(imp['names'])}")

print(f"\nLocal Modules ({len(local_imports)}):")
for imp in local_imports:
    print(f"  from {imp['module']} import {', '.join(imp['names'])}")

# Show function dependencies
print(f"\n{'='*60}")
print("Function Dependency Graph:")
print("="*60)

for func_name, deps in result.data['dependency_graph'].items():
    if deps:
        print(f"{func_name}")
        for dep in deps:
            print(f"  └─> {dep}")
    else:
        print(f"{func_name} (no dependencies)")
```

**Output:**
```
Import Analysis:
============================================================

Standard Library (4):
  from typing import Dict, List, Optional
  from datetime import datetime
  from decimal import Decimal
  from json import dumps, loads

Third Party (3):
  from sqlalchemy import Column, Integer, String
  from pydantic import BaseModel, validator
  from redis import Redis

Local Modules (5):
  from .models import Order, OrderItem
  from .payment import PaymentProcessor
  from .inventory import InventoryService
  from ..utils.logging import logger
  from ..config import settings

============================================================
Function Dependency Graph:
============================================================
create_order
  └─> validate_order
  └─> check_inventory
  └─> process_payment
  └─> send_notification

validate_order
  └─> validate_items
  └─> calculate_total

process_payment
  └─> charge_card
  └─> create_receipt

send_notification (no dependencies)
```

---

## Example 5: Pattern Detection

**Scenario:** Find all Singleton implementations in the codebase.

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

# Step 1: Find files with Singleton pattern
result = analyze_codebase("src/", response_format="filtered")

singleton_files = [
    f for f in result.data["files"]
    if "singleton" in f.get("has_patterns", [])
]

print(f"Found {len(singleton_files)} files with Singleton pattern\n")
print("="*60)

# Step 2: Examine each Singleton
for file_data in singleton_files:
    details = analyze_file(file_data['path'], response_format="detailed")

    # Find Singleton patterns
    for pattern in details.data['patterns_detected']:
        if pattern['type'] == 'singleton':
            print(f"\nFile: {file_data['path']}")
            print(f"  Class: {pattern['class']}")
            print(f"  Line: {pattern['line']}")
            print(f"  Confidence: {pattern['confidence']:.1%}")

            # Show the class details
            for cls in details.data['classes']:
                if cls['name'] == pattern['class']:
                    print(f"  Base classes: {', '.join(cls['base_classes']) if cls['base_classes'] else 'None'}")
                    print(f"  Methods: {len(cls['methods'])}")

                    # Check for _instance attribute
                    if '_instance' in cls.get('attributes', []):
                        print(f"  ✓ Has _instance attribute")

                    # Check for __new__ method
                    if any(m['name'] == '__new__' for m in cls['methods']):
                        print(f"  ✓ Has __new__ method")

print("\n" + "="*60)
print(f"Total Singleton implementations: {len(singleton_files)}")
```

**Output:**
```
Found 3 files with Singleton pattern

============================================================

File: src/config/settings.py
  Class: Settings
  Line: 15
  Confidence: 98.5%
  Base classes: None
  Methods: 5
  ✓ Has _instance attribute
  ✓ Has __new__ method

File: src/services/database.py
  Class: DatabaseConnection
  Line: 23
  Confidence: 95.0%
  Base classes: ABC
  Methods: 8
  ✓ Has _instance attribute
  ✓ Has __new__ method

File: src/logging/logger.py
  Class: Logger
  Line: 10
  Confidence: 92.3%
  Base classes: None
  Methods: 12
  ✓ Has _instance attribute

============================================================
Total Singleton implementations: 3
```

---

## Example 6: Integration Point Discovery

**Scenario:** Find all external integrations (APIs, databases, etc.).

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

# Step 1: Get overview of integration points
overview = analyze_codebase("src/")
print(f"Total integration points found: {overview.data['integration_points_count']}\n")

# Step 2: Get files with integration points
result = analyze_codebase("src/", response_format="filtered")

integration_files = [
    f for f in result.data["files"]
    if f.get("has_integration_points")
]

# Step 3: Categorize by type
from collections import defaultdict
by_type = defaultdict(list)

for file_data in integration_files:
    details = analyze_file(file_data['path'], response_format="detailed")

    for integration in details.data.get('integration_points', []):
        by_type[integration['type']].append({
            'file': file_data['path'],
            'line': integration['line'],
            'method': integration.get('method'),
            'details': integration.get('details')
        })

# Step 4: Display by category
print("Integration Points by Type:")
print("="*60)

for int_type, integrations in sorted(by_type.items()):
    print(f"\n{int_type.upper()} ({len(integrations)} integrations):")

    for integration in integrations:
        print(f"  {integration['file']}:{integration['line']}")
        if integration.get('method'):
            print(f"    Method: {integration['method']}")
        if integration.get('details'):
            print(f"    Details: {integration['details']}")
```

**Output:**
```
Total integration points found: 23

Integration Points by Type:
============================================================

API (8 integrations):
  src/services/payment.py:92
    Method: charge_card
    Details: Stripe API

  src/services/shipping.py:45
    Method: calculate_rate
    Details: FedEx API

  src/services/weather.py:28
    Method: get_forecast
    Details: OpenWeather API

...

DATABASE (12 integrations):
  src/models/user.py:15
    Method: __tablename__
    Details: PostgreSQL via SQLAlchemy

  src/repositories/order.py:34
    Method: create
    Details: PostgreSQL via SQLAlchemy ORM

...

MESSAGE_QUEUE (3 integrations):
  src/workers/email.py:23
    Method: send_email
    Details: RabbitMQ

  src/workers/notifications.py:56
    Method: process_notification
    Details: Redis Pub/Sub

...
```

---

## Example 7: Analyzing Single File in Detail

**Scenario:** Deep dive into a specific file to understand its structure.

```python
from skills.code_analysis.operations import analyze_file

# Get detailed analysis
result = analyze_file("src/services/payment_processor.py", response_format="detailed")

print("File Analysis:")
print("="*60)
print(f"File: {result.data['file_path']}")
print(f"Total lines: {result.data['total_lines']}")
print(f"Total entities: {result.data['total_entities']}")

# Classes
print(f"\nCLASSES ({len(result.data['classes'])}):")
for cls in result.data['classes']:
    print(f"\n  {cls['name']} (line {cls['line_number']})")

    if cls['base_classes']:
        print(f"    Inherits: {', '.join(cls['base_classes'])}")

    if cls['docstring']:
        print(f"    Doc: {cls['docstring'][:60]}...")

    print(f"    Methods ({len(cls['methods'])}):")
    for method in cls['methods'][:5]:  # Show first 5
        params = f"({len(method['parameters'])} params)" if method['parameters'] else "()"
        complexity_str = f"complexity: {method['complexity']}"
        print(f"      - {method['name']}{params} [{complexity_str}]")

    if cls.get('decorators'):
        print(f"    Decorators: {', '.join(cls['decorators'])}")

# Functions
print(f"\nFUNCTIONS ({len(result.data['functions'])}):")
for func in result.data['functions']:
    print(f"\n  {func['name']} (line {func['line_number']})")

    if func['docstring']:
        print(f"    Doc: {func['docstring'][:60]}...")

    print(f"    Complexity: {func['complexity']}")

    if func['parameters']:
        print(f"    Parameters:")
        for param in func['parameters']:
            param_str = f"      - {param['name']}"
            if param.get('type'):
                param_str += f": {param['type']}"
            if param.get('default'):
                param_str += f" = {param['default']}"
            print(param_str)

    if func['returns']:
        print(f"    Returns: {func['returns']}")

    if func['raises']:
        print(f"    Raises: {', '.join(func['raises'])}")

    if func['calls']:
        print(f"    Calls: {', '.join(func['calls'][:5])}...")

# Patterns
if result.data.get('patterns_detected'):
    print(f"\nPATTERNS DETECTED:")
    for pattern in result.data['patterns_detected']:
        print(f"  - {pattern['type']} in {pattern.get('class') or pattern.get('function')}")

# Integration points
if result.data.get('integration_points'):
    print(f"\nINTEGRATION POINTS:")
    for integration in result.data['integration_points']:
        print(f"  - {integration['type']} at line {integration['line']}")
        if integration.get('details'):
            print(f"    {integration['details']}")
```

---

## Example 8: Batch Analysis with Filtering

**Scenario:** Analyze multiple directories and aggregate results.

```python
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter
from pathlib import Path

# Directories to analyze
directories = ["src/services", "src/models", "src/utils"]

total_results = {
    'files': 0,
    'lines': 0,
    'avg_complexity': [],
    'patterns': {},
    'integrations': 0
}

print("Batch Analysis:")
print("="*60)

for directory in directories:
    result = analyze_codebase(directory)

    if result.success:
        print(f"\n{directory}:")
        print(f"  Files: {result.data['total_files']}")
        print(f"  Lines: {result.data['total_lines']}")
        print(f"  Avg Complexity: {result.data['avg_complexity']:.1f}")

        # Aggregate
        total_results['files'] += result.data['total_files']
        total_results['lines'] += result.data['total_lines']
        total_results['avg_complexity'].append(result.data['avg_complexity'])
        total_results['integrations'] += result.data['integration_points_count']

        # Aggregate patterns
        for pattern, count in result.data['patterns_summary'].items():
            total_results['patterns'][pattern] = total_results['patterns'].get(pattern, 0) + count

# Summary
print(f"\n{'='*60}")
print("AGGREGATE SUMMARY:")
print(f"{'='*60}")
print(f"Total files: {total_results['files']}")
print(f"Total lines: {total_results['lines']}")

if total_results['avg_complexity']:
    overall_avg = sum(total_results['avg_complexity']) / len(total_results['avg_complexity'])
    print(f"Overall avg complexity: {overall_avg:.1f}")

print(f"Total integration points: {total_results['integrations']}")

print(f"\nPattern distribution:")
for pattern, count in sorted(total_results['patterns'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {pattern}: {count}")
```

**Output:**
```
Batch Analysis:
============================================================

src/services:
  Files: 23
  Lines: 3,456
  Avg Complexity: 5.2

src/models:
  Files: 15
  Lines: 1,234
  Avg Complexity: 2.8

src/utils:
  Files: 8
  Lines: 567
  Avg Complexity: 3.1

============================================================
AGGREGATE SUMMARY:
============================================================
Total files: 46
Total lines: 5,257
Overall avg complexity: 3.7
Total integration points: 12

Pattern distribution:
  decorator: 15
  factory: 8
  singleton: 5
  observer: 3
  strategy: 2
```

---

## Example 9: Progressive Analysis Workflow

**Scenario:** Start broad, narrow down progressively.

```python
from skills.code_analysis.operations import analyze_codebase, analyze_file
from skills.common.filters import ResultFilter

print("Progressive Analysis Workflow")
print("="*60)

# Phase 1: Overview (summary - 500 tokens)
print("\n[Phase 1] Getting overview...")
overview = analyze_codebase("src/")
print(f"  Files: {overview.data['total_files']}")
print(f"  Avg complexity: {overview.data['avg_complexity']:.1f}")

# Phase 2: Filter for specific area (filtered - 2000 tokens)
print("\n[Phase 2] Filtering for authentication code...")
result = analyze_codebase("src/", response_format="filtered")
auth_files = ResultFilter.search(result.data["files"], "auth", ["path", "name"])
print(f"  Found {len(auth_files)} auth-related files")

# Phase 3: Find complex auth files (local filtering - 0 tokens)
print("\n[Phase 3] Finding complex auth files...")
complex_auth = ResultFilter.top_n_by_field(auth_files, "avg_complexity", 3)
print(f"  Top 3 complex auth files:")
for file_data in complex_auth:
    print(f"    - {file_data['path']} (complexity: {file_data['avg_complexity']:.1f})")

# Phase 4: Deep dive into most complex (detailed - 3000 tokens)
print("\n[Phase 4] Analyzing most complex file...")
most_complex_path = complex_auth[0]['path']
details = analyze_file(most_complex_path, response_format="detailed")

print(f"  File: {most_complex_path}")
print(f"  Functions: {len(details.data['functions'])}")
print(f"  Classes: {len(details.data['classes'])}")

# Find most complex function
if details.data['functions']:
    most_complex_func = max(details.data['functions'], key=lambda f: f['complexity'])
    print(f"\n  Most complex function:")
    print(f"    Name: {most_complex_func['name']}")
    print(f"    Complexity: {most_complex_func['complexity']}")
    print(f"    Line: {most_complex_func['line_number']}")

print("\n" + "="*60)
print("Total tokens used: ~5,500")
print("Without filtering: ~50,000 tokens")
print("Savings: 89%!")
```

---

## Common Patterns

### Pattern: Summary → Filtered → Detailed

```python
# Always start with summary
overview = analyze_codebase("src/")

# If large, use filtered + local filtering
if overview.data['total_files'] > 100:
    result = analyze_codebase("src/", response_format="filtered")
    filtered = ResultFilter.search(result.data["files"], "target")
    # Then analyze specific files in detail

# If small, use detailed directly
else:
    result = analyze_codebase("src/", response_format="detailed")
```

### Pattern: Error-Resilient Analysis

```python
result = analyze_codebase("src/")

if not result.success:
    print(f"Error: {result.error}")

    # Try suggestions
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")

    # Try alternative paths
    alternative_paths = ["lib/", "app/", "code/"]
    for path in alternative_paths:
        result = analyze_codebase(path)
        if result.success:
            break
```

### Pattern: Complexity-Based Priorities

```python
result = analyze_codebase("src/", response_format="filtered")

# Categorize by complexity
high = [f for f in result.data["files"] if f["avg_complexity"] > 8]
medium = [f for f in result.data["files"] if 5 <= f["avg_complexity"] <= 8]
low = [f for f in result.data["files"] if f["avg_complexity"] < 5]

print(f"High complexity: {len(high)} files (priority 1)")
print(f"Medium complexity: {len(medium)} files (priority 2)")
print(f"Low complexity: {len(low)} files (priority 3)")
```

---

## Next Steps

- Review **reference.md** for complete API documentation
- Try these examples with your own codebase
- Combine with **test_orchestrator** for comprehensive quality analysis
- Use with **refactor_assistant** for targeted improvements

---

*Last Updated: 2025-11-07*
