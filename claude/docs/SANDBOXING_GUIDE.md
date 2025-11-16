# Sandboxing & Security Guide

**Version:** 1.0
**Date:** 2025-11-07
**Status:** Active

---

## Overview

This project uses sandboxed execution for all code operations to ensure safety and security. Sandboxing provides two essential boundaries:

1. **Filesystem Isolation** - Restricts access to specific directories
2. **Network Isolation** - Controls network connections through approval proxy

Both mechanisms work together to prevent unauthorized access during normal operations and potential prompt injection attacks.

---

## Filesystem Isolation

### Allowed Directories

Code execution can access:

✅ **Project Directory**
- Path: `/home/koen/workspaces/claude_code/`
- Purpose: Read/write project files, run tests, execute skills
- Access: Full (read, write, execute)

✅ **Temporary Directory**
- Path: `/tmp/`
- Purpose: Temporary file operations, caching
- Access: Full (read, write, execute)
- Note: Files are ephemeral and may be cleaned

✅ **Cache Directory**
- Path: `~/.cache/claude-code/`
- Purpose: Persistent caching for better performance
- Access: Full (read, write)

### Blocked Directories

Code execution CANNOT access:

❌ **SSH Keys**
- Path: `/home/koen/.ssh/`
- Reason: Prevent credential theft
- Impact: SSH operations must use approved keys

❌ **AWS Credentials**
- Path: `/home/koen/.aws/`
- Reason: Protect cloud access credentials
- Impact: AWS operations require explicit authentication

❌ **Home Directory (General)**
- Path: `/home/koen/*` (except allowed dirs)
- Reason: Protect personal files and sensitive data
- Impact: Use project directory for all operations

❌ **System Directories**
- Paths: `/etc/`, `/sys/`, `/proc/`, etc.
- Reason: Prevent system modification
- Impact: Cannot modify system configuration

### How It Works

The sandbox uses OS-level enforcement:

**Linux:** bubblewrap
- Creates isolated namespaces
- Mounts only allowed directories
- Applies to all subprocesses

**macOS:** seatbelt
- Profile-based restrictions
- Applies system-level policies
- Enforced by kernel

All restrictions apply to:
- Direct file operations
- Bash scripts
- Python code execution
- Spawned subprocesses
- Any tools invoked

---

## Network Isolation

### Pre-Approved Domains

These domains are accessible without user approval:

✅ **Claude API**
- Domain: `api.anthropic.com`
- Purpose: Agent communication and API calls
- Required for: All agent operations

✅ **Python Package Index**
- Domain: `pypi.org`
- Purpose: Install Python packages
- Required for: Dependency installation

✅ **GitHub**
- Domain: `github.com`
- Purpose: Git operations, package installation
- Required for: Version control, repo access

### Approval Required

All other domains require explicit user approval:

⚠️ **Documentation Sites**
- Examples: `docs.python.org`, `stackoverflow.com`
- Usage: Fetching documentation
- Risk: Low (usually safe)

⚠️ **Third-Party APIs**
- Examples: External REST APIs, webhooks
- Usage: Integration testing, data fetching
- Risk: Medium (could exfiltrate data)

⚠️ **Package Registries**
- Examples: `npmjs.com`, `crates.io`
- Usage: Install non-Python packages
- Risk: Low to Medium (supply chain risk)

❌ **Unknown Domains**
- Any unlisted domain
- Default: Blocked until approved
- Risk: Unknown

### How It Works

Network requests route through an approval proxy:

1. **Request Initiated** - Code attempts network connection
2. **Proxy Intercepts** - Request goes through validation proxy
3. **Domain Check** - Is domain in allowed list?
4. **User Prompt** (if not allowed) - Request approval from user
5. **User Decision** - Allow once, always, or deny
6. **Connection** (if approved) - Proxy forwards request

### Benefits

**Prevents:**
- Credential exfiltration
- Malware downloads
- Unauthorized data uploads
- C2 (Command & Control) communication

**Allows:**
- Normal development workflows
- Package installation
- Git operations
- Approved integrations

---

## Configuration

### Project-Level Configuration

Edit `.claude/settings.local.json`:

