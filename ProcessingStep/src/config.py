"""
Configuration settings and constants for hadith processing.
"""

# Markers used for cleaning and extracting hadith explanations
EXPLANATION_MARKERS = [
    'هذا الحديثُ', 'مُناسبةُ هذا الحديثِ', 'وفي هذا الحديثِ', 'وفي هذا الأثرِ', 'وفي الحديثِ',
    'وفيه:', 'وفي هذا يَقولُ', 'وفي هذا الأثَرِ', 'وفي هذا الحَديثِ', 'وفي هذا يَحكي',
    'وفي هذا يَذكُرُ', 'وفي هذا يَروي', 'وفي هذا يَخبِرُ', 'وفي هذا يَقولُ',
    'في هذا الحديثِ', 'يُبيِّن', 'يَدُلُّ', 'أخبر', 'بيَّن', 'يُخبر', 'يُبين', 'يَروي', 
    'تَروي', 'يَذكر', 'تَذكر', 'يَحكي', 'تَحكي'
]

# Markers used to identify isnad (chain of narration) sections
ISNAD_MARKERS = [
    'الراوي', 'المحدث', 'المصدر', 'الصفحة أو الرقم', 'خلاصة حكم المحدث', 'التخريج'
]

# Default input/output paths
DEFAULT_INPUT_PATH = "../DATA/ScrappingOutput/Sample_Hadiths.json"
DEFAULT_OUTPUT_DIR = "../DATA/ProcessingOutput"

# Supported hadith books
SUPPORTED_BOOKS = [
    "صحيح البخاري",
    "صحيح مسلم",
    "صحيح أبي داود"
]