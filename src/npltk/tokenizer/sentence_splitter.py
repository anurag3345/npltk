from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class SentenceSpan:
    text: str
    start: int
    end: int


DEFAULT_ENDERS: Tuple[str, ...] = ("।", "?", "!")


def split_sentences(text: str, enders: Tuple[str, ...] = DEFAULT_ENDERS) -> List[SentenceSpan]:
    """
    Simple sentence splitter for Nepali:
    - Splits on । ? !
    - Keeps the ender inside the sentence
    - Trims whitespace around each sentence span
    """
    spans: List[SentenceSpan] = []
    n = len(text)
    i = 0
    sent_start = 0

    while i < n:
        ch = text[i]
        if ch in enders:
            sent_end = i + 1

            # include trailing closing quotes/brackets if present
            while sent_end < n and text[sent_end] in ('"', "'", "”", "’", ")", "]", "}", "»"):
                sent_end += 1

            raw = text[sent_start:sent_end]

            # trim sentence whitespace but keep span aligned to original text
            ltrim = len(raw) - len(raw.lstrip())
            rtrim_len = len(raw.rstrip())
            real_start = sent_start + ltrim
            real_end = sent_start + rtrim_len

            if real_start < real_end:
                spans.append(SentenceSpan(text=text[real_start:real_end], start=real_start, end=real_end))

            sent_start = sent_end
            i = sent_end
            continue

        i += 1

    # tail sentence
    if sent_start < n:
        raw = text[sent_start:n]
        ltrim = len(raw) - len(raw.lstrip())
        rtrim_len = len(raw.rstrip())
        real_start = sent_start + ltrim
        real_end = sent_start + rtrim_len
        if real_start < real_end:
            spans.append(SentenceSpan(text=text[real_start:real_end], start=real_start, end=real_end))

    return spans
