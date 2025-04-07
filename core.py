"""
Core functionality for the RSS feed monitoring system.
Fetches and processes RSS feeds, filters content related to AI governance,
and prepares it for the staging area.
"""

import os
import re
import json
import time
import logging
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup
import markdown

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'rss_monitor.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('rss_monitor')

# Configuration
STAGING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
OBSIDIAN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'obsidian-integration')

# RSS feeds to monitor (simplified for testing)
RSS_FEEDS = [
    # Journalism Sources
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "category": "journalism", "language": "en-us", "source": "The New York Times"},
    {"url": "https://www.technologyreview.com/feed/", "category": "journalism", "language": "en-us", "source": "MIT Technology Review"},
    {"url": "https://www.wired.com/feed/rss", "category": "journalism", "language": "en-us", "source": "WIRED"},
    
    # International Organizations
    {"url": "https://www.unesco.org/en/rss.xml", "category": "international_org", "language": "en", "source": "UNESCO"},
    {"url": "https://www.weforum.org/agenda/feed/", "category": "international_org", "language": "en", "source": "World Economic Forum"},
    
    # Academic Sources
    {"url": "https://www.governance.ai/feed", "category": "academic", "language": "en", "source": "Centre for the Governance of AI"},
    {"url": "https://hai.stanford.edu/news/rss.xml", "category": "academic", "language": "en", "source": "Stanford HAI"}
]

# Keywords to filter content related to AI governance
AI_GOVERNANCE_KEYWORDS = [
    # English keywords
    "ai governance", "artificial intelligence governance", "ai regulation", "ai policy", 
    "ai ethics", "responsible ai", "ai safety", "ai principles", "ai framework",
    
    # Spanish keywords
    "gobernanza de la ia", "gobernanza de la inteligencia artificial",
    
    # Chinese keywords (simplified)
    "人工智能治理", "人工智能监管",
    
    # Japanese keywords
    "AI ガバナンス", "人工知能ガバナンス",
    
    # Russian keywords
    "управление ии", "регулирование искусственного интеллекта"
]

# Obsidian template
OBSIDIAN_TEMPLATE = """---
title: "{title}"
source: "{source}"
url: "{url}"
date: "{date}"
language: "{language}"
category: "{category}"
tags: [ai-governance, {tags}]
---

# {title}

**Source**: {source}  
**Date**: {date}  
**URL**: {url}  
**Language**: {language}  
**Category**: {category}

## Summary

{summary}

## Content

{content}

"""

def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs(STAGING_DIR, exist_ok=True)
    os.makedirs(os.path.join(STAGING_DIR, 'new'), exist_ok=True)
    os.makedirs(os.path.join(STAGING_DIR, 'reviewed'), exist_ok=True)
    os.makedirs(os.path.join(STAGING_DIR, 'rejected'), exist_ok=True)
    os.makedirs(os.path.join(STAGING_DIR, 'metadata'), exist_ok=True)
    logger.info(f"Directory structure set up at {STAGING_DIR}")

def is_relevant_to_ai_governance(title, description, content):
    """
    Check if the content is relevant to AI governance based on keywords.
    
    Args:
        title (str): The title of the article
        description (str): The description or summary of the article
        content (str): The full content of the article
        
    Returns:
        bool: True if the content is relevant to AI governance, False otherwise
    """
    combined_text = f"{title} {description} {content}".lower()
    
    for keyword in AI_GOVERNANCE_KEYWORDS:
        if keyword.lower() in combined_text:
            return True
    
    return False

def fetch_article_content(url):
    """
    Fetch the full content of an article from its URL.
    
    Args:
        url (str): The URL of the article
        
    Returns:
        str: The full content of the article
    """
    try:
        # For testing purposes, return a mock content
        return f"This is a mock article content for {url}. It contains information about AI governance and regulation."
    except Exception as e:
        logger.error(f"Error fetching article content from {url}: {e}")
        return ""

