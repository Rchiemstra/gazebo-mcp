"""
Output Validator

Validates program output against expected results.
"""

import json
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from difflib import unified_diff


@dataclass
class OutputValidationResult:
    """Result of output validation"""
    is_match: bool
    differences: List[str] = field(default_factory=list)
    similarity_score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


class OutputValidator:
    """Validates program output"""

    def validate_exact(self, expected: str, actual: str) -> OutputValidationResult:
        """
        Validate exact match.

        Args:
            expected: Expected output
            actual: Actual output

        Returns:
            OutputValidationResult
        """
        is_match = expected == actual

        if not is_match:
            # Generate diff
            diff = list(unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                lineterm='',
                fromfile='expected',
                tofile='actual'
            ))
            differences = diff if diff else [f"Expected: {expected!r}", f"Actual: {actual!r}"]
        else:
            differences = []

        return OutputValidationResult(
            is_match=is_match,
            differences=differences,
            similarity_score=1.0 if is_match else 0.0,
            details={'match_type': 'exact'}
        )

    def validate_contains(self, expected: str, actual: str) -> OutputValidationResult:
        """
        Validate that actual contains expected.

        Args:
            expected: Expected substring
            actual: Actual output

        Returns:
            OutputValidationResult
        """
        is_match = expected in actual

        differences = [] if is_match else [
            f"Expected to find: {expected!r}",
            f"In output: {actual!r}"
        ]

        return OutputValidationResult(
            is_match=is_match,
            differences=differences,
            similarity_score=1.0 if is_match else 0.0,
            details={'match_type': 'contains'}
        )

    def validate_regex(self, pattern: str, actual: str) -> OutputValidationResult:
        """
        Validate using regex pattern.

        Args:
            pattern: Regex pattern
            actual: Actual output

        Returns:
            OutputValidationResult
        """
        try:
            match = re.search(pattern, actual)
            is_match = match is not None

            differences = [] if is_match else [
                f"Pattern: {pattern}",
                f"Did not match: {actual!r}"
            ]

            details = {'match_type': 'regex', 'pattern': pattern}
            if match:
                details['matched_groups'] = match.groups()

            return OutputValidationResult(
                is_match=is_match,
                differences=differences,
                similarity_score=1.0 if is_match else 0.0,
                details=details
            )
        except re.error as e:
            return OutputValidationResult(
                is_match=False,
                differences=[f"Invalid regex pattern: {e}"],
                similarity_score=0.0,
                details={'match_type': 'regex', 'error': str(e)}
            )

    def validate_json(self, expected: Union[str, Dict, List], actual: str) -> OutputValidationResult:
        """
        Validate JSON output.

        Args:
            expected: Expected JSON (string or object)
            actual: Actual JSON output (string)

        Returns:
            OutputValidationResult
        """
        try:
            # Parse expected if string
            if isinstance(expected, str):
                expected_obj = json.loads(expected)
            else:
                expected_obj = expected

            # Parse actual
            actual_obj = json.loads(actual)

            # Compare
            is_match = expected_obj == actual_obj

            if not is_match:
                differences = [
                    f"Expected JSON: {json.dumps(expected_obj, indent=2)}",
                    f"Actual JSON: {json.dumps(actual_obj, indent=2)}"
                ]
            else:
                differences = []

            return OutputValidationResult(
                is_match=is_match,
                differences=differences,
                similarity_score=1.0 if is_match else self._json_similarity(expected_obj, actual_obj),
                details={'match_type': 'json'}
            )

        except json.JSONDecodeError as e:
            return OutputValidationResult(
                is_match=False,
                differences=[f"JSON parse error: {e}"],
                similarity_score=0.0,
                details={'match_type': 'json', 'error': str(e)}
            )

    def validate_lines(self, expected_lines: List[str], actual: str, order_matters: bool = True) -> OutputValidationResult:
        """
        Validate line-by-line output.

        Args:
            expected_lines: List of expected lines
            actual: Actual output
            order_matters: Whether line order matters

        Returns:
            OutputValidationResult
        """
        actual_lines = [line.strip() for line in actual.strip().split('\n')]
        expected_lines = [line.strip() for line in expected_lines]

        if order_matters:
            is_match = expected_lines == actual_lines
            if not is_match:
                diff = list(unified_diff(expected_lines, actual_lines, lineterm=''))
                differences = diff
            else:
                differences = []
        else:
            # Check if all expected lines are present (unordered)
            expected_set = set(expected_lines)
            actual_set = set(actual_lines)

            missing = expected_set - actual_set
            extra = actual_set - expected_set

            is_match = len(missing) == 0 and len(extra) == 0

            differences = []
            if missing:
                differences.append(f"Missing lines: {missing}")
            if extra:
                differences.append(f"Extra lines: {extra}")

        # Calculate similarity
        if is_match:
            similarity = 1.0
        else:
            matching = sum(1 for line in expected_lines if line in actual_lines)
            similarity = matching / max(len(expected_lines), len(actual_lines)) if expected_lines or actual_lines else 0.0

        return OutputValidationResult(
            is_match=is_match,
            differences=differences,
            similarity_score=similarity,
            details={'match_type': 'lines', 'order_matters': order_matters}
        )

    def _json_similarity(self, expected: Any, actual: Any) -> float:
        """Calculate similarity between JSON objects"""
        if expected == actual:
            return 1.0

        # Simple similarity based on matching keys/values
        if isinstance(expected, dict) and isinstance(actual, dict):
            all_keys = set(expected.keys()) | set(actual.keys())
            if not all_keys:
                return 0.0

            matching = sum(1 for key in all_keys if expected.get(key) == actual.get(key))
            return matching / len(all_keys)

        elif isinstance(expected, list) and isinstance(actual, list):
            if not expected and not actual:
                return 1.0
            if not expected or not actual:
                return 0.0

            matching = sum(1 for i in range(min(len(expected), len(actual))) if expected[i] == actual[i])
            return matching / max(len(expected), len(actual))

        return 0.0
