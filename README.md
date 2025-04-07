# AI Governance Content Aggregator

A comprehensive system for aggregating, reviewing, and publishing AI Governance content from around the world in multiple languages.

## Overview

The AI Governance Content Aggregator is a complete solution that:

1. **Automatically monitors** top sources of AI Governance content across journalism, international organizations, NGOs, governments, and academia
2. **Supports multiple languages** including English variants, Chinese, Japanese, Russian, and Spanish
3. **Provides a staging area** for content review before publishing
4. **Integrates with Obsidian** for content organization and annotation
5. **Publishes as a digital garden** with a clean, minimalist design and tag-based navigation

This system creates an automated pipeline from content discovery to publishing, while maintaining human review to ensure quality and relevance.

## System Architecture

The system consists of several integrated components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  RSS Monitoring │────▶│  Staging Area   │────▶│    Obsidian     │────▶│  Digital Garden │
│     System      │     │                 │     │  Integration    │     │     Website     │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. **RSS Monitoring System**: Fetches content from configured sources and filters for AI Governance relevance
2. **Staging Area**: Holds content for review before importing into Obsidian
3. **Obsidian Integration**: Organizes content in a structured vault with templates and metadata
4. **Digital Garden Website**: Presents the content in a clean, minimalist design with tag-based navigation

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- Obsidian (desktop application)
- Obsidian Digital Garden plugin

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/hxfxrx/AI-Governance-aggregator.git
   cd AI-Governance-aggregator
   ```

2. Install required Python packages:
   ```bash
   pip install feedparser requests beautifulsoup4 markdown tabulate
   ```

3. Configure the system:
   ```bash
   # Create configuration directory if it doesn't exist
   mkdir -p config
   
   # Edit the configuration file
   # You can use the default configuration or customize it
   nano config/pipeline.json
   ```

4. Set up the directory structure:
   ```bash
   python scripts/content_pipeline.py setup
   ```

## Usage

### Running the Content Pipeline

The content pipeline can be run in several modes:

1. **Complete Pipeline**: Runs the entire pipeline from RSS monitoring to digital garden generation
   ```bash
   python scripts/content_pipeline.py run
   ```

2. **RSS Monitoring Only**: Only fetches new content from RSS feeds
   ```bash
   python scripts/rss_cli.py
   ```

3. **Staging Management**: Manage content in the staging area
   ```bash
   python scripts/staging_cli.py list  # List new articles
   python scripts/staging_cli.py approve <article_id>  # Approve an article
   python scripts/staging_cli.py reject <article_id>  # Reject an article
   ```

4. **Obsidian Integration**: Import approved content into Obsidian
   ```bash
   python scripts/obsidian_cli.py import  # Import all approved articles
   ```

5. **Digital Garden Generation**: Generate the digital garden website
   ```bash
   python scripts/content_pipeline.py generate
   ```

6. **GitHub Pages Deployment**: Deploy the digital garden to GitHub Pages
   ```bash
   python scripts/content_pipeline.py deploy
   ```

### Automated Workflow

For a fully automated workflow, you can set up a cron job to run the pipeline at regular intervals:

```bash
# Run the pipeline every hour
0 * * * * cd /path/to/AI-Governance-aggregator && python scripts/content_pipeline.py run
```

## Configuration

The system is configured through the `config/pipeline.json` file:

```json
{
  "staging_dir": "/path/to/staging",
  "obsidian_vault_path": "/path/to/obsidian-vault",
  "digital_garden_path": "/path/to/digital-garden",
  "github_pages_repo": "https://github.com/username/repo.git",
  "auto_approve": false,
  "auto_publish": true,
  "run_interval": 3600
}
```

- `staging_dir`: Directory for the staging area
- `obsidian_vault_path`: Path to your Obsidian vault
- `digital_garden_path`: Directory for the generated digital garden website
- `github_pages_repo`: GitHub repository URL for deployment
- `auto_approve`: Whether to automatically approve all new articles (not recommended)
- `auto_publish`: Whether to automatically publish to GitHub Pages
- `run_interval`: Interval in seconds between pipeline runs

### RSS Feed Configuration

RSS feeds are configured in `scripts/rss_monitor/core.py`. The default configuration includes feeds from:

- **Journalism**: The New York Times, MIT Technology Review, WIRED
- **International Organizations**: UNESCO, World Economic Forum
- **Academic Sources**: Centre for the Governance of AI, Stanford HAI

You can add or remove feeds by editing the `RSS_FEEDS` list in this file.

### AI Governance Keywords

The system filters content based on keywords related to AI governance. These are configured in the `AI_GOVERNANCE_KEYWORDS` list in `scripts/rss_monitor/core.py`. The default configuration includes keywords in multiple languages:

- English: "ai governance", "artificial intelligence governance", etc.
- Spanish: "gobernanza de la ia", "gobernanza de la inteligencia artificial"
- Chinese: "人工智能治理", "人工智能监管"
- Japanese: "AI ガバナンス", "人工知能ガバナンス"
- Russian: "управление ии", "регулирование искусственного интеллекта"

## Digital Garden Website

The digital garden website is a static site with a clean, minimalist design. It features:

- **Tag-based navigation**: Filter content by tags
- **Highlighted key points**: Important information is highlighted
- **Multiple language support**: Content in English, Chinese, Japanese, Russian, and Spanish
- **Responsive design**: Works on desktop and mobile devices

### Customizing the Website

The website can be customized by editing the files in the `digital-garden` directory:

- `css/style.css`: Styling for the website
- `js/main.js`: JavaScript functionality
- `templates/`: HTML templates for different page types

## Obsidian Integration

The system integrates with Obsidian by:

1. Creating a structured vault with directories for different content categories
2. Providing templates for articles and daily notes
3. Setting up metadata for easy filtering and searching
4. Supporting the Digital Garden plugin for publishing

### Obsidian Digital Garden Plugin

To publish the content as a digital garden, you need to install the [Digital Garden plugin](https://github.com/oleeskild/obsidian-digital-garden) in Obsidian and configure it to point to your GitHub repository.

## Testing

The system includes a comprehensive test suite to verify all components:

```bash
# Run all tests
python tests/test_workflow.py

