import pytest

from dango import tokenize


@pytest.mark.parametrize(('phrase', 'expected'), [
    ('昨日映画お見ました', ['昨日', '映画', 'お', '見', 'まし', 'た'])
])
def test_tokenize(phrase: str, expected: str):
    assert expected == [w.surface for w in tokenize(phrase)]
