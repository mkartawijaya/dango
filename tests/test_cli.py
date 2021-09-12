import io
import sys
from unittest.mock import patch, mock_open

from _pytest.capture import CaptureFixture
from _pytest.monkeypatch import MonkeyPatch

import dango.cli


def test_reading_from_stdin(capsys: CaptureFixture, monkeypatch: MonkeyPatch):
    monkeypatch.setattr('sys.argv', ['dango'])
    monkeypatch.setattr('sys.stdin', io.StringIO('私は昨日映画を見ました\n東京に住んでいます\n明日雨が降りそう'))

    dango.cli.main()
    out, err = capsys.readouterr()

    assert err == ''
    assert out == '私 は 昨日 映画 を 見ました\n東京 に 住んでいます\n明日 雨 が 降りそう\n'


def test_reading_from_file(capsys: CaptureFixture, monkeypatch: MonkeyPatch):
    monkeypatch.setattr('sys.argv', ['dango', 'input.txt'])

    read_data = '私は昨日映画を見ました\n東京に住んでいます\n明日雨が降りそう'
    mock = mock_open(read_data=read_data)

    # The mock returned by mock_open does not support iteration i.e. "for line in file" in Python < 3.7
    # see: https://stackoverflow.com/a/24779923
    # see: https://bugs.python.org/issue21258
    if sys.version_info < (3, 7):
        mock.return_value.__iter__ = lambda self: iter(read_data.splitlines())

    with patch('builtins.open', mock):
        dango.cli.main()

    out, err = capsys.readouterr()

    assert err == ''
    assert out == '私 は 昨日 映画 を 見ました\n東京 に 住んでいます\n明日 雨 が 降りそう\n'
