import os

import yaml


def load_config() -> dict:
    """
    Load configuration from a YAML file.
    
    Returns:
        dict: Configuration dictionary.
    """
    with open ("config.yaml") as f:
        config = yaml.safe_load(f)
        return config