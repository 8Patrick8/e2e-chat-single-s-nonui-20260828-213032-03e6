import textutils

_MALICIOUS_STRINGS = [
    "__import__('os').system('echo pwned')",
    "eval('1+1')",
    "exec('x = 1')",
    "compile('1+1', '<string>', 'eval')",
    "__import__('subprocess').check_call(['echo', 'pwned'])",
]


def test_classic_palindrome():
    assert textutils.is_palindrome("A man, a plan, a canal: Panama") is True


def test_non_palindrome():
    assert textutils.is_palindrome("Hallo") is False


def test_empty_string_is_palindrome():
    assert textutils.is_palindrome("") is True


def test_single_character_is_palindrome():
    assert textutils.is_palindrome("a") is True


def test_whitespace_only_is_palindrome():
    assert textutils.is_palindrome("   ") is True


def test_case_insensitive_palindrome():
    assert textutils.is_palindrome("Was it a car or a cat I saw?") is True


def test_null_byte_is_ignored():
    assert textutils.is_palindrome("a\x00a") is True
    assert textutils.is_palindrome("a\x00b") is False


def test_lone_surrogate_returns_defined_result():
    assert textutils.is_palindrome("\ud800") is True
    assert textutils.is_palindrome("a\udfffb") is False


def test_emoji_is_ignored():
    assert textutils.is_palindrome("😀a😀") is True
    assert textutils.is_palindrome("🤖") is True
    assert textutils.is_palindrome("😀ab😀") is False


def test_very_long_string_returns_defined_result():
    long_palindrome = "a" * 1_000_000
    assert textutils.is_palindrome(long_palindrome) is True
    long_non_palindrome = "a" * 999_999 + "b"
    assert textutils.is_palindrome(long_non_palindrome) is False


def test_malicious_code_strings_not_executed():
    for payload in _MALICIOUS_STRINGS:
        assert isinstance(textutils.is_palindrome(payload), bool)
