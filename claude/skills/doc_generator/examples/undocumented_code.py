"""
Undocumented Code Example

This file contains code without proper docstrings to demonstrate
the doc-generator skill.
"""


class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.data = []

    def load_data(self, file_path: str) -> bool:
        try:
            with open(file_path, 'r') as f:
                self.data = f.readlines()
            return True
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def process(self, transformations: list) -> dict:
        results = {
            'processed': 0,
            'failed': 0,
            'data': []
        }

        for item in self.data:
            try:
                processed_item = item
                for transform in transformations:
                    processed_item = transform(processed_item)
                results['data'].append(processed_item)
                results['processed'] += 1
            except Exception as e:
                results['failed'] += 1

        return results

    def save_results(self, output_path: str, data: list):
        with open(output_path, 'w') as f:
            for item in data:
                f.write(str(item) + '\n')


def calculate_metrics(data: list, metric_type: str = 'mean') -> float:
    if not data:
        raise ValueError("Data list cannot be empty")

    if metric_type == 'mean':
        return sum(data) / len(data)
    elif metric_type == 'median':
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    elif metric_type == 'max':
        return max(data)
    elif metric_type == 'min':
        return min(data)
    else:
        raise ValueError(f"Unknown metric type: {metric_type}")


def validate_config(config: dict) -> bool:
    required_keys = ['input_path', 'output_path', 'mode']

    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: {key}")

    if config['mode'] not in ['batch', 'stream']:
        raise ValueError("Mode must be 'batch' or 'stream'")

    return True


class ConfigManager:
    def __init__(self):
        self.configs = {}

    def load(self, config_file: str):
        import json
        with open(config_file, 'r') as f:
            self.configs = json.load(f)

    def get(self, key: str, default=None):
        return self.configs.get(key, default)

    def set(self, key: str, value):
        self.configs[key] = value

    def save(self, config_file: str):
        import json
        with open(config_file, 'w') as f:
            json.dump(self.configs, f, indent=2)
