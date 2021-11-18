from typing import List

import pytest

import dango


def test_empty_phrase():
    assert dango.tokenize('') == [], 'an empty phrase contains no tokens'


@pytest.mark.parametrize('expected', [
    # inflected verbs should be kept as one word
    ['昨日', '映画', 'を', '見ました'],
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
    assert [w.surface for w in dango.tokenize(''.join(expected))] == expected


# Since extracting the reading of the dictionary form depends on knowledge
# of the internal workings of SudachiPy we treat this functionality as a
# black box and just perform a smoke test if we get some plausible output.
# This test could break depending on the dictionary used as the readings
# for the words might change.
@pytest.mark.parametrize(['phrase', 'expected'], [
    ('昨日映画を見ました', ['きのう', 'えいが', 'を', 'みる']),
    ('私はその本を読んだ', ['わたくし', 'は', 'その', 'ほん', 'を', 'よむ']),
    ('東京に住んでいます', ['とうきょう', 'に', 'すむ']),
    ('この店はまだ開いてない', ['この', 'みせ', 'は', 'まだ', 'ひらく']),
    ('ラーメンを作ってみた', ['らーめん', 'を', 'つくる']),
    ('このビルは高くなかった', ['この', 'びる', 'は', 'たかい']),
    ('そのケーキはおいしそう', ['その', 'けーき', 'は', 'おいしい']),
    ('明日雨が降りそう', ['あす', 'あめ', 'が', 'ふる'])
], ids=lambda e: ''.join(e))
def test_dictionary_form_reading(phrase: str, expected: List[str]):
    assert [w.dictionary_form_reading for w in dango.tokenize(phrase)] == expected
