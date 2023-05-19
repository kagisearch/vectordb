"""
This module provides the Memory class that represents a memory storage system
for text and associated metadata, with functionality for saving, searching, and
managing memory entries.
"""

from typing import List, Dict, Any
from .chunking import Chunker
from .embedding import Embedder
from .vector_search import VectorSearch
from .storage import Storage
import time
import tensorflow as tf


class Memory:
    """
    Memory class represents a memory storage system for text and associated metadata.
    It provides functionality for saving, searching, and managing memory entries.
    """

    def __init__(
        self,
        memory_file: str = None,
        chunking_strategy: dict = None,
        embeddings: str = "normal",
    ):
        """
        Initializes the Memory class.

        :param memory_file: a string containing the path to the memory file. (default: None)
        :param chunking_strategy: a dictionary containing the chunking mode (default: {"mode": "sliding_window"}).
        :param embedding_model: a string containing the name of the pre-trained model to be used for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2").
        """
        self.memory_file = memory_file
        self.memory = (
            [] if memory_file is None else Storage(memory_file).load_from_disk()
        )
        if chunking_strategy is None:
            chunking_strategy = {"mode": "sliding_window"}
        self.chunker = Chunker(chunking_strategy)
        self.embedder = Embedder(embeddings)
        self.vector_search = VectorSearch()

    def save(
        self,
        texts,
        metadata: list = [],
        memory_file: str = None,
        embed_at_search: bool = False,
    ):
        """
        Saves the given texts and metadata to memory.

        :param texts: a string or a list of strings containing the texts to be saved.
        :param metadata: a dictionary or a list of dictionaries containing the metadata associated with the texts.
        :param memory_file: a string containing the path to the memory file. (default: None)
        """
        if not isinstance(texts, list):
            texts = [texts]
        if not isinstance(metadata, list):
            metadata = [metadata]

        # Extend metadata to be the same length as texts, if it's shorter.
        metadata += [{}] * (len(texts) - len(metadata))

        if memory_file is None:
            memory_file = self.memory_file

        for text, meta in zip(texts, metadata):
            chunks = self.chunker.strategy(text)
            embeddings = self.embedder.embed_text(chunks)
            for chunk, embedding in zip(chunks, embeddings):
                entry = {
                    "chunk": chunk,
                    "embedding": embedding.numpy().tolist()
                    if isinstance(embedding, tf.Tensor)
                    else embedding.tolist(),
                    "metadata": meta,
                }
                self.memory.append(entry)

        if memory_file is not None:
            Storage(memory_file).save_to_disk(self.memory)

    def search(self, query: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for the most similar chunks to the given query in memory.

        :param query: a string containing the query text.
        :param top_n: the number of most similar chunks to return. (default: 5)
        :return: a list of dictionaries containing the top_n most similar chunks and their associated metadata.
        """
        query_embedding = self.embedder.embed_text([query])[0]
        embeddings = [entry["embedding"] for entry in self.memory]
        indices = self.vector_search.search_vectors(query_embedding, embeddings, top_n)
        results = [
            {"chunk": self.memory[i]["chunk"], "metadata": self.memory[i]["metadata"]}
            for i in indices
        ]
        return results

    def clear(self):
        """
        Clears the memory.
        """
        self.memory = []
        if self.memory_file is not None:
            Storage(self.memory_file).save_to_disk(self.memory)

    def dump(self):
        """
        Prints the contents of the memory.
        """
        for entry in self.memory:
            print("Chunk:", entry["chunk"])
            print("Embedding Length:", len(entry["embedding"]))
            print("Metadata:", entry["metadata"])
            print("-" * 40)
        print("Total entries: ", len(self.memory))
