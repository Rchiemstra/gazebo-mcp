"""
Network Proxy for Domain Filtering.

Implements secure network isolation for sandboxed code execution:
- Whitelist-based domain filtering
- Prevents data exfiltration
- Logs all network attempts
- Part of 84% permission prompt reduction strategy

Based on Anthropic's sandboxing best practices:
"Both filesystem and network isolation are required together"
"""

import urllib.request
import urllib.error
import urllib.parse
import socket
import ssl
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class NetworkLog:
    """Log entry for network request."""
    timestamp: datetime
    url: str
    allowed: bool
    reason: Optional[str] = None


class NetworkProxy:
    """
    Network proxy with domain whitelisting.

    Intercepts network requests and only allows approved domains.
    Prevents malicious code from exfiltrating data.

    Example:
        proxy = NetworkProxy(allowed_domains=[
            "api.anthropic.com",
            "pypi.org",
            "github.com"
        ])

        # This will succeed
        data = proxy.fetch("https://api.anthropic.com/v1/messages")

        # This will be blocked
        data = proxy.fetch("https://evil.com/steal-data")  # Raises PermissionError
    """

    def __init__(
        self,
        allowed_domains: Optional[List[str]] = None,
        log_requests: bool = True
    ):
        """
        Initialize network proxy.

        Args:
            allowed_domains: List of allowed domains (default: Anthropic, PyPI, GitHub)
            log_requests: Whether to log network requests
        """
        self.allowed_domains = allowed_domains or [
            "api.anthropic.com",
            "pypi.org",
            "github.com",
            "files.pythonhosted.org",  # For pip installs
            "raw.githubusercontent.com",  # For GitHub raw content
        ]
        self.log_requests = log_requests
        self.request_log: List[NetworkLog] = []

    def is_domain_allowed(self, url: str) -> tuple[bool, Optional[str]]:
        """
        Check if a URL's domain is allowed.

        Args:
            url: URL to check

        Returns:
            (is_allowed, reason) tuple
        """
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()

            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]

            # Check against whitelist
            for allowed in self.allowed_domains:
                if domain == allowed or domain.endswith('.' + allowed):
                    return True, None

            return False, f"Domain '{domain}' not in allowed list: {', '.join(self.allowed_domains)}"

        except Exception as e:
            return False, f"Error parsing URL: {str(e)}"

    def fetch(
        self,
        url: str,
        method: str = "GET",
        data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> bytes:
        """
        Fetch URL with domain filtering.

        Args:
            url: URL to fetch
            method: HTTP method (GET, POST, etc.)
            data: Request body (for POST/PUT)
            headers: HTTP headers
            timeout: Request timeout in seconds

        Returns:
            Response body as bytes

        Raises:
            PermissionError: If domain is not allowed
            urllib.error.URLError: If request fails
        """
        # Check domain
        is_allowed, reason = self.is_domain_allowed(url)

        # Log request
        if self.log_requests:
            self.request_log.append(NetworkLog(
                timestamp=datetime.now(),
                url=url,
                allowed=is_allowed,
                reason=reason
            ))

        if not is_allowed:
            raise PermissionError(
                f"Network request blocked: {reason}\n"
                f"URL: {url}\n"
                f"Allowed domains: {', '.join(self.allowed_domains)}"
            )

        # Make request
        try:
            req = urllib.request.Request(
                url,
                data=data,
                headers=headers or {},
                method=method
            )

            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()

        except urllib.error.HTTPError as e:
            raise urllib.error.URLError(
                f"HTTP {e.code} error: {e.reason}"
            ) from e
        except urllib.error.URLError as e:
            raise urllib.error.URLError(
                f"Network error: {e.reason}"
            ) from e

    def fetch_json(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ) -> Any:
        """
        Fetch JSON from URL with domain filtering.

        Args:
            url: URL to fetch
            method: HTTP method
            data: JSON data (will be serialized)
            headers: HTTP headers
            timeout: Request timeout

        Returns:
            Parsed JSON response

        Raises:
            PermissionError: If domain not allowed
            ValueError: If response is not valid JSON
        """
        # Prepare data
        body = None
        if data:
            body = json.dumps(data).encode('utf-8')
            if headers is None:
                headers = {}
            headers['Content-Type'] = 'application/json'

        # Fetch
        response_bytes = self.fetch(url, method, body, headers, timeout)

        # Parse JSON
        try:
            return json.loads(response_bytes.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {str(e)}")

    def get_log(self) -> List[Dict[str, Any]]:
        """
        Get network request log.

        Returns:
            List of log entries as dictionaries
        """
        return [
            {
                "timestamp": log.timestamp.isoformat(),
                "url": log.url,
                "allowed": log.allowed,
                "reason": log.reason
            }
            for log in self.request_log
        ]

    def clear_log(self):
        """Clear network request log."""
        self.request_log.clear()

    def add_allowed_domain(self, domain: str):
        """
        Add a domain to the whitelist.

        Args:
            domain: Domain to allow (e.g., "example.com")
        """
        if domain not in self.allowed_domains:
            self.allowed_domains.append(domain)

    def remove_allowed_domain(self, domain: str):
        """
        Remove a domain from the whitelist.

        Args:
            domain: Domain to remove
        """
        if domain in self.allowed_domains:
            self.allowed_domains.remove(domain)


class MonkeyPatchedNetworkProxy(NetworkProxy):
    """
    Network proxy that monkey-patches urllib to enforce filtering.

    This can be used to automatically intercept all urllib requests
    in sandboxed code without requiring code changes.

    WARNING: This is a more invasive approach. Use with caution.

    Example:
        with MonkeyPatchedNetworkProxy() as proxy:
            # All urllib requests inside this block are filtered
            import urllib.request
            urllib.request.urlopen("https://api.anthropic.com")  # Allowed
            urllib.request.urlopen("https://evil.com")  # Blocked
    """

    def __enter__(self):
        """Enable monkey patching."""
        self._original_urlopen = urllib.request.urlopen
        urllib.request.urlopen = self._patched_urlopen
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original urlopen."""
        urllib.request.urlopen = self._original_urlopen

    def _patched_urlopen(self, url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *args, **kwargs):
        """Patched urlopen that checks domain filtering."""
        # Get URL string
        if isinstance(url, str):
            url_str = url
        elif hasattr(url, 'full_url'):
            url_str = url.full_url
        else:
            url_str = str(url)

        # Check domain
        is_allowed, reason = self.is_domain_allowed(url_str)

        # Log
        if self.log_requests:
            self.request_log.append(NetworkLog(
                timestamp=datetime.now(),
                url=url_str,
                allowed=is_allowed,
                reason=reason
            ))

        if not is_allowed:
            raise PermissionError(
                f"Network request blocked: {reason}\n"
                f"URL: {url_str}\n"
                f"Allowed domains: {', '.join(self.allowed_domains)}"
            )

        # Call original
        return self._original_urlopen(url, data, timeout, *args, **kwargs)


def create_default_proxy() -> NetworkProxy:
    """
    Create network proxy with default secure settings.

    Returns:
        NetworkProxy with Anthropic, PyPI, and GitHub allowed
    """
    return NetworkProxy()
