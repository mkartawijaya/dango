from typing import List

import pytest

from dango import tokenize


@pytest.mark.parametrize('expected', [
    # inflected verbs should be kept as one word
    ['昨日', '映画', 'お', '見ました'],
    ['私', 'は', '本', 'を', '読む'],
    ['私', 'は', '本', 'を', '読まない'],
    ['私', 'は', '本', 'を', '読んだ'],
    ['私', 'は', '本', 'を', '読まなかった'],
    ['私', 'は', '本', 'を', '読みます'],
    ['私', 'は', '本', 'を', '読みました'],
    ['私', 'は', '本', 'を', '読みません'],
    ['私', 'は', '本', 'を', '読みませんでした'],
    ['東京', 'に', '住んでいる'],
    ['東京', 'に', '住んでる'],
    ['東京', 'に', '住んでいます'],
    ['東京', 'に', '住んでます'],
    ['この', '店', 'は', 'まだ', '開いていない'],
    ['この', '店', 'は', 'まだ', '開いてない'],
    ['この', '店', 'は', 'まだ', '開いていません'],
    ['この', '店', 'は', 'まだ', '開いてません'],
    ['ラーメン', 'を', '作ってみた'],
    # inflected adjectives should be kept as one word as well
    ['この', 'ビル', 'は', '高い'],
    ['この', 'ビル', 'は', '高くない'],
    ['この', 'ビル', 'は', '高かった'],
    ['この', 'ビル', 'は', '高くなかった'],
    # seems/looks-like suffixes should be kept with their verb/adjective
    ['その', 'ケーキ', 'は', 'おいしそう'],
    ['明日', '雨', 'が', '降りそう']
], ids=lambda e: ''.join(e))
def test_tokenize(expected: List[str]):
    assert expected == [w.surface for w in tokenize(''.join(expected))]
