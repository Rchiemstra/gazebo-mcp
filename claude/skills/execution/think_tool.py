"""
Think Tool Integration for Claude Agents.

Implements Anthropic's "Think" tool pattern for improved reasoning:
- 54% improvement in complex domains
- 1.6% average improvement on SWE-Bench
- Allows agent to pause and analyze before proceeding

Based on Anthropic's research:
"The 'think' tool allows Claude to 'stop and think about whether it has all
the information it needs to move forward' during active tool use"

Best for:
- Long chains of tool calls
- Policy-heavy environments
- Sequential decisions with consequences
- Complex multi-step reasoning
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ThinkEntry:
    """Record of a thinking session."""
    timestamp: datetime
    reasoning: str
    context: Optional[Dict[str, Any]] = None
    decision: Optional[str] = None
    confidence: Optional[float] = None


class ThinkTool:
    """
    Think tool for agent reasoning.

    Allows agent to pause, analyze information, and decide on next steps
    before proceeding with tool calls.

    Example usage in agent prompt:
        When faced with complex decisions:
        1. Use **think tool** to analyze the situation
        2. Consider: Do I have all needed information?
        3. Consider: What are the risks of each option?
        4. Decide on the best approach
        5. Then proceed with tool calls

    Example in code:
        think_tool = ThinkTool()

        # Agent pauses to think
        think_tool.think('''
        I need to analyze this codebase architecture.
        Questions:
        - Do I understand the current structure?
        - What patterns am I seeing?
        - What are the potential issues?

        Analysis:
        - Seeing tight coupling between modules
        - No clear separation of concerns
        - High complexity in core components

        Decision: Focus on the 3 highest complexity modules first
        ''')

        # Then proceed with actions based on thinking
    """

    def __init__(self, enable_logging: bool = True):
        """
        Initialize think tool.

        Args:
            enable_logging: Whether to log thinking sessions
        """
        self.enable_logging = enable_logging
        self.think_history: List[ThinkEntry] = []

    def think(
        self,
        reasoning: str,
        context: Optional[Dict[str, Any]] = None,
        decision: Optional[str] = None,
        confidence: Optional[float] = None
    ) -> ThinkEntry:
        """
        Pause and think about the current situation.

        This is the main "think" tool call that agents use.

        Args:
            reasoning: The agent's reasoning process (can be multi-line)
            context: Optional context information
            decision: Optional explicit decision made
            confidence: Optional confidence level (0.0 - 1.0)

        Returns:
            ThinkEntry record of this thinking session
        """
        entry = ThinkEntry(
            timestamp=datetime.now(),
            reasoning=reasoning.strip(),
            context=context,
            decision=decision,
            confidence=confidence
        )

        if self.enable_logging:
            self.think_history.append(entry)

        return entry

    def get_history(self) -> List[ThinkEntry]:
        """Get history of thinking sessions."""
        return self.think_history.copy()

    def clear_history(self):
        """Clear thinking history."""
        self.think_history.clear()

    def analyze_thinking_patterns(self) -> Dict[str, Any]:
        """
        Analyze thinking patterns for improvements.

        Returns statistics about thinking sessions:
        - How often agent pauses to think
        - Average confidence levels
        - Common decision patterns
        """
        if not self.think_history:
            return {
                "total_sessions": 0,
                "message": "No thinking sessions recorded"
            }

        total = len(self.think_history)
        with_decisions = sum(1 for e in self.think_history if e.decision)
        with_confidence = [e.confidence for e in self.think_history if e.confidence is not None]

        return {
            "total_sessions": total,
            "sessions_with_decisions": with_decisions,
            "decision_rate": with_decisions / total if total > 0 else 0,
            "average_confidence": sum(with_confidence) / len(with_confidence) if with_confidence else None,
            "min_confidence": min(with_confidence) if with_confidence else None,
            "max_confidence": max(with_confidence) if with_confidence else None,
            "recent_sessions": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "reasoning_length": len(e.reasoning),
                    "has_decision": e.decision is not None,
                    "confidence": e.confidence
                }
                for e in self.think_history[-5:]
            ]
        }


# Global think tool instance for agent use
_global_think_tool = ThinkTool()


def think(
    reasoning: str,
    context: Optional[Dict[str, Any]] = None,
    decision: Optional[str] = None,
    confidence: Optional[float] = None
) -> ThinkEntry:
    """
    Global think function for easy agent use.

    This is the function agents call directly.

    Example in agent code:
        from skills.execution.think_tool import think

        # Pause to analyze
        think('''
        Current situation: Need to refactor authentication module
        Questions:
        - Are there any breaking changes?
        - What's the test coverage?
        - Who uses this module?

        Analysis:
        - 15 files depend on this
        - Test coverage is 67%
        - Need to check integration tests

        Decision: Start with isolated functions, avoid breaking changes
        ''', decision="Refactor isolated functions first", confidence=0.8)
    """
    return _global_think_tool.think(reasoning, context, decision, confidence)


def get_think_history() -> List[ThinkEntry]:
    """Get global thinking history."""
    return _global_think_tool.get_history()


def clear_think_history():
    """Clear global thinking history."""
    _global_think_tool.clear_history()


def analyze_thinking() -> Dict[str, Any]:
    """Analyze global thinking patterns."""
    return _global_think_tool.analyze_thinking_patterns()


# Tool definition for Claude SDK integration
THINK_TOOL_DEFINITION = {
    "name": "think",
    "description": (
        "Pause and think before proceeding with tool calls. "
        "Use this when you need to:\n"
        "- Analyze complex information\n"
        "- Decide between multiple options\n"
        "- Verify you have all needed information\n"
        "- Consider risks and trade-offs\n"
        "- Plan multi-step approaches\n\n"
        "54% improvement in complex domains. "
        "Use liberally for better decision-making."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": (
                    "Your reasoning process. Can include:\n"
                    "- Questions you're asking yourself\n"
                    "- Analysis of the situation\n"
                    "- Pros and cons of options\n"
                    "- Information gaps\n"
                    "- Tentative conclusions"
                )
            },
            "decision": {
                "type": "string",
                "description": "The decision or next step you've decided on (optional)"
            },
            "confidence": {
                "type": "number",
                "description": "Your confidence level (0.0 to 1.0) in this decision (optional)"
            }
        },
        "required": ["reasoning"]
    }
}


def enable_think_tool(tools_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Add think tool to a list of tool definitions.

    Args:
        tools_list: Existing list of tool definitions

    Returns:
        Updated list with think tool added

    Example:
        tools = [
            {"name": "read_file", ...},
            {"name": "write_file", ...},
        ]

        tools = enable_think_tool(tools)
        # Now includes "think" tool
    """
    # Check if think tool already present
    if any(t.get("name") == "think" for t in tools_list):
        return tools_list

    return tools_list + [THINK_TOOL_DEFINITION]


