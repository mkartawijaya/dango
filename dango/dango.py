from typing import List

from sudachipy import dictionary
from sudachipy.morpheme import Morpheme

from .fsm import StateMachine, State
from .util import katakana_to_hiragana
from .word import Word


class WordState(State):

    def __init__(self, name: str, start_new_word=False):
        self.name = name
        self.start_new_word = start_new_word

    def on_input(self, context: List[List[Morpheme]], morpheme: Morpheme) -> None:
        if self.start_new_word:
            context.append([])
        context[-1].append(morpheme)


UNSPECIFIED_WORD_STATE = WordState('UNSPECIFIED', start_new_word=True)
VERB_STATE = WordState('VERB', start_new_word=True)
VERB_INFLECTION_STATE = WordState('VERB_INFLECTION')
ADJECTIVE_STATE = WordState('ADJECTIVE', start_new_word=True)
ADJECTIVE_INFLECTION_STATE = WordState('ADJECTIVE_INFLECTION')

WORD_AGGREGATION_FSM = StateMachine(
    [
        UNSPECIFIED_WORD_STATE,
        VERB_STATE,
        VERB_INFLECTION_STATE,
        ADJECTIVE_STATE,
        ADJECTIVE_INFLECTION_STATE
    ],
    UNSPECIFIED_WORD_STATE,
    UNSPECIFIED_WORD_STATE,
    [
        # --- transitions to aggregate inflected verbs ---

        # start of a verb
        (None, ('動詞', '一般', '*', '*'), VERB_STATE),
        # Some verbs (for example 見る) are detected as non independent even when standing alone, so we also need
        # account for these cases for starting a new verb. Since specific transitions have higher priority than
        # wildcard transition we don't risk accidentally breaking apart an inflected verb apart.
        (None, ('動詞', '非自立可能', '*', '*'), VERB_STATE),
        # The inflected part of a verb is started by either an auxiliary verb, ...
        (VERB_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),
        # or a conjunctive particle, i.e. て or で.
        (VERB_STATE, ('助詞', '接続助詞', '*', '*'), VERB_INFLECTION_STATE),
        # continue aggregating any auxiliary verbs ...
        (VERB_INFLECTION_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),
        # and non independent verbs, e.g. the いる　of the continuous form
        (VERB_INFLECTION_STATE, ('動詞', '非自立可能', '*', '*'), VERB_INFLECTION_STATE),

        # suffix for seeming/looks-like
        (VERB_STATE, ('形状詞', '助動詞語幹', '*', '*'), VERB_INFLECTION_STATE),

        # --- transitions to aggregate inflected adjectives ---

        # start of an adjective
        (None, ('形容詞', '一般', '*', '*'), ADJECTIVE_STATE),
        # can be followed by negating suffix
        (ADJECTIVE_STATE, ('形容詞', '非自立可能', '*', '*'), ADJECTIVE_INFLECTION_STATE),
        # and/or suffix for the past-tense
        (ADJECTIVE_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),
        (ADJECTIVE_INFLECTION_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),

        # suffix for seeming/looks-like
        (ADJECTIVE_STATE, ('形状詞', '助動詞語幹', '*', '*'), ADJECTIVE_INFLECTION_STATE)
    ])


class Tokenizer:
    def __init__(self):
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
        return [self.make_word(mm) for mm in WORD_AGGREGATION_FSM.run([], morphemes)]


TOKENIZER = Tokenizer()


def tokenize(phrase: str) -> List[Word]:
    return TOKENIZER.tokenize(phrase)
