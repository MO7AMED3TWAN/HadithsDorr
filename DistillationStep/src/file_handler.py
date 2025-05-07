"""
This module handles all file operations including reading and writing JSON files,
finding files in directories, and managing paths.
"""

import os
import json
import glob
from typing import List, Dict, Any

class FileHandler:
    """
    Handles all file operations for the hadith processing system.
    This includes reading/writing JSON files and managing directories.
    """

    def read_json(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Read and parse a JSON file.

        Args:
            file_path (str): Path to the JSON file to read

        Returns:
            List[Dict[str, Any]]: The parsed JSON data
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return []

    def write_json(self, file_path: str, data: List[Dict[str, Any]]) -> bool:
        """
        Write data to a JSON file.

        Args:
            file_path (str): Path where to save the JSON file
            data (List[Dict[str, Any]]): Data to save

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {str(e)}")
            return False

    def get_json_files(self, directory: str) -> List[str]:
        """
        Get all JSON files in a directory.

        Args:
            directory (str): Directory to search for JSON files

        Returns:
            List[str]: List of full paths to JSON files
        """
        return glob.glob(os.path.join(directory, "*.json"))

    def ensure_directory(self, directory: str) -> bool:
        """
        Create a directory if it doesn't exist.

        Args:
            directory (str): Directory path to create

        Returns:
            bool: True if directory exists or was created, False on error
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
            return False

    def clean_empty_files(self, directory: str) -> None:
        """
        Remove JSON files that have empty or invalid content.

        Args:
            directory (str): Directory to clean
        """
        for filename in os.listdir(directory):
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(directory, filename)
            try:
                data = self.read_json(file_path)
                
                if isinstance(data, list):
                    all_empty = True
                    for entry in data:
                        if (entry.get("hadith_lessons") or 
                            entry.get("hadith_application") or 
                            entry.get("FT_Pairs")):
                            all_empty = False
                            break

                    if all_empty:
                        os.remove(file_path)
                        print(f"Removed empty file: {filename}")

            except Exception as e:
                print(f"Error checking file {filename}: {str(e)}")