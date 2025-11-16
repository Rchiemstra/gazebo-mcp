"""
MCP Security Validator Operations.

Validates MCP server security configuration following Anthropic best practices.
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class OperationResult:
    """Result from an operation."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    duration: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class ErrorCodes:
    """Standard error codes."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    OPERATION_ERROR = "OPERATION_ERROR"


# Security best practices from Anthropic
ALLOWED_PATHS = ["workspace", "/tmp"]
BLOCKED_PATHS = ["/root", "~/.ssh", "~/.aws", "~/.config"]
RECOMMENDED_DOMAINS = ["api.anthropic.com", "pypi.org", "github.com"]
MAX_CPU_TIMEOUT = 30  # seconds
MAX_MEMORY_MB = 512
MAX_PROCESSES = 10


def _check_filesystem_isolation(server_path: Path) -> Dict[str, Any]:
    """Check filesystem isolation configuration."""
    issues = []
    score = 100

    # Check for server.py or config.py
    server_py = server_path / "server.py"
    config_py = server_path / "config.py"

    if not server_py.exists() and not config_py.exists():
        issues.append({
            'severity': 'high',
            'issue': 'No server.py or config.py found',
            'recommendation': 'Create server configuration file',
            'file': str(server_path)
        })
        score -= 30

    # Basic heuristic checks (simplified)
    # In a real implementation, would parse and analyze the files
    if server_py.exists():
        content = server_py.read_text()

        # Check for workspace directory configuration
        if 'workspace' not in content.lower():
            issues.append({
                'severity': 'medium',
                'issue': 'Workspace directory not configured',
                'recommendation': 'Configure workspace_dir parameter',
                'file': str(server_py)
            })
            score -= 15

    return {
        'score': score,
        'issues': issues,
        'checks_passed': 2 - len(issues),
        'checks_total': 2
    }


def _check_network_filtering(server_path: Path) -> Dict[str, Any]:
    """Check network filtering configuration."""
    issues = []
    score = 100

    config_py = server_path / "config.py"
    server_py = server_path / "server.py"

    config_found = False
    for file in [config_py, server_py]:
        if file.exists():
            content = file.read_text()
            if 'allowed_domains' in content.lower() or 'network' in content.lower():
                config_found = True
                break

    if not config_found:
        issues.append({
            'severity': 'high',
            'issue': 'Network filtering not configured',
            'recommendation': 'Configure allowed_domains list',
            'file': str(server_path)
        })
        score -= 40

    return {
        'score': score,
        'issues': issues,
        'checks_passed': 1 if config_found else 0,
        'checks_total': 1
    }


def _check_resource_limits(server_path: Path) -> Dict[str, Any]:
    """Check resource limits configuration."""
    issues = []
    score = 100

    # Check for timeout/limit configuration
    config_py = server_path / "config.py"
    server_py = server_path / "server.py"

    limits_configured = False
    for file in [config_py, server_py]:
        if file.exists():
            content = file.read_text()
            if any(keyword in content.lower() for keyword in ['timeout', 'memory_limit', 'cpu']):
                limits_configured = True
                break

    if not limits_configured:
        issues.append({
            'severity': 'medium',
            'issue': 'Resource limits not configured',
            'recommendation': f'Set CPU timeout (<= {MAX_CPU_TIMEOUT}s), memory limit (<= {MAX_MEMORY_MB}MB)',
            'file': str(server_path)
        })
        score -= 20

    return {
        'score': score,
        'issues': issues,
        'checks_passed': 1 if limits_configured else 0,
        'checks_total': 1
    }


def validate_server_security(
    server_path: str,
    response_format: str = "summary"
) -> OperationResult:
    """
    Validate MCP server security configuration.

    Args:
        server_path: Path to MCP server directory
        response_format: "summary" for score only, "complete" for all details

    Returns:
        OperationResult with security validation results

    Example:
        result = validate_server_security("mcp/servers/my-server/")
        if result.success:
            print(f"Security Score: {result.data['security_score']}/100")
    """
    start_time = time.time()

    try:
        server_dir = Path(server_path)

        if not server_dir.exists():
            return OperationResult(
                success=False,
                error=f"Server directory not found: {server_path}",
                error_code=ErrorCodes.FILE_NOT_FOUND,
                duration=time.time() - start_time
            )

        if not server_dir.is_dir():
            return OperationResult(
                success=False,
                error=f"Path is not a directory: {server_path}",
                error_code=ErrorCodes.VALIDATION_ERROR,
                duration=time.time() - start_time
            )

        # Run security checks
        filesystem_check = _check_filesystem_isolation(server_dir)
        network_check = _check_network_filtering(server_dir)
        resource_check = _check_resource_limits(server_dir)

        # Aggregate results
        all_issues = (
            filesystem_check['issues'] +
            network_check['issues'] +
            resource_check['issues']
        )

        # Calculate overall score (weighted average)
        overall_score = int(
            (filesystem_check['score'] * 0.4) +
            (network_check['score'] * 0.4) +
            (resource_check['score'] * 0.2)
        )

        # Count issues by severity
        critical = [i for i in all_issues if i['severity'] == 'critical']
        high = [i for i in all_issues if i['severity'] == 'high']
        medium = [i for i in all_issues if i['severity'] == 'medium']
        low = [i for i in all_issues if i['severity'] == 'low']

        # Total checks
        checks_passed = (
            filesystem_check['checks_passed'] +
            network_check['checks_passed'] +
            resource_check['checks_passed']
        )
        checks_total = (
            filesystem_check['checks_total'] +
            network_check['checks_total'] +
            resource_check['checks_total']
        )

        # Prepare response
        if response_format == "summary":
            data = {
                'security_score': overall_score,
                'checks_passed': checks_passed,
                'checks_total': checks_total,
                'issues_count': {
                    'critical': len(critical),
                    'high': len(high),
                    'medium': len(medium),
                    'low': len(low)
                },
                'production_ready': overall_score >= 90 and len(critical) == 0
            }
        else:  # complete
            data = {
                'security_score': overall_score,
                'checks_passed': checks_passed,
                'checks_failed': checks_total - checks_passed,
                'checks_total': checks_total,
                'issues': all_issues,
                'recommendations': [
                    "Review all high-severity issues",
                    "Configure filesystem isolation (workspace + /tmp only)",
                    "Set up network filtering with allowed domains",
                    "Configure resource limits (CPU, memory, processes)",
                    "Enable AST validation for code execution"
                ] if overall_score < 90 else ["Security configuration is good!"]
            }

        return OperationResult(
            success=True,
            data=data,
            duration=time.time() - start_time,
            metadata={
                'server_path': server_path,
                'format': response_format
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to validate server security: {str(e)}",
            error_code=ErrorCodes.OPERATION_ERROR,
            duration=time.time() - start_time
        )


def validate_sandbox_config(config: Dict[str, Any]) -> OperationResult:
    """
    Validate sandbox configuration dictionary.

    Args:
        config: Sandbox configuration dict with keys: filesystem, network, resources

    Returns:
        OperationResult with validation results

    Example:
        config = {
            "filesystem": {"allowed_paths": ["/workspace", "/tmp"]},
            "network": {"allowed_domains": ["api.anthropic.com"]},
            "resources": {"cpu_timeout": 30}
        }
        result = validate_sandbox_config(config)
    """
    start_time = time.time()

    try:
        issues = []
        score = 100

        # Check filesystem configuration
        if 'filesystem' not in config:
            issues.append({
                'severity': 'critical',
                'issue': 'Filesystem configuration missing',
                'recommendation': 'Add filesystem isolation config'
            })
            score -= 40
        else:
            fs = config['filesystem']
            if 'allowed_paths' not in fs:
                issues.append({
                    'severity': 'high',
                    'issue': 'Allowed paths not configured',
                    'recommendation': 'Configure allowed_paths list'
                })
                score -= 20

        # Check network configuration
        if 'network' not in config:
            issues.append({
                'severity': 'critical',
                'issue': 'Network configuration missing',
                'recommendation': 'Add network filtering config'
            })
            score -= 40
        else:
            net = config['network']
            if 'allowed_domains' not in net:
                issues.append({
                    'severity': 'high',
                    'issue': 'Allowed domains not configured',
                    'recommendation': 'Configure allowed_domains list'
                })
                score -= 20

        # Check resource limits
        if 'resources' not in config:
            issues.append({
                'severity': 'medium',
                'issue': 'Resource limits not configured',
                'recommendation': 'Add resource limits config'
            })
            score -= 20
        else:
            res = config['resources']
            if 'cpu_timeout' in res and res['cpu_timeout'] > MAX_CPU_TIMEOUT:
                issues.append({
                    'severity': 'medium',
                    'issue': f'CPU timeout too high ({res["cpu_timeout"]}s)',
                    'recommendation': f'Set CPU timeout <= {MAX_CPU_TIMEOUT}s'
                })
                score -= 10

        data = {
            'valid': score >= 70,
            'score': max(0, score),
            'issues': issues,
            'warnings': [i for i in issues if i['severity'] in ['medium', 'low']],
            'errors': [i for i in issues if i['severity'] in ['critical', 'high']]
        }

        return OperationResult(
            success=True,
            data=data,
            duration=time.time() - start_time
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Failed to validate sandbox config: {str(e)}",
            error_code=ErrorCodes.VALIDATION_ERROR,
            duration=time.time() - start_time
        )
