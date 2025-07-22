# 1週目 ユーティリティ開発カリキュラム

## 概要（7日間）
| Day | アプリ | 概要 |
| --- | --- | --- |
| 1 | 文字列反転 CLI | コマンドライン引数で受け取った文字列を逆順に表示（完了） |
| 2 | TODO リスト CLI | タスク追加・一覧をターミナルで操作 |
| 3 | 通貨換算ツール (Node.js) | 任意通貨→JPY などレート計算 |
| 4 | 天気取得スクリプト (Python) | OpenWeatherMap API で現在天気を表示 |
| 5 | Markdown→HTML 変換 (Node.js) | ファイル入力→HTML 出力 |
| 6 | ショートカット練習 | Cursor の Jump to Definition / AI Explain で既存コードをレビュー |
| 7 | 1週間振り返り | README 更新と振り返りメモ作成 |

---

## Day2 TODO リスト CLI 詳細
1. `todo_cli/` ディレクトリを作成し `main.py` 実装
   - `todo add "Buy milk"` でタスク追加
   - `todo list` で番号付きタスク一覧表示
2. pytest でテストケース追加
   - 追加後に一覧が期待どおりか確認
3. Cursor リファクタ提案を試す
   - コード選択 → Ctrl+K → AI: Fix / Improve Code
4. Git 操作
   ```bash
   git add .
   git commit -m "Day2: add todo_cli"
   git push
   ```
5. Obsidian に Day2 学習ログ作成 