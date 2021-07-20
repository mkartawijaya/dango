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
            VERB_INFLECTION_STATE
        ],
        [
            (None, ('動詞', '一般', '*', '*'), VERB_STATE),
            (None, ('動詞', '非自立可能', '*', '*'), VERB_STATE),
            (VERB_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE),
            (VERB_INFLECTION_STATE, ('助動詞', '*', '*', '*'), VERB_INFLECTION_STATE)
        ],
        UNSPECIFIED_WORD_STATE,
        UNSPECIFIED_WORD_STATE
    )
