#!/usr/bin/env bash

#
# Claude Agents & Skills Installation Script
# Installs ROS2 development skills and agents globally
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_SRC="${SCRIPT_DIR}/.claude/commands"
REFERENCE_DOCS_SRC="${SCRIPT_DIR}/.claude"

# Determine installation directory
# Priority: ~/.claude/commands or $XDG_CONFIG_HOME/claude/commands
if [ -d "$HOME/.claude" ]; then
    INSTALL_DIR="$HOME/.claude/commands"
    DOCS_DIR="$HOME/.claude"
else
    XDG_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
    INSTALL_DIR="${XDG_CONFIG}/claude/commands"
    DOCS_DIR="${XDG_CONFIG}/claude"
fi

BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"

# Helper functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}$1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check if source directory exists
check_source() {
    if [ ! -d "$COMMANDS_SRC" ]; then
        print_error "Commands source directory not found: $COMMANDS_SRC"
        print_error "Please run this script from the claude_agents repository root."
        exit 1
    fi

    if [ ! -d "$REFERENCE_DOCS_SRC" ]; then
        print_error "Reference docs directory not found: $REFERENCE_DOCS_SRC"
        exit 1
    fi

    print_success "Source directory found: $COMMANDS_SRC"
}

# Backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR" ] || [ -L "$INSTALL_DIR" ]; then
        print_info "Backing up existing installation..."

        # If it's a symlink, just remove it
        if [ -L "$INSTALL_DIR" ]; then
            print_info "Removing existing symlink: $INSTALL_DIR"
            rm "$INSTALL_DIR"
        else
            # If it's a real directory, back it up
            print_info "Creating backup: $BACKUP_DIR"
            mv "$INSTALL_DIR" "$BACKUP_DIR"
            print_success "Backup created"
        fi
    fi
}

# Install via symlink (recommended)
install_symlink() {
    print_info "Installing via symlink (updates automatically)..."

    # Create parent directory if needed
    mkdir -p "$(dirname "$INSTALL_DIR")"

    # Create symlink
    ln -s "$COMMANDS_SRC" "$INSTALL_DIR"

    print_success "Commands symlinked: $INSTALL_DIR → $COMMANDS_SRC"
}

# Install via copy (static)
install_copy() {
    print_info "Installing via copy (static installation)..."

    # Create installation directory
    mkdir -p "$INSTALL_DIR"

    # Copy commands
    cp -r "$COMMANDS_SRC"/* "$INSTALL_DIR/"

    print_success "Commands copied to: $INSTALL_DIR"
}

# Install reference documentation
install_docs() {
    print_info "Installing reference documentation..."

    # Copy reference docs
    for doc in CLAUDE.md ros-patterns.md modbus-patterns.md cpp-best-practices.md python-best-practices.md verification-checklist.md test-strategies.md; do
        if [ -f "${REFERENCE_DOCS_SRC}/${doc}" ]; then
            cp "${REFERENCE_DOCS_SRC}/${doc}" "${DOCS_DIR}/"
            print_info "Installed: ${doc}"
        fi
    done

    print_success "Reference documentation installed to: $DOCS_DIR"
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."

    local skills_count=$(find "$INSTALL_DIR/skills" -name "*.md" 2>/dev/null | wc -l)
    local agents_count=$(find "$INSTALL_DIR/agents" -name "*.md" 2>/dev/null | wc -l)

    if [ "$skills_count" -gt 0 ] && [ "$agents_count" -gt 0 ]; then
        print_success "Installation verified:"
        print_info "  - Skills: $skills_count"
        print_info "  - Agents: $agents_count"
        return 0
    else
        print_error "Installation verification failed"
        return 1
    fi
}

# Show usage information
show_usage() {
    print_header "Installation Complete!"

    echo "Claude Agents & Skills have been installed globally."
    echo ""
    echo "Installation Directory: $INSTALL_DIR"
    echo "Documentation: $DOCS_DIR"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "AVAILABLE COMMANDS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Skills (Foundation Tools):"
    echo "  /gather-context    - Analyze codebase"
    echo "  /plan              - Create implementation plan"
    echo "  /verify-ros-node   - Validate ROS2 nodes"
    echo "  /verify-build      - Check compilation"
    echo "  /verify-tests      - Run test suites"
    echo "  /verify-lint       - Code quality checks"
    echo "  /git-commit        - Create commits"
    echo "  ... and 11 more skills"
    echo ""
    echo "Agents (High-Level Orchestrators):"
    echo "  /dev               - Complete development workflow"
    echo "  /execute           - Execute implementation plan"
    echo "  /create-ros-node   - Create ROS2 node"
    echo "  /modbus-bridge     - Modbus-ROS bridge"
    echo "  /ros-debug         - Debug ROS system"
    echo "  ... and 28 more agents"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "QUICK START"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. View main documentation:"
    echo "   cat $DOCS_DIR/CLAUDE.md"
    echo ""
    echo "2. Try the complete workflow:"
    echo "   /dev Create a ROS2 sensor node"
    echo ""
    echo "3. See all available commands:"
    echo "   ls $INSTALL_DIR/skills/"
    echo "   ls $INSTALL_DIR/agents/"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    print_success "Installation successful!"
    echo ""
}

# Main installation flow
main() {
    print_header "Claude Agents & Skills Installer"

    print_info "This will install 51 ROS2 development skills and agents"
    print_info "Source: $COMMANDS_SRC"
    print_info "Target: $INSTALL_DIR"
    echo ""

    # Ask for installation method
    echo "Installation method:"
    echo "  1) Symlink (recommended - updates automatically)"
    echo "  2) Copy (static - won't auto-update)"
    echo ""
    read -p "Choose method [1]: " method
    method=${method:-1}

    echo ""

    # Perform checks
    check_source

    # Backup existing installation
    backup_existing

    # Install based on method
    case "$method" in
        1)
            install_symlink
            ;;
        2)
            install_copy
            ;;
        *)
            print_error "Invalid choice: $method"
            exit 1
            ;;
    esac

    # Install reference docs
    install_docs

    # Verify installation
    if verify_installation; then
        show_usage
    else
        print_error "Installation completed but verification failed"
        print_info "Please check $INSTALL_DIR manually"
        exit 1
    fi

    # Show backup info if created
    if [ -d "$BACKUP_DIR" ]; then
        echo ""
        print_info "Previous installation backed up to:"
        print_info "  $BACKUP_DIR"
        print_info "You can safely delete this if everything works."
    fi
}

# Run main
main "$@"
