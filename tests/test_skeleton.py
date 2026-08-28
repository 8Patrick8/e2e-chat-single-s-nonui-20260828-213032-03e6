import inspect

import textutils

EXPECTED_CONTRACT = {
    "slugify": (("text",), "str"),
    "truncate": (("text", "max_len"), "str"),
    "word_count": (("text",), "int"),
    "is_palindrome": (("text",), "bool"),
    "reverse_words": (("text",), "str"),
}


def test_import_facade_is_importable():
    assert textutils is not None


def test_all_functions_exported_and_callable():
    for name in EXPECTED_CONTRACT:
        assert callable(getattr(textutils, name)), f"textutils.{name} is not callable"


def test_signatures_match_contract():
    for name, (params, return_name) in EXPECTED_CONTRACT.items():
        func = getattr(textutils, name)
        sig = inspect.signature(func)
        assert tuple(sig.parameters) == params, f"textutils.{name} has unexpected parameters"
        assert sig.return_annotation.__name__ == return_name, (
            f"textutils.{name} has unexpected return annotation"
        )
