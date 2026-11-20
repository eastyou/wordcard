from __future__ import annotations

import unittest

from wordcard.sheet import (
    EN2ZH,
    MIXED,
    ZH2EN,
    SheetError,
    build_cards,
)
from wordcard.words import Word


class BuildCardsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.words = [
            Word("apple", "苹果"),
            Word("book", "书"),
            Word("cat", "猫"),
        ]

    def test_en2zh(self) -> None:
        cards = build_cards(self.words, EN2ZH)
        self.assertEqual(cards[0].prompt, "apple")
        self.assertEqual(cards[0].answer, "苹果")
        self.assertEqual(cards[0].direction, EN2ZH)

    def test_zh2en(self) -> None:
        cards = build_cards(self.words, ZH2EN)
        self.assertEqual(cards[0].prompt, "苹果")
        self.assertEqual(cards[0].answer, "apple")

    def test_mixed_alternates(self) -> None:
        cards = build_cards(self.words, MIXED)
        self.assertEqual(
            [card.direction for card in cards],
            [EN2ZH, ZH2EN, EN2ZH],
        )

    def test_shuffle_is_deterministic(self) -> None:
        first = build_cards(self.words, EN2ZH, seed=5, shuffle=True)
        second = build_cards(self.words, EN2ZH, seed=5, shuffle=True)
        self.assertEqual(first, second)
        self.assertEqual(
            sorted(card.prompt for card in first),
            sorted(word.english for word in self.words),
        )

    def test_no_shuffle_keeps_order(self) -> None:
        cards = build_cards(self.words, EN2ZH, shuffle=False)
        self.assertEqual(
            [card.prompt for card in cards],
            ["apple", "book", "cat"],
        )

    def test_invalid_mode(self) -> None:
        with self.assertRaises(SheetError):
            build_cards(self.words, "auto")

    def test_empty_words(self) -> None:
        with self.assertRaises(SheetError):
            build_cards([], EN2ZH)


if __name__ == "__main__":
    unittest.main()
