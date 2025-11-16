"""
Cross-Skill Analyzer

Analyzes interactions, dependencies, and patterns across multiple skills
to identify optimization opportunities and potential issues.
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import time


class CrossSkillAnalyzer:
    """
    Analyzes interactions and dependencies between skills.

    Provides insights into:
    - Skill interaction patterns
    - Dependency chains
    - Workflow bottlenecks
    - Cross-skill performance issues
    - Optimization opportunities
    """

    def __init__(self, history_tracker):
        """
        Initialize the cross-skill analyzer.

        Args:
            history_tracker: ExecutionHistoryTracker instance
        """
        self.history_tracker = history_tracker

    def analyze_skill_interactions(
        self,
        time_period_days: int = 30,
        min_interactions: int = 2
    ) -> Dict[str, Any]:
        """
        Analyze how skills interact with each other.

        Args:
            time_period_days: Time period to analyze
            min_interactions: Minimum interaction count to include

        Returns:
            Dictionary containing interaction analysis
        """
        # Get all tracked skills
        all_skills = self.history_tracker.get_all_tracked_skills()

        if len(all_skills) < 2:
            return {
                'has_data': False,
                'message': 'Need at least 2 skills with execution history'
            }

        # Analyze interactions by time proximity
        interactions = defaultdict(int)
        skill_pairs = defaultdict(list)

        # For each skill, get recent executions
        for skill in all_skills:
            since = (datetime.now() - timedelta(days=time_period_days)).timestamp()
            executions = self.history_tracker.get_recent_executions(
                skill_name=skill,
                limit=1000,
                since=since
            )

            for exec_record in executions:
                # Look for executions of other skills within 5 seconds
                exec_time = exec_record.timestamp

                for other_skill in all_skills:
                    if other_skill == skill:
                        continue

                    other_execs = self.history_tracker.get_recent_executions(
                        skill_name=other_skill,
                        limit=1000,
                        since=since
                    )

                    for other_exec in other_execs:
                        time_diff = abs(other_exec.timestamp - exec_time)
                        if time_diff < 5.0:  # Within 5 seconds
                            pair = tuple(sorted([skill, other_skill]))
                            interactions[pair] += 1
                            skill_pairs[pair].append({
                                'skill1': skill,
                                'skill2': other_skill,
                                'time_diff': time_diff,
                                'timestamp': exec_time
                            })

        # Filter by minimum interactions
        filtered_interactions = {
            pair: count for pair, count in interactions.items()
            if count >= min_interactions
        }

        # Identify most common interactions
        top_interactions = sorted(
            filtered_interactions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Calculate interaction matrix
        interaction_matrix = self._build_interaction_matrix(
            all_skills,
            filtered_interactions
        )

        # Identify skill clusters
        clusters = self._identify_clusters(interaction_matrix, all_skills)

        return {
            'has_data': True,
            'total_skills': len(all_skills),
            'interacting_pairs': len(filtered_interactions),
            'total_interactions': sum(filtered_interactions.values()),
            'top_interactions': [
                {
                    'skills': list(pair),
                    'interaction_count': count,
                    'avg_time_between': sum(
                        sp['time_diff'] for sp in skill_pairs[pair]
                    ) / len(skill_pairs[pair])
                }
                for pair, count in top_interactions
            ],
            'interaction_matrix': interaction_matrix,
            'skill_clusters': clusters,
            'time_period_days': time_period_days
        }

    def detect_dependency_chains(
        self,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Detect skill dependency chains and execution sequences.

        Args:
            time_period_days: Time period to analyze

        Returns:
            Dictionary containing dependency chain analysis
        """
        all_skills = self.history_tracker.get_all_tracked_skills()

        if len(all_skills) < 2:
            return {
                'has_data': False,
                'message': 'Need at least 2 skills with execution history'
            }

        # Track sequences: skill A followed by skill B
        sequences = defaultdict(int)
        sequence_details = defaultdict(list)

        since = (datetime.now() - timedelta(days=time_period_days)).timestamp()

        # Get all executions across all skills, sorted by time
        all_executions = []
        for skill in all_skills:
            execs = self.history_tracker.get_recent_executions(
                skill_name=skill,
                limit=1000,
                since=since
            )
            for exec_record in execs:
                all_executions.append({
                    'skill': skill,
                    'timestamp': exec_record.timestamp,
                    'success': exec_record.success,
                    'duration': exec_record.duration
                })

        # Sort by timestamp
        all_executions.sort(key=lambda x: x['timestamp'])

        # Find sequences (within 10 seconds)
        for i in range(len(all_executions) - 1):
            current = all_executions[i]
            next_exec = all_executions[i + 1]

            time_diff = next_exec['timestamp'] - current['timestamp']
            if time_diff < 10.0 and current['skill'] != next_exec['skill']:
                sequence = (current['skill'], next_exec['skill'])
                sequences[sequence] += 1
                sequence_details[sequence].append({
                    'time_diff': time_diff,
                    'first_success': current['success'],
                    'second_success': next_exec['success']
                })

        # Identify most common chains
        top_chains = sorted(
            sequences.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Detect circular dependencies
        circular_deps = self._detect_circular_dependencies(sequences)

        # Calculate chain reliability
        chain_reliability = {}
        for chain, count in sequences.items():
            details = sequence_details[chain]
            successful_chains = sum(
                1 for d in details
                if d['first_success'] and d['second_success']
            )
            chain_reliability[chain] = {
                'count': count,
                'success_rate': successful_chains / count * 100 if count > 0 else 0,
                'avg_time_between': sum(d['time_diff'] for d in details) / len(details)
            }

        return {
            'has_data': True,
            'total_sequences': len(sequences),
            'total_occurrences': sum(sequences.values()),
            'top_chains': [
                {
                    'from_skill': chain[0],
                    'to_skill': chain[1],
                    'occurrences': count,
                    'reliability': chain_reliability[chain]
                }
                for chain, count in top_chains
            ],
            'circular_dependencies': circular_deps,
            'time_period_days': time_period_days
        }

    def analyze_workflow_patterns(
        self,
        time_period_days: int = 30,
        min_pattern_length: int = 2,
        max_pattern_length: int = 5
    ) -> Dict[str, Any]:
        """
        Identify common workflow patterns (skill execution sequences).

        Args:
            time_period_days: Time period to analyze
            min_pattern_length: Minimum pattern length
            max_pattern_length: Maximum pattern length

        Returns:
            Dictionary containing workflow pattern analysis
        """
        all_skills = self.history_tracker.get_all_tracked_skills()

        if len(all_skills) < 2:
            return {
                'has_data': False,
                'message': 'Need at least 2 skills with execution history'
            }

        since = (datetime.now() - timedelta(days=time_period_days)).timestamp()

        # Get all executions, sorted by time
        all_executions = []
        for skill in all_skills:
            execs = self.history_tracker.get_recent_executions(
                skill_name=skill,
                limit=1000,
                since=since
            )
            for exec_record in execs:
                all_executions.append({
                    'skill': skill,
                    'timestamp': exec_record.timestamp,
                    'success': exec_record.success
                })

        all_executions.sort(key=lambda x: x['timestamp'])

        # Extract patterns
        patterns = defaultdict(int)
        pattern_details = defaultdict(list)

        for length in range(min_pattern_length, max_pattern_length + 1):
            for i in range(len(all_executions) - length + 1):
                window = all_executions[i:i + length]

                # Check if executions are close in time (within 30 seconds total)
                time_span = window[-1]['timestamp'] - window[0]['timestamp']
                if time_span < 30.0:
                    pattern = tuple(w['skill'] for w in window)
                    patterns[pattern] += 1
                    pattern_details[pattern].append({
                        'timestamp': window[0]['timestamp'],
                        'duration': time_span,
                        'all_successful': all(w['success'] for w in window)
                    })

        # Filter and rank patterns
        significant_patterns = {
            p: count for p, count in patterns.items()
            if count >= 2  # Occurred at least twice
        }

        top_patterns = sorted(
            significant_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Analyze pattern characteristics
        pattern_analysis = []
        for pattern, count in top_patterns:
            details = pattern_details[pattern]
            successful_count = sum(1 for d in details if d['all_successful'])

            pattern_analysis.append({
                'pattern': list(pattern),
                'occurrences': count,
                'success_rate': successful_count / count * 100 if count > 0 else 0,
                'avg_duration': sum(d['duration'] for d in details) / len(details),
                'length': len(pattern)
            })

        return {
            'has_data': True,
            'total_patterns_found': len(significant_patterns),
            'top_patterns': pattern_analysis,
            'time_period_days': time_period_days
        }

    def identify_bottlenecks(
        self,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Identify skills that are bottlenecks in workflows.

        A bottleneck is identified by:
        - High frequency in chains
        - Long duration
        - High failure rate

        Args:
            time_period_days: Time period to analyze

        Returns:
            Dictionary containing bottleneck analysis
        """
        all_skills = self.history_tracker.get_all_tracked_skills()

        bottleneck_scores = {}

        for skill in all_skills:
            stats = self.history_tracker.get_execution_stats(
                skill_name=skill,
                time_period_days=time_period_days
            )

            if stats['total_executions'] < 5:
                continue

            # Calculate bottleneck score based on multiple factors
            frequency_score = min(stats['total_executions'] / 100, 1.0) * 30
            duration_score = min(stats['avg_duration'] / 10.0, 1.0) * 40
            failure_score = (stats['error_rate'] / 100) * 30

            total_score = frequency_score + duration_score + failure_score

            bottleneck_scores[skill] = {
                'bottleneck_score': total_score,
                'frequency': stats['total_executions'],
                'avg_duration': stats['avg_duration'],
                'error_rate': stats['error_rate'],
                'factors': {
                    'high_frequency': frequency_score,
                    'slow_execution': duration_score,
                    'high_failure_rate': failure_score
                }
            }

        # Rank by bottleneck score
        ranked_bottlenecks = sorted(
            bottleneck_scores.items(),
            key=lambda x: x[1]['bottleneck_score'],
            reverse=True
        )

        # Categorize severity
        bottlenecks_by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }

        for skill, data in ranked_bottlenecks:
            score = data['bottleneck_score']
            if score >= 70:
                bottlenecks_by_severity['critical'].append({'skill': skill, **data})
            elif score >= 50:
                bottlenecks_by_severity['high'].append({'skill': skill, **data})
            elif score >= 30:
                bottlenecks_by_severity['medium'].append({'skill': skill, **data})
            else:
                bottlenecks_by_severity['low'].append({'skill': skill, **data})

        return {
            'has_data': True,
            'total_analyzed': len(bottleneck_scores),
            'bottlenecks': ranked_bottlenecks[:10],
            'by_severity': bottlenecks_by_severity,
            'recommendations': self._generate_bottleneck_recommendations(
                bottlenecks_by_severity
            ),
            'time_period_days': time_period_days
        }

    def suggest_workflow_optimizations(
        self,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Suggest optimizations for skill workflows.

        Args:
            time_period_days: Time period to analyze

        Returns:
            Dictionary containing optimization suggestions
        """
        suggestions = []

        # Analyze interactions
        interactions = self.analyze_skill_interactions(time_period_days)
        if interactions.get('has_data'):
            if interactions['total_interactions'] > 100:
                suggestions.append({
                    'type': 'high_coupling',
                    'severity': 'medium',
                    'description': f"High coupling detected: {interactions['interacting_pairs']} skill pairs interact frequently",
                    'recommendation': "Consider creating composite skills for common interaction patterns",
                    'impact': 'Reduce overhead and improve maintainability'
                })

        # Analyze chains
        chains = self.detect_dependency_chains(time_period_days)
        if chains.get('has_data'):
            # Check for circular dependencies
            if chains['circular_dependencies']:
                suggestions.append({
                    'type': 'circular_dependency',
                    'severity': 'high',
                    'description': f"Circular dependencies detected: {len(chains['circular_dependencies'])} cycles",
                    'recommendation': "Break circular dependencies by refactoring skill interfaces",
                    'impact': 'Prevent potential deadlocks and improve system stability',
                    'details': chains['circular_dependencies']
                })

            # Check chain reliability
            unreliable_chains = [
                chain for chain in chains['top_chains']
                if chain['reliability']['success_rate'] < 80
            ]
            if unreliable_chains:
                suggestions.append({
                    'type': 'unreliable_chain',
                    'severity': 'high',
                    'description': f"{len(unreliable_chains)} skill chains have low reliability (<80%)",
                    'recommendation': "Improve error handling in chain components",
                    'impact': 'Increase workflow success rate',
                    'details': unreliable_chains[:3]
                })

        # Analyze bottlenecks
        bottlenecks = self.identify_bottlenecks(time_period_days)
        if bottlenecks.get('has_data'):
            critical_bottlenecks = bottlenecks['by_severity']['critical']
            if critical_bottlenecks:
                suggestions.append({
                    'type': 'critical_bottleneck',
                    'severity': 'critical',
                    'description': f"{len(critical_bottlenecks)} critical bottlenecks identified",
                    'recommendation': "Optimize critical bottleneck skills urgently",
                    'impact': 'Significant performance improvement',
                    'details': [b['skill'] for b in critical_bottlenecks]
                })

        # Analyze patterns
        patterns = self.analyze_workflow_patterns(time_period_days)
        if patterns.get('has_data'):
            common_patterns = [
                p for p in patterns['top_patterns']
                if p['occurrences'] >= 10 and p['length'] >= 3
            ]
            if common_patterns:
                suggestions.append({
                    'type': 'workflow_consolidation',
                    'severity': 'low',
                    'description': f"{len(common_patterns)} common workflow patterns detected",
                    'recommendation': "Consider creating dedicated workflow skills for common patterns",
                    'impact': 'Simplify usage and improve performance',
                    'details': common_patterns[:3]
                })

        return {
            'has_data': len(suggestions) > 0,
            'total_suggestions': len(suggestions),
            'suggestions': suggestions,
            'priority_actions': [
                s for s in suggestions
                if s['severity'] in ['critical', 'high']
            ],
            'time_period_days': time_period_days
        }

    # Helper methods

    def _build_interaction_matrix(
        self,
        skills: List[str],
        interactions: Dict[Tuple[str, str], int]
    ) -> Dict[str, Dict[str, int]]:
        """Build an interaction matrix for skills."""
        matrix = {skill: {other: 0 for other in skills} for skill in skills}

        for (skill1, skill2), count in interactions.items():
            matrix[skill1][skill2] = count
            matrix[skill2][skill1] = count

        return matrix

    def _identify_clusters(
        self,
        interaction_matrix: Dict[str, Dict[str, int]],
        skills: List[str]
    ) -> List[Set[str]]:
        """Identify clusters of frequently interacting skills."""
        clusters = []
        visited = set()

        for skill in skills:
            if skill in visited:
                continue

            # Find skills that interact with this one
            cluster = {skill}
            queue = [skill]

            while queue:
                current = queue.pop(0)
                visited.add(current)

                # Find strongly connected skills (interaction count >= 5)
                for other, count in interaction_matrix[current].items():
                    if count >= 5 and other not in visited and other not in cluster:
                        cluster.add(other)
                        queue.append(other)

            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def _detect_circular_dependencies(
        self,
        sequences: Dict[Tuple[str, str], int]
    ) -> List[List[str]]:
        """Detect circular dependency chains."""
        # Build directed graph
        graph = defaultdict(set)
        for (from_skill, to_skill), count in sequences.items():
            graph[from_skill].add(to_skill)

        # Find cycles using DFS
        cycles = []
        visited = set()
        rec_stack = []

        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = rec_stack.index(node)
                cycle = rec_stack[cycle_start:] + [node]
                if len(cycle) >= 3:  # Only include cycles of 3+ skills
                    cycles.append(cycle)
                return

            if node in visited:
                return

            visited.add(node)
            rec_stack.append(node)

            for neighbor in graph.get(node, []):
                dfs(neighbor, path + [node])

            rec_stack.pop()

        for skill in graph.keys():
            dfs(skill, [])

        # Remove duplicates
        unique_cycles = []
        seen = set()
        for cycle in cycles:
            normalized = tuple(sorted(cycle))
            if normalized not in seen:
                seen.add(normalized)
                unique_cycles.append(cycle)

        return unique_cycles

    def _generate_bottleneck_recommendations(
        self,
        bottlenecks_by_severity: Dict[str, List[Dict]]
    ) -> List[str]:
        """Generate recommendations for addressing bottlenecks."""
        recommendations = []

        if bottlenecks_by_severity['critical']:
            recommendations.append(
                f"Address {len(bottlenecks_by_severity['critical'])} critical bottlenecks immediately - "
                "these are significantly impacting workflow performance"
            )

        if bottlenecks_by_severity['high']:
            recommendations.append(
                f"Prioritize optimization of {len(bottlenecks_by_severity['high'])} high-impact bottlenecks"
            )

        # Check for high failure rates
        high_failure = [
            b for severity in ['critical', 'high']
            for b in bottlenecks_by_severity.get(severity, [])
            if b.get('error_rate', 0) > 20
        ]
        if high_failure:
            recommendations.append(
                f"Focus on reliability improvements for {len(high_failure)} skills with high failure rates"
            )

        # Check for slow execution
        slow_skills = [
            b for severity in ['critical', 'high']
            for b in bottlenecks_by_severity.get(severity, [])
            if b.get('avg_duration', 0) > 5.0
        ]
        if slow_skills:
            recommendations.append(
                f"Optimize performance for {len(slow_skills)} slow-executing skills"
            )

        if not recommendations:
            recommendations.append("No critical bottlenecks detected - system is performing well")

        return recommendations
