from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class VectorSearch:
    @staticmethod
    def search_vectors(
        query_embedding: List[float], embeddings: List[List[float]], top_n: int
    ) -> List[int]:
        """
        Searches for the most similar vectors to the query_embedding in the given embeddings.

        :param query_embedding: a list of floats representing the query vector.
        :param embeddings: a list of vectors to be searched, where each vector is a list of floats.
        :param top_n: the number of most similar vectors to return.
        :return: a list of indices of the top_n most similar vectors in the embeddings.
        """
        similarities = cosine_similarity([query_embedding], embeddings)
        indices = np.argsort(similarities[0])[-top_n:][::-1]
        return indices
