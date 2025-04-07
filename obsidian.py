"""
Obsidian integration module for the AI Governance content aggregator.
Handles the formatting and preparation of content for Obsidian and Digital Garden publishing.
"""

import os
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'obsidian_integration.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('obsidian_integration')

class ObsidianIntegration:
    """Class to handle integration with Obsidian for digital garden publishing."""
    
    def __init__(self, obsidian_vault_path, digital_garden_path=None):
        """
        Initialize the Obsidian integration.
        
        Args:
            obsidian_vault_path (str): Path to the Obsidian vault
            digital_garden_path (str, optional): Path to the digital garden directory
        """
        self.obsidian_vault_path = Path(obsidian_vault_path)
        self.digital_garden_path = Path(digital_garden_path) if digital_garden_path else None
        
        # Create directories if they don't exist
        self.obsidian_vault_path.mkdir(parents=True, exist_ok=True)
        
        # Create standard Obsidian directories
        (self.obsidian_vault_path / "AI Governance").mkdir(exist_ok=True)
        (self.obsidian_vault_path / "Templates").mkdir(exist_ok=True)
        
        # Create category directories
        categories = [
            "Journalism", 
            "International Organizations", 
            "NGOs", 
            "Government", 
            "Academic",
            "Chinese Sources",
            "Japanese Sources",
            "Russian Sources",
            "Spanish Sources"
        ]
        
        for category in categories:
            (self.obsidian_vault_path / "AI Governance" / category).mkdir(exist_ok=True)
        
        logger.info(f"Initialized Obsidian integration with vault at {self.obsidian_vault_path}")
    
    def create_templates(self):
        """Create standard templates for Obsidian notes."""
        templates = {
            "article_template.md": """---
title: {{title}}
source: {{source}}
url: {{url}}
date: {{date}}
language: {{language}}
category: {{category}}
tags: [ai-governance, {{tags}}]
---

# {{title}}

**Source**: {{source}}  
**Date**: {{date}}  
**URL**: {{url}}  
**Language**: {{language}}  
**Category**: {{category}}

## Summary

{{summary}}

## Content

{{content}}

## Notes

{{notes}}
""",
            "daily_note_template.md": """---
date: {{date}}
tags: [daily-note]
---

# {{date}}

## New AI Governance Content

{{content_list}}

## Tasks

- [ ] Review new articles
- [ ] Update digital garden
- [ ] Research on {{research_topic}}

## Notes

{{notes}}
"""
        }
        
        templates_dir = self.obsidian_vault_path / "Templates"
        
        for filename, content in templates.items():
            file_path = templates_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Created template: {file_path}")
    
    def create_obsidian_config(self):
        """Create basic Obsidian configuration files."""
        # Create .obsidian directory
        obsidian_config_dir = self.obsidian_vault_path / ".obsidian"
        obsidian_config_dir.mkdir(exist_ok=True)
        
        # Create basic config.json
        config = {
            "baseFontSize": 16,
            "theme": "obsidian",
            "translucency": False,
            "enabledPlugins": [
                "obsidian-git",
                "obsidian-digital-garden",
                "dataview"
            ],
            "newFileLocation": "folder",
            "newFileFolderPath": "AI Governance",
            "attachmentFolderPath": "Attachments",
            "userIgnoreFilters": [
                "Attachments/"
            ],
            "alwaysUpdateLinks": True
        }
        
        config_path = obsidian_config_dir / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Created Obsidian config: {config_path}")
        
        # Create appearance.json
        appearance = {
            "theme": "obsidian",
            "baseFontSize": 16,
            "translucency": False,
            "accentColor": "#7B68EE"
        }
        
        appearance_path = obsidian_config_dir / "appearance.json"
        with open(appearance_path, 'w', encoding='utf-8') as f:
            json.dump(appearance, f, indent=2)
        
        logger.info(f"Created Obsidian appearance config: {appearance_path}")
    
    def create_digital_garden_config(self):
        """Create configuration for the Digital Garden plugin."""
        if not self.digital_garden_path:
            logger.warning("Digital garden path not set, skipping digital garden config creation")
            return
        
        # Create digital garden directory if it doesn't exist
        self.digital_garden_path.mkdir(parents=True, exist_ok=True)
        
        # Create digital garden config
        digital_garden_config = {
            "githubRepo": "ai-governance-digital-garden",
            "githubToken": "",
            "githubUserName": "",
            "gardenBaseUrl": "",
            "prHistory": [],
            "theme": "dark",
            "baseTheme": "dark",
            "siteName": "AI Governance Digital Garden",
            "siteBaseUrl": "",
            "defaultNoteSettings": {
                "dgHomeLink": True,
                "dgPassFrontmatter": False,
                "dgShowBacklinks": True,
                "dgShowLocalGraph": True,
                "dgShowInlineTitle": True,
                "dgShowFileTree": True,
                "dgEnableSearch": True,
                "dgShowToc": True,
                "dgLinkPreview": True,
                "dgShowTags": True
            }
        }
        
        # Create .obsidian/plugins/obsidian-digital-garden directory
        plugin_dir = self.obsidian_vault_path / ".obsidian" / "plugins" / "obsidian-digital-garden"
        plugin_dir.mkdir(parents=True, exist_ok=True)
        
        # Save digital garden config
        config_path = plugin_dir / "data.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(digital_garden_config, f, indent=2)
        
        logger.info(f"Created Digital Garden plugin config: {config_path}")
    
    def import_article(self, article_path, category=None):
        """
        Import an article from the staging area into Obsidian.
        
        Args:
            article_path (str): Path to the article markdown file
            category (str, optional): Category to place the article in
            
        Returns:
            str: Path to the imported article in Obsidian
        """
        try:
            article_path = Path(article_path)
            
            # Read the article content
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter = {}
            frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter_text = frontmatter_match.group(1)
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
            
            # Determine category
            if not category:
                category = frontmatter.get('category', 'Uncategorized')
            
            # Map category to Obsidian directory
            category_mapping = {
                'journalism': 'Journalism',
                'international_org': 'International Organizations',
                'ngo': 'NGOs',
                'government': 'Government',
                'academic': 'Academic',
                'zh-cn': 'Chinese Sources',
                'ja': 'Japanese Sources',
                'ru': 'Russian Sources',
                'es': 'Spanish Sources'
            }
            
            obsidian_category = category_mapping.get(category, category)
            
            # Create target directory if it doesn't exist
            target_dir = self.obsidian_vault_path / "AI Governance" / obsidian_category
            target_dir.mkdir(exist_ok=True)
            
            # Generate filename
            title = frontmatter.get('title', article_path.stem)
            date = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Clean title for filename
            clean_title = re.sub(r'[^\w\s-]', '', title)
            clean_title = re.sub(r'[\s]+', ' ', clean_title).strip()
            clean_title = clean_title.replace(' ', '-')
            
            # Create filename with date prefix
            if ' ' in date:
                date = date.split(' ')[0]  # Get just the date part
            
            filename = f"{date} - {clean_title}.md"
            target_path = target_dir / filename
            
            # Copy the file
            shutil.copy2(article_path, target_path)
            
            logger.info(f"Imported article from {article_path} to {target_path}")
            return str(target_path)
        
        except Exception as e:
            logger.error(f"Error importing article {article_path}: {e}")
            return None
    
    def batch_import(self, source_dir, category_mapping=None):
        """
        Import multiple articles from a directory.
        
        Args:
            source_dir (str): Directory containing articles to import
            category_mapping (dict, optional): Mapping of article IDs to categories
            
        Returns:
            dict: Statistics about the import process
        """
        stats = {
            'total': 0,
            'imported': 0,
            'errors': 0,
            'articles': []
        }
        
        try:
            source_dir = Path(source_dir)
            
            # Get all markdown files
            markdown_files = list(source_dir.glob('*.md'))
            stats['total'] = len(markdown_files)
            
            for file_path in markdown_files:
                try:
                    article_id = file_path.stem
                    category = None
                    
                    if category_mapping and article_id in category_mapping:
                        category = category_mapping[article_id]
                    
                    imported_path = self.import_article(file_path, category)
                    
                    if imported_path:
                        stats['imported'] += 1
                        stats['articles'].append({
                            'id': article_id,
                            'source': str(file_path),
                            'destination': imported_path
                        })
                    else:
                        stats['errors'] += 1
                
                except Exception as e:
                    logger.error(f"Error importing {file_path}: {e}")
                    stats['errors'] += 1
            
            return stats
        
        except Exception as e:
            logger.error(f"Error in batch_import: {e}")
            return stats
    
    def create_index_note(self):
        """
        Create an index note for the AI Governance vault.
        
        Returns:
            str: Path to the created index note
        """
        try:
            index_content = """---
title: AI Governance Index
tags: [index, ai-governance]
---

# AI Governance Digital Garden

Welcome to the AI Governance Digital Garden. This is a collection of curated content about AI Governance from around the world.

## Categories

### By Source Type

- [[Journalism Sources]]
- [[International Organizations]]
- [[NGOs]]
- [[Government Sources]]
- [[Academic Sources]]

### By Language

- [[English Sources]]
- [[Chinese Sources]]
- [[Japanese Sources]]
- [[Russian Sources]]
- [[Spanish Sources]]

## Recent Additions

```dataview
TABLE source, date, category
FROM "AI Governance"
SORT date DESC
LIMIT 10
```

## Tags

- #ai-governance
- #ai-ethics
- #ai-regulation
- #ai-policy
"""
            
            index_path = self.obsidian_vault_path / "AI Governance" / "AI Governance Index.md"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logger.info(f"Created index note at {index_path}")
            return str(index_path)
        
        except Exception as e:
            logger.error(f"Error creating index note: {e}")
            return None
    
    def setup_complete_vault(self):
        """
        Set up a complete Obsidian vault with all necessary configurations and templates.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            # Create templates
            self.create_templates()
            
            # Create Obsidian config
            self.create_obsidian_config()
            
            # Create Digital Garden config if path is set
            if self.digital_garden_path:
                self.create_digital_garden_config()
            
            # Create index note
            self.create_index_note()
            
            # Create category index notes
            categories = [
                ("Journalism", "Journalism Sources"),
                ("International Organizations", "International Organizations"),
                ("NGOs", "NGO Sources"),
                ("Government", "Government Sources"),
                ("Academic", "Academic Sources"),
                ("Chinese Sources", "Chinese Sources"),
                ("Japanese Sources", "Japanese Sources"),
                ("Russian Sources", "Russian Sources"),
                ("Spanish Sources", "Spanish Sources")
            ]
            
            for folder_name, title in categories:
                category_path = self.obsidian_vault_path / "AI Governance" / folder_name / f"{title}.md"
                
                category_content = f"""---
title: {title}
tags: [index, ai-governance, {folder_name.lower().replace(' ', '-')}]
---

# {title}

This is an index of AI Governance content from {title}.

## Recent Articles

```dataview
TABLE source, date
FROM "AI Governance/{folder_name}"
SORT date DESC
```
"""
                
                with open(category_path, 'w', encoding='utf-8') as f:
                    f.write(category_content)
                
                logger.info(f"Created category index note at {category_path}")
            
            logger.info("Completed Obsidian vault setup")
            return True
        
        except Exception as e:
            logger.error(f"Error setting up complete vault: {e}")
            return False
