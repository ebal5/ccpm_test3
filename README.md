# CCPM タスク管理ツール

Critical Chain Project Management (CCPM) の原則に基づいた個人向けタスク進捗・バッファ管理ツール。
プロジェクト管理、タスク追跡、時間管理、およびCCPM特有のバッファ管理機能を提供します。

## 機能概要

- タスクの作成、編集、削除、ステータス管理
- 50%確率見積りの入力と実績工数の記録
- クリティカルチェーンの識別と表示
- プロジェクトバッファの管理
- バッファ消費率の計算と表示（緑/黄/赤の3段階）
- 時間トラッキング（開始/停止機能）

## 開発環境のセットアップ

### 前提条件

- Python 3.12以上

### インストール手順

```bash
# リポジトリのクローン
git clone https://github.com/ebal5/ccpm_test3.git
cd ccpm_test3

# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate

# 依存関係のインストール
pip install -e ".[dev]"
```

### 開発用コマンド

```bash
# アプリケーションの実行
python -m ccpm.app

# テストの実行
pytest

# コードフォーマット
ruff format .

# リンター実行
ruff check .

# 型チェック
mypy ccpm
```

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。