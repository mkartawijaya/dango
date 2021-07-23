from typing import List

from dango.fsm import create_fsm
from dango.word import Word
from sudachipy import dictionary


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
