"""单词表读取与校验。"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


class WordError(ValueError):
    """单词表内容不合法。"""


@dataclass(frozen=True)
class Word:
    english: str
    chinese: str


ENGLISH_KEYS = {"英文", "英语", "单词", "word", "english"}
CHINESE_KEYS = {"中文", "释义", "意思", "meaning", "chinese"}


def load_words(path: Union[str, Path]) -> List[Word]:
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise WordError("单词表不存在: %s" % file_path) from None
    except UnicodeDecodeError:
        raise WordError(
            "单词表不是 UTF-8 编码，请用 Excel「另存为 CSV UTF-8」"
        ) from None
    except OSError as exc:
        raise WordError("读取单词表失败: %s" % exc) from None
    return parse_words(text)


def parse_words(text: str) -> List[Word]:
    rows = [
        row
        for row in csv.reader(text.splitlines())
        if row and any(cell.strip() for cell in row)
    ]
    if len(rows) < 2:
        raise WordError("单词表至少需要一行表头和一行单词")

    header = [cell.strip().lower() for cell in rows[0]]
    english_index = None
    chinese_index = None
    for index, cell in enumerate(header):
        if cell in ENGLISH_KEYS:
            english_index = index
        elif cell in CHINESE_KEYS:
            chinese_index = index
    if english_index is None or chinese_index is None:
        raise WordError("表头需要包含「英文」和「中文」两列")

    words: List[Word] = []
    seen = set()
    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(header):
            raise WordError(
                "第 %d 行有 %d 列，应与表头的 %d 列一致"
                % (line_number, len(row), len(header))
            )
        english = row[english_index].strip()
        chinese = row[chinese_index].strip()
        if not english or not chinese:
            raise WordError("第 %d 行英文或中文为空" % line_number)
        key = english.lower()
        if key in seen:
            raise WordError("第 %d 行单词重复: %s" % (line_number, english))
        seen.add(key)
        words.append(Word(english, chinese))

    if not words:
        raise WordError("单词表里没有有效单词")
    return words


__all__ = ["Word", "WordError", "load_words", "parse_words"]
