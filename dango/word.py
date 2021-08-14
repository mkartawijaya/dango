from typing import List

from sudachipy.morpheme import Morpheme

from .util import katakana_to_hiragana


class Word:

    def __init__(self, morphemes: List[Morpheme], dictionary_form_reading: str = None):
        self._morphemes = morphemes
        self.dictionary_form_reading = dictionary_form_reading

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
        return katakana_to_hiragana(''.join(m.reading_form() for m in self._morphemes))

    @property
    def dictionary_form(self) -> str:
        """The the dictionary form of the word."""
        return self._morphemes[0].dictionary_form() if self._morphemes else ''
