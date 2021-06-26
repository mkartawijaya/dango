from typing import List
from unittest.mock import Mock

import pytest

from dango.dango import Word


@pytest.mark.parametrize(('surfaces', 'expected'), [
    ([], ''),
    (['見る'], '見る'),
    (['見', 'まし', 'た'], '見ました')
])
def test_surface_property(surfaces: List[str], expected: str):
    word = Word([Mock(**{'surface.return_value': s}) for s in surfaces])
    assert word.surface == expected
