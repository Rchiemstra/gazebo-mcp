"""
Advanced Parameter Value Inference

Infers realistic parameter values based on:
- Parameter names
- Type hints
- Docstrings
- Code context
- Common patterns
"""

import ast
import re
from typing import Any, Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ParameterHint:
    """Information about a parameter to help infer values."""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[Any] = None
    description: Optional[str] = None


class ParameterInference:
    """Smart parameter value inference."""

    # Common patterns for parameter names
    PATTERNS = {
        # Identifiers
        r'.*_?id$': '"test_id_123"',
        r'.*uuid.*': '"550e8400-e29b-41d4-a716-446655440000"',
        r'.*key.*': '"test_key_abc"',

        # Names and strings
        r'.*name$': '"test_name"',
        r'.*username.*': '"testuser"',
        r'.*email.*': '"test@example.com"',
        r'.*url.*': '"https://example.com"',
        r'.*path.*': '"/tmp/test/path"',
        r'.*message.*': '"Test message"',
        r'.*description.*': '"Test description"',
        r'.*title.*': '"Test Title"',
        r'.*text.*': '"Test text"',

        # Numbers
        r'.*amount.*': '100.00',
        r'.*price.*': '99.99',
        r'.*cost.*': '50.00',
        r'.*fee.*': '2.50',
        r'.*total.*': '150.00',
        r'.*count.*': '5',
        r'.*quantity.*': '10',
        r'.*num.*': '42',
        r'.*age.*': '25',
        r'.*limit.*': '100',
        r'.*offset.*': '0',
        r'.*size.*': '1024',

        # Booleans
        r'is_.*': 'True',
        r'has_.*': 'True',
        r'should_.*': 'True',
        r'.*enabled.*': 'True',
        r'.*active.*': 'True',

        # Collections
        r'.*items.*': '[]',
        r'.*list.*': '[]',
        r'.*data.*': '{}',
        r'.*params.*': '{}',
        r'.*options.*': '{}',
        r'.*config.*': '{}',
        r'.*settings.*': '{}',

        # Dates and times
        r'.*date.*': '"2025-10-25"',
        r'.*time.*': '"10:30:00"',
        r'.*timestamp.*': '1729852200',

        # Currencies
        r'.*currency.*': '"USD"',

        # Tokens and credentials
        r'.*token.*': '"test_token_xyz"',
        r'.*password.*': '"Test123!"',
        r'.*secret.*': '"test_secret"',

        # Status
        r'.*status.*': '"active"',
        r'.*state.*': '"pending"',
    }

    # Type-based defaults
    TYPE_DEFAULTS = {
        'str': '"test_string"',
        'int': '42',
        'float': '3.14',
        'bool': 'True',
        'list': '[]',
        'dict': '{}',
        'tuple': '()',
        'set': 'set()',
        'None': 'None',
        'Any': 'None',
    }

    def infer_value(self, param: ParameterHint, context: Optional[Dict] = None) -> str:
        """
        Infer a realistic value for a parameter.

        Args:
            param: Parameter information
            context: Additional context (function name, module, etc.)

        Returns:
            String representation of the value
        """
        # 1. Check for default value
        if param.default_value is not None:
            return self._format_value(param.default_value)

        # 2. Check type hint
        if param.type_hint:
            type_value = self._infer_from_type(param.type_hint)
            if type_value:
                return type_value

        # 3. Check name patterns
        for pattern, value in self.PATTERNS.items():
            if re.match(pattern, param.name, re.IGNORECASE):
                return value

        # 4. Use context if available
        if context:
            context_value = self._infer_from_context(param.name, context)
            if context_value:
                return context_value

        # 5. Fallback
        return 'None  # TODO: Provide value'

    def infer_multiple_values(self, param: ParameterHint, count: int = 3) -> List[str]:
        """
        Infer multiple test values for parametrized tests.

        Args:
            param: Parameter information
            count: Number of values to generate

        Returns:
            List of value strings
        """
        base_value = self.infer_value(param)

        # Generate variations based on type
        if param.type_hint and 'int' in param.type_hint.lower():
            return ['0', '1', '100', '-1', '999999'][:count]
        elif param.type_hint and 'float' in param.type_hint.lower():
            return ['0.0', '1.5', '100.0', '-1.5', '999999.99'][:count]
        elif param.type_hint and 'bool' in param.type_hint.lower():
            return ['True', 'False']
        elif param.type_hint and 'str' in param.type_hint.lower():
            return ['"test1"', '"test2"', '"test3"', '""', '"very_long_string_value"'][:count]
        elif param.type_hint and 'list' in param.type_hint.lower():
            return ['[]', '[1]', '[1, 2, 3]'][:count]

        # Name-based variations
        if 'amount' in param.name.lower() or 'price' in param.name.lower():
            return ['0.01', '100.00', '999.99', '0.00', '1000000.00'][:count]
        elif 'email' in param.name.lower():
            return ['"test@example.com"', '"user+tag@domain.co"', '"invalid-email"'][:count]
        elif 'id' in param.name.lower():
            return ['"id_123"', '"id_456"', '"id_789"'][:count]

        # Default variations
        return [base_value] * count

    def infer_boundary_values(self, param: ParameterHint) -> Dict[str, str]:
        """
        Infer boundary values for edge case testing.

        Returns:
            Dict with 'min', 'max', 'zero', 'negative' values
        """
        boundaries = {}

        if param.type_hint:
            if 'int' in param.type_hint.lower():
                boundaries['min'] = '0'
                boundaries['max'] = '2147483647'  # Max int32
                boundaries['zero'] = '0'
                boundaries['negative'] = '-1'
            elif 'float' in param.type_hint.lower():
                boundaries['min'] = '0.0'
                boundaries['max'] = '1e308'
                boundaries['zero'] = '0.0'
                boundaries['negative'] = '-1.0'
            elif 'str' in param.type_hint.lower():
                boundaries['empty'] = '""'
                boundaries['long'] = '"' + 'x' * 1000 + '"'
                boundaries['special_chars'] = r'"!@#$%^&*()"'
            elif 'list' in param.type_hint.lower():
                boundaries['empty'] = '[]'
                boundaries['single'] = '[1]'
                boundaries['many'] = '[' + ','.join(['1'] * 100) + ']'

        # Name-based boundaries
        if 'amount' in param.name.lower() or 'price' in param.name.lower():
            boundaries['min'] = '0.01'
            boundaries['max'] = '1000000.00'
            boundaries['zero'] = '0.00'
            boundaries['negative'] = '-1.00'

        return boundaries

    def _infer_from_type(self, type_hint: str) -> Optional[str]:
        """Infer value from type hint."""
        # Handle Optional types
        if 'Optional' in type_hint:
            inner_type = type_hint.replace('Optional[', '').replace(']', '').strip()
            return self.TYPE_DEFAULTS.get(inner_type)

        # Handle List types
        if 'List[' in type_hint or 'list[' in type_hint:
            return '[]'

        # Handle Dict types
        if 'Dict[' in type_hint or 'dict[' in type_hint:
            return '{}'

        # Direct type match
        return self.TYPE_DEFAULTS.get(type_hint)

    def _infer_from_context(self, param_name: str, context: Dict) -> Optional[str]:
        """Infer value from context."""
        func_name = context.get('function_name', '')

        # Payment context
        if 'payment' in func_name.lower():
            if 'amount' in param_name.lower():
                return '100.00'
            elif 'currency' in param_name.lower():
                return '"USD"'
            elif 'card' in param_name.lower():
                return '"tok_visa_4242"'

        # User context
        if 'user' in func_name.lower():
            if 'id' in param_name.lower():
                return '"user_123"'
            elif 'email' in param_name.lower():
                return '"user@example.com"'

        # Database context
        if 'db' in func_name.lower() or 'database' in func_name.lower():
            if 'id' in param_name.lower():
                return '"db_id_123"'

        return None

    def _format_value(self, value: Any) -> str:
        """Format a Python value as a string for test code."""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif value is None:
            return 'None'
        elif isinstance(value, (list, tuple, set, dict)):
            return repr(value)
        else:
            return repr(value)


def infer_parameter_value(
    param_name: str,
    type_hint: Optional[str] = None,
    default_value: Optional[Any] = None,
    context: Optional[Dict] = None
) -> str:
    """
    Convenience function to infer a parameter value.

    Args:
        param_name: Name of the parameter
        type_hint: Optional type hint
        default_value: Optional default value
        context: Optional context information

    Returns:
        Inferred value as string
    """
    param = ParameterHint(
        name=param_name,
        type_hint=type_hint,
        default_value=default_value
    )
    inference = ParameterInference()
    return inference.infer_value(param, context)
