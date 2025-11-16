"""
Context Manager Operations

Agent-friendly interface for context optimization and management.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time
from skills.common.registry import SkillRegistry


@dataclass
class OperationResult:
    """Result from a skill operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


def analyze_context_usage(
    estimated_tokens: int = 0,
    max_tokens: int = 200000,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze current context usage and provide optimization recommendations.

    Args:
        estimated_tokens: Current estimated token count
        max_tokens: Maximum context window size
        response_format: "summary" (recommendations only) or "detailed" (full analysis)

    Returns:
        OperationResult with context analysis and recommendations

    Token Efficiency:
        - This operation itself uses minimal tokens (< 200)
        - Provides recommendations that can save 50-95% tokens on large operations
    """
    start_time = time.time()

    try:
        # Calculate usage metrics
        usage_percent = (estimated_tokens / max_tokens) * 100
        remaining = max_tokens - estimated_tokens

        # Determine status
        if usage_percent < 25:
            status = "low"
            priority = "none"
        elif usage_percent < 50:
            status = "moderate"
            priority = "low"
        elif usage_percent < 75:
            status = "high"
            priority = "medium"
        else:
            status = "critical"
            priority = "high"

        # Generate recommendations
        recommendations = []

        if usage_percent > 50:
            recommendations.append({
                "type": "use_summary_format",
                "description": "Use response_format='summary' instead of 'detailed' for operations",
                "potential_savings": "80-95%",
                "priority": "high"
            })

        if usage_percent > 60:
            recommendations.append({
                "type": "local_filtering",
                "description": "Use ResultFilter for local data filtering instead of returning all data",
                "potential_savings": "95-99%",
                "priority": "high"
            })

        if usage_percent > 70:
            recommendations.append({
                "type": "create_notes",
                "description": "Create persistent notes for important information to reduce context",
                "potential_savings": "Variable",
                "priority": "medium"
            })

        if usage_percent > 80:
            recommendations.append({
                "type": "compact_conversation",
                "description": "Compact conversation history by summarizing completed work",
                "potential_savings": "50-80%",
                "priority": "critical"
            })

        duration = time.time() - start_time

        data = {
            "tokens_used": estimated_tokens,
            "tokens_max": max_tokens,
            "tokens_remaining": remaining,
            "usage_percent": round(usage_percent, 1),
            "status": status,
            "priority": priority,
            "recommendations_count": len(recommendations)
        }

        if response_format == "detailed":
            data.update({
                "recommendations": recommendations,
                "optimization_strategies": {
                    "progressive_disclosure": "Load summary first, details on demand",
                    "local_filtering": "Filter data in code, not in agent context",
                    "response_formats": "Use 'summary' or 'concise' formats",
                    "result_filter": "Use ResultFilter for 95-99% savings",
                    "notes": "Persist important info to disk",
                    "compaction": "Summarize completed work"
                },
                "efficiency_metrics": {
                    "typical_summary": "200-1000 tokens",
                    "typical_detailed": "2000-10000 tokens",
                    "typical_savings": "80-95%"
                }
            })
        else:
            # Summary format - just key recommendations
            if recommendations:
                data["top_recommendations"] = [
                    f"{rec['type']}: {rec['description']} (save {rec['potential_savings']})"
                    for rec in recommendations[:3]
                ]

        return OperationResult(
            success=True,
            data=data,
            duration=duration
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to analyze context usage: {str(e)}",
            error_code="ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check that estimated_tokens and max_tokens are positive integers",
                    "Verify estimated_tokens <= max_tokens",
                    "Ensure parameters are numeric values, not strings"
                ],
                "example_fix": "analyze_context_usage(estimated_tokens=50000, max_tokens=200000)"
            }
        )


def create_notes(
    notes_content: str,
    notes_file: str = ".claude/notes/NOTES.md",
    append: bool = True,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Create or append to persistent notes file for important information.

    Args:
        notes_content: Content to save to notes
        notes_file: Path to notes file (default: .claude/notes/NOTES.md)
        append: If True, append to existing notes; if False, overwrite
        response_format: "summary" (brief confirmation) or "detailed" (with recommendations)

    Returns:
        OperationResult with notes creation status

    Token Efficiency:
        - Saves important info to disk instead of keeping in context
        - Can reduce context by 1000-5000 tokens per note session
        - Notes persist across conversations
    """
    start_time = time.time()

    try:
        notes_path = Path(notes_file)

        # Create directory if it doesn't exist
        notes_path.parent.mkdir(parents=True, exist_ok=True)

        # Add timestamp to content
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_content = f"\n---\n**{timestamp}**\n\n{notes_content}\n"

        # Write or append
        if append and notes_path.exists():
            with open(notes_path, 'a') as f:
                f.write(formatted_content)
            action = "appended"
        else:
            with open(notes_path, 'w') as f:
                if not notes_path.exists() or not append:
                    f.write(f"# Notes\n\nPersistent notes for context management.\n")
                f.write(formatted_content)
            action = "created"

        duration = time.time() - start_time

        data = {
            "notes_file": str(notes_path),
            "action": action,
            "content_length": len(notes_content),
            "estimated_tokens_saved": len(notes_content.split()) * 1.3,  # Rough estimate
            "message": f"Notes {action} successfully at {notes_path}"
        }

        if response_format == "detailed":
            data.update({
                "recommendations": [
                    "Reference notes file in future conversations to recall this information",
                    "Notes persist across sessions, saving context tokens",
                    "Consider organizing notes by topic or date for easier reference"
                ],
                "usage_tips": {
                    "read_notes": f"Read notes with: Read('{notes_path}')",
                    "append_more": f"Append more with: create_notes('new content', append=True)",
                    "organize": "Create separate notes files for different topics"
                }
            })

        return OperationResult(
            success=True,
            data=data,
            duration=duration
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to create notes: {str(e)}",
            error_code="NOTES_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check that the notes directory is writable",
                    "Verify the file path is valid",
                    "Ensure parent directory exists",
                    "Try with a simpler path like '.claude/notes/NOTES.md'"
                ],
                "example_fix": "create_notes('Important info', notes_file='.claude/notes/NOTES.md')"
            }
        )


