from __future__ import annotations

import re
from typing import List

from .types import Token, TokenType


# Unicode blocks
DEV_RANGE = r"\u0900-\u0963\u0966-\u097F"  # Devanagari
NEP_DIGIT = r"\u0966-\u096F"   # Nepali digits ०-९

# Punctuation/symbol chars we want as separate tokens
# (includes Nepali danda, quotes, brackets, dashes, etc.)
PUNCT_CHARS = r"""।!?.,;:…—–\-(){}\[\]<>«»"“”'‘’/\\|@#%^&*_+=~`"""

# Basic URL pattern (optional but helpful)
URL_RE = re.compile(r"(?P<URL>(https?://|www\.)\S+)", re.IGNORECASE)


def _is_emojiish(ch: str) -> bool:
    """Heuristic emoji detector (good enough for toolkit use)."""
    code = ord(ch)
    return (
        0x1F300 <= code <= 0x1FAFF  # emoji blocks
        or 0x2600 <= code <= 0x26FF  # misc symbols
        or 0x2700 <= code <= 0x27BF  # dingbats
    )


def _build_master_pattern() -> re.Pattern:
    # Order matters: URLs first, then numbers, then devanagari/latin, then punct, then whitespace, then other.
    url = r"(?P<URL>(https?://|www\.)\S+)"
    number = rf"(?P<NUMBER>[\d{NEP_DIGIT}]+(?:[,\.:/-][\d{NEP_DIGIT}]+)*)"
    dev_word = rf"(?P<DEVWORD>[{DEV_RANGE}]+)"
    lat_word = r"(?P<LATWORD>[A-Za-z]+(?:'[A-Za-z]+)?)"
    punct = rf"(?P<PUNCT>[{re.escape(PUNCT_CHARS)}])"
    ws = r"(?P<WS>\s+)"
    other = r"(?P<OTHER>.)"

    master = "|".join([url, number, dev_word, lat_word, punct, ws, other])
    return re.compile(master)


_MASTER = _build_master_pattern()


def tokenize_words(text: str, *, keep_punct: bool = True) -> List[Token]:
    """
    Rule-based word tokenizer.
    - Works on normalized text.
    - Returns tokens with spans and types.
    """
    tokens: List[Token] = []

    for m in _MASTER.finditer(text):
        kind = m.lastgroup
        val = m.group(0)
        start, end = m.start(), m.end()

        if kind == "WS":
            continue

        if kind == "URL":
            # treat URL as a SYMBOL token (or add a URL type later)
            tokens.append(Token(val, start, end, TokenType.SYMBOL))
        elif kind == "NUMBER":
            tokens.append(Token(val, start, end, TokenType.NUM))
        elif kind == "DEVWORD":
            tokens.append(Token(val, start, end, TokenType.WORD_DEV))
        elif kind == "LATWORD":
            tokens.append(Token(val, start, end, TokenType.WORD_LAT))
        elif kind == "PUNCT":
            if keep_punct:
                tokens.append(Token(val, start, end, TokenType.PUNCT))
        else:
            # OTHER: emoji/symbol/unknown
            if _is_emojiish(val):
                tokens.append(Token(val, start, end, TokenType.EMOJI))
            else:
                tokens.append(Token(val, start, end, TokenType.SYMBOL))

    return tokens
