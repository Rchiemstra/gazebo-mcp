# Anthropic Engineering Insights

This document contains comprehensive insights and best practices from Anthropic's engineering blog (https://www.anthropic.com/engineering), saved for offline reference.

**Last Updated:** 2025-11-11
**Total Articles:** 14

---

## Table of Contents

### Core Concepts
1. [Building Effective Agents](#building-effective-agents)
2. [Effective Context Engineering](#effective-context-engineering)
3. [Agent Skills](#agent-skills)
4. [Code Execution with MCP](#code-execution-with-mcp)

### Development Tools & Practices
5. [Claude Agent SDK](#claude-agent-sdk)
6. [Writing Effective Tools](#writing-effective-tools)
7. [Claude Code Best Practices](#claude-code-best-practices)
8. [The "Think" Tool](#the-think-tool)

### Security & Infrastructure
9. [Claude Code Sandboxing](#claude-code-sandboxing)
10. [Desktop Extensions](#desktop-extensions)
11. [Infrastructure Postmortem](#infrastructure-postmortem)

### Advanced Topics
12. [Multi-Agent Research Systems](#multi-agent-research-systems)
13. [Contextual Retrieval](#contextual-retrieval)
14. [SWE-Bench Performance](#swe-bench-performance)

### Summary
15. [Key Takeaways](#key-takeaways)

---

## Building Effective Agents

### Core Philosophy

Successful AI agent implementations prioritize **simplicity over complexity**. Anthropic distinguishes between:
- **Workflows:** Predefined execution paths
- **Agents:** LLM-directed processes with dynamic tool usage

**Key Quote:** "Success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs."

**Principle:** Complexity should only increase when simpler solutions demonstrably underperform.

### Essential Architectural Patterns

#### Foundation: The Augmented LLM

The basic building block enhances language models with:
- Retrieval capabilities
- Tools
- Memory systems

**Recommendation:** Use the Model Context Protocol for streamlined integration with third-party tools.

#### Key Workflow Patterns

**1. Prompt Chaining**
- Decomposes tasks into sequential steps
- Each LLM call builds on previous outputs
- Ideal for decomposable problems like content generation followed by translation

**2. Routing**
- Classifies inputs and directs them to specialized handlers
- Enables optimized prompts for distinct categories
- Example: Different customer support query types

**3. Parallelization**
- Runs tasks simultaneously through:
  - **Sectioning:** Independent subtasks
  - **Voting:** Multiple attempts
- Particularly effective for safety-critical evaluations

**4. Orchestrator-Workers**
- A central LLM dynamically breaks down complex tasks
- Delegates to worker instances
- Ideal for unpredictable problem decomposition like multi-file code changes

**5. Evaluator-Optimizer**
- Implements iterative refinement loops
- Evaluation drives improvement
- Mimics human editorial processes

#### Autonomous Agents

True agents operate independently using environmental feedback loops. Requirements:
- "Ground truth" validation at each step (test results, execution outputs)
- Stopping conditions
- Human checkpoints

### Implementation Guidance

**Framework Approach:**
- Start with direct LLM API calls rather than complex frameworks
- If frameworks are used, developers must understand underlying mechanics to avoid common implementation errors

**Three Core Principles:**
1. Maintain simplicity in design
2. Prioritize transparency through explicit planning visualization
3. Carefully craft agent-computer interfaces with thorough tool documentation

### Tool Design Best Practices

Tool specifications deserve equal prompt engineering attention as overall prompts.

**Recommendations:**
- Provide sufficient context for model reasoning
- Maintain natural formatting similar to internet text
- Eliminate unnecessary overhead (line counting, string escaping)
- Invest in agent-computer interfaces as heavily as human-computer interfaces
- Comprehensive testing to identify usage mistakes
- Implement "poka-yoke" principles to reduce error potential

### Practical Applications

**Customer Support:**
- Natural fit for agents combining conversation with tool integration
- Data retrieval and transaction processing

**Software Development:**
- Agents excel at code problems with verifiable solutions
- Automated test feedback
- Demonstrates real GitHub issue resolution capabilities

---

## Effective Context Engineering

### Core Concept

**Definition:** "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

This evolved from earlier prompt engineering practices as agents became more sophisticated. While prompt engineering focuses on writing effective instructions, context engineering addresses the broader challenge of managing all information flowing to a model across multiple inference turns.

### Why Context Matters

**Context Rot:** Research shows "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."

This stems from the transformer architecture's computational constraints—every token must attend to every other token, creating n² relationships.

### Components of Effective Context

**System Prompts:**
- Should achieve the "right altitude"
- Specific enough to guide behavior effectively
- Flexible enough to avoid brittle, hardcoded logic

**Tools:**
- Must be minimal, non-overlapping, and clearly defined
- Encourage efficient agent behavior
- Reduce token waste

**Examples:**
- Provide canonical, diverse instances of desired behavior
- Rather than exhaustive edge-case lists

### Runtime Strategies

**Just-in-Time Approach:**
- Maintains lightweight identifiers
- Dynamically loads data using tools
- Mirrors human cognition
- Contrasts with pre-computing all relevant information upfront

### Long-Horizon Solutions

For extended tasks exceeding context windows:

**1. Compaction**
- Summarizing conversations
- Restarting with compressed context

**2. Structured Note-Taking**
- Agents maintain persistent memory files
- Outside the context window

**3. Sub-Agent Architectures**
- Specialized agents handle focused tasks
- Return only distilled summaries

### Fundamental Principle

**Core Guidance:** "Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

This principle guides all context curation decisions.

---

## Agent Skills

### Overview

Agent Skills are modular capabilities that extend Claude's functionality through organized directories containing instructions, scripts, and resources.

**Key Concept:** "Skills extend Claude's capabilities by packaging your expertise into composable resources for Claude, transforming general-purpose agents into specialized agents that fit your needs."

### Core Architecture

#### SKILL.md Structure

Each skill requires a `SKILL.md` file with YAML frontmatter containing metadata (`name` and `description`).

**At startup:** "The agent pre-loads the name and description of every installed skill into its system prompt."

#### Progressive Disclosure Model

Skills use a layered information architecture:

1. **First Level:** Metadata in system prompt (name and description)
2. **Second Level:** Full SKILL.md content loaded when relevant
3. **Third Level and Beyond:** Additional bundled files (reference.md, forms.md) that Claude accesses contextually

**Purpose:** Prevents excessive context consumption while maintaining flexibility.

### Implementation Approach

#### File Organization

Skills bundle related documentation and resources as references within the skill directory. The PDF skill example demonstrates this: separate files for general references and form-filling instructions keep the core SKILL.md lean.

#### Code Execution

Skills can include executable scripts (Python, Bash) that Claude runs deterministically. "Claude can run this script without loading either the script or the PDF into context."

### Best Practices for Development

1. **Start with evaluation:** Identify capability gaps through testing before building skills
2. **Structure for scale:** Split unwieldy SKILL.md files into separate references to reduce token usage
3. **Think from Claude's perspective:** Monitor real usage patterns and iterate based on skill triggering behavior
4. **Iterate with Claude:** Collaborate with Claude to capture successful patterns directly into reusable skill components

### Security Considerations

**Warning:** "Install skills only from trusted sources. When installing a skill from a less-trusted source, thoroughly audit it before use."

Pay particular attention to:
- Code dependencies
- Instructions directing external network connections

### Availability

Agent Skills are supported across:
- Claude.ai
- Claude Code
- Claude Agent SDK
- Claude Developer Platform

---

## Code Execution with MCP

### Overview

Code execution environments can dramatically improve AI agent efficiency when working with the Model Context Protocol (MCP). This approach reduces token consumption by up to **98.7%** compared to traditional direct tool-calling methods.

### Core Problems Addressed

**1. Tool Definition Overload**
- Conventional MCP implementations load all tool definitions directly into the model's context window upfront
- This creates excessive token consumption before the model even processes user requests
- "Tool descriptions occupy more context window space, increasing response time and costs"

**2. Intermediate Result Bloat**
- When agents retrieve data for intermediate steps, results must flow through the model context repeatedly
- A 2-hour meeting transcript could add 50,000 tokens per operation
- Extremely large documents may exceed context window limits entirely

### Solution: Filesystem-Based Tool APIs

Rather than exposing tools as direct calls, the architecture presents MCP servers as code APIs through a filesystem structure:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
```

Agents discover and load only necessary tool definitions by exploring the filesystem, reducing token usage from **150,000 to 2,000 tokens** for comparable tasks.

### Key Benefits

**Progressive Disclosure**
- Models excel at filesystem navigation
- Enables on-demand tool definition loading rather than upfront exposure to all available tools

**Context-Efficient Data Processing**
- Filtering and transformation occur in the execution environment
- "The agent sees five rows instead of 10,000"
- Similar patterns work for aggregations, joins across multiple data sources, or extracting specific fields

**Privacy Preservation**
- Sensitive data can flow through workflows without entering the model's context
- The MCP client can tokenize personally identifiable information automatically
- Allows real data to transfer between services while remaining hidden from the model

**Improved Control Flow**
- Loops, conditionals, and error handling use native programming patterns
- Rather than chaining individual tool calls
- Reduces latency and improves efficiency

**State Persistence and Skills**
- Agents can save intermediate results and reusable code functions
- Enables progressive capability development and resumable workflows

### Implementation Considerations

**Security Warning:**
"Running agent-generated code requires a secure execution environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add operational overhead and security considerations that direct tool calls avoid."

**Trade-offs:**
Developers must weigh:
- ✅ Token savings
- ✅ Latency improvements
- ✅ Better tool composition
- ❌ Sandbox infrastructure costs
- ❌ Security requirements

### Community Impact

Cloudflare independently published similar findings using the term "Code Mode," validating the approach's effectiveness across implementations.

---

## Claude Agent SDK

### Core Concept

The Claude Agent SDK empowers developers to build autonomous agents by providing Claude access to a computer environment.

**Fundamental Principle:** "Give your agents a computer, allowing them to work like humans do."

### Architecture & Design Loop

The SDK operates on a four-stage feedback mechanism:

1. **Gather Context** - Agents retrieve and understand relevant information
2. **Take Action** - Agents execute tasks using available tools
3. **Verify Work** - Agents evaluate and validate outputs
4. **Repeat** - Continuous improvement through iteration

### Key Capabilities for Context Management

**Agentic Search & File Systems:**
- The folder structure becomes an organization layer
- Agents intelligently use bash commands like `grep` and `tail` to load pertinent information
- Rather than entire files

**Semantic Search:**
- Faster than agentic search but less transparent
- Uses vector embeddings
- Recommended only when performance becomes critical

**Subagents:**
- Enable parallel task execution
- Isolated context windows
- Prevents bloat when processing large datasets

**Compaction:**
- Automatically summarizes conversation history
- When approaching context limits

### Action Mechanisms

**Tools:**
- Primary actions developers should define
- Prominently featured in the agent's decision-making

**Bash Scripts:**
- Flexible general-purpose command execution
- For complex digital workflows

**Code Generation:**
- Ideal for tasks requiring precision
- Composability and reusability

**MCPs (Model Context Protocol):**
- Standardized integrations
- Handling authentication automatically

### Verification Strategies

**Rules-Based Feedback:**
- Provides explicit rules
- Identifies violations (e.g., code linting with TypeScript)

**Visual Feedback:**
- Screenshots and renders
- Enable agents to verify layout, styling, and responsiveness

**LLM-as-Judge:**
- Secondary models evaluate outputs against fuzzy criteria
- Useful but resource-intensive

### Agent Improvement Framework

Developers should evaluate:
- Does the agent have correct tools?
- Can search APIs be restructured?
- Should formal validation rules be added?
- Are additional creative tools needed?
- Does performance require programmatic evaluation testing?

### Getting Started

Documentation at `docs.claude.com/en/api/agent-sdk/overview` provides implementation guidance, with migration guides for existing SDK users.

---

## Writing Effective Tools

### Overview

"Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."

### Core Development Process

**Three-Phase Workflow:**

**1. Prototyping**
- Start with quick tool implementations using Claude Code
- Leverage LLM-friendly documentation
- Test locally before deployment

**2. Evaluation**
- Create real-world evaluation tasks requiring multiple tool calls
- Run these programmatically
- Collect metrics beyond accuracy:
  - Runtime
  - Token consumption
  - Error rates

**3. Optimization**
- Use agents to analyze evaluation results
- Iteratively improve tool implementations
- Based on agent feedback patterns

### Five Design Principles

**1. Choosing the Right Tools**
- Avoid simply wrapping existing APIs
- Design tools matching agent affordances
- Constrained context favors search over list operations
- Consolidate frequently chained operations into single tools

**2. Namespacing**
- Group related tools using consistent prefixes
  - Example: `asana_search`, `asana_projects_search`
- Reduces context load
- Helps agents select appropriate tools

**3. Meaningful Context Returns**
- Prioritize "name" and "image_url" over technical identifiers like UUIDs
- Semantic language reduces hallucinations
- Offer flexible response formats via `response_format` parameters:
  - Detailed outputs
  - Concise outputs

**4. Token Efficiency**
- Implement pagination, filtering, and truncation
- With sensible defaults
- Use helpful error messages guiding agents toward better strategies
- Rather than opaque codes

**5. Tool Descriptions**
- Refine specifications precisely
- Even small improvements significantly boost performance
- Be explicit about:
  - Query formats
  - Niche terminology
  - Resource relationships

### Results

Internal testing showed Claude-optimized tools substantially outperformed manually written versions on held-out test sets for both Slack and Asana integrations.

---

## Claude Code Best Practices

### Customization & Setup

**CLAUDE.md Files:**
- Special configuration files that Claude automatically incorporates into conversations
- Should document:
  - Bash commands
  - Code style guidelines
  - Testing instructions
  - Repository-specific information
- Can be placed at:
  - Project root
  - Parent/child directories
  - Home folders for global application

### Tool Integration

Claude Code can leverage:
- Bash tools
- MCP (Model Context Protocol) servers
- Custom slash commands

**Slash Commands:**
- Document custom tools
- Store prompt templates as Markdown files in `.claude/commands` folders
- Accessible to teams through slash command menus

### Effective Workflows

**1. Explore-Plan-Code-Commit**
- Ask Claude to read files first
- Create a detailed plan (using extended thinking modes like "think" or "ultrathink")
- Then implement and commit changes
- Initial research prevents premature coding

**2. Test-Driven Development**
- Have Claude write tests based on expected inputs/outputs
- Confirm they fail
- Then iteratively code solutions that pass tests
- Provides clear evaluation targets

**3. Visual Iteration**
- Provide design mocks or enable screenshots
- Allow Claude to implement and refine designs
- Through multiple iterations until they match visual targets

**4. Safe YOLO Mode**
- Use `--dangerously-skip-permissions` in isolated containers
- For autonomous work on lint fixes or boilerplate generation
- Requires careful safety considerations

### Optimization Techniques

- Provide specific, detailed instructions rather than vague requests
- Include images, diagrams, and screenshots for visual reference
- Use file path mentions via tab-completion for precise context
- Provide URLs alongside prompts for Claude to fetch relevant documentation
- Interrupt and redirect Claude early using Escape to preserve context
- Clear context frequently with `/clear` to maintain performance

### Advanced Patterns

**Parallel Claude Instances:**
- Multiple Claude instances running in parallel
- Can provide effective code reviews and verification

**Git Worktrees:**
- Enable simultaneous work on independent tasks
- Without merge conflicts

### Infrastructure Automation

**Headless Mode:**
- Use `-p` flag for non-interactive usage
- Enables CI/CD pipelines, issue triage, and automated code reviews
- Beyond traditional linting capabilities

### Philosophy

The guidance emphasizes that Claude Code's low-level, unopinionated design requires experimentation to discover effective team-specific workflows, but these patterns provide evidence-based starting points from Anthropic's internal usage.

---

## The "Think" Tool

### Overview

The "think" tool gives Claude dedicated space for reasoning during complex tasks.

**Key Difference:** Unlike extended thinking (which occurs before response generation), the "think" tool allows Claude to "stop and think about whether it has all the information it needs to move forward" during active tool use.

### When to Use

**Think Tool:**
- For scenarios where Claude must process external information from tool results
- Reasoning is more focused on newly discovered information
- Rather than comprehensive pre-planning
- Excels in "long chains of tool calls" requiring careful analysis

**Extended Thinking:**
- Works better for simpler scenarios
- Comprehensive pre-planning before action

### Performance Results

**τ-Bench (customer service benchmark):**

- **Airline domain:** With optimized prompting, achieved 0.570 performance versus 0.370 baseline—**54% relative improvement**
- **Retail domain:** Achieved 0.812 without additional prompting versus 0.783 baseline
- **SWE-Bench:** Contributed to state-of-the-art 0.623 score with **1.6% average performance gains**

### Best Use Cases

The tool benefits scenarios involving:
1. Tool output analysis before taking action
2. Policy-heavy environments requiring compliance verification
3. Sequential decisions where errors carry consequences

### Implementation Guidance

**Key Finding:** Providing "domain-specific examples" through strategic prompting yielded the strongest results.

**Best Practice:** Complex instructions work better in system prompts than tool descriptions alone.

### When Not to Use

The tool offers no advantage for:
- Non-sequential tool calls
- Simple instruction-following tasks

---

## Claude Code Sandboxing

### Overview

Anthropic introduced sandboxing features that reduce permission prompts by **84%** while maintaining robust security. The approach uses operating system-level protections to define work boundaries.

### Key Security Features

**Filesystem Isolation:**
- Claude gains read/write access only to the current working directory
- System blocks modifications to files outside designated areas
- Prevents "prompt-injected Claude from modifying sensitive system files"

**Network Isolation:**
- Internet access routes through a proxy server outside the sandbox
- Enforces domain restrictions
- Prevents compromised agents from:
  - Exfiltrating sensitive data like SSH keys
  - Downloading malware

### Technical Implementation

The sandboxing relies on OS-level primitives:
- **Linux:** Bubblewrap container technology
- **macOS:** Seatbelt restrictions

**Critical Requirement:** Both filesystem and network isolation are required together.
- Without network isolation: Sensitive files could be stolen
- Without filesystem isolation: Agents could escape the sandbox entirely

### Practical Applications

**Sandboxed Bash Tool:**
- Claude executes commands within defined limits
- Without repeated permission prompts
- Attempts to access restricted resources trigger immediate user notifications

**Claude Code on the Web:**
- Sessions run in isolated cloud sandboxes
- Credentials remain external
- Custom proxy handles Git interactions
- Validates authentication
- Prevents unauthorized repository pushes

### Getting Started

- Run `/sandbox` in Claude and review configuration documentation
- Access Claude Code on the web at claude.com/code
- Developers can integrate the open-sourced sandbox runtime into custom agents

---

## Desktop Extensions

### Overview

Desktop Extensions (`.mcpb` files) dramatically simplify how users install Model Context Protocol (MCP) servers in Claude Desktop.

### The Problem Solved

**Before Desktop Extensions, installation required:**
- External runtime installation (Node.js, Python)
- Manual JSON configuration editing
- Package dependency conflict resolution
- GitHub searching to discover servers
- Manual reinstallation for updates

### How It Works

**New Process:**
1. Download a `.mcpb` file
2. Double-click
3. Click "Install"
4. Done

### Technical Structure

A Desktop Extension is essentially a ZIP archive containing:
- `manifest.json` (required) - metadata and configuration
- `server/` directory - MCP server code
- `dependencies/` - bundled packages
- Optional icon and documentation

### Key Architecture Features

**Built-in Benefits:**
- Node.js runtime included with Claude Desktop
- Automatic security updates
- OS keychain storage for sensitive credentials
- User-friendly configuration interface
- Cross-platform support (Windows, macOS, Linux)

### Building Extensions

**Three Simple Commands:**
```bash
npx @anthropic-ai/mcpb init
npx @anthropic-ai/mcpb pack
```

The manifest supports declaring user configuration needs, which Claude Desktop collects securely and injects as environment variables or arguments.

### Open Ecosystem

Anthropic open-sourced:
- Complete specification
- Toolchain
- Reference implementations

Enabling broader AI application adoption beyond Claude Desktop.

---

## Infrastructure Postmortem

### Summary

Between August and early September 2025, three separate infrastructure bugs degraded Claude's response quality. Anthropic resolved these issues and published a detailed technical postmortem.

### The Three Bugs

**1. Context Window Routing Error (August 5)**
- Short-context requests mistakenly directed to servers configured for the upcoming 1M token context window
- Initially affecting 0.8% of Sonnet 4 requests
- Load balancing adjustment on August 29 escalated this to 16% during peak impact
- Approximately 30% of Claude Code users experienced at least one misdirected message
- "Sticky" routing meant subsequent requests followed the same incorrect path

**Resolution:** Fixed routing logic on September 4, with full rollout completed by September 18.

**2. Output Corruption (August 25)**
- TPU server misconfiguration caused token generation errors
- Occasionally assigned high probability to contextually inappropriate tokens
- Users reported unexpected Thai or Chinese characters appearing in English responses
- Syntax errors in code outputs

**Affected:** Opus 4.1, Opus 4, and Sonnet 4 between August 25-September 2.

**Resolution:** Issue identified and rolled back September 2; added detection tests for unexpected character outputs.

**3. Approximate Top-K XLA:TPU Miscompilation (August 25)**
- Code deployment triggered a latent compiler bug
- Affected token selection during text generation
- Manifested inconsistently depending on batch sizes and model configurations
- Made reproduction difficult

**Affected:** Claude Haiku 3.5, potentially Sonnet 4 and Opus 3.

**Resolution:** Switched from approximate to exact top-k selection, accepting minor efficiency costs to guarantee quality.

### Root Cause: Precision Mismatch

**Technical Issue:**
- Models compute probabilities in bf16 (16-bit)
- Vector processor operates natively in fp32 (32-bit)
- Precision mismatch caused operations to disagree on highest-probability tokens
- Sometimes eliminating the correct token entirely

**History:** A December 2024 workaround had inadvertently masked this underlying compiler bug until the August fix attempt exposed it more severely.

### Detection Challenges

Anthropic identified three critical gaps:

1. **Evaluation Gap:** "The evaluations we ran simply didn't capture the degradation users were reporting" due to Claude's resilience in recovering from isolated errors
2. **Privacy Constraints:** Limited engineer access to unreported user interactions prevented bug reproduction
3. **Platform Fragmentation:** Multiple platforms experiencing different symptoms at different rates created confusing, contradictory feedback

### Improvements Implemented

1. **Enhanced evaluations** better differentiating working from broken implementations
2. **Continuous production monitoring** rather than periodic testing
3. **Improved debugging tools** for community-sourced feedback while maintaining privacy
4. **User feedback integration** as critical signal for quality issues

**User Action:** Continue reporting problems via the `/bug` command in Claude Code or the thumbs-down button in Claude apps.

---

## Multi-Agent Research Systems

### System Overview

Anthropic's Research feature implements an **orchestrator-worker pattern** where a lead agent coordinates specialized subagents operating in parallel.

**Workflow:**
- User submits queries
- Lead agent analyzes requirements and develops strategy
- Spawns subagents to explore different aspects simultaneously

### Key Architecture Components

**Multi-step Dynamic Search:**
- Replaces traditional static retrieval
- "Dynamically finds relevant information, adapts to new findings, and analyzes results"
- Through iterative agent exploration

**Complete Workflow:**
- LeadResearcher planning approach and persisting context to memory
- Specialized subagents performing independent web searches
- Extended thinking and interleaved thinking for evaluation
- CitationAgent ensuring proper attribution
- Results returned with verified citations

### Performance Advantages

**Key Finding:** "A multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by **90.2%**."

**Analysis:** Token usage explains 80% of performance variance, with tool calls and model choice as secondary factors.

**Trade-offs:**
- Agents use approximately **4× more tokens** than chat
- Multi-agent systems use **~15× more tokens** than conversations

### Eight Core Prompting Principles

**1. Think like your agents**
- Build simulations to observe step-by-step behavior
- Identify failure modes

**2. Teach delegation**
- Provide subagents with:
  - Clear objectives
  - Output formats
  - Tool guidance
  - Task boundaries

**3. Scale effort appropriately**
- Embed scaling rules:
  - Simple queries: 1 agent (3-10 calls)
  - Complex research: 10+ subagents

**4. Design tools critically**
- Poor tool descriptions derail agents
- Each tool needs distinct purpose and clear documentation

**5. Enable self-improvement**
- Claude models can diagnose failures
- Suggest prompt refinements

**6. Start broad, then narrow**
- Begin with short, general queries
- Progressively focus

**7. Guide thinking processes**
- Use extended thinking for planning
- Interleaved thinking for adaptation

**8. Parallelize execution**
- Spin up 3-5 subagents and 3+ tools simultaneously
- Reduces research time by **90%**

### Evaluation Strategies

**Start Small Immediately:**
- With 20 test queries representing actual usage
- "A prompt tweak might boost success rates from 30% to 80%"
- Early changes have dramatic impact

**LLM-as-Judge Evaluation:**
- Scalable for free-form outputs
- Single LLM calls scoring against rubric criteria:
  - Factual accuracy
  - Citations
  - Completeness
  - Source quality
  - Tool efficiency
- Aligns well with human judgment

**Human Testing:**
- Catches automation gaps
- Edge cases, hallucinations, and subtle biases
- Example: Preferring "SEO-optimized content farms over authoritative but less highly-ranked sources"

### Production Reliability Challenges

**Stateful Error Propagation:**
- Minor failures cascade unpredictably
- Systems require:
  - Durable execution
  - Error handling
  - Resumption capabilities
  - Deterministic safeguards like retry logic and checkpoints

**Non-Deterministic Debugging:**
- Agents make dynamic decisions differently each run
- Full production tracing needed of "decision patterns and interaction structures"
- Without monitoring conversation contents (maintains privacy)

**Deployment Complexity:**
- Rainbow deployments gradually shift traffic between versions
- Prevents disruption to running agents

**Synchronous Bottlenecks:**
- Currently, lead agents wait for subagent completion before proceeding
- Asynchronous execution could improve parallelism
- But adds coordination complexity

### Real-World Impact

**User Reports:**
- Find business opportunities they hadn't considered
- Navigate complex healthcare options
- Resolve technical bugs
- Save up to days of work by uncovering research connections

**Top Use Cases:**
- Developing specialized software systems (10%)
- Optimizing professional content (8%)
- Generating growth strategies (8%)
- Supporting academic research (7%)
- Verifying organizational information (5%)

---

## Contextual Retrieval

### Core Problem

AI models need background knowledge to function effectively in specific contexts. Traditional Retrieval-Augmented Generation (RAG) systems struggle because they "remove context when encoding information, which often results in the system failing to retrieve the relevant information."

### The Solution: Contextual Retrieval

Anthropic's approach combines two techniques to dramatically improve knowledge retrieval:

**Contextual Embeddings & Contextual BM25** work by prepending explanatory context to each data chunk before processing. This transforms isolated snippets into meaningful segments with surrounding context.

### Performance Gains

- Contextual Embeddings alone: **35% reduction** in retrieval failures
- Combined with BM25: **49% reduction** in failures
- Adding reranking: **67% total improvement**

### Implementation Method

Rather than manual annotation, Claude generates contextual explanations automatically.

**Prompt:** Instructs the model to provide "short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval."

### Cost Efficiency

Using prompt caching with Claude, contextualization costs approximately **$1.02 per million document tokens**—making it economically viable even for massive knowledge bases.

### Key Findings

The research demonstrates that combining:
- Gemini or Voyage embeddings
- Contextual BM25
- Reranking
- Retrieving the top 20 chunks

Yields optimal performance across diverse knowledge domains.

---

## SWE-Bench Performance

### Achievement

Claude 3.5 Sonnet achieved **49% on SWE-bench Verified**, a software engineering evaluation, beating the previous state-of-the-art model's 45%.

### Benchmark Overview

SWE-bench evaluates AI models on real-world software engineering tasks from open-source Python repositories. Rather than testing isolated models, it assesses complete "agent" systems combining language models with scaffolding that generates prompts, parses outputs, and manages interaction loops.

### Agent Architecture

**The optimized agent uses:**

**Bash Tool:**
- Executes commands
- With detailed error-handling instructions

**Edit Tool:**
- Views, creates, and modifies files
- Using string-replacement matching

**Minimal Scaffolding:**
- "Give as much control as possible to the language model itself"

### Key Implementation Strategy

**Critical Insight:** "Much more attention should go into designing tool interfaces for models, in the same way that a large amount of attention goes into designing tool interfaces for humans."

**Error-Proofing:**
- Requiring absolute file paths
- Ensuring single-match string replacements

### Performance Comparison

| Model | SWE-Bench Score |
|-------|-----------------|
| Claude 3.5 Sonnet (new) | 49% |
| Previous SOTA | 45% |
| Claude 3.5 Sonnet (old) | 33% |
| Claude 3 Opus | 22% |

### Notable Challenges

- High token costs (often >100k tokens per task)
- Grading complexity and environment setup issues
- Hidden test mismatches where solutions work but don't match original unit tests
- Limited multimodal capabilities for visualization-heavy tasks

---

## Key Takeaways

### Context Management
1. **Context is finite** - Treat it as a critical resource requiring careful curation
2. **Progressive disclosure** - Load information on-demand, not all upfront
3. **Token efficiency** - Use code execution and local filtering to achieve 95-99% token savings
4. **Just-in-time loading** - Maintain lightweight identifiers and dynamically load data using tools
5. **Context rot** - As token count increases, model's ability to recall decreases

### Agent Architecture
1. **Start simple** - Direct API calls before complex frameworks
2. **Composable patterns** - Build with well-understood workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
3. **Transparency** - Make planning and decision-making visible
4. **Ground truth** - Validate with real execution outputs, not just LLM responses
5. **Four-stage loop** - Gather context → Take action → Verify work → Repeat

### Skills & Tools
1. **Modular design** - Package expertise into reusable components
2. **Layered information** - Use YAML metadata + progressive file loading
3. **Security first** - Audit all skills, especially code and network access
4. **Tool documentation** - Invest as much in tool specs as prompts
5. **Five tool principles** - Right tools, namespacing, meaningful context, token efficiency, precise descriptions
6. **Agent-optimized tools** - Design for agent affordances, not just API wrappers

### Code Execution
1. **Filesystem-based APIs** - Present tools as navigable code structures (150K → 2K tokens)
2. **Data processing** - Filter and transform outside the model context
3. **Privacy** - Keep sensitive data in execution environment
4. **State persistence** - Enable resumable workflows and skill development
5. **Sandboxing required** - Filesystem + network isolation together

### Multi-Agent Systems
1. **Orchestrator-worker pattern** - Lead agent coordinates specialized subagents in parallel
2. **Token trade-off** - 15× more tokens but 90.2% better performance
3. **Eight principles** - Think like agents, teach delegation, scale effort, design tools critically, enable self-improvement, start broad, guide thinking, parallelize
4. **Start small** - 20 test queries can reveal 30% → 80% improvement opportunities
5. **Durable execution** - Error handling, resumption, checkpoints for production reliability

### Evaluation & Iteration
1. **Test-driven development** - Identify gaps through evaluation first
2. **Monitor patterns** - Watch how agents actually use tools/skills
3. **Iterate with Claude** - Collaborate to capture successful patterns
4. **Measure performance** - Track token usage, latency, success rates
5. **Three-phase process** - Prototype → Evaluate → Optimize
6. **LLM-as-judge** - Scalable evaluation for free-form outputs
7. **Human validation** - Catches edge cases and subtle biases

### Workflows & Best Practices
1. **Explore-plan-code-commit** - Research first, plan with extended thinking, then implement
2. **Test-driven development** - Write failing tests first, then implement solutions
3. **Visual iteration** - Use screenshots and design mocks for refinement
4. **CLAUDE.md files** - Document bash commands, style guidelines, testing instructions
5. **Slash commands** - Store prompt templates in `.claude/commands`
6. **Context hygiene** - Clear frequently with `/clear`, interrupt early with Escape

### Security & Reliability
1. **Sandboxing** - 84% reduction in permission prompts while maintaining security
2. **OS-level primitives** - Bubblewrap (Linux), Seatbelt (macOS)
3. **Both isolations required** - Filesystem + network together
4. **Desktop Extensions** - One-click MCP installation with automatic security updates
5. **Continuous monitoring** - Production monitoring catches what periodic testing misses
6. **User feedback critical** - Report issues via `/bug` command

### Advanced Techniques
1. **Think tool** - For long chains of tool calls requiring analysis (54% improvement)
2. **Extended thinking** - For comprehensive pre-planning
3. **Subagents** - Isolated context windows prevent bloat
4. **Compaction** - Automatic conversation summarization near limits
5. **Contextual retrieval** - 67% improvement with contextual embeddings + BM25 + reranking
6. **Parallel instances** - Multiple Claude instances for code review and verification

---

## Additional Resources

- **Anthropic Engineering Blog:** https://www.anthropic.com/engineering
- **Model Context Protocol:** https://modelcontextprotocol.io
- **Claude Agent SDK:** https://github.com/anthropics/anthropic-sdk-python
- **Claude Developer Platform:** https://console.anthropic.com
- **Claude Documentation:** https://docs.claude.com

---

## Article Index

All 14 articles from Anthropic's engineering blog:

1. Code execution with MCP (Nov 4, 2025)
2. Claude Code Sandboxing (Oct 20, 2025)
3. Agent Skills (Oct 16, 2025)
4. Claude Agent SDK (Sep 29, 2025)
5. Effective Context Engineering (Sep 29, 2025)
6. Infrastructure Postmortem (Sep 17, 2025)
7. Writing Effective Tools (Sep 11, 2025)
8. Desktop Extensions (Jun 26, 2025)
9. Multi-Agent Research Systems (Jun 13, 2025)
10. Claude Code Best Practices (Apr 18, 2025)
11. The Think Tool (Mar 20, 2025)
12. SWE-Bench Performance (Jan 6, 2025)
13. Building Effective Agents (Dec 19, 2024)
14. Contextual Retrieval (Sep 19, 2024)

---

**Document Purpose:** This document serves as a comprehensive offline reference for Anthropic's engineering best practices, enabling the Claude Code Learning System to apply these insights without requiring web fetches during analysis and improvement planning.
