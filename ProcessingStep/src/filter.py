"""
Module for filtering hadith collections by book name.

This module provides functionality to filter hadith collections by specific book names,
making it easier to process hadiths from different books separately.
"""

import json
from typing import List, Dict
from .config import SUPPORTED_BOOKS

def filter_hadiths(input_path: str, book_name: str) -> List[Dict]:
    """
    Filter hadiths by book name from the main JSON file.
    
    This function reads a JSON file containing multiple hadiths and filters them
    based on the specified book name. Only hadiths from the requested book are returned.
    
    Args:
        input_path (str): Path to the main JSON file containing all hadiths
        book_name (str): Name of the book to filter hadiths from
        
    Returns:
        List[Dict]: List of hadiths from the specified book
        
    Raises:
        FileNotFoundError: If input_path does not exist
        ValueError: If book_name is not in SUPPORTED_BOOKS
        json.JSONDecodeError: If input file is not valid JSON
        
    Example:
        >>> hadiths = filter_hadiths("hadiths.json", "صحيح البخاري")
        >>> print(len(hadiths))
        1234
    """
    if book_name not in SUPPORTED_BOOKS:
        raise ValueError(f"Book {book_name} not in supported books: {SUPPORTED_BOOKS}")
        
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            all_hadiths = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON in file: {input_path}")
    
    filtered = [
        h for h in all_hadiths 
        if h.get("explanation", {}).get("data", {}).get("book") == book_name
    ]
    
    print(f"Filtered {len(filtered)} hadiths for book: {book_name}")
    return filtered