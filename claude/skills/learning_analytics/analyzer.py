"""
Learning Analytics Analyzer

Main analyzer class that performs comprehensive analysis of learning plans.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import statistics

from skills.learning_plan_manager import LearningPlanManager, LearningPlan, Task, TaskStatus, CheckpointStatus
from .models import (
    VelocityMetrics,
    StruggleArea,
    StruggleIndicator,
    CheckpointAnalysis,
    CheckpointPerformance,
    LearningPattern,
    PatternType,
    TimeEstimationAnalysis,
    LearningRecommendation,
    RecommendationPriority,
    RecommendationType,
    LearningAnalytics
)


class LearningAnalyzer:
    """Analyzes learning plan data to generate insights"""

    def __init__(self):
        """Initialize analyzer"""
        self.plan_manager = LearningPlanManager()

    def analyze_plan(
        self,
        plan: LearningPlan,
        include_predictions: bool = True
    ) -> LearningAnalytics:
        """
        Perform comprehensive analysis of learning plan.

        Args:
            plan: LearningPlan to analyze
            include_predictions: Whether to include future predictions

        Returns:
            LearningAnalytics with all metrics and recommendations
        """
        # Calculate all metrics
        velocity = self.calculate_velocity(plan)
        struggles = self.detect_struggle_areas(plan)
        checkpoints = self.analyze_checkpoints(plan)
        patterns = self.detect_patterns(plan)
        time_est = self.analyze_time_estimates(plan)

        # Generate recommendations
        analytics = LearningAnalytics(
            plan_title=plan.metadata.title,
            velocity_metrics=velocity,
            struggle_areas=struggles,
            checkpoint_analysis=checkpoints,
            time_estimation=time_est,
            learning_patterns=patterns,
            recommendations=[],  # Will be filled
            overall_health="good",  # Will be determined
            key_insights=[],
            strengths=[],
            growth_areas=[]
        )

        # Generate recommendations based on all metrics
        analytics.recommendations = self.generate_recommendations(plan, analytics)

        # Determine overall health
        analytics.overall_health = self._determine_overall_health(analytics)

        # Extract key insights
        analytics.key_insights = self._extract_key_insights(analytics, plan)

        # Identify strengths and growth areas
        analytics.strengths = self._identify_strengths(analytics, plan)
        analytics.growth_areas = self._identify_growth_areas(analytics, plan)

        return analytics

    def calculate_velocity(
        self,
        plan: LearningPlan
    ) -> VelocityMetrics:
        """Calculate learning velocity metrics"""

        # Get all completed tasks
        completed_tasks = []
        for phase in plan.phases:
            for task in phase.tasks:
                if task.status == TaskStatus.COMPLETED:
                    completed_tasks.append(task)

        if not completed_tasks:
            # No completed tasks yet
            return VelocityMetrics(
                tasks_per_week=0.0,
                tasks_completed_total=0,
                days_active=0,
                velocity_trend="unknown",
                recent_velocity=0.0,
                overall_velocity=0.0,
                on_track=True  # Not enough data to determine
            )

        # Calculate time range
        start_date = self._parse_date(plan.metadata.created)
        current_date = datetime.now()

        if start_date:
            days_active = (current_date - start_date).days
            weeks_active = max(days_active / 7.0, 0.1)  # Minimum 0.1 weeks
        else:
            # Estimate based on completed task dates
            days_active = 30  # Default estimate
            weeks_active = 4.0

        # Calculate overall velocity
        overall_velocity = len(completed_tasks) / weeks_active

        # Calculate recent velocity (last 2 weeks)
        two_weeks_ago = current_date - timedelta(days=14)
        recent_tasks = [
            t for t in completed_tasks
            if t.completed_at and self._parse_date(t.completed_at) and
            self._parse_date(t.completed_at) >= two_weeks_ago
        ]
        recent_velocity = len(recent_tasks) / 2.0  # Per week over last 2 weeks

        # Determine trend
        velocity_trend = self._analyze_velocity_trend(
            completed_tasks, overall_velocity, recent_velocity
        )

        # Calculate estimated completion date
        total_tasks = sum(len(phase.tasks) for phase in plan.phases)
        remaining_tasks = total_tasks - len(completed_tasks)

        estimated_completion_date = None
        on_track = True

        if overall_velocity > 0:
            weeks_remaining = remaining_tasks / overall_velocity
            completion_date = current_date + timedelta(weeks=weeks_remaining)
            estimated_completion_date = completion_date.strftime("%Y-%m-%d")

            # Check if on track (compare to original estimate)
            estimated_weeks = self._parse_time_estimate(plan.metadata.estimated_time)
            if estimated_weeks:
                projected_weeks = weeks_active + weeks_remaining
                on_track = projected_weeks <= estimated_weeks * 1.2  # 20% buffer

        return VelocityMetrics(
            tasks_per_week=round(overall_velocity, 2),
            tasks_completed_total=len(completed_tasks),
            days_active=days_active,
            velocity_trend=velocity_trend,
            recent_velocity=round(recent_velocity, 2),
            overall_velocity=round(overall_velocity, 2),
            estimated_completion_date=estimated_completion_date,
            on_track=on_track
        )

    def detect_struggle_areas(
        self,
        plan: LearningPlan
    ) -> List[StruggleArea]:
        """Identify areas where student is struggling"""

        struggles = []
        current_date = datetime.now()

        for phase in plan.phases:
            for task in phase.tasks:
                # Check if task is in progress for a long time
                if task.status == TaskStatus.IN_PROGRESS:
                    if task.started_at:
                        start = self._parse_date(task.started_at)
                        if start:
                            duration = (current_date - start).days

                            # Determine severity and create struggle area
                            if duration >= 7:
                                indicators = [StruggleIndicator.LONG_DURATION]

                                if duration >= 21:
                                    severity = "severe"
                                elif duration >= 14:
                                    severity = "moderate"
                                else:
                                    severity = "minor"

                                # Check for stuck indicator in notes
                                if task.notes and any(
                                    word in task.notes.lower()
                                    for word in ["stuck", "difficult", "help", "struggling"]
                                ):
                                    indicators.append(StruggleIndicator.STUCK)
                                    # Increase severity
                                    if severity == "minor":
                                        severity = "moderate"

                                recommendation = self._generate_struggle_recommendation(
                                    severity, duration, task.title
                                )

                                specialist = self._suggest_specialist(task.title, plan.metadata.title)

                                struggles.append(StruggleArea(
                                    task_id=task.id,
                                    task_title=task.title,
                                    phase_number=phase.number,
                                    indicators=indicators,
                                    severity=severity,
                                    duration_days=duration,
                                    expected_duration_days=7,  # Default expectation
                                    recommendation=recommendation,
                                    specialist_suggestion=specialist
                                ))

        # Check for failed checkpoints
        for phase in plan.phases:
            for checkpoint in phase.checkpoints:
                if checkpoint.status == CheckpointStatus.FAILED:
                    # Find related tasks
                    related_tasks = [t.id for t in phase.tasks if t.status == TaskStatus.COMPLETED]

                    struggles.append(StruggleArea(
                        task_id=checkpoint.id,
                        task_title=checkpoint.title,
                        phase_number=phase.number,
                        indicators=[StruggleIndicator.CHECKPOINT_FAILED],
                        severity="severe",
                        recommendation="Review phase concepts before retrying checkpoint",
                        specialist_suggestion="learning-coordinator"
                    ))

        # Sort by severity (severe first)
        severity_order = {"severe": 0, "moderate": 1, "minor": 2}
        struggles.sort(key=lambda s: severity_order.get(s.severity, 3))

        return struggles

    def analyze_checkpoints(
        self,
        plan: LearningPlan
    ) -> CheckpointAnalysis:
        """Analyze checkpoint performance"""

        all_checkpoints = []
        passed = 0
        failed = 0
        not_attempted = 0
        first_try_passes = 0

        for phase in plan.phases:
            for checkpoint in phase.checkpoints:
                # Determine status
                if checkpoint.status == CheckpointStatus.PASSED:
                    passed += 1
                    passed_first = True  # Assume first try unless noted
                    first_try_passes += 1
                elif checkpoint.status == CheckpointStatus.FAILED:
                    failed += 1
                    passed_first = False
                else:
                    not_attempted += 1
                    passed_first = False

                # Find related struggles
                phase_tasks = [t.id for t in phase.tasks]

                perf = CheckpointPerformance(
                    checkpoint_id=checkpoint.id,
                    checkpoint_title=checkpoint.title,
                    phase_number=phase.number,
                    status=checkpoint.status.value,
                    passed_on_first_try=passed_first,
                    related_struggle_areas=phase_tasks if failed > 0 else []
                )
                all_checkpoints.append(perf)

        total = passed + failed + not_attempted
        attempted = passed + failed

        pass_rate = (passed / attempted * 100) if attempted > 0 else 0.0
        first_try_rate = (first_try_passes / attempted * 100) if attempted > 0 else 0.0

        # Detect patterns
        patterns = []
        if first_try_rate == 100 and attempted > 0:
            patterns.append("All attempted checkpoints passed on first try")
            patterns.append("Strong conceptual understanding demonstrated")
        elif pass_rate == 100 and attempted > 0:
            patterns.append("All checkpoints eventually passed")

        if failed > 0:
            patterns.append(f"{failed} checkpoint(s) failed - may need concept review")

        return CheckpointAnalysis(
            total_checkpoints=total,
            passed_checkpoints=passed,
            failed_checkpoints=failed,
            not_attempted_checkpoints=not_attempted,
            pass_rate=round(pass_rate, 1),
            first_try_pass_rate=round(first_try_rate, 1),
            checkpoint_performances=all_checkpoints,
            patterns=patterns
        )

    def detect_patterns(
        self,
        plan: LearningPlan
    ) -> List[LearningPattern]:
        """Detect learning patterns"""

        patterns = []

        # Get completed tasks
        completed_tasks = []
        for phase in plan.phases:
            for task in phase.tasks:
                if task.status == TaskStatus.COMPLETED and task.completed_at:
                    completed_tasks.append(task)

        if len(completed_tasks) >= 3:
            # Check for steady progress pattern
            steady = self._detect_steady_progress_pattern(completed_tasks)
            if steady:
                patterns.append(steady)

            # Check for burst progress pattern
            burst = self._detect_burst_progress_pattern(completed_tasks)
            if burst:
                patterns.append(burst)

        # Sort by confidence
        patterns.sort(key=lambda p: p.confidence, reverse=True)

        return patterns

    def analyze_time_estimates(
        self,
        plan: LearningPlan
    ) -> TimeEstimationAnalysis:
        """Analyze time estimation accuracy"""

        # Parse estimated time from plan
        estimated_weeks = self._parse_time_estimate(plan.metadata.estimated_time)

        # Calculate actual weeks so far
        start_date = self._parse_date(plan.metadata.created)
        if start_date:
            actual_weeks = (datetime.now() - start_date).days / 7.0
        else:
            actual_weeks = 1.0  # Default

        # Calculate progress
        progress = plan.calculate_progress()
        completion_pct = progress["overall_percentage"] / 100.0

        # Project total weeks
        projected_weeks = None
        estimation_accuracy = None
        variance_pct = None
        recommendations = []

        if completion_pct > 0.1:  # At least 10% complete
            projected_weeks = actual_weeks / completion_pct

            if estimated_weeks:
                variance_pct = ((projected_weeks - estimated_weeks) / estimated_weeks) * 100

                if abs(variance_pct) < 10:
                    estimation_accuracy = "accurate"
                elif variance_pct < 0:
                    estimation_accuracy = "pessimistic"
                    recommendations.append(
                        f"Original estimate was {abs(variance_pct):.1f}% longer than needed"
                    )
                else:
                    estimation_accuracy = "optimistic"
                    recommendations.append(
                        f"Consider adding {variance_pct:.1f}% buffer to future estimates"
                    )

        return TimeEstimationAnalysis(
            estimated_total_weeks=estimated_weeks,
            actual_weeks_so_far=round(actual_weeks, 1),
            projected_total_weeks=round(projected_weeks, 1) if projected_weeks else None,
            estimation_accuracy=estimation_accuracy,
            variance_percentage=round(variance_pct, 1) if variance_pct else None,
            recommendations=recommendations
        )

    def generate_recommendations(
        self,
        plan: LearningPlan,
        analytics: Optional[LearningAnalytics] = None
    ) -> List[LearningRecommendation]:
        """Generate actionable recommendations"""

        if analytics is None:
            analytics = self.analyze_plan(plan, include_predictions=False)

        recommendations = []

        # Struggle-based recommendations (CRITICAL/HIGH)
        for struggle in analytics.struggle_areas:
            if struggle.severity == "severe":
                recommendations.append(LearningRecommendation(
                    priority=RecommendationPriority.CRITICAL,
                    recommendation_type=RecommendationType.SPECIALIST_CONSULTATION,
                    title=f"Address {struggle.task_title} immediately",
                    description=f"Student has been struggling with this task for {struggle.duration_days} days",
                    rationale=f"Severe struggle detected: {', '.join(i.value for i in struggle.indicators)}",
                    suggested_action=f"Engage {struggle.specialist_suggestion or 'appropriate specialist'} for guidance",
                    target_agent="learning-coordinator",
                    expected_impact="Unblock student and restore progress",
                    evidence=[
                        f"Task duration: {struggle.duration_days} days",
                        f"Expected: {struggle.expected_duration_days} days"
                    ]
                ))
            elif struggle.severity == "moderate":
                recommendations.append(LearningRecommendation(
                    priority=RecommendationPriority.HIGH,
                    recommendation_type=RecommendationType.SPECIALIST_CONSULTATION,
                    title=f"Schedule review for {struggle.task_title}",
                    description="Task taking longer than expected",
                    rationale=struggle.recommendation,
                    suggested_action=f"Consult {struggle.specialist_suggestion or 'specialist'} if still stuck in 3-4 days",
                    target_agent="learning-coordinator",
                    expected_impact="Faster task completion with guidance",
                    evidence=[f"Task duration: {struggle.duration_days} days"]
                ))

        # Velocity-based recommendations
        if analytics.velocity_metrics.velocity_trend == "decreasing":
            recommendations.append(LearningRecommendation(
                priority=RecommendationPriority.HIGH,
                recommendation_type=RecommendationType.PACE_ADJUSTMENT,
                title="Velocity decreasing",
                description="Learning pace has slowed recently",
                rationale=f"Recent velocity ({analytics.velocity_metrics.recent_velocity}) < overall ({analytics.velocity_metrics.overall_velocity})",
                suggested_action="Check for blockers, consider adjusting task difficulty",
                target_agent="learning-coordinator",
                expected_impact="Restore learning momentum"
            ))

        # Checkpoint-based recommendations
        if analytics.checkpoint_analysis.pass_rate < 100 and analytics.checkpoint_analysis.failed_checkpoints > 0:
            recommendations.append(LearningRecommendation(
                priority=RecommendationPriority.HIGH,
                recommendation_type=RecommendationType.CONCEPT_REVIEW,
                title="Review concepts before proceeding",
                description=f"{analytics.checkpoint_analysis.failed_checkpoints} checkpoint(s) failed",
                rationale="Failed checkpoints indicate gaps in understanding",
                suggested_action="Review phase concepts before moving to next phase",
                target_agent="learning-coordinator",
                expected_impact="Stronger foundation for advanced topics"
            ))

        # Positive reinforcement (LOW priority celebrations)
        if analytics.checkpoint_analysis.first_try_pass_rate == 100 and analytics.checkpoint_analysis.passed_checkpoints > 0:
            recommendations.append(LearningRecommendation(
                priority=RecommendationPriority.LOW,
                recommendation_type=RecommendationType.CELEBRATION,
                title="Celebrate checkpoint success!",
                description="Student passed all checkpoints on first try",
                rationale=f"{analytics.checkpoint_analysis.passed_checkpoints} checkpoints passed flawlessly",
                suggested_action="Acknowledge this achievement to boost confidence",
                target_agent="learning-coordinator",
                expected_impact="Increased motivation and confidence"
            ))

        # Sort by priority
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3
        }
        recommendations.sort(key=lambda r: priority_order[r.priority])

        return recommendations

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _analyze_velocity_trend(
        self,
        completed_tasks: List[Task],
        overall_velocity: float,
        recent_velocity: float
    ) -> str:
        """Determine velocity trend"""

        if len(completed_tasks) < 4:
            return "stable"  # Not enough data

        if recent_velocity > overall_velocity * 1.2:
            return "increasing"
        elif recent_velocity < overall_velocity * 0.8:
            return "decreasing"
        else:
            return "stable"

    def _detect_steady_progress_pattern(
        self,
        completed_tasks: List[Task]
    ) -> Optional[LearningPattern]:
        """Detect steady progress pattern"""

        if len(completed_tasks) < 3:
            return None

        # Calculate gaps between completions
        dates = []
        for task in completed_tasks:
            if task.completed_at:
                date = self._parse_date(task.completed_at)
                if date:
                    dates.append(date)

        if len(dates) < 3:
            return None

        dates.sort()
        gaps = [(dates[i+1] - dates[i]).days for i in range(len(dates) - 1)]

        if not gaps:
            return None

        std_dev = statistics.stdev(gaps) if len(gaps) > 1 else 0
        mean_gap = statistics.mean(gaps)

        # Determine if steady
        if std_dev < 3:
            confidence = 0.9
            description = f"Consistent task completion every {mean_gap:.1f} days"
        elif std_dev < 7:
            confidence = 0.7
            description = f"Fairly regular task completion (avg {mean_gap:.1f} days)"
        else:
            return None  # Not steady

        return LearningPattern(
            pattern_type=PatternType.STEADY_PROGRESS,
            confidence=confidence,
            description=description,
            evidence=[
                f"Standard deviation of completion gaps: {std_dev:.1f} days",
                f"Completed {len(completed_tasks)} tasks"
            ],
            recommendation="Maintain current pace and schedule",
            impact="positive"
        )

    def _detect_burst_progress_pattern(
        self,
        completed_tasks: List[Task]
    ) -> Optional[LearningPattern]:
        """Detect burst progress pattern"""

        if len(completed_tasks) < 5:
            return None

        # Look for clusters of tasks completed in short time
        dates = []
        for task in completed_tasks:
            if task.completed_at:
                date = self._parse_date(task.completed_at)
                if date:
                    dates.append(date)

        if len(dates) < 5:
            return None

        dates.sort()

        # Find bursts (3+ tasks in 3 days)
        bursts = 0
        for i in range(len(dates) - 2):
            window = dates[i+2] - dates[i]
            if window.days <= 3:
                bursts += 1

        if bursts >= 2:
            return LearningPattern(
                pattern_type=PatternType.BURST_PROGRESS,
                confidence=0.8,
                description=f"Rapid progress in bursts ({bursts} bursts detected)",
                evidence=[
                    f"Multiple instances of 3+ tasks in 3 days",
                    f"Total tasks: {len(completed_tasks)}"
                ],
                recommendation="Schedule regular focused work sessions to leverage this pattern",
                impact="positive"
            )

        return None

    def _determine_overall_health(self, analytics: LearningAnalytics) -> str:
        """Determine overall learning health"""

        # Count critical/high priority recommendations
        critical_issues = sum(
            1 for r in analytics.recommendations
            if r.priority in [RecommendationPriority.CRITICAL, RecommendationPriority.HIGH]
        )

        # Check struggle severity
        severe_struggles = sum(1 for s in analytics.struggle_areas if s.severity == "severe")

        # Check velocity
        on_track = analytics.velocity_metrics.on_track

        # Determine health
        if severe_struggles > 0 or critical_issues >= 2:
            return "struggling"
        elif critical_issues > 0 or not on_track:
            return "needs_attention"
        elif analytics.velocity_metrics.velocity_trend == "increasing":
            return "excellent"
        else:
            return "good"

    def _extract_key_insights(
        self,
        analytics: LearningAnalytics,
        plan: LearningPlan
    ) -> List[str]:
        """Extract key insights"""

        insights = []

        # Velocity insight
        insights.append(
            f"Maintaining {analytics.velocity_metrics.tasks_per_week} tasks per week on average"
        )

        # Checkpoint insight
        if analytics.checkpoint_analysis.passed_checkpoints > 0:
            if analytics.checkpoint_analysis.first_try_pass_rate == 100:
                insights.append("Strong conceptual understanding (100% checkpoint pass rate)")
            else:
                insights.append(
                    f"Checkpoint pass rate: {analytics.checkpoint_analysis.pass_rate}%"
                )

        # Struggle insight
        if analytics.struggle_areas:
            severe = sum(1 for s in analytics.struggle_areas if s.severity == "severe")
            if severe > 0:
                insights.append(f"Currently facing {severe} severe challenge(s)")
            else:
                insights.append("Some minor challenges being worked through")

        # Trend insight
        if analytics.velocity_metrics.on_track:
            insights.append("On track to complete plan by estimated date")
        else:
            insights.append("May need pace adjustment to meet target date")

        return insights[:5]  # Top 5

    def _identify_strengths(
        self,
        analytics: LearningAnalytics,
        plan: LearningPlan
    ) -> List[str]:
        """Identify student strengths"""

        strengths = []

        # Consistent work
        if any(p.pattern_type == PatternType.STEADY_PROGRESS for p in analytics.learning_patterns):
            strengths.append("Consistent work habits")

        # Strong understanding
        if analytics.checkpoint_analysis.first_try_pass_rate >= 80:
            strengths.append("Strong conceptual understanding")

        # Good velocity
        if analytics.velocity_metrics.tasks_per_week >= 2.0:
            strengths.append("Good learning pace")

        # Passing checkpoints
        if analytics.checkpoint_analysis.pass_rate == 100 and analytics.checkpoint_analysis.passed_checkpoints > 0:
            strengths.append("Excellent checkpoint performance")

        return strengths

    def _identify_growth_areas(
        self,
        analytics: LearningAnalytics,
        plan: LearningPlan
    ) -> List[str]:
        """Identify growth areas"""

        growth_areas = []

        # Struggles
        for struggle in analytics.struggle_areas:
            if struggle.severity in ["moderate", "severe"]:
                growth_areas.append(f"{struggle.task_title} (currently struggling)")

        # Failed checkpoints
        if analytics.checkpoint_analysis.failed_checkpoints > 0:
            growth_areas.append("Checkpoint preparation and understanding verification")

        # Velocity concerns
        if analytics.velocity_metrics.velocity_trend == "decreasing":
            growth_areas.append("Maintaining consistent learning pace")

        return growth_areas

    def _generate_struggle_recommendation(
        self,
        severity: str,
        duration: int,
        task_title: str
    ) -> str:
        """Generate recommendation for struggle"""

        if severity == "severe":
            return f"Immediate specialist consultation recommended - stuck for {duration} days"
        elif severity == "moderate":
            return f"Consider breaking task into smaller pieces or consulting specialist"
        else:
            return f"Monitor progress, consult specialist if stuck after {14 - duration} more days"

    def _suggest_specialist(self, task_title: str, plan_title: str) -> Optional[str]:
        """Suggest appropriate specialist based on task/plan context"""

        task_lower = task_title.lower()
        plan_lower = plan_title.lower()

        # Domain-specific specialists
        if any(word in task_lower or word in plan_lower for word in ["navigation", "path", "slam", "odometry"]):
            return "robotics-vision-navigator"
        elif any(word in task_lower or word in plan_lower for word in ["ros2", "node", "publisher", "subscriber"]):
            return "ros2-learning-mentor"
        elif any(word in task_lower or word in plan_lower for word in ["motor", "control", "hardware", "sensor"]):
            return "jetank-hardware-specialist"
        elif any(word in task_lower or word in plan_lower for word in ["test", "testing", "coverage"]):
            return "testing-specialist"
        elif any(word in task_lower or word in plan_lower for word in ["debug", "error", "bug"]):
            return "debugging-detective"
        elif any(word in task_lower or word in plan_lower for word in ["architecture", "design", "pattern"]):
            return "code-architecture-mentor"
        elif any(word in task_lower or word in plan_lower for word in ["python"]):
            return "python-best-practices"
        elif any(word in task_lower or word in plan_lower for word in ["c++"]):
            return "cpp-best-practices"
        else:
            return "learning-coordinator"

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime"""

        if not date_str:
            return None

        try:
            # Try ISO format first
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                # Try simple YYYY-MM-DD
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return None

    def _parse_time_estimate(self, time_str: Optional[str]) -> Optional[float]:
        """Parse time estimate string to weeks"""

        if not time_str:
            return None

        time_lower = time_str.lower()

        # Extract number
        import re
        numbers = re.findall(r'\d+', time_lower)
        if not numbers:
            return None

        num = float(numbers[0])

        # Convert to weeks
        if 'week' in time_lower:
            return num
        elif 'month' in time_lower:
            return num * 4
        elif 'day' in time_lower:
            return num / 7
        else:
            return num  # Assume weeks
