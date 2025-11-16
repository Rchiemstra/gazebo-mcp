# Documentation Directory Guide

This directory contains comprehensive documentation for the Claude Code Learning System.

---

## 📋 What's in This Directory

This directory contains **architecture documentation**, **guides**, and **implementation plans** that explain how the system works and how to use it effectively.

---

## 🔍 Using Metadata for Navigation

**Skills have YAML frontmatter** in their SKILL.md files:
```yaml
---
name: test-orchestrator
category: testing
tools: [Read, Write, Bash]
dependencies: []
---
```

**Quick skill discovery:**
```bash
# Find skills by category
grep "category: testing" ../skills/*/SKILL.md

# Find skills using specific tools
grep "tools:.*Bash" ../skills/*/SKILL.md

# Find skills with no dependencies
grep "dependencies: \[\]" ../skills/*/SKILL.md
```

**Progressive disclosure pattern:**
1. Load SKILL.md first (~200-500 tokens) - Quick overview
2. Load reference.md on demand - Complete API
3. Load examples.md as needed - Usage patterns

---

## 📁 Directory Contents

### Architecture & Design

**SDK_INTEGRATION.md**
- Python SDK integration guide
- Agent coordination patterns
- Skill invocation examples
- API reference

**ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md**
- Comprehensive improvement roadmap
- Implementation phases and progress
- Token efficiency patterns
- Progressive disclosure strategy
- Week-by-week task breakdown

### Security & Safety

**SANDBOXING_GUIDE.md**
- Filesystem isolation details
- Network access controls
- Security best practices
- Configuration examples
- Troubleshooting guide

### Weekly Summaries

**WEEK1_QUICK_WINS_SUMMARY.md**
- Week 1 accomplishments
- Token efficiency improvements
- Files created/modified
- Impact assessment
- Lessons learned

**MIGRATION_SUMMARY.md** (if exists)
- Migration guides and summaries
- Breaking changes
- Upgrade paths

---

## 🎯 Finding the Right Documentation

### For New Users

Start with these documents:

1. **`../CLAUDE.md`** (project root)
   - Overall navigation guide
   - Directory structure
   - Common patterns
   - Getting started

2. **`../README.md`** (project root)
   - Quick start guide
   - Installation instructions
   - Basic usage examples

3. **`../COMMANDS_README.md`** (project root)
   - Slash command reference
   - Command usage examples

### For Understanding the System

**Architecture:**
- `SDK_INTEGRATION.md` - How skills and agents work together
- `../skills/INTEGRATION_ARCHITECTURE.md` - Skill composition patterns

**Security:**
- `SANDBOXING_GUIDE.md` - Security boundaries and configuration

**Planning:**
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - System improvement roadmap

### For Contributing

**Before contributing, read:**

1. **`ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md`**
   - Current improvement priorities
   - Planned features
   - Implementation patterns to follow

2. **`../skills/CLAUDE.md`**
   - Skill development guidelines
   - Token efficiency patterns
   - Security best practices

3. **`SANDBOXING_GUIDE.md`**
   - Security requirements
   - Safe coding practices

### For Troubleshooting

**Issue Type → Documentation**

| Issue | Read This |
|-------|-----------|
| Setup problems | `../README.md` |
| Security/permissions | `SANDBOXING_GUIDE.md` |
| Command not working | `../COMMANDS_README.md` |
| Skill integration | `SDK_INTEGRATION.md` |
| Understanding architecture | `../skills/INTEGRATION_ARCHITECTURE.md` |
| Token usage high | `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` → Token Efficiency |

---

## 📖 Documentation Organization

### By Purpose

**Getting Started:**
- `../README.md` - First stop for new users
- `../CLAUDE.md` - Navigation and patterns
- `../COMMANDS_README.md` - Command reference

**Using the System:**
- `SDK_INTEGRATION.md` - SDK and API usage
- `../skills/CLAUDE.md` - Using skills
- `../examples/CLAUDE.md` - Learning from examples

**Understanding Internals:**
- `../skills/INTEGRATION_ARCHITECTURE.md` - How skills compose
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - System design principles

**Security:**
- `SANDBOXING_GUIDE.md` - Security model and configuration

