from typing import List, Dict, Any
import pickle
import os


class Storage:
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
        with open(self.memory_file, "wb") as f:
            pickle.dump(data, f)

    def load_from_disk(self) -> List[Dict[str, Any]]:
        """
        Loads the data from the memory file as a list of dictionaries.

        :return: a list of dictionaries containing the data loaded from the memory file.
        """
        if not os.path.exists(self.memory_file):
            return []
        with open(self.memory_file, "rb") as f:
            data = pickle.load(f)
        return data
