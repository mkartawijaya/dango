# dango

`dango` is an easy to use tokenizer for Japanese text, aimed at language learners and non-linguists.

```bash
$ echo "私は昨日映画を見ました" | dango 
私 は 昨日 映画 を 見ました
```

If used as a library it can also provide you with additional information such as:

* Dictionary form: For inflected words it can tell you the dictionary form for easier lookup. 
* Part-of-speech tagging: It can tell you if a word is a verb, noun, adjective, etc.
* Reading in hiragana for words containing kanji

## Installation

```bash
$ pip install dango
```

One of the dependencies is [SudachiDict-core], which might take a while to download due to its size of ~70MB.

## Usage

A simple CLI for tokenizing text is provided. Input is read from `stdin` or from a file.

```bash
$ echo "私は昨日映画を見ました" | tee input.txt | dango
私 は 昨日 映画 を 見ました

$ dango input.txt
私 は 昨日 映画 を 見ました
```

Usage as a library: 

```python
import dango

words = dango.tokenize('私は昨日映画を見ました')

print([w.surface for w in words])
# => ['私', 'は', '昨日', '映画', 'を', '見ました']

print(words[-1].part_of_speech)
# => VERB
print(words[-1].surface)
# => 見ました
print(words[-1].surface_reading)
# => みました
print(words[-1].dictionary_form)
# => 見る
print(words[-1].dictionary_form_reading)
# => みる
```

## Motivation & Acknowledgements

`dango` was created out of a need to extract vocabulary in bulk from Japanese
texts to serve as learning materials.

While you can get quite far by using a morphological analyzer like [MeCab]
directly, there is the problem that it will segment text into much smaller
units than one would like if you are trying to learn the language.
For example `見た` would be separated into `見` and `た` which is a bit like
separating `watched` into `watch` and `ed`.

`dango` uses [SudachiPy] for tokenization/analysis and adds some processing
to aggregate the individual tokens into words and make the part-of-speech
information a bit easier to digest.

`dango` takes some inspiration from [Ve], which provides the text parsing of
[jisho.org].

## License

Released under the BSD-3-Clause License

[MeCab]: https://taku910.github.io/mecab/
[jisho.org]: https://jisho.org/
[Ve]: https://github.com/Kimtaro/ve
[SudachiPy]: https://github.com/WorksApplications/SudachiPy
[SudachiDict-core]: https://pypi.org/project/SudachiDict-core/
