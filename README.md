# LangChain 練習プロジェクト

このプロジェクトは、LangChainを使用した実験的な機能の実装と練習を行うためのリポジトリです。

## 要件

- Python 3.10以上
- OpenAI API キー

## セットアップ

1. 環境変数の設定:
   `.env.example` を `.env` にコピーし、必要なAPI キーを設定します。

   ```bash
   cp .env.example .env
   # .envファイルを編集してAPI キーを設定
   ```

2. 依存ライブラリのインストール:

   ```bash
   make setup
   ```

## 使用方法

### QuickStart

基本的な機能を試すには：

```bash
make quick
```

### Finish Reasonの確認

LLMの応答完了理由を確認するには：

```bash
make finish_reason
```

### クリーンアップ

一時ファイルを削除するには：

```bash
make clean
```

## プロジェクト構造

```
src/
├── __init__.py
├── evaluation/    - 評価関連の実装
└── prompt/        - プロンプト関連の実装
```

## 開発

このプロジェクトは `pyproject.toml` を使用してパッケージ管理を行っています。
依存関係の管理には `uv` を使用しています。

## トラブルシューティング

### モジュールが見つからないエラー

```
ModuleNotFoundError: No module named 'langchain'
```

このエラーが発生した場合は、以下の手順を試してください：

1. セットアップを再実行：
   ```bash
   make setup
   ```

2. 依存関係が正しくインストールされているか確認：
   ```bash
   uv pip list | grep langchain
   ```

### OpenAI API キーが見つからないエラー

```
エラー: OPENAI_API_KEYが設定されていません
```

`.env` ファイルに `OPENAI_API_KEY` が正しく設定されているか確認してください。