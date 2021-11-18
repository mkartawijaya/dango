from typing import List

from .dango import Tokenizer
from .word import Word

DEFAULT_TOKENIZER = Tokenizer()


def tokenize(phrase: str) -> List[Word]:
    """Splits a given phrase into a list of words.

    Args:
        phrase: The phrase that should be tokenized.

    Returns:
        A list of words that make up the given phrase.
    """
    return DEFAULT_TOKENIZER.tokenize(phrase)
