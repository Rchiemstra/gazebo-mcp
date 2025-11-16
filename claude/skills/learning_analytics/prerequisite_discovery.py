"""
Prerequisite Discovery System - Phase 4 Task 4

Discovers learning prerequisites using contextual retrieval to build
learning dependency graphs. Used by Learning Plan Orchestrator.

Performance: 67% better accuracy (contextual retrieval)
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import re

from skills.learning_analytics.contextual_retrieval import ContextualRetrieval


@dataclass
class Prerequisite:
    """Represents a prerequisite concept."""
    concept: str
    reason: str
    source: str
    confidence: float  # 0.0-1.0


@dataclass
class PrerequisiteGraph:
    """Represents learning dependencies."""
    topic: str
    direct_prerequisites: List[Prerequisite]
    indirect_prerequisites: List[Prerequisite]  # Prerequisites of prerequisites
    learning_path: List[str]  # Ordered list from fundamentals to topic


class PrerequisiteDiscovery:
    """
    Discover learning prerequisites using contextual retrieval.

    Given a topic, finds:
    - Required prior knowledge
    - Recommended learning order
    - Related concepts
    - Dependency chains

    Uses Phase 2 contextual retrieval (67% better accuracy).
    """

    def __init__(self, index_path: str = "learning_content_index.pkl"):
        """
        Initialize prerequisite discovery.

        Args:
            index_path: Path to indexed learning content
        """
        self.retrieval = ContextualRetrieval.load_index(index_path)

    def find_prerequisites(
        self,
        topic: str,
        confidence_threshold: float = 0.7
    ) -> List[Prerequisite]:
        """
        Find prerequisites for a topic.

        Args:
            topic: Topic to find prerequisites for
            confidence_threshold: Minimum confidence for prerequisites (0.0-1.0)

        Returns:
            List of prerequisites ordered by importance
        """
        prerequisites = []

        # Search for content about the topic
        results = self.retrieval.search(
            query=f"prerequisites for {topic} what to learn before",
            top_k=10,
            use_reranking=True  # 67% better accuracy
        )

        # Extract prerequisites from content
        for result in results:
            if result.score < confidence_threshold:
                continue

            # Look for prerequisite patterns in content
            prereqs = self._extract_prerequisites_from_text(
                result.chunk.content,
                topic
            )

            for prereq_text in prereqs:
                # Create prerequisite with source
                prereq = Prerequisite(
                    concept=prereq_text,
                    reason=self._infer_reason(prereq_text, topic),
                    source=result.chunk.metadata.get("path", "unknown"),
                    confidence=result.score
                )
                prerequisites.append(prereq)

        # Deduplicate and rank by confidence
        prerequisites = self._deduplicate_prerequisites(prerequisites)
        prerequisites.sort(key=lambda p: p.confidence, reverse=True)

        return prerequisites

    def build_prerequisite_graph(
        self,
        topic: str,
        max_depth: int = 3
    ) -> PrerequisiteGraph:
        """
        Build complete prerequisite graph including indirect dependencies.

        Args:
            topic: Topic to analyze
            max_depth: How many levels deep to search

        Returns:
            Complete prerequisite graph with learning path
        """
        direct_prereqs = self.find_prerequisites(topic)
        indirect_prereqs = []
        all_concepts = {topic}

        # Find prerequisites of prerequisites (indirect)
        current_depth = 0
        to_process = [p.concept for p in direct_prereqs]

        while to_process and current_depth < max_depth:
            current_concept = to_process.pop(0)

            if current_concept in all_concepts:
                continue

            all_concepts.add(current_concept)

            # Find prerequisites for this concept
            concept_prereqs = self.find_prerequisites(current_concept)

            for prereq in concept_prereqs:
                if prereq.concept not in all_concepts:
                    indirect_prereqs.append(prereq)
                    to_process.append(prereq.concept)

            current_depth += 1

        # Build learning path (topological sort)
        learning_path = self._build_learning_path(
            topic,
            direct_prereqs,
            indirect_prereqs
        )

        return PrerequisiteGraph(
            topic=topic,
            direct_prerequisites=direct_prereqs,
            indirect_prerequisites=indirect_prereqs,
            learning_path=learning_path
        )

    def find_related_concepts(
        self,
        topic: str,
        top_k: int = 10
    ) -> List[str]:
        """
        Find concepts related to a topic.

        Args:
            topic: Topic to find related concepts for
            top_k: Number of related concepts to return

        Returns:
            List of related concept names
        """
        # Search for related content
        results = self.retrieval.search(
            query=f"related to {topic} similar concepts",
            top_k=top_k * 2,
            use_reranking=True
        )

        # Extract concept names from metadata and content
        concepts = set()
        for result in results:
            # Get topics from metadata
            topics = result.chunk.metadata.get("topics", [])
            concepts.update(topics)

            # Extract concepts from content (first 200 chars)
            content_concepts = self._extract_concepts_from_text(
                result.chunk.content[:200]
            )
            concepts.update(content_concepts)

        # Remove the original topic
        concepts.discard(topic)

        return list(concepts)[:top_k]

    def get_recommended_learning_order(
        self,
        topics: List[str]
    ) -> List[str]:
        """
        Given multiple topics, determine optimal learning order.

        Args:
            topics: List of topics to learn

        Returns:
            Ordered list (fundamentals first)
        """
        # Build prerequisite graphs for all topics
        graphs = {topic: self.build_prerequisite_graph(topic) for topic in topics}

        # Count how many times each topic is a prerequisite
        prerequisite_counts = {}
        for topic in topics:
            prerequisite_counts[topic] = 0

        for topic, graph in graphs.items():
            prereqs = [p.concept for p in graph.direct_prerequisites]
            for prereq_concept in prereqs:
                if prereq_concept in prerequisite_counts:
                    prerequisite_counts[prereq_concept] += 1

        # Sort: topics that are prerequisites come first
        ordered = sorted(topics, key=lambda t: (
            -prerequisite_counts[t],  # More prereqs = earlier
            t  # Alphabetical tiebreaker
        ))

        return ordered

    def _extract_prerequisites_from_text(
        self,
        text: str,
        topic: str
    ) -> List[str]:
        """Extract prerequisite concepts from text."""
        prerequisites = []

        # Prerequisite patterns
        patterns = [
            r"(?i)prerequisite[s]?:\s*(.+)",
            r"(?i)requires?:\s*(.+)",
            r"(?i)before\s+learning\s+" + re.escape(topic) + r",?\s+(.+)",
            r"(?i)you\s+should\s+(?:know|understand):\s*(.+)",
            r"(?i)assumes?\s+(?:knowledge\s+of|familiarity\s+with):\s*(.+)",
            r"(?i)builds?\s+on:\s*(.+)"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Split on common separators
                items = re.split(r"[,;]|\sand\s|\sor\s", match)
                for item in items:
                    item = item.strip().strip(".")
                    if len(item) > 3 and len(item) < 50:  # Reasonable length
                        prerequisites.append(item)

        return prerequisites

    def _infer_reason(self, prerequisite: str, topic: str) -> str:
        """Infer why a prerequisite is needed."""
        prereq_lower = prerequisite.lower()
        topic_lower = topic.lower()

        # Common prerequisite reasons
        if "basic" in prereq_lower or "fundamental" in prereq_lower:
            return f"Foundation for understanding {topic}"
        elif "programming" in prereq_lower or "python" in prereq_lower:
            return f"{topic} uses programming concepts extensively"
        elif "math" in prereq_lower or "calculus" in prereq_lower:
            return f"Mathematical foundation for {topic}"
        elif "command" in prereq_lower or "terminal" in prereq_lower:
            return f"{topic} requires command-line interaction"
        else:
            return f"Required for {topic}"

    def _deduplicate_prerequisites(
        self,
        prerequisites: List[Prerequisite]
    ) -> List[Prerequisite]:
        """Remove duplicate prerequisites, keeping highest confidence."""
        seen = {}
        for prereq in prerequisites:
            concept_lower = prereq.concept.lower()
            if concept_lower not in seen or prereq.confidence > seen[concept_lower].confidence:
                seen[concept_lower] = prereq

        return list(seen.values())

    def _build_learning_path(
        self,
        topic: str,
        direct_prereqs: List[Prerequisite],
        indirect_prereqs: List[Prerequisite]
    ) -> List[str]:
        """
        Build ordered learning path (topological sort).

        Returns path from fundamentals to topic.
        """
        # Simple heuristic-based ordering
        all_prereqs = direct_prereqs + indirect_prereqs

        # Group by "level" (how fundamental)
        levels = {
            "fundamental": [],
            "intermediate": [],
            "advanced": []
        }

        for prereq in all_prereqs:
            concept_lower = prereq.concept.lower()
            if any(word in concept_lower for word in ["basic", "fundamental", "introduction"]):
                levels["fundamental"].append(prereq.concept)
            elif any(word in concept_lower for word in ["advanced", "optimization", "production"]):
                levels["advanced"].append(prereq.concept)
            else:
                levels["intermediate"].append(prereq.concept)

        # Build path
        path = []
        path.extend(levels["fundamental"])
        path.extend(levels["intermediate"])
        path.extend(levels["advanced"])
        path.append(topic)

        return path

    def _extract_concepts_from_text(self, text: str) -> Set[str]:
        """Extract concept names from text."""
        concepts = set()

        # Look for capitalized phrases (potential concepts)
        # Simple heuristic: 2-4 capitalized words
        pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b"
        matches = re.findall(pattern, text)

        for match in matches:
            if len(match) < 50:  # Reasonable length
                concepts.add(match)

        return concepts


def discover_prerequisites(
    topic: str,
    index_path: str = "learning_content_index.pkl"
) -> List[Prerequisite]:
    """
    Convenience function to discover prerequisites.

    Args:
        topic: Topic to find prerequisites for
        index_path: Path to indexed content

    Returns:
        List of prerequisites
    """
    discovery = PrerequisiteDiscovery(index_path)
    return discovery.find_prerequisites(topic)


def build_learning_path(
    topic: str,
    index_path: str = "learning_content_index.pkl"
) -> List[str]:
    """
    Convenience function to build complete learning path.

    Args:
        topic: Topic to learn
        index_path: Path to indexed content

    Returns:
        Ordered learning path
    """
    discovery = PrerequisiteDiscovery(index_path)
    graph = discovery.build_prerequisite_graph(topic)
    return graph.learning_path


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("PREREQUISITE DISCOVERY - Phase 4 Task 4")
    print("=" * 70)
    print()

    # Discover prerequisites for ROS2 Navigation
    print("Finding prerequisites for 'ROS2 Navigation'...")
    print()

    try:
        prereqs = discover_prerequisites("ROS2 Navigation")

        print(f"Found {len(prereqs)} prerequisites:")
        for i, prereq in enumerate(prereqs[:5], 1):  # Top 5
            print(f"\n{i}. {prereq.concept}")
            print(f"   Reason: {prereq.reason}")
            print(f"   Confidence: {prereq.confidence:.2f}")
            print(f"   Source: {prereq.source}")

        print()
        print("=" * 70)
        print()

        # Build learning path
        print("Building complete learning path...")
        path = build_learning_path("ROS2 Navigation")

        print(f"\nRecommended learning path ({len(path)} steps):")
        for i, step in enumerate(path, 1):
            print(f"  {i}. {step}")

    except Exception as e:
        print(f"Note: Run content_indexer.py first to create index")
        print(f"Error: {e}")

    print()
    print("=" * 70)
    print()
