from typing import List

from sudachipy import dictionary
from sudachipy.morpheme import Morpheme

from .fsm import StateMachine, State
from .util import katakana_to_hiragana
from .word import Word


class WordState(State):
    """FSM state used to aggregate morphemes into "word chunks"."""

    def __init__(self, name: str, start_new_word=False):
        """Constructs a new word aggregation state.

        Args:
            name: The name of the state.
            start_new_word: Flag if a new chunk should be started on_input or if the morpheme
                should just be appended to the last chunk.
        """
        self.name = name
        self.start_new_word = start_new_word

    def on_input(self, context: List[List[Morpheme]], morpheme: Morpheme) -> None:
        """Processes the current morpheme.

        Args:
            context: The list of morpheme chunks so far.
            morpheme: The morpheme to process.
        """
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
        # to account for these cases for starting a new verb. Since specific transitions have higher priority than
        # wildcard transition we don't risk breaking apart an inflected verb by accident.
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
    """Tokenizer used to split phrases into words."""

    def __init__(self):
        self._dictionary = dictionary.Dictionary()
        self._tokenizer = self._dictionary.create()

    def find_dictionary_form_reading(self, morpheme: Morpheme) -> str:
        """Returns the dictionary form for a given morpheme.

        Args:
            morpheme: The morpheme for which to find the dictionary form.
        """
        word_id = morpheme.get_word_info().dictionary_form_word_id

        if word_id == -1:
            # If the word ID is -1, then the morpheme is already in
            # dictionary form and we can use its own reading form.
            return katakana_to_hiragana(morpheme.reading_form())
        else:
            # Otherwise we need to look up the word info for the
            # dictionary form and get the reading form of that.
            return katakana_to_hiragana(self._dictionary.lexicon.get_word_info(word_id).reading_form)

    def create_word(self, morphemes: List[Morpheme]) -> Word:
        """Returns a new word created as an aggregation of morphemes.

        Args:
            morphemes: The morphemes that the new word will be composed of.
        """
        return Word(morphemes, self.find_dictionary_form_reading(morphemes[0]))

    def tokenize(self, phrase: str) -> List[Word]:
        """Splits a given phrase into a list of words.

        Args:
            phrase: The phrase that should be tokenized.

        Returns:
            A list of words that make up the given phrase.
        """
        morphemes = self._tokenizer.tokenize(phrase)

        # Aggregating the individual morphemes we get from the tokenizer into words,
        # for example inflected verbs, is heavily dependent on what was already processed
        # (e.g. "was the previous morpheme a verb stem?"). Therefore this problem is well
        # suited to be solved by applying a FSM to process the list of morphemes.
        # By doing so we don't have to resort to writing deeply nested if-statements
        # but can instead declare the dependencies through the transition rules.

        return [self.create_word(mm) for mm in WORD_AGGREGATION_FSM.run([], morphemes)]
