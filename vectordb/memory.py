"""
This module provides the Memory class that represents a memory storage system
for text and associated metadata, with functionality for saving, searching, and
managing memory entries.
"""

from typing import List, Dict, Any, Union
from .chunking import Chunker
from .embedding import BaseEmbedder, Embedder
from .vector_search import VectorSearch
from .storage import Storage
import itertools
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
        embeddings: Union[BaseEmbedder, str] = "normal",
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

        if isinstance(embeddings, str):
            self.embedder = Embedder(embeddings)
        elif isinstance(embeddings, BaseEmbedder):
            self.embedder = embeddings
        else:
            raise TypeError("Embeddings must be an Embedder instance or string")

        self.vector_search = VectorSearch()

    def save(
        self,
        texts,
        metadata: Union[List, List[dict], None] = None,
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

        if metadata is None:
            metadata = []
        elif not isinstance(metadata, list):
            metadata = [metadata]

        # Extend metadata to be the same length as texts, if it's shorter.
        metadata += [{}] * (len(texts) - len(metadata))

        if memory_file is None:
            memory_file = self.memory_file

        text_chunks = [self.chunker(text) for text in texts]
        chunks_size = [len(chunks) for chunks in text_chunks]

        flatten_chunks = itertools.chain.from_iterable(text_chunks)
        embeddings = self.embedder.embed_text(flatten_chunks)

        # accumulated size is end_index of each chunk
        for size, end_index, chunk, meta in zip(
            chunks_size,
            itertools.accumulate(chunks_size),
            text_chunks,
            metadata
        ):
            start_index = end_index - size
            embedding = embeddings[start_index: end_index]
            entry = {
                "chunk": chunk,
                "embedding": embedding,
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
        if self.memory_file is not None:
            Storage(self.memory_file).save_to_disk(self.memory)
        self.memory = []

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
