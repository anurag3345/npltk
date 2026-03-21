from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol


@dataclass
class Transform:
    rule: str
    before: str
    after: str
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormResult:
    text: str
    transforms: List[Transform] = field(default_factory=list)


class Rule(Protocol):
    name: str
    def apply(self, text: str) -> tuple[str, Dict[str, Any]]:
        ...


class Normalizer:
    """Applies a list of rules sequentially and records transformations."""
    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def normalize(self, text: str) -> NormResult:
        current = text
        transforms: List[Transform] = []

        for rule in self.rules:
            updated, meta = rule.apply(current)
            if updated != current:
                transforms.append(Transform(rule=rule.name, before=current, after=updated, meta=meta))
            current = updated

        return NormResult(text=current, transforms=transforms)