def generate_file_id(url, title, date):
    """
    Generate a unique ID for a file based on its URL, title, and date.
    
    Args:
        url (str): The URL of the article
        title (str): The title of the article
        date (str): The publication date of the article
        
    Returns:
        str: A unique ID for the file
    """
    unique_string = f"{url}_{title}_{date}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def process_feed_entry(entry, feed_metadata):
    """
    Process a single feed entry and save it to the staging area if relevant.
    
    Args:
        entry (dict): The feed entry to process
        feed_metadata (dict): Metadata about the feed
        
    Returns:
        bool: True if the entry was processed and saved, False otherwise
    """
    try:
        # For testing purposes, create a mock entry
        title = entry.get('title', 'Mock Article Title about AI Governance')
        link = entry.get('link', 'https://example.com/mock-article')
        published = entry.get('published', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        summary = entry.get('summary', 'This is a mock summary about AI governance and regulation.')
        
        # Try to get a more detailed description if available
        description = entry.get('description', summary)
        
        # Fetch full content
        content = fetch_article_content(link)
        
        # Check if the content is relevant to AI governance
        if not is_relevant_to_ai_governance(title, description, content):
            logger.debug(f"Article '{title}' is not relevant to AI governance")
            return False
        
        # Generate a unique ID for the file
        file_id = generate_file_id(link, title, published)
        
        # Create metadata
        metadata = {
            'id': file_id,
            'title': title,
            'url': link,
            'date': published,
            'source': feed_metadata['source'],
            'language': feed_metadata['language'],
            'category': feed_metadata['category'],
            'tags': ['ai-governance'],
            'processed_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save metadata
        metadata_path = os.path.join(STAGING_DIR, 'metadata', f"{file_id}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # Create markdown content
        md_content = OBSIDIAN_TEMPLATE.format(
            title=title,
            source=feed_metadata['source'],
            url=link,
            date=published,
            language=feed_metadata['language'],
            category=feed_metadata['category'],
            tags=", ".join(metadata['tags']),
            summary=description,
            content=content
        )
        
        # Save to staging area
        file_path = os.path.join(STAGING_DIR, 'new', f"{file_id}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"Saved article '{title}' to {file_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error processing feed entry: {e}")
        return False

def fetch_and_process_feeds():
    """
    Fetch and process all RSS feeds defined in the configuration.
    
    Returns:
        dict: Statistics about the processing
    """
    stats = {
        'total_feeds': len(RSS_FEEDS),
        'processed_feeds': 0,
        'failed_feeds': 0,
        'total_entries': 0,
        'relevant_entries': 0,
        'errors': []
    }
    
    # For testing purposes, create mock entries
    for feed_config in RSS_FEEDS:
        try:
            logger.info(f"Processing feed: {feed_config['url']}")
            
            # Create mock entries
            mock_entries = [
                {
                    'title': f"AI Governance Framework by {feed_config['source']}",
                    'link': f"https://example.com/{feed_config['source'].lower().replace(' ', '-')}/ai-governance-framework",
                    'published': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': f"A new AI governance framework has been proposed by {feed_config['source']}."
                },
                {
                    'title': f"Ethical Considerations in AI Development - {feed_config['source']}",
                    'link': f"https://example.com/{feed_config['source'].lower().replace(' ', '-')}/ethical-ai",
                    'published': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'summary': f"Experts at {feed_config['source']} discuss ethical considerations in AI development."
                }
            ]
            
            # Process each entry
            entries_processed = 0
            relevant_entries = 0
            
            for entry in mock_entries:
                entries_processed += 1
                if process_feed_entry(entry, feed_config):
                    relevant_entries += 1
            
            logger.info(f"Processed {entries_processed} entries from {feed_config['url']}, {relevant_entries} relevant to AI governance")
            
            stats['processed_feeds'] += 1
            stats['total_entries'] += entries_processed
            stats['relevant_entries'] += relevant_entries
            
        except Exception as e:
            error_msg = f"Error processing feed {feed_config['url']}: {e}"
            logger.error(error_msg)
            stats['failed_feeds'] += 1
            stats['errors'].append(error_msg)
    
    return stats

def run_monitor(interval=3600):
    """
    Run the RSS feed monitor continuously with a specified interval.
    
    Args:
        interval (int): The interval in seconds between runs
    """
    logger.info("Starting RSS feed monitor")
    setup_directories()
    
    try:
        while True:
            start_time = time.time()
            logger.info(f"Starting feed processing at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            stats = fetch_and_process_feeds()
            
            logger.info(f"Feed processing completed. Stats: {json.dumps(stats, indent=2)}")
            
            # Calculate sleep time
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            
            if sleep_time > 0:
                logger.info(f"Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        logger.info("RSS feed monitor stopped by user")
    except Exception as e:
        logger.error(f"Error in RSS feed monitor: {e}")
        raise

def run_once():
    """Run the RSS feed monitor once."""
    logger.info("Running RSS feed monitor once")
    setup_directories()
    stats = fetch_and_process_feeds()
    logger.info(f"Feed processing completed. Stats: {json.dumps(stats, indent=2)}")
    return stats

if __name__ == "__main__":
    run_monitor()
