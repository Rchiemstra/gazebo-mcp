"""
Learning Plan Parser

Parses markdown learning plans into structured LearningPlan objects.
"""

import re
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

from .models import (
    LearningPlan,
    LearningPlanMetadata,
    Phase,
    Task,
    Checkpoint,
    JournalEntry,
    Prerequisite,
    TaskStatus,
    CheckpointStatus,
    ComplexityLevel,
)


class LearningPlanParser:
    """Parses markdown learning plans into LearningPlan objects"""

    def parse(self, markdown_content: str) -> LearningPlan:
        """
        Parse markdown content into LearningPlan.

        Args:
            markdown_content: Full markdown content of learning plan

        Returns:
            Parsed LearningPlan object
        """
        lines = markdown_content.split("\n")

        # Parse each section
        metadata = self._parse_metadata(lines)
        learning_objectives = self._parse_learning_objectives(lines)
        prerequisites = self._parse_prerequisites(lines)
        phases = self._parse_phases(lines)
        learning_team = self._parse_learning_team(lines)
        milestones = self._parse_milestones(lines)
        journal_entries = self._parse_journal_entries(lines)
        resources = self._parse_resources(lines)
        common_pitfalls = self._parse_common_pitfalls(lines)

        return LearningPlan(
            metadata=metadata,
            learning_objectives=learning_objectives,
            prerequisites=prerequisites,
            phases=phases,
            learning_team=learning_team,
            milestones=milestones,
            journal_entries=journal_entries,
            resources=resources,
            common_pitfalls=common_pitfalls,
        )

    def _parse_metadata(self, lines: List[str]) -> LearningPlanMetadata:
        """Parse header metadata"""
        # Find title (first H1)
        title = ""
        for line in lines[:20]:  # Check first 20 lines
            if line.startswith("# ") and not line.startswith("##"):
                title = line[2:].strip()
                break

        # Parse metadata fields
        created = None
        last_updated = None
        estimated_time = ""
        complexity_level = ComplexityLevel.INTERMEDIATE
        progress_summary = None

        for line in lines[:50]:  # Check first 50 lines
            # Created: 2025-10-09
            if match := re.match(r"\*\*Created\*\*:\s*(.+)", line):
                created = self._parse_date(match.group(1))

            # Last Updated: 2025-10-09 (Progress: ...)
            elif match := re.match(r"\*\*Last Updated\*\*:\s*(.+)", line):
                updated_str = match.group(1)
                # Extract date part
                date_match = re.match(r"(\d{4}-\d{2}-\d{2})", updated_str)
                if date_match:
                    last_updated = self._parse_date(date_match.group(1))
                # Extract progress summary
                if "(" in updated_str:
                    progress_summary = updated_str[updated_str.index("(") + 1 : updated_str.rindex(")")]

            # Estimated Learning Time: 8-10 weeks
            elif match := re.match(
                r"\*\*Estimated Learning Time\*\*:\s*(.+)", line
            ):
                estimated_time = match.group(1).strip()

            # Complexity Level: Advanced
            elif match := re.match(r"\*\*Complexity Level\*\*:\s*(.+)", line):
                level_str = match.group(1).strip().lower()
                # Extract just the level word, ignore parenthetical
                level_word = level_str.split("(")[0].strip()
                try:
                    complexity_level = ComplexityLevel(level_word)
                except ValueError:
                    pass  # Keep default

        # Use current time if dates not found
        if not created:
            created = datetime.now()
        if not last_updated:
            last_updated = created

        return LearningPlanMetadata(
            title=title or "Untitled Learning Plan",
            created=created,
            last_updated=last_updated,
            estimated_time=estimated_time or "Unknown",
            complexity_level=complexity_level,
            progress_summary=progress_summary,
        )

    def _parse_learning_objectives(self, lines: List[str]) -> Dict[str, List[str]]:
        """Parse learning objectives section"""
        objectives = {
            "what_you_will_learn": [],
            "skills_you_will_develop": [],
            "outcomes": [],
        }

        # Find the learning objectives section
        in_section = False
        current_subsection = None

        for i, line in enumerate(lines):
            # Start of section
            if re.match(r"##\s+.*Learning Objectives", line, re.IGNORECASE):
                in_section = True
                continue

            # End of section (next ## header)
            if in_section and line.startswith("##") and "Learning Objectives" not in line:
                break

            if not in_section:
                continue

            # Subsections
            if line.startswith("###"):
                subsection_title = line[3:].strip().lower()
                if "what you" in subsection_title and "learn" in subsection_title:
                    current_subsection = "what_you_will_learn"
                elif "skills" in subsection_title:
                    current_subsection = "skills_you_will_develop"
                elif "outcome" in subsection_title:
                    current_subsection = "outcomes"
                continue

            # Extract bullet points
            if current_subsection and line.strip().startswith("-"):
                # Remove markdown formatting (**, *, etc.)
                item = line.strip()[1:].strip()
                item = re.sub(r"\*\*(.+?)\*\*", r"\1", item)  # Remove bold
                objectives[current_subsection].append(item)

        return objectives

    def _parse_prerequisites(self, lines: List[str]) -> List[Prerequisite]:
        """Parse prerequisites section"""
        prerequisites = []
        in_section = False

        for line in lines:
            # Start of section
            if re.match(r"##\s+.*Prerequisites", line, re.IGNORECASE):
                in_section = True
                continue

            # End of section
            if in_section and line.startswith("##") and "Prerequisites" not in line:
                break

            if not in_section:
                continue

            # Parse checkbox items
            if match := re.match(r"-\s+\[([ x])\]\s+(.+)", line):
                completed = match.group(1) == "x"
                description = match.group(2).strip()
                prerequisites.append(
                    Prerequisite(description=description, completed=completed)
                )

        return prerequisites

    def _parse_phases(self, lines: List[str]) -> List[Phase]:
        """Parse all phases"""
        phases = []
        current_phase_start = None

        # Find all phase headers
        phase_indices = []
        for i, line in enumerate(lines):
            if match := re.match(r"##\s+Phase\s+(\d+)[:：]\s+(.+)", line):
                phase_indices.append((i, int(match.group(1)), match.group(2).strip()))

        # Parse each phase
        for idx, (line_num, phase_num, phase_title) in enumerate(phase_indices):
            # Determine end of this phase
            end_line = (
                phase_indices[idx + 1][0] if idx + 1 < len(phase_indices) else len(lines)
            )

            phase_lines = lines[line_num:end_line]
            phase = self._parse_phase(phase_lines, phase_num, phase_title)
            phases.append(phase)

        return phases

    def _parse_phase(
        self, phase_lines: List[str], phase_number: int, phase_title: str
    ) -> Phase:
        """Parse a single phase"""
        # Extract duration from title if present
        duration = None
        if match := re.search(r"\((.+?)\)", phase_title):
            duration = match.group(1)
            phase_title = phase_title[: match.start()].strip()

        learning_goals = []
        tasks = []
        checkpoints = []
        specialist_support = {}

        # Parse phase content
        in_goals = False
        in_tasks = False
        current_task = None

        for i, line in enumerate(phase_lines):
            # Learning Goals section
            if re.match(r"###\s+Learning Goals", line, re.IGNORECASE):
                in_goals = True
                in_tasks = False
                continue

            # Tasks section
            if re.match(r"###\s+(Research\s+)?Tasks?", line, re.IGNORECASE):
                in_goals = False
                in_tasks = True
                continue

            # Other subsections end tasks/goals
            if line.startswith("###") and not any(
                x in line.lower() for x in ["task", "goal"]
            ):
                in_goals = False
                in_tasks = False

            # Checkpoints
            if re.match(r"###\s+Understanding Checkpoint", line, re.IGNORECASE):
                checkpoint = self._parse_checkpoint(phase_lines[i:], phase_number)
                if checkpoint:
                    checkpoints.append(checkpoint)

            # Extract learning goals
            if in_goals and line.strip().startswith("-"):
                goal = line.strip()[1:].strip()
                learning_goals.append(goal)

            # Extract tasks
            if in_tasks:
                # Task header (#### Task X.Y: Title)
                if match := re.match(r"####\s+Task\s+([\d.]+):\s+(.+)", line):
                    # Save previous task
                    if current_task:
                        tasks.append(current_task)

                    task_id = f"task-{match.group(1)}"
                    task_title = match.group(2).strip()

                    # Detect status from emoji
                    status = TaskStatus.NOT_STARTED
                    if "✅" in task_title or "COMPLETED" in task_title.upper():
                        status = TaskStatus.COMPLETED
                    elif "🔄" in task_title or "IN PROGRESS" in task_title.upper():
                        status = TaskStatus.IN_PROGRESS

                    current_task = Task(
                        id=task_id,
                        title=task_title,
                        description="",
                        status=status,
                    )

        # Add last task
        if current_task:
            tasks.append(current_task)

        phase_id = f"phase-{phase_number}"

        return Phase(
            id=phase_id,
            number=phase_number,
            title=phase_title,
            duration=duration,
            learning_goals=learning_goals,
            tasks=tasks,
            checkpoints=checkpoints,
            specialist_support=specialist_support,
        )

    def _parse_checkpoint(
        self, lines: List[str], phase_number: int
    ) -> Optional[Checkpoint]:
        """Parse an understanding checkpoint"""
        questions = []
        status = CheckpointStatus.NOT_REACHED

        # Look for checkpoint questions
        in_questions = False
        for line in lines[:30]:  # Check next 30 lines
            # Stop at next major section
            if line.startswith("##"):
                break

            # Questions start after "verify you can" or similar
            if any(
                phrase in line.lower()
                for phrase in ["verify you can", "before moving", "can you"]
            ):
                in_questions = True
                continue

            # Extract numbered questions
            if in_questions:
                if match := re.match(r"\d+\.\s+(.+)", line):
                    questions.append(match.group(1).strip())

        if not questions:
            return None

        checkpoint_id = f"checkpoint-phase-{phase_number}"

        return Checkpoint(
            id=checkpoint_id,
            title=f"Phase {phase_number} Understanding Checkpoint",
            questions=questions,
            status=status,
        )

    def _parse_learning_team(self, lines: List[str]) -> Dict[str, str]:
        """Parse learning team section"""
        team = {}
        in_section = False

        for line in lines:
            if re.match(r"##\s+.*Learning Team", line, re.IGNORECASE):
                in_section = True
                continue

            if in_section and line.startswith("##"):
                break

            if not in_section:
                continue

            # Parse agent names and roles
            # Format: - **agent-name**: Role description
            if match := re.match(r"-\s+\*\*(.+?)\*\*:\s+(.+)", line):
                agent_name = match.group(1).strip()
                role = match.group(2).strip()
                team[agent_name] = role

        return team

    def _parse_milestones(self, lines: List[str]) -> List[str]:
        """Parse learning milestones"""
        milestones = []
        in_section = False

        for line in lines:
            if re.match(r"##\s+.*Milestones?", line, re.IGNORECASE):
                in_section = True
                continue

            if in_section and line.startswith("##"):
                break

            if not in_section:
                continue

            # Extract milestone items
            if line.strip().startswith("-"):
                milestone = line.strip()[1:].strip()
                # Remove checkbox if present
                milestone = re.sub(r"\[[ x]\]\s+", "", milestone)
                milestones.append(milestone)

        return milestones

    def _parse_journal_entries(self, lines: List[str]) -> List[JournalEntry]:
        """Parse learning journal entries"""
        entries = []
        in_journal = False
        current_entry = None
        current_entry_lines = []

        for i, line in enumerate(lines):
            # Find journal section
            if re.match(r"##\s+.*Learning Journal", line, re.IGNORECASE):
                in_journal = True
                continue

            # End of journal section
            if in_journal and line.startswith("##") and "journal" not in line.lower():
                # Save last entry
                if current_entry_lines:
                    entry_text = "\n".join(current_entry_lines)
                    entry = JournalEntry(
                        id=f"entry-{len(entries) + 1}",
                        raw_content=entry_text,
                        date=datetime.now(),
                    )
                    entries.append(entry)
                break

            if not in_journal:
                continue

            # Entry headers (### Date or ### Week N)
            if line.startswith("###"):
                # Save previous entry
                if current_entry_lines:
                    entry_text = "\n".join(current_entry_lines)
                    entry = JournalEntry(
                        id=f"entry-{len(entries) + 1}",
                        raw_content=entry_text,
                        date=datetime.now(),
                    )
                    entries.append(entry)

                current_entry_lines = [line]
            elif in_journal:
                current_entry_lines.append(line)

        return entries

    def _parse_resources(self, lines: List[str]) -> List[str]:
        """Parse resources section"""
        resources = []
        in_section = False

        for line in lines:
            if re.match(r"##\s+.*Resources?", line, re.IGNORECASE):
                in_section = True
                continue

            if in_section and line.startswith("##"):
                break

            if not in_section:
                continue

            # Extract resource items
            if line.strip().startswith("-"):
                resource = line.strip()[1:].strip()
                resources.append(resource)

        return resources

    def _parse_common_pitfalls(self, lines: List[str]) -> List[str]:
        """Parse common pitfalls section"""
        pitfalls = []
        in_section = False

        for line in lines:
            if re.match(r"##\s+.*Common Pitfalls?", line, re.IGNORECASE):
                in_section = True
                continue

            if in_section and line.startswith("##"):
                break

            if not in_section:
                continue

            # Pitfall headers (### 1. ...)
            if match := re.match(r"###\s+\d+\.\s+(.+)", line):
                pitfalls.append(match.group(1).strip())

        return pitfalls

    def _parse_date(self, date_str: str) -> datetime:
        """Parse a date string in various formats"""
        # Remove leading/trailing whitespace
        date_str = date_str.strip()

        # Try different formats
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m/%d/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If all formats fail, return current time
        return datetime.now()
