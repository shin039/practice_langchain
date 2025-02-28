.PHONY: setup clean quick finish_reason help

setup:
	@echo "セットアップを開始します..."
	uv pip install -e .
	@echo "セットアップが完了しました"


clean:
	@echo "一時ファイルを削除しています..."
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf .pytest_cache
	@echo "クリーンアップが完了しました"

help:
	@echo "使用方法:"
	@echo "  make setup         - 必要なライブラリをインストールします"
	@echo "  make clean         - 一時ファイルを削除します"
	@echo "  make quick         - QuickStartを実行します"
	@echo "  make finish_reason - Finish Reasonの確認を実行します"

# QuickStart
quick:
	@echo "QuickStartを実行します..."
	uv run python -m src.evaluation.quickstart

finish_reason:
	@echo "Finish Reasonの確認を実行します..."
	uv run python -m src.prompt.finish_reason