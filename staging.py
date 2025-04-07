"""
Staging area management for the RSS feed monitoring system.
Handles the workflow for reviewing and processing content in the staging area.
"""

import os
import json
import shutil
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'rss_monitor.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('staging_manager')

def list_new_articles():
    """
    List all new articles in the staging area.
    
    Returns:
        list: A list of dictionaries containing article metadata
    """
    articles = []
    staging_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
    metadata_dir = os.path.join(staging_dir, 'metadata')
    new_dir = os.path.join(staging_dir, 'new')
    
    # Create directories if they don't exist
    os.makedirs(metadata_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)
    
    # Get all metadata files for articles in the new directory
    if os.path.exists(new_dir):
        for filename in os.listdir(new_dir):
            if filename.endswith('.md'):
                article_id = filename[:-3]  # Remove .md extension
                metadata_path = os.path.join(metadata_dir, f"{article_id}.json")
                
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            articles.append(metadata)
                    except Exception as e:
                        logger.error(f"Error reading metadata for {article_id}: {e}")
    
    # Sort by date, newest first
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)
    return articles

def approve_article(article_id):
    """
    Approve an article and move it to the reviewed directory.
    
    Args:
        article_id (str): The ID of the article to approve
        
    Returns:
        bool: True if the article was approved successfully, False otherwise
    """
    try:
        staging_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
        new_path = os.path.join(staging_dir, 'new', f"{article_id}.md")
        reviewed_path = os.path.join(staging_dir, 'reviewed', f"{article_id}.md")
        
        # Create reviewed directory if it doesn't exist
        os.makedirs(os.path.join(staging_dir, 'reviewed'), exist_ok=True)
        
        if not os.path.exists(new_path):
            logger.error(f"Article {article_id} not found in new directory")
            return False
        
        # Move the file
        shutil.move(new_path, reviewed_path)
        
        # Update metadata
        metadata_path = os.path.join(staging_dir, 'metadata', f"{article_id}.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            metadata['status'] = 'approved'
            metadata['approved_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Article {article_id} approved and moved to reviewed directory")
        return True
    
    except Exception as e:
        logger.error(f"Error approving article {article_id}: {e}")
        return False

def reject_article(article_id):
    """
    Reject an article and move it to the rejected directory.
    
    Args:
        article_id (str): The ID of the article to reject
        
    Returns:
        bool: True if the article was rejected successfully, False otherwise
    """
    try:
        staging_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
        new_path = os.path.join(staging_dir, 'new', f"{article_id}.md")
        rejected_path = os.path.join(staging_dir, 'rejected', f"{article_id}.md")
        
        # Create rejected directory if it doesn't exist
        os.makedirs(os.path.join(staging_dir, 'rejected'), exist_ok=True)
        
        if not os.path.exists(new_path):
            logger.error(f"Article {article_id} not found in new directory")
            return False
        
        # Move the file
        shutil.move(new_path, rejected_path)
        
        # Update metadata
        metadata_path = os.path.join(staging_dir, 'metadata', f"{article_id}.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            metadata['status'] = 'rejected'
            metadata['rejected_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Article {article_id} rejected and moved to rejected directory")
        return True
    
    except Exception as e:
        logger.error(f"Error rejecting article {article_id}: {e}")
        return False

def export_to_obsidian(article_id=None):
    """
    Export approved articles to Obsidian.
    
    Args:
        article_id (str, optional): The ID of a specific article to export.
            If None, all approved articles will be exported.
            
    Returns:
        dict: Statistics about the export process
    """
    stats = {
        'exported': 0,
        'errors': 0,
        'articles': []
    }
    
    try:
        staging_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
        obsidian_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'obsidian-integration')
        
        # Create Obsidian directory if it doesn't exist
        os.makedirs(obsidian_dir, exist_ok=True)
        
        reviewed_dir = os.path.join(staging_dir, 'reviewed')
        metadata_dir = os.path.join(staging_dir, 'metadata')
        
        # Create reviewed directory if it doesn't exist
        os.makedirs(reviewed_dir, exist_ok=True)
        
        # Get list of articles to export
        if article_id:
            articles = [f"{article_id}.md"]
        else:
            if os.path.exists(reviewed_dir):
                articles = [f for f in os.listdir(reviewed_dir) if f.endswith('.md')]
            else:
                articles = []
        
        # Export each article
        for article_file in articles:
            try:
                article_id = article_file[:-3]  # Remove .md extension
                source_path = os.path.join(reviewed_dir, article_file)
                
                # Get metadata
                metadata_path = os.path.join(metadata_dir, f"{article_id}.json")
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                else:
                    logger.warning(f"Metadata not found for {article_id}, using default values")
                    metadata = {
                        'title': article_id,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'category': 'unknown'
                    }
                
                # Create category directory if it doesn't exist
                category_dir = os.path.join(obsidian_dir, metadata.get('category', 'uncategorized'))
                os.makedirs(category_dir, exist_ok=True)
                
                # Format the destination filename
                date_str = metadata.get('date', '').split(' ')[0]  # Get just the date part
                if not date_str:
                    date_str = datetime.now().strftime('%Y-%m-%d')
                
                # Clean the title for use in a filename
                title = metadata.get('title', article_id)
                clean_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in title)
                clean_title = clean_title.strip()
                
                dest_filename = f"{date_str} - {clean_title}.md"
                dest_path = os.path.join(category_dir, dest_filename)
                
                # Copy the file
                with open(source_path, 'r', encoding='utf-8') as src:
                    content = src.read()
                
                with open(dest_path, 'w', encoding='utf-8') as dest:
                    dest.write(content)
                
                # Update metadata
                metadata['exported_to_obsidian'] = True
                metadata['export_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                metadata['obsidian_path'] = dest_path
                
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Exported article {article_id} to {dest_path}")
                stats['exported'] += 1
                stats['articles'].append({
                    'id': article_id,
                    'title': metadata.get('title', ''),
                    'path': dest_path
                })
            
            except Exception as e:
                logger.error(f"Error exporting article {article_file}: {e}")
                stats['errors'] += 1
        
        return stats
    
    except Exception as e:
        logger.error(f"Error in export_to_obsidian: {e}")
        return stats

def get_staging_stats():
    """
    Get statistics about the staging area.
    
    Returns:
        dict: Statistics about the staging area
    """
    stats = {
        'new': 0,
        'reviewed': 0,
        'rejected': 0,
        'total': 0,
        'by_category': {},
        'by_language': {},
        'by_source': {}
    }
    
    try:
        staging_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'staging')
        
        # Create directories if they don't exist
        os.makedirs(os.path.join(staging_dir, 'new'), exist_ok=True)
        os.makedirs(os.path.join(staging_dir, 'reviewed'), exist_ok=True)
        os.makedirs(os.path.join(staging_dir, 'rejected'), exist_ok=True)
        os.makedirs(os.path.join(staging_dir, 'metadata'), exist_ok=True)
        
        # Count files in each directory
        if os.path.exists(os.path.join(staging_dir, 'new')):
            stats['new'] = len([f for f in os.listdir(os.path.join(staging_dir, 'new')) if f.endswith('.md')])
        
        if os.path.exists(os.path.join(staging_dir, 'reviewed')):
            stats['reviewed'] = len([f for f in os.listdir(os.path.join(staging_dir, 'reviewed')) if f.endswith('.md')])
        
        if os.path.exists(os.path.join(staging_dir, 'rejected')):
            stats['rejected'] = len([f for f in os.listdir(os.path.join(staging_dir, 'rejected')) if f.endswith('.md')])
        
        stats['total'] = stats['new'] + stats['reviewed'] + stats['rejected']
        
        # Analyze metadata
        metadata_dir = os.path.join(staging_dir, 'metadata')
        if os.path.exists(metadata_dir):
            for filename in os.listdir(metadata_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(metadata_dir, filename), 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        
                        # Count by category
                        category = metadata.get('category', 'unknown')
                        stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
                        
                        # Count by language
                        language = metadata.get('language', 'unknown')
                        stats['by_language'][language] = stats['by_language'].get(language, 0) + 1
                        
                        # Count by source
                        source = metadata.get('source', 'unknown')
                        stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
                    
                    except Exception as e:
                        logger.error(f"Error reading metadata file {filename}: {e}")
        
        return stats
    
    except Exception as e:
        logger.error(f"Error in get_staging_stats: {e}")
        return stats
