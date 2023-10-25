"""
This module provides classes for generating text embeddings using various pre-trained models.
"""

#pylint: disable = line-too-long, trailing-whitespace, trailing-newlines, line-too-long, missing-module-docstring, import-error, too-few-public-methods, too-many-instance-attributes, too-many-locals

from abc import ABC, abstractmethod
from typing import List

import tensorflow_hub as hub
from sentence_transformers import SentenceTransformer


class BaseEmbedder(ABC):
    """Base class for Embedder."""
    @abstractmethod
    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of text chunks."""



class Embedder(BaseEmbedder):
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
        elif model_name == "multilingual" :
            self.model = hub.load(
                "universal-sentence-encoder-multilingual-large/3"
            )
            self.sbert = False
        else:
            #if model_name == "normal":
            #    model_name = "sentence-transformers/all-MiniLM-L6-v2"
            if model_name == "normal":
                model_name = "BAAI/bge-small-en-v1.5"
            elif model_name == "best":
                model_name = "BAAI/bge-base-en-v1.5"
                

            self.model = SentenceTransformer(model_name)

        print("OK.")

    def embed_text(self, chunks: List[str]) -> List[List[float]]:
        """
        Converts a list of text chunks into their corresponding embeddings.

        :param chunks: a list of strings containing the text chunks to be embedded.
        :return: a list of embeddings, where each embedding is represented as a list of floats.
        """
        if self.sbert:
            embeddings = self.model.encode(chunks).tolist()
        else:
            embeddings = self.model(chunks).numpy().tolist()
        return embeddings
