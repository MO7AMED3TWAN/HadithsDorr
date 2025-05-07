"""
Hadith Crawler Module

This module handles the crawling of hadith explanations from the API.
"""

import requests
import time
from tqdm import tqdm
import json

class HadithCrawler:
    def __init__(self, server_manager, data_manager, max_id=88430, batch_size=70):
        """
        Initialize the hadith crawler
        
        Args:
            server_manager: Instance of ServerManager
            data_manager: Instance of DataManager
            max_id (int): Maximum hadith ID to process
            batch_size (int): Number of requests before server restart
        """
        self.server_manager = server_manager
        self.data_manager = data_manager
        self.max_id = max_id
        self.batch_size = batch_size
        
    def crawl_hadith_explanations(self):
        """Crawl hadith explanations"""
        all_explanations = self.data_manager.load_existing_data()
        start_id = self.data_manager.load_last_id() + 1
        
        # Load previous successful IDs if they exist
        try:
            with open(self.data_manager.successful_ids_file, 'r', encoding='utf-8') as f:
                successful_ids = json.load(f)
        except FileNotFoundError:
            successful_ids = []
        
        # Remove duplicates from successful IDs
        successful_ids = list(set(successful_ids))
        
        # Extract IDs from saved data
        existing_ids = [item['hadith_id'] for item in all_explanations]
        
        print(f"Starting process from hadith ID: {start_id}")
        print(f"Number of previously saved explanations: {len(all_explanations)}")
        print(f"Number of recorded successful hadiths: {len(successful_ids)}")
        
        # Ensure server is running before starting
        if not self.server_manager.test_server_health():
            print("❌ Server is not available, restarting before starting...")
            self.server_manager.restart_server()
        
        current_batch_count = 0
        found_count = 0
        skipped_count = 0
        failed_count = 0
        
        # Create progress bar
        total_ids = self.max_id - start_id + 1
        pbar = tqdm(total=total_ids, desc="Processing hadiths")
        
        def update_progress_bar(pbar, found, skipped, failed, current_id):
            pbar.set_postfix({
                'Found': found,
                'Skipped': skipped,
                'Failed': failed,
                'Current': current_id
            })
        
        for hadith_id in range(start_id, self.max_id + 1):
            try:
                if hadith_id in existing_ids:
                    skipped_count += 1
                    update_progress_bar(pbar, found_count, skipped_count, failed_count, hadith_id)
                    pbar.update(1)
                    continue
                
                response = requests.get(
                    f"{self.server_manager.base_url}/v1/site/sharh/{hadith_id}",
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data and isinstance(data, list) and len(data) > 0:
                        all_explanations.append({
                            'hadith_id': hadith_id,
                            'explanations': data
                        })
                        successful_ids.append(hadith_id)
                        found_count += 1
                    else:
                        failed_count += 1
                else:
                    failed_count += 1
                
                current_batch_count += 1
                
                # Save progress every 100 hadiths
                if current_batch_count % 100 == 0:
                    self.data_manager.save_data(all_explanations, successful_ids)
                    self.data_manager.save_last_id(hadith_id)
                
                # Restart server after batch_size requests
                if current_batch_count >= self.batch_size:
                    pbar.set_description(f"🔄 Restarting server ({len(all_explanations)} hadiths)")
                    
                    # Save data before restarting server
                    self.data_manager.save_data(all_explanations, successful_ids)
                    
                    self.server_manager.restart_server()
                    current_batch_count = 0
                    
                    # Reset progress bar description
                    pbar.set_description("Processing hadiths")
                
                update_progress_bar(pbar, found_count, skipped_count, failed_count, hadith_id)
                pbar.update(1)
                
            except Exception as e:
                failed_count += 1
                update_progress_bar(pbar, found_count, skipped_count, failed_count, hadith_id)
                
                # Try to restart server on error
                try:
                    self.server_manager.restart_server()
                    current_batch_count = 0
                except:
                    time.sleep(60)
                
                pbar.update(1)
                
                # Save last state anyway
                self.data_manager.save_last_id(hadith_id)
                self.data_manager.save_data(all_explanations, successful_ids)
        
        # Save final data
        self.data_manager.save_data(all_explanations, successful_ids)
        
        print(f"\n🔹 Total explanations found: {found_count}")
        print(f"🔹 Total hadiths skipped: {skipped_count}")
        print(f"🔹 Total hadiths failed to retrieve: {failed_count}")
        print("✅ Data saved to 'all_hadiths_explanations2.json'")
        print("✅ Successful IDs saved to 'successful_hadith_ids2.json'") 