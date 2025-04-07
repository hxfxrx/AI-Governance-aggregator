"""
Command-line interface for the Obsidian integration module.
"""

import os
import sys
import argparse
import json
import logging
from pathlib import Path
from obsidian_integration.obsidian import ObsidianIntegration

def main():
    """Main entry point for the Obsidian integration CLI."""
    parser = argparse.ArgumentParser(description='AI Governance Obsidian Integration')
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up a new Obsidian vault')
    setup_parser.add_argument('--vault-path', required=True, help='Path to the Obsidian vault')
    setup_parser.add_argument('--digital-garden-path', help='Path to the digital garden directory (optional)')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import an article into Obsidian')
    import_parser.add_argument('--vault-path', required=True, help='Path to the Obsidian vault')
    import_parser.add_argument('--article-path', required=True, help='Path to the article markdown file')
    import_parser.add_argument('--category', help='Category to place the article in (optional)')
    
    # Batch import command
    batch_parser = subparsers.add_parser('batch-import', help='Import multiple articles into Obsidian')
    batch_parser.add_argument('--vault-path', required=True, help='Path to the Obsidian vault')
    batch_parser.add_argument('--source-dir', required=True, help='Directory containing articles to import')
    batch_parser.add_argument('--mapping-file', help='JSON file mapping article IDs to categories (optional)')
    
    # Create index command
    index_parser = subparsers.add_parser('create-index', help='Create an index note for the AI Governance vault')
    index_parser.add_argument('--vault-path', required=True, help='Path to the Obsidian vault')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'obsidian_cli.log')),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('obsidian_cli')
    
    # Execute the appropriate command
    if args.command == 'setup':
        logger.info(f"Setting up Obsidian vault at {args.vault_path}")
        integration = ObsidianIntegration(args.vault_path, args.digital_garden_path)
        success = integration.setup_complete_vault()
        
        if success:
            print(f"Obsidian vault successfully set up at {args.vault_path}")
        else:
            print("Failed to set up Obsidian vault")
            return 1
    
    elif args.command == 'import':
        logger.info(f"Importing article {args.article_path} into Obsidian vault at {args.vault_path}")
        integration = ObsidianIntegration(args.vault_path)
        imported_path = integration.import_article(args.article_path, args.category)
        
        if imported_path:
            print(f"Article successfully imported to {imported_path}")
        else:
            print(f"Failed to import article {args.article_path}")
            return 1
    
    elif args.command == 'batch-import':
        logger.info(f"Batch importing articles from {args.source_dir} into Obsidian vault at {args.vault_path}")
        
        # Load category mapping if provided
        category_mapping = None
        if args.mapping_file:
            try:
                with open(args.mapping_file, 'r', encoding='utf-8') as f:
                    category_mapping = json.load(f)
            except Exception as e:
                logger.error(f"Error loading mapping file {args.mapping_file}: {e}")
                print(f"Error loading mapping file: {e}")
                return 1
        
        integration = ObsidianIntegration(args.vault_path)
        stats = integration.batch_import(args.source_dir, category_mapping)
        
        print(f"Batch import completed: {stats['imported']} of {stats['total']} articles imported, {stats['errors']} errors")
        if stats['imported'] > 0:
            print("\nImported articles:")
            for article in stats['articles']:
                print(f"- {article['id']} -> {article['destination']}")
    
    elif args.command == 'create-index':
        logger.info(f"Creating index note in Obsidian vault at {args.vault_path}")
        integration = ObsidianIntegration(args.vault_path)
        index_path = integration.create_index_note()
        
        if index_path:
            print(f"Index note successfully created at {index_path}")
        else:
            print("Failed to create index note")
            return 1
    
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
