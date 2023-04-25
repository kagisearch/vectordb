from typing import List, Callable
import spacy
import re

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])


class Chunker:
    def __init__(self, strategy: dict):
        """
        Initializes the Chunker with a specified strategy.

        :param strategy: a dictionary containing the chunking mode (paragraph or sliding_window)
                         and optional window_size and overlap values for sliding_window mode.
        """
        if strategy["mode"] == "paragraph":
            self.strategy = self.paragraph_chunking
        elif strategy["mode"] == "sliding_window":
            self.strategy = self.sliding_window_chunking
            self.window_size = strategy.get("window_size", 256)
            self.overlap = strategy.get("overlap", 32)
        else:
            raise ValueError(f"Invalid chunking strategy: {strategy}")

    def clean_text(self, text: str) -> str:
        """
        Removes extra whitespaces from the input text.

        :param text: a string containing the text to be cleaned.
        :return: a cleaned version of the input text.
        """
        # Remove extra whitespaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def paragraph_chunking(self, text: str) -> List[str]:
        """
        Splits the input text into paragraphs.

        :param text: a string containing the text to be chunked.
        :return: a list of paragraphs extracted from the input text.
        """
        paragraphs = text.split("\n\n")
        cleaned_paragraphs = []
        for p in paragraphs:
            cleaned_p = self.clean_text(p)
            if cleaned_p:
                cleaned_paragraphs.append(cleaned_p)
        return cleaned_paragraphs

    def sliding_window_chunking(self, text: str) -> List[str]:
        """
        Splits the input text into chunks using the sliding window technique.

        :param text: a string containing the text to be chunked.
        :return: a list of chunks generated from the input text.
        """
        if self.window_size is None or self.overlap is None:
            raise ValueError(
                "Window size and overlap must be specified for sliding window chunking."
            )

        text = self.clean_text(text)
        tokens = [t.text for t in nlp(text)]

        # Use a list comprehension to create chunks from windows
        step = self.window_size - self.overlap
        # Ensure the range covers the entire length of the tokens
        chunks = [
            " ".join(tokens[i : i + self.window_size])
            for i in range(0, len(tokens) - self.window_size + step, step)
        ]

        return chunks
