# wordcard

[![CI](https://github.com/eastyou/wordcard/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/wordcard/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

把单词表 CSV 变成可打印的英语默写纸：看英文写中文、看中文写英文，或者两种交替；支持打乱顺序、切换 1~3 列，附参考答案页。**零依赖，不联网，单文件 HTML，A4 直接打印。**

老师用 Excel 维护单元单词，一条命令就能出一张默写纸，省去排版和复制粘贴。

## 特性

- **三种模式**：`en2zh` 看英文写中文、`zh2en` 看中文写英文、`mixed` 交替
- **可选打乱**：按种子打乱单词顺序
- **多列排版**：每行 1~3 列，单词多时更省纸
- **答案页**：附全部单词对照，可关闭
- **A4 打印**：卡片不跨页，答案另起一页
- **31 个单元测试**：CSV 校验、模式切换、HTML 输出与命令行

## 安装

```bash
pip install "git+https://github.com/eastyou/wordcard.git"
```

或者不安装，直接运行：

```bash
git clone https://github.com/eastyou/wordcard.git
cd wordcard
python3 -m wordcard -i examples/words.csv -o wordcard.html
```

## 单词表格式

CSV 表头（UTF-8）：

```csv
英文,中文
apple,苹果
book,书
```

- 表头必须有「英文」「中文」，允许额外的音标等列（会被忽略）
- 英文重复（不区分大小写）、单元格为空、列数不一致都会报错并指出行号
- 空行会被忽略

## 快速开始

生成看英文写中文的默写纸：

```console
$ wordcard -i examples/words.csv -o 默写纸.html
已生成 默写纸.html：12 个单词（看英文写中文），2 列
```

英中交替、三列、打乱顺序：

```console
$ wordcard -i examples/words.csv -o 默写纸.html --mode mixed --columns 3 --shuffle
已生成 默写纸.html：12 个单词（英中交替），3 列
```

浏览器打开后按 `Cmd/Ctrl + P`，选择 A4、纵向即可。

## 参数

| 参数 | 说明 |
| --- | --- |
| `-i, --input` | 单词表 CSV（必填） |
| `-o, --html` | 输出文件，默认 `wordcard.html` |
| `--title` | 页面标题，默认「英语单词默写」 |
| `--mode` | `en2zh` / `zh2en` / `mixed`，默认 `en2zh` |
| `--columns` | 每行几列，1~3，默认 2 |
| `--seed` | 随机种子，默认 2026 |
| `--shuffle` | 打乱单词顺序 |
| `--no-answers` | 不生成答案页 |

### 退出码

| 退出码 | 含义 |
| --- | --- |
| `0` | 成功 |
| `1` | 文件写入失败 |
| `2` | 单词表或参数有误 |

## 说明与边界

- 单词表必须是 UTF-8 编码；用 Excel 保存时选「CSV UTF-8」
- 每张卡片留两条横线，适合写单词或中文释义
- 暂不支持例句、图片和音标自动排版；额外列会被忽略

## 常见问题

**可以在手机上用吗？**
生成的 HTML 可以在手机浏览器打开，但排版是按 A4 设计的，打印效果最好。

**答案页能单独打印吗？**
答案页另起一页，可以在打印设置里选择页码范围，只打印前面部分。

**打乱后答案会乱吗？**
不会。卡片和答案使用同一份顺序，测试覆盖了这一点。

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
```

CI 覆盖 Python 3.9 ~ 3.13 与 Linux/macOS/Windows。

## License

[MIT](LICENSE) © 2026 eastyou
