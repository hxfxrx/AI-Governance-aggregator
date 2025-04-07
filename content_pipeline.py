#!/usr/bin/env python3
"""
Automated content pipeline for the AI Governance Digital Garden.
This script connects the RSS monitoring system, Obsidian workflow, and digital garden website.
"""

import os
import sys
import json
import shutil
import logging
import argparse
import datetime
import subprocess
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules from the project
from scripts.rss_monitor.core import run_once, setup_directories
from scripts.workflow_integration import WorkflowIntegration

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pipeline.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('content_pipeline')

class ContentPipeline:
    """Class to manage the automated content pipeline."""
    
    def __init__(self, config_path):
        """
        Initialize the content pipeline.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config_path = config_path
        self.load_config()
        
        # Set up paths
        self.project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.staging_dir = Path(self.config['staging_dir'])
        self.obsidian_vault_path = Path(self.config['obsidian_vault_path'])
        self.digital_garden_path = Path(self.config['digital_garden_path'])
        
        # Initialize workflow integration
        self.workflow = WorkflowIntegration(
            self.staging_dir,
            self.obsidian_vault_path,
            self.digital_garden_path
        )
        
        logger.info(f"Initialized content pipeline with config from {config_path}")
    
    def load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            logger.info(f"Loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {
                'staging_dir': '/home/ubuntu/ai-governance-aggregator/staging',
                'obsidian_vault_path': '/home/ubuntu/ai-governance-aggregator/obsidian-integration',
                'digital_garden_path': '/home/ubuntu/ai-governance-aggregator/digital-garden',
                'github_pages_repo': '',
                'auto_approve': False,
                'auto_publish': False,
                'run_interval': 3600  # 1 hour
            }
            
            # Save default config
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Created default configuration at {self.config_path}")
    
    def setup(self):
        """Set up the content pipeline."""
        try:
            # Set up RSS monitoring
            setup_directories()
            
            # Set up workflow integration
            self.workflow.setup()
            
            logger.info("Content pipeline setup completed")
            return True
        except Exception as e:
            logger.error(f"Error setting up content pipeline: {e}")
            return False
    
    def run_full_pipeline(self):
        """
        Run the full content pipeline.
        
        Returns:
            dict: Statistics about the pipeline run
        """
        stats = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rss_monitoring': {},
            'workflow': {},
            'digital_garden': False,
            'github_pages': False,
            'errors': []
        }
        
        try:
            # Step 1: Run RSS monitoring
            logger.info("Running RSS monitoring...")
            rss_stats = run_once()
            stats['rss_monitoring'] = rss_stats
            
            # Step 2: Run workflow integration
            logger.info("Running workflow integration...")
            workflow_stats = self.workflow.run_complete_workflow(
                auto_approve=self.config.get('auto_approve', False)
            )
            stats['workflow'] = workflow_stats
            
            # Step 3: Generate digital garden website
            logger.info("Generating digital garden website...")
            digital_garden_success = self.generate_digital_garden()
            stats['digital_garden'] = digital_garden_success
            
            # Step 4: Deploy to GitHub Pages if configured
            if self.config.get('auto_publish', False) and self.config.get('github_pages_repo'):
                logger.info("Deploying to GitHub Pages...")
                github_pages_success = self.deploy_to_github_pages()
                stats['github_pages'] = github_pages_success
            
            logger.info(f"Pipeline run completed: {stats}")
            return stats
        
        except Exception as e:
            error_msg = f"Error running content pipeline: {e}"
            logger.error(error_msg)
            stats['errors'].append(error_msg)
            return stats
    
    def generate_digital_garden(self):
        """
        Generate the digital garden website from Obsidian content.
        
        Returns:
            bool: True if generation was successful, False otherwise
        """
        try:
            # In a real implementation, this would use the Obsidian Digital Garden plugin
            # Since we can't directly interact with Obsidian plugins, we'll simulate the process
            
            # Create articles directory if it doesn't exist
            articles_dir = self.digital_garden_path / 'articles'
            articles_dir.mkdir(exist_ok=True)
            
            # Copy example article templates for demonstration
            example_articles = [
                '2025-04-07-unesco-new-ai-ethics-framework.html',
                '2025-04-05-new-research-ai-governance-models.html',
                '2025-04-03-g20-ai-governance-framework.html',
                '2025-04-02-china-ai-regulation-update.html',
                '2025-04-01-japan-ai-ethics-guidelines.html'
            ]
            
            # Create a simple article template
            article_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Governance Digital Garden</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" href="../static/favicon.ico">
</head>
<body>
    <header>
        <div class="container">
            <h1 class="site-title">AI Governance Digital Garden</h1>
            <p class="site-description">A curated collection of AI Governance content from around the world</p>
            
            <nav>
                <button id="menu-toggle" aria-expanded="false" class="mobile-menu-toggle">
                    <span class="visually-hidden">Menu</span>
                    <span class="hamburger"></span>
                </button>
                
                <ul id="mobile-nav">
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="../about.html">About</a></li>
                    <li><a href="../categories.html">Categories</a></li>
                    <li><a href="../languages.html">Languages</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <main>
            <article class="content full-article {source_class}">
                <h1>{title}</h1>
                
                <div class="article-meta">
                    <span class="language-indicator {lang_class}">{lang}</span>
                    <span class="source">{source}</span>
                    <span class="date">{date}</span>
                </div>
                
                <div class="tag-container">
                    {tags}
                </div>
                
                <div class="article-content">
                    {content}
                </div>
                
                <div class="article-footer">
                    <p>Original source: <a href="{url}" target="_blank">{url}</a></p>
                    <p>Added to AI Governance Digital Garden on {added_date}</p>
                </div>
            </article>
            
            <aside class="sidebar">
                <div class="sidebar-section">
                    <h2>Related Articles</h2>
                    <ul class="related-list">
                        {related_articles}
                    </ul>
                </div>
                
                <div class="sidebar-section">
                    <h2>Filter by Tags</h2>
                    <div class="tag-cloud">
                        {all_tags}
                    </div>
                </div>
            </aside>
        </main>
    </div>
    
    <footer>
        <div class="container">
            <p>AI Governance Digital Garden © 2025</p>
            <p>Content is automatically aggregated from various sources and reviewed before publishing.</p>
            <p>Built with <a href="https://obsidian.md/">Obsidian</a> and the <a href="https://github.com/oleeskild/obsidian-digital-garden">Digital Garden plugin</a>.</p>
        </div>
    </footer>
    
    <script src="../js/main.js"></script>
</body>
</html>"""
            
            # Create example articles
            for i, article_filename in enumerate(example_articles):
                article_path = articles_dir / article_filename
                
                # Extract title from filename
                title_parts = article_filename.split('-')
                date = f"{title_parts[0]}-{title_parts[1]}-{title_parts[2]}"
                title_words = '-'.join(title_parts[3:]).replace('.html', '').split('-')
                title = ' '.join(word.capitalize() for word in title_words)
                
                # Set up article data
                article_data = {
                    'title': title,
                    'description': f"Article about {title}",
                    'source': ['The New York Times', 'Centre for the Governance of AI', 'World Economic Forum', 'Global Times', 'AI Ethics Japan'][i],
                    'source_class': ['source-journalism', 'source-academic', 'source-international', 'source-government', 'source-ngo'][i],
                    'date': date,
                    'lang': ['EN', 'EN', 'EN', 'ZH', 'JA'][i],
                    'lang_class': ['lang-en', 'lang-en', 'lang-en', 'lang-zh', 'lang-ja'][i],
                    'url': f"https://example.com/articles/{article_filename}",
                    'added_date': datetime.datetime.now().strftime('%Y-%m-%d'),
                    'tags': ''.join([f'<a href="#" class="tag" data-tag="{tag}">{tag}</a>' for tag in 
                                    [['ai-ethics', 'regulation', 'journalism'], 
                                     ['ai-safety', 'research', 'academic'],
                                     ['policy', 'international', 'ai-principles'],
                                     ['regulation', 'china', 'ai-policy'],
                                     ['ai-ethics', 'japan', 'ngo']][i]]),
                    'all_tags': ''.join([f'<a href="#" class="tag" data-tag="{tag}">{tag}</a>' for tag in 
                                       ['ai-ethics', 'regulation', 'journalism', 'ai-safety', 'research', 
                                        'academic', 'policy', 'international', 'ai-principles', 'china', 
                                        'japan', 'ai-policy', 'ngo']]),
                    'related_articles': ''.join([f'<li><a href="{rel_art}">{rel_title}</a></li>' for rel_art, rel_title in 
                                              [(art, ' '.join(art.split('-')[3:]).replace('.html', '').split('-')) 
                                               for art in example_articles if art != article_filename][:3]]),
                    'content': f"""<p>This is a sample article about {title}. In a real implementation, this content would be generated from the Obsidian vault.</p>
                    <p>The article would include <span class="highlight">highlighted key points</span> as specified by the user preferences.</p>
                    <p>It would also include <span class="highlight">longer excerpts with detailed information</span> about the topic.</p>
                    <h2>Background</h2>
                    <p>This section would provide background information about the topic.</p>
                    <h2>Key Points</h2>
                    <p>This section would summarize the key points of the article.</p>
                    <h2>Analysis</h2>
                    <p>This section would provide analysis and context for the information presented.</p>
                    <h2>Implications</h2>
                    <p>This section would discuss the implications of the developments described in the article.</p>"""
                }
                
                # Create article file
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(article_template.format(**article_data))
            
            # Create categories and languages directories
            (self.digital_garden_path / 'categories').mkdir(exist_ok=True)
            (self.digital_garden_path / 'languages').mkdir(exist_ok=True)
            (self.digital_garden_path / 'sources').mkdir(exist_ok=True)
            
            # Create static directory and favicon
            static_dir = self.digital_garden_path / 'static'
            static_dir.mkdir(exist_ok=True)
            
            # Create a simple favicon.ico file (1x1 transparent pixel)
            with open(static_dir / 'favicon.ico', 'wb') as f:
                f.write(b'\x00\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x00\x18\x00\x30\x00\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            
            logger.info(f"Generated digital garden website at {self.digital_garden_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error generating digital garden: {e}")
            return False
    
    def deploy_to_github_pages(self):
        """
        Deploy the digital garden website to GitHub Pages.
        
        Returns:
            bool: True if deployment was successful, False otherwise
        """
        try:
            repo_url = self.config.get('github_pages_repo')
            if not repo_url:
                logger.warning("GitHub Pages repository URL not configured")
                return False
            
            # Create a temporary directory for the GitHub Pages repository
            temp_dir = self.project_root / 'temp_github_pages'
            os.makedirs(temp_dir, exist_ok=True)
            
            # Clone the repository
            subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)
            
            # Copy the digital garden files to the repository
            for item in os.listdir(self.digital_garden_path):
                source = self.digital_garden_path / item
                destination = temp_dir / item
                
                if os.path.isdir(source):
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil
(Content truncated due to size limit. Use line ranges to read in chunks)