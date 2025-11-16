#!/usr/bin/env python3
"""
Unit tests for Skill Evaluator - Phase 1

Basic tests to validate core functionality.
"""

import unittest
import tempfile
import shutil
import time
from pathlib import Path

from skills.skill_evaluator.core.models import (
    ExecutionRecord,
    ExecutionContext,
    ImprovementSuggestion,
    SkillEvaluationMetrics,
    QualityScores,
    PerformanceScores,
    ReliabilityScores,
    CodeQualityScores,
    ImprovementCategory,
    ImprovementSeverity,
    HealthTrend
)
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker
from skills.skill_evaluator.core.monitor import ExecutionMonitor
from skills.skill_evaluator.core.quality_evaluator import QualityEvaluator


class TestModels(unittest.TestCase):
    """Test core data models."""

    def test_improvement_suggestion_creation(self):
        """Test creating an improvement suggestion."""
        suggestion = ImprovementSuggestion(
            category=ImprovementCategory.PERFORMANCE.value,
            severity=ImprovementSeverity.HIGH.value,
            description="Optimize database queries",
            expected_impact="30% faster execution"
        )

        self.assertEqual(suggestion.category, "performance")
        self.assertEqual(suggestion.severity, "high")
        self.assertIsNotNone(suggestion.id)
        self.assertTrue(suggestion.confidence >= 0 and suggestion.confidence <= 1)

    def test_execution_context_creation(self):
        """Test creating an execution context."""
        context = ExecutionContext(
            skill_name="test-skill",
            operation="test-op",
            parameters={"key": "value"}
        )

        self.assertEqual(context.skill_name, "test-skill")
        self.assertEqual(context.operation, "test-op")
        self.assertIsNotNone(context.execution_id)
        self.assertTrue(context.timestamp > 0)

    def test_execution_record_serialization(self):
        """Test execution record to/from dict."""
        record = ExecutionRecord(
            execution_id="test-123",
            skill_name="test-skill",
            operation="test-op",
            parameters={"param": "value"},
            success=True,
            duration=1.5,
            timestamp=time.time()
        )

        # Convert to dict
        data = record.to_dict()
        self.assertEqual(data['execution_id'], "test-123")
        self.assertEqual(data['skill_name'], "test-skill")

        # Convert back from dict
        restored = ExecutionRecord.from_dict(data)
        self.assertEqual(restored.execution_id, record.execution_id)
        self.assertEqual(restored.skill_name, record.skill_name)

    def test_skill_evaluation_metrics(self):
        """Test skill evaluation metrics calculation."""
        metrics = SkillEvaluationMetrics(skill_name="test-skill")

        # Set sub-scores
        metrics.quality_scores = QualityScores(
            output_quality_score=80,
            correctness_score=85,
            consistency_score=90,
            completeness_score=75
        )

        metrics.performance_scores = PerformanceScores(
            performance_score=85,
            resource_efficiency=80
        )

        metrics.reliability_scores = ReliabilityScores(
            reliability_score=90,
            error_handling_quality=85,
            recovery_capability=80,
            success_rate=90,
            error_rate=10
        )

        metrics.code_quality_scores = CodeQualityScores(
            code_quality_score=75,
            maintainability_index=80,
            complexity_score=30,
            test_coverage=70,
            documentation_score=75
        )

        # Calculate overall health
        health_score = metrics.calculate_overall_health()

        self.assertTrue(health_score > 0)
        self.assertTrue(health_score <= 100)
        self.assertIn(metrics.get_health_grade(), ['A', 'B', 'C', 'D', 'F'])