# Example usage patterns
THINK_TOOL_EXAMPLES = {
    "code_review": """
think('''
Reviewing authentication.py for security issues.

Questions:
- Are passwords hashed properly?
- Is there SQL injection protection?
- Are sessions managed securely?

Analysis:
- Password hashing uses bcrypt ✓
- SQL queries use parameterized statements ✓
- Session tokens are random and expire ✓
- BUT: No rate limiting on login attempts ✗

Risks:
- Brute force attacks possible without rate limiting
- Medium severity issue

Decision: Flag rate limiting as required change
''', decision="Add rate limiting requirement", confidence=0.9)
""",

    "architecture_decision": """
think('''
Deciding between microservices vs monolith for this project.

Context:
- Team size: 3 developers
- Expected scale: 10K users initially
- Deployment: Cloud (AWS)

Microservices Pros:
- Better scalability
- Independent deployment
- Technology flexibility

Microservices Cons:
- Operational complexity
- Distributed system challenges
- Small team overhead

Monolith Pros:
- Simpler to develop
- Easier debugging
- Lower operational cost

Monolith Cons:
- Harder to scale later
- Deployment coupling

Analysis:
Given small team + moderate scale, monolith is better starting point.
Can extract services later if needed.

Decision: Start with modular monolith, design for future service extraction
''', decision="Modular monolith architecture", confidence=0.85)
""",

    "debugging": """
think('''
Bug: Users can't log in. Need to diagnose systematically.

What I know:
- Started after yesterday's deployment
- Affects ~50% of users
- No clear error message

Hypotheses:
1. Database connection issue?
2. Session storage problem?
3. Authentication service down?
4. Cache invalidation issue?

Need to check:
- Server logs
- Database connectivity
- Redis/session store status
- Recent code changes

Most likely: Cache invalidation issue (50% of users suggests some cached data)

Decision: Check cache first, then review auth changes from yesterday's deploy
''', decision="Check cache configuration", confidence=0.7)
"""
}


def get_examples() -> Dict[str, str]:
    """Get example usage patterns for think tool."""
    return THINK_TOOL_EXAMPLES.copy()
