from typing import List
from unittest.mock import Mock

import pytest

from dango.word import Word


def test_morphemes_property():
    morphemes = [Mock()] * 3
    word = Word(morphemes)
    assert word.morphemes == morphemes


@pytest.mark.parametrize(('surfaces', 'expected'), [
    ([], ''),
    (['見る'], '見る'),
    (['見', 'まし', 'た'], '見ました')
])
def test_surface_property(surfaces: List[str], expected: str):
    word = Word([Mock(**{'surface.return_value': s}) for s in surfaces])
    assert word.surface == expected


@pytest.mark.parametrize(('reading_forms', 'expected'), [
    ([], ''),
    (['ミル'], 'みる'),
    (['ミ', 'マシ', 'タ'], 'みました')
])
def test_surface_reading_property(reading_forms: List[str], expected: str):
    word = Word([Mock(**{'reading_form.return_value': s}) for s in reading_forms])
    assert word.surface_reading == expected


@pytest.mark.parametrize(('dictionary_forms', 'expected'), [
    ([], ''),
    (['見る'], '見る'),
    (['見る', 'ます', 'た'], '見る')
])
def test_dictionary_form_property(dictionary_forms: List[str], expected: str):
    word = Word([Mock(**{'dictionary_form.return_value': s}) for s in dictionary_forms])
    assert word.dictionary_form == expected
