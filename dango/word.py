from typing import List

from sudachipy.morpheme import Morpheme


class Word:

    def __init__(self, morphemes: List[Morpheme]):
        self._morphemes = morphemes

    @property
    def morphemes(self) -> List[Morpheme]:
        """The morphemes the word is made up of."""
        return self._morphemes

    @property
    def surface(self) -> str:
        """The surface representation of the word."""
        return ''.join(m.surface() for m in self._morphemes)

    @property
    def surface_reading(self) -> str:
        """The kana reading of the surface representation."""
        return ''.join(m.reading_form() for m in self._morphemes)

    @property
    def dictionary_form(self) -> str:
        """The the dictionary form of the word."""
        return self._morphemes[0].dictionary_form() if self._morphemes else ''
