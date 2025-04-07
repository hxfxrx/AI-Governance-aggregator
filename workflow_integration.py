"""
Integration module to connect the RSS monitoring system with Obsidian.
This module provides the bridge between the staging area and Obsidian.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

from scripts.rss_monitor.staging import list_new_articles, approve_article, export_to_obsidian
from scripts.obsidian_integration.obsidian import ObsidianIntegration

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workflow_integration.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('workflow_integration')

class WorkflowIntegration:
    """Class to handle the workflow integration between RSS monitoring and Obsidian."""
    
    def __init__(self, staging_dir, obsidian_vault_path, digital_garden_path=None):
        """
        Initialize the workflow integration.
        
        Args:
            staging_dir (str): Path to the staging directory
            obsidian_vault_path (str): Path to the Obsidian vault
            digital_garden_path (str, optional): Path to the digital garden directory
        """
        self.staging_dir = Path(staging_dir)
        self.obsidian_vault_path = Path(obsidian_vault_path)
        self.digital_garden_path = Path(digital_garden_path) if digital_garden_path else None
        
        # Initialize Obsidian integration
        self.obsidian = ObsidianIntegration(obsidian_vault_path, digital_garden_path)
        
        logger.info(f"Initialized workflow integration between {staging_dir} and {obsidian_vault_path}")
    
    def setup(self):
        """
        Set up the workflow integration.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            # Create staging directories if they don't exist
            os.makedirs(self.staging_dir / 'new', exist_ok=True)
            os.makedirs(self.staging_dir / 'reviewed', exist_ok=True)
            os.makedirs(self.staging_dir / 'rejected', exist_ok=True)
            os.makedirs(self.staging_dir / 'metadata', exist_ok=True)
            
            # Set up Obsidian vault
            self.obsidian.setup_complete_vault()
            
            logger.info("Workflow integration setup completed")
            return True
        
        except Exception as e:
            logger.error(f"Error setting up workflow integration: {e}")
            return False
    
    def process_new_articles(self, auto_approve=False):
        """
        Process new articles in the staging area.
        
        Args:
            auto_approve (bool): Whether to automatically approve all new articles
            
        Returns:
            dict: Statistics about the processing
        """
        stats = {
            'total': 0,
            'approved': 0,
            'imported': 0,
            'errors': 0
        }
        
        try:
            # Get list of new articles
            articles = list_new_articles()
            stats['total'] = len(articles)
            
            if auto_approve:
                # Automatically approve all articles
                for article in articles:
                    article_id = article['id']
                    
                    # Approve the article
                    if approve_article(article_id):
                        stats['approved'] += 1
                    else:
                        logger.error(f"Failed to approve article {article_id}")
                        stats['errors'] += 1
            
            # Export approved articles to Obsidian
            export_stats = export_to_obsidian()
            stats['imported'] = export_stats['exported']
            
            # Import articles from the reviewed directory to Obsidian
            reviewed_dir = self.staging_dir / 'reviewed'
            import_stats = self.obsidian.batch_import(reviewed_dir)
            
            # Update stats
            stats['imported'] = import_stats['imported']
            stats['errors'] += import_stats['errors']
            
            logger.info(f"Processed {stats['total']} new articles: {stats['approved']} approved, {stats['imported']} imported, {stats['errors']} errors")
            return stats
        
        except Exception as e:
            logger.error(f"Error processing new articles: {e}")
            return stats
    
    def create_daily_note(self):
        """
        Create a daily note in Obsidian with a summary of new content.
        
        Returns:
            str: Path to the created daily note
        """
        try:
            # Get today's date
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get list of articles approved today
            articles = []
            metadata_dir = self.staging_dir / 'metadata'
            
            for filename in os.listdir(metadata_dir):
                if filename.endswith('.json'):
                    try:
                        with open(metadata_dir / filename, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # Check if the article was approved today
                        approved_date = metadata.get('approved_date', '')
                        if approved_date.startswith(today):
                            articles.append(metadata)
                    
                    except Exception as e:
                        logger.error(f"Error reading metadata file {filename}: {e}")
            
            # Sort articles by date
            articles.sort(key=lambda x: x.get('date', ''), reverse=True)
            
            # Create content list
            content_list = ""
            for article in articles:
                title = article.get('title', 'Untitled')
                source = article.get('source', 'Unknown')
                category = article.get('category', 'Uncategorized')
                
                content_list += f"- [[{title}]] from {source} ({category})\n"
            
            if not content_list:
                content_list = "No new articles today."
            
            # Create daily note content
            daily_note_content = f"""---
date: {today}
tags: [daily-note, ai-governance]
---

# Daily Note: {today}

## New AI Governance Content

{content_list}

## Tasks

- [ ] Review new articles
- [ ] Update digital garden
- [ ] Research trending AI governance topics

## Notes

"""
            
            # Create daily notes directory if it doesn't exist
            daily_notes_dir = self.obsidian_vault_path / "Daily Notes"
            daily_notes_dir.mkdir(exist_ok=True)
            
            # Save daily note
            daily_note_path = daily_notes_dir / f"{today}.md"
            with open(daily_note_path, 'w', encoding='utf-8') as f:
                f.write(daily_note_content)
            
            logger.info(f"Created daily note at {daily_note_path}")
            return str(daily_note_path)
        
        except Exception as e:
            logger.error(f"Error creating daily note: {e}")
            return None
    
    def update_digital_garden(self):
        """
        Update the digital garden with the latest content.
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        if not self.digital_garden_path:
            logger.warning("Digital garden path not set, skipping update")
            return False
        
        try:
            # This would typically involve running the Obsidian Digital Garden plugin
            # Since we can't directly interact with Obsidian plugins, we'll simulate the process
            
            # Create digital garden directory if it doesn't exist
            self.digital_garden_path.mkdir(parents=True, exist_ok=True)
            
            # Create a simple index.html file
            index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Governance Digital Garden</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #1a1a1a;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .category {
            margin-bottom: 30px;
        }
        .article {
            margin-bottom: 15px;
            padding: 10px;
            border-left: 3px solid #0366d6;
            background-color: #f6f8fa;
        }
        .article-title {
            font-weight: bold;
        }
        .article-meta {
            font-size: 0.9em;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>AI Governance Digital Garden</h1>
    <p>A collection of curated content about AI Governance from around the world.</p>
    
    <h2>Categories</h2>
    
    <div class="category">
        <h3>Journalism</h3>
        <div class="article">
            <div class="article-title">Latest AI Governance Developments</div>
            <div class="article-meta">Source: The New York Times | Date: 2025-04-07</div>
            <p>Summary of the latest developments in AI governance...</p>
        </div>
    </div>
    
    <div class="category">
        <h3>International Organizations</h3>
        <div class="article">
            <div class="article-title">UNESCO's New AI Ethics Framework</div>
            <div class="article-meta">Source: UNESCO | Date: 2025-04-05</div>
            <p>Details about UNESCO's latest framework for AI ethics...</p>
        </div>
    </div>
    
    <div class="category">
        <h3>Academic</h3>
        <div class="article">
            <div class="article-title">Research on AI Governance Models</div>
            <div class="article-meta">Source: Centre for the Governance of AI | Date: 2025-04-03</div>
            <p>Summary of recent research on AI governance models...</p>
        </div>
    </div>
    
    <footer>
        <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        <p>Generated from Obsidian Digital Garden</p>
    </footer>
</body>
</html>"""
            
            index_path = self.digital_garden_path / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            logger.info(f"Updated digital garden at {self.digital_garden_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error updating digital garden: {e}")
            return False
    
    def run_complete_workflow(self, auto_approve=False):
        """
        Run the complete workflow from RSS monitoring to digital garden publishing.
        
        Args:
            auto_approve (bool): Whether to automatically approve all new articles
            
        Returns:
            dict: Statistics about the workflow
        """
        stats = {
            'new_articles': 0,
            'approved': 0,
            'imported': 0,
            'digital_garden_updated': False,
            'daily_note_created': False,
            'errors': 0
        }
        
        try:
            # Process new articles
            process_stats = self.process_new_articles(auto_approve)
            stats['new_articles'] = process_stats['total']
            stats['approved'] = process_stats['approved']
            stats['imported'] = process_stats['imported']
            stats['errors'] = process_stats['errors']
            
            # Create daily note
            daily_note_path = self.create_daily_note()
            stats['daily_note_created'] = bool(daily_note_path)
            
            # Update digital garden
            if self.digital_garden_path:
                stats['digital_garden_updated'] = self.update_digital_garden()
            
            logger.info(f"Completed workflow: {stats}")
            return stats
        
        except Exception as e:
            logger.error(f"Error running complete workflow: {e}")
            return stats
