"""
Coverage Analyzer for Test Orchestrator

Analyzes test coverage and identifies gaps.
"""

import subprocess
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class CoverageGap:
    """Represents a gap in test coverage."""
    file: str
    lines: List[int]
    description: str
    severity: str  # low, medium, high


@dataclass
class CoverageReport:
    """Test coverage analysis report."""
    overall_coverage: float
    files: Dict[str, float]  # file -> coverage percentage
    gaps: List[CoverageGap]
    missing_lines: Dict[str, List[int]]  # file -> list of uncovered lines


class CoverageAnalyzer:
    """Analyzes test coverage for Python code."""

    def analyze_coverage(self, source_dir: str = "src", test_dir: str = "tests") -> Optional[CoverageReport]:
        """
        Run coverage analysis on tests.

        Args:
            source_dir: Directory containing source code
            test_dir: Directory containing tests

        Returns:
            CoverageReport or None if coverage tools not available
        """
        try:
            # Run pytest with coverage
            result = subprocess.run(
                ["pytest", f"--cov={source_dir}", "--cov-report=json", test_dir],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Parse coverage report
            if Path("coverage.json").exists():
                return self._parse_coverage_json("coverage.json")
            else:
                return None

        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _parse_coverage_json(self, coverage_file: str) -> CoverageReport:
        """Parse coverage JSON report."""
        with open(coverage_file, 'r') as f:
            data = json.load(f)

        # Extract overall coverage
        totals = data.get("totals", {})
        overall_coverage = totals.get("percent_covered", 0.0)

        # Extract per-file coverage
        files = {}
        missing_lines = {}
        for file_path, file_data in data.get("files", {}).items():
            summary = file_data.get("summary", {})
            coverage = summary.get("percent_covered", 0.0)
            files[file_path] = coverage

            # Get missing lines
            missing = file_data.get("missing_lines", [])
            if missing:
                missing_lines[file_path] = missing

        # Identify coverage gaps
        gaps = self._identify_gaps(files, missing_lines)

        return CoverageReport(
            overall_coverage=overall_coverage,
            files=files,
            gaps=gaps,
            missing_lines=missing_lines
        )

    def _identify_gaps(self, files: Dict[str, float], missing_lines: Dict[str, List[int]]) -> List[CoverageGap]:
        """Identify significant coverage gaps."""
        gaps = []

        for file, coverage in files.items():
            if coverage < 50:
                gaps.append(CoverageGap(
                    file=file,
                    lines=missing_lines.get(file, []),
                    description=f"Low coverage: {coverage:.1f}%",
                    severity="high"
                ))
            elif coverage < 80:
                if file in missing_lines and len(missing_lines[file]) > 10:
                    gaps.append(CoverageGap(
                        file=file,
                        lines=missing_lines.get(file, []),
                        description=f"Medium coverage: {coverage:.1f}%, {len(missing_lines[file])} uncovered lines",
                        severity="medium"
                    ))

        return gaps

    def suggest_tests_for_gaps(self, gaps: List[CoverageGap]) -> List[str]:
        """
        Suggest test names for coverage gaps.

        Args:
            gaps: List of coverage gaps

        Returns:
            List of suggested test names
        """
        suggestions = []

        for gap in gaps:
            file_name = Path(gap.file).stem
            suggestions.append(f"test_{file_name}_uncovered_lines_{gap.lines[0] if gap.lines else 'unknown'}")

        return suggestions

    def calculate_improvement_needed(self, current: float, target: float, total_lines: int) -> int:
        """
        Calculate how many more lines need to be covered.

        Args:
            current: Current coverage percentage
            target: Target coverage percentage
            total_lines: Total lines in codebase

        Returns:
            Number of additional lines to cover
        """
        current_covered = (current / 100) * total_lines
        target_covered = (target / 100) * total_lines
        return int(target_covered - current_covered)
