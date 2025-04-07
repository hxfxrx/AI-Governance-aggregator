"""
Configuration file for RSS feed monitoring system.
Contains the list of RSS feeds to monitor and their metadata.
"""

# RSS feeds to monitor
RSS_FEEDS = [
    # Journalism Sources
    {"url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "category": "journalism", "language": "en-us", "source": "The New York Times"},
    {"url": "https://www.technologyreview.com/feed/", "category": "journalism", "language": "en-us", "source": "MIT Technology Review"},
    {"url": "https://www.wired.com/feed/rss", "category": "journalism", "language": "en-us", "source": "WIRED"},
    {"url": "https://www.theverge.com/rss/index.xml", "category": "journalism", "language": "en-us", "source": "The Verge"},
    {"url": "https://www.zdnet.com/news/rss.xml", "category": "journalism", "language": "en-us", "source": "ZDNet"},
    {"url": "https://www.bloomberg.com/feed/technology/rss", "category": "journalism", "language": "en-us", "source": "Bloomberg"},
    {"url": "https://www.cnbc.com/id/19854910/device/rss/rss.xml", "category": "journalism", "language": "en-us", "source": "CNBC"},
    {"url": "https://www.techrepublic.com/rssfeeds/articles/", "category": "journalism", "language": "en-us", "source": "TechRepublic"},
    {"url": "https://www.theatlantic.com/feed/all/", "category": "journalism", "language": "en-us", "source": "The Atlantic"},
    
    # International Organizations
    {"url": "https://www.unesco.org/en/rss.xml", "category": "international_org", "language": "en", "source": "UNESCO"},
    {"url": "https://www.weforum.org/agenda/feed/", "category": "international_org", "language": "en", "source": "World Economic Forum"},
    {"url": "https://iapp.org/feed/", "category": "international_org", "language": "en", "source": "IAPP"},
    {"url": "https://oecd.ai/en/feed", "category": "international_org", "language": "en", "source": "OECD AI Policy Observatory"},
    {"url": "https://carnegieendowment.org/rss/solr?query=artificial+intelligence", "category": "international_org", "language": "en", "source": "Carnegie Endowment"},
    {"url": "https://www.csis.org/analysis/rss.xml", "category": "international_org", "language": "en", "source": "CSIS"},
    {"url": "https://thefuturesociety.org/feed/", "category": "international_org", "language": "en", "source": "The Future Society"},
    {"url": "https://futureoflife.org/feed/", "category": "international_org", "language": "en", "source": "Future of Life Institute"},
    
    # Academic Sources
    {"url": "https://www.governance.ai/feed", "category": "academic", "language": "en", "source": "Centre for the Governance of AI"},
    {"url": "https://hai.stanford.edu/news/rss.xml", "category": "academic", "language": "en", "source": "Stanford HAI"},
    {"url": "https://www.nyu.edu/about/news-publications/news/rss.html", "category": "academic", "language": "en", "source": "NYU-KAIST AI Research"},
    {"url": "https://ainowinstitute.org/feed", "category": "academic", "language": "en", "source": "AI Now Institute"},
    {"url": "https://www.nature.com/subjects/artificial-intelligence.rss", "category": "academic", "language": "en", "source": "Nature: AI & Society"},
    {"url": "https://link.springer.com/search.rss?facet-content-type=Article&facet-journal-id=146&channel-name=AI+%26+SOCIETY", "category": "academic", "language": "en", "source": "AI & Society Journal"},
    
    # Multilingual Sources
    {"url": "https://www.globaltimes.cn/rss/index.xml", "category": "international", "language": "zh-cn", "source": "Global Times China"},
    {"url": "https://www.meti.go.jp/english/press/rss/index.rdf", "category": "government", "language": "ja", "source": "METI Japan"},
    {"url": "https://www.eldiario.es/rss/", "category": "journalism", "language": "es", "source": "El Diario"},
    {"url": "https://www.eleconomista.es/rss/rss-categoria.php?categoria=tecnologia", "category": "journalism", "language": "es", "source": "El Economista"},
]

# Keywords to filter content related to AI governance
AI_GOVERNANCE_KEYWORDS = [
    # English keywords
    "ai governance", "artificial intelligence governance", "ai regulation", "ai policy", 
    "ai ethics", "responsible ai", "ai safety", "ai principles", "ai framework",
    "algorithmic governance", "ai oversight", "ai transparency", "ai accountability",
    
    # Spanish keywords
    "gobernanza de la ia", "gobernanza de la inteligencia artificial", "regulación de la ia",
    "política de ia", "ética de la ia", "ia responsable", "seguridad de la ia",
    
    # Chinese keywords (simplified)
    "人工智能治理", "人工智能监管", "人工智能政策", "人工智能伦理", "负责任的人工智能",
    
    # Japanese keywords
    "AI ガバナンス", "人工知能ガバナンス", "AI 規制", "AI 政策", "AI 倫理",
    
    # Russian keywords
    "управление ии", "регулирование искусственного интеллекта", "политика ии", "этика ии"
]

# Configuration for the staging area
STAGING_DIR = "/home/ubuntu/ai-governance-aggregator/staging"

# Configuration for Obsidian integration
OBSIDIAN_DIR = "/home/ubuntu/ai-governance-aggregator/obsidian-integration"
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
