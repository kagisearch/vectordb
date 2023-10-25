"""
This module provides the VectorSearch class for performing vector search using various algorithms.
"""

#pylint: disable = line-too-long, trailing-whitespace, trailing-newlines, line-too-long, missing-module-docstring, import-error, too-few-public-methods, too-many-instance-attributes, too-many-locals

from typing import List, Tuple
import numpy as np
import faiss
import sklearn



MRPT_LOADED = True
try:
    import mrpt
except ImportError:
    print(
        "Warning: mrpt could not be imported. Install with 'pip install git+https://github.com/vioshyvo/mrpt/'. "
        "Falling back to Faiss."
    )
    MRPT_LOADED = False


class VectorSearch:
    """
    A class to perform vector search using different methods (MRPT, Faiss, or scikit-learn).
    """

    @staticmethod
    def run_mrpt(vector, vectors, k=15):
        """
        Search for the most similar vectors using MRPT method.
        """
        if isinstance(vector, list):
            vector = np.array(vector).astype(np.float32)
        index = mrpt.MRPTIndex(vectors)
        res = index.exact_search(vector, k, return_distances=True)
        return res[0].tolist(), res[1].tolist()

    @staticmethod
    def run_faiss(vector, vectors, k=15):
        """
        Search for the most similar vectors using Faiss method.
        """
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        dis, indices = index.search(np.array([vector]), k)
        return indices[0], dis[0]

    @staticmethod
    def run_sk(vector, vectors, k=15):
        """
        Search for the most similar vectors using scikit-learn method.
        """
        similarities = sklearn.metrics.pairwise_distances(
            [vector], vectors, metric="euclidean", n_jobs=-1
        )
        partition_indices = np.argpartition(similarities[0], k)
        indices = partition_indices[:k]
        return indices

    @staticmethod
    def search_vectors(
        query_embedding: List[float], embeddings: List[List[float]], top_n: int
    ) -> List[Tuple[int, float]]:
        """
        Searches for the most similar vectors to the query_embedding in the given embeddings.

        :param query_embedding: a list of floats representing the query vector.
        :param embeddings: a list of vectors to be searched, where each vector is a list of floats.
        :param top_n: the number of most similar vectors to return.
        :return: a list of indices of the top_n most similar vectors in the embeddings.
        """
        if isinstance(embeddings, list):
            embeddings = np.array(embeddings).astype(np.float32)

        if len(embeddings) < 3000 or not MRPT_LOADED:
            call_search = VectorSearch.run_faiss
        else:
            call_search = VectorSearch.run_mrpt

        indices, dis = call_search(query_embedding, embeddings, top_n)

        return list(zip(indices, dis))
