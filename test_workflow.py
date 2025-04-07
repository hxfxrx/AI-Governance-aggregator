#!/usr/bin/env python3
"""
Test script for the AI Governance content aggregation system.
This script tests the end-to-end workflow from RSS monitoring to digital garden publishing.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules from the project
from scripts.rss_monitor.core import run_once, setup_directories
from scripts.workflow_integration import WorkflowIntegration
from scripts.content_pipeline import ContentPipeline

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_workflow.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('test_workflow')

class WorkflowTester:
    """Class to test the end-to-end workflow of the AI Governance content aggregation system."""
    
    def __init__(self, config_path):
        """
        Initialize the workflow tester.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config_path = config_path
        self.load_config()
        
        # Set up paths
        self.project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Initialize content pipeline
        self.pipeline = ContentPipeline(config_path)
        
        logger.info(f"Initialized workflow tester with config from {config_path}")
    
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
    
    def test_setup(self):
        """
        Test the setup process.
        
        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            logger.info("Testing setup process...")
            
            # Set up the content pipeline
            setup_success = self.pipeline.setup()
            
            if setup_success:
                logger.info("Setup process completed successfully")
                return True
            else:
                logger.error("Setup process failed")
                return False
        
        except Exception as e:
            logger.error(f"Error testing setup process: {e}")
            return False
    
    def test_rss_monitoring(self):
        """
        Test the RSS monitoring system.
        
        Returns:
            bool: True if RSS monitoring was successful, False otherwise
        """
        try:
            logger.info("Testing RSS monitoring system...")
            
            # Run RSS monitoring once
            rss_stats = run_once()
            
            if rss_stats:
                logger.info(f"RSS monitoring completed successfully: {rss_stats}")
                return True
            else:
                logger.error("RSS monitoring failed")
                return False
        
        except Exception as e:
            logger.error(f"Error testing RSS monitoring: {e}")
            return False
    
    def test_workflow_integration(self):
        """
        Test the workflow integration.
        
        Returns:
            bool: True if workflow integration was successful, False otherwise
        """
        try:
            logger.info("Testing workflow integration...")
            
            # Initialize workflow integration
            workflow = WorkflowIntegration(
                self.config['staging_dir'],
                self.config['obsidian_vault_path'],
                self.config['digital_garden_path']
            )
            
            # Run workflow integration
            workflow_stats = workflow.run_complete_workflow(auto_approve=True)
            
            if workflow_stats:
                logger.info(f"Workflow integration completed successfully: {workflow_stats}")
                return True
            else:
                logger.error("Workflow integration failed")
                return False
        
        except Exception as e:
            logger.error(f"Error testing workflow integration: {e}")
            return False
    
    def test_digital_garden_generation(self):
        """
        Test the digital garden generation.
        
        Returns:
            bool: True if digital garden generation was successful, False otherwise
        """
        try:
            logger.info("Testing digital garden generation...")
            
            # Generate digital garden
            generation_success = self.pipeline.generate_digital_garden()
            
            if generation_success:
                logger.info("Digital garden generation completed successfully")
                return True
            else:
                logger.error("Digital garden generation failed")
                return False
        
        except Exception as e:
            logger.error(f"Error testing digital garden generation: {e}")
            return False
    
    def test_full_pipeline(self):
        """
        Test the full content pipeline.
        
        Returns:
            bool: True if the full pipeline was successful, False otherwise
        """
        try:
            logger.info("Testing full content pipeline...")
            
            # Run the full pipeline
            pipeline_stats = self.pipeline.run_full_pipeline()
            
            if pipeline_stats and not pipeline_stats.get('errors'):
                logger.info(f"Full pipeline completed successfully: {pipeline_stats}")
                return True
            else:
                logger.error(f"Full pipeline failed: {pipeline_stats}")
                return False
        
        except Exception as e:
            logger.error(f"Error testing full pipeline: {e}")
            return False
    
    def run_all_tests(self):
        """
        Run all tests.
        
        Returns:
            dict: Results of all tests
        """
        results = {
            'setup': False,
            'rss_monitoring': False,
            'workflow_integration': False,
            'digital_garden_generation': False,
            'full_pipeline': False,
            'overall': False
        }
        
        try:
            # Test setup
            results['setup'] = self.test_setup()
            
            # Test RSS monitoring
            results['rss_monitoring'] = self.test_rss_monitoring()
            
            # Test workflow integration
            results['workflow_integration'] = self.test_workflow_integration()
            
            # Test digital garden generation
            results['digital_garden_generation'] = self.test_digital_garden_generation()
            
            # Test full pipeline
            results['full_pipeline'] = self.test_full_pipeline()
            
            # Overall result
            results['overall'] = all([
                results['setup'],
                results['rss_monitoring'],
                results['workflow_integration'],
                results['digital_garden_generation'],
                results['full_pipeline']
            ])
            
            logger.info(f"All tests completed: {results}")
            return results
        
        except Exception as e:
            logger.error(f"Error running all tests: {e}")
            results['overall'] = False
            return results

def main():
    """Main entry point for the workflow tester."""
    parser = argparse.ArgumentParser(description='AI Governance Workflow Tester')
    
    # Add arguments
    parser.add_argument('--config', default='/home/ubuntu/ai-governance-aggregator/config/pipeline.json', help='Path to configuration file')
    parser.add_argument('--test', choices=['setup', 'rss', 'workflow', 'digital-garden', 'pipeline', 'all'], default='all', help='Test to run')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize workflow tester
    tester = WorkflowTester(args.config)
    
    # Run the specified test
    if args.test == 'setup':
        success = tester.test_setup()
        print(f"Setup test {'succeeded' if success else 'failed'}")
    
    elif args.test == 'rss':
        success = tester.test_rss_monitoring()
        print(f"RSS monitoring test {'succeeded' if success else 'failed'}")
    
    elif args.test == 'workflow':
        success = tester.test_workflow_integration()
        print(f"Workflow integration test {'succeeded' if success else 'failed'}")
    
    elif args.test == 'digital-garden':
        success = tester.test_digital_garden_generation()
        print(f"Digital garden generation test {'succeeded' if success else 'failed'}")
    
    elif args.test == 'pipeline':
        success = tester.test_full_pipeline()
        print(f"Full pipeline test {'succeeded' if success else 'failed'}")
    
    else:  # 'all'
        results = tester.run_all_tests()
        
        print("\nTest Results:")
        print(f"Setup: {'✓' if results['setup'] else '✗'}")
        print(f"RSS Monitoring: {'✓' if results['rss_monitoring'] else '✗'}")
        print(f"Workflow Integration: {'✓' if results['workflow_integration'] else '✗'}")
        print(f"Digital Garden Generation: {'✓' if results['digital_garden_generation'] else '✗'}")
        print(f"Full Pipeline: {'✓' if results['full_pipeline'] else '✗'}")
        print(f"\nOverall: {'✓ PASSED' if results['overall'] else '✗ FAILED'}")
    
    return 0 if success or results.get('overall', False) else 1

if __name__ == '__main__':
    sys.exit(main())
