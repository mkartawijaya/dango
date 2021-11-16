from typing import Iterable, List, Tuple, Optional, Any

from sudachipy.morpheme import Morpheme


class State:

    def on_input(self, context: Any, morpheme: Morpheme) -> None:
        pass


MorphemeFeatures = Tuple[str, str, str, str]

StateTransitionRule = Tuple[Optional[State], MorphemeFeatures, State]


def get_morpheme_features(morpheme: Morpheme) -> MorphemeFeatures:
    pos = morpheme.part_of_speech()
    return pos[0], pos[1], pos[2], pos[3]


class StateMachine:

    def __init__(
            self,
            states: List[State],
            initial_state: State,
            default_state: State,
            transitions: List[StateTransitionRule]
    ):
        self._states = frozenset(states)
        self._transitions = {}

        for src, features, dst in transitions:
            assert src is None or src in self._states
            assert dst in self._states
            self._transitions[(src, features)] = dst

        assert initial_state in self._states
        self._initial_state = initial_state

        assert default_state in self._states
        self._default_state = default_state

    def get_next_state(self, src_state: State, morpheme: Morpheme):
        features = get_morpheme_features(morpheme)

        # 1) transition from specific source state
        if (src_state, features) in self._transitions:
            return self._transitions[(src_state, features)]
        # 2) wildcard transition from any source state
        elif (None, features) in self._transitions:
            return self._transitions[(None, features)]
        # 3) fallback to default state
        else:
            return self._default_state

    def run(self, context: Any, morphemes: Iterable[Morpheme]):
        current_state = self._initial_state

        for m in morphemes:
            next_state = self.get_next_state(current_state, m)
            next_state.on_input(context, m)
            current_state = next_state

        return context