class TestHistoryTracker(unittest.TestCase):
    """Test execution history tracker."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ExecutionHistoryTracker(storage_dir=self.temp_dir)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_record_execution(self):
        """Test recording an execution."""
        record = ExecutionRecord(
            execution_id="test-1",
            skill_name="test-skill",
            operation="test-op",
            parameters={},
            success=True,
            duration=1.0,
            timestamp=time.time()
        )

        self.tracker.record_execution(record)

        # Retrieve it
        retrieved = self.tracker.get_execution_by_id("test-1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.execution_id, "test-1")

    def test_get_recent_executions(self):
        """Test getting recent executions."""
        # Record multiple executions
        for i in range(10):
            record = ExecutionRecord(
                execution_id=f"test-{i}",
                skill_name="test-skill",
                operation="test-op",
                parameters={},
                success=True,
                duration=1.0 + i * 0.1,
                timestamp=time.time() - (10 - i) * 60
            )
            self.tracker.record_execution(record)

        # Get recent 5
        recent = self.tracker.get_recent_executions("test-skill", limit=5)
        self.assertEqual(len(recent), 5)

        # Should be sorted by timestamp descending
        self.assertTrue(recent[0].timestamp >= recent[-1].timestamp)

    def test_execution_stats(self):
        """Test execution statistics."""
        # Record some successes and failures
        for i in range(10):
            record = ExecutionRecord(
                execution_id=f"test-{i}",
                skill_name="test-skill",
                operation="test-op",
                parameters={},
                success=i < 8,  # 8 successes, 2 failures
                duration=1.0 + i * 0.1,
                timestamp=time.time(),
                error="Error" if i >= 8 else None,
                error_code="TEST_ERROR" if i >= 8 else None
            )
            self.tracker.record_execution(record)

        stats = self.tracker.get_execution_stats("test-skill")

        self.assertEqual(stats['total_executions'], 10)
        self.assertEqual(stats['successful_executions'], 8)
        self.assertEqual(stats['failed_executions'], 2)
        self.assertEqual(stats['success_rate'], 80.0)
        self.assertEqual(stats['error_rate'], 20.0)
        self.assertTrue(stats['avg_duration'] > 0)

    def test_failed_executions(self):
        """Test getting failed executions."""
        # Record some failures
        for i in range(5):
            record = ExecutionRecord(
                execution_id=f"test-{i}",
                skill_name="test-skill",
                operation="test-op",
                parameters={},
                success=False,
                duration=1.0,
                timestamp=time.time(),
                error="Test error",
                error_code="TEST_ERROR"
            )
            self.tracker.record_execution(record)

        failed = self.tracker.get_failed_executions("test-skill")
        self.assertEqual(len(failed), 5)
        for record in failed:
            self.assertFalse(record.success)

    def test_performance_baseline(self):
        """Test performance baseline calculation."""
        # Record enough executions for baseline
        for i in range(20):
            record = ExecutionRecord(
                execution_id=f"test-{i}",
                skill_name="test-skill",
                operation="test-op",
                parameters={},
                success=True,
                duration=1.0 + (i % 5) * 0.1,
                timestamp=time.time()
            )
            self.tracker.record_execution(record)

        baseline = self.tracker.get_performance_baseline("test-skill", days=1)

        self.assertIsNotNone(baseline)
        self.assertTrue(baseline['avg_duration'] > 0)
        self.assertTrue(baseline['sample_size'] >= 10)


class TestExecutionMonitor(unittest.TestCase):
    """Test execution monitor."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ExecutionHistoryTracker(storage_dir=self.temp_dir)
        self.monitor = ExecutionMonitor(self.tracker)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pre_execution_check(self):
        """Test pre-execution check."""
        context = self.monitor.pre_execution_check(
            skill_name="test-skill",
            operation="test-op",
            parameters={"key": "value"}
        )

        self.assertIsNotNone(context)
        self.assertEqual(context.skill_name, "test-skill")
        self.assertEqual(context.operation, "test-op")
        self.assertIsNotNone(context.execution_id)

    def test_post_execution_analysis(self):
        """Test post-execution analysis."""
        # Pre-execution
        context = self.monitor.pre_execution_check(
            "test-skill", "test-op", {}
        )

        # Simulate some work
        time.sleep(0.1)

        # Post-execution
        analysis = self.monitor.post_execution_analysis(
            execution_id=context.execution_id,
            success=True,
            result_data={"result": "success"}
        )

        self.assertIsNotNone(analysis)
        self.assertIn('warnings', analysis)
        self.assertIn('recommendations', analysis)
        self.assertIn('performance_profile', analysis)

        # Check that record was saved
        record = self.tracker.get_execution_by_id(context.execution_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.execution_id, context.execution_id)

    def test_monitoring_summary(self):
        """Test monitoring summary."""
        # Record some executions first
        for i in range(10):
            context = self.monitor.pre_execution_check(
                "test-skill", "test-op", {}
            )
            self.monitor.post_execution_analysis(
                execution_id=context.execution_id,
                success=True
            )

        summary = self.monitor.get_monitoring_summary("test-skill", time_period_days=1)

        self.assertEqual(summary['skill_name'], "test-skill")
        self.assertIn('health_status', summary)
        self.assertIn('trend', summary)
        self.assertTrue(summary['total_executions'] >= 10)


