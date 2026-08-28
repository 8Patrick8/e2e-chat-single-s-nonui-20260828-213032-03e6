from textutils import reverse_words


def test_reverse_words_three_words():
    assert reverse_words("eins zwei drei") == "drei zwei eins"


def test_reverse_words_empty():
    assert reverse_words("") == ""


def test_reverse_words_normalizes_double_whitespace():
    assert reverse_words("a  b") == "b a"


def test_reverse_words_whitespace_only():
    assert reverse_words("   ") == ""


def test_reverse_words_single_word():
    assert reverse_words("eins") == "eins"
    assert reverse_words("  nur  ") == "nur"


def test_reverse_words_tabs_and_newlines_normalized():
    assert reverse_words("a\tb\nc") == "c b a"
    assert reverse_words("  eins \n\t zwei  ") == "zwei eins"


def test_reverse_words_punctuation_stays_attached():
    assert reverse_words("Hallo, Welt!") == "Welt! Hallo,"


def test_reverse_words_malicious_code_treated_as_text():
    payload = "__import__('os').system('echo pwned')"
    assert reverse_words(payload) == " ".join(payload.split()[::-1])


def test_reverse_words_null_byte():
    assert reverse_words("a\x00b c") == "c a\x00b"


def test_reverse_words_lone_surrogate():
    assert reverse_words("\ud800") == "\ud800"


def test_reverse_words_emoji():
    assert reverse_words("👋 welt 🌍") == "🌍 welt 👋"


def test_reverse_words_very_long_string():
    long_input = " ".join([f"word{i}" for i in range(50000)])
    expected = " ".join(long_input.split()[::-1])
    assert reverse_words(long_input) == expected
