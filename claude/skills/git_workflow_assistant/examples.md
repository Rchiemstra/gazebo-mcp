# Git Workflow Assistant - Usage Examples

Real-world usage examples for git_workflow_assistant skill.

---

## Example 1: Basic Commit Message Generation

**Scenario:** You've made changes and want a properly formatted conventional commit message.

```python
from skills.git_workflow_assistant.operations import generate_commit_message

# After staging changes: git add src/auth.py tests/test_auth.py

# Generate conventional commit message
result = generate_commit_message()

if result.success:
    data = result.data

    print("Suggested Commit Message:")
    print("=" * 60)
    print(data['commit_message'])
    print("=" * 60)
    print()
    print(f"Type: {data['commit_type']}")
    print(f"Scope: {data['scope']}")
    print(f"Breaking: {data['is_breaking']}")
    print(f"Files analyzed: {data['files_analyzed']}")

    # Use the message
    # git commit -m "{data['commit_message']}"
else:
    print(f"❌ Error: {result.error}")
    if result.error_code == "NO_CHANGES":
        print("Make sure you've staged changes with 'git add'")
```

**Output:**
```
Suggested Commit Message:
============================================================
feat(auth): add OAuth2 authentication

Implements OAuth2 flow with token management.
Adds authentication endpoints and middleware.
============================================================

Type: feat
Scope: auth
Breaking: False
Files analyzed: 2
```

**Token Usage:** ~300 tokens

---

## Example 2: Feature Branch Creation

**Scenario:** Starting new feature work with proper branch naming.

```python
from skills.git_workflow_assistant.operations import suggest_branch_name

# Suggest branch name for new feature
result = suggest_branch_name(
    description="add user notifications",
    branch_type="feature",
    issue_number="JIRA-789",
    strategy="gitflow"
)

if result.success:
    data = result.data

    print(f"Suggested Branch: {data['branch_name']}")
    print(f"Strategy: {data['strategy']}")
    print(f"Type: {data['branch_type']}")
    print()

    print("Alternative names:")
    for alt in data['alternative_names']:
        print(f"  - {alt}")
    print()

    print("Convention rules:")
    for key, value in data['convention'].items():
        print(f"  {key}: {value}")
    print()

    print(f"Create with: git checkout -b {data['branch_name']}")
else:
    print(f"❌ Error: {result.error}")
```

**Output:**
```
Suggested Branch: feature/JIRA-789-add-user-notifications
Strategy: gitflow
Type: feature

Alternative names:
  - feature/add-notifications
  - feature/user-notifications
  - feature/notification-system

Convention rules:
  prefix: feature/
  include_issue: True
  separator: -
  max_length: 50

Create with: git checkout -b feature/JIRA-789-add-user-notifications
```

**Token Usage:** ~150 tokens

---

## Example 3: Analyzing Changes Before Commit

**Scenario:** Review what you're about to commit to ensure it makes sense.

```python
from skills.git_workflow_assistant.operations import analyze_changes

# Analyze staged changes
result = analyze_changes(repo_path=".", include_unstaged=False)

if result.success:
    data = result.data

    print(f"Repository: {data['repo_path']}")
    print(f"Current Branch: {data['current_branch']}")
    print(f"Total Files Changed: {data['total_files_changed']}")
    print(f"  Staged: {data['files_staged']}")
    print(f"  Unstaged: {data['files_unstaged']}")
    print()

    print("Changes:")
    for change_type, files in data['changes'].items():
        if files:
            print(f"  {change_type.capitalize()}: {len(files)}")
            for file in files:
                print(f"    - {file}")
    print()

    print("Statistics:")
    print(f"  Lines added: +{data['statistics']['lines_added']}")
    print(f"  Lines deleted: -{data['statistics']['lines_deleted']}")
    print(f"  Net change: {data['statistics']['net_lines']}")
    print()

    print("File Types:")
    for ext, count in data['file_types'].items():
        print(f"  {ext}: {count} files")
    print()

    print("Categorization:")
    for category, files in data['categorization'].items():
        if files:
            print(f"  {category.capitalize()}: {', '.join(files)}")
    print()

    print(f"Suggested commit type: {data['commit_type_suggestion']}")
    if data['scope_suggestion']:
        print(f"Suggested scope: {data['scope_suggestion']}")
```

