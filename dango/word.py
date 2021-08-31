from enum import Enum, auto
from typing import List

from pygtrie import Trie
from sudachipy.morpheme import Morpheme

from .util import katakana_to_hiragana


class PartOfSpeech(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name

    ADJECTIVAL_NOUN = auto()
    ADJECTIVE = auto()
    ADVERB = auto()
    AUXILIARY_VERB = auto()
    CONJUNCTION = auto()
    COUNTER = auto()
    INTERJECTION = auto()
    NAME = auto()
    NOUN = auto()
    NUMBER = auto()
    PARTICLE = auto()
    PLACE_NAME = auto()
    PREFIX = auto()
    PRE_NOUN_ADJECTIVAL = auto()
    PRONOUN = auto()
    SUFFIX = auto()
    SYMBOL = auto()
    UNKNOWN = auto()
    VERB = auto()
    WHITESPACE = auto()


POS_MAPPING = Trie([
    (['代名詞'], PartOfSpeech.PRONOUN),
    (['副詞'], PartOfSpeech.ADVERB),

    # These are not really auxiliary verbs in the common sense, but rather the okurigana that represent the inflection.
    # Words with this POS should never really occur on their own in the result. But this mapping is included in case
    # one of them slips through the aggregation process.
    (['助動詞'], PartOfSpeech.AUXILIARY_VERB),

    (['助詞'], PartOfSpeech.PARTICLE),

    (['動詞'], PartOfSpeech.VERB),

    (['名詞'], PartOfSpeech.NOUN),
    (['名詞', '固有名詞', '人名'], PartOfSpeech.NAME),
    (['名詞', '固有名詞', '地名'], PartOfSpeech.PLACE_NAME),
    (['名詞', '数詞'], PartOfSpeech.NUMBER),
    (['名詞', '普通名詞', '助数詞可能'], PartOfSpeech.COUNTER),

    (['形容詞'], PartOfSpeech.ADJECTIVE),
    (['形状詞'], PartOfSpeech.ADJECTIVAL_NOUN),
    (['感動詞'], PartOfSpeech.INTERJECTION),
    (['接尾辞'], PartOfSpeech.SUFFIX),
    (['接尾辞', '名詞的', '助数詞'], PartOfSpeech.COUNTER),

    (['接続詞'], PartOfSpeech.CONJUNCTION),
    (['接頭辞'], PartOfSpeech.PREFIX),
    (['空白'], PartOfSpeech.WHITESPACE),
    (['補助記号'], PartOfSpeech.SYMBOL),
    (['記号'], PartOfSpeech.SYMBOL),
    (['連体詞'], PartOfSpeech.PRE_NOUN_ADJECTIVAL)
])


class Word:

    def __init__(self, morphemes: List[Morpheme], dictionary_form_reading: str = None):
        self._morphemes = morphemes
        self.dictionary_form_reading = dictionary_form_reading

    @property
    def morphemes(self) -> List[Morpheme]:
        """The morphemes the word is made up of."""
        return self._morphemes

    @property
    def surface(self) -> str:
        """The surface representation of the word."""
        return ''.join(m.surface() for m in self._morphemes)

    @property
    def surface_reading(self) -> str:
        """The kana reading of the surface representation."""
        return katakana_to_hiragana(''.join(m.reading_form() for m in self._morphemes))

    @property
    def dictionary_form(self) -> str:
        """The the dictionary form of the word."""
        return self._morphemes[0].dictionary_form() if self._morphemes else ''

    @property
    def part_of_speech(self) -> PartOfSpeech:
        return POS_MAPPING.longest_prefix(self.morphemes[0].part_of_speech()[:4]).value or PartOfSpeech.UNKNOWN
