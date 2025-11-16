"""
Mutation Testing

Validates test quality by introducing code mutations and checking if tests catch them.
"""

import ast
import copy
import tempfile
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from pathlib import Path


@dataclass
class Mutation:
    """Represents a single code mutation."""
    mutation_type: str
    original_code: str
    mutated_code: str
    line_number: int
    description: str


@dataclass
class MutationResult:
    """Result of testing a mutation."""
    mutation: Mutation
    killed: bool  # True if tests detected the mutation
    test_output: str
    error: Optional[str] = None


@dataclass
class MutationScore:
    """Mutation testing score."""
    total_mutants: int
    killed_mutants: int
    survived_mutants: int
    mutation_score: float  # Percentage of mutants killed
    results: List[MutationResult]

    def get_survived_mutations(self) -> List[Mutation]:
        """Get mutations that survived (tests didn't catch them)."""
        return [r.mutation for r in self.results if not r.killed]

    def get_killed_mutations(self) -> List[Mutation]:
        """Get mutations that were killed (tests caught them)."""
        return [r.mutation for r in self.results if r.killed]


class MutationOperator:
    """Base class for mutation operators."""

    def mutate(self, node: ast.AST) -> List[ast.AST]:
        """Generate mutations for a given AST node."""
        raise NotImplementedError


class ComparisonOperatorMutator(MutationOperator):
    """Mutates comparison operators (>, <, >=, <=, ==, !=)."""

    MUTATIONS = {
        ast.Gt: [ast.GtE, ast.Lt, ast.Eq],  # > -> >=, <, ==
        ast.GtE: [ast.Gt, ast.Lt],  # >= -> >, <
        ast.Lt: [ast.LtE, ast.Gt, ast.Eq],  # < -> <=, >, ==
        ast.LtE: [ast.Lt, ast.Gt],  # <= -> <, >
        ast.Eq: [ast.NotEq, ast.Lt, ast.Gt],  # == -> !=, <, >
        ast.NotEq: [ast.Eq],  # != -> ==
    }

    def mutate(self, node: ast.Compare) -> List[ast.Compare]:
        """Generate comparison operator mutations."""
        mutations = []

        for i, op in enumerate(node.ops):
            op_type = type(op)
            if op_type in self.MUTATIONS:
                for new_op_type in self.MUTATIONS[op_type]:
                    mutated = copy.deepcopy(node)
                    mutated.ops[i] = new_op_type()
                    mutations.append(mutated)

        return mutations


class ArithmeticOperatorMutator(MutationOperator):
    """Mutates arithmetic operators (+, -, *, /, //, %, **)."""

    MUTATIONS = {
        ast.Add: [ast.Sub, ast.Mult],  # + -> -, *
        ast.Sub: [ast.Add, ast.Mult],  # - -> +, *
        ast.Mult: [ast.Div, ast.Add],  # * -> /, +
        ast.Div: [ast.Mult, ast.FloorDiv],  # / -> *, //
        ast.FloorDiv: [ast.Div, ast.Mod],  # // -> /, %
        ast.Mod: [ast.Mult, ast.FloorDiv],  # % -> *, //
    }

    def mutate(self, node: ast.BinOp) -> List[ast.BinOp]:
        """Generate arithmetic operator mutations."""
        mutations = []

        op_type = type(node.op)
        if op_type in self.MUTATIONS:
            for new_op_type in self.MUTATIONS[op_type]:
                mutated = copy.deepcopy(node)
                mutated.op = new_op_type()
                mutations.append(mutated)

        return mutations


class BooleanOperatorMutator(MutationOperator):
    """Mutates boolean operators (and, or)."""

    MUTATIONS = {
        ast.And: [ast.Or],
        ast.Or: [ast.And],
    }

    def mutate(self, node: ast.BoolOp) -> List[ast.BoolOp]:
        """Generate boolean operator mutations."""
        mutations = []

        op_type = type(node.op)
        if op_type in self.MUTATIONS:
            for new_op_type in self.MUTATIONS[op_type]:
                mutated = copy.deepcopy(node)
                mutated.op = new_op_type()
                mutations.append(mutated)

        return mutations