**Output:**
```
Repository: /home/user/project
Current Branch: feature/user-auth
Total Files Changed: 5
  Staged: 5
  Unstaged: 0

Changes:
  Added: 2
    - src/auth/oauth.py
    - tests/test_oauth.py
  Modified: 3
    - src/api/routes.py
    - README.md
    - requirements.txt

Statistics:
  Lines added: +245
  Lines deleted: -67
  Net change: 178

File Types:
  .py: 4 files
  .md: 1 files
  .txt: 1 files

Categorization:
  Features: src/auth/oauth.py
  Tests: tests/test_oauth.py
  Documentation: README.md
  Dependencies: requirements.txt
  Other: src/api/routes.py

Suggested commit type: feat
Suggested scope: auth
```

**Token Usage:** ~600 tokens

---

## Example 4: Complete Feature Workflow

**Scenario:** End-to-end workflow from branch creation to PR.

```python
from skills.git_workflow_assistant.operations import (
    suggest_branch_name,
    analyze_changes,
    generate_commit_message,
    create_pull_request
)

print("🚀 Feature Development Workflow")
print("=" * 60)

# Step 1: Create feature branch
print("\n1. Creating feature branch...")
branch_result = suggest_branch_name(
    description="add payment processing",
    branch_type="feature",
    issue_number="PROJ-456"
)

if branch_result.success:
    branch_name = branch_result.data['branch_name']
    print(f"✅ Branch: {branch_name}")
    print(f"   Create with: git checkout -b {branch_name}")

# Step 2: (Make changes...)
print("\n2. Making changes...")
print("   (Developer implements feature)")

# Step 3: Analyze changes
print("\n3. Analyzing changes...")
changes_result = analyze_changes()

if changes_result.success:
    print(f"✅ {changes_result.data['total_files_changed']} files changed")
    print(f"   +{changes_result.data['statistics']['lines_added']} lines")

# Step 4: Generate commit message
print("\n4. Generating commit message...")
commit_result = generate_commit_message()

if commit_result.success:
    commit_msg = commit_result.data['commit_message']
    print(f"✅ Commit message generated:")
    print()
    for line in commit_msg.split('\n')[:3]:  # First 3 lines
        print(f"   {line}")
    print()
    print(f"   Execute: git commit -m \"{commit_msg.split(chr(10))[0]}\"")

# Step 5: Create pull request
print("\n5. Creating pull request...")
pr_result = create_pull_request(base_branch="main")

if pr_result.success:
    print(f"✅ PR ready:")
    print(f"   Title: {pr_result.data['title']}")
    print(f"   Base: {pr_result.data['base_branch']} ← {pr_result.data['head_branch']}")
    print(f"   Commits: {pr_result.data['commits_ahead']}")
    print(f"   Files: {pr_result.data['files_changed']}")

print("\n" + "=" * 60)
print("✅ Workflow complete!")
```

**Output:**
```
🚀 Feature Development Workflow
============================================================

1. Creating feature branch...
✅ Branch: feature/PROJ-456-add-payment-processing
   Create with: git checkout -b feature/PROJ-456-add-payment-processing

2. Making changes...
   (Developer implements feature)

3. Analyzing changes...
✅ 7 files changed
   +312 lines

4. Generating commit message...
✅ Commit message generated:

   feat(payment): add payment processing

   Implements Stripe integration for payments.

   Execute: git commit -m "feat(payment): add payment processing"

5. Creating pull request...
✅ PR ready:
   Title: feat(payment): Add payment processing
   Base: main ← feature/PROJ-456-add-payment-processing
   Commits: 3
   Files: 7

============================================================
✅ Workflow complete!
```

---

## Example 5: Hotfix Workflow

**Scenario:** Urgent production bug fix with expedited process.

```python
from skills.git_workflow_assistant.operations import (
    suggest_branch_name,
    generate_commit_message,
    create_pull_request
)

print("🚨 Hotfix Workflow")
print("=" * 60)

# Step 1: Create hotfix branch
print("\n1. Creating hotfix branch...")
branch = suggest_branch_name(
    description="fix critical security vulnerability",
    branch_type="hotfix",
    issue_number="SEC-789"
)

print(f"Branch: {branch.data['branch_name']}")
print(f"git checkout -b {branch.data['branch_name']}")

# Step 2: (Make fix...)
print("\n2. Applying security patch...")

# Step 3: Generate commit
print("\n3. Generating commit...")
commit = generate_commit_message(
    commit_type="fix",
    scope="security",
    breaking=False
)

print(f"Commit: {commit.data['commit_message'].split(chr(10))[0]}")

# Step 4: Expedited PR to main
print("\n4. Creating expedited PR...")
pr = create_pull_request(base_branch="main")

print(f"Title: {pr.data['title']}")
print(f"⚠️  URGENT: Review and merge ASAP")

print("\n" + "=" * 60)
```

