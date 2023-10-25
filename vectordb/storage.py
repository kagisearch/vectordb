"""
This module provides the Storage class for saving and loading data to and from a disk.
"""

#pylint: disable = line-too-long, trailing-whitespace, trailing-newlines, line-too-long, missing-module-docstring, import-error, too-few-public-methods, too-many-instance-attributes, too-many-locals

from typing import List, Dict, Any
import pickle
import os


class Storage:
    """
    A class to handle saving and loading data to and from a memory file.
    """

    def __init__(self, memory_file: str = "long_memory.pkl"):
        """
        Initializes the Storage with a specified memory file.

        :param memory_file: a string containing the path to the memory file.
        """
        self.memory_file = memory_file

    def save_to_disk(self, data: List[Dict[str, Any]]):
        """
        Saves a list of dictionaries containing data to the memory file.

        :param data: a list of dictionaries to be saved.
        """
        with open(self.memory_file, "wb") as file_handler:
            pickle.dump(data, file_handler)

    def load_from_disk(self) -> List[Dict[str, Any]]:
        """
        Loads the data from the memory file as a list of dictionaries.

        :return: a list of dictionaries containing the data loaded from the memory file.
        """
        if not os.path.exists(self.memory_file):
            return []
        with open(self.memory_file, "rb") as file_handler:
            data = pickle.load(file_handler)
        return data
