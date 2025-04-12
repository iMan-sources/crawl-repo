import json
import csv
import os
from itemadapter import ItemAdapter
import logging

class JsonWriterPipeline:
    def __init__(self):
        self.file = None
        self.first_item = True
        self.item_count = 0
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        """Initialize the output file when the spider starts"""
        try:
            # Ensure the output directory exists
            output_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Open the file
            output_file = os.path.join(output_dir, 'github_repos.json')
            self.file = open(output_file, 'w', encoding='utf-8')
            self.file.write('[\n')  # Start JSON array
            self.first_item = True
            self.item_count = 0
            self.logger.info(f"Opened JSON output file: {output_file}")
        except Exception as e:
            self.logger.error(f"Error opening JSON file: {str(e)}")
            raise

    def close_spider(self, spider):
        """Close the output file when the spider finishes"""
        try:
            if self.file:
                self.file.write('\n]')  # End JSON array
                self.file.close()
                self.logger.info(f"JSON file closed. Processed {self.item_count} repositories.")
        except Exception as e:
            self.logger.error(f"Error closing JSON file: {str(e)}")
            raise

    def process_item(self, item, spider):
        """Process each item and write to JSON file"""
        try:
            self.item_count += 1
            
            # Convert to dict and ensure proper types
            item_dict = ItemAdapter(item).asdict()
            
            # Write to JSON with proper formatting
            line = json.dumps(item_dict, ensure_ascii=False)
            if not self.first_item:
                self.file.write(',\n')
            self.file.write(line)
            self.first_item = False
            
            # Flush the file to ensure data is written
            self.file.flush()
            
            return item
        except Exception as e:
            self.logger.error(f"Error processing item: {str(e)}")
            raise

class CsvWriterPipeline:
    def __init__(self):
        self.file = None
        self.writer = None
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        """Initialize the CSV file when the spider starts"""
        try:
            # Ensure the output directory exists
            output_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Open the file
            output_file = os.path.join(output_dir, 'github_repos.csv')
            self.file = open(output_file, 'w', newline='', encoding='utf-8')
            self.writer = None
            self.logger.info(f"Opened CSV output file: {output_file}")
        except Exception as e:
            self.logger.error(f"Error opening CSV file: {str(e)}")
            raise

    def close_spider(self, spider):
        """Close the CSV file when the spider finishes"""
        try:
            if self.file:
                self.file.close()
                self.logger.info("CSV file closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing CSV file: {str(e)}")
            raise

    def process_item(self, item, spider):
        """Process each item and write to CSV file"""
        try:
            item_dict = ItemAdapter(item).asdict()
            
            # Initialize writer with headers if this is the first item
            if self.writer is None:
                fieldnames = item_dict.keys()
                self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
                self.writer.writeheader()
            
            self.writer.writerow(item_dict)
            # Flush the file to ensure data is written
            self.file.flush()
            
            return item
        except Exception as e:
            self.logger.error(f"Error processing item for CSV: {str(e)}")
            raise 