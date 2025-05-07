"""
Utility functions for hadith processing including token estimation
and fixed question management.
"""

from typing import List, Dict

def estimate_tokens(text: str) -> int:
    """
    Estimate token count in Arabic text (rough approximation).
    
    Args:
        text (str): Input text to estimate tokens for
        
    Returns:
        int: Estimated number of tokens
    """
    # For Arabic text, rough estimation is about 1 token per 2.5 characters
    return len(text) // 2

def get_fixed_questions() -> List[Dict[str, str]]:
    """
    Get the list of fixed questions with their full diacritics.
    
    Returns:
        List[Dict[str, str]]: List of question-answer template pairs
    """
    return [
        {
            "question": "مَا هِيَ الرَّسَائِلُ الرَّئِيسِيَّةُ وَالدُّرُوسُ المُسْتَفَادَةُ والفَوَائِد المُستَخلصَة مِنَ الحَدِيثِ؟",
            "answer": "{answer1}"
        },
        {
            "question": "كَيْفَ يُمْكِنُ تَطْبِيقُ الحَدِيثِ فِي الحَيَاةِ اليَوْمِيَّةِ؟",
            "answer": "{answer2}"
        },
        {
            "question": "مَا أَهَمِّيَّةُ الحَدِيثِ فِي الفِقْهِ الإِسْلَامِيِّ؟",
            "answer": "{answer3}"
        },
        {
            "question": "مَا سَبَبُ وُرُودِ الحَدِيثِ؟",
            "answer": "{answer4}"
        }
    ]