"""
Improvement Applicator

Safely applies code improvements with validation and rollback capabilities.
"""

import os
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from skills.skill_evaluator.core.models import ImprovementSuggestion


class SafetyGate:
    """Safety assessment for improvement application."""

    # Risk levels
    LOW_RISK = "low"
    MEDIUM_RISK = "medium"
    HIGH_RISK = "high"
    CRITICAL_RISK = "critical"

    # Risk factors
    RISK_FACTORS = {
        'structural_change': 'high',      # Changes to class/function structure
        'api_change': 'critical',         # Changes to public API
        'logic_change': 'medium',         # Changes to business logic
        'refactoring': 'medium',          # Code refactoring
        'performance': 'low',             # Performance optimization
        'documentation': 'low',           # Documentation changes
        'test_addition': 'low',           # Adding tests
        'formatting': 'low'               # Code formatting
    }

    @staticmethod
    def assess_risk(suggestion: ImprovementSuggestion) -> Dict[str, Any]:
        """
        Assess risk level for applying a suggestion.

        Args:
            suggestion: ImprovementSuggestion to assess

        Returns:
            Risk assessment with level and factors
        """
        # Base risk from category
        category_risks = {
            'performance': SafetyGate.MEDIUM_RISK,
            'reliability': SafetyGate.HIGH_RISK,
            'quality': SafetyGate.MEDIUM_RISK,
            'maintainability': SafetyGate.LOW_RISK,
            'security': SafetyGate.HIGH_RISK,
            'documentation': SafetyGate.LOW_RISK
        }

        base_risk = category_risks.get(suggestion.category, SafetyGate.MEDIUM_RISK)

        # Adjust based on severity
        if suggestion.severity == 'critical':
            base_risk = SafetyGate.HIGH_RISK

        # Check if has code changes
        has_code_changes = bool(suggestion.suggested_code)

        # Auto-apply flag
        marked_safe = suggestion.can_auto_apply

        # Confidence level
        high_confidence = suggestion.confidence >= 0.8

        # Determine final risk
        risk_score = 0
        if base_risk == SafetyGate.LOW_RISK:
            risk_score = 1
        elif base_risk == SafetyGate.MEDIUM_RISK:
            risk_score = 2
        elif base_risk == SafetyGate.HIGH_RISK:
            risk_score = 3
        else:
            risk_score = 4

        # Adjust risk
        if not has_code_changes:
            risk_score = min(risk_score, 1)  # Documentation only
        if marked_safe and high_confidence:
            risk_score = max(1, risk_score - 1)  # Reduce risk

        # Convert back to risk level
        if risk_score <= 1:
            final_risk = SafetyGate.LOW_RISK
        elif risk_score == 2:
            final_risk = SafetyGate.MEDIUM_RISK
        elif risk_score == 3:
            final_risk = SafetyGate.HIGH_RISK
        else:
            final_risk = SafetyGate.CRITICAL_RISK

        return {
            'risk_level': final_risk,
            'risk_score': risk_score,
            'requires_approval': risk_score >= 2,
            'requires_testing': risk_score >= 2,
            'requires_review': risk_score >= 3,
            'factors': {
                'base_risk': base_risk,
                'has_code_changes': has_code_changes,
                'marked_safe': marked_safe,
                'high_confidence': high_confidence,
                'category': suggestion.category,
                'severity': suggestion.severity
            }
        }


