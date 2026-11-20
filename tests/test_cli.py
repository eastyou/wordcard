from __future__ import annotations

import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from wordcard.cli import main


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.input = os.path.join(self._tmp.name, "words.csv")
        with open(self.input, "w", encoding="utf-8") as handle:
            handle.write("英文,中文\napple,苹果\nbook,书\ncat,猫\n")
        self.output = os.path.join(self._tmp.name, "cards.html")

    def run_cli(self, args):
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_generate(self) -> None:
        code, output, _ = self.run_cli(
            ["-i", self.input, "-o", self.output]
        )
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(self.output))
        self.assertIn("3 个单词", output)

    def test_mode_and_columns(self) -> None:
        code, _, _ = self.run_cli(
            [
                "-i",
                self.input,
                "-o",
                self.output,
                "--mode",
                "mixed",
                "--columns",
                "3",
            ]
        )
        self.assertEqual(code, 0)
        with open(self.output, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("repeat(3, minmax(0, 1fr))", content)
        self.assertIn("英→中", content)

    def test_no_answers(self) -> None:
        code, _, _ = self.run_cli(
            ["-i", self.input, "-o", self.output, "--no-answers"]
        )
        self.assertEqual(code, 0)
        with open(self.output, encoding="utf-8") as handle:
            self.assertNotIn("参考答案", handle.read())

    def test_missing_file(self) -> None:
        code, _, stderr = self.run_cli(
            ["-i", "/tmp/not-here-98765.csv", "-o", self.output]
        )
        self.assertEqual(code, 2)
        self.assertIn("不存在", stderr)

    def test_invalid_columns(self) -> None:
        code, _, stderr = self.run_cli(
            ["-i", self.input, "-o", self.output, "--columns", "4"]
        )
        self.assertEqual(code, 2)
        self.assertIn("列数", stderr)

    def test_empty_title(self) -> None:
        code, _, stderr = self.run_cli(
            ["-i", self.input, "-o", self.output, "--title", " "]
        )
        self.assertEqual(code, 2)
        self.assertIn("标题", stderr)

    def test_write_failure(self) -> None:
        bad = os.path.join(self._tmp.name, "missing", "cards.html")
        code, _, stderr = self.run_cli(["-i", self.input, "-o", bad])
        self.assertEqual(code, 1)
        self.assertIn("写入文件失败", stderr)


if __name__ == "__main__":
    unittest.main()
