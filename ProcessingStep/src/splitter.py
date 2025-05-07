"""
Module for splitting and saving hadith collections into individual files.

This module provides functionality to save processed hadiths as individual JSON files,
making it easier to manage and access individual hadiths.
"""

import os
import json
import re
from tqdm import tqdm
from typing import List, Dict

def sanitize_filename(filename: str) -> str:
    """
    Sanitize string to be used as filename.
    
    Removes or replaces characters that are not safe for filenames.
    
    Args:
        filename (str): Original filename string
        
    Returns:
        str: Sanitized filename safe for filesystem use
        
    Example:
        >>> sanitize_filename("file/with\\unsafe:chars")
        'file_with_unsafe_chars'
    """
    return re.sub(r'[\\/*?:"<>|]', '_', str(filename))

def save_as_individual_cards(hadiths: List[Dict], output_dir: str) -> str:
    """
    Save each hadith as individual JSON file.
    
    Creates the output directory if it doesn't exist and saves each hadith
    as a separate JSON file with a sanitized filename based on the hadith ID.
    
    Args:
        hadiths (List[Dict]): List of processed hadith dictionaries
        output_dir (str): Directory path where hadith files will be saved
        
    Returns:
        str: Path to the output directory containing saved files
        
    Raises:
        OSError: If directory creation or file writing fails
        
    Example:
        >>> hadiths = [{"hadith_id": "123", ...}]
        >>> output_dir = save_as_individual_cards(hadiths, "output/")
        >>> print(output_dir)
        'output/'
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create output directory {output_dir}: {e}")
    
    for hadith in tqdm(hadiths, desc="Creating cards"):
        hadith_id = hadith.get('hadith_id', 'unknown')
        safe_name = sanitize_filename(hadith_id)
        output_path = os.path.join(output_dir, f"{safe_name}.json")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(hadith, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"Warning: Failed to save hadith {hadith_id}: {e}")
            continue
    
    print(f"Created {len(hadiths)} hadith cards in {output_dir}")
    return output_dir