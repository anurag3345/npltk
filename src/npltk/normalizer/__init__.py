from .core import Normalizer, NormResult
from .config import NormalizerConfig
from .rules import (
    UnicodeNFC,
    WhitespaceNormalize,
    RemoveInvisibleChars,
    ZWJZWNJCleanup,
    HalantCleanup,
    DiacriticDedupe,
    PostpositionSplit,
)

def build_normalizer(cfg: NormalizerConfig | None = None) -> Normalizer:
    cfg = cfg or NormalizerConfig()
    rules = []

    if cfg.unicode_nfc:
        rules.append(UnicodeNFC())
    if cfg.whitespace:
        rules.append(WhitespaceNormalize())
    if cfg.invisible_chars:
        rules.append(RemoveInvisibleChars())
    if cfg.zwj_zwnj:
        rules.append(ZWJZWNJCleanup())
    if cfg.halant_cleanup:
        rules.append(HalantCleanup())
    if cfg.diacritic_dedupe:
        rules.append(DiacriticDedupe())
    if cfg.postposition_split:
        rules.append(PostpositionSplit())

    return Normalizer(rules)