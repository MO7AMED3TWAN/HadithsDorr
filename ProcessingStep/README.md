# Data Processing Documentation

## Overview
This document describes the data transformation and preprocessing steps performed in the `Data_Processing.ipynb` notebook. The main focus is on how hadith data retrieved from the dorar API is filtered, cleaned, and transformed into a simplified format for further use.

## Preprocessing Pipeline
### 1. Filtering Hadiths by Book
- The initial dataset (`all_hadiths_explanations2.json`) contains hadiths from various books.
- Only hadiths from "صحيح البخاري" (Sahih Bukhari) and "صحيح مسلم" (Sahih Muslim) are retained.
- Filtering is performed by checking the `book` field under `explanation.data` for each hadith.

### 2. Data Structure Before Transformation
#### Original Data Structure (from dorar API)
```json
{
  "hadith_id": 1,
  "explanation": {
    "status": "success",
    "metadata": { "isCached": false },
    "data": {
      "hadith": "...",
      "rawi": "...",
      "mohdith": "...",
      "book": "...",
      "numberOrPage": "...",
      "grade": "...",
      "takhrij": "...",
      "hasSharhMetadata": true,
      "sharhMetadata": {
        "id": "1",
        "isContainSharh": true,
        "urlToGetSharhById": "/v1/site/sharh/1",
        "sharh": "..."
      }
    }
  }
}
```

### 3. Data Transformation: Flattening and Cleaning
- Unnecessary keys and nested metadata are removed.
- Only essential fields are extracted: `hadith_id`, `hadith`, `rawi`, `mohdith`, `book`, `numberOrPage`, `grade`, `takhrij`, and (if present) `sharh`.
- The transformation flattens the structure for easier downstream processing.

#### Transformed Data Structure (Simplified)
```json
{
  "hadith_id": "1",
  "hadith": "...",
  "rawi": "...",
  "mohdith": "...",
  "book": "...",
  "numberOrPage": "...",
  "grade": "...",
  "takhrij": "...",
  "sharh": "..."
}
```
### 4. Sharh Field Explanation Extraction
- Issue: The `sharh` field sometimes contained both the hadith text and takhrij (referencing and grading information), making it difficult to isolate the actual explanation.
- Solution: To address this, a text analysis step was introduced. All files were programmatically scanned to detect specific markers or keywords that indicate the start of the actual explanation within the `sharh` field.
- The process involved identifying patterns or phrases that typically precede the explanation, then extracting only the relevant portion for each hadith.
- This ensures that only the true explanatory content is retained in the cleaned data, improving the quality and consistency of the dataset.
- **Keywords used for extraction:**
  - **Explanation markers:** [
'هذا الحديثُ', 'مُناسبةُ هذا الحديثِ', 'وفي هذا الحديثِ', 'وفي هذا الأثرِ', 'وفي الحديثِ',
'وفيه:', 'وفي هذا يَقولُ', 'وفي هذا الأثَرِ', 'وفي هذا الحَديثِ', 'وفي هذا يَحكي',
'وفي هذا يَذكُرُ', 'وفي هذا يَروي', 'وفي هذا يَخبِرُ', 'وفي هذا يَقولُ',
'في هذا الحديثِ', 'يُبيِّن', 'يَدُلُّ', 'أخبر', 'بيَّن', 'يُخبر', 'يُبين', 'يَروي',
'تَروي', 'يَذكر', 'تَذكر', 'يَحكي', 'تَحكي'
]
  - **Isnad/takhrij markers:** [
'الراوي', 'المحدث', 'المصدر', 'الصفحة أو الرقم', 'خلاصة حكم المحدث', 'التخريج'
]
- These lists are used to programmatically split or filter the `sharh` field, ensuring only the explanation is retained for downstream processing.

### 5. Batch Processing and Saving
- The transformation is applied to all filtered hadiths.
- The processed data is saved to a new file for further use.


## Transformation Notes
- The original data contains nested fields under `explanation` and `sharhMetadata`.
- The transformation flattens the structure, extracting only the essential fields for each hadith.
- Unnecessary metadata and nested explanation details are omitted in the simplified format.
- This process enables easier downstream processing and integration with Q&A generation workflows.
- removing the hadith_id and replace it with NumberOrPage id 
- filtering the sharh data using the keywords that aimt to

## How the Transformation is Performed
The notebook reads the original JSON, extracts the relevant fields, and writes the simplified structure to a new file or data store. This is typically done using Python's `json` module and custom extraction logic.

---

For more details, refer to the code and comments in `Data_Processing.ipynb` or in `main.ipynb` as an OOP Logic.

