# pylint: disable = line-too-long, trailing-whitespace, trailing-newlines, line-too-long, missing-module-docstring, import-error, too-few-public-methods, too-many-instance-attributes, too-many-locals
from ._version import version as VERSION  # noqa

from .chunking import Chunker
from .embedding import BaseEmbedder, Embedder
from .memory import Memory
from .storage import Storage
from .vector_search import VectorSearch

__version__ = VERSION
__author__ = "kagisearch"

__all__ = [
    "Chunker",
    "BaseEmbedder",
    "Embedder",
    "Memory",
    "Storage",
    "VectorSearch",
]