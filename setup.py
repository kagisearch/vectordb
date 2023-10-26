#pylint: disable = line-too-long, trailing-whitespace, trailing-newlines, line-too-long, missing-module-docstring, import-error, too-few-public-methods, too-many-instance-attributes, too-many-locals

from setuptools import setup, find_packages

setup(
    name="vectordb2",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "transformers>=4.10.0",
        "numpy>=1.21.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.7.0",
        "sentence_transformers",
        "faiss-cpu",
        "tensorflow_text"
    ],
    author="Vladimir Prelovac",
    author_email="vlad@kagi.com",
    description="A lightweight Python package for storing and retrieving text using chunking, embedding, and vector search",
    keywords="text chunking embedding vector search",
    url="https://github.com/kagisearch/vectordb",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
