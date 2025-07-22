import sys
import pathlib

# プロジェクトルートを Python パスに追加
project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import pytest

from reverse_string.main import reverse  # パッケージが見つからない場合でも動くようモジュールを明示


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("abc", "cba"),
        ("", ""),
        ("12345", "54321"),
    ],
)
def test_reverse(input_text: str, expected: str) -> None:
    """reverse 関数が正しく文字列を反転するか確認"""
    assert reverse(input_text) == expected 