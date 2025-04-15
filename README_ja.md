[English](README.md) | 中国語 | [한국어](README_ko.md) | [日本語](README_ja.md)

[![GitHub stars](https://img.shields.io/github/stars/mannaandpoem/OpenManus?style=social)](https://github.com/mannaandpoem/OpenManus/stargazers)
&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &ensp;
[![Discord Follow](https://dcbadge.vercel.app/api/server/DYn29wFk9z?style=flat)](https://discord.gg/DYn29wFk9z)

# 👋 AskManus

OpenManusに基づいて提供しています：
- インストールスクリプト
- ユーザーの発言後に必要に応じてコマンドラインで選択肢を表示し、各選択肢に必要に応じて説明を付加します

## インストールガイド

2つのインストール方法を提供します。方法2（uv）が推奨されます（より高速なインストールと依存関係管理が可能です）。

### 方法1：condaを使用

1. 新しいconda環境を作成：

```bash
conda create -n open_manus python=3.12
conda activate open_manus
```

2. リポジトリをクローン：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3. 依存関係をインストール：

```bash
pip install -r requirements.txt
```

### 方法2：uvを使用（推奨）

1. uv（高速Pythonパッケージマネージャー）をインストール：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. リポジトリをクローン：

```bash
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus
```

3.仮想環境を作成して有効化：

```bash
uv venv --python 3.12
source .venv/bin/activate  # Unix/macOSの場合
# Windowsの場合：
# .venv\Scripts\activate
```

4.依存関係をインストール：

```bash
uv pip install -r requirements.txt
```

### ブラウザ自動化ツール（オプション）

```bash
playwright install
```

## 設定ガイド

AskManusは使用するLLM APIの設定が必要です。以下の手順で設定してください：

1. `config`ディレクトリに`config.toml`ファイルを作成（例からコピー）：

```bash
cp config/config.example.toml config/config.toml
```

2. `config/config.toml`を編集し、APIキーとカスタム設定を追加：

```toml
# 全体のLLM設定
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 実際のAPIキーに置換
max_tokens = 4096
temperature = 0.0

# 特定LLMモデルの設定（オプション）
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # 実際のAPIキーに置換
```

## クイックスタート

一行コマンドでAskManusを実行：

```bash
python main.py
```

その後、ターミナルでアイデアを入力できます！

MCPツールバージョンを使用する場合は：
```bash
python run_mcp.py
```

不安定なマルチエージェントバージョンを体験する場合は：
```bash
python run_flow.py
```

## コントリビューションガイド

友好的な提案や価値あるコントリビューションを歓迎します！Issueの作成やPull Requestの送信が可能です。

**注意**: Pull Requestを送信する前に、`pre-commit run --all-files`で変更内容をチェックしてください。

## コミュニティ

## スター数推移

[![Star History Chart](https://api.star-history.com/svg?repos=mannaandpoem/OpenManus&type=Date)](https://star-history.com/#mannaandpoem/OpenManus&Date)

## クレジット

本プロジェクトはOpenManusに基づいています。特別に[OpenManus](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)が提供した基盤技術に感謝します！