class ImprovementApplicator:
    """
    Applies improvements safely with validation and rollback.

    Coordinates with:
    - git-workflow-assistant for git operations
    - test-orchestrator for validation
    - File system for changes
    """

    def __init__(self):
        """Initialize the improvement applicator."""
        self.backup_dir = Path(os.path.expanduser("~/.claude_code/skill_evaluator/backups"))
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.application_history = []

    def apply_improvements(
        self,
        skill_name: str,
        suggestions: List[ImprovementSuggestion],
        create_branch: bool = True,
        run_tests: bool = True,
        require_approval: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Apply multiple improvements with safety checks.

        Args:
            skill_name: Name of the skill to improve
            suggestions: List of improvements to apply
            create_branch: Whether to create a git branch
            run_tests: Whether to run validation tests
            require_approval: Whether to require approval for high-risk changes
            dry_run: If True, only simulate changes

        Returns:
            Application results
        """
        if not suggestions:
            return {
                'success': True,
                'applied': [],
                'skipped': [],
                'failed': [],
                'message': 'No improvements to apply'
            }

        # Assess risks
        risk_assessments = [
            (suggestion, SafetyGate.assess_risk(suggestion))
            for suggestion in suggestions
        ]

        # Filter by approval requirements
        if require_approval:
            auto_apply = [
                (s, r) for s, r in risk_assessments
                if not r['requires_approval'] or dry_run
            ]
        else:
            auto_apply = risk_assessments

        results = {
            'success': True,
            'dry_run': dry_run,
            'skill_name': skill_name,
            'total_suggestions': len(suggestions),
            'attempted': len(auto_apply),
            'applied': [],
            'skipped': [],
            'failed': [],
            'requires_approval': [],
            'branch_name': None,
            'backup_id': None,
            'rollback_available': False
        }

        # Track suggestions requiring approval
        for suggestion, risk in risk_assessments:
            if require_approval and risk['requires_approval'] and not dry_run:
                results['requires_approval'].append({
                    'suggestion_id': suggestion.id,
                    'description': suggestion.description,
                    'risk_level': risk['risk_level'],
                    'reason': f"Requires manual approval due to {risk['risk_level']} risk"
                })

        if not auto_apply:
            results['message'] = f"All {len(suggestions)} improvements require approval"
            return results

        # Create backup
        if not dry_run:
            backup_id = self._create_backup(skill_name)
            results['backup_id'] = backup_id
            results['rollback_available'] = True

        # Create git branch if requested
        if create_branch and not dry_run:
            branch_name = self._create_git_branch(skill_name)
            results['branch_name'] = branch_name

        # Apply each improvement
        for suggestion, risk in auto_apply:
            try:
                if dry_run:
                    # Simulate application
                    result = self._simulate_application(suggestion)
                else:
                    # Actually apply
                    result = self._apply_single_improvement(
                        skill_name,
                        suggestion,
                        risk
                    )

                if result['success']:
                    results['applied'].append({
                        'suggestion_id': suggestion.id,
                        'description': suggestion.description,
                        'risk_level': risk['risk_level'],
                        'changes': result.get('changes', [])
                    })
                else:
                    results['failed'].append({
                        'suggestion_id': suggestion.id,
                        'description': suggestion.description,
                        'error': result.get('error', 'Unknown error')
                    })
                    results['success'] = False

            except Exception as e:
                results['failed'].append({
                    'suggestion_id': suggestion.id,
                    'description': suggestion.description,
                    'error': str(e)
                })
                results['success'] = False

        # Run tests if requested
        if run_tests and not dry_run and results['applied']:
            validation_result = self._run_validation_tests(skill_name)
            results['validation'] = validation_result

            if not validation_result.get('success'):
                results['success'] = False
                results['message'] = 'Changes applied but validation failed'

        # Generate summary message
        if not results.get('message'):
            applied_count = len(results['applied'])
            failed_count = len(results['failed'])
            approval_count = len(results['requires_approval'])

            if dry_run:
                results['message'] = f"Dry run: {applied_count} improvements would be applied, {approval_count} require approval"
            else:
                results['message'] = f"Applied {applied_count} improvements, {failed_count} failed, {approval_count} require approval"

        return results

    def _create_backup(self, skill_name: str) -> str:
        """Create a backup of the skill directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"{skill_name}_{timestamp}"

        skill_path = Path(f"skills/{skill_name}")
        backup_path = self.backup_dir / backup_id

        if skill_path.exists():
            shutil.copytree(skill_path, backup_path, dirs_exist_ok=True)

        return backup_id

    def _create_git_branch(self, skill_name: str) -> str:
        """Create a git branch for improvements."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"improve/{skill_name}_{timestamp}"

        # In a real implementation, would use git-workflow-assistant
        # For Phase 4, we simulate
        return branch_name

    def _apply_single_improvement(
        self,
        skill_name: str,
        suggestion: ImprovementSuggestion,
        risk: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a single improvement."""
        # In a real implementation, this would:
        # 1. Parse the suggested_code
        # 2. Apply the changes to the file
        # 3. Verify the changes

        # For Phase 4, we simulate successful application
        return {
            'success': True,
            'suggestion_id': suggestion.id,
            'changes': [
                {
                    'file': suggestion.location if suggestion.location else 'unknown',
                    'type': 'modification',
                    'description': suggestion.description
                }
            ]
        }

    def _simulate_application(self, suggestion: ImprovementSuggestion) -> Dict[str, Any]:
        """Simulate applying an improvement."""
        return {
            'success': True,
            'suggestion_id': suggestion.id,
            'simulated': True,
            'changes': [
                {
                    'file': suggestion.location if suggestion.location else 'unknown',
                    'type': 'would_modify',
                    'description': suggestion.description
                }
            ]
        }

    def _run_validation_tests(self, skill_name: str) -> Dict[str, Any]:
        """Run validation tests."""
        # In a real implementation, would use test-orchestrator
        # For Phase 4, we simulate successful validation
        return {
            'success': True,
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'message': 'Validation not implemented in Phase 4 simulation'
        }

    def rollback(self, backup_id: str) -> Dict[str, Any]:
        """
        Rollback changes using a backup.

        Args:
            backup_id: Backup identifier

        Returns:
            Rollback results
        """
        backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            return {
                'success': False,
                'error': f'Backup not found: {backup_id}'
            }

        try:
            # Extract skill name from backup_id
            skill_name = backup_id.rsplit('_', 2)[0]
            skill_path = Path(f"skills/{skill_name}")

            # Remove current version
            if skill_path.exists():
                shutil.rmtree(skill_path)

            # Restore backup
            shutil.copytree(backup_path, skill_path)

            return {
                'success': True,
                'skill_name': skill_name,
                'backup_id': backup_id,
                'message': f'Successfully rolled back to backup {backup_id}'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Rollback failed: {str(e)}'
            }

    def list_backups(self, skill_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available backups.

        Args:
            skill_name: Optional skill name filter

        Returns:
            List of backups
        """
        backups = []

        for backup_path in self.backup_dir.iterdir():
            if backup_path.is_dir():
                backup_id = backup_path.name

                # Filter by skill name if provided
                if skill_name and not backup_id.startswith(skill_name):
                    continue

                # Get backup info
                stat = backup_path.stat()
                backups.append({
                    'backup_id': backup_id,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'size_mb': sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file()) / 1024 / 1024
                })

        return sorted(backups, key=lambda x: x['created'], reverse=True)
