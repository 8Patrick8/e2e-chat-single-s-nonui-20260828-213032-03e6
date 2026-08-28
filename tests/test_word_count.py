import builtins
import inspect
from unittest import mock

from textutils.word_count import word_count

MALICIOUS = "__import__('os').system('echo pwned')"


def test_word_count_simple_sentence():
    assert word_count("eins zwei drei") == 3


def test_word_count_whitespace_only():
    assert word_count("   ") == 0


def test_word_count_empty_string():
    assert word_count("") == 0


def test_word_count_leading_trailing_whitespace():
    assert word_count("  eins zwei drei  ") == 3


def test_word_count_multiple_and_mixed_whitespace():
    assert word_count("a\nb  c\t d") == 4


def test_word_count_newline_separated():
    assert word_count("a\nb  c") == 3


def test_word_count_single_word():
    assert word_count("wort") == 1


def test_word_count_malicious_string_is_plain_text():
    assert word_count(MALICIOUS) == len(MALICIOUS.split())


def test_word_count_does_not_evaluate_or_exec_input():
    with (
        mock.patch.object(builtins, "eval", wraps=eval) as mock_eval,
        mock.patch.object(builtins, "exec", wraps=exec) as mock_exec,
    ):
        word_count(MALICIOUS)
        word_count("__import__('os').getcwd()")
        mock_eval.assert_not_called()
        mock_exec.assert_not_called()


def test_word_count_source_has_no_code_execution_primitives():
    source = inspect.getsource(word_count)
    for forbidden in ("eval", "exec", "compile", "subprocess"):
        assert forbidden not in source


def test_word_count_nullbyte_input():
    assert word_count("a\x00b") == 1
    assert word_count("a\x00 b") == 2


def test_word_count_surrogate_input():
    text = "surrog\ud800ate"
    assert word_count(text) == 1
    assert word_count("surrog \ud800ate") == 2


def test_word_count_emoji_input():
    text = "Größe 😀🎉 Text"
    assert word_count(text) == 3
    assert word_count("😀🎉") == 1


def test_word_count_very_long_string():
    text = "a " * 500_000
    assert word_count(text) == 500_000
