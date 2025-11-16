# Context Manager - Usage Examples

Real-world examples demonstrating how to use context_manager effectively for token optimization.

---

## Example 1: Basic Context Monitoring

**Scenario:** Monitor context usage during development work.

```python
from skills.context_manager.operations import analyze_context_usage

# Check current context usage
analysis = analyze_context_usage(estimated_tokens=75000)

print(f"Context Usage Analysis:")
print(f"  Tokens used: {analysis.data['tokens_used']:,}")
print(f"  Usage: {analysis.data['usage_percent']}%")
print(f"  Status: {analysis.data['status']}")
print(f"  Priority: {analysis.data['priority']}")

if analysis.data['usage_percent'] > 50:
    print(f"\n⚠ Optimization recommended!")
    print(f"Top recommendations:")
    for rec in analysis.data.get('top_recommendations', []):
        print(f"  • {rec}")
```

**Output:**
```
Context Usage Analysis:
  Tokens used: 75,000
  Usage: 37.5%
  Status: moderate
  Priority: low

```

---

## Example 2: Creating Persistent Notes

**Scenario:** Save important architectural decisions to avoid losing them.

```python
from skills.context_manager.operations import create_notes

# Save architectural decisions
result = create_notes("""
## Architectural Decisions - 2025-01-15

### Database Layer
- **Primary Database:** PostgreSQL 15
  - Reason: Better performance for complex queries
  - ACID compliance required
  - Good Python ORM support (SQLAlchemy)

### Caching Strategy
- **Cache:** Redis 7
  - Session storage
  - API response caching (5min TTL)
  - Rate limiting counters

### Message Queue
- **Queue:** RabbitMQ
  - Async task processing
  - Email notifications
  - Background jobs

### Authentication
- **Method:** JWT tokens
  - 60 minute expiry
  - Refresh tokens: 7 days
  - Stored in Redis for quick invalidation
""")

if result.success:
    print(f"✓ Decisions saved to: {result.data['notes_file']}")
    print(f"  Estimated tokens saved: {result.data['estimated_tokens_saved']:.0f}")
    print(f"  Content length: {result.data['content_length']} characters")
```

**Output:**
```
✓ Decisions saved to: .claude/notes/NOTES.md
  Estimated tokens saved: 305
  Content length: 682 characters
```

---

## Example 3: Compacting Long Conversations

**Scenario:** Multi-hour development session needs context reduction.

```python
from skills.context_manager.operations import compact_conversation

# After several hours of work
summary = compact_conversation(
    work_completed=[
        "Set up Django project structure",
        "Implemented user authentication (login, logout, register)",
        "Created database models (User, Profile, Post, Comment)",
        "Added API endpoints (/api/auth/, /api/posts/)",
        "Wrote unit tests (85% coverage)",
        "Set up CI/CD pipeline (GitHub Actions)",
        "Deployed to staging environment"
    ],
    decisions_made=[
        "Use Django REST Framework for API",
        "PostgreSQL for production database",
        "JWT authentication with djangorestframework-simplejwt",
        "Docker for containerization",
        "AWS ECS for deployment",
        "SendGrid for email notifications"
    ],
    unresolved_issues=[
        "Performance optimization for large datasets",
        "Add WebSocket support for real-time features",
        "Implement rate limiting on API endpoints",
        "Set up monitoring and alerting",
        "Schedule production deployment"
    ]
)

print("=" * 60)
print("SESSION SUMMARY")
print("=" * 60)
print(summary.data['compact_summary'])
print("\n" + "=" * 60)
print(f"Summary tokens: {summary.data['estimated_tokens']}")
print(f"Original conversation: ~10,000 tokens")
print(f"Savings: ~{10000 - summary.data['estimated_tokens']} tokens (95%)")
```

**Output:**
```
============================================================
SESSION SUMMARY
============================================================
Completed (7 items):
  ✓ Set up Django project structure
  ✓ Implemented user authentication (login, logout, register)
  ✓ Created database models (User, Profile, Post, Comment)
  ✓ Added API endpoints (/api/auth/, /api/posts/)
  ✓ Wrote unit tests (85% coverage)
  ✓ Set up CI/CD pipeline (GitHub Actions)
  ✓ Deployed to staging environment

Decisions (6 items):
  • Use Django REST Framework for API
  • PostgreSQL for production database
  • JWT authentication with djangorestframework-simplejwt
  • Docker for containerization
  • AWS ECS for deployment
  • SendGrid for email notifications

Unresolved (5 items):
  ⚠ Performance optimization for large datasets
  ⚠ Add WebSocket support for real-time features
  ⚠ Implement rate limiting on API endpoints
  ⚠ Set up monitoring and alerting
  ⚠ Schedule production deployment

============================================================
Summary tokens: 312
Original conversation: ~10,000 tokens
Savings: ~9688 tokens (95%)
```