class ConstantMutator(MutationOperator):
    """Mutates constant values."""

    @staticmethod
    def mutate_number(value):
        """Generate mutations for numeric constants."""
        mutations = []
        if value == 0:
            mutations.extend([1, -1])
        elif value == 1:
            mutations.extend([0, 2, -1])
        elif value > 0:
            mutations.extend([value + 1, value - 1, 0, -value])
        else:
            mutations.extend([value + 1, value - 1, 0, -value])
        return mutations[:3]  # Limit to 3 mutations

    @staticmethod
    def mutate_string(value):
        """Generate mutations for string constants."""
        if not value:
            return ["x"]
        return ["", value + "x", value[:-1] if len(value) > 1 else ""]

    def mutate(self, node: ast.Constant) -> List[ast.Constant]:
        """Generate constant value mutations."""
        mutations = []

        if isinstance(node.value, bool):
            # Boolean constants
            mutated = copy.deepcopy(node)
            mutated.value = not node.value
            mutations.append(mutated)
        elif isinstance(node.value, (int, float)):
            # Numeric constants
            for new_value in self.mutate_number(node.value):
                mutated = copy.deepcopy(node)
                mutated.value = new_value
                mutations.append(mutated)
        elif isinstance(node.value, str):
            # String constants
            for new_value in self.mutate_string(node.value):
                mutated = copy.deepcopy(node)
                mutated.value = new_value
                mutations.append(mutated)

        return mutations


class UnaryOperatorMutator(MutationOperator):
    """Mutates unary operators (not, -, +)."""

    def mutate(self, node: ast.UnaryOp) -> List[ast.UnaryOp]:
        """Generate unary operator mutations."""
        mutations = []

        if isinstance(node.op, ast.Not):
            # Remove 'not' operator - return the operand directly
            # This is handled by returning empty list and the transformer will skip it
            pass
        elif isinstance(node.op, ast.USub):
            # Change -x to +x
            mutated = copy.deepcopy(node)
            mutated.op = ast.UAdd()
            mutations.append(mutated)
        elif isinstance(node.op, ast.UAdd):
            # Change +x to -x
            mutated = copy.deepcopy(node)
            mutated.op = ast.USub()
            mutations.append(mutated)

        return mutations


class ReturnValueMutator(MutationOperator):
    """Mutates return values."""

    def mutate(self, node: ast.Return) -> List[ast.Return]:
        """Generate return value mutations."""
        mutations = []

        if node.value is None:
            # No return value - can't mutate
            return mutations

        # Mutation 1: Return None instead
        mutated = copy.deepcopy(node)
        mutated.value = ast.Constant(value=None)
        mutations.append(mutated)

        # Mutation 2: Return opposite boolean if returning bool constant
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, bool):
            mutated = copy.deepcopy(node)
            mutated.value.value = not node.value.value
            mutations.append(mutated)

        return mutations


class MutationGenerator:
    """Generates mutations for source code."""

    def __init__(self):
        self.operators = [
            ComparisonOperatorMutator(),
            ArithmeticOperatorMutator(),
            BooleanOperatorMutator(),
            ConstantMutator(),
            UnaryOperatorMutator(),
            ReturnValueMutator(),
        ]

    def generate_mutations(self, source_code: str) -> List[Mutation]:
        """
        Generate all possible mutations for source code.

        Args:
            source_code: Python source code to mutate

        Returns:
            List of Mutation objects
        """
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return []

        mutations = []

        # Visit all nodes and generate mutations
        for node in ast.walk(tree):
            node_mutations = self._generate_node_mutations(node, source_code, tree)
            mutations.extend(node_mutations)

        return mutations

    def _generate_node_mutations(
        self,
        node: ast.AST,
        original_code: str,
        original_tree: ast.AST
    ) -> List[Mutation]:
        """Generate mutations for a specific node."""
        mutations = []

        for operator in self.operators:
            # Check if operator can mutate this node type
            if isinstance(node, ast.Compare) and isinstance(operator, ComparisonOperatorMutator):
                mutated_nodes = operator.mutate(node)
            elif isinstance(node, ast.BinOp) and isinstance(operator, ArithmeticOperatorMutator):
                mutated_nodes = operator.mutate(node)
            elif isinstance(node, ast.BoolOp) and isinstance(operator, BooleanOperatorMutator):
                mutated_nodes = operator.mutate(node)
            elif isinstance(node, ast.Constant) and isinstance(operator, ConstantMutator):
                mutated_nodes = operator.mutate(node)
            elif isinstance(node, ast.UnaryOp) and isinstance(operator, UnaryOperatorMutator):
                mutated_nodes = operator.mutate(node)
            elif isinstance(node, ast.Return) and isinstance(operator, ReturnValueMutator):
                mutated_nodes = operator.mutate(node)
            else:
                continue

            # Create Mutation objects for each mutated node
            for mutated_node in mutated_nodes:
                mutation = self._create_mutation(
                    node, mutated_node, original_code, original_tree, operator
                )
                if mutation:
                    mutations.append(mutation)

        return mutations

    def _create_mutation(
        self,
        original_node: ast.AST,
        mutated_node: ast.AST,
        original_code: str,
        original_tree: ast.AST,
        operator: MutationOperator
    ) -> Optional[Mutation]:
        """Create a Mutation object from nodes."""
        try:
            # Create a new tree with the mutation
            mutated_tree = copy.deepcopy(original_tree)

            # Replace the node in the tree
            replacer = NodeReplacer(original_node, mutated_node)
            replacer.visit(mutated_tree)

            # Generate code from both trees
            original_snippet = ast.unparse(original_node)
            mutated_snippet = ast.unparse(mutated_node)
            mutated_full_code = ast.unparse(mutated_tree)

            return Mutation(
                mutation_type=type(operator).__name__,
                original_code=original_code,
                mutated_code=mutated_full_code,
                line_number=getattr(original_node, 'lineno', 0),
                description=f"Changed '{original_snippet}' to '{mutated_snippet}'"
            )
        except Exception:
            return None