# Run specific tests
python tests/test_workflow.py --test setup
python tests/test_workflow.py --test rss
python tests/test_workflow.py --test workflow
python tests/test_workflow.py --test digital-garden
python tests/test_workflow.py --test pipeline
```

## Directory Structure

```
AI-Governance-aggregator/
├── config/                  # Configuration files
├── digital-garden/          # Generated digital garden website
│   ├── css/                 # CSS styles
│   ├── js/                  # JavaScript files
│   ├── articles/            # Generated article pages
│   └── index.html           # Main page
├── obsidian-integration/    # Obsidian vault
│   ├── AI Governance/       # Content categories
│   ├── Templates/           # Note templates
│   └── Daily Notes/         # Daily summaries
├── research/                # Research on AI Governance sources
├── scripts/                 # Python scripts
│   ├── rss_monitor/         # RSS monitoring system
│   ├── obsidian_integration/# Obsidian integration
│   ├── content_pipeline.py  # Main pipeline script
│   ├── rss_cli.py           # CLI for RSS monitoring
│   ├── staging_cli.py       # CLI for staging area
│   └── obsidian_cli.py      # CLI for Obsidian integration
├── staging/                 # Staging area for content review
│   ├── new/                 # New articles
│   ├── reviewed/            # Approved articles
│   ├── rejected/            # Rejected articles
│   └── metadata/            # Article metadata
└── tests/                   # Test suite
```

## Workflow

The typical workflow for the system is:

1. **Content Discovery**: The RSS monitoring system fetches content from configured sources and filters for AI Governance relevance
2. **Content Review**: New articles are placed in the staging area for review
3. **Approval Process**: Articles are approved or rejected through the staging CLI
4. **Obsidian Import**: Approved articles are imported into Obsidian with proper formatting and metadata
5. **Digital Garden Generation**: The digital garden website is generated from the Obsidian content
6. **Deployment**: The website is deployed to GitHub Pages

## Troubleshooting

### Common Issues

1. **RSS feeds not updating**: Check internet connectivity and feed URLs
2. **Staging area empty**: Verify that the RSS monitoring system is running and finding relevant content
3. **Obsidian import failing**: Ensure Obsidian is not running when importing content
4. **Digital garden not generating**: Check file permissions and paths in configuration
5. **GitHub Pages deployment failing**: Verify GitHub repository URL and access permissions

### Logs

The system generates logs for each component:

- `rss_monitor.log`: RSS monitoring system logs
- `staging.log`: Staging area logs
- `obsidian_integration.log`: Obsidian integration logs
- `pipeline.log`: Full pipeline logs
- `test_workflow.log`: Test logs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Obsidian](https://obsidian.md/) for the knowledge management system
- [Obsidian Digital Garden](https://github.com/oleeskild/obsidian-digital-garden) for the publishing plugin
- All the sources of AI Governance content that make this aggregator valuable