---

## Example 4: Complete Long-Horizon Workflow

**Scenario:** Managing context throughout a multi-day project.

```python
from skills.context_manager.operations import (
    analyze_context_usage,
    create_notes,
    compact_conversation
)

# Day 1 Start
print("=== DAY 1: Project Start ===")

create_notes("""
## Project: E-commerce Platform MVP

**Timeline:** 2 weeks
**Team:** Solo developer
**Stack:** Django + React + PostgreSQL

**Phase 1 Goals:**
- User authentication
- Product catalog
- Shopping cart
- Checkout flow
""")

# Day 1 Midday - Check context
analysis = analyze_context_usage(estimated_tokens=45000)
print(f"Midday check: {analysis.data['usage_percent']}% - {analysis.data['status']}")

# Day 1 End
day1_summary = compact_conversation(
    work_completed=[
        "Project setup",
        "User auth implemented",
        "Database models created"
    ],
    decisions_made=[
        "Use Stripe for payments",
        "Use Tailwind CSS for styling"
    ],
    unresolved_issues=[
        "Product catalog UI",
        "Shopping cart logic"
    ]
)

create_notes(f"""
## Day 1 Summary
{day1_summary.data['compact_summary']}
""")

# Day 2 Start - Fresh context
print("\n=== DAY 2: Resume ===")
# Load yesterday's summary from notes
# Continue with fresh context

# Day 2 Midday - High usage
analysis = analyze_context_usage(estimated_tokens=125000)
print(f"Midday check: {analysis.data['usage_percent']}% - {analysis.data['status']}")

if analysis.data['usage_percent'] > 60:
    print("⚠ High context usage detected!")

    # Get detailed recommendations
    detailed = analyze_context_usage(
        estimated_tokens=125000,
        response_format="detailed"
    )

    print("\nRecommendations:")
    for rec in detailed.data['recommendations']:
        print(f"  [{rec['priority'].upper()}] {rec['description']}")
        print(f"    Potential savings: {rec['potential_savings']}")

    # Take action
    print("\nTaking action: Creating checkpoint...")

    checkpoint = compact_conversation(
        work_completed=[
            "Product catalog complete",
            "Shopping cart implemented"
        ],
        decisions_made=[
            "Use React Context for cart state",
            "Lazy load product images"
        ],
        unresolved_issues=[
            "Checkout flow",
            "Payment integration"
        ]
    )

    create_notes(f"""
## Day 2 Checkpoint
{checkpoint.data['compact_summary']}
""")

    print(f"✓ Checkpoint saved - Freed ~8000 tokens")

# Day 2 End
print("\n=== DAY 2: Complete ===")
# Final summary and notes
```

**Output:**
```
=== DAY 1: Project Start ===
Midday check: 22.5% - low

=== DAY 2: Resume ===
Midday check: 62.5% - high
⚠ High context usage detected!

Recommendations:
  [HIGH] Use response_format='summary' instead of 'detailed'
    Potential savings: 80-95%
  [HIGH] Use ResultFilter for local data filtering
    Potential savings: 95-99%
  [MEDIUM] Create persistent notes for important information
    Potential savings: Variable

Taking action: Creating checkpoint...
✓ Checkpoint saved - Freed ~8000 tokens

=== DAY 2: Complete ===
```

---

## Example 5: Emergency Context Recovery

**Scenario:** Context overflow is imminent - need to save everything.

```python
from skills.context_manager.operations import (
    analyze_context_usage,
    create_notes,
    compact_conversation
)

# Critical situation
analysis = analyze_context_usage(estimated_tokens=190000)

print(f"🚨 CRITICAL: Context at {analysis.data['usage_percent']}%")
print(f"Remaining: {analysis.data['tokens_remaining']:,} tokens")

if analysis.data['status'] == 'critical':
    print("\n⚠ EMERGENCY SAVE INITIATED ⚠")

    # 1. Save ALL important information
    emergency_notes = create_notes("""
## EMERGENCY CONTEXT SAVE - 2025-01-15 18:45

### Current State
- **Feature:** Payment integration
- **Status:** 90% complete
- **Blocked:** Waiting for Stripe API keys from client

### Completed This Session
- Implemented Stripe checkout flow
- Added payment webhooks
- Created invoice generation
- Tested with Stripe test mode
- Added error handling for failed payments

### Key Architectural Decisions
- **Payment Gateway:** Stripe
- **Webhook Handling:** Async with Celery
- **Invoice Storage:** S3 + database reference
- **Failed Payments:** Retry logic with exponential backoff

### Critical Code Locations
- Payment flow: `app/payments/views.py:PaymentCheckoutView`
- Webhooks: `app/payments/webhooks.py:stripe_webhook_handler`
- Invoice generation: `app/invoices/generator.py:generate_pdf_invoice`

### TODO (Priority Order)
1. Get production Stripe API keys from client
2. Test webhook delivery in production
3. Set up invoice email notifications
4. Add payment analytics dashboard
5. Document payment flow for team

### Environment Variables Needed
```
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Known Issues
- Invoice PDF generation is slow for large orders (>50 items)
  - TODO: Optimize or move to background job
