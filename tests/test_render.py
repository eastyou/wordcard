from __future__ import annotations

import unittest

from wordcard.render import render_sheet
from wordcard.sheet import EN2ZH, MIXED, ZH2EN, Card, SheetError
from wordcard.words import Word


class RenderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cards = [
            Card("apple", "苹果", EN2ZH),
            Card("书", "book", ZH2EN),
            Card("cat", "猫", EN2ZH),
        ]

    def test_content(self) -> None:
        page = render_sheet(self.cards, "第一单元")
        self.assertIn("第一单元", page)
        self.assertIn("apple", page)
        self.assertIn("苹果", page)
        self.assertIn("参考答案", page)
        self.assertIn("英→中", page)
        self.assertIn("中→英", page)

    def test_columns(self) -> None:
        page = render_sheet(self.cards, columns=3)
        self.assertIn("repeat(3, minmax(0, 1fr))", page)

    def test_invalid_columns(self) -> None:
        with self.assertRaises(SheetError):
            render_sheet(self.cards, columns=0)
        with self.assertRaises(SheetError):
            render_sheet(self.cards, columns=4)

    def test_no_answers(self) -> None:
        page = render_sheet(self.cards, include_answers=False)
        self.assertNotIn("参考答案", page)

    def test_title_escaped(self) -> None:
        page = render_sheet(self.cards, "<i>测试</i>")
        self.assertNotIn("<i>测试</i>", page)
        self.assertIn("&lt;i&gt;", page)

    def test_empty_cards(self) -> None:
        with self.assertRaises(SheetError):
            render_sheet([])

    def test_mixed_directions(self) -> None:
        words = [Word("apple", "苹果"), Word("book", "书")]
        from wordcard.sheet import build_cards

        cards = build_cards(words, MIXED)
        page = render_sheet(cards)
        self.assertIn("英→中", page)
        self.assertIn("中→英", page)


if __name__ == "__main__":
    unittest.main()
