from typing import List

from sudachipy import dictionary
from sudachipy.morpheme import Morpheme


class Word:

    def __init__(self, morphemes: List[Morpheme]):
        self._morphemes = morphemes

    @property
    def surface(self):
        """The surface representation of the word."""
        return ''.join(m.surface() for m in self._morphemes)


def tokenize(phrase: str) -> List[Word]:
    tokenizer = dictionary.Dictionary().create()
    return [Word([m]) for m in tokenizer.tokenize(phrase)]
