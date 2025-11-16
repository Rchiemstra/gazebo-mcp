"""
Trend Analyzer

Time-series analysis for skill performance trends.
"""

import statistics
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from skills.skill_evaluator.core.models import HealthTrend
from skills.skill_evaluator.core.history_tracker import ExecutionHistoryTracker


class TrendAnalyzer:
    """
    Analyzes performance trends over time.

    Provides time-series analysis, forecasting, and anomaly detection.
    """

    def __init__(self, history_tracker: ExecutionHistoryTracker):
        """
        Initialize the trend analyzer.

        Args:
            history_tracker: ExecutionHistoryTracker for accessing execution data
        """
        self.history_tracker = history_tracker

    def analyze_trends(
        self,
        skill_name: str,
        time_period_days: int = 30,
        bucket_size_hours: int = 24,
        operation: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze performance trends over time.

        Args:
            skill_name: Name of the skill
            time_period_days: Days to analyze
            bucket_size_hours: Size of time buckets for aggregation
            operation: Specific operation to analyze

        Returns:
            Trend analysis results
        """
        # Get all executions for the period
        since = (datetime.now() - timedelta(days=time_period_days)).timestamp()
        records = self.history_tracker.get_recent_executions(
            skill_name,
            limit=10000,
            since=since
        )

        if operation:
            records = [r for r in records if r.operation == operation]

        if len(records) < 10:
            return {
                'has_data': False,
                'error': 'Insufficient data for trend analysis',
                'recommendation': f'Need at least 10 executions in the last {time_period_days} days'
            }

        # Create time buckets
        buckets = self._create_time_buckets(
            records,
            bucket_size_hours=bucket_size_hours
        )

        # Analyze each metric trend
        duration_trend = self._analyze_metric_trend(
            buckets,
            metric='avg_duration'
        )

        error_rate_trend = self._analyze_metric_trend(
            buckets,
            metric='error_rate'
        )

        throughput_trend = self._analyze_metric_trend(
            buckets,
            metric='count'
        )

        # Detect anomalies
        anomalies = self._detect_anomalies(buckets)

        # Calculate overall trend
        overall_trend = self._calculate_overall_trend(
            duration_trend,
            error_rate_trend,
            throughput_trend
        )

        # Generate forecast (simple linear projection)
        forecast = self._generate_forecast(
            buckets,
            periods_ahead=3
        )

        return {
            'has_data': True,
            'skill_name': skill_name,
            'operation': operation,
            'time_period_days': time_period_days,
            'bucket_size_hours': bucket_size_hours,
            'total_buckets': len(buckets),
            'total_executions': sum(b['count'] for b in buckets),
            'overall_trend': overall_trend,
            'duration_trend': duration_trend,
            'error_rate_trend': error_rate_trend,
            'throughput_trend': throughput_trend,
            'anomalies': anomalies,
            'forecast': forecast,
            'time_series': buckets
        }

    def _create_time_buckets(
        self,
        records: List,
        bucket_size_hours: int
    ) -> List[Dict[str, Any]]:
        """Create time buckets and aggregate metrics."""
        if not records:
            return []

        # Determine time range
        timestamps = [r.timestamp for r in records]
        min_time = min(timestamps)
        max_time = max(timestamps)

        # Create buckets
        bucket_size_seconds = bucket_size_hours * 3600
        buckets = []

        current_time = min_time
        while current_time <= max_time:
            bucket_end = current_time + bucket_size_seconds

            # Get records in this bucket
            bucket_records = [
                r for r in records
                if current_time <= r.timestamp < bucket_end
            ]

            if bucket_records:
                successful = [r for r in bucket_records if r.success]
                failed = [r for r in bucket_records if not r.success]

                durations = [r.duration for r in successful]

                buckets.append({
                    'timestamp': current_time,
                    'datetime': datetime.fromtimestamp(current_time).isoformat(),
                    'count': len(bucket_records),
                    'successful': len(successful),
                    'failed': len(failed),
                    'error_rate': len(failed) / len(bucket_records) * 100 if bucket_records else 0,
                    'avg_duration': statistics.mean(durations) if durations else 0,
                    'min_duration': min(durations) if durations else 0,
                    'max_duration': max(durations) if durations else 0,
                    'median_duration': statistics.median(durations) if durations else 0
                })

            current_time = bucket_end

        return buckets

    def _analyze_metric_trend(
        self,
        buckets: List[Dict[str, Any]],
        metric: str
    ) -> Dict[str, Any]:
        """Analyze trend for a specific metric."""
        if not buckets:
            return {'trend': HealthTrend.UNKNOWN.value}

        values = [b[metric] for b in buckets]

        # Calculate linear regression (simple slope calculation)
        n = len(values)
        if n < 3:
            return {
                'trend': HealthTrend.UNKNOWN.value,
                'reason': 'Insufficient data points'
            }

        # Simple linear regression: y = mx + b
        x = list(range(n))
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(values)

        numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0

        # Calculate R-squared for trend strength
        if denominator != 0:
            predictions = [slope * xi + (mean_y - slope * mean_x) for xi in x]
            ss_res = sum((values[i] - predictions[i]) ** 2 for i in range(n))
            ss_tot = sum((values[i] - mean_y) ** 2 for i in range(n))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        else:
            r_squared = 0

        # Determine trend direction and strength
        # For duration and error_rate: negative slope is good
        # For throughput (count): positive slope is good
        threshold = mean_y * 0.01 if mean_y > 0 else 0.01  # 1% of mean

        if metric in ['avg_duration', 'error_rate']:
            if slope < -threshold:
                trend_direction = HealthTrend.IMPROVING.value
            elif slope > threshold:
                trend_direction = HealthTrend.DECLINING.value
            else:
                trend_direction = HealthTrend.STABLE.value
        else:  # count/throughput
            if slope > threshold:
                trend_direction = HealthTrend.IMPROVING.value
            elif slope < -threshold:
                trend_direction = HealthTrend.DECLINING.value
            else:
                trend_direction = HealthTrend.STABLE.value

        # Calculate percentage change
        if values[0] != 0:
            percent_change = ((values[-1] - values[0]) / values[0]) * 100
        else:
            percent_change = 0

        return {
            'trend': trend_direction,
            'slope': slope,
            'r_squared': r_squared,
            'trend_strength': 'strong' if abs(r_squared) > 0.7 else 'moderate' if abs(r_squared) > 0.4 else 'weak',
            'percent_change': percent_change,
            'start_value': values[0],
            'end_value': values[-1],
            'mean_value': mean_y,
            'min_value': min(values),
            'max_value': max(values)
        }

    def _detect_anomalies(
        self,
        buckets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect anomalous time periods."""
        if len(buckets) < 5:
            return []

        anomalies = []

        # Analyze duration anomalies
        durations = [b['avg_duration'] for b in buckets if b['avg_duration'] > 0]
        if durations:
            mean_duration = statistics.mean(durations)
            stdev_duration = statistics.stdev(durations) if len(durations) > 1 else 0

            for bucket in buckets:
                if bucket['avg_duration'] > 0:
                    z_score = (bucket['avg_duration'] - mean_duration) / stdev_duration if stdev_duration > 0 else 0

                    if abs(z_score) > 2:  # More than 2 standard deviations
                        anomalies.append({
                            'timestamp': bucket['timestamp'],
                            'datetime': bucket['datetime'],
                            'type': 'duration_anomaly',
                            'severity': 'high' if abs(z_score) > 3 else 'medium',
                            'description': f'Unusual duration: {bucket["avg_duration"]:.2f}s (z-score: {z_score:.2f})',
                            'value': bucket['avg_duration'],
                            'expected_range': f'{mean_duration - 2*stdev_duration:.2f}s - {mean_duration + 2*stdev_duration:.2f}s'
                        })

        # Analyze error rate anomalies
        error_rates = [b['error_rate'] for b in buckets]
        mean_error_rate = statistics.mean(error_rates)
        stdev_error_rate = statistics.stdev(error_rates) if len(error_rates) > 1 else 0

        for bucket in buckets:
            z_score = (bucket['error_rate'] - mean_error_rate) / stdev_error_rate if stdev_error_rate > 0 else 0

            if z_score > 2 and bucket['error_rate'] > 20:  # High error rate spike
                anomalies.append({
                    'timestamp': bucket['timestamp'],
                    'datetime': bucket['datetime'],
                    'type': 'error_rate_spike',
                    'severity': 'critical' if bucket['error_rate'] > 50 else 'high',
                    'description': f'Error rate spike: {bucket["error_rate"]:.1f}%',
                    'value': bucket['error_rate'],
                    'expected_range': f'0% - {mean_error_rate + 2*stdev_error_rate:.1f}%'
                })

        # Analyze throughput anomalies
        counts = [b['count'] for b in buckets]
        mean_count = statistics.mean(counts)
        stdev_count = statistics.stdev(counts) if len(counts) > 1 else 0

        for bucket in buckets:
            if bucket['count'] > 0:
                z_score = (bucket['count'] - mean_count) / stdev_count if stdev_count > 0 else 0

                if z_score < -2:  # Unusually low throughput
                    anomalies.append({
                        'timestamp': bucket['timestamp'],
                        'datetime': bucket['datetime'],
                        'type': 'low_throughput',
                        'severity': 'medium',
                        'description': f'Low execution count: {bucket["count"]} (expected ~{mean_count:.0f})',
                        'value': bucket['count'],
                        'expected_range': f'{max(0, mean_count - 2*stdev_count):.0f} - {mean_count + 2*stdev_count:.0f}'
                    })

        return sorted(anomalies, key=lambda x: x['timestamp'], reverse=True)

    def _calculate_overall_trend(
        self,
        duration_trend: Dict[str, Any],
        error_rate_trend: Dict[str, Any],
        throughput_trend: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall trend from individual metrics."""
        # Weighted scoring: duration and error rate are most important
        trend_scores = {
            HealthTrend.IMPROVING.value: 1,
            HealthTrend.STABLE.value: 0,
            HealthTrend.DECLINING.value: -1,
            HealthTrend.UNKNOWN.value: 0
        }

        duration_score = trend_scores.get(duration_trend.get('trend'), 0) * 0.4
        error_rate_score = trend_scores.get(error_rate_trend.get('trend'), 0) * 0.4
        throughput_score = trend_scores.get(throughput_trend.get('trend'), 0) * 0.2

        overall_score = duration_score + error_rate_score + throughput_score

        if overall_score > 0.3:
            overall_trend = HealthTrend.IMPROVING.value
        elif overall_score < -0.3:
            overall_trend = HealthTrend.DECLINING.value
        else:
            overall_trend = HealthTrend.STABLE.value

        # Determine confidence based on trend strength
        r_squared_values = [
            duration_trend.get('r_squared', 0),
            error_rate_trend.get('r_squared', 0),
            throughput_trend.get('r_squared', 0)
        ]
        avg_r_squared = statistics.mean([abs(r) for r in r_squared_values])

        return {
            'trend': overall_trend,
            'confidence': avg_r_squared,
            'confidence_level': 'high' if avg_r_squared > 0.7 else 'medium' if avg_r_squared > 0.4 else 'low',
            'contributing_factors': {
                'duration': duration_trend.get('trend'),
                'error_rate': error_rate_trend.get('trend'),
                'throughput': throughput_trend.get('trend')
            }
        }

    def _generate_forecast(
        self,
        buckets: List[Dict[str, Any]],
        periods_ahead: int = 3
    ) -> Dict[str, Any]:
        """Generate simple forecast for next periods."""
        if len(buckets) < 3:
            return {'available': False, 'reason': 'Insufficient historical data'}

        # Use simple linear regression for forecast
        durations = [b['avg_duration'] for b in buckets if b['avg_duration'] > 0]
        error_rates = [b['error_rate'] for b in buckets]

        if not durations:
            return {'available': False, 'reason': 'No successful executions'}

        n = len(durations)
        x = list(range(n))

        # Forecast duration
        mean_x = statistics.mean(x)
        mean_duration = statistics.mean(durations)

        numerator = sum((x[i] - mean_x) * (durations[i] - mean_duration) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        slope_duration = numerator / denominator if denominator != 0 else 0
        intercept_duration = mean_duration - slope_duration * mean_x

        # Forecast error rate
        mean_error_rate = statistics.mean(error_rates)
        numerator_er = sum((x[i] - mean_x) * (error_rates[i] - mean_error_rate) for i in range(n))
        slope_error_rate = numerator_er / denominator if denominator != 0 else 0
        intercept_error_rate = mean_error_rate - slope_error_rate * mean_x

        # Generate forecasts
        forecasts = []
        for i in range(1, periods_ahead + 1):
            future_x = n + i
            predicted_duration = slope_duration * future_x + intercept_duration
            predicted_error_rate = max(0, min(100, slope_error_rate * future_x + intercept_error_rate))

            forecasts.append({
                'period': i,
                'predicted_duration': max(0, predicted_duration),
                'predicted_error_rate': predicted_error_rate
            })

        return {
            'available': True,
            'forecasts': forecasts,
            'method': 'linear_regression',
            'note': 'Forecast based on simple linear trend - actual values may vary'
        }

    def detect_patterns(
        self,
        skill_name: str,
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Detect recurring patterns in execution behavior.

        Args:
            skill_name: Name of the skill
            time_period_days: Days to analyze

        Returns:
            Detected patterns
        """
        since = (datetime.now() - timedelta(days=time_period_days)).timestamp()
        records = self.history_tracker.get_recent_executions(
            skill_name,
            limit=10000,
            since=since
        )

        if len(records) < 20:
            return {
                'has_data': False,
                'error': 'Insufficient data for pattern detection'
            }

        patterns = []

        # Pattern 1: Time-of-day patterns
        hour_stats = defaultdict(list)
        for record in records:
            if record.success:
                hour = datetime.fromtimestamp(record.timestamp).hour
                hour_stats[hour].append(record.duration)

        if len(hour_stats) >= 8:  # Need data for at least 8 different hours
            hour_averages = {
                hour: statistics.mean(durations)
                for hour, durations in hour_stats.items()
                if len(durations) >= 3
            }

            if hour_averages:
                overall_avg = statistics.mean(hour_averages.values())
                slow_hours = [
                    (hour, avg) for hour, avg in hour_averages.items()
                    if avg > overall_avg * 1.3
                ]

                if slow_hours:
                    patterns.append({
                        'type': 'time_of_day',
                        'description': f'Slower performance during specific hours',
                        'details': {
                            'slow_hours': [f'{h:02d}:00 ({avg:.2f}s)' for h, avg in sorted(slow_hours)],
                            'overall_average': overall_avg
                        },
                        'recommendation': 'Consider scaling resources during peak hours'
                    })

        # Pattern 2: Day-of-week patterns
        dow_stats = defaultdict(list)
        for record in records:
            if record.success:
                dow = datetime.fromtimestamp(record.timestamp).weekday()
                dow_stats[dow].append(record.duration)

        dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_averages = {
            dow: statistics.mean(durations)
            for dow, durations in dow_stats.items()
            if len(durations) >= 3
        }

        if len(dow_averages) >= 5:
            overall_avg = statistics.mean(dow_averages.values())
            slow_days = [
                (dow, avg) for dow, avg in dow_averages.items()
                if avg > overall_avg * 1.2
            ]

            if slow_days:
                patterns.append({
                    'type': 'day_of_week',
                    'description': 'Performance varies by day of week',
                    'details': {
                        'slow_days': [f'{dow_names[dow]} ({avg:.2f}s)' for dow, avg in sorted(slow_days)],
                        'overall_average': overall_avg
                    },
                    'recommendation': 'Investigate load patterns and resource availability'
                })

        # Pattern 3: Error clustering
        failed_records = [r for r in records if not r.success]
        if len(failed_records) >= 5:
            # Check if errors are clustered in time
            failed_timestamps = sorted([r.timestamp for r in failed_records])
            time_gaps = [
                failed_timestamps[i+1] - failed_timestamps[i]
                for i in range(len(failed_timestamps) - 1)
            ]

            if time_gaps:
                median_gap = statistics.median(time_gaps)
                # If errors occur in bursts (median gap < 1 hour)
                if median_gap < 3600:
                    patterns.append({
                        'type': 'error_clustering',
                        'description': 'Errors occur in temporal clusters',
                        'details': {
                            'total_errors': len(failed_records),
                            'median_gap_minutes': median_gap / 60
                        },
                        'recommendation': 'Investigate cascading failures or dependency issues'
                    })

        return {
            'has_data': True,
            'skill_name': skill_name,
            'time_period_days': time_period_days,
            'patterns_found': len(patterns),
            'patterns': patterns
        }
