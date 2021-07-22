from typing import Iterable, List

from sudachipy.morpheme import Morpheme


class WordState(object):
    def __init__(self, name, start_new_word=False):
        self._name = name
        self._start_new_word = start_new_word

    def on_input(self, context: List[List[Morpheme]], morpheme: Morpheme):
        if self._start_new_word:
            context.append([])
        context[-1].append(morpheme)

    def __str__(self):
        return self._name


UNSPECIFIED_WORD_STATE = WordState('UNSPECIFIED', start_new_word=True)
VERB_STATE = WordState('VERB', start_new_word=True)
VERB_INFLECTION_STATE = WordState('VERB_INFLECTION')
ADJECTIVE_STATE = WordState('ADJECTIVE', start_new_word=True)
ADJECTIVE_INFLECTION_STATE = WordState('ADJECTIVE_INFLECTION')


def node_features(node: Morpheme):
    return tuple(node.part_of_speech()[:4])


class StateMachine(object):
    def __init__(self, states, transitions, initial_state, default_state=None):
        self._states = frozenset(states)

        self._transitions = {}
        for src, features, dst in transitions:
            assert src is None or src in self._states
            assert dst in self._states
            assert features is not None
            self._transitions[(src, features)] = dst

        assert initial_state in self._states
        self._initial_state = initial_state

        assert default_state is None or default_state in self._states
        self._default_state = default_state

    def get_next_state(self, src_state, node):

        features = node_features(node)

        if (src_state, features) in self._transitions:
            dst_state = self._transitions[(src_state, features)]
        elif (None, features) in self._transitions:
            dst_state = self._transitions[(None, features)]
        else:
            dst_state = self._default_state

        return dst_state

    def run(self, inputs: Iterable[Morpheme]):
        context = []

        current_state = self._initial_state

        for node in inputs:
            next_state = self.get_next_state(current_state, node)
            next_state.on_input(context, node)
            current_state = next_state

        return context


def create_fsm():
    return StateMachine(
        [
            UNSPECIFIED_WORD_STATE,
            VERB_STATE,
            VERB_INFLECTION_STATE,
            ADJECTIVE_STATE,
            ADJECTIVE_INFLECTION_STATE
        ],
        [
            # --- transitions to aggregate inflected verbs ---

            # start of a verb
            (None, ('動詞', '一般', '*', '*'), VERB_STATE),
            # Some verbs (for example 見る) are detected as non independent even when standing alone,
            # so we need to take this into account well for starting a new verb.
            # However this wildcard state is overridden by a more specific state so that we don't accidentally
            # break an inflected verb apart.
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
        ],
        UNSPECIFIED_WORD_STATE,
        UNSPECIFIED_WORD_STATE
    )
