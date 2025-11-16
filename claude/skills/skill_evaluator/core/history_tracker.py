"""
Execution History Tracker

Tracks and persists skill execution history for analysis and monitoring.
"""

import json
import os
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

from skills.skill_evaluator.core.models import ExecutionRecord, ExecutionContext


class ExecutionHistoryTracker:
    """
    Tracks execution history with JSON persistence.

    Thread-safe tracker that records all skill executions and provides
    querying capabilities for analysis.
    """

    def __init__(self, storage_dir: Optional[str] = None):
        """
        Initialize the history tracker.

        Args:
            storage_dir: Directory for storing history files.
                        Defaults to ~/.claude_code/skill_evaluator/history/
        """
        if storage_dir is None:
            storage_dir = os.path.expanduser(
                "~/.claude_code/skill_evaluator/history"
            )

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # In-memory cache for fast access
        self._history: Dict[str, List[ExecutionRecord]] = defaultdict(list)
        self._improvement_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._lock = threading.Lock()

        # Load existing history
        self._load_history()
        self._load_improvement_history()

    def record_execution(self, record: ExecutionRecord) -> None:
        """
        Record a skill execution.

        Args:
            record: ExecutionRecord to store
        """
        with self._lock:
            self._history[record.skill_name].append(record)

            # Persist to disk
            self._persist_record(record)

    def get_recent_executions(
        self,
        skill_name: str,
        limit: int = 100,
        since: Optional[float] = None
    ) -> List[ExecutionRecord]:
        """
        Get recent executions for a skill.

        Args:
            skill_name: Name of the skill
            limit: Maximum number of records to return
            since: Only return records after this timestamp

        Returns:
            List of ExecutionRecords, most recent first
        """
        with self._lock:
            records = self._history.get(skill_name, [])

            # Filter by time if specified
            if since is not None:
                records = [r for r in records if r.timestamp >= since]

            # Sort by timestamp descending and limit
            records = sorted(records, key=lambda r: r.timestamp, reverse=True)
            return records[:limit]

    def get_execution_stats(
        self,
        skill_name: str,
        time_period_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get execution statistics for a skill.

        Args:
            skill_name: Name of the skill
            time_period_days: Limit to last N days (None for all time)

        Returns:
            Dictionary containing execution statistics
        """
        since = None
        if time_period_days is not None:
            since = (datetime.now() - timedelta(days=time_period_days)).timestamp()

        records = self.get_recent_executions(skill_name, limit=10000, since=since)

        if not records:
            return {
                'total_executions': 0,
                'successful_executions': 0,
                'failed_executions': 0,
                'success_rate': 0.0,
                'error_rate': 0.0,
                'avg_duration': 0.0,
                'min_duration': 0.0,
                'max_duration': 0.0,
                'errors_by_code': {},
                'operations_breakdown': {}
            }

        # Calculate statistics
        successful = [r for r in records if r.success]
        failed = [r for r in records if not r.success]

        durations = [r.duration for r in records]
        errors_by_code = defaultdict(int)
        operations_breakdown = defaultdict(int)

        for record in records:
            operations_breakdown[record.operation] += 1
            if record.error_code:
                errors_by_code[record.error_code] += 1

        return {
            'total_executions': len(records),
            'successful_executions': len(successful),
            'failed_executions': len(failed),
            'success_rate': len(successful) / len(records) * 100 if records else 0.0,
            'error_rate': len(failed) / len(records) * 100 if records else 0.0,
            'avg_duration': sum(durations) / len(durations) if durations else 0.0,
            'min_duration': min(durations) if durations else 0.0,
            'max_duration': max(durations) if durations else 0.0,
            'errors_by_code': dict(errors_by_code),
            'operations_breakdown': dict(operations_breakdown),
            'first_execution': min(r.timestamp for r in records),
            'last_execution': max(r.timestamp for r in records),
            'time_period_days': time_period_days
        }

    def get_failed_executions(
        self,
        skill_name: str,
        limit: int = 50,
        error_code: Optional[str] = None
    ) -> List[ExecutionRecord]:
        """
        Get failed executions for analysis.

        Args:
            skill_name: Name of the skill
            limit: Maximum number of records to return
            error_code: Filter by specific error code

        Returns:
            List of failed ExecutionRecords
        """
        with self._lock:
            records = self._history.get(skill_name, [])

            # Filter failures
            failed = [r for r in records if not r.success]

            # Filter by error code if specified
            if error_code is not None:
                failed = [r for r in failed if r.error_code == error_code]

            # Sort by timestamp descending and limit
            failed = sorted(failed, key=lambda r: r.timestamp, reverse=True)
            return failed[:limit]

    def get_execution_by_id(self, execution_id: str) -> Optional[ExecutionRecord]:
        """
        Get a specific execution by ID.

        Args:
            execution_id: Execution ID to find

        Returns:
            ExecutionRecord if found, None otherwise
        """
        with self._lock:
            for records in self._history.values():
                for record in records:
                    if record.execution_id == execution_id:
                        return record
        return None

    def get_all_tracked_skills(self) -> List[str]:
        """
        Get list of all skills with tracked executions.

        Returns:
            List of skill names
        """
        with self._lock:
            return list(self._history.keys())

    def clear_history(self, skill_name: Optional[str] = None) -> None:
        """
        Clear execution history.

        Args:
            skill_name: Clear specific skill (None to clear all)
        """
        with self._lock:
            if skill_name:
                self._history.pop(skill_name, None)
                # Delete file
                history_file = self._get_history_file(skill_name)
                if history_file.exists():
                    history_file.unlink()
            else:
                self._history.clear()
                # Delete all files
                for file in self.storage_dir.glob("*.json"):
                    file.unlink()

    def _get_history_file(self, skill_name: str) -> Path:
        """Get the history file path for a skill."""
        safe_name = skill_name.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{safe_name}.json"

    def _persist_record(self, record: ExecutionRecord) -> None:
        """Persist a record to disk."""
        try:
            history_file = self._get_history_file(record.skill_name)

            # Load existing records
            if history_file.exists():
                with open(history_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {'skill_name': record.skill_name, 'records': []}

            # Append new record
            data['records'].append(record.to_dict())

            # Keep only last 1000 records per skill to prevent unbounded growth
            if len(data['records']) > 1000:
                data['records'] = data['records'][-1000:]

            # Write back
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            # Log error but don't fail the operation
            print(f"Warning: Failed to persist execution record: {e}")

    def _load_history(self) -> None:
        """Load existing history from disk."""
        try:
            for history_file in self.storage_dir.glob("*.json"):
                with open(history_file, 'r') as f:
                    data = json.load(f)

                skill_name = data.get('skill_name')
                if not skill_name:
                    continue

                records = []
                for record_data in data.get('records', []):
                    try:
                        record = ExecutionRecord.from_dict(record_data)
                        records.append(record)
                    except Exception as e:
                        print(f"Warning: Failed to load record: {e}")
                        continue

                self._history[skill_name] = records

        except Exception as e:
            print(f"Warning: Failed to load execution history: {e}")

    def get_performance_baseline(
        self,
        skill_name: str,
        operation: Optional[str] = None,
        days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Get performance baseline for comparison.

        Args:
            skill_name: Name of the skill
            operation: Specific operation (None for all)
            days: Number of days for baseline

        Returns:
            Baseline metrics or None if insufficient data
        """
        since = (datetime.now() - timedelta(days=days)).timestamp()
        records = self.get_recent_executions(skill_name, limit=10000, since=since)

        # Filter by operation if specified
        if operation:
            records = [r for r in records if r.operation == operation]

        if len(records) < 10:  # Need minimum sample size
            return None

        successful = [r for r in records if r.success]
        if not successful:
            return None

        durations = [r.duration for r in successful]

        return {
            'avg_duration': sum(durations) / len(durations),
            'median_duration': sorted(durations)[len(durations) // 2],
            'p95_duration': sorted(durations)[int(len(durations) * 0.95)],
            'min_duration': min(durations),
            'max_duration': max(durations),
            'sample_size': len(successful),
            'success_rate': len(successful) / len(records) * 100,
            'time_period_days': days
        }

    # Improvement History Tracking (Phase 5)

    def record_improvement(
        self,
        skill_name: str,
        improvement_data: Dict[str, Any]
    ) -> None:
        """
        Record an applied improvement.

        Args:
            skill_name: Name of the skill that was improved
            improvement_data: Dictionary containing improvement details:
                - improvement_id: Unique identifier
                - timestamp: When improvement was applied
                - category: Category of improvement
                - severity: Severity level
                - description: Description of improvement
                - expected_impact: Expected impact
                - applied_by: Who/what applied it
                - backup_id: Backup identifier for rollback
                - validation_status: Test validation status
                - actual_impact: Measured impact (added later)
        """
        with self._lock:
            # Add timestamp if not present
            if 'timestamp' not in improvement_data:
                improvement_data['timestamp'] = datetime.now().isoformat()

            # Add improvement_id if not present
            if 'improvement_id' not in improvement_data:
                improvement_data['improvement_id'] = f"{skill_name}_{int(datetime.now().timestamp())}"

            self._improvement_history[skill_name].append(improvement_data)

            # Persist to disk
            self._persist_improvement_history(skill_name)

    def get_improvement_history(
        self,
        skill_name: str,
        limit: int = 50,
        time_period_days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get improvement history for a skill.

        Args:
            skill_name: Name of the skill
            limit: Maximum number of records to return
            time_period_days: Limit to last N days (None for all time)

        Returns:
            List of improvement records, most recent first
        """
        with self._lock:
            improvements = self._improvement_history.get(skill_name, [])

            # Filter by time if specified
            if time_period_days is not None:
                cutoff = (datetime.now() - timedelta(days=time_period_days)).isoformat()
                improvements = [
                    i for i in improvements
                    if i.get('timestamp', '') >= cutoff
                ]

            # Sort by timestamp descending
            improvements = sorted(
                improvements,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )

            return improvements[:limit]

    def get_improvement_stats(
        self,
        skill_name: str,
        time_period_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get improvement statistics for a skill.

        Args:
            skill_name: Name of the skill
            time_period_days: Limit to last N days (None for all time)

        Returns:
            Dictionary containing improvement statistics
        """
        improvements = self.get_improvement_history(
            skill_name,
            limit=1000,
            time_period_days=time_period_days
        )

        if not improvements:
            return {
                'total_improvements': 0,
                'by_category': {},
                'by_severity': {},
                'successful_applications': 0,
                'failed_applications': 0,
                'avg_improvements_per_month': 0.0,
                'most_recent': None
            }

        # Categorize improvements
        by_category = defaultdict(int)
        by_severity = defaultdict(int)
        successful = 0
        failed = 0

        for imp in improvements:
            category = imp.get('category', 'unknown')
            severity = imp.get('severity', 'unknown')
            validation = imp.get('validation_status', {})

            by_category[category] += 1
            by_severity[severity] += 1

            if validation.get('success', False):
                successful += 1
            elif 'success' in validation:
                failed += 1

        # Calculate rate
        if improvements and time_period_days:
            months = time_period_days / 30.0
            avg_per_month = len(improvements) / months if months > 0 else 0
        else:
            avg_per_month = 0

        return {
            'total_improvements': len(improvements),
            'by_category': dict(by_category),
            'by_severity': dict(by_severity),
            'successful_applications': successful,
            'failed_applications': failed,
            'success_rate': successful / len(improvements) * 100 if improvements else 0,
            'avg_improvements_per_month': avg_per_month,
            'most_recent': improvements[0] if improvements else None,
            'time_period_days': time_period_days
        }

    def update_improvement_impact(
        self,
        skill_name: str,
        improvement_id: str,
        impact_data: Dict[str, Any]
    ) -> bool:
        """
        Update the actual impact of an applied improvement.

        Args:
            skill_name: Name of the skill
            improvement_id: ID of the improvement
            impact_data: Dictionary containing impact metrics:
                - actual_impact: Measured impact description
                - metrics_before: Metrics before improvement
                - metrics_after: Metrics after improvement
                - improvement_percentage: Percentage improvement
                - verified: Whether impact was verified

        Returns:
            True if updated, False if improvement not found
        """
        with self._lock:
            improvements = self._improvement_history.get(skill_name, [])

            for imp in improvements:
                if imp.get('improvement_id') == improvement_id:
                    imp['impact_data'] = impact_data
                    imp['impact_measured_at'] = datetime.now().isoformat()

                    # Persist changes
                    self._persist_improvement_history(skill_name)
                    return True

        return False

    def analyze_improvement_effectiveness(
        self,
        skill_name: str,
        time_period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze the effectiveness of applied improvements.

        Args:
            skill_name: Name of the skill
            time_period_days: Period to analyze

        Returns:
            Dictionary containing effectiveness analysis
        """
        improvements = self.get_improvement_history(
            skill_name,
            limit=1000,
            time_period_days=time_period_days
        )

        if not improvements:
            return {
                'has_data': False,
                'message': 'No improvements found in time period'
            }

        # Analyze improvements with impact data
        measured = [i for i in improvements if 'impact_data' in i]
        verified_positive = [
            i for i in measured
            if i.get('impact_data', {}).get('verified') and
            i.get('impact_data', {}).get('improvement_percentage', 0) > 0
        ]
        verified_negative = [
            i for i in measured
            if i.get('impact_data', {}).get('verified') and
            i.get('impact_data', {}).get('improvement_percentage', 0) <= 0
        ]

        # Calculate average impact by category
        impact_by_category = defaultdict(list)
        for imp in verified_positive:
            category = imp.get('category', 'unknown')
            percentage = imp.get('impact_data', {}).get('improvement_percentage', 0)
            impact_by_category[category].append(percentage)

        avg_impact_by_category = {
            cat: sum(percentages) / len(percentages)
            for cat, percentages in impact_by_category.items()
        }

        return {
            'has_data': True,
            'total_improvements': len(improvements),
            'measured_improvements': len(measured),
            'measurement_rate': len(measured) / len(improvements) * 100,
            'verified_positive': len(verified_positive),
            'verified_negative': len(verified_negative),
            'effectiveness_rate': len(verified_positive) / len(measured) * 100 if measured else 0,
            'avg_impact_by_category': avg_impact_by_category,
            'most_effective_category': max(
                avg_impact_by_category.items(),
                key=lambda x: x[1]
            )[0] if avg_impact_by_category else None,
            'recommendations': self._generate_improvement_recommendations(
                improvements, impact_by_category
            )
        }

    def _generate_improvement_recommendations(
        self,
        improvements: List[Dict[str, Any]],
        impact_by_category: Dict[str, List[float]]
    ) -> List[str]:
        """Generate recommendations based on improvement history."""
        recommendations = []

        # Recommend focusing on high-impact categories
        if impact_by_category:
            best_category = max(impact_by_category.items(), key=lambda x: sum(x[1]))
            recommendations.append(
                f"Focus on {best_category[0]} improvements - showing {sum(best_category[1])/len(best_category[1]):.1f}% average impact"
            )

        # Check for unmeasured improvements
        measured_count = sum(1 for i in improvements if 'impact_data' in i)
        if measured_count < len(improvements) * 0.5:
            recommendations.append(
                "Increase impact measurement rate - currently only "
                f"{measured_count/len(improvements)*100:.0f}% of improvements are measured"
            )

        # Check for recent activity
        recent_improvements = [
            i for i in improvements
            if (datetime.now() - datetime.fromisoformat(i.get('timestamp', datetime.now().isoformat()))).days < 30
        ]
        if len(recent_improvements) < 2:
            recommendations.append(
                "Low improvement activity - consider running evaluation to identify opportunities"
            )

        return recommendations

    def _get_improvement_history_file(self, skill_name: str) -> Path:
        """Get the improvement history file path for a skill."""
        safe_name = skill_name.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{safe_name}_improvements.json"

    def _persist_improvement_history(self, skill_name: str) -> None:
        """Persist improvement history to disk."""
        try:
            history_file = self._get_improvement_history_file(skill_name)
            improvements = self._improvement_history.get(skill_name, [])

            data = {
                'skill_name': skill_name,
                'improvements': improvements
            }

            # Keep only last 500 improvement records to prevent unbounded growth
            if len(data['improvements']) > 500:
                data['improvements'] = data['improvements'][-500:]

            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Warning: Failed to persist improvement history: {e}")

    def _load_improvement_history(self) -> None:
        """Load existing improvement history from disk."""
        try:
            for history_file in self.storage_dir.glob("*_improvements.json"):
                with open(history_file, 'r') as f:
                    data = json.load(f)

                skill_name = data.get('skill_name')
                if not skill_name:
                    continue

                improvements = data.get('improvements', [])
                self._improvement_history[skill_name] = improvements

        except Exception as e:
            print(f"Warning: Failed to load improvement history: {e}")