def compact_conversation(
    work_completed: List[str],
    decisions_made: List[str],
    unresolved_issues: List[str],
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Create a compact summary of conversation/work for context reduction.

    Args:
        work_completed: List of completed tasks/items
        decisions_made: List of key decisions made
        unresolved_issues: List of issues still to address
        response_format: "summary" (compact) or "detailed" (with recommendations)

    Returns:
        OperationResult with compacted summary

    Token Efficiency:
        - Reduces conversation history by 50-80%
        - Preserves critical information
        - Enables clearing old context safely
    """
    start_time = time.time()

    try:
        # Create compact summary
        summary_parts = []

        if work_completed:
            summary_parts.append(f"Completed ({len(work_completed)} items):")
            summary_parts.extend([f"  ✓ {item}" for item in work_completed])

        if decisions_made:
            summary_parts.append(f"\nDecisions ({len(decisions_made)} items):")
            summary_parts.extend([f"  • {item}" for item in decisions_made])

        if unresolved_issues:
            summary_parts.append(f"\nUnresolved ({len(unresolved_issues)} items):")
            summary_parts.extend([f"  ⚠ {item}" for item in unresolved_issues])

        compact_summary = "\n".join(summary_parts)

        duration = time.time() - start_time

        data = {
            "compact_summary": compact_summary,
            "items_completed": len(work_completed),
            "items_decided": len(decisions_made),
            "items_unresolved": len(unresolved_issues),
            "total_items": len(work_completed) + len(decisions_made) + len(unresolved_issues),
            "estimated_tokens": len(compact_summary.split()) * 1.3,
            "usage_tip": "Use this summary to replace verbose conversation history"
        }

        if response_format == "detailed":
            data.update({
                "recommendations": [
                    "Save this summary with create_notes() for persistence",
                    "Clear old conversation history",
                    "Continue with fresh context using this summary",
                    "Reference specific items by number when needed"
                ],
                "next_steps": [
                    "Persist summary to notes if needed",
                    "Clear conversation (if supported)",
                    "Continue work referencing summary"
                ]
            })

        return OperationResult(
            success=True,
            data=data,
            duration=duration
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to compact conversation: {str(e)}",
            error_code="COMPACTION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure all parameters are lists of strings",
                    "Check that work_completed, decisions_made, and unresolved_issues are valid lists",
                    "Try with simpler input first to verify the operation works",
                    "Verify list items don't contain special characters causing formatting issues"
                ],
                "example_fix": "compact_conversation(['Task 1', 'Task 2'], ['Decision 1'], ['Issue 1'])"
            }
        )

def analyze_available_skills(
    include_operations: bool = False,
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """
    Analyze available skills in the workspace for context documentation.

    This operation uses the SkillRegistry to discover all available skills,
    helping agents understand workspace capabilities and validate dependencies.

    Args:
        include_operations: If True, list operations for each skill
        response_format: "summary" (skill count) or "detailed" (full skill info)

    Returns:
        OperationResult with skill availability information

    Token Efficiency:
        - Summary mode: ~500 tokens (skill names only)
        - Detailed mode: ~2000-5000 tokens (with operations)
        - Use summary mode for quick availability checks

    Example:
        # Quick check
        result = analyze_available_skills(response_format="summary")
        print(f"Available skills: {result.data['skill_count']}")

        # Detailed inventory
        result = analyze_available_skills(
            include_operations=True,
            response_format="detailed"
        )
        for skill, info in result.data['skills'].items():
            print(f"{skill}: {len(info['operations'])} operations")
    """
    start_time = time.time()

    try:
        # Discover all skills
        skills = SkillRegistry.discover_skills()

        # Build skill summary
        skill_names = sorted(skills.keys())
        skill_count = len(skill_names)

        # Count total operations across all skills
        total_operations = sum(len(info.operations) for info in skills.values())

        # Categorize by operation count (proxy for complexity)
        simple_skills = [name for name, info in skills.items() if len(info.operations) <= 2]
        medium_skills = [name for name, info in skills.items() if 3 <= len(info.operations) <= 5]
        complex_skills = [name for name, info in skills.items() if len(info.operations) > 5]

        # Count skills with documentation and tests
        documented = sum(1 for info in skills.values() if info.has_skill_md)
        tested = sum(1 for info in skills.values() if info.has_tests)

        duration = time.time() - start_time

        if response_format == "summary":
            data = {
                "skill_count": skill_count,
                "total_operations": total_operations,
                "documented_skills": documented,
                "tested_skills": tested,
                "categories": {
                    "simple": len(simple_skills),
                    "medium": len(medium_skills),
                    "complex": len(complex_skills)
                },
                "skill_names": skill_names,
                "usage_tip": "Use response_format='detailed' to see operations for each skill"
            }
        else:
            # Detailed mode
            skill_details = {}
            for name, info in skills.items():
                skill_details[name] = {
                    "version": info.version,
                    "operations": info.operations if include_operations else len(info.operations),
                    "has_documentation": info.has_skill_md,
                    "has_tests": info.has_tests,
                    "path": str(info.path)
                }

            data = {
                "skill_count": skill_count,
                "total_operations": total_operations,
                "documented_skills": documented,
                "tested_skills": tested,
                "skills": skill_details,
                "categories": {
                    "simple": simple_skills,
                    "medium": medium_skills,
                    "complex": complex_skills
                },
                "recommendations": [
                    f"Document {skill_count - documented} undocumented skills" if documented < skill_count else "All skills documented",
                    f"Add tests to {skill_count - tested} skills" if tested < skill_count else "All skills have tests",
                    "Use SkillRegistry.validate_dependencies() before invoking skills",
                    "Check skill operations with SkillRegistry.get_skill_operations(skill_name)"
                ]
            }

        return OperationResult(
            success=True,
            data=data,
            duration=duration,
            metadata={
                "skill": "context_manager",
                "operation": "analyze_available_skills",
                "discovery_method": "SkillRegistry"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to analyze skills: {str(e)}",
            error_code="SKILL_ANALYSIS_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Verify skills directory exists and is accessible",
                    "Check SkillRegistry is properly imported",
                    "Try running SkillRegistry.discover_skills() directly",
                    "Clear skill cache with SkillRegistry.clear_cache()"
                ],
                "example_fix": "analyze_available_skills(response_format='summary')"
            }
        )
