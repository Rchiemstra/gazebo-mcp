"""
Main Module

Main application logic.
"""

from .utils import process_data, DataProcessor, MAX_ITEMS


def main():
    """Main entry point."""
    # Use process_data function
    data = [1, 2, 3, 4, 5]
    result = process_data(data, lambda x: x * 2)
    print(f"Processed: {result}")

    # Use DataProcessor class
    processor = DataProcessor({'transform': lambda x: x ** 2})
    output = processor.process(data)
    print(f"Output: {output}")

    # Use constant
    if len(data) > MAX_ITEMS:
        print("Too many items!")


def run_analysis(data_source: str):
    """
    Run data analysis.

    Args:
        data_source: Path to data source
    """
    # Create processor
    config = {'timeout': 60}
    processor = DataProcessor(config)

    # Load and process data
    data = load_data(data_source)
    results = processor.process(data)

    # Clear cache after processing
    processor.clear_cache()

    return results


def load_data(source: str) -> list:
    """
    Load data from source.

    Args:
        source: Data source path

    Returns:
        Loaded data
    """
    # Stub implementation
    return [1, 2, 3]


if __name__ == "__main__":
    main()
