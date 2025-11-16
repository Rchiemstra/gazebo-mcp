#!/bin/bash

# Claude Code Global Uninstallation Script
# Removes global symlinks and configuration

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    CONFIG_DIR="$HOME/.config/claude-code"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    CONFIG_DIR="$HOME/Library/Application Support/Claude/claude-code"
else
    echo -e "${RED}Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${YELLOW}=== Claude Code Global Uninstallation ===${NC}"
echo -e "Config directory: ${YELLOW}$CONFIG_DIR${NC}"
echo ""

# Confirm
read -p "Remove global Claude Code configuration? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled"
    exit 0
fi

# Remove symlinks
echo -e "${GREEN}[1/4]${NC} Removing symlinks..."

if [ -L "$CONFIG_DIR/agents" ]; then
    rm "$CONFIG_DIR/agents"
    echo "  ✓ Agents symlink removed"
elif [ -d "$CONFIG_DIR/agents" ]; then
    echo -e "${YELLOW}  Warning: agents is a directory, not a symlink. Not removing.${NC}"
fi

if [ -L "$CONFIG_DIR/commands" ]; then
    rm "$CONFIG_DIR/commands"
    echo "  ✓ Commands symlink removed"
elif [ -d "$CONFIG_DIR/commands" ]; then
    echo -e "${YELLOW}  Warning: commands is a directory, not a symlink. Not removing.${NC}"
fi

if [ -L "$CONFIG_DIR/agent-registry.json" ]; then
    rm "$CONFIG_DIR/agent-registry.json"
    echo "  ✓ Agent registry symlink removed"
fi

# Ask about settings.json
echo -e "${GREEN}[2/4]${NC} Configuration file..."
if [ -f "$CONFIG_DIR/settings.json" ]; then
    read -p "Remove settings.json? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$CONFIG_DIR/settings.json"
        echo "  ✓ Settings removed"
    else
        echo "  - Settings kept"
    fi
fi

# Restore backups if they exist
echo -e "${GREEN}[3/4]${NC} Checking for backups..."
if [ -d "$CONFIG_DIR/agents.backup" ]; then
    mv "$CONFIG_DIR/agents.backup" "$CONFIG_DIR/agents"
    echo "  ✓ Restored agents.backup"
fi

if [ -d "$CONFIG_DIR/commands.backup" ]; then
    mv "$CONFIG_DIR/commands.backup" "$CONFIG_DIR/commands"
    echo "  ✓ Restored commands.backup"
fi

if [ -f "$CONFIG_DIR/agent-registry.json.backup" ]; then
    mv "$CONFIG_DIR/agent-registry.json.backup" "$CONFIG_DIR/agent-registry.json"
    echo "  ✓ Restored agent-registry.json.backup"
fi

# Uninstall Python package
echo -e "${GREEN}[4/4]${NC} Uninstalling Python package..."
if command -v pip &> /dev/null; then
    # Get package name from setup
    PACKAGE_NAME=$(python -c "import tomli; print(tomli.load(open('$SCRIPT_DIR/pyproject.toml', 'rb'))['project']['name'])" 2>/dev/null || echo "claude-learning")

    if pip show "$PACKAGE_NAME" &> /dev/null; then
        pip uninstall -y "$PACKAGE_NAME" --quiet
        echo "  ✓ Python package uninstalled"
    else
        echo "  - Package not installed"
    fi
else
    echo -e "${YELLOW}  Warning: pip not found. Skipping package uninstallation.${NC}"
fi

echo ""
echo -e "${GREEN}=== Uninstallation Complete! ===${NC}"
echo ""
echo "Your repository at $SCRIPT_DIR is unchanged."
echo "Run ./install.sh to reinstall."
echo ""