**Progress Tracking:**
- `WEEK1_QUICK_WINS_SUMMARY.md` - Week 1 progress
- (More weekly summaries as they're created)

### By Audience

**Students/Learners:**
- `../README.md` - Get started
- `../CLAUDE.md` - Navigate the system
- `../examples/CLAUDE.md` - Learn from examples
- `../COMMANDS_README.md` - Use commands

**Developers:**
- `SDK_INTEGRATION.md` - Build with the SDK
- `../skills/CLAUDE.md` - Create/use skills
- `SANDBOXING_GUIDE.md` - Security considerations

**Contributors:**
- `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Improvement roadmap
- All architecture docs
- Weekly summaries for context

**Administrators:**
- `SANDBOXING_GUIDE.md` - Configure security
- `.claude/CLAUDE.md` - Agent configuration
- `SDK_INTEGRATION.md` - Deployment patterns

---

## 🔍 Quick Reference

### Common Questions

**"How do I get started?"**
→ `../README.md`

**"Where is the feature X?"**
→ `../CLAUDE.md` for navigation

**"How do I use skill Y?"**
→ `../skills/Y/SKILL.md` → `reference.md` → `examples.md`

**"Why is my command not working?"**
→ `../COMMANDS_README.md` or `.claude/CLAUDE.md`

**"Is this safe to run?"**
→ `SANDBOXING_GUIDE.md`

**"How do I contribute?"**
→ `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` for roadmap

**"What changed recently?"**
→ Weekly summary files (e.g., `WEEK1_QUICK_WINS_SUMMARY.md`)

### Key Concepts Explained

**Progressive Disclosure:**
- Explained in: `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` → Phase 2
- Examples in: `../skills/test_orchestrator/SKILL.md`

**Token Efficiency:**
- Explained in: `../CLAUDE.md` → Token Efficiency Patterns
- Examples in: `../skills/CLAUDE.md` → Response Formats
- Deep dive: `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` → Phase 3

**Skills Architecture:**
- Overview: `SDK_INTEGRATION.md`
- Details: `../skills/INTEGRATION_ARCHITECTURE.md`
- Usage: `../skills/CLAUDE.md`

**Security Model:**
- Complete guide: `SANDBOXING_GUIDE.md`
- Quick ref: `../CLAUDE.md` → Security & Safety

---

## 📝 Documentation Standards

### Structure

All documentation in this directory follows these standards:

**Markdown Format:**
- Clear headings (H1, H2, H3)
- Code blocks with language tags
- Tables for comparisons
- Emoji for visual markers (sparingly)

**Sections:**
- Overview/Purpose
- Quick Reference
- Detailed Content
- Examples
- Related Documentation links

**Code Examples:**
- Always include context
- Show expected output
- Include error cases
- Mark good/bad practices

### Updating Documentation

When updating docs:

1. **Update "Last Updated" date**
2. **Add to related docs** if structure changes
3. **Update implementation plan** if adding features
4. **Keep examples current** with actual code
5. **Test all code snippets** before committing

### Creating New Documentation

Use this template:

```markdown
# [Document Title]

Brief description of what this document covers.

---

## 📋 Purpose

What this document is for and who should read it.

---

## 🎯 Quick Reference

Key information at a glance.

---

## [Main Content Sections]

Detailed information organized by topic.

---

## 📖 Related Documentation

- Link to related doc 1
- Link to related doc 2

---

*Last Updated: YYYY-MM-DD*
```

---

## 🚀 Documentation Roadmap

### Planned Documentation

According to `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md`:

**Phase 6: Best Practices Integration**
- [ ] Tool permissions guide
- [ ] Workflow guide (explore-plan-code-commit, TDD, learning)
- [ ] Optimization techniques guide

**Future:**
- Migration guides (as needed)
- API changelog
- Performance tuning guide
- Advanced patterns guide

### Current Status

**Complete:**
- ✅ Root CLAUDE.md
- ✅ Skills CLAUDE.md
- ✅ Examples CLAUDE.md
- ✅ .claude CLAUDE.md
- ✅ Docs CLAUDE.md (this file)
- ✅ Sandboxing guide
- ✅ Implementation plan
- ✅ Week 1 summary

**In Progress:**
- 🔄 Tests CLAUDE.md
- 🔄 Weekly summaries
- 🔄 Skill SKILL.md files (2/24 complete)

**Planned:**
- 📅 Tool permissions guide
- 📅 Workflow guide
- 📅 Optimization guide

---

## 💡 Tips for Reading Documentation

### Efficient Documentation Navigation

**1. Start Broad, Go Deep:**
```
README.md → CLAUDE.md → Specific guides
```

**2. Use Search:**
```bash
# Find all mentions of "token efficiency"
grep -r "token efficiency" docs/ README.md CLAUDE.md
```

**3. Follow Cross-References:**
- Links to related docs are always at the end
- Related sections reference each other

**4. Check Last Updated:**
- Newer docs reflect current best practices
- Check implementation plan for future changes

### Understanding Examples

All code examples follow this pattern:

```python
# ❌ INEFFICIENT or wrong way
bad_example()

# ✅ EFFICIENT or correct way
good_example()

# Output or explanation
"""
Expected result
"""
```

### Getting Help

1. **Check relevant CLAUDE.md** for navigation
2. **Read related docs** for context
3. **Try examples** to understand
4. **Use `/ask-specialist`** for specific questions
5. **Consult implementation plan** for future features

---

## 🔐 Security & Documentation Safety

### Reading Documentation Safely

Documentation files are safe to read, but be aware of:

**Code Examples:**
- Documentation contains code examples for illustration
- Review examples before running them
- Check sandboxing requirements
- Verify file paths and permissions

**Configuration Examples:**
- Tool allowlisting configs in SANDBOXING_GUIDE.md
- Network access configs
- Security settings
- Test examples in safe, isolated contexts first

### Security Documentation

**Primary Security Resources:**
- `SANDBOXING_GUIDE.md` - Complete security model
- `../CLAUDE.md` → Security & Safety section
- `../skills/CLAUDE.md` → Security & Safety section
- `.claude/CLAUDE.md` → Security & Safety section

**Key Security Concepts:**
1. **Filesystem Sandboxing** - Project directory isolation
2. **Network Controls** - Domain allowlisting
3. **Tool Permissions** - Granular tool access
4. **Agent Tool Access** - Minimal necessary permissions

### Implementation Plan Security

`ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` includes:
- Security phases and milestones
- Security best practices integration
- Skill security auditing framework
- Safe implementation patterns

**When Implementing from Plan:**
- Review security implications of each phase
- Check skill security requirements
- Test in sandboxed environment first
- Validate tool permissions needed

### Documentation for Security Features

**Security Features Documented:**
- Sandboxing configuration (`SANDBOXING_GUIDE.md`)
- Tool allowlisting patterns (`.claude/CLAUDE.md`)
- Safe skill usage (`skills/CLAUDE.md`)
- Network security (`SANDBOXING_GUIDE.md`)
- Agent security (`.claude/CLAUDE.md`)

**Security Checklists:**
- Before running examples
- Before enabling new tools
- Before adding network access
- Before creating custom agents

See `SANDBOXING_GUIDE.md` for complete security documentation.

---

## 📚 Complete Documentation Map

```
project-root/
├── README.md                 # Quick start
├── CLAUDE.md                # Navigation guide
├── COMMANDS_README.md       # Command reference
├── .claude/
│   └── CLAUDE.md           # Agent configuration
├── skills/
│   ├── CLAUDE.md           # Skills usage guide
│   ├── INTEGRATION_ARCHITECTURE.md
│   └── */
│       ├── SKILL.md        # Progressive disclosure entry
│       ├── reference.md    # Detailed API docs
│       └── examples.md     # Usage examples
├── examples/
│   └── CLAUDE.md           # Examples guide
├── tests/
│   └── CLAUDE.md           # Testing guide (planned)
└── docs/                    # You are here!
    ├── CLAUDE.md           # This file
    ├── SANDBOXING_GUIDE.md
    ├── SDK_INTEGRATION.md
    ├── ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md
    └── WEEK1_QUICK_WINS_SUMMARY.md
```

---

## 🎓 Learning Path Through Documentation

### Week 1: Getting Started
1. `../README.md` - Install and run
2. `../CLAUDE.md` - Understand structure
3. `../COMMANDS_README.md` - Try commands
4. `../examples/CLAUDE.md` - Run examples

### Week 2: Understanding Skills
1. `../skills/CLAUDE.md` - Skills overview
2. `../skills/test_orchestrator/SKILL.md` - First skill
3. `../skills/test_orchestrator/examples.md` - Try examples
4. `SDK_INTEGRATION.md` - How skills work

### Week 3: Advanced Usage
1. `ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Design principles
2. `../skills/code_analysis/SKILL.md` - Advanced skill
3. `SANDBOXING_GUIDE.md` - Security model
4. `../skills/INTEGRATION_ARCHITECTURE.md` - Composition

### Week 4: Contributing
1. All architecture docs
2. Weekly summaries for context
3. Implementation plan for roadmap
4. Create your first skill/agent

---

## 🔗 External Resources

### Anthropic Blog Posts

The implementation plan references these articles:

1. [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
2. [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
3. [Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
4. [Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
5. [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
6. [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

### Community

- GitHub Issues: Report bugs, request features
- Discussions: Ask questions, share patterns

---

**Remember:** Documentation is a map, not the territory. The best way to learn is to read the docs, try the examples, and build something! 🚀

*Last Updated: 2025-11-08*