**Output:**
```
🚨 Hotfix Workflow
============================================================

1. Creating hotfix branch...
Branch: hotfix/SEC-789-fix-critical-security-vulnerability
git checkout -b hotfix/SEC-789-fix-critical-security-vulnerability

2. Applying security patch...

3. Generating commit...
Commit: fix(security): patch critical vulnerability

4. Creating expedited PR...
Title: fix(security): Patch critical vulnerability
⚠️  URGENT: Review and merge ASAP

============================================================
```

---

## Example 6: Breaking Change Management

**Scenario:** Making breaking changes with proper documentation.

```python
from skills.git_workflow_assistant.operations import generate_commit_message

# After staging breaking API changes
result = generate_commit_message(
    commit_type="feat",
    scope="api",
    breaking=True  # Mark as breaking change
)

if result.success:
    data = result.data

    print("Breaking Change Commit:")
    print("=" * 60)
    print(data['commit_message'])
    print("=" * 60)
    print()

    if data['is_breaking']:
        print("⚠️  WARNING: This is a BREAKING CHANGE")
        print()
        print("Breaking changes detected in commit message:")
        print(data['footer'])
        print()
        print("Impact:")
        print("  - Requires version bump (major version)")
        print("  - May affect existing users/integrations")
        print("  - Needs migration guide in PR description")
```

**Output:**
```
Breaking Change Commit:
============================================================
feat(api)!: redesign authentication endpoints

Simplifies authentication flow and improves security.
Moves all auth endpoints to /v2/auth.

BREAKING CHANGE: Authentication endpoints moved from /auth to /v2/auth.
Clients must update their API calls to use the new endpoint structure.
============================================================

⚠️  WARNING: This is a BREAKING CHANGE

Breaking changes detected in commit message:
BREAKING CHANGE: Authentication endpoints moved from /auth to /v2/auth.
Clients must update their API calls to use the new endpoint structure.

Impact:
  - Requires version bump (major version)
  - May affect existing users/integrations
  - Needs migration guide in PR description
```

---

## Example 7: Multi-Strategy Branch Naming

**Scenario:** Working in teams with different branching strategies.

```python
from skills.git_workflow_assistant.operations import suggest_branch_name

description = "add user dashboard"

strategies = ["gitflow", "github-flow", "gitlab-flow"]

print("Branch Naming Across Strategies")
print("=" * 60)
print(f"Feature: {description}")
print()

for strategy in strategies:
    result = suggest_branch_name(
        description=description,
        branch_type="feature",
        strategy=strategy
    )

    if result.success:
        print(f"{strategy.upper()}:")
        print(f"  Branch: {result.data['branch_name']}")
        print(f"  Prefix: {result.data['convention']['prefix']}")
        print()
```

**Output:**
```
Branch Naming Across Strategies
============================================================
Feature: add user dashboard

GITFLOW:
  Branch: feature/add-user-dashboard
  Prefix: feature/

GITHUB-FLOW:
  Branch: add-user-dashboard
  Prefix:

GITLAB-FLOW:
  Branch: feature/add-user-dashboard
  Prefix: feature/
```

---

## Example 8: Automated Pre-Commit Hook

**Scenario:** Validate commit messages in pre-commit hook.

```python
#!/usr/bin/env python3
# .git/hooks/pre-commit

import sys
from skills.git_workflow_assistant.operations import (
    analyze_changes,
    generate_commit_message
)

def validate_commit():
    """Validate staged changes before commit."""

    print("🔍 Pre-commit validation...")

    # Analyze staged changes
    changes = analyze_changes(include_unstaged=False)

    if not changes.success:
        print(f"❌ Failed to analyze changes: {changes.error}")
        return 1

    if changes.data['files_staged'] == 0:
        print("❌ No staged changes found")
        print("   Use 'git add' to stage files")
        return 1

    # Check for common issues
    print(f"✅ {changes.data['files_staged']} files staged")

    # Warn about large changes
    if changes.data['total_files_changed'] > 20:
        print(f"⚠️  Large changeset ({changes.data['total_files_changed']} files)")
        print("   Consider splitting into smaller commits")

    # Generate suggested commit message
    commit = generate_commit_message()

    if commit.success:
        print()
        print("Suggested commit message:")
        print(commit.data['commit_message'].split('\n')[0])
        print()

    return 0

if __name__ == "__main__":
    sys.exit(validate_commit())
```

