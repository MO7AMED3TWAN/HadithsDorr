"""
This module contains the main HadithProcessor class that handles the processing of hadith texts.
It coordinates between API calls, file operations, and data transformations.
"""

from typing import List, Dict, Any, Tuple
import os
from .api_client import TogetherAPIClient
from .file_handler import FileHandler
from .utils import estimate_tokens, get_fixed_questions

class HadithProcessor:
    """
    Main class for processing hadith texts using the Together API.
    Handles the complete workflow of reading, processing, and saving hadith data.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the HadithProcessor with necessary components.
        
        Args:
            api_key (str): The Together API key
        """
        self.api_client = TogetherAPIClient(api_key)
        self.file_handler = FileHandler()
        self.fixed_questions = get_fixed_questions()

    def process_single_file(self, input_file: str, output_file: str) -> Tuple[int, int, int]:
        """
        Process a single hadith JSON file.

        Args:
            input_file (str): Path to input JSON file
            output_file (str): Path to save processed JSON file

        Returns:
            Tuple[int, int, int]: (processed_count, tokens_before, tokens_after)
        """
        # Load data
        data = self.file_handler.read_json(input_file)
        
        total_tokens_before = 0
        total_tokens_after = 0
        processed_count = 0

        # Process each hadith
        for entry in data:
            if not entry.get("sharh") or entry["sharh"] == ".":
                continue

            # Process the hadith
            processed = self.api_client.process_hadith(
                hadith=entry["hadith"],
                sharh=entry["sharh"]
            )

            if processed:
                total_tokens_before += processed["tokens_before"]
                total_tokens_after += processed["tokens_after"]
                
                # Update entry with processed data
                entry.update({
                    "FT_Pairs": processed["qa_pairs"],
                    "hadith_lessons": [processed["answers"][0]] if processed["answers"][0] else [],
                    "hadith_application": [processed["answers"][1]] if processed["answers"][1] else []
                })
                processed_count += 1

        # Save processed data
        self.file_handler.write_json(output_file, data)
        
        return processed_count, total_tokens_before, total_tokens_after

    def process_directory(self, input_dir: str, output_dir: str = None) -> None:
        """
        Process all hadith JSON files in a directory.

        Args:
            input_dir (str): Path to input directory containing JSON files
            output_dir (str): Path to save processed files (if None, adds '_processed' to input_dir)
        """
        # Setup output directory
        if output_dir is None:
            output_dir = input_dir + "_processed"
        os.makedirs(output_dir, exist_ok=True)

        # Get all JSON files
        json_files = self.file_handler.get_json_files(input_dir)
        if not json_files:
            print(f"No JSON files found in {input_dir}")
            return

        # Process each file
        total_processed = 0
        total_tokens_before = 0
        total_tokens_after = 0

        for input_file in json_files:
            file_name = os.path.basename(input_file)
            output_file = os.path.join(output_dir, file_name)
            
            print(f"\nProcessing file: {file_name}")
            processed, tokens_before, tokens_after = self.process_single_file(
                input_file, output_file
            )
            
            total_processed += processed
            total_tokens_before += tokens_before
            total_tokens_after += tokens_after

        # Print summary
        self._print_summary(len(json_files), total_processed, 
                          total_tokens_before, total_tokens_after, output_dir)

    def _print_summary(self, total_files: int, total_processed: int,
                      tokens_before: int, tokens_after: int, output_dir: str) -> None:
        """Print processing summary statistics."""
        print("\n===== OVERALL PROCESSING SUMMARY =====")
        print(f"Total files processed: {total_files}")
        print(f"Total hadiths processed: {total_processed}")
        print(f"Total tokens before generation: {tokens_before}")
        print(f"Total tokens after generation: {tokens_after}")
        if tokens_after > 0:
            print(f"Overall token reduction ratio: {tokens_before/tokens_after:.2f}x")
        print(f"All processed files saved to '{output_dir}'")