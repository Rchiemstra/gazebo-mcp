"""
Unit tests for Spec to Implementation skill operations.

Tests verify that operations return proper OperationResult objects
with correct error handling and duration tracking.
"""

import unittest
from skills.spec_to_implementation.operations import OperationResult


class TestSpecToImplementationOperations(unittest.TestCase):
    """Test suite for Spec to Implementation operations."""

    def test_operation_result_structure(self):
        """Test that OperationResult has expected fields."""
        result = OperationResult(
            success=True,
            data={"test": "data"},
            duration=0.1
        )

        self.assertTrue(result.success)
        self.assertEqual(result.data, {"test": "data"})
        self.assertIsNone(result.error)
        self.assertIsNone(result.error_code)
        self.assertEqual(result.duration, 0.1)

    def test_operation_result_error(self):
        """Test error result structure."""
        result = OperationResult(
            success=False,
            error="Test error",
            error_code="TEST_ERROR",
            duration=0.05
        )

        self.assertFalse(result.success)
        self.assertEqual(result.error, "Test error")
        self.assertEqual(result.error_code, "TEST_ERROR")
        self.assertIsNone(result.data)


if __name__ == "__main__":
    unittest.main()
