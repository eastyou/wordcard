"""默写卡片的模式与顺序。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Sequence

from .words import Word

EN2ZH = "en2zh"
ZH2EN = "zh2en"
MIXED = "mixed"
MODES = (EN2ZH, ZH2EN, MIXED)
MODE_LABELS = {
    EN2ZH: "看英文写中文",
    ZH2EN: "看中文写英文",
    MIXED: "英中交替",
}


class SheetError(ValueError):
    """排版参数不合法。"""


@dataclass(frozen=True)
class Card:
    prompt: str
    answer: str
    direction: str


def build_cards(
    words: Sequence[Word],
    mode: str = EN2ZH,
    seed: int = 2026,
    shuffle: bool = False,
) -> List[Card]:
    """按模式生成卡片列表。"""
    if mode not in MODES:
        raise SheetError("模式只能是 en2zh、zh2en 或 mixed")
    if not words:
        raise SheetError("至少需要一个单词")

    ordered = list(words)
    if shuffle:
        random.Random(seed).shuffle(ordered)

    cards: List[Card] = []
    for index, word in enumerate(ordered):
        direction = mode
        if mode == MIXED:
            direction = EN2ZH if index % 2 == 0 else ZH2EN
        if direction == EN2ZH:
            cards.append(Card(word.english, word.chinese, EN2ZH))
        else:
            cards.append(Card(word.chinese, word.english, ZH2EN))
    return cards


__all__ = [
    "Card",
    "EN2ZH",
    "MIXED",
    "MODE_LABELS",
    "MODES",
    "SheetError",
    "ZH2EN",
    "build_cards",
]
