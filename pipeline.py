"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format
json --verbose
"""
import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)
def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="data processing pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    
pass

def validate_input(filepath):
    """Check whether the input path exists and is a file"""
pass # TODO: implement
def main():
pass