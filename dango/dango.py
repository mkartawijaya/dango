from typing import List

from sudachipy import dictionary
from sudachipy.morpheme import Morpheme

from .fsm import create_fsm
from .util import katakana_to_hiragana
from .word import Word


class Tokenizer:
    def __init__(self):
        self._fsm = create_fsm()
        self._dictionary = dictionary.Dictionary()
        self._tokenizer = self._dictionary.create()

    def find_dictionary_form_reading(self, morpheme: Morpheme) -> str:
        word_id = morpheme.get_word_info().dictionary_form_word_id

        if word_id == -1:
            # If the word ID is -1, then the morpheme is already in
            # dictionary form and we can use its own reading form.
            return katakana_to_hiragana(morpheme.reading_form())
        else:
            # Otherwise we need to look up the word info for the
            # dictionary form and get the reading form of that.
            return katakana_to_hiragana(self._dictionary.lexicon.get_word_info(word_id).reading_form)

    def make_word(self, morphemes: List[Morpheme]) -> Word:
        return Word(morphemes, self.find_dictionary_form_reading(morphemes[0]))

    def tokenize(self, phrase: str) -> List[Word]:
        morphemes = self._tokenizer.tokenize(phrase)
        return [self.make_word(mm) for mm in self._fsm.run(morphemes)]


TOKENIZER = Tokenizer()


def tokenize(phrase: str) -> List[Word]:
    return TOKENIZER.tokenize(phrase)
