"""Main entry point for F1 Fantasy Analysis application."""

import argparse
import logging
import sys
from typing import List

import uvicorn

from backend.utils.config import API_DEBUG, API_HOST, API_PORT
from backend.utils.logging import setup_logging


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="F1 Fantasy Analysis")
    parser.add_argument(
        "--host", type=str, default=API_HOST, help="Host to run the API server on"
    )
    parser.add_argument(
        "--port", type=int, default=API_PORT, help="Port to run the API server on"
    )
    parser.add_argument(
        "--debug", action="store_true", default=API_DEBUG, help="Enable debug mode"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    parser.add_argument(
        "--log-file", type=str, default=None, help="Log file path (logs to console if not specified)"
    )
    
    return parser.parse_args(args)


def main() -> None:
    """Main entry point for the application."""
    args = parse_args(sys.argv[1:])
    
    # Set up logging
    setup_logging(log_level=args.log_level, log_file=args.log_file)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting F1 Fantasy Analysis API on {args.host}:{args.port}")
    
    # Run the API server
    uvicorn.run(
        "backend.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level=args.log_level.lower(),
    )


if __name__ == "__main__":
    main() 