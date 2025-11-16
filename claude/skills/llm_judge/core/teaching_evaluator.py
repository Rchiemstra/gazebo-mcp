"""
Teaching Quality Evaluator

Evaluates agent responses to ensure they follow teaching-first principles.
Checks for guidance vs solutions, explanation quality, and pedagogical approach.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import re


@dataclass
class TeachingIssue:
    """An issue found in teaching response."""
    severity: str  # "error", "warning", "info"
    category: str  # "solution_given", "no_guidance", "unclear", "missing_questions"
    message: str
    line: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class TeachingEvaluationResult:
    """Result of teaching quality evaluation."""
    is_teaching_focused: bool
    quality_score: float  # 0.0 to 1.0
    issues: List[TeachingIssue]
    metrics: Dict[str, Any]
    strengths: List[str]
    improvements: List[str]


class TeachingEvaluator:
    """Evaluates agent responses for teaching quality."""

    # Patterns indicating complete solutions (anti-patterns)
    SOLUTION_PATTERNS = [
        r'def\s+\w+\([^)]*\):[\s\S]{20,}',  # Complete function definitions
        r'class\s+\w+[:\(][\s\S]{30,}',      # Complete class definitions
        r'```(?:python|cpp|javascript)[\s\S]{50,}```',  # Large code blocks
        r'Here(?:\'s| is) the (?:complete|full) (?:code|implementation|solution)',
        r'Copy (?:and paste )?this code',
        r'Use this implementation',
    ]

    # Patterns indicating good teaching (positive patterns)
    TEACHING_PATTERNS = [
        r'\?$',  # Questions
        r'(?:Can you|Could you|Try to|Consider|Think about)',  # Prompts to think
        r'(?:Let\'s|We can|You might) (?:break|start|try)',  # Guided exploration
        r'(?:What|How|Why) (?:would|could|do)',  # Socratic questions
        r'(?:Step \d+|First|Next|Then):',  # Step-by-step guidance
        r'Example:[\s\S]{1,100}$',  # Small examples (not solutions)
    ]

    # Patterns indicating explanation attempts
    EXPLANATION_PATTERNS = [
        r'(?:This|It) (?:means|works|helps)',
        r'(?:The reason|Because|Due to)',
        r'For example,',
        r'In other words,',
        r'To understand this,',
    ]

    def evaluate(
        self,
        agent_response: str,
        student_question: Optional[str] = None,
        teaching_criteria: Optional[Dict[str, bool]] = None
    ) -> TeachingEvaluationResult:
        """
        Evaluate agent response for teaching quality.

        Args:
            agent_response: The agent's response to evaluate
            student_question: Optional student question for context
            teaching_criteria: Optional criteria to check
                - require_questions: Must ask guiding questions
                - forbid_solutions: Must not give complete solutions
                - require_examples: Must include small examples
                - require_explanations: Must explain concepts

        Returns:
            TeachingEvaluationResult with evaluation details
        """
        criteria = teaching_criteria or {
            "require_questions": True,
            "forbid_solutions": True,
            "require_examples": False,
            "require_explanations": True
        }

        issues = []
        strengths = []
        improvements = []
        metrics = {
            "response_length": len(agent_response),
            "code_block_count": len(re.findall(r'```[\s\S]*?```', agent_response)),
            "question_count": len(re.findall(r'\?', agent_response)),
            "teaching_pattern_count": 0,
            "solution_pattern_count": 0
        }

        # Check for complete solutions (anti-pattern)
        solution_matches = []
        for pattern in self.SOLUTION_PATTERNS:
            matches = re.findall(pattern, agent_response, re.IGNORECASE)
            if matches:
                solution_matches.extend(matches)
                metrics["solution_pattern_count"] += len(matches)

        if solution_matches and criteria.get("forbid_solutions"):
            issues.append(TeachingIssue(
                severity="error",
                category="solution_given",
                message=f"Response contains {len(solution_matches)} complete solution(s)",
                suggestion="Provide guidance and small examples instead of complete implementations"
            ))
        elif not solution_matches:
            strengths.append("No complete solutions given - focuses on guidance")

        # Check for teaching patterns (positive)
        teaching_matches = []
        for pattern in self.TEACHING_PATTERNS:
            matches = re.findall(pattern, agent_response, re.IGNORECASE)
            if matches:
                teaching_matches.extend(matches)
                metrics["teaching_pattern_count"] += len(matches)

        if teaching_matches:
            strengths.append(f"Uses {len(teaching_matches)} teaching patterns (questions, prompts, step-by-step)")
        elif criteria.get("require_questions"):
            issues.append(TeachingIssue(
                severity="warning",
                category="no_guidance",
                message="Response lacks guiding questions or prompts",
                suggestion="Ask questions to guide student thinking (e.g., 'What data structure would work best?')"
            ))

        # Check for questions
        if metrics["question_count"] == 0 and criteria.get("require_questions"):
            issues.append(TeachingIssue(
                severity="warning",
                category="missing_questions",
                message="Response contains no questions to guide student thinking",
                suggestion="Add Socratic questions to prompt deeper understanding"
            ))
        elif metrics["question_count"] > 0:
            strengths.append(f"Asks {metrics['question_count']} guiding question(s)")

        # Check for explanations
        explanation_matches = []
        for pattern in self.EXPLANATION_PATTERNS:
            matches = re.findall(pattern, agent_response, re.IGNORECASE)
            if matches:
                explanation_matches.extend(matches)

        metrics["explanation_count"] = len(explanation_matches)

        if explanation_matches:
            strengths.append(f"Provides {len(explanation_matches)} explanation(s) of concepts")
        elif criteria.get("require_explanations"):
            issues.append(TeachingIssue(
                severity="warning",
                category="unclear",
                message="Response lacks clear explanations of concepts",
                suggestion="Explain the 'why' behind suggestions, not just the 'what'"
            ))

        # Check code block size
        code_blocks = re.findall(r'```[\s\S]*?```', agent_response)
        large_blocks = [b for b in code_blocks if len(b) > 200]

        if large_blocks:
            issues.append(TeachingIssue(
                severity="warning",
                category="solution_given",
                message=f"Contains {len(large_blocks)} large code block(s) (>200 chars)",
                suggestion="Use small, focused examples (2-5 lines) instead of large code blocks"
            ))
        elif code_blocks and all(len(b) <= 100 for b in code_blocks):
            strengths.append("Uses small, focused code examples")

        # Calculate quality score
        quality_score = self._calculate_quality_score(metrics, issues, strengths)

        # Determine if teaching-focused
        error_count = sum(1 for i in issues if i.severity == "error")
        is_teaching_focused = error_count == 0 and quality_score >= 0.6

        # Generate improvement suggestions
        if not is_teaching_focused:
            if error_count > 0:
                improvements.append("Remove complete solutions - provide guidance instead")
            if metrics["question_count"] == 0:
                improvements.append("Add guiding questions to prompt student thinking")
            if metrics["explanation_count"] == 0:
                improvements.append("Explain concepts and reasoning, not just steps")
            if quality_score < 0.6:
                improvements.append("Focus on teaching process over final answers")

        return TeachingEvaluationResult(
            is_teaching_focused=is_teaching_focused,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            strengths=strengths,
            improvements=improvements
        )

    def _calculate_quality_score(
        self,
        metrics: Dict[str, Any],
        issues: List[TeachingIssue],
        strengths: List[str]
    ) -> float:
        """Calculate overall teaching quality score (0.0 to 1.0)."""
        score = 0.5  # Start at neutral

        # Positive factors
        if metrics["question_count"] > 0:
            score += 0.15
        if metrics["teaching_pattern_count"] > 2:
            score += 0.15
        if metrics["explanation_count"] > 0:
            score += 0.10
        if metrics["code_block_count"] > 0 and metrics["solution_pattern_count"] == 0:
            score += 0.10  # Has examples but not solutions

        # Negative factors
        for issue in issues:
            if issue.severity == "error":
                score -= 0.25
            elif issue.severity == "warning":
                score -= 0.10

        return max(0.0, min(1.0, score))
