import builtins
import inspect
from unittest import mock

from textutils.truncate import truncate

MALICIOUS = "__import__('os').system('echo pwned')"


def test_truncate_short_text_unchanged():
    assert truncate("kurz", 10) == "kurz"


def test_truncate_long_text_ends_with_ellipsis_and_stays_within_limit():
    result = truncate("ein langer Text", 8)
    assert result.endswith("…")
    assert len(result) <= 8


def test_truncate_long_text_result_is_exactly_max_len():
    assert len(truncate("ein langer Text", 8)) == 8


def test_truncate_max_len_zero_returns_empty():
    assert truncate("egal", 0) == ""


def test_truncate_max_len_negative_returns_empty():
    assert truncate("egal", -1) == ""


def test_truncate_empty_string():
    assert truncate("", 5) == ""
    assert truncate("", 0) == ""


def test_truncate_max_len_one():
    assert truncate("abc", 1) == "…"


def test_truncate_treats_malicious_string_as_plain_text():
    result = truncate(MALICIOUS, len(MALICIOUS) + 10)
    assert result == MALICIOUS


def test_truncate_does_not_evaluate_or_exec_input():
    with (
        mock.patch.object(builtins, "eval", wraps=eval) as mock_eval,
        mock.patch.object(builtins, "exec", wraps=exec) as mock_exec,
    ):
        truncate(MALICIOUS, 8)
        truncate("__import__('os').getcwd()", 4)
        mock_eval.assert_not_called()
        mock_exec.assert_not_called()


def test_truncate_source_has_no_code_execution_primitives():
    source = inspect.getsource(truncate)
    for forbidden in ("eval", "exec", "compile", "subprocess"):
        assert forbidden not in source


def test_truncate_nullbyte_input():
    text = "abc\x00def"
    assert truncate(text, len(text)) == text
    result = truncate(text, 3)
    assert result.endswith("…")
    assert len(result) == 3


def test_truncate_surrogate_input():
    text = "surrog\ud800ate"
    result = truncate(text, 4)
    assert isinstance(result, str)
    assert result.endswith("…")
    assert len(result) == 4


def test_truncate_emoji_input():
    text = "Größe 😀🎉 Text"
    assert truncate(text, len(text)) == text
    result = truncate(text, 6)
    assert result.endswith("…")
    assert len(result) == 6


def test_truncate_very_long_string():
    text = "a" * 1_000_000
    result = truncate(text, 5)
    assert len(result) == 5
    assert result.endswith("…")
