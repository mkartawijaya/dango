import pytest

from dango.util import katakana_to_hiragana

KATAKANA = (
    'ァアィイゥウェエォオカガキギク'
    'グケゲコゴサザシジスズセゼソゾタ'
    'ダチヂッツヅテデトドナニヌネノハ'
    'バパヒビピフブプヘベペホボポマミ'
    'ムメモャヤュユョヨラリルレロヮワ'
    'ヰヱヲンヴヵヶヽヾ'
)

HIRAGANA = (
    'ぁあぃいぅうぇえぉおかがきぎく'
    'ぐけげこごさざしじすずせぜそぞた'
    'だちぢっつづてでとどなにぬねのは'
    'ばぱひびぴふぶぷへべぺほぼぽまみ'
    'むめもゃやゅゆょよらりるれろゎわ'
    'ゐゑをんゔゕゖゝゞ'
)


@pytest.mark.parametrize(['string', 'expected'], [
    ('This string contains no kana or kanji.', 'This string contains no kana or kanji.'),
    ('A mix of 漢字, ひらがな and カタカナ.', 'A mix of 漢字, ひらがな and かたかな.'),
    ('このビルは高い', 'このびるは高い'),
    ('そのケーキはおいしそう', 'そのけーきはおいしそう'),
    ('ラーメン', 'らーめん'),
    (KATAKANA, HIRAGANA)
])
def test_katakana_to_hiragana(string: str, expected: str):
    assert katakana_to_hiragana(string) == expected
