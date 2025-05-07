"""
Data Manager Module

This module handles all data-related operations including saving, loading, and managing hadith data.
"""

import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_dir="."):
        """
        Initialize the data manager
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.last_id_file = os.path.join(data_dir, 'last_processed_id.json')
        self.explanations_file = os.path.join(data_dir, 'all_hadiths_explanations2.json')
        self.successful_ids_file = os.path.join(data_dir, 'successful_hadith_ids2.json')
        
    def save_last_id(self, last_id):
        """Save the last processed ID"""
        with open(self.last_id_file, 'w', encoding='utf-8') as f:
            json.dump({'last_id': last_id}, f, ensure_ascii=False, indent=4)

    def load_last_id(self):
        """Load the last processed ID"""
        try:
            with open(self.last_id_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('last_id', 865)  # Start from 865 if no file exists
        except FileNotFoundError:
            return 865  # Start from 865 if no file exists

    def load_existing_data(self):
        """Load existing data"""
        try:
            with open(self.explanations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, all_explanations, successful_ids):
        """Save data to files"""
        # Save all explanations to JSON file
        with open(self.explanations_file, 'w', encoding='utf-8') as f:
            json.dump(all_explanations, f, ensure_ascii=False, indent=4)
        
        # Save successful hadith IDs
        with open(self.successful_ids_file, 'w', encoding='utf-8') as f:
            json.dump(successful_ids, f, ensure_ascii=False, indent=4)
            
    def create_backup(self):
        """Create a backup of current data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.data_dir, "hadith_backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = os.path.join(backup_dir, f"backup_before_recovery_{timestamp}.json")
        
        if os.path.exists(self.explanations_file):
            with open(self.explanations_file, 'r', encoding='utf-8') as src:
                data = json.load(src)
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    json.dump(data, dst, ensure_ascii=False, indent=4)
                    
        return backup_file 