"""Command-line entry point for the MP1 data pipeline."""

import argparse
import logging
import sys

from pathlib import Path

from data_loaders import load_data


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure console logging for the pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    """Parse command-line arguments for the pipeline."""
    parser = argparse.ArgumentParser(description="Load data files from the command line.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument(
        "--format",
        choices=("csv", "json"),
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def validate_input(filepath):
    """Return whether filepath exists and refers to a file, logging the result."""
    path = Path(filepath)
    if not path.is_file():
        logger.error("Input file not found: %s", filepath)
        return False

    logger.info("Input file validated: %s", filepath)
    return True


def main():
    """Validate and load the requested input file."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, output=%s, format=%s",
        args.input,
        args.output,
        args.format,
    )

    if not validate_input(args.input):
        sys.exit(1)

    try:
        data = load_data(args.input)
    except ValueError:
        sys.exit(1)

    # Part 2 loads the data; later parts will transform and write it.
    return data


if __name__ == "__main__":
    main()