**Hook Output:**
```
🔍 Pre-commit validation...
✅ 3 files staged
⚠️  Large changeset (25 files)
   Consider splitting into smaller commits

Suggested commit message:
feat(api): add REST endpoints for user management
```

---

## Example 9: PR Description Generation

**Scenario:** Generate comprehensive PR description with all details.

```python
from skills.git_workflow_assistant.operations import create_pull_request

# Create PR with auto-generated description
result = create_pull_request(
    repo_path=".",
    base_branch="main"
)

if result.success:
    data = result.data

    print("Pull Request Preview")
    print("=" * 70)
    print(f"Title: {data['title']}")
    print(f"Base: {data['base_branch']} ← {data['head_branch']}")
    print(f"Commits: {data['commits_ahead']}")
    print(f"Files: {data['files_changed']}")
    print()
    print("Description:")
    print("-" * 70)
    print(data['body'])
    print("-" * 70)
    print()

    # Metadata
    if data['metadata']['conventional_commit']:
        print("✅ Follows conventional commits")

    if data['metadata']['breaking_changes']:
        print("⚠️  Contains breaking changes")

    if data['metadata']['has_tests']:
        print("✅ Includes tests")

    if data['metadata']['closes_issues']:
        print(f"🔗 Closes issues: {', '.join(data['metadata']['closes_issues'])}")

    print()
    print("Ready to submit:")
    print(f"  gh pr create --title \"{data['title']}\" --body \"{data['body'][:50]}...\"")
else:
    print(f"❌ Failed to create PR: {result.error}")
```

**Output:**
```
Pull Request Preview
======================================================================
Title: feat(api): Add REST endpoints for user management
Base: main ← feature/PROJ-123-add-user-api
Commits: 5
Files: 12

Description:
----------------------------------------------------------------------
## Summary

Implements RESTful API endpoints for user management operations.

## Changes
- Add user CRUD endpoints
- Implement authentication middleware
- Add request validation
- Add comprehensive tests

## Testing
- [x] Unit tests passing (45 tests)
- [x] Integration tests passing (12 tests)
- [x] Manual testing completed
- [x] Documentation updated

## Breaking Changes
None

## Related Issues
Closes #123
Refs #456
----------------------------------------------------------------------

✅ Follows conventional commits
✅ Includes tests
🔗 Closes issues: #123

Ready to submit:
  gh pr create --title "feat(api): Add REST endpoints for user management" --body "## Summary...
```

---

## Best Practices Summary

### 1. Always Analyze Before Committing
- Use `analyze_changes()` to understand what you're committing
- Review file types and categorization
- Check line counts to avoid massive commits

### 2. Use Conventional Commits
- Let `generate_commit_message()` create standardized messages
- Consistent history makes changelogs easier
- Tools can parse conventional commits

### 3. Follow Team's Branching Strategy
- Configure `strategy` parameter consistently
- Include issue numbers for traceability
- Use descriptive names

### 4. Mark Breaking Changes
- Always use `breaking=True` for incompatible changes
- Breaking changes trigger major version bumps
- Critical for library/API developers

### 5. Automate with Hooks
- Use pre-commit hooks for validation
- Generate commit messages in hooks
- Prevent bad commits early

---

## Token Efficiency Tips

**Lightweight operations:**
```python
# Branch suggestion: ~100 tokens
suggest_branch_name("add feature")

# Change analysis: ~400 tokens
analyze_changes()
```

**Standard operations:**
```python
# Commit message: ~300 tokens
generate_commit_message()

# PR creation: ~600 tokens
create_pull_request()
```

**Optimization:**
```python
# Don't include unstaged if not needed
analyze_changes(include_unstaged=False)  # Faster, fewer tokens
```

---

## Related Examples

- **pr_review_assistant/examples.md** - Reviewing PRs created by this skill
- **test_orchestrator/examples.md** - Running tests before commits
- **dependency_guardian/examples.md** - Checking dependency changes

---

*Last Updated: 2025-11-08*
