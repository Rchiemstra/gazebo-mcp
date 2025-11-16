"""
Test Quality Scorer

Analyzes and scores the quality of generated tests.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import re


@dataclass
class QualityMetrics:
    """Quality metrics for generated tests."""
    completeness_score: float  # 0-100
    coverage_estimate: float  # 0-100
    assertion_quality: float  # 0-100
    test_variety_score: float  # 0-100
    mutation_score: Optional[float]  # 0-100, None if not run
    overall_score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


class TestQualityScorer:
    """Scores test quality based on various metrics."""

    def score_test_suite(
        self,
        test_code: str,
        num_tests: int,
        completeness_scores: List[float],
        test_types: List[str],
        mutation_score: Optional[float] = None
    ) -> QualityMetrics:
        """
        Score the overall quality of a test suite.

        Args:
            test_code: Generated test code
            num_tests: Number of tests
            completeness_scores: Individual test completeness scores
            test_types: Types of tests generated
            mutation_score: Optional mutation testing score (0-100)

        Returns:
            QualityMetrics with scores and analysis
        """
        # 1. Completeness Score
        avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0
        completeness_score = avg_completeness * 100

        # 2. Coverage Estimate (based on test types and variety)
        coverage_estimate = self._estimate_coverage(test_types, num_tests)

        # 3. Assertion Quality
        assertion_quality = self._analyze_assertion_quality(test_code)

        # 4. Test Variety Score
        variety_score = self._calculate_variety_score(test_types)

        # 5. Overall Score (weighted average)
        if mutation_score is not None:
            # Include mutation score in calculation
            overall_score = (
                completeness_score * 0.25 +
                coverage_estimate * 0.20 +
                assertion_quality * 0.20 +
                variety_score * 0.10 +
                mutation_score * 0.25
            )
        else:
            # Without mutation testing
            overall_score = (
                completeness_score * 0.35 +
                coverage_estimate * 0.25 +
                assertion_quality * 0.25 +
                variety_score * 0.15
            )

        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(
            completeness_score,
            coverage_estimate,
            assertion_quality,
            variety_score,
            test_code,
            test_types,
            mutation_score
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            completeness_score,
            coverage_estimate,
            assertion_quality,
            variety_score,
            test_code,
            mutation_score
        )

        return QualityMetrics(
            completeness_score=round(completeness_score, 1),
            coverage_estimate=round(coverage_estimate, 1),
            assertion_quality=round(assertion_quality, 1),
            test_variety_score=round(variety_score, 1),
            mutation_score=round(mutation_score, 1) if mutation_score is not None else None,
            overall_score=round(overall_score, 1),
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )

    def _estimate_coverage(self, test_types: List[str], num_tests: int) -> float:
        """Estimate test coverage based on test types."""
        # Base coverage from number of tests
        base_coverage = min(num_tests * 5, 50)  # Up to 50% from quantity

        # Bonus for test variety
        unique_types = set(test_types)
        variety_bonus = len(unique_types) * 10  # Up to 40% from variety

        # Bonus for edge cases
        edge_case_count = test_types.count('edge_case')
        edge_bonus = min(edge_case_count * 3, 15)

        # Bonus for parametrized tests
        parametrized_count = test_types.count('parametrized')
        param_bonus = min(parametrized_count * 5, 15)

        total = base_coverage + variety_bonus + edge_bonus + param_bonus
        return min(total, 100)

    def _analyze_assertion_quality(self, test_code: str) -> float:
        """Analyze quality of assertions."""
        score = 0.0

        # Count assertions
        assert_count = len(re.findall(r'\bassert\b', test_code))
        if assert_count > 0:
            score += 30

        # Check for specific assertions (not just "assert result")
        specific_assertions = len(re.findall(r'assert\s+\w+\s*(==|!=|<|>|in|is)', test_code))
        if specific_assertions > 0:
            score += 20

        # Check for isinstance checks
        isinstance_checks = len(re.findall(r'isinstance\(', test_code))
        if isinstance_checks > 0:
            score += 15

        # Check for multiple assertions per test (thorough testing)
        lines = test_code.split('\n')
        tests_with_multiple_asserts = 0
        current_test_asserts = 0
        in_test = False

        for line in lines:
            if line.strip().startswith('def test_'):
                if current_test_asserts > 1:
                    tests_with_multiple_asserts += 1
                current_test_asserts = 0
                in_test = True
            elif in_test and 'assert' in line:
                current_test_asserts += 1

        if tests_with_multiple_asserts > 0:
            score += 20

        # Penalty for TODOs in assertions
        todo_in_asserts = len(re.findall(r'assert.*#.*TODO', test_code))
        if todo_in_asserts > 0:
            score -= todo_in_asserts * 5

        # Penalty for generic assertions
        generic_asserts = len(re.findall(r'assert result is not None', test_code))
        if generic_asserts > 2:
            score -= (generic_asserts - 2) * 3

        return max(min(score, 100), 0)

    def _calculate_variety_score(self, test_types: List[str]) -> float:
        """Calculate test variety score."""
        if not test_types:
            return 0.0

        unique_types = set(test_types)
        type_distribution = {t: test_types.count(t) for t in unique_types}

        # Ideal distribution: mix of all types
        score = 0.0

        # Bonus for having multiple types
        score += len(unique_types) * 20

        # Check for good distribution (not all one type)
        max_count = max(type_distribution.values())
        if max_count / len(test_types) < 0.7:  # No single type dominates
            score += 20

        # Bonus for having edge cases
        if 'edge_case' in unique_types:
            score += 15

        # Bonus for having parametrized tests
        if 'parametrized' in unique_types:
            score += 15

        # Bonus for having exception tests
        if 'exception' in unique_types:
            score += 15

        return min(score, 100)

    def _identify_strengths_weaknesses(
        self,
        completeness: float,
        coverage: float,
        assertion: float,
        variety: float,
        test_code: str,
        test_types: List[str],
        mutation_score: Optional[float] = None
    ) -> tuple[List[str], List[str]]:
        """Identify strengths and weaknesses."""
        strengths = []
        weaknesses = []

        # Completeness
        if completeness >= 80:
            strengths.append("High completeness - most tests are fully implemented")
        elif completeness < 50:
            weaknesses.append("Low completeness - many tests need manual completion")

        # Coverage
        if coverage >= 70:
            strengths.append("Good estimated coverage from test variety")
        elif coverage < 50:
            weaknesses.append("Limited coverage - need more diverse test cases")

        # Assertions
        if assertion >= 70:
            strengths.append("Strong assertions - tests validate behavior thoroughly")
        elif assertion < 50:
            weaknesses.append("Weak assertions - tests lack specific validations")

        # Variety
        if variety >= 70:
            strengths.append("Excellent test variety - multiple test types")
        elif variety < 50:
            weaknesses.append("Limited test variety - mostly one type of test")

        # Mutation Testing
        if mutation_score is not None:
            if mutation_score >= 80:
                strengths.append(f"Excellent mutation score ({mutation_score:.0f}%) - tests catch most code changes")
            elif mutation_score >= 60:
                strengths.append(f"Good mutation score ({mutation_score:.0f}%) - tests detect many defects")
            elif mutation_score < 40:
                weaknesses.append(f"Low mutation score ({mutation_score:.0f}%) - tests miss many code changes")

        # Check for specific patterns
        if 'edge_case' in test_types:
            strengths.append("Includes edge case testing")
        else:
            weaknesses.append("No edge case tests generated")

        if 'exception' in test_types:
            strengths.append("Tests exception handling")
        else:
            weaknesses.append("No exception handling tests")

        # Check for TODOs
        todo_count = len(re.findall(r'TODO', test_code))
        if todo_count == 0:
            strengths.append("No TODOs - tests are complete")
        elif todo_count > 10:
            weaknesses.append(f"Many TODOs ({todo_count}) requiring manual completion")

        return strengths, weaknesses

    def _generate_recommendations(
        self,
        completeness: float,
        coverage: float,
        assertion: float,
        variety: float,
        test_code: str,
        mutation_score: Optional[float] = None
    ) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []

        if completeness < 70:
            recommendations.append(
                "Review and complete TODOs in generated tests"
            )

        if coverage < 60:
            recommendations.append(
                "Add more test cases to improve coverage"
            )

        if assertion < 60:
            recommendations.append(
                "Strengthen assertions - add specific checks for expected behavior"
            )

        if variety < 60:
            recommendations.append(
                "Add more test variety - include edge cases, exceptions, and parametrized tests"
            )

        # Mutation testing recommendations
        if mutation_score is not None:
            if mutation_score < 70:
                recommendations.append(
                    f"Improve mutation score ({mutation_score:.0f}%) - add tests that verify specific behaviors"
                )
            if mutation_score < 50:
                recommendations.append(
                    "Review survived mutations to identify gaps in test coverage"
                )

        # Specific recommendations
        if 'TODO' in test_code and 'parametrize' in test_code:
            recommendations.append(
                "Fill in parametrized test case values with realistic data"
            )

        if test_code.count('assert result is not None') > 5:
            recommendations.append(
                "Replace generic assertions with specific checks for expected values"
            )

        if 'mock' in test_code.lower():
            recommendations.append(
                "Configure mocks with expected return values for more realistic tests"
            )

        # Always good practices
        if not recommendations:
            recommendations.append("Run tests and verify they pass")
            recommendations.append("Measure actual coverage with pytest-cov")
            recommendations.append("Review tests for business logic accuracy")

        return recommendations


def score_test_quality(
    test_code: str,
    num_tests: int,
    completeness_scores: List[float],
    test_types: List[str],
    mutation_score: Optional[float] = None
) -> QualityMetrics:
    """
    Convenience function to score test quality.

    Args:
        test_code: Generated test code
        num_tests: Number of tests
        completeness_scores: Individual test completeness scores
        test_types: Types of tests generated
        mutation_score: Optional mutation testing score (0-100)

    Returns:
        QualityMetrics with analysis
    """
    scorer = TestQualityScorer()
    return scorer.score_test_suite(test_code, num_tests, completeness_scores, test_types, mutation_score)
