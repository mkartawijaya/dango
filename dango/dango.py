from typing import List

from sudachipy import dictionary

from dango.fsm import create_fsm
from dango.word import Word


def tokenize(phrase: str) -> List[Word]:
    tokenizer = dictionary.Dictionary().create()

    fsm = create_fsm()

    morphemes = tokenizer.tokenize(phrase)
    return map(Word, fsm.run(morphemes))
