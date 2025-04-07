#!/usr/bin/env python3
"""
Command-line interface for the RSS feed monitoring system.
"""

import os
import sys
import argparse
import logging
from rss_monitor.core import run_monitor, run_once, setup_directories

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='AI Governance RSS Feed Monitor')
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up the directory structure')
    
    # Run once command
    once_parser = subparsers.add_parser('once', help='Run the monitor once')
    
    # Run continuously command
    continuous_parser = subparsers.add_parser('run', help='Run the monitor continuously')
    continuous_parser.add_argument(
        '--interval', 
        type=int, 
        default=3600, 
        help='Interval in seconds between runs (default: 3600)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rss_monitor.log')),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('rss_monitor_cli')
    
    # Execute the appropriate command
    if args.command == 'setup':
        logger.info("Setting up directory structure")
        setup_directories()
        logger.info("Directory structure set up successfully")
    elif args.command == 'once':
        logger.info("Running monitor once")
        run_once()
    elif args.command == 'run':
        logger.info(f"Running monitor continuously with interval {args.interval} seconds")
        run_monitor(interval=args.interval)
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
