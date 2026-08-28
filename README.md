# textutils

textutils ist eine kleine, eigenständige Python-Bibliothek mit fünf einfachen, unabhängigen String-Hilfsfunktionen: `slugify`, `truncate`, `word_count`, `is_palindrome` und `reverse_words`. Reine Backend-Bibliothek ohne UI und ohne Framework — jede Funktion ist minimal gehalten und über die Paket-Fassade `textutils/__init__.py` zugänglich.

## Tech-Stack

- Python 3, ausschließlich Standardbibliothek
- pytest als Test-Runner

## Installation

```bash
python -m pip install pytest
```

Das Paket selbst hat keine weiteren Abhängigkeiten — es nutzt nur die Python-Standardbibliothek.

## Ausführung

Tests ausführen:

```bash
python -m pytest
```

Import der öffentlichen API prüfen:

```bash
python -c "from textutils import slugify, truncate, word_count, is_palindrome, reverse_words"
```

## Hinweis zu RUN.json

Wie dieses Produkt gestartet und geprüft wird, ist maschinenlesbar in `RUN.json` im Repository-Stamm hinterlegt: Der Dienst `textutils` wird als CLI-Dienst mit `python -m pytest` gestartet — ein erfolgreicher Exit-Code 0 gilt als gesunder Start. Als manueller Schnellcheck, dass das Paket importierbar ist, dient der Import aus dem Abschnitt „Ausführung".
