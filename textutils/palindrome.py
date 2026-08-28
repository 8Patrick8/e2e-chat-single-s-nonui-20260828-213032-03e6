import re

_NON_ALNUM = re.compile(r"[^a-z0-9]")


def is_palindrome(text: str) -> bool:
    normalized = _NON_ALNUM.sub("", text.lower())
    return normalized == normalized[::-1]
