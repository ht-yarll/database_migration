from src.config.load_config import load_config
from src.core.clouds.aws.aws import AWSHelper
from src.core.clouds.gcp.gcp import GCPHelper


def main():
    config = load_config()
    ...