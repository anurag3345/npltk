from dataclasses import dataclass

@dataclass
class NormalizerConfig:
    unicode_nfc: bool = True
    whitespace: bool = True
    invisible_chars: bool = True
    zwj_zwnj: bool = True
    halant_cleanup: bool = True
    diacritic_dedupe: bool = True
    postposition_split: bool = True