from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List

DEVANAGARI_WORD = re.compile(r"^[\u0900-\u097F]+$")

SPACE_MAP = {
    "\u00A0": " ",  # NBSP
    "\u202F": " ",  # narrow NBSP
    "\u2009": " ",  # thin space
    "\u200B": "",   # ZWSP
    "\uFEFF": "",   # BOM
}

POSTPOSITIONS = sorted({
    "देखि", "सम्म", "बाट", "लाई", "सँग",
    "को", "का", "की",
    "मा", "ले", "त", "नि", "नै",
    "हरू",
}, key=len, reverse=True)


@dataclass
class UnicodeNFC:
    name: str = "unicode_nfc"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        out = unicodedata.normalize("NFC", text)
        return out, {}


@dataclass
class WhitespaceNormalize:
    name: str = "whitespace_normalize"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        for k, v in SPACE_MAP.items():
            text = text.replace(k, v)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()
        return text, {"changed": before != text}


@dataclass
class RemoveInvisibleChars:
    name: str = "remove_invisible_chars"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        removed = 0
        out_chars = []
        for ch in text:
            cat = unicodedata.category(ch)
            if cat == "Cc" and ch not in ("\n", "\t"):
                removed += 1
                continue
            out_chars.append(ch)
        out = "".join(out_chars)
        return out, {"removed": removed, "changed": before != out}


@dataclass
class ZWJZWNJCleanup:
    name: str = "zwj_zwnj_cleanup"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        out = text.replace("\u200D", "").replace("\u200C", "")
        return out, {"changed": before != out}


@dataclass
class HalantCleanup:
    name: str = "halant_cleanup"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        text = re.sub(r"्\s+", "्", text)   # halant + spaces
        text = re.sub(r"्{2,}", "्", text)  # repeated halant
        return text, {"changed": before != text}


@dataclass
class DiacriticDedupe:
    name: str = "diacritic_dedupe"
    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        text = re.sub(r"ं{2,}", "ं", text)
        text = re.sub(r"ँ{2,}", "ँ", text)
        return text, {"changed": before != text}


@dataclass
class PostpositionSplit:
    name: str = "postposition_split"
    min_root_len: int = 2

    def apply(self, text: str) -> Tuple[str, Dict[str, Any]]:
        before = text
        tokens = text.split(" ")
        out: List[str] = []
        splits = 0

        for tok in tokens:
            if not tok or not DEVANAGARI_WORD.match(tok) or len(tok) < 3:
                out.append(tok)
                continue

            did_split = False
            for suf in POSTPOSITIONS:
                if tok.endswith(suf) and len(tok) > len(suf) + self.min_root_len - 1:
                    root = tok[:-len(suf)]
                    if len(root) >= self.min_root_len:
                        out.extend([root, suf])
                        splits += 1
                        did_split = True
                        break

            if not did_split:
                out.append(tok)

        after = " ".join(out)
        return after, {"splits": splits, "changed": before != after}