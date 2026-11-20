"""生成可打印的单词默写纸。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .sheet import Card, EN2ZH, SheetError

PAGE_CSS = """
  @page { size: A4 portrait; margin: 12mm; }
  * { box-sizing: border-box; }
  body {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    color: #202124;
    margin: 0;
    padding: 12mm;
    background: #fff;
    font-size: 14px;
  }
  h1 { font-size: 22px; text-align: center; margin: 0 0 6px; }
  .meta { display: flex; justify-content: space-between; font-size: 13px; color: #3c4043; margin: 12px 0 4px; }
  .summary { text-align: center; color: #5f6368; font-size: 12px; margin-bottom: 16px; }
  .page-break { break-before: page; page-break-before: always; }
  .grid { display: grid; gap: 10px; }
  .card { border: 1px solid #d0d5dd; border-radius: 6px; padding: 8px 10px 10px; break-inside: avoid; }
  .card .top { display: flex; justify-content: space-between; color: #80868b; font-size: 11px; }
  .tag { color: #1a73e8; }
  .prompt { font-size: 16px; font-weight: 600; margin: 2px 0 6px; min-height: 24px; }
  .line { border-bottom: 1px solid #c4c9d0; height: 22px; }
  h2 { font-size: 18px; margin: 0 0 12px; }
  .answer-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 18px; font-size: 13px; }
  .answer-grid div { break-inside: avoid; }
  .answer-grid .en { font-weight: 600; }
  @media screen {
    body { background: #f7f8fa; }
    .sheet, .answers { background: #fff; padding: 12mm; margin-bottom: 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
  }
  @media print {
    body { padding: 0; background: #fff; }
    .sheet, .answers { padding: 0; margin: 0; box-shadow: none; }
    .grid { gap: 8px; }
  }
"""


def render_sheet(
    cards: Sequence[Card],
    title: str = "英语单词默写",
    columns: int = 2,
    include_answers: bool = True,
) -> str:
    if not cards:
        raise SheetError("没有单词可以生成默写纸")
    if not 1 <= columns <= 3:
        raise SheetError("列数必须在 1 到 3 之间")

    grid_style = "grid-template-columns: repeat(%d, minmax(0, 1fr));" % columns
    items: List[str] = []
    for index, card in enumerate(cards, start=1):
        tag = "英→中" if card.direction == EN2ZH else "中→英"
        items.append(
            '<div class="card">'
            '<div class="top"><span>%d</span><span class="tag">%s</span></div>'
            '<div class="prompt">%s</div>'
            '<div class="line"></div><div class="line"></div>'
            "</div>"
            % (index, tag, html.escape(card.prompt))
        )

    body = (
        '<section class="sheet">'
        "<h1>%s</h1>"
        '<div class="meta"><span>姓名：__________</span>'
        "<span>班级：__________</span><span>日期：__________</span></div>"
        '<div class="summary">共 %d 个单词 · 默写后对照答案自批</div>'
        '<div class="grid" style="%s">%s</div></section>'
        % (
            html.escape(title),
            len(cards),
            grid_style,
            "".join(items),
        )
    )

    if include_answers:
        body += (
            '<div class="page-break"></div>'
            '<section class="answers"><h2>参考答案</h2>'
            '<div class="answer-grid">%s</div></section>' % _render_answers(cards)
        )

    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n"
        % (html.escape(title), PAGE_CSS, body)
    )


def _render_answers(cards: Sequence[Card]) -> str:
    parts: List[str] = []
    for index, card in enumerate(cards, start=1):
        if card.direction == EN2ZH:
            english, chinese = card.prompt, card.answer
        else:
            english, chinese = card.answer, card.prompt
        parts.append(
            "<div>%d. <span class=\"en\">%s</span> — %s</div>"
            % (index, html.escape(english), html.escape(chinese))
        )
    return "".join(parts)


__all__ = ["render_sheet"]
