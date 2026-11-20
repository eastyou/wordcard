"""命令行入口：生成英语单词默写纸。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .render import render_sheet
from .sheet import MODE_LABELS, MODES, SheetError, build_cards
from .words import WordError, load_words


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcard",
        description="英语单词默写纸：读单词表 CSV，输出可打印的 A4 默写卡",
    )
    parser.add_argument("--version", action="version", version="wordcard 0.1.0")
    parser.add_argument("-i", "--input", required=True, help="单词表 CSV")
    parser.add_argument(
        "-o", "--html", default="wordcard.html", help="输出 HTML 路径"
    )
    parser.add_argument("--title", default="英语单词默写", help="页面标题")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="en2zh",
        help="en2zh 看英文写中文，zh2en 看中文写英文，mixed 交替",
    )
    parser.add_argument("--columns", type=int, default=2, help="每行几列，1~3")
    parser.add_argument("--seed", type=int, default=2026, help="随机种子")
    parser.add_argument("--shuffle", action="store_true", help="打乱单词顺序")
    parser.add_argument(
        "--no-answers", action="store_true", help="不生成答案页"
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.title.strip():
        print("错误: 页面标题不能为空", file=sys.stderr)
        return 2
    if not 1 <= args.columns <= 3:
        print("错误: 列数必须在 1 到 3 之间", file=sys.stderr)
        return 2

    try:
        words = load_words(args.input)
        cards = build_cards(words, args.mode, args.seed, args.shuffle)
        page = render_sheet(
            cards,
            args.title,
            args.columns,
            include_answers=not args.no_answers,
        )
    except (WordError, SheetError) as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    try:
        Path(args.html).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1

    print(
        "已生成 %s：%d 个单词（%s），%d 列"
        % (
            args.html,
            len(cards),
            MODE_LABELS[args.mode],
            args.columns,
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
