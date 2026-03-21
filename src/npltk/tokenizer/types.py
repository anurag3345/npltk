from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    WORD_DEV = "WORD_DEV"   # Devanagari word
    WORD_LAT = "WORD_LAT"   # Latin word (code-mix)
    NUM = "NUM"             # numbers, dates, times
    PUNCT = "PUNCT"         # punctuation
    EMOJI = "EMOJI"         # emoji-like characters (heuristic)
    SYMBOL = "SYMBOL"       # other symbols


@dataclass(frozen=True)
class Token:
    text: str
    start: int  # start offset in the input string
    end: int    # end offset (exclusive)
    type: TokenType
