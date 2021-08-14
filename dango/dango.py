from typing import List

from sudachipy import dictionary

from .fsm import create_fsm
from .word import Word


class Tokenizer:
    def __init__(self):
        self._fsm = create_fsm()
        self._tokenizer = dictionary.Dictionary().create()

    def tokenize(self, phrase: str) -> List[Word]:
        morphemes = self._tokenizer.tokenize(phrase)
        return map(Word, self._fsm.run(morphemes))


TOKENIZER = Tokenizer()


def tokenize(phrase: str) -> List[Word]:
    return TOKENIZER.tokenize(phrase)