class TestQualityEvaluator(unittest.TestCase):
    """Test quality evaluator."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = ExecutionHistoryTracker(storage_dir=self.temp_dir)
        self.evaluator = QualityEvaluator(self.tracker)

        # Add some test data
        for i in range(30):
            record = ExecutionRecord(
                execution_id=f"test-{i}",
                skill_name="test-skill",
                operation="test-op",
                parameters={},
                success=i < 25,  # 25 successes, 5 failures
                duration=1.0 + i * 0.05,
                timestamp=time.time() - (30 - i) * 3600,
                error="Error" if i >= 25 else None,
                error_code="TEST_ERROR" if i >= 25 else None,
                result_data={"data": "value"} if i < 25 else None
            )
            self.tracker.record_execution(record)

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_evaluate(self):
        """Test comprehensive evaluation."""
        metrics = self.evaluator.evaluate(
            skill_name="test-skill",
            execution_samples=30,
            include_code_analysis=True
        )

        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.skill_name, "test-skill")
        self.assertTrue(metrics.overall_health_score > 0)
        self.assertIn(metrics.health_trend, [t.value for t in HealthTrend])

    def test_quality_scores(self):
        """Test quality score calculation."""
        metrics = self.evaluator.evaluate("test-skill", execution_samples=30)

        self.assertTrue(metrics.quality_scores.overall_score() > 0)
        self.assertTrue(metrics.quality_scores.overall_score() <= 100)

    def test_performance_scores(self):
        """Test performance score calculation."""
        metrics = self.evaluator.evaluate("test-skill", execution_samples=30)

        self.assertTrue(metrics.performance_scores.overall_score() > 0)
        self.assertTrue(metrics.performance_scores.overall_score() <= 100)

    def test_reliability_scores(self):
        """Test reliability score calculation."""
        metrics = self.evaluator.evaluate("test-skill", execution_samples=30)

        self.assertTrue(metrics.reliability_scores.overall_score() > 0)
        self.assertTrue(metrics.reliability_scores.overall_score() <= 100)
        # With 5 failures out of 30, success rate should be ~83%
        self.assertTrue(80 <= metrics.reliability_scores.success_rate <= 90)

    def test_strengths_and_weaknesses(self):
        """Test identification of strengths and weaknesses."""
        metrics = self.evaluator.evaluate("test-skill", execution_samples=30)

        self.assertIsInstance(metrics.strengths, list)
        self.assertIsInstance(metrics.weaknesses, list)

    def test_improvement_suggestions(self):
        """Test improvement suggestion generation."""
        metrics = self.evaluator.evaluate("test-skill", execution_samples=30)

        self.assertIsInstance(metrics.improvement_opportunities, list)
        # May or may not have suggestions depending on the scores


def run_tests():
    """Run all tests."""
    print("Running Skill Evaluator Unit Tests (Phase 1)")
    print("=" * 70)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestHistoryTracker))
    suite.addTests(loader.loadTestsFromTestCase(TestExecutionMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityEvaluator))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
