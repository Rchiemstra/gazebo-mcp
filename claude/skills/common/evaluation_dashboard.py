"""
Performance Dashboard for Agent Evaluation.

Generates visual dashboard showing:
- Agent performance metrics
- Success rates over time
- Quality trends
- Improvement tracking

Part of Phase 3: Polish & Optimization
"""

from skills.common.agent_evaluation import (
    AgentEvaluator,
    create_evaluator_with_default_queries
)
from typing import Dict, Any


def generate_markdown_dashboard(evaluator: AgentEvaluator) -> str:
    """
    Generate Markdown dashboard from evaluation data.

    Args:
        evaluator: AgentEvaluator instance

    Returns:
        Markdown-formatted dashboard
    """
    dashboard_data = evaluator.generate_dashboard_data()

    md = []
    md.append("# Agent Performance Dashboard\n")
    md.append(f"**Generated:** {dashboard_data['generated_at']}\n")
    md.append("---\n")

    # Overall stats
    md.append("## Overall Statistics\n")
    md.append(f"- **Total Test Queries:** {dashboard_data['overall']['total_queries']}")
    md.append(f"- **Total Evaluations:** {dashboard_data['overall']['total_evaluations']}")
    md.append(f"- **Agent Types:** {dashboard_data['overall']['agent_types']}\n")

    # Per-agent metrics
    md.append("## Agent Performance\n")

    for agent_type, metrics in dashboard_data['agents'].items():
        md.append(f"### {agent_type}\n")

        if metrics['total_queries'] == 0:
            md.append("*No evaluations yet*\n")
            continue

        md.append(f"- **Total Queries:** {metrics['total_queries']}")
        md.append(f"- **Success Rate:** {metrics['success_rate']:.1%}")
        md.append(f"- **Average Score:** {metrics['average_score']:.2f}/1.0")
        md.append(f"- **Avg Response Time:** {metrics['average_response_time']:.1f}s\n")

        # By difficulty
        if metrics['by_difficulty']:
            md.append("**Performance by Difficulty:**\n")
            for diff, stats in metrics['by_difficulty'].items():
                success_rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
                md.append(f"- {diff.capitalize()}: {stats['success']}/{stats['total']} ({success_rate:.1%})")
            md.append("")

        # Trend
        if metrics['trend']:
            md.append("**Recent Trend:**\n")
            md.append("| Week | Queries | Success Rate | Avg Score |")
            md.append("|------|---------|--------------|-----------|")
            for week_data in metrics['trend'][-4:]:  # Last 4 weeks
                md.append(
                    f"| {week_data['week']} | "
                    f"{week_data['total']} | "
                    f"{week_data['success_rate']:.1%} | "
                    f"{week_data['average_score']:.2f} |"
                )
            md.append("")

    md.append("---\n")
    md.append("*Dashboard updates automatically as evaluations are recorded.*\n")

    return "\n".join(md)


def generate_text_dashboard(evaluator: AgentEvaluator) -> str:
    """
    Generate text-based dashboard for terminal display.

    Args:
        evaluator: AgentEvaluator instance

    Returns:
        Text-formatted dashboard
    """
    dashboard_data = evaluator.generate_dashboard_data()

    lines = []
    lines.append("=" * 70)
    lines.append("AGENT PERFORMANCE DASHBOARD".center(70))
    lines.append("=" * 70)
    lines.append(f"Generated: {dashboard_data['generated_at']}")
    lines.append("")

    # Overall
    lines.append("OVERALL STATISTICS")
    lines.append("-" * 70)
    lines.append(f"Total Test Queries:  {dashboard_data['overall']['total_queries']:>5}")
    lines.append(f"Total Evaluations:   {dashboard_data['overall']['total_evaluations']:>5}")
    lines.append(f"Agent Types:         {dashboard_data['overall']['agent_types']:>5}")
    lines.append("")

    # Per-agent
    for agent_type, metrics in dashboard_data['agents'].items():
        lines.append(f"AGENT: {agent_type}")
        lines.append("-" * 70)

        if metrics['total_queries'] == 0:
            lines.append("  No evaluations yet")
            lines.append("")
            continue

        lines.append(f"  Total Queries:       {metrics['total_queries']:>6}")
        lines.append(f"  Success Rate:        {metrics['success_rate']:>6.1%}")
        lines.append(f"  Average Score:       {metrics['average_score']:>6.2f}/1.0")
        lines.append(f"  Avg Response Time:   {metrics['average_response_time']:>6.1f}s")

        # Progress bar for success rate
        bar_length = 40
        filled = int(metrics['success_rate'] * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        lines.append(f"  Progress: [{bar}] {metrics['success_rate']:.1%}")

        lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def print_dashboard(evaluator: AgentEvaluator):
    """Print text dashboard to console."""
    dashboard = generate_text_dashboard(evaluator)
    print(dashboard)


def save_markdown_dashboard(evaluator: AgentEvaluator, path: str = "DASHBOARD.md"):
    """
    Save Markdown dashboard to file.

    Args:
        evaluator: AgentEvaluator instance
        path: Path to save dashboard
    """
    dashboard = generate_markdown_dashboard(evaluator)

    with open(path, 'w') as f:
        f.write(dashboard)

    print(f"Dashboard saved to {path}")


def main():
    """Demo dashboard generation."""
    print("Creating evaluation framework with default test queries...")
    evaluator = create_evaluator_with_default_queries()

    print(f"Loaded {len(evaluator.test_queries)} test queries")
    print("")

    # Add some sample evaluations for demo
    print("Adding sample evaluations...")
    evaluator.evaluate_agent_manually(
        query_id="code_review_1",
        success=True,
        score=0.92,
        response_time=120.5,
        token_usage=15000,
        capabilities_demonstrated=["security_analysis", "parallel_workers"],
        notes="Excellent security analysis with parallel workers"
    )

    evaluator.evaluate_agent_manually(
        query_id="code_review_2",
        success=True,
        score=0.88,
        response_time=95.3,
        token_usage=12000,
        capabilities_demonstrated=["test_coverage", "documentation"],
        notes="Good coverage analysis"
    )

    evaluator.evaluate_agent_manually(
        query_id="architecture_1",
        success=True,
        score=0.95,
        response_time=45.2,
        token_usage=5000,
        capabilities_demonstrated=["design_thinking", "teaching"],
        notes="Excellent teaching approach, no complete solutions given"
    )

    print("")

    # Display dashboard
    print_dashboard(evaluator)

    # Save Markdown
    save_markdown_dashboard(evaluator)


if __name__ == "__main__":
    main()
