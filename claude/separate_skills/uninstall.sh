#!/usr/bin/env bash

#
# Claude Agents & Skills Uninstallation Script
# Removes globally installed skills and agents
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect installation directory
if [ -d "$HOME/.claude" ]; then
    INSTALL_DIR="$HOME/.claude/commands"
    DOCS_DIR="$HOME/.claude"
else
    XDG_CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
    INSTALL_DIR="${XDG_CONFIG}/claude/commands"
    DOCS_DIR="${XDG_CONFIG}/claude"
fi

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

# Check if installation exists
check_installation() {
    if [ ! -d "$INSTALL_DIR" ] && [ ! -L "$INSTALL_DIR" ]; then
        print_warning "No installation found at: $INSTALL_DIR"
        print_info "Nothing to uninstall."
        exit 0
    fi

    print_info "Found installation at: $INSTALL_DIR"

    if [ -L "$INSTALL_DIR" ]; then
        print_info "Installation type: Symlink"
    else
        print_info "Installation type: Copy"
    fi
}

# Find and remove documentation
remove_docs() {
    print_info "Removing reference documentation..."

    local docs_removed=0

    for doc in CLAUDE.md ros-patterns.md modbus-patterns.md cpp-best-practices.md python-best-practices.md verification-checklist.md test-strategies.md; do
        if [ -f "${DOCS_DIR}/${doc}" ]; then
            rm "${DOCS_DIR}/${doc}"
            print_info "Removed: ${doc}"
            docs_removed=$((docs_removed + 1))
        fi
    done

    if [ $docs_removed -gt 0 ]; then
        print_success "Removed $docs_removed reference documents"
    else
        print_info "No reference documents found to remove"
    fi
}

# Remove installation
remove_installation() {
    print_info "Removing commands installation..."

    if [ -L "$INSTALL_DIR" ]; then
        # It's a symlink, just remove it
        rm "$INSTALL_DIR"
        print_success "Symlink removed: $INSTALL_DIR"
    elif [ -d "$INSTALL_DIR" ]; then
        # It's a directory, remove it
        rm -rf "$INSTALL_DIR"
        print_success "Directory removed: $INSTALL_DIR"
    fi
}

# Restore backup if available
restore_backup() {
    print_info "Checking for backups..."

    # Find most recent backup
    local backup_dir=$(find "$(dirname "$INSTALL_DIR")" -maxdepth 1 -name "$(basename "$INSTALL_DIR").backup.*" -type d 2>/dev/null | sort -r | head -n 1)

    if [ -n "$backup_dir" ]; then
        print_info "Found backup: $backup_dir"
        read -p "Restore this backup? [y/N]: " restore
        restore=${restore:-N}

        if [[ "$restore" =~ ^[Yy]$ ]]; then
            mv "$backup_dir" "$INSTALL_DIR"
            print_success "Backup restored to: $INSTALL_DIR"
        else
            print_info "Backup not restored. You can manually restore it later:"
            print_info "  mv \"$backup_dir\" \"$INSTALL_DIR\""
        fi
    else
        print_info "No backups found"
    fi
}

# Clean up empty directories
cleanup_empty_dirs() {
    print_info "Cleaning up empty directories..."

    # Remove parent directory if empty
    if [ -d "$DOCS_DIR" ] && [ -z "$(ls -A "$DOCS_DIR")" ]; then
        rmdir "$DOCS_DIR"
        print_info "Removed empty directory: $DOCS_DIR"
    fi
}

# Verify removal
verify_removal() {
    if [ ! -d "$INSTALL_DIR" ] && [ ! -L "$INSTALL_DIR" ]; then
        print_success "Uninstallation verified - commands removed"
        return 0
    else
        print_error "Uninstallation verification failed"
        print_error "Installation still exists at: $INSTALL_DIR"
        return 1
    fi
}

# Show completion message
show_completion() {
    print_header "Uninstallation Complete"

    echo "Claude Agents & Skills have been uninstalled."
    echo ""
    echo "The following were removed:"
    echo "  - Commands: $INSTALL_DIR"
    echo "  - Documentation: $DOCS_DIR/*.md"
    echo ""

    # Check for backups
    local backup_count=$(find "$(dirname "$INSTALL_DIR")" -maxdepth 1 -name "$(basename "$INSTALL_DIR").backup.*" -type d 2>/dev/null | wc -l)

    if [ "$backup_count" -gt 0 ]; then
        print_info "Backup(s) still present: $backup_count"
        print_info "You can safely delete them if you don't need them:"
        print_info "  rm -rf $(dirname "$INSTALL_DIR")/$(basename "$INSTALL_DIR").backup.*"
        echo ""
    fi

    print_success "Uninstall successful!"
    echo ""
}

# Main uninstallation flow
main() {
    print_header "Claude Agents & Skills Uninstaller"

    # Check if installation exists
    check_installation

    # Confirm uninstallation
    echo "This will remove all installed skills and agents."
    echo "Installation: $INSTALL_DIR"
    echo ""
    read -p "Proceed with uninstallation? [y/N]: " confirm
    confirm=${confirm:-N}

    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled."
        exit 0
    fi

    echo ""

    # Perform uninstallation
    remove_docs
    remove_installation

    # Verify removal
    if verify_removal; then
        # Clean up empty directories
        cleanup_empty_dirs

        # Offer to restore backup
        restore_backup

        # Show completion message
        show_completion
    else
        print_error "Uninstallation completed but verification failed"
        print_info "Please check $INSTALL_DIR manually"
        exit 1
    fi
}

# Run main
main "$@"
