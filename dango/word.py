from typing import List

from sudachipy.morpheme import Morpheme


class Word:

    def __init__(self, morphemes: List[Morpheme]):
        self._morphemes = morphemes

    @property
    def morphemes(self):
        """The morphemes the word is made up of."""
        return self._morphemes

    @property
    def surface(self):
        """The surface representation of the word."""
        return ''.join(m.surface() for m in self._morphemes)
