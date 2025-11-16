"""
Skill Invoker

Executes skill operations with standardized protocol.
"""

import time
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from .skill_loader import SkillLoader


class SkillError:
    """Error codes for skill invocation."""
    # Client errors (4xx)
    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    INVALID_OPERATION = "INVALID_OPERATION"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    VALIDATION_ERROR = "VALIDATION_ERROR"

    # Server errors (5xx)
    SKILL_ERROR = "SKILL_ERROR"
    TIMEOUT = "TIMEOUT"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass
class SkillRequest:
    """Request to invoke a skill."""
    skill_name: str
    operation: str
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    timeout: int = 60
    request_id: Optional[str] = None


@dataclass
class SkillResult:
    """Result from skill invocation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SkillMetrics:
    """Metrics for skill usage."""
    skill_name: str
    total_invocations: int = 0
    successful_invocations: int = 0
    failed_invocations: int = 0
    total_duration: float = 0.0
    avg_duration: float = 0.0
    max_duration: float = 0.0
    min_duration: float = float('inf')
    error_rate: float = 0.0
    errors_by_code: Dict[str, int] = field(default_factory=dict)


class SkillInvoker:
    """Invokes skills with standardized protocol."""

    def __init__(self, loader: SkillLoader):
        self.loader = loader
        self._metrics: Dict[str, SkillMetrics] = {}

    def invoke(
        self,
        skill_name: str,
        operation: str,
        params: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        timeout: int = 60
    ) -> SkillResult:
        """
        Invoke a skill operation.

        Args:
            skill_name: Name of the skill
            operation: Operation to perform
            params: Operation parameters
            context: Optional context information
            timeout: Timeout in seconds

        Returns:
            SkillResult
        """
        request = SkillRequest(
            skill_name=skill_name,
            operation=operation,
            parameters=params,
            context=context,
            timeout=timeout
        )

        return self._execute_request(request)

    async def invoke_async(
        self,
        skill_name: str,
        operation: str,
        params: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        timeout: int = 60
    ) -> SkillResult:
        """
        Invoke a skill operation asynchronously.

        Args:
            skill_name: Name of the skill
            operation: Operation to perform
            params: Operation parameters
            context: Optional context information
            timeout: Timeout in seconds

        Returns:
            SkillResult
        """
        request = SkillRequest(
            skill_name=skill_name,
            operation=operation,
            parameters=params,
            context=context,
            timeout=timeout
        )

        return await asyncio.get_event_loop().run_in_executor(
            None, self._execute_request, request
        )

    def invoke_batch(self, requests: List[SkillRequest]) -> List[SkillResult]:
        """
        Invoke multiple skills in batch.

        Args:
            requests: List of skill requests

        Returns:
            List of SkillResults (same order as requests)
        """
        results = []
        for request in requests:
            result = self._execute_request(request)
            results.append(result)

        return results

    def get_metrics(self, skill_name: str) -> Optional[SkillMetrics]:
        """
        Get metrics for a skill.

        Args:
            skill_name: Name of the skill

        Returns:
            SkillMetrics or None if no metrics available
        """
        return self._metrics.get(skill_name)

    def reset_metrics(self, skill_name: Optional[str] = None) -> None:
        """
        Reset metrics for a skill or all skills.

        Args:
            skill_name: Name of skill to reset, or None for all
        """
        if skill_name:
            if skill_name in self._metrics:
                self._metrics[skill_name] = SkillMetrics(skill_name=skill_name)
        else:
            self._metrics.clear()

    def _execute_request(self, request: SkillRequest) -> SkillResult:
        """Execute a skill request."""
        start_time = time.time()

        try:
            # Load skill if not loaded
            instance = self.loader.get_skill_instance(request.skill_name)
            if not instance:
                instance = self.loader.load_skill(request.skill_name)

            # Validate operation exists
            if request.operation not in instance.operations:
                # Try to find operation in module
                operation_func = self._find_operation(instance, request.operation)
                if not operation_func:
                    return self._error_result(
                        f"Operation '{request.operation}' not found in skill '{request.skill_name}'",
                        SkillError.INVALID_OPERATION,
                        time.time() - start_time,
                        request.skill_name
                    )
            else:
                operation_func = instance.operations[request.operation]

            # Execute operation
            try:
                # Call the operation
                result_data = operation_func(**request.parameters)

                # Check if result is an OperationResult from skills.*.operations
                if hasattr(result_data, 'success') and hasattr(result_data, 'data'):
                    # This is an OperationResult from the new operations interface
                    duration = result_data.duration if hasattr(result_data, 'duration') else (time.time() - start_time)

                    # Update metrics
                    self._update_metrics(request.skill_name, result_data.success, duration,
                                       result_data.error_code if hasattr(result_data, 'error_code') else None)

                    # Extract metadata from OperationResult
                    op_metadata = result_data.metadata if hasattr(result_data, 'metadata') else {}
                    combined_metadata = {
                        "skill_version": instance.metadata.version,
                        "operation": request.operation,
                        **op_metadata
                    }

                    return SkillResult(
                        success=result_data.success,
                        data=result_data.data,
                        error=result_data.error if hasattr(result_data, 'error') else None,
                        error_code=result_data.error_code if hasattr(result_data, 'error_code') else None,
                        duration=duration,
                        metadata=combined_metadata
                    )

                # Legacy: wrap result if not already a dict
                if not isinstance(result_data, dict):
                    result_data = {"result": result_data}

                duration = time.time() - start_time

                # Update metrics
                self._update_metrics(request.skill_name, True, duration, None)

                return SkillResult(
                    success=True,
                    data=result_data,
                    duration=duration,
                    metadata={
                        "skill_version": instance.metadata.version,
                        "operation": request.operation
                    }
                )

            except TypeError as e:
                # Parameter validation error
                return self._error_result(
                    f"Invalid parameters: {str(e)}",
                    SkillError.INVALID_PARAMETERS,
                    time.time() - start_time,
                    request.skill_name
                )

            except Exception as e:
                # Skill execution error
                return self._error_result(
                    f"Skill error: {str(e)}",
                    SkillError.SKILL_ERROR,
                    time.time() - start_time,
                    request.skill_name
                )

        except ValueError as e:
            # Skill not found or load error
            return self._error_result(
                str(e),
                SkillError.SKILL_NOT_FOUND,
                time.time() - start_time,
                request.skill_name
            )

        except Exception as e:
            # Internal error
            return self._error_result(
                f"Internal error: {str(e)}",
                SkillError.INTERNAL_ERROR,
                time.time() - start_time,
                request.skill_name
            )

    def _find_operation(self, instance, operation_name: str):
        """Try to find an operation function in the skill module."""
        # Try module level
        if hasattr(instance.module, operation_name):
            return getattr(instance.module, operation_name)

        # Try core submodule
        if hasattr(instance.module, 'core'):
            core = instance.module.core
            if hasattr(core, operation_name):
                return getattr(core, operation_name)

        # Try common class patterns
        class_names = [
            operation_name.title().replace('_', ''),
            operation_name.upper(),
            f"{instance.name.title().replace('-', '')}",
        ]

        for class_name in class_names:
            if hasattr(instance.module, class_name):
                cls = getattr(instance.module, class_name)
                # Try to instantiate and call
                try:
                    obj = cls()
                    if hasattr(obj, operation_name):
                        return getattr(obj, operation_name)
                    # Try __call__
                    if hasattr(obj, '__call__'):
                        return obj
                except:
                    pass

        return None

    def _error_result(
        self,
        error_message: str,
        error_code: str,
        duration: float,
        skill_name: str
    ) -> SkillResult:
        """Create an error result."""
        self._update_metrics(skill_name, False, duration, error_code)

        return SkillResult(
            success=False,
            error=error_message,
            error_code=error_code,
            duration=duration
        )

    def _update_metrics(
        self,
        skill_name: str,
        success: bool,
        duration: float,
        error_code: Optional[str]
    ) -> None:
        """Update metrics for a skill invocation."""
        if skill_name not in self._metrics:
            self._metrics[skill_name] = SkillMetrics(skill_name=skill_name)

        metrics = self._metrics[skill_name]
        metrics.total_invocations += 1
        metrics.total_duration += duration

        if success:
            metrics.successful_invocations += 1
        else:
            metrics.failed_invocations += 1
            if error_code:
                metrics.errors_by_code[error_code] = \
                    metrics.errors_by_code.get(error_code, 0) + 1

        # Update duration stats
        metrics.max_duration = max(metrics.max_duration, duration)
        metrics.min_duration = min(metrics.min_duration, duration)
        metrics.avg_duration = metrics.total_duration / metrics.total_invocations

        # Update error rate
        metrics.error_rate = metrics.failed_invocations / metrics.total_invocations
