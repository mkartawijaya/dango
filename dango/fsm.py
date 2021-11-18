from typing import Iterable, List, Tuple, Optional, Any

from sudachipy.morpheme import Morpheme


class State:
    """Interface for any states a StateMachine can be constructed with."""

    def on_input(self, context: Any, morpheme: Morpheme) -> None:
        """Processes the current input.

        Args:
            context: The current context. Its type and shape depends on the concrete state implementation.
            morpheme: The current input.
        """
        pass


MorphemeFeatures = Tuple[str, str, str, str]

StateTransitionRule = Tuple[Optional[State], MorphemeFeatures, State]


def get_morpheme_features(morpheme: Morpheme) -> MorphemeFeatures:
    """Returns the relevant features from a morpheme.

    Args:
        morpheme: The morpheme to extract features from.
    """
    pos = morpheme.part_of_speech()
    return pos[0], pos[1], pos[2], pos[3]


class StateMachine:
    """A finite-state machine that can be used to process a stream of morphemes.

    Other than consuming the provided input and managing state transitions the
    state machine does no processing of its own. Any logic for operating on the
    input has to be provided by the states a state machine is constructed with.
    """

    def __init__(
            self,
            states: List[State],
            initial_state: State,
            default_state: State,
            transitions: List[StateTransitionRule]
    ):
        """Constructs a state machine from the given specification.

        Args:
            states:
                The set of states the state machine could possibly enter.
            initial_state:
                The initial state to start in when this state machine is run.
                This state has to be a member of the set of possible states.
            default_state:
                A state to fall back on if there is no matching transition
                for the current state and input. This state has to be a
                member of the set of possible states.
            transitions:
                The transitions rules the state machine will operate with.
                All source and destination states specified in the rules
                have to be members of the set of possible states.
        """
        self._states = frozenset(states)
        self._transitions = {}

        # construct internal transition table for faster lookup.
        for src, features, dst in transitions:
            assert src is None or src in self._states
            assert dst in self._states
            self._transitions[(src, features)] = dst

        assert initial_state in self._states
        self._initial_state = initial_state

        assert default_state in self._states
        self._default_state = default_state

    def get_next_state(self, source_state: State, morpheme: Morpheme):
        """Returns the next state to advance to.

        The next state is determined based on the source state and current input depending
        on the set of transition rules the state machine was constructed with.
        If there is no matching transition for the inputs the default state is returned.

        Args:
            source_state: The source state for the transition.
            morpheme: The input on which to transition.
        """
        features = get_morpheme_features(morpheme)

        # 1) transition from specific source state
        if (source_state, features) in self._transitions:
            return self._transitions[(source_state, features)]
        # 2) wildcard transition from any source state
        elif (None, features) in self._transitions:
            return self._transitions[(None, features)]
        # 3) fallback to default state
        else:
            return self._default_state

    def run(self, context: Any, morphemes: Iterable[Morpheme]) -> Any:
        """Runs the state machine on a stream of morphemes.

        Args:
            context: The context to provide to the states for processing.
            morphemes: The stream of morphemes to process.

        Returns:
            The context after processing of all input is complete.
        """
        current_state = self._initial_state

        for m in morphemes:
            next_state = self.get_next_state(current_state, m)
            next_state.on_input(context, m)
            current_state = next_state

        return context
