#!/bin/bash
#
# Build script for Claude Code Skills Desktop Extension
#
# Creates a distributable .mcpb (MCP Bundle) file containing:
# - MCP server code
# - Skill adapters
# - Installation scripts
# - Documentation

set -e

echo "========================================="
echo "Building Claude Code Skills Desktop Extension"
echo "========================================="
echo

# Get directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_ROOT="$( cd "${SCRIPT_DIR}/.." && pwd )"
PROJECT_ROOT="$( cd "${MCP_ROOT}/.." && pwd )"
BUILD_DIR="${MCP_ROOT}/build"
DIST_DIR="${MCP_ROOT}/dist"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf "${BUILD_DIR}" "${DIST_DIR}"
mkdir -p "${BUILD_DIR}" "${DIST_DIR}"

# Create package directory structure
PACKAGE_DIR="${BUILD_DIR}/claude-code-skills"
mkdir -p "${PACKAGE_DIR}"

echo "✓ Build directories created"
echo

# Copy MCP server
echo "Copying MCP server..."
cp -r "${MCP_ROOT}/servers/skills-mcp" "${PACKAGE_DIR}/"
echo "✓ MCP server copied"

# Copy installation scripts
echo "Copying installation scripts..."
cp "${SCRIPT_DIR}/manifest.json" "${PACKAGE_DIR}/"
cp "${SCRIPT_DIR}/install.sh" "${PACKAGE_DIR}/"
chmod +x "${PACKAGE_DIR}/install.sh"
echo "✓ Installation scripts copied"

# Copy README
echo "Copying documentation..."
cp "${MCP_ROOT}/README.md" "${PACKAGE_DIR}/"
echo "✓ Documentation copied"

# Create symlink or reference to skills
echo "Creating skills reference..."
cat > "${PACKAGE_DIR}/SKILLS_PATH.txt" << EOF
This MCP server requires the full Claude Code project to run.

Skills are located at:
  ${PROJECT_ROOT}/skills/

When installing, ensure the project root is accessible.
EOF
echo "✓ Skills reference created"

# Create version info
echo "Creating version info..."
VERSION=$(cat "${PACKAGE_DIR}/manifest.json" | grep '"version"' | head -1 | sed 's/.*: "\(.*\)".*/\1/')
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
GIT_COMMIT=$(cd "${PROJECT_ROOT}" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")

cat > "${PACKAGE_DIR}/VERSION" << EOF
Version: ${VERSION}
Build Date: ${BUILD_DATE}
Git Commit: ${GIT_COMMIT}
Platform: Multi-platform (Linux, macOS, Windows)
EOF
echo "✓ Version info created"

# Package as .mcpb (tar.gz)
echo
echo "Creating distribution package..."
cd "${BUILD_DIR}"
tar -czf "claude-code-skills-${VERSION}.mcpb" claude-code-skills/
mv "claude-code-skills-${VERSION}.mcpb" "${DIST_DIR}/"

# Create checksum
cd "${DIST_DIR}"
sha256sum "claude-code-skills-${VERSION}.mcpb" > "claude-code-skills-${VERSION}.mcpb.sha256"

echo "✓ Package created"
echo

# Show summary
PACKAGE_SIZE=$(du -h "${DIST_DIR}/claude-code-skills-${VERSION}.mcpb" | cut -f1)
CHECKSUM=$(cat "${DIST_DIR}/claude-code-skills-${VERSION}.mcpb.sha256" | cut -d' ' -f1)

echo "========================================="
echo "Build complete!"
echo "========================================="
echo
echo "Package: claude-code-skills-${VERSION}.mcpb"
echo "Size: ${PACKAGE_SIZE}"
echo "SHA256: ${CHECKSUM}"
echo
echo "Location: ${DIST_DIR}/"
echo
echo "To install:"
echo "  1. Run: cd ${DIST_DIR}"
echo "  2. Extract: tar -xzf claude-code-skills-${VERSION}.mcpb"
echo "  3. Install: cd claude-code-skills && ./install.sh"
echo
echo "Or install directly in Claude Desktop by importing the .mcpb file"
echo "========================================="