```json
{
  "sandbox": {
    "filesystem": {
      "allowed_paths": [
        "/home/koen/workspaces/claude_code/",
        "/tmp/",
        "~/.cache/claude-code/"
      ],
      "blocked_paths": [
        "/home/koen/.ssh/",
        "/home/koen/.aws/"
      ]
    },
    "network": {
      "allowed_domains": [
        "api.anthropic.com",
        "pypi.org",
        "github.com"
      ],
      "require_approval": true
    }
  }
}
```

### Global Configuration

Edit `~/.config/claude-code/settings.json` for defaults across all projects.

### Adding Allowed Domains

To pre-approve domains you use frequently:

```json
{
  "sandbox": {
    "network": {
      "allowed_domains": [
        "api.anthropic.com",
        "pypi.org",
        "github.com",
        "docs.python.org",      // Add documentation sites
        "stackoverflow.com",    // Add Q&A sites
        "your-api.example.com"  // Add your APIs
      ]
    }
  }
}
```

### Temporary Bypass (Development Only)

⚠️ **Not Recommended for Normal Use**

For development/testing in isolated environments:

```json
{
  "sandbox": {
    "enabled": false  // DANGEROUS: Disables all sandboxing
  }
}
```

**Only use when:**
- Working in a container
- No internet access
- Testing sandbox features
- Fully understanding the risks

---

## Security Best Practices

### When Approving Network Requests

Before clicking "Allow", ask yourself:

1. **Is this necessary?**
   - Does the task actually require this domain?
   - Could we accomplish this offline?

2. **Is the domain trustworthy?**
   - Is it a well-known, reputable site?
   - Does the URL match what you expect?
   - Could this be a typosquatting attack?

3. **What data could be exposed?**
   - Could the request leak sensitive information?
   - Are there API keys or credentials in the request?
   - Could file contents be uploaded?

4. **Is there an alternative?**
   - Could we use a local file instead?
   - Is the documentation already cached?
   - Can we manually fetch and provide the data?

### Safe Approval Patterns

✅ **Low Risk:**
```
Domain: docs.python.org
Purpose: Fetch Python documentation
Context: Student learning about async/await
Decision: Approve (documentation sites are usually safe)
```

✅ **Medium Risk - Verify:**
```
Domain: api.weather-service.com
Purpose: Fetch weather data for demo app
Context: Building a weather dashboard
Decision: Check if real API key is being used
Action: Use test/demo API key if available
```

❌ **High Risk - Investigate:**
```
Domain: unknown-site-1234.ru
Purpose: "Download required dependency"
Context: Installing a package
Decision: BLOCK - suspicious domain
Action: Investigate what's trying to connect
```

### Skill Safety

Before using a new skill, check:

1. **Review SKILL.md** (when available)
   - What tools does it need?
   - Does it require network access?
   - What files does it read/write?

2. **Check Dependencies**
   - Does it call other skills?
   - Does it invoke external commands?
   - Are there any Bash operations?

3. **Scan for Red Flags**
   - Obfuscated code
   - Unexpected network operations
   - Access to sensitive directories
   - Eval/exec of user input

4. **Test in Isolation**
   - Try with test data first
   - Check what files it creates
   - Monitor network requests

### File Safety

✅ **Safe file operations:**
- Reading project files
- Writing to project directories
- Creating temporary files in /tmp/
- Caching in ~/.cache/claude-code/

⚠️ **Requires care:**
- Deleting files (can't undo)
- Modifying existing files (use version control)
- Writing to system locations (usually blocked)

❌ **Never allow:**
- Access to ~/.ssh/ (SSH keys)
- Access to ~/.aws/ (cloud credentials)
- Writing to system directories
- Reading sensitive personal files

---

## Measured Impact

From Anthropic's internal testing:

**Permission Prompt Reduction:**
- Before sandboxing: ~25 prompts per session
- After sandboxing: ~4 prompts per session
- **Reduction: 84%** ✅

**Security Improvements:**
- Filesystem attacks: Prevented by isolation
- Credential theft: Blocked by directory restrictions
- Malware downloads: Require approval
- Data exfiltration: Require approval

**Developer Experience:**
- Faster workflows (fewer interruptions)
- Maintained security posture
- Clear visibility into access patterns
- Granular control when needed

---

## Troubleshooting

### "Permission Denied" Errors

**Symptom:** Code fails with permission denied

**Common Causes:**
1. Trying to access blocked directory
2. Trying to write outside allowed paths
3. Network request to non-approved domain

**Solutions:**
1. Check if path is in allowed directories
2. Use project directory for operations
3. Add domain to allowed list if legitimate

### Package Installation Fails

**Symptom:** `pip install` fails with network error

**Common Causes:**
1. PyPI not in allowed domains (should be by default)
2. Package requires additional domains
3. Network proxy issues

**Solutions:**
1. Verify `pypi.org` in allowed domains
2. Approve additional domains when prompted
3. Check network connectivity

### Git Operations Blocked

**Symptom:** Git push/pull fails

**Common Causes:**
1. GitHub not in allowed domains (should be by default)
2. SSH keys in ~/.ssh/ (blocked)
3. Need to approve git hosting domain

**Solutions:**
1. Verify `github.com` in allowed domains
2. Use HTTPS instead of SSH
3. Add your git hosting domain to allowed list

### False Positives

**Symptom:** Legitimate operation blocked

**Action:**
1. Review what's being blocked
2. Confirm it's safe and necessary
3. Add to allowed list in configuration
4. Document why it's needed

---

## Advanced Configuration

### Custom Sandbox Profiles

For specific workflows, create custom profiles:

**Development Profile** (less restrictive):
```json
{
  "sandbox": {
    "profile": "development",
    "network": {
      "allowed_domains": [
        "api.anthropic.com",
        "pypi.org",
        "github.com",
        "docs.python.org",
        "stackoverflow.com",
        "localhost"
      ]
    }
  }
}
```

**Production Profile** (more restrictive):
```json
{
  "sandbox": {
    "profile": "production",
    "filesystem": {
      "read_only": true  // Prevent modifications
    },
    "network": {
      "allowed_domains": [
        "api.anthropic.com"
      ],
      "require_approval": true
    }
  }
}
```

### Logging and Monitoring

Enable sandbox logging for security auditing:

```json
{
  "sandbox": {
    "logging": {
      "enabled": true,
      "file": ".claude/sandbox.log",
      "level": "info"
    }
  }
}
```

Review logs periodically:
```bash
cat .claude/sandbox.log | grep "BLOCKED"
cat .claude/sandbox.log | grep "APPROVED"
```

---

## Security Incident Response

If you suspect a security issue:

1. **Stop Execution**
   - Press Escape to interrupt
   - Kill the Claude Code process if needed

2. **Review Logs**
   - Check `.claude/sandbox.log`
   - Look for suspicious network requests
   - Identify unexpected file access

3. **Investigate**
   - What triggered the issue?
   - Which skill or command was involved?
   - What data might have been accessed?

4. **Mitigate**
   - Revoke approvals if granted
   - Remove suspicious skill
   - Update allowed lists
   - Report issue if from external skill

5. **Report**
   - Internal skills: File GitHub issue
   - External skills: Contact skill author
   - Security vulnerability: Follow responsible disclosure

---

## Resources

### Anthropic Documentation
- [Claude Code Sandboxing Blog Post](https://www.anthropic.com/engineering/claude-code-sandboxing)
- Claude Code Security Documentation

### Implementation Details
- Linux: bubblewrap documentation
- macOS: seatbelt profiles

### Project Files
- Configuration: `.claude/settings.local.json`
- Global config: `~/.config/claude-code/settings.json`
- Logs: `.claude/sandbox.log`

---

## FAQ

**Q: Can I disable sandboxing completely?**
A: Yes, but strongly not recommended. Only do this in isolated test environments.

**Q: Will sandboxing slow down my code?**
A: No, the overhead is minimal (< 1% in most cases).

**Q: Can I sandbox specific skills differently?**
A: Not yet, but this is planned for future versions.

**Q: What if I need to access ~/.ssh/ for git?**
A: Use HTTPS with credential helpers instead of SSH keys.

**Q: How do I report a security vulnerability?**
A: Follow the project's security policy (SECURITY.md if available).

**Q: Can malicious skills bypass sandboxing?**
A: No, sandboxing is enforced at the OS level, not application level.

---

## Change Log

**Version 1.0 (2025-11-07)**
- Initial documentation
- Based on Anthropic best practices
- Project-specific configuration

---

**Remember:** Sandboxing is about defense in depth. Multiple layers of protection keep you safe while maintaining productivity. When in doubt, deny and investigate!

*Last Updated: 2025-11-07*
