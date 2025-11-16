"""
LLM-as-Judge Skill Operations

Agent-friendly interface for evaluating teaching quality and student understanding.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import time

from .core.teaching_evaluator import TeachingEvaluator
from .core.understanding_checker import UnderstandingChecker


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def evaluate_teaching(
    agent_response: str,
    student_question: Optional[str] = None,
    teaching_criteria: Optional[Dict[str, bool]] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Evaluate agent response for teaching quality.

    Args:
        agent_response: The agent's response to evaluate
        student_question: Optional student question for context
        teaching_criteria: Criteria to check
            - require_questions: Must ask guiding questions (default: True)
            - forbid_solutions: Must not give complete solutions (default: True)
            - require_examples: Must include small examples (default: False)
            - require_explanations: Must explain concepts (default: True)
        response_format: "summary" (overview) or "detailed" (all issues)

    Returns:
        OperationResult with evaluation results

    Token Efficiency:
        - Use response_format="summary" for teaching-focused status and score
        - Use response_format="detailed" for all issues and suggestions
        - Summary mode saves 70-85% tokens
    """
    start_time = time.time()

    try:
        evaluator = TeachingEvaluator()
        result = evaluator.evaluate(agent_response, student_question, teaching_criteria)

        duration = time.time() - start_time

        # Format response
        data = {
            "is_teaching_focused": result.is_teaching_focused,
            "quality_score": result.quality_score,
            "issue_count": len(result.issues),
            "strength_count": len(result.strengths)
        }

        if response_format == "detailed":
            data.update({
                "issues": [
                    {
                        "severity": issue.severity,
                        "category": issue.category,
                        "message": issue.message,
                        "suggestion": issue.suggestion
                    }
                    for issue in result.issues
                ],
                "strengths": result.strengths,
                "improvements": result.improvements,
                "metrics": result.metrics
            })
        else:  # summary
            if result.issues:
                data["top_issues"] = [
                    f"{issue.severity.upper()}: {issue.message}"
                    for issue in result.issues[:3]
                ]
            if result.strengths:
                data["top_strengths"] = result.strengths[:3]
            if result.improvements:
                data["top_improvements"] = result.improvements[:3]

            data["efficiency_tip"] = (
                f"Teaching evaluation complete! Quality score: {result.quality_score:.1%}.\\n"
                f"For all issues, strengths, and detailed metrics:\\n"
                f"evaluate_teaching(response, response_format='detailed')"
            )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "llm_judge",
                "operation": "evaluate_teaching",
                "version": "1.0.0"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Teaching evaluation failed: {str(e)}",
            error_code="EVALUATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure agent_response is a string",
                    "Check that response contains text to evaluate",
                    "Verify teaching_criteria is a dict if provided"
                ],
                "example_fix": "evaluate_teaching('Your response here', teaching_criteria={'require_questions': True})"
            }
        )


def check_understanding(
    student_code: str,
    expected_concepts: Optional[List[str]] = None,
    learning_context: Optional[Dict[str, Any]] = None,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Check student understanding through code analysis.

    Args:
        student_code: Student's code to analyze
        expected_concepts: Concepts student should demonstrate
            - "functions", "classes", "loops", "conditionals"
            - "error_handling", "typing", "docstrings"
            - "list_comprehension", "generators", "decorators"
        learning_context: Optional context
            - level: "beginner", "intermediate", "advanced"
            - previous_attempts: int
            - known_struggles: List[str]
        response_format: "summary" (overview) or "detailed" (all gaps)

    Returns:
        OperationResult with understanding analysis

    Token Efficiency:
        - Use response_format="summary" for understanding status and confidence
        - Use response_format="detailed" for all knowledge gaps and suggestions
        - Summary mode saves 75-90% tokens
    """
    start_time = time.time()

    try:
        checker = UnderstandingChecker()
        result = checker.check_code_understanding(student_code, expected_concepts, learning_context)

        duration = time.time() - start_time

        # Format response
        data = {
            "demonstrates_understanding": result.demonstrates_understanding,
            "confidence_level": result.confidence_level,
            "knowledge_gap_count": len(result.knowledge_gaps),
            "concepts_demonstrated": len(result.demonstrated_concepts)
        }

        if response_format == "detailed":
            data.update({
                "knowledge_gaps": [
                    {
                        "concept": gap.concept,
                        "severity": gap.severity,
                        "evidence": gap.evidence,
                        "suggestion": gap.suggestion
                    }
                    for gap in result.knowledge_gaps
                ],
                "demonstrated_concepts": result.demonstrated_concepts,
                "recommended_review": result.recommended_review,
                "next_learning_steps": result.next_learning_steps,
                "metrics": result.metrics
            })
        else:  # summary
            # Show critical gaps
            critical_gaps = [g for g in result.knowledge_gaps if g.severity == "critical"]
            if critical_gaps:
                data["critical_gaps"] = [
                    f"{gap.concept}: {gap.evidence}"
                    for gap in critical_gaps[:3]
                ]

            # Show top demonstrated concepts
            if result.demonstrated_concepts:
                data["top_demonstrated"] = result.demonstrated_concepts[:5]

            # Show next steps
            if result.next_learning_steps:
                data["next_steps"] = result.next_learning_steps[:2]

            data["efficiency_tip"] = (
                f"Understanding check complete! Confidence: {result.confidence_level:.1%}.\\n"
                f"For all knowledge gaps and learning recommendations:\\n"
                f"check_understanding(code, expected_concepts, response_format='detailed')"
            )

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "llm_judge",
                "operation": "check_understanding",
                "version": "1.0.0"
            }
        )

    except SyntaxError as e:
        # Syntax errors are expected and informative
        data = {
            "demonstrates_understanding": False,
            "confidence_level": 0.0,
            "knowledge_gap_count": 1,
            "concepts_demonstrated": 0,
            "critical_gaps": [
                f"syntax: Syntax error at line {e.lineno}: {e.msg}"
            ],
            "next_steps": [
                "Review Python syntax basics",
                "Ensure proper indentation and structure"
            ]
        }

        return OperationResult(
            success=True,  # This is a valid result, not an error
            data=data,
            duration=time.time() - start_time,
            metadata={
                "skill": "llm_judge",
                "operation": "check_understanding",
                "version": "1.0.0",
                "note": "Syntax errors detected in student code"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Understanding check failed: {str(e)}",
            error_code="CHECK_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure student_code is a string containing Python code",
                    "Check that expected_concepts is a list of strings if provided",
                    "Verify learning_context is a dict if provided",
                    "If code has syntax errors, this is normal - they'll be reported"
                ],
                "example_fix": "check_understanding('def hello():\\n    print(\"Hi\")', expected_concepts=['functions'])"
            }
        )
