"""
Module for cleaning and processing hadith texts.

This module provides functionality for cleaning and extracting explanations from hadith texts,
removing metadata and other non-essential information while preserving the actual content.
"""

import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from tqdm import tqdm

from .config import EXPLANATION_MARKERS, ISNAD_MARKERS

def clean_sharh(sharh: str) -> str:
    """
    Clean and extract the actual explanation from sharh text.
    
    Args:
        sharh (str): Raw sharh text containing metadata and explanation
        
    Returns:
        str: Cleaned explanation text with metadata removed
        
    Example:
        >>> text = "الحديث\\n     الراوي : أبو هريرة\\n...\\nهذا الحديث يدل على..."
        >>> clean_sharh(text)
        'هذا الحديث يدل على...'
    """
    if not sharh:
        return ""
    
    # Remove hadith text if it appears at beginning
    hadith_text_end = sharh.find('\n     الراوي :')
    if hadith_text_end != -1:
        sharh = sharh[hadith_text_end:]
    
    # Remove metadata section
    metadata_pattern = re.compile(r'\s*الراوي :.*?التخريج :.*?\n\s*\n', re.DOTALL)
    match = metadata_pattern.search(sharh)
    after_metadata = sharh[match.end():] if match else sharh
    
    # Find explanation markers
    for marker in EXPLANATION_MARKERS:
        idx = after_metadata.find(marker)
        if idx != -1:
            return after_metadata[idx:].strip()
    
    return after_metadata.strip()

def clean_hadiths(hadiths: List[Dict]) -> List[Dict]:
    """
    Clean a list of hadiths by processing them in parallel.
    
    This function extracts and cleans relevant fields from each hadith,
    including the explanation text (sharh), and processes them using
    parallel execution for better performance.
    
    Args:
        hadiths (List[Dict]): List of raw hadith dictionaries
        
    Returns:
        List[Dict]: List of cleaned hadith dictionaries with processed fields
        
    Example:
        >>> hadiths = [{"hadith_id": 1, "explanation": {"data": {...}}}]
        >>> cleaned = clean_hadiths(hadiths)
    """
    def process_single(hadith: Dict) -> Dict:
        """Process a single hadith by extracting and cleaning its fields"""
        cleaned = {
            "hadith_id": hadith.get("hadith_id"),
            "book": hadith.get("explanation", {}).get("data", {}).get("book"),
            "rawi": hadith.get("explanation", {}).get("data", {}).get("rawi"),
            "hadith": hadith.get("explanation", {}).get("data", {}).get("hadith"),
            "sharh": clean_sharh(
                hadith.get("explanation", {}).get("data", {}).get("sharhMetadata", {}).get("sharh")
            )
        }
        return cleaned
    
    with ThreadPoolExecutor() as executor:
        cleaned = list(tqdm(
            executor.map(process_single, hadiths),
            total=len(hadiths),
            desc="Cleaning hadiths"
        ))
    
    print(f"Cleaned {len(cleaned)} hadiths")
    return cleaned