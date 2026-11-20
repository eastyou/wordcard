from __future__ import annotations

import os
import tempfile
import unittest

from wordcard.words import WordError, load_words, parse_words


class ParseWordsTest(unittest.TestCase):
    def test_basic(self) -> None:
        words = parse_words("英文,中文\napple,苹果\nbook,书\n")
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0].english, "apple")
        self.assertEqual(words[0].chinese, "苹果")

    def test_english_header(self) -> None:
        words = parse_words("word,meaning\napple,苹果\n")
        self.assertEqual(words[0].english, "apple")

    def test_extra_column_allowed(self) -> None:
        words = parse_words("英文,音标,中文\napple,/ˈæpl/,苹果\n")
        self.assertEqual(words[0].chinese, "苹果")

    def test_duplicate_word(self) -> None:
        with self.assertRaises(WordError):
            parse_words("英文,中文\napple,苹果\nApple,苹果\n")

    def test_empty_cell(self) -> None:
        with self.assertRaises(WordError):
            parse_words("英文,中文\napple,\n")
        with self.assertRaises(WordError):
            parse_words("英文,中文\n,苹果\n")

    def test_column_count(self) -> None:
        with self.assertRaises(WordError):
            parse_words("英文,中文\napple\n")

    def test_missing_header(self) -> None:
        with self.assertRaises(WordError):
            parse_words("abc,def\napple,苹果\n")

    def test_single_row(self) -> None:
        with self.assertRaises(WordError):
            parse_words("英文,中文\n")

    def test_load_with_bom(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "words.csv")
            with open(path, "w", encoding="utf-8-sig") as handle:
                handle.write("英文,中文\napple,苹果\n")
            words = load_words(path)
        self.assertEqual(words[0].english, "apple")

    def test_load_missing_file(self) -> None:
        with self.assertRaises(WordError):
            load_words("/tmp/definitely-not-here-12345.csv")


if __name__ == "__main__":
    unittest.main()
