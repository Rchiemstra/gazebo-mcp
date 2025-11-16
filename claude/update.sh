#!/bin/bash

# Claude Code Update Script
# Updates global installation after changes to repository

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/claude-code"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude/claude-code"
else
    echo -e "${RED}Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${BLUE}=== Claude Code Update ===${NC}"
echo -e "Repository: ${YELLOW}$SCRIPT_DIR${NC}"
echo ""

# Check if installed
if [ ! -L "$CONFIG_DIR/agents" ] && [ ! -L "$CONFIG_DIR/commands" ]; then
    echo -e "${RED}Error: Global installation not found.${NC}"
    echo "Run ./install.sh first"
    exit 1
fi

# Update type
UPDATE_TYPE="${1:-full}"

case "$UPDATE_TYPE" in
    agents)
        echo -e "${GREEN}Updating agents only...${NC}"
        # Agents are symlinked, no action needed
        echo "  ✓ Agents update automatically (symlinked)"
        ;;

    commands)
        echo -e "${GREEN}Updating commands only...${NC}"
        # Commands are symlinked, no action needed
        echo "  ✓ Commands update automatically (symlinked)"
        ;;

    skills)
        echo -e "${GREEN}Updating skills (Python package)...${NC}"
        if command -v pip &> /dev/null; then
            pip install -e "$SCRIPT_DIR" --upgrade --quiet
            echo "  ✓ Skills package updated"
        else
            echo -e "${RED}  ✗ pip not found${NC}"
            exit 1
        fi
        ;;

    settings)
        echo -e "${GREEN}Updating settings...${NC}"
        if [ -f "$CONFIG_DIR/settings.json" ]; then
            echo -e "${YELLOW}Warning: This will overwrite your global settings!${NC}"
            read -p "Continue? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp "$SCRIPT_DIR/.claude/settings.local.json" "$CONFIG_DIR/settings.json"
                echo "  ✓ Settings updated"
            else
                echo "  - Cancelled"
            fi
        else
            cp "$SCRIPT_DIR/.claude/settings.local.json" "$CONFIG_DIR/settings.json"
            echo "  ✓ Settings created"
        fi
        ;;

    full|*)
        echo -e "${GREEN}Full update...${NC}"
        echo ""

        # Agents (symlinked, auto-update)
        echo -e "${GREEN}[1/4]${NC} Agents..."
        if [ -L "$CONFIG_DIR/agents" ]; then
            TARGET=$(readlink "$CONFIG_DIR/agents")
            if [ "$TARGET" = "$SCRIPT_DIR/.claude/agents" ]; then
                echo "  ✓ Already linked (auto-updates)"
            else
                echo -e "${YELLOW}  Warning: Linked to different location: $TARGET${NC}"
                read -p "  Relink to current repository? (y/N) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$CONFIG_DIR/agents"
                    ln -sf "$SCRIPT_DIR/.claude/agents" "$CONFIG_DIR/agents"
                    echo "  ✓ Relinked"
                fi
            fi
        else
            echo -e "${YELLOW}  Warning: Not symlinked. Run ./install.sh${NC}"
        fi

        # Commands (symlinked, auto-update)
        echo -e "${GREEN}[2/4]${NC} Commands..."
        if [ -L "$CONFIG_DIR/commands" ]; then
            TARGET=$(readlink "$CONFIG_DIR/commands")
            if [ "$TARGET" = "$SCRIPT_DIR/.claude/commands" ]; then
                echo "  ✓ Already linked (auto-updates)"
            else
                echo -e "${YELLOW}  Warning: Linked to different location: $TARGET${NC}"
                read -p "  Relink to current repository? (y/N) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$CONFIG_DIR/commands"
                    ln -sf "$SCRIPT_DIR/.claude/commands" "$CONFIG_DIR/commands"
                    echo "  ✓ Relinked"
                fi
            fi
        else
            echo -e "${YELLOW}  Warning: Not symlinked. Run ./install.sh${NC}"
        fi

        # Agent Registry (symlinked, auto-update)
        echo -e "${GREEN}[3/4]${NC} Agent Registry..."
        if [ -L "$CONFIG_DIR/agent-registry.json" ]; then
            echo "  ✓ Already linked (auto-updates)"
        elif [ -f "$CONFIG_DIR/agent-registry.json" ]; then
            echo -e "${YELLOW}  Warning: File exists but not symlinked${NC}"
            read -p "  Replace with symlink? (y/N) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                mv "$CONFIG_DIR/agent-registry.json" "$CONFIG_DIR/agent-registry.json.backup"
                ln -sf "$SCRIPT_DIR/.claude/agent-registry.json" "$CONFIG_DIR/agent-registry.json"
                echo "  ✓ Linked (backup created)"
            fi
        fi

        # Skills (Python package, needs reinstall)
        echo -e "${GREEN}[4/4]${NC} Skills (Python package)..."
        if command -v pip &> /dev/null; then
            # Check if package is installed
            PACKAGE_NAME="claude-learning"
            if pip show "$PACKAGE_NAME" &> /dev/null; then
                pip install -e "$SCRIPT_DIR" --upgrade --quiet --no-deps
                echo "  ✓ Package updated"
            else
                echo -e "${YELLOW}  Package not installed. Installing...${NC}"
                pip install -e "$SCRIPT_DIR" --quiet
                echo "  ✓ Package installed"
            fi
        else
            echo -e "${YELLOW}  Warning: pip not found. Skipping.${NC}"
        fi
        ;;
esac

echo ""
echo -e "${GREEN}=== Update Summary ===${NC}"
echo ""
echo "Updated components:"
echo "  • Agents: ${GREEN}auto-update${NC} (symlinked)"
echo "  • Commands: ${GREEN}auto-update${NC} (symlinked)"
echo "  • Agent Registry: ${GREEN}auto-update${NC} (symlinked)"
echo "  • Skills: ${GREEN}updated${NC} (Python package)"
echo ""
echo -e "${BLUE}New features available:${NC}"
echo "  • Dynamic Model Selection (30-85% cost savings)"
echo "  • Parallel Execution (40-70% faster workflows)"
echo "  • Token Efficiency (95-99% token reduction)"
echo ""
echo -e "${BLUE}How updates work:${NC}"
echo "  • Agents/Commands: Edit files in this repo, changes reflect immediately"
echo "  • Skills: Run ${YELLOW}./update.sh skills${NC} after code changes"
echo "  • Settings: Run ${YELLOW}./update.sh settings${NC} to sync global settings"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  • Copy .env.example to .env to configure dynamic model selection"
echo "  • See docs/DYNAMIC_MODEL_SELECTION.md for details"
echo ""
echo -e "${GREEN}✓ Update complete!${NC}"
echo ""
echo "Restart Claude Code to ensure all changes are loaded."
