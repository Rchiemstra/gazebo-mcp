"""
Utility Functions

Common utility functions used throughout the project.
"""


def process_data(data: list, transform: callable = None) -> list:
    """
    Process data with optional transformation.

    Args:
        data: List of data items
        transform: Optional transformation function

    Returns:
        Processed data list
    """
    if transform:
        return [transform(item) for item in data]
    return data


def validate_input(value: any, required: bool = False) -> bool:
    """
    Validate input value.

    Args:
        value: Value to validate
        required: Whether value is required

    Returns:
        True if valid, False otherwise
    """
    if required and not value:
        return False
    return True


class DataProcessor:
    """Processes data with various transformations."""

    def __init__(self, config: dict):
        """
        Initialize data processor.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.cache = {}

    def process(self, data: list) -> dict:
        """
        Process data and return results.

        Args:
            data: Data to process

        Returns:
            Processing results
        """
        results = process_data(data, self.config.get('transform'))

        return {
            'processed': results,
            'count': len(results)
        }

    def clear_cache(self):
        """Clear processing cache."""
        self.cache = {}


MAX_ITEMS = 1000
DEFAULT_TIMEOUT = 30
