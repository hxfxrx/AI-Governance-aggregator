#!/usr/bin/env python3
"""
Main script for the staging area management CLI.
"""

import os
import sys
import argparse
import json
import logging
from tabulate import tabulate
from rss_monitor.staging import (
    list_new_articles, 
    approve_article, 
    reject_article, 
    export_to_obsidian, 
    get_staging_stats
)

def main():
    """Main entry point for the staging CLI."""
    parser = argparse.ArgumentParser(description='AI Governance RSS Feed Staging Manager')
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List articles in the staging area')
    list_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    # Approve command
    approve_parser = subparsers.add_parser('approve', help='Approve an article')
    approve_parser.add_argument('article_id', help='ID of the article to approve')
    
    # Reject command
    reject_parser = subparsers.add_parser('reject', help='Reject an article')
    reject_parser.add_argument('article_id', help='ID of the article to reject')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export approved articles to Obsidian')
    export_parser.add_argument('--article-id', help='ID of a specific article to export (optional)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Get statistics about the staging area')
    stats_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staging_manager.log')),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger('staging_cli')
    
    # Execute the appropriate command
    if args.command == 'list':
        articles = list_new_articles()
        if args.format == 'json':
            print(json.dumps(articles, indent=2))
        else:
            if not articles:
                print("No new articles found in the staging area.")
            else:
                table_data = []
                for article in articles:
                    table_data.append([
                        article.get('id', ''),
                        article.get('title', ''),
                        article.get('source', ''),
                        article.get('language', ''),
                        article.get('date', '')
                    ])
                
                headers = ['ID', 'Title', 'Source', 'Language', 'Date']
                print(tabulate(table_data, headers=headers, tablefmt='grid'))
                print(f"\nTotal: {len(articles)} articles")
    
    elif args.command == 'approve':
        success = approve_article(args.article_id)
        if success:
            print(f"Article {args.article_id} approved successfully.")
        else:
            print(f"Failed to approve article {args.article_id}.")
            return 1
    
    elif args.command == 'reject':
        success = reject_article(args.article_id)
        if success:
            print(f"Article {args.article_id} rejected successfully.")
        else:
            print(f"Failed to reject article {args.article_id}.")
            return 1
    
    elif args.command == 'export':
        stats = export_to_obsidian(args.article_id)
        print(f"Export completed: {stats['exported']} articles exported, {stats['errors']} errors.")
        if stats['exported'] > 0:
            print("\nExported articles:")
            for article in stats['articles']:
                print(f"- {article['title']} -> {article['path']}")
    
    elif args.command == 'stats':
        stats = get_staging_stats()
        if args.format == 'json':
            print(json.dumps(stats, indent=2))
        else:
            print("\nStaging Area Statistics:")
            print(f"New articles: {stats['new']}")
            print(f"Reviewed articles: {stats['reviewed']}")
            print(f"Rejected articles: {stats['rejected']}")
            print(f"Total articles: {stats['total']}")
            
            print("\nBy Category:")
            category_data = [[category, count] for category, count in stats['by_category'].items()]
            print(tabulate(category_data, headers=['Category', 'Count'], tablefmt='simple'))
            
            print("\nBy Language:")
            language_data = [[language, count] for language, count in stats['by_language'].items()]
            print(tabulate(language_data, headers=['Language', 'Count'], tablefmt='simple'))
            
            print("\nBy Source:")
            source_data = [[source, count] for source, count in stats['by_source'].items()]
            print(tabulate(source_data, headers=['Source', 'Count'], tablefmt='simple'))
    
    else:
        parser.print_help()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