- Webhook endpoint occasionally times out
  - TODO: Investigate and add retry logic

### Next Steps
1. Contact client for API keys (ASAP)
2. Deploy to staging with test keys
3. Schedule production deployment for Friday
    """, notes_file=".claude/notes/EMERGENCY_SAVE.md", append=False)

    print(f"✓ Emergency notes saved: {emergency_notes.data['notes_file']}")

    # 2. Create compact summary
    summary = compact_conversation(
        work_completed=[
            "Stripe checkout integration",
            "Payment webhooks",
            "Invoice generation",
            "Error handling",
            "Test mode validation"
        ],
        decisions_made=[
            "Use Stripe for payments",
            "Async webhooks with Celery",
            "S3 for invoice storage",
            "Exponential backoff for retries"
        ],
        unresolved_issues=[
            "Need production API keys",
            "Webhook timeout issues",
            "Invoice PDF performance"
        ],
        response_format="detailed"
    )

    print("\nCompact Summary:")
    print(summary.data['compact_summary'])

    print("\nNext Steps:")
    for step in summary.data['next_steps']:
        print(f"  • {step}")

    print("\n✓ Context saved. Safe to continue with fresh session.")
```

**Output:**
```
🚨 CRITICAL: Context at 95.0%
Remaining: 10,000 tokens

⚠ EMERGENCY SAVE INITIATED ⚠
✓ Emergency notes saved: .claude/notes/EMERGENCY_SAVE.md

Compact Summary:
Completed (5 items):
  ✓ Stripe checkout integration
  ✓ Payment webhooks
  ✓ Invoice generation
  ✓ Error handling
  ✓ Test mode validation

Decisions (4 items):
  • Use Stripe for payments
  • Async webhooks with Celery
  • S3 for invoice storage
  • Exponential backoff for retries

Unresolved (3 items):
  ⚠ Need production API keys
  ⚠ Webhook timeout issues
  ⚠ Invoice PDF performance

Next Steps:
  • Persist summary to notes if needed
  • Clear conversation (if supported)
  • Continue work referencing summary

✓ Context saved. Safe to continue with fresh session.
```

---

## Example 6: Integration with Other Skills

**Scenario:** Combine context management with code analysis for large codebases.

```python
from skills.context_manager.operations import analyze_context_usage, create_notes
from skills.code_analysis.operations import analyze_codebase
from skills.common.filters import ResultFilter

print("=== Analyzing Large Codebase ===")

# Check context before starting
analysis = analyze_context_usage(estimated_tokens=30000)
print(f"Starting context: {analysis.data['usage_percent']}%")

# Analyze codebase with token efficiency
print("\n1. Getting codebase overview...")
overview = analyze_codebase("src/", response_format="summary")
print(f"   Found {overview.data['total_files']} files")

# Check context after overview
analysis = analyze_context_usage(estimated_tokens=31000)
print(f"   Context now: {analysis.data['usage_percent']}% (+{1000} tokens)")

# Use filtered format for efficient data access
print("\n2. Getting detailed data with filtering...")
result = analyze_codebase("src/", response_format="filtered")

# Filter locally - 0 additional tokens!
auth_files = ResultFilter.search(result.data["files"], "auth", ["path"])
complex_files = ResultFilter.top_n_by_field(auth_files, "complexity", 5)

print(f"   Found {len(auth_files)} auth files")
print(f"   Top 5 complex auth files identified")

# Check context - should be similar
analysis = analyze_context_usage(estimated_tokens=33000)
print(f"   Context now: {analysis.data['usage_percent']}% (+{2000} tokens)")

# Save findings to notes instead of keeping in context
findings = "\n".join([
    f"- {f['path']} (complexity: {f['avg_complexity']})"
    for f in complex_files
])

create_notes(f"""
## Code Analysis Findings

