from textutils.slugify import slugify

_SAFE_SLUG_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")


def test_slugify_acceptance_basic():
    assert slugify("Hallo Welt!") == "hallo-welt"


def test_slugify_acceptance_umlauts():
    assert slugify("Äpfel & Übung") == "aepfel-uebung"


def test_slugify_acceptance_empty():
    assert slugify("") == ""


def test_slugify_uppercase_umlauts_transliterated():
    assert slugify("ÄÖÜ") == "aeoeue"
    assert slugify("Straße") == "strasse"


def test_slugify_collapses_consecutive_separators():
    assert slugify("a---b") == "a-b"
    assert slugify("a b c") == "a-b-c"


def test_slugify_strips_leading_and_trailing_separators():
    assert slugify("-a-b-") == "a-b"
    assert slugify("!!!") == ""
    assert slugify("---") == ""


def test_slugify_keeps_digits():
    assert slugify("ABC 123") == "abc-123"


def test_slugify_malicious_input_is_not_executed():
    malicious = '__import__("os").system("echo pwned")'
    result = slugify(malicious)
    assert result == "import-os-system-echo-pwned"
    assert set(result) <= _SAFE_SLUG_CHARS


def test_slugify_nullbyte():
    assert slugify("a\x00b") == "a-b"
    assert slugify("\x00") == ""


def test_slugify_surrogates():
    assert slugify("\ud800") == ""
    assert slugify("x\ud800y") == "x-y"


def test_slugify_emoji():
    assert slugify("Hallo 🚀 Welt") == "hallo-welt"
    assert slugify("🚀") == ""


def test_slugify_very_long_string_is_linear_and_defined():
    long_text = "ab c!" * 20_000
    result = slugify(long_text)
    assert result == "-".join(["ab-c"] * 20_000)
    assert set(result) <= _SAFE_SLUG_CHARS
    assert result == result.strip("-")
