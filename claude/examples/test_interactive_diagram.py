"""
Test suite for interactive-diagram skill

Tests diagram generation functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.interactive_diagram import DiagramGenerator, DiagramType
from skills.learning_plan_manager import LearningPlanManager
from skills.learning_analytics import LearningAnalyzer

def print_header(title):
    print("\n" + "="*60)
    print(f"{title}")
    print("="*60)

def test_progress_chart():
    """Test progress chart generation"""
    print_header("Test 1: Progress Chart Generation")

    manager = LearningPlanManager()
    analyzer = LearningAnalyzer()
    generator = DiagramGenerator()

    plan = manager.find_latest_plan()
    if not plan:
        print("⚠️  No plans found")
        return False

    analytics = analyzer.analyze_plan(plan)
    diagram = generator.generate_progress_chart(analytics)

    print(f"✅ Generated progress chart")
    print(f"   Title: {diagram.title}")
    print(f"   Type: {diagram.diagram_type}")
    print(f"   Mermaid code length: {len(diagram.mermaid_code)} chars")

    assert diagram.diagram_type == DiagramType.PROGRESS_CHART
    assert len(diagram.mermaid_code) > 0
    assert "pie" in diagram.mermaid_code.lower()

    return True

def test_learning_journey():
    """Test learning journey generation"""
    print_header("Test 2: Learning Journey Generation")

    manager = LearningPlanManager()
    generator = DiagramGenerator()

    plan = manager.find_latest_plan()
    if not plan:
        print("⚠️  No plans found")
        return False

    diagram = generator.generate_learning_journey(plan)

    print(f"✅ Generated learning journey")
    print(f"   Title: {diagram.title}")
    print(f"   Type: {diagram.diagram_type}")
    print(f"   Phases: {diagram.metadata.get('phases_count', 0)}")

    assert diagram.diagram_type == DiagramType.LEARNING_JOURNEY
    assert "flowchart" in diagram.mermaid_code.lower()

    return True

def test_gantt_chart():
    """Test Gantt chart generation"""
    print_header("Test 3: Gantt Chart Generation")

    manager = LearningPlanManager()
    generator = DiagramGenerator()

    plan = manager.find_latest_plan()
    if not plan:
        print("⚠️  No plans found")
        return False

    diagram = generator.generate_gantt_chart(plan)

    print(f"✅ Generated Gantt chart")
    print(f"   Title: {diagram.title}")
    print(f"   Type: {diagram.diagram_type}")

    assert diagram.diagram_type == DiagramType.GANTT_CHART
    assert "gantt" in diagram.mermaid_code.lower()

    return True

def test_markdown_export():
    """Test markdown export"""
    print_header("Test 4: Markdown Export")

    manager = LearningPlanManager()
    generator = DiagramGenerator()

    plan = manager.find_latest_plan()
    if not plan:
        print("⚠️  No plans found")
        return False

    diagram = generator.generate_learning_journey(plan)
    markdown = diagram.to_markdown()

    print(f"✅ Exported to markdown")
    print(f"   Length: {len(markdown)} chars")

    assert "##" in markdown
    assert "```mermaid" in markdown
    assert diagram.title in markdown

    return True

def test_html_export():
    """Test HTML export"""
    print_header("Test 5: HTML Export")

    manager = LearningPlanManager()
    generator = DiagramGenerator()

    plan = manager.find_latest_plan()
    if not plan:
        print("⚠️  No plans found")
        return False

    diagram = generator.generate_learning_journey(plan)
    html = diagram.to_html()

    print(f"✅ Exported to HTML")
    print(f"   Length: {len(html)} chars")

    assert "<h2>" in html
    assert 'class="mermaid"' in html

    return True

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Interactive Diagram - Test Suite")
    print("="*60)

    tests = [
        ("Progress Chart", test_progress_chart),
        ("Learning Journey", test_learning_journey),
        ("Gantt Chart", test_gantt_chart),
        ("Markdown Export", test_markdown_export),
        ("HTML Export", test_html_export),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    if passed == total:
        print(f"\n✅ All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
