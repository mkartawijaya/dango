from typing import List

from sudachipy import dictionary


def tokenize(phrase: str) -> List[str]:
    tokenizer = dictionary.Dictionary().create()
    return [m.surface() for m in tokenizer.tokenize(phrase)]
