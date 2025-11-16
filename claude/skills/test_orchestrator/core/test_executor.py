"""
Test Executor for Test Orchestrator

Executes generated tests and validates them.
"""

import subprocess
import tempfile
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TestResult:
    """Result of running a test."""
    test_name: str
    passed: bool
    error_message: Optional[str] = None
    duration: float = 0.0


@dataclass
class ExecutionReport:
    """Report from test execution."""
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration: float
    test_results: List[TestResult]
    syntax_valid: bool = True
    syntax_errors: List[str] = None


class TestExecutor:
    """Executes and validates generated tests."""

    def validate_syntax(self, test_code: str) -> tuple[bool, List[str]]:
        """
        Validate Python syntax of generated test code.

        Args:
            test_code: Test file content

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        try:
            compile(test_code, '<string>', 'exec')
            return True, []
        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return False, errors
        except Exception as e:
            errors.append(f"Compilation error: {str(e)}")
            return False, errors

    def execute_tests(
        self,
        test_file_path: str,
        source_file_path: Optional[str] = None,
        timeout: int = 60
    ) -> ExecutionReport:
        """
        Execute tests using pytest.

        Args:
            test_file_path: Path to test file
            source_file_path: Path to source file being tested
            timeout: Timeout in seconds

        Returns:
            ExecutionReport with results
        """
        # Check if test file exists
        if not Path(test_file_path).exists():
            return ExecutionReport(
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                duration=0.0,
                test_results=[],
                syntax_valid=False,
                syntax_errors=[f"Test file not found: {test_file_path}"]
            )

        try:
            # Run pytest with JSON report
            result = subprocess.run(
                [
                    "pytest",
                    test_file_path,
                    "-v",
                    "--tb=short",
                    "--json-report",
                    "--json-report-file=test_report.json",
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path(test_file_path).parent
            )

            # Parse JSON report if available
            report_file = Path(test_file_path).parent / "test_report.json"
            if report_file.exists():
                return self._parse_json_report(report_file)
            else:
                # Fallback: parse text output
                return self._parse_text_output(result.stdout, result.returncode)

        except subprocess.TimeoutExpired:
            return ExecutionReport(
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                duration=timeout,
                test_results=[],
                syntax_valid=True,
                syntax_errors=[f"Test execution timed out after {timeout}s"]
            )
        except FileNotFoundError:
            return ExecutionReport(
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                duration=0.0,
                test_results=[],
                syntax_valid=True,
                syntax_errors=["pytest not found. Install with: pip install pytest"]
            )
        except Exception as e:
            return ExecutionReport(
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                duration=0.0,
                test_results=[],
                syntax_valid=True,
                syntax_errors=[f"Execution error: {str(e)}"]
            )

    def _parse_json_report(self, report_file: Path) -> ExecutionReport:
        """Parse pytest JSON report."""
        with open(report_file, 'r') as f:
            data = json.load(f)

        summary = data.get('summary', {})
        test_results = []

        for test in data.get('tests', []):
            test_results.append(TestResult(
                test_name=test.get('nodeid', 'unknown'),
                passed=test.get('outcome') == 'passed',
                error_message=test.get('call', {}).get('longrepr') if test.get('outcome') != 'passed' else None,
                duration=test.get('duration', 0.0)
            ))

        return ExecutionReport(
            total_tests=summary.get('total', 0),
            passed=summary.get('passed', 0),
            failed=summary.get('failed', 0),
            errors=summary.get('error', 0),
            skipped=summary.get('skipped', 0),
            duration=data.get('duration', 0.0),
            test_results=test_results,
            syntax_valid=True
        )

    def _parse_text_output(self, output: str, return_code: int) -> ExecutionReport:
        """Parse pytest text output (fallback)."""
        lines = output.split('\n')

        # Simple parsing of summary line
        # Example: "5 passed, 2 failed in 1.23s"
        passed = failed = errors = skipped = 0
        duration = 0.0

        for line in lines:
            if ' passed' in line or ' failed' in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed':
                        passed = int(parts[i-1])
                    elif part == 'failed':
                        failed = int(parts[i-1])
                    elif part == 'error':
                        errors = int(parts[i-1])
                    elif part == 'skipped':
                        skipped = int(parts[i-1])
                    elif 'in' in part and i+1 < len(parts):
                        try:
                            duration = float(parts[i+1].rstrip('s'))
                        except:
                            pass

        total = passed + failed + errors + skipped

        return ExecutionReport(
            total_tests=total,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            duration=duration,
            test_results=[],
            syntax_valid=return_code != 2  # Exit code 2 is syntax error
        )

    def dry_run(self, test_code: str) -> Dict[str, any]:
        """
        Perform a dry run - syntax check without execution.

        Args:
            test_code: Test file content

        Returns:
            Dict with validation results
        """
        syntax_valid, errors = self.validate_syntax(test_code)

        return {
            'syntax_valid': syntax_valid,
            'errors': errors,
            'can_execute': syntax_valid and 'pytest' in test_code
        }
