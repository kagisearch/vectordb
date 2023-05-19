from typing import List
from sentence_transformers import SentenceTransformer
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import tensorflow as tf


class Embedder:
    """
    This class provides a way to generate embeddings for given text chunks using a specified
    pre-trained model.
    """

    def __init__(self, model_name: str = "normal"):
        """
        Initializes the Embedder with a specified model.

        :param model_name: a string containing the name of the pre-trained model to be used
        for embeddings.
        """
        self.sbert = True
        print("Initiliazing embeddings: ", model_name)
        if model_name == "fast":
            self.model = hub.load(
                "https://tfhub.dev/google/universal-sentence-encoder/4"
            )
            self.sbert = False

        else:
            if model_name == "normal":
                model_name = "sentence-transformers/all-MiniLM-L6-v2"
            elif model_name == "best":
                model_name = "sentence-transformers/all-mpnet-base-v2"

            self.model = SentenceTransformer(model_name)

        print("OK.")

    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """
        Converts a list of text chunks into their corresponding embeddings.

        :param chunks: a list of strings containing the text chunks to be embedded.
        :return: a list of embeddings, where each embedding is represented as a list of floats.
        """
        if self.sbert:
            embeddings = self.model.encode(chunks)
        else:
            embeddings = self.model(chunks)
        return embeddings
