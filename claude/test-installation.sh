#!/bin/bash

# Test script to verify Claude Code installation

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/claude-code"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude/claude-code"
else
    echo -e "${RED}Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${GREEN}=== Claude Code Installation Test ===${NC}"
echo ""

# Test 1: Config directory exists
echo -n "Config directory exists... "
if [ -d "$CONFIG_DIR" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "Expected: $CONFIG_DIR"
fi

# Test 2: Agents symlink
echo -n "Agents linked... "
if [ -L "$CONFIG_DIR/agents" ]; then
    TARGET=$(readlink "$CONFIG_DIR/agents")
    echo -e "${GREEN}✓${NC}"
    echo "  → $TARGET"
else
    echo -e "${RED}✗${NC}"
fi

# Test 3: Commands symlink
echo -n "Commands linked... "
if [ -L "$CONFIG_DIR/commands" ]; then
    TARGET=$(readlink "$CONFIG_DIR/commands")
    echo -e "${GREEN}✓${NC}"
    echo "  → $TARGET"
else
    echo -e "${RED}✗${NC}"
fi

# Test 4: Agent registry
echo -n "Agent registry... "
if [ -e "$CONFIG_DIR/agent-registry.json" ]; then
    if python -m json.tool "$CONFIG_DIR/agent-registry.json" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} (valid JSON)"
    else
        echo -e "${YELLOW}!${NC} (invalid JSON)"
    fi
else
    echo -e "${RED}✗${NC}"
fi

# Test 5: Count agents
echo -n "Available agents... "
if [ -d "$CONFIG_DIR/agents" ]; then
    AGENT_COUNT=$(find "$CONFIG_DIR/agents" -name "*.md" | wc -l)
    echo -e "${GREEN}$AGENT_COUNT${NC} found"
else
    echo -e "${RED}0${NC}"
fi

# Test 6: Count commands
echo -n "Available commands... "
if [ -d "$CONFIG_DIR/commands" ]; then
    CMD_COUNT=$(find "$CONFIG_DIR/commands" -name "*.md" | wc -l)
    echo -e "${GREEN}$CMD_COUNT${NC} found"
else
    echo -e "${RED}0${NC}"
fi

# Test 7: Python skills import
echo -n "Python skills package... "
if python -c "from skills.code_analysis import CodeAnalysisSkill" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}!${NC} (import failed)"
    echo "  Try: pip install -e ."
fi

# Test 8: Dynamic model selection
echo -n "Dynamic model selection... "
if python -c "from skills.common import ModelSelector, ClaudeModel" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}!${NC} (import failed)"
fi

# Test 9: Parallel execution
echo -n "Parallel execution... "
if python -c "from skills.common import ParallelExecutor, ResultAggregator" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}!${NC} (import failed)"
fi

# Test 10: List some available commands
echo ""
echo -e "${GREEN}Sample commands available:${NC}"
if [ -d "$CONFIG_DIR/commands" ]; then
    find "$CONFIG_DIR/commands" -name "*.md" -type f,l | head -5 | while read cmd; do
        CMD_NAME=$(basename "$cmd" .md)
        echo "  /$CMD_NAME"
    done
else
    echo "  (none)"
fi

# Test 11: List some available agents
echo ""
echo -e "${GREEN}Sample agents available:${NC}"
if [ -d "$CONFIG_DIR/agents" ]; then
    find "$CONFIG_DIR/agents" -name "*.md" -type f,l | head -5 | while read agent; do
        AGENT_NAME=$(basename "$agent" .md)
        echo "  $AGENT_NAME"
    done
else
    echo "  (none)"
fi

echo ""
echo -e "${GREEN}=== Test Complete ===${NC}"
echo ""
echo -e "${YELLOW}Try these commands:${NC}"
echo "  ${YELLOW}/start-learning${NC} - Start a learning journey"
echo "  ${YELLOW}/dev \"Create a ROS2 node\"${NC} - Complete workflow"
echo "  ${YELLOW}/verify-all${NC} - Parallel verification"
echo ""
echo -e "${YELLOW}Or test skills from Python:${NC}"
echo "  ${YELLOW}from skills.common import ModelSelector${NC}"
echo "  ${YELLOW}from skills.code_analysis import analyze_codebase_parallel${NC}"
