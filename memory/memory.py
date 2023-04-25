from typing import List, Dict, Any
from .chunking import Chunker
from .embedding import Embedder
from .vector_search import VectorSearch
from .storage import Storage


class Memory:
    def __init__(
        self,
        memory_file: str = None,
        chunking_strategy: dict = {"mode": "sliding_window"},
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
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
        self.chunker = Chunker(chunking_strategy)
        self.embedder = Embedder(embedding_model)
        self.vector_search = VectorSearch()

    def save(self, texts, metadata_list, memory_file: str = None):
        """
        Saves the given texts and metadata to memory.

        :param texts: a string or a list of strings containing the texts to be saved.
        :param metadata_list: a dictionary or a list of dictionaries containing the metadata associated with the texts.
        :param memory_file: a string containing the path to the memory file. (default: None)
        """
        if not isinstance(texts, list):
            texts = [texts]
        if not isinstance(metadata_list, list):
            metadata_list = [metadata_list]

        if memory_file is None:
            memory_file = self.memory_file
        for text, metadata in zip(texts, metadata_list):
            chunks = self.chunker.strategy(text)
            embeddings = self.embedder.embed_text(chunks)
            for chunk, embedding in zip(chunks, embeddings):
                entry = {
                    "chunk": chunk,
                    "embedding": embedding.tolist(),
                    "metadata": metadata,
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
        print("Total entries: ", len)
