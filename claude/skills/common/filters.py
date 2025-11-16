"""
Common filtering utilities for all skills.
Enables local data filtering before results reach the model.

This is a key component of MCP code execution efficiency, allowing agents to:
1. Generate code that calls skills
2. Filter results locally (in execution environment)
3. Return only relevant data to the model

Expected token savings: 95-99% for large datasets
"""

from typing import List, Dict, Any, Callable, Optional


class ResultFilter:
    """
    Efficient filtering operations for skill results.

    Usage:
        from skills.common.filters import ResultFilter

        # Limit results
        files = analyze_codebase("src/")  # 10,000 files
        top_5 = ResultFilter.limit(files, 5)  # Only 5 files to model

        # Filter by field
        tests = generate_tests()
        failed = ResultFilter.filter_by_field(tests, "status", "failed")

        # Summarize instead of full data
        history = get_learning_history()  # 6 months, 30,000 tokens
        summary = ResultFilter.summarize(history)  # 100 tokens
    """

    @staticmethod
    def limit(results: List[Any], n: int) -> List[Any]:
        """
        Return first n results.

        Example:
            files = analyze_codebase("src/")  # 10,000 files
            top_5 = ResultFilter.limit(files, 5)  # Only 5 files

        Args:
            results: List of results
            n: Number of results to return

        Returns:
            First n results
        """
        return results[:n] if results else []

    @staticmethod
    def filter_by_field(
        results: List[Dict],
        field: str,
        value: Any
    ) -> List[Dict]:
        """
        Filter results where field equals value.

        Example:
            tests = generate_tests()  # All tests
            failed = ResultFilter.filter_by_field(tests, "status", "failed")

        Args:
            results: List of dict results
            field: Field name to check
            value: Value to match

        Returns:
            Filtered results
        """
        return [r for r in results if r.get(field) == value]

    @staticmethod
    def filter_by_predicate(
        results: List[Any],
        predicate: Callable[[Any], bool]
    ) -> List[Any]:
        """
        Filter results using custom predicate.

        Example:
            files = analyze_codebase("src/")
            complex = ResultFilter.filter_by_predicate(
                files,
                lambda f: f.complexity > 10
            )

        Args:
            results: List of results
            predicate: Function that returns True to keep item

        Returns:
            Filtered results
        """
        return [r for r in results if predicate(r)]

    @staticmethod
    def summarize(results: List[Any], sample_size: int = 3) -> Dict[str, Any]:
        """
        Return summary instead of full dataset.

        This is extremely efficient for large datasets!

        Example:
            history = get_learning_history()  # 6 months, 30,000 tokens
            summary = ResultFilter.summarize(history)  # 100 tokens
            # Returns: {"total_count": 1000, "sample": [...], "has_more": True}

        Args:
            results: List of results
            sample_size: Number of sample items to include

        Returns:
            Summary dict with count and sample
        """
        return {
            "total_count": len(results),
            "sample": results[:sample_size] if results else [],
            "has_more": len(results) > sample_size
        }

    @staticmethod
    def top_n_by_field(
        results: List[Dict],
        field: str,
        n: int,
        reverse: bool = True
    ) -> List[Dict]:
        """
        Return top n results sorted by field.

        Example:
            files = analyze_codebase("src/")
            most_complex = ResultFilter.top_n_by_field(
                files, "complexity", 5
            )

        Args:
            results: List of dict results
            field: Field name to sort by
            n: Number of results to return
            reverse: If True, sort descending (highest first)

        Returns:
            Top n results
        """
        sorted_results = sorted(
            results,
            key=lambda x: x.get(field, 0),
            reverse=reverse
        )
        return sorted_results[:n]

    @staticmethod
    def group_by(
        results: List[Dict],
        field: str
    ) -> Dict[Any, List[Dict]]:
        """
        Group results by field value.

        Example:
            tests = generate_tests()
            by_status = ResultFilter.group_by(tests, "status")
            # Returns: {"passed": [...], "failed": [...]}

        Args:
            results: List of dict results
            field: Field name to group by

        Returns:
            Dict mapping field value to list of results
        """
        groups = {}
        for result in results:
            key = result.get(field)
            if key not in groups:
                groups[key] = []
            groups[key].append(result)
        return groups

    @staticmethod
    def extract_fields(
        results: List[Dict],
        fields: List[str]
    ) -> List[Dict]:
        """
        Extract only specified fields from results.

        Reduces token usage by removing unnecessary fields.

        Example:
            files = analyze_codebase("src/")  # Full file objects
            names_only = ResultFilter.extract_fields(files, ["path", "name"])

        Args:
            results: List of dict results
            fields: List of field names to extract

        Returns:
            Results with only specified fields
        """
        return [
            {field: r.get(field) for field in fields}
            for r in results
        ]

    @staticmethod
    def search(
        results: List[Dict],
        query: str,
        fields: List[str]
    ) -> List[Dict]:
        """
        Search results where any field contains query.

        Example:
            files = analyze_codebase("src/")
            navigation_files = ResultFilter.search(
                files, "navigation", ["path", "name"]
            )

        Args:
            results: List of dict results
            query: Search query string
            fields: List of field names to search in

        Returns:
            Matching results
        """
        query = query.lower()
        return [
            r for r in results
            if any(
                query in str(r.get(field, "")).lower()
                for field in fields
            )
        ]

    @staticmethod
    def paginate(
        results: List[Any],
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Paginate results.

        Example:
            files = analyze_codebase("src/")  # 10,000 files
            page_1 = ResultFilter.paginate(files, page=1, page_size=20)
            # Returns: {"items": [...], "page": 1, "total_pages": 500, ...}

        Args:
            results: List of results
            page: Page number (1-indexed)
            page_size: Items per page

        Returns:
            Paginated results with metadata
        """
        total = len(results)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "items": results[start:end],
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }

    @staticmethod
    def deduplicate(
        results: List[Dict],
        key_field: str
    ) -> List[Dict]:
        """
        Remove duplicates based on key field.

        Example:
            files = find_all_references("NavController")
            unique = ResultFilter.deduplicate(files, "path")

        Args:
            results: List of dict results
            key_field: Field to use for uniqueness check

        Returns:
            Deduplicated results
        """
        seen = set()
        unique = []
        for result in results:
            key = result.get(key_field)
            if key not in seen:
                seen.add(key)
                unique.append(result)
        return unique

    @staticmethod
    def filter_by_threshold(
        results: List[Dict],
        field: str,
        threshold: float,
        comparator: str = ">"
    ) -> List[Dict]:
        """
        Filter results by numeric threshold.

        Example:
            files = analyze_codebase("src/")
            high_complexity = ResultFilter.filter_by_threshold(
                files, "complexity", 10, ">"
            )

        Args:
            results: List of dict results
            field: Numeric field to check
            threshold: Threshold value
            comparator: Comparison operator (>, <, >=, <=, ==)

        Returns:
            Filtered results
        """
        comparators = {
            ">": lambda x, t: x > t,
            "<": lambda x, t: x < t,
            ">=": lambda x, t: x >= t,
            "<=": lambda x, t: x <= t,
            "==": lambda x, t: x == t
        }

        comp_func = comparators.get(comparator)
        if not comp_func:
            raise ValueError(f"Invalid comparator: {comparator}")

        return [
            r for r in results
            if comp_func(r.get(field, 0), threshold)
        ]

    @staticmethod
    def aggregate(
        results: List[Dict],
        group_by_field: str,
        agg_field: str,
        operation: str = "sum"
    ) -> Dict[Any, float]:
        """
        Aggregate numeric values grouped by field.

        Example:
            tests = run_all_tests()
            duration_by_suite = ResultFilter.aggregate(
                tests, "suite", "duration", "sum"
            )

        Args:
            results: List of dict results
            group_by_field: Field to group by
            agg_field: Numeric field to aggregate
            operation: Aggregation operation (sum, avg, min, max, count)

        Returns:
            Dict mapping group key to aggregated value
        """
        from statistics import mean

        operations = {
            "sum": sum,
            "avg": mean,
            "min": min,
            "max": max,
            "count": len
        }

        agg_func = operations.get(operation)
        if not agg_func:
            raise ValueError(f"Invalid operation: {operation}")

        # Group results
        groups = ResultFilter.group_by(results, group_by_field)

        # Aggregate each group
        aggregated = {}
        for key, group in groups.items():
            if operation == "count":
                aggregated[key] = len(group)
            else:
                values = [r.get(agg_field, 0) for r in group]
                aggregated[key] = agg_func(values) if values else 0

        return aggregated


class TokenEstimator:
    """
    Estimate token counts for results.

    Useful for measuring efficiency gains.
    """

    @staticmethod
    def estimate_tokens(data: Any) -> int:
        """
        Estimate token count for data.

        Rough estimate: 1 token ≈ 4 characters

        Args:
            data: Any data structure

        Returns:
            Estimated token count
        """
        import json

        try:
            if isinstance(data, (dict, list)):
                data_str = json.dumps(data)
            else:
                data_str = str(data)

            # Rough estimate: 1 token ≈ 4 characters
            return len(data_str) // 4

        except:
            return 0

    @staticmethod
    def compare_efficiency(
        unfiltered: Any,
        filtered: Any
    ) -> Dict[str, Any]:
        """
        Compare token efficiency of filtered vs unfiltered results.

        Args:
            unfiltered: Original results
            filtered: Filtered results

        Returns:
            Efficiency comparison dict
        """
        unfiltered_tokens = TokenEstimator.estimate_tokens(unfiltered)
        filtered_tokens = TokenEstimator.estimate_tokens(filtered)
        tokens_saved = unfiltered_tokens - filtered_tokens
        savings_percent = (tokens_saved / unfiltered_tokens * 100) if unfiltered_tokens > 0 else 0

        return {
            "tokens_without_filtering": unfiltered_tokens,
            "tokens_with_filtering": filtered_tokens,
            "tokens_saved": tokens_saved,
            "savings_percent": round(savings_percent, 2),
            "efficiency_gain": f"{savings_percent:.1f}% reduction"
        }
