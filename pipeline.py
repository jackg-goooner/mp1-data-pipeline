"""Command-line entry point for the complete MP1 data pipeline."""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments for the pipeline."""
    parser = argparse.ArgumentParser(description="Load, validate, and clean data files.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main():
    """Run the configured load, validation, cleaning, and save workflow."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input,
        args.config,
        args.output,
    )

    if not validate_input(args.input) or not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except (ValueError, OSError):
        sys.exit(1)

    validation = config.get("validation", {})
    required_columns = validation.get("required_columns", [])
    numeric_columns = validation.get("numeric_columns", [])
    rows_before_validation = len(data)
    try:
        validated_data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(
        "Validation complete: %s -> %s rows",
        rows_before_validation,
        len(validated_data),
    )

    try:
        cleaned_data = process_data(validated_data, config)
    except (KeyError, ValueError):
        sys.exit(1)

    report = create_cleaning_report(validated_data, cleaned_data)
    logger.info(
        "Processing complete: %s -> %s rows",
        report["rows_before"],
        report["rows_after"],
    )
    save_data(cleaned_data, args.output)
    logger.info("Saved cleaned data to %s", args.output)

    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()