### Auth Module Analysis
Top 5 complex files:
{findings}

### Recommendations
- Review high-complexity auth files for refactoring
- Add comprehensive tests for complex auth logic
- Consider breaking down into smaller modules
""")

print("\n3. Findings saved to notes")

# Final context check
analysis = analyze_context_usage(estimated_tokens=33500)
print(f"\nFinal context: {analysis.data['usage_percent']}%")
print(f"Total tokens used: ~{500} (vs ~10,000 without optimization)")
print(f"Savings: ~{9500} tokens (95%)")
```

**Output:**
```
=== Analyzing Large Codebase ===
Starting context: 15.0%

1. Getting codebase overview...
   Found 247 files
   Context now: 15.5% (+1000 tokens)

2. Getting detailed data with filtering...
   Found 23 auth files
   Top 5 complex auth files identified
   Context now: 16.5% (+2000 tokens)

3. Findings saved to notes

Final context: 16.8%
Total tokens used: ~500 (vs ~10,000 without optimization)
Savings: ~9500 tokens (95%)
```

---

## Example 7: Periodic Context Checkpoints

**Scenario:** Regular checkpoints during development to prevent overflow.

```python
from skills.context_manager.operations import (
    analyze_context_usage,
    create_notes,
    compact_conversation
)

class ContextMonitor:
    """Helper class for context management."""

    def __init__(self, checkpoint_threshold=60):
        self.checkpoint_threshold = checkpoint_threshold
        self.checkpoints = []

    def check(self, current_tokens, session_info):
        """Check context and create checkpoint if needed."""
        analysis = analyze_context_usage(current_tokens)

        print(f"Context: {analysis.data['usage_percent']}% ({analysis.data['status']})")

        if analysis.data['usage_percent'] >= self.checkpoint_threshold:
            print(f"⚠ Checkpoint threshold reached!")
            return self.create_checkpoint(session_info)

        return None

    def create_checkpoint(self, session_info):
        """Create a context checkpoint."""
        summary = compact_conversation(
            work_completed=session_info['completed'],
            decisions_made=session_info['decisions'],
            unresolved_issues=session_info['unresolved']
        )

        # Save to notes
        checkpoint_id = len(self.checkpoints) + 1
        create_notes(f"""
## Checkpoint {checkpoint_id}
{summary.data['compact_summary']}
        """, notes_file=f".claude/notes/checkpoint_{checkpoint_id}.md")

        self.checkpoints.append(summary)
        print(f"✓ Checkpoint {checkpoint_id} created")

        return summary

# Use during development
monitor = ContextMonitor(checkpoint_threshold=60)

# Work session
print("=== Work Session ===\n")

# After task 1
monitor.check(40000, {
    'completed': ["Task 1"],
    'decisions': ["Decision A"],
    'unresolved': ["Task 2", "Task 3"]
})

# After task 2
monitor.check(85000, {
    'completed': ["Task 1", "Task 2"],
    'decisions': ["Decision A", "Decision B"],
    'unresolved': ["Task 3"]
})

# After task 3
monitor.check(130000, {
    'completed': ["Task 1", "Task 2", "Task 3"],
    'decisions': ["Decision A", "Decision B", "Decision C"],
    'unresolved': []
})

print(f"\nTotal checkpoints: {len(monitor.checkpoints)}")
```

**Output:**
```
=== Work Session ===

Context: 20.0% (low)
Context: 42.5% (moderate)
Context: 65.0% (high)
⚠ Checkpoint threshold reached!
✓ Checkpoint 1 created

Total checkpoints: 1
```

---

## Common Patterns

### Pattern: Proactive Monitoring

```python
# Check context regularly
def work_session():
    analysis = analyze_context_usage(current_tokens)

    if analysis.data['usage_percent'] > 50:
        # Take action early
        pass
```

### Pattern: Save Important Info

```python
# Instead of keeping in context
create_notes("Important architectural decision made...")

# Frees up tokens for actual work
```

### Pattern: Emergency Save

```python
analysis = analyze_context_usage(estimated_tokens)

if analysis.data['status'] == 'critical':
    # Save everything immediately
    create_notes("EMERGENCY SAVE: ...")
    summary = compact_conversation(...)
```

---

## Next Steps

- Review **reference.md** for complete API documentation
- Use proactively when context > 50%
- Combine with response_format and ResultFilter for maximum efficiency
- Create notes for long-horizon tasks

---

*Last Updated: 2025-11-08*
