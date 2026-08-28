import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")
_UMLAUT_TABLE = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})


def slugify(text: str) -> str:
    transliterated = text.lower().translate(_UMLAUT_TABLE)
    return _NON_ALNUM.sub("-", transliterated).strip("-")