class NodeReplacer(ast.NodeTransformer):
    """AST transformer that replaces a specific node."""

    def __init__(self, target_node: ast.AST, replacement_node: ast.AST):
        self.target_node = target_node
        self.replacement_node = replacement_node
        self.replaced = False

    def visit(self, node):
        """Visit a node and replace if it matches target."""
        # Check if this is the node to replace
        # We compare by id since nodes are unique objects
        if not self.replaced and self._nodes_equal(node, self.target_node):
            self.replaced = True
            return self.replacement_node
        return super().visit(node)

    def _nodes_equal(self, node1: ast.AST, node2: ast.AST) -> bool:
        """Check if two nodes are equal (same location in tree)."""
        # Compare by line number and type as a heuristic
        if type(node1) != type(node2):
            return False

        line1 = getattr(node1, 'lineno', None)
        line2 = getattr(node2, 'lineno', None)
        col1 = getattr(node1, 'col_offset', None)
        col2 = getattr(node2, 'col_offset', None)

        return line1 == line2 and col1 == col2


class MutationRunner:
    """Runs tests against mutated code."""

    def run_mutation_tests(
        self,
        source_file: Path,
        test_file: Path,
        mutations: List[Mutation],
        max_mutations: Optional[int] = None
    ) -> MutationScore:
        """
        Run tests against mutations.

        Args:
            source_file: Path to source code file
            test_file: Path to test file
            mutations: List of mutations to test
            max_mutations: Maximum number of mutations to test (for performance)

        Returns:
            MutationScore with results
        """
        if max_mutations:
            mutations = mutations[:max_mutations]

        results = []

        for mutation in mutations:
            result = self._test_mutation(source_file, test_file, mutation)
            results.append(result)

        killed = sum(1 for r in results if r.killed)
        total = len(results)
        score = (killed / total * 100) if total > 0 else 0.0

        return MutationScore(
            total_mutants=total,
            killed_mutants=killed,
            survived_mutants=total - killed,
            mutation_score=score,
            results=results
        )

    def _test_mutation(
        self,
        source_file: Path,
        test_file: Path,
        mutation: Mutation
    ) -> MutationResult:
        """Test a single mutation."""
        # Create temporary file with mutated code
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            dir=source_file.parent
        ) as f:
            f.write(mutation.mutated_code)
            temp_file = Path(f.name)

        try:
            # Backup original file
            original_content = source_file.read_text()

            # Replace with mutated code
            source_file.write_text(mutation.mutated_code)

            # Run tests
            result = subprocess.run(
                ['pytest', str(test_file), '-v'],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Mutation is killed if tests fail
            killed = result.returncode != 0

            return MutationResult(
                mutation=mutation,
                killed=killed,
                test_output=result.stdout + result.stderr
            )

        except subprocess.TimeoutExpired:
            return MutationResult(
                mutation=mutation,
                killed=False,
                test_output="",
                error="Test execution timed out"
            )
        except Exception as e:
            return MutationResult(
                mutation=mutation,
                killed=False,
                test_output="",
                error=str(e)
            )
        finally:
            # Restore original file
            source_file.write_text(original_content)
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()
