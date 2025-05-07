# Dorar Hadith API Crawler
=
This project provides a modular system for crawling hadith explanations from the Dorar Hadith API. The system is designed to be robust, maintainable, and user-friendly.


## Project Structure

```
HadithsDorr/
├── src/
│   ├── __init__.py
│   ├── server_manager.py    # Server management
│   ├── data_manager.py      # Data handling
│   └── hadith_crawler.py    # Crawling logic
├── ScrapingStep/
│   ├── Main.ipynb           # Main notebook
│   └── dorar-hadith-api/    # API server
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites

1. Python 3.8 or higher
2. Node.js 16.14.0 or higher
3. npm 8.3.1 or higher

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/HadithsDorr.git
   cd HadithsDorr
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   cd ScrapingStep/dorar-hadith-api
   npm install
   ```

## Running the Crawler
## تشغيل الزاحف

1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Navigate to `ScrapingStep/Main.ipynb`

3. Run the cells in order:
   - First cell: Imports and setup
   - Second cell: Initialize components
   - Third cell: Start crawling
   - Fourth cell: Shutdown server (when done)

## Server Management
## إدارة الخادم

The system automatically manages the API server:
- Starts the server when needed
- Restarts after every 70 requests
- Handles errors and retries
- Shuts down properly when done


## Data Management

The system handles data automatically:
- Saves progress every 100 hadiths
- Creates backups before major operations
- Stores data in JSON format
- Tracks successful and failed requests


## Output Files

The system creates several files:
- `all_hadiths_explanations2.json`: All collected explanations
- `successful_hadith_ids2.json`: IDs of successfully processed hadiths
- `last_processed_id.json`: Last processed hadith ID
- `hadith_backups/`: Directory containing backup files



## Error Handling

The system includes robust error handling:
- Automatic server restart on failure
- Progress saving on interruption
- Detailed error messages
- Recovery from crashes



## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Making your changes
4. Submitting a pull request